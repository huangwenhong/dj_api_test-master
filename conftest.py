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
# cpsol.net 的 token 存储，由 auto_login 填充
cpsol_token = {}

# smart.onlinecps.cn 域名登录配置（智能体模块使用-预发布环境）
SMART_BASE_URL = "https://smart.onlinecps.cn"
# smart.onlinecps.cn 的 token 存储，由 auto_login 填充
smart_token = {}

# smart.cpsol.net 域名登录配置（产品上架模块使用）
SMART_CPSOL_BASE_URL = "https://smart.cpsol.net"
# smart.cpsol.net 的 token 存储，由 auto_login 填充
smart_cpsol_token = {}

# oatest.cpsol.net 域名登录配置（签到模块使用-阿里云环境）
OATEST_CPSOL_BASE_URL = "https://oatest.cpsol.net"
# oatest.cpsol.net 的 token 存储，由 auto_login 填充
oatest_token = {}

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
    """每次执行用例前自动登录，获取新 token 并更新 config.default_cookies。"""
    from test_case.page_api.public.login_api import LoginAPI

    if not LOGIN_USERNAME or not LOGIN_PASSWORD:
        pytest.exit("请先设置 API_TEST_USERNAME 和 API_TEST_PASSWORD 环境变量。", returncode=4)
    if urlparse(config.base_url).hostname == "example.invalid":
        pytest.exit("请先设置 API_TEST_BASE_URL 环境变量或配置 config.base_url。", returncode=4)

    # 1. 主域名登录（后端 IP 直连时 IP 不提供 CAS 登录，按抓包改走 cpsol.net 登录域名）
    login_base_url = CPSOL_BASE_URL if _is_ip_host(config.base_url) else config.base_url
    api = LoginAPI(base_url=login_base_url)
    token, details = api.login(LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_APP_NAME)

    if not token:
        pytest.exit(f"登录失败，无法获取 token，终止测试执行。\n详情: {details}")

    # 更新 config 中的 default_cookies，后续所有接口自动携带新 token
    config.default_cookies["token"] = token
    print(f"\n[auto_login] {login_base_url} 登录成功")

    # 2. cpsol.net 域名登录（履约模块使用）
    try:
        cpsol_api = LoginAPI(base_url=CPSOL_BASE_URL)
        cpsol_tok, cpsol_details = cpsol_api.login(LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_APP_NAME)
        if cpsol_tok:
            cpsol_token["token"] = cpsol_tok
            print("[auto_login] cpsol.net 登录成功")
        else:
            print(f"[auto_login] cpsol.net 登录失败: {cpsol_details}")
    except Exception as e:
        print(f"[auto_login] cpsol.net 登录异常: {e}")

    # 3. smart.onlinecps.cn 域名登录（智能体模块使用）
    try:
        smart_api = LoginAPI(base_url=SMART_BASE_URL)
        smart_tok, smart_details = smart_api.login(LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_APP_NAME)
        if smart_tok:
            smart_token["token"] = smart_tok
            print("[auto_login] smart.onlinecps.cn 登录成功")
        else:
            print(f"[auto_login] smart.onlinecps.cn 登录失败: {smart_details}")
    except Exception as e:
        print(f"[auto_login] smart.onlinecps.cn 登录异常: {e}")

    # 4. smart.cpsol.net 域名登录（产品上架模块使用，阿里云环境）
    # 阿里云环境 exchangetoken 可能失败，改用 casToken 作为认证
    try:
        smart_cpsol_api = LoginAPI(base_url=SMART_CPSOL_BASE_URL)
        # 先尝试标准登录流程
        smart_cpsol_tok, smart_cpsol_details = smart_cpsol_api.login(LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_APP_NAME)
        if smart_cpsol_tok:
            smart_cpsol_token["token"] = smart_cpsol_tok
            print("[auto_login] smart.cpsol.net 登录成功")
        else:
            # 阿里云环境回退：使用 casToken 作为认证
            cas_token = smart_cpsol_api.session.cookies.get("casToken", "")
            if cas_token:
                smart_cpsol_token["token"] = cas_token
                print("[auto_login] smart.cpsol.net 使用 casToken 登录")
            else:
                print(f"[auto_login] smart.cpsol.net 登录失败: {smart_cpsol_details}")
    except Exception as e:
        print(f"[auto_login] smart.cpsol.net 登录异常: {e}")

    # 5. oatest.cpsol.net 域名登录（签到模块使用，阿里云环境）
    try:
        oatest_api = LoginAPI(base_url=OATEST_CPSOL_BASE_URL)
        oatest_tok, oatest_details = oatest_api.login(LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_APP_NAME)
        if oatest_tok:
            oatest_token["token"] = oatest_tok
            print("[auto_login] oatest.cpsol.net 登录成功")
        else:
            # 阿里云环境回退：使用 casToken 作为认证
            cas_token = oatest_api.session.cookies.get("casToken", "")
            if cas_token:
                oatest_token["token"] = cas_token
                print("[auto_login] oatest.cpsol.net 使用 casToken 登录")
            else:
                print(f"[auto_login] oatest.cpsol.net 登录失败: {oatest_details}")
    except Exception as e:
        print(f"[auto_login] oatest.cpsol.net 登录异常: {e}")

    # 6. aiagent.djcps.com 域名（市场分析智能体，token 由外部提供）
    if not corrusense_token.get("token"):
        corrusense_token["token"] = os.getenv("API_TEST_AIAGENT_TOKEN", "")
        if corrusense_token["token"]:
            print("[auto_login] aiagent.djcps.com 已配置外部 token")
