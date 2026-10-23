import os
import pytest
from urllib.parse import urlparse

import config

# 登录账号配置，按需修改
LOGIN_USERNAME = os.getenv("API_TEST_USERNAME", "")
LOGIN_PASSWORD = os.getenv("API_TEST_PASSWORD", "")
LOGIN_APP_NAME = "DJSUPPLIER"

# cpsol.net 域名登录配置（履约模块使用-测试环境）
CPSOL_BASE_URL = "https://suppliertest.cpsol.net"


class _LazyTokenDict(dict):
    """按需登录的 token 容器：首次 get("token") 为空时同步触发对应域名登录。

    设计目的：避免 auto_login 在会话开始时对全部域名登录（5 组三步登录），
    改为接口方法首次读取对应 token 时才登录，减少不必要的登录请求。
    接口方法代码无需改动（仍然调用 conftest.xxx_token.get("token", "")）。
    """

    def __init__(self, name, base_url, fallback_cas_token=False):
        super().__init__()
        self._name = name
        self._base_url = base_url
        self._fallback_cas_token = fallback_cas_token
        self._loaded = False

    def _load(self):
        if self._loaded:
            return
        self._loaded = True
        from test_case.page_api.public.login_api import LoginAPI

        try:
            api = LoginAPI(base_url=self._base_url)
            tok, details = api.login(LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_APP_NAME)
            if tok:
                self["token"] = tok
                print(f"[auto_login] {self._name} 登录成功（按需）")
            elif self._fallback_cas_token:
                cas = api.session.cookies.get("casToken", "")
                if cas:
                    self["token"] = cas
                    print(f"[auto_login] {self._name} 使用 casToken 登录（按需）")
                else:
                    print(f"[auto_login] {self._name} 登录失败: {details}")
            else:
                print(f"[auto_login] {self._name} 登录失败: {details}")
        except Exception as e:
            print(f"[auto_login] {self._name} 登录异常: {e}")

    def get(self, key, default=None):
        if key == "token":
            self._load()
        return super().get(key, default)

    def __getitem__(self, key):
        if key == "token":
            self._load()
        return super().__getitem__(key)


# cpsol.net 的 token 存储，由接口方法首次读取时按需登录填充
cpsol_token = _LazyTokenDict("cpsol.net", CPSOL_BASE_URL)

# ==================== 阿里云后端 IP 直连登录说明 ====================
# 所有 IP 直连模式的登录统一回退到 CPSOL_BASE_URL（测试环境）。
# 当前已确认的直连服务端口（测试环境推断，待 k8s 命名空间确认）：
#   DJEASYORDER      → http://172.31.0.16:31086  (TCP已验证，测试环境)
#   djcockpit        → http://172.31.0.16:32221  (TCP已验证，测试环境)
#   djfinancemanage  → http://172.31.0.16:30852  (已在核价用例全量验证，测试环境)
# 环境归属依据：上述服务在现有用例中均走 suppliertest 系列域名登录。
# 预发布环境端口可能不同，未确认前必须通过环境变量覆盖，不得复用上述测试端口值。
# 执行前必须开启 VPN，否则 172.31.0.0/16 私网不可达。
# ==========================================================

# smart.onlinecps.cn 域名登录配置（智能体模块使用-预发布环境）
SMART_BASE_URL = "https://smart.onlinecps.cn"
# smart.onlinecps.cn 的 token 存储，由接口方法首次读取时按需登录填充
smart_token = _LazyTokenDict("smart.onlinecps.cn", SMART_BASE_URL)

# smart.cpsol.net 域名登录配置（产品上架模块使用）
SMART_CPSOL_BASE_URL = "https://smart.cpsol.net"
# smart.cpsol.net 的 token 存储，由接口方法首次读取时按需登录填充（阿里云环境回退 casToken）
smart_cpsol_token = _LazyTokenDict("smart.cpsol.net", SMART_CPSOL_BASE_URL, fallback_cas_token=True)

# oatest.cpsol.net 域名登录配置（签到模块使用-阿里云环境）
OATEST_CPSOL_BASE_URL = "https://oatest.cpsol.net"
# oatest.cpsol.net 的 token 存储，由接口方法首次读取时按需登录填充（阿里云环境回退 casToken）
oatest_token = _LazyTokenDict("oatest.cpsol.net", OATEST_CPSOL_BASE_URL, fallback_cas_token=True)

# aiagent.djcps.com 域名配置（市场分析智能体使用）
AIAGENT_BASE_URL = "https://aiagent.djcps.com"
# aiagent.djcps.com 的 token 存储，由外部提供
corrusense_token = {}


