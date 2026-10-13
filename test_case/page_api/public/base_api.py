"""接口请求基类模块。

本模块提供 BaseAPI，作为所有 page_api 接口封装类的公共父类。
它统一处理 base_url 拼接、requests.Session 初始化、默认 headers/cookies/proxies、
HTTP 状态码断言、JSON 响应解析，以及接口用例中常用的多层数据取值能力。
"""

import json

import config
import allure
from urllib.parse import urlparse
from utils.timeout_http_adapter import create_http_session


class BaseAPI:
    """接口封装层公共基类。

    业务接口类应继承该类，并通过 self.get/self.post/self.put/self.delete
    发送请求。这样可以复用统一的超时、代理、证书、断言和响应解析逻辑，
    避免在每个接口方法中重复创建 session 或手写状态码断言。
    """

    def __init__(
        self,
        base_url=None,
        headers=None,
        cookies=None,
        timeout=None,
        verify_ssl=None,
        proxies=None,
    ):
        """初始化接口请求上下文。
        Args:
            base_url: 被测系统基础地址；不传时使用 config.base_url。
            headers: 本接口类额外请求头，会与 config.default_headers 合并。
            cookies: 本接口类额外 cookies，会与 config.default_cookies 合并。
            timeout: 默认请求超时时间；不传时使用 config.timeout。
            verify_ssl: 是否校验 HTTPS 证书；不传时使用 config.verify_ssl。
            proxies: requests 代理配置；不传时使用 config.proxies。
        """
        # 校验并规范化 base_url，保证后续 URL 拼接时基础地址合法。
        self.base_url = config.validate_base_url(base_url or config.base_url)

        # 默认 headers/cookies 作为基础配置，调用方传入的值拥有更高优先级。
        self.headers = {**config.default_headers, **(headers or {})}
        self._extra_cookies = cookies or {}
        self.cookies = {**config.default_cookies, **self._extra_cookies}

        # timeout 支持按接口类覆盖；未覆盖时使用全局配置。
        self.timeout = timeout or config.timeout

        # verify_ssl 支持显式传 False，因此必须用 is None 判断是否采用配置默认值。
        self.verify_ssl = config.verify_ssl if verify_ssl is None else verify_ssl

        # proxies 允许显式传空字典关闭代理，因此使用 is not None 判断。
        self.proxies = proxies if proxies is not None else config.proxies

        # 判断是否为阿里云后端 IP 直连模式。
        # 全局开关：当 config.base_url 为 IP 时，所有接口实例（含自有域名默认值的子类）均启用路由。
        # 实例级开关：当子类 __init__ 显式传入 IP base_url 时也同样启用。
        # IP 模式下 BaseAPI.build_url 自动剥除网关前缀并按服务上下文路由到对应端口。
        def _is_ip(url):
            h = urlparse(url).hostname or ""
            return bool(h) and h.replace(".", "").isdigit()
        self.direct_mode = _is_ip(config.base_url) or _is_ip(self.base_url)

        # requests.Session 延迟初始化，只有真正发送请求时才创建。
        self.base_request = None

    @classmethod
    def http_timeout(
        cls,
        timeout=None,
        verify_ssl=None,
        headers=None,
        cookies=None,
        proxies=None,
    ):
        """创建带超时适配器的 requests.Session。
        Args:
            timeout: 默认请求超时时间。
            verify_ssl: 是否校验 HTTPS 证书。
            headers: 需要合并到 session 的请求头。
            cookies: 需要合并到 session 的 cookies。
            proxies: requests 代理配置。
        Returns:
            requests.Session | TimeoutCurlCffiSession: 已配置好的 session。
        """
        return create_http_session(
            timeout=timeout or config.timeout,
            verify_ssl=verify_ssl,
            headers=headers,
            cookies=cookies,
            proxies=proxies,
            use_curl_cffi=config.use_curl_cffi,
            curl_impersonate=config.curl_impersonate,
        )

    def get_base_request(self):
        """获取当前接口类复用的 requests.Session。
        Returns:
            requests.Session: 当前 BaseAPI 实例持有的 session。
        """
        # session 采用懒加载，避免只实例化接口类但不发请求时创建无用连接对象。
        # 每次获取时同步 config.default_cookies，确保 auto_login 更新 token 后能生效。
        self.cookies = {**config.default_cookies, **(self._extra_cookies or {})}
        if self.base_request is None:
            self.base_request = self.http_timeout(
                timeout=self.timeout,
                verify_ssl=self.verify_ssl,
                headers=self.headers,
                cookies=self.cookies,
                proxies=self.proxies,
            )
        else:
            # session 已存在时，同步更新其 cookies 以获取最新 token。
            for k, v in self.cookies.items():
                self.base_request.cookies.set(k, v)
        return self.base_request

    # 网关路径上下文（第一个路径段）对应 config.SVC_PORTS 键名。
    # 新增服务时在此登记；未登记的服务会打印警告并使用 self.base_url 兆底。
    _DIRECT_ROUTE_MAP: dict = {
        "DJEASYORDER": "DJEASYORDER",
        "djfinancemanage": "djfinancemanage",
        "djcockpit": "djcockpit",
        # 以下服务待确认端口后按格式添加：
        # "oms":               "DJEASYORDER",   # TODO: 确认 OMS 服务端口
        # "marketingActivity": "DJEASYORDER",   # TODO: 确认 marketingActivity 服务端口
        # "orderManager":      "DJEASYORDER",   # TODO: 确认 orderManager 服务端口
        # "analysis":          "djcockpit",     # TODO: 确认 analysis 服务端口
        # "product":           "DJEASYORDER",   # TODO: 确认 product 服务端口
    }

    def build_url(self, path_or_url):
        """根据相对路径或完整 URL 构造最终请求 URL。

        IP 直连模式（self.direct_mode=True）时：
        1. 剥除网关前缀 /djsupplier[/app]。
        2. 按剩作路径的第一个段匹配服务上下文，路由到 config.svc_url() 对应的端口。
        3. 未匹配的服务上下文会输出警告并退回到标准 base_url 拼接。

        域名模式时行为不变，直接拼接 self.base_url + 相对路径。

        Args:
            path_or_url: 接口相对路径，或已经包含协议和域名的完整 URL。
        Returns:
            str: 可直接用于 requests 请求的完整 URL。
        """
        full = str(path_or_url)
        parsed = urlparse(full)
        # 已是完整 URL（包含协议和域名），直接返回。
        if parsed.scheme and parsed.netloc:
            return full

        # IP 直连模式：剥除网关前缀，按服务上下文路由到对应端口。
        if self.direct_mode:
            stripped = full
            # 剥除优先级：/djsupplier/app 比 /djsupplier 更具体，必须优先匹配。
            for gw in ("/djsupplier/app", "/djsupplier"):
                if stripped.startswith(gw):
                    stripped = stripped[len(gw):]
                    break
            # 取剥除后的第一个路径段作为服务上下文标识。
            ctx = stripped.lstrip("/").split("/")[0] if stripped else ""
            svc_key = self._DIRECT_ROUTE_MAP.get(ctx)
            if svc_key:
                return config.svc_url(svc_key) + stripped
            # 未注册的服务：输出警告并使用 self.base_url 拼接，避免默默发出错误请求。
            import sys
            print(
                f"[BaseAPI direct_mode WARN] 服务上下文 '{ctx}' 未在 _DIRECT_ROUTE_MAP 中注册，"
                f"将使用 self.base_url={self.base_url} 拼接。"
                f"请在 config.SVC_PORTS 中确认并添加对应端口。原始路径={full}",
                file=sys.stderr,
            )

        # 标准路径拼接（域名模式或 IP 模式下的未匹配上下文）。
        base = self.base_url.rstrip("/")
        path = full.lstrip("/")
        return f"{base}/{path}" if path else base

    @allure.step("发送接口请求")
    def request(self, method, path_or_url, status_code=200, return_response=False, error_msg=None, **kwargs):
        """发送接口请求并统一断言 HTTP 状态码。
        Args:
            method: HTTP 方法，如 GET、POST、PUT、DELETE。
            path_or_url: 接口相对路径或完整 URL。
            status_code: 期望 HTTP 状态码，默认 200。
            return_response: 是否返回原始 Response；False 时默认返回 response.json()。
            error_msg: 断言失败或 JSON 解析失败时使用的中文错误说明。
            **kwargs: 传给 requests 的请求参数，如 params、json、data、headers 等。
        Returns:
            dict | list | requests.Response: 默认返回 JSON 解析结果；return_response=True 时返回原始响应。
        """
        # 统一在基类中构造完整 URL，接口方法只需传相对路径即可。
        url = self.build_url(path_or_url)

        # 通过复用 session 发送请求，继承统一 headers、cookies、timeout、proxies 等配置。
        response = self.get_base_request().request(method.upper(), url, **kwargs)

        # error_msg 可由接口方法传入，用于让失败日志更贴近业务接口含义。
        message = error_msg or f"接口<{url}>请求失败"

        # 接口方法层只断言 HTTP 状态码，业务 code 断言应放在 pytest 用例层处理。
        # status_code=0 表示跳过状态码检查，由调用方自行处理
        if status_code != 0:
            assert response.status_code == status_code, (
                f"{message},接口<{url}>报错-{response.status_code},"
                f"reason:{response.reason},text:{response.text}"
            )

        # 非 JSON、下载、重定向等特殊场景可要求返回原始 response。
        if return_response:
            # 记录原始响应文本到 Allure
            allure.attach(
                response.text[:5000],
                name="响应内容",
                attachment_type=allure.attachment_type.TEXT,
            )
            return response
        try:
            # 默认返回 JSON 结果，方便用例直接基于响应数据做断言。
            json_result = response.json()
            # 将 JSON 响应格式化后附加到 Allure 报告
            allure.attach(
                json.dumps(json_result, ensure_ascii=False, indent=2)[:5000],
                name="响应内容",
                attachment_type=allure.attachment_type.JSON,
            )
            return json_result
        except ValueError as exc:
            # 接口声明应返回 JSON 但实际不是 JSON 时，抛出带响应文本的断言错误。
            allure.attach(
                response.text[:5000],
                name="响应内容(非JSON)",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise AssertionError(f"{message},接口<{url}>返回不是合法 JSON,text:{response.text}") from exc

    def get(self, path_or_url, **kwargs):
        """发送 GET 请求。
        Args:
            path_or_url: 接口相对路径或完整 URL。
            **kwargs: 传给 request 的请求参数。
        Returns:
            dict | list | requests.Response: 默认返回 JSON 解析结果。
        """
        return self.request("GET", path_or_url, **kwargs)

    def post(self, path_or_url, **kwargs):
        """发送 POST 请求。
        Args:
            path_or_url: 接口相对路径或完整 URL。
            **kwargs: 传给 request 的请求参数。
        Returns:
            dict | list | requests.Response: 默认返回 JSON 解析结果。
        """
        return self.request("POST", path_or_url, **kwargs)

    def put(self, path_or_url, **kwargs):
        """发送 PUT 请求。
        Args:
            path_or_url: 接口相对路径或完整 URL。
            **kwargs: 传给 request 的请求参数。
        Returns:
            dict | list | requests.Response: 默认返回 JSON 解析结果。
        """
        return self.request("PUT", path_or_url, **kwargs)

    def delete(self, path_or_url, **kwargs):
        """发送 DELETE 请求。
        Args:
            path_or_url: 接口相对路径或完整 URL。
            **kwargs: 传给 request 的请求参数。
        Returns:
            dict | list | requests.Response: 默认返回 JSON 解析结果。
        """
        return self.request("DELETE", path_or_url, **kwargs)

    def get_value(self, data, list_key=None, **kwargs):
        """按路径从嵌套数据中取值。
        Args:
            data: 原始数据，通常为接口响应 JSON。
            list_key: 取值路径；可以是单个 key，也可以是 key/index 组成的列表。
            **kwargs: 可传入 msg 作为断言失败时的额外说明。
        Returns:
            Any: 按路径取出的目标值。
        Raises:
            AssertionError: 路径不存在或取值失败时抛出。
        """
        # 未传 list_key 时，默认按 ["data", "data"] 取值，兼容常见响应结构。
        keys = ["data", "data"] if list_key is None else list_key

        # 单个 key 自动转成列表，统一后续遍历逻辑。
        if not isinstance(keys, list):
            keys = [keys]

        # 保留原始数据和当前 key，便于失败时输出可定位的信息。
        original_data = data
        key = ""
        try:
            for key in keys:
                # key 可以是字典 key，也可以是列表 index，按调用方传入路径逐层取值。
                data = data[key]
            return data
        except Exception as exc:
            # 取值失败时抛 AssertionError，让 pytest 直接展示清晰失败原因。
            msg = f"数据{data}不存在取值'{key}'！原始数据:{original_data};"
            if kwargs.get("msg"):
                msg = f"{kwargs.get('msg')}:{msg}"
            raise AssertionError(msg) from exc