def _is_ip_host(url):
    """判断 base_url 是否为后端 IP 直连（IP 服务不提供 CAS 登录和网关前缀）。"""
    host = urlparse(url).hostname or ""
    return bool(host) and host.replace(".", "").isdigit()


def pytest_addoption(parser):
    """注册 pytest 命令行参数。
    这些参数用于在不修改 config.py 的情况下覆盖运行环境配置，
    适合本地调试、CI 多环境执行或临时切换被测站点。
    """
    # --base-url 用于临时覆盖 config.base_url，常用于切换测试环境域名。
    parser.addoption("--base-url", action="store", default=None, help="override config.base_url")

    # --website-name 用于覆盖 Allure 报告中的网站/项目名称展示。
    parser.addoption("--website-name", action="store", default=None, help="override Allure epic website name")


def pytest_collection_modifyitems(config, items):
    """用户要求：跳过的用例不执行、不统计。

    collect 后 deselect 带 skip / skipif marker 的用例（静态跳过），
    使其不进入执行阶段、也不出现在报告统计中。
    动态跳过（用例内 pytest.skip()）无法在 collect 阶段预知，
    仍会执行到 skip 调用点，但报告生成时会过滤不统计。
    """
    deselected = []
    kept = []
    for item in items:
        if item.get_closest_marker("skip") or item.get_closest_marker("skipif"):
            deselected.append(item)
        else:
            kept.append(item)
    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = kept
        print(
            f"\n[conftest] 已 deselect {len(deselected)} 个带 skip marker 的用例"
            f"（不执行、不统计）: {[i.name for i in deselected]}"
        )


@pytest.fixture(scope="session")
def base_url(request):
    """返回当前测试会话使用的 base_url。
    优先级：
    1. pytest 命令行传入的 --base-url。
    2. config.py 中配置的 base_url。
    返回前会调用 config.validate_base_url 校验 URL 必须包含协议和域名。
    """
    # pytest 命令行参数优先级高于配置文件，便于同一套用例在不同环境执行。
    return config.validate_base_url(request.config.getoption("--base-url") or config.base_url)


@pytest.fixture(scope="session")
def website_name(request, base_url):
    """返回 Allure 报告中使用的网站名称。
    优先级：
    1. pytest 命令行传入的 --website-name。
    2. config.py 中配置的 website_name。
    3. 从 base_url 中解析出的域名。
    """
    # base_url 作为兜底输入，保证未显式配置网站名称时仍能生成可读的报告标题。
    return config.get_website_name(request.config.getoption("--website-name"), base_url)


@pytest.fixture(scope="session", autouse=True)
def auto_login():
    """每次执行用例前自动登录主域名，获取新 token 并更新 config.default_cookies。

    其他域名（cpsol.net / smart.onlinecps.cn / smart.cpsol.net / oatest.cpsol.net）
    改为按需登录：接口方法首次读取对应 token 容器时由 _LazyTokenDict 同步触发。
    """
    from test_case.page_api.public.login_api import LoginAPI

    if not LOGIN_USERNAME or not LOGIN_PASSWORD:
        pytest.exit("请先设置 API_TEST_USERNAME 和 API_TEST_PASSWORD 环境变量。", returncode=4)
    if _is_ip_host(config.base_url):
        print(
            f"\n[auto_login] 已启用阿里云后端 IP 直连：{config.base_url}；"
            f"登录域名={CPSOL_BASE_URL}。请确认 VPN 已开启。"
        )
    elif urlparse(config.base_url).hostname == "example.invalid":
        pytest.exit("请先设置 API_TEST_BASE_URL 环境变量或配置 config.base_url。", returncode=4)

    # 主域名登录（后端 IP 直连时 IP 不提供 CAS 登录，按抓包改走 cpsol.net 登录域名）
    login_base_url = CPSOL_BASE_URL if _is_ip_host(config.base_url) else config.base_url
    api = LoginAPI(base_url=login_base_url)
    token, details = api.login(LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_APP_NAME)

    if not token:
        pytest.exit(f"登录失败，无法获取 token，终止测试执行。\n详情: {details}")

    # 更新 config 中的 default_cookies，后续所有接口自动携带新 token
    config.default_cookies["token"] = token
    print(f"\n[auto_login] {login_base_url} 登录成功")

    # aiagent.djcps.com 域名（市场分析智能体，token 由外部提供）
    if not corrusense_token.get("token"):
        corrusense_token["token"] = os.getenv("API_TEST_AIAGENT_TOKEN", "")
        if corrusense_token["token"]:
            print("[auto_login] aiagent.djcps.com 已配置外部 token")
