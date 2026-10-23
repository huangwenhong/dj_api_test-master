# -*- coding: utf-8 -*-
"""公共模块 - CAS 单点登录接口用例（复用 test_case/page_api/public/login_api.py）

登录链路（三步）：
    1. weblogin.do       → 用账号密码换取 onceToken（密码 MD5 由 LoginAPI 内部处理）
    2. casTokenLogin.do  → 用 onceToken 换取业务 token
    3. exchangetoken.do  → 用 onceToken 换取最终 token（Set-Cookie 落地到 session）

设计说明：
    - conftest.auto_login 是 session-scope autouse fixture，会在会话开始时完成一次全量登录，
      并把 token 写入 config.default_cookies；本用例聚焦"CAS 三步接口链路本身能否跑通"，
      因此显式再走一次 web_login → cas_token_login → exchange_token，并交叉验证 login() 主流程。
    - 登录域名解析规则与 conftest.auto_login 保持一致：config.base_url 为 IP 直连时回退 CPSOL 域名。
"""

import re
from pathlib import Path

import allure
import pytest

import config
from conftest import (
    CPSOL_BASE_URL,
    LOGIN_APP_NAME,
    LOGIN_PASSWORD,
    LOGIN_USERNAME,
    _is_ip_host,
)
from test_case.page_api.public.login_api import LoginAPI, login_and_update_config


def _resolve_login_base_url():
    """与 conftest.auto_login 保持一致：IP 直连场景登录回退到 CPSOL 域名。"""
    return CPSOL_BASE_URL if _is_ip_host(config.base_url) else config.base_url


def _require_credentials():
    """前置：账号密码必须就绪，否则跳过（conftest.auto_login 已在会话级兜底 exit）。"""
    if not LOGIN_USERNAME or not LOGIN_PASSWORD:
        pytest.skip("未设置 API_TEST_USERNAME / API_TEST_PASSWORD 环境变量，跳过 CAS 登录用例")


def _login_step_ok(res, step_name):
    """校验 CAS 单步接口返回结构：必须是 dict 且至少带 code 或 success 字段。"""
    assert isinstance(res, dict), \
        f"{step_name} 返回不是 dict, 实际类型={type(res).__name__}, 值={res}"
    assert res.get("code") is not None or res.get("success") is not None, \
        f"{step_name} 返回既无 code 也无 success, 接口返回={res}"


def _extract_once_token(weblogin_resp):
    """从 weblogin 响应中提取 onceToken（可能落在 data.url 查询串、data.onceToken 或顶层）。

    与 LoginAPI.login() 内部提取逻辑保持一致，用于单步验证场景。
    """
    if not isinstance(weblogin_resp, dict):
        return ""
    data = weblogin_resp.get("data") or {}
    if isinstance(data, dict):
        url = data.get("url") or ""
        m = re.search(r"onceToken=([^&]+)", url)
        if m:
            return m.group(1)
        tok = data.get("onceToken") or data.get("token") or ""
        if tok:
            return tok
    return weblogin_resp.get("onceToken") or weblogin_resp.get("token") or ""


# ==================== 公共-CAS 登录 ====================

@allure.feature("公共-CAS登录")
class TestCasLogin:

    @allure.story("CAS 三步登录成功获取 token")
    def test_public_LOGIN_cas_three_steps_success(self):
        """CAS 三步登录成功获取 token：weblogin → casTokenLogin → exchangetoken → session token 落地"""
        # Author: Author
        # Create Date: 2026-10-20
        # IsAI: True

        # 1. 前置：凭据校验 + 决定登录域名（IP 直连时回退到 CPSOL 域名，与 auto_login 一致）
        _require_credentials()
        login_base_url = _resolve_login_base_url()
        api = LoginAPI(base_url=login_base_url)

        # 2. 第一步 weblogin：用账号密码换取 onceToken（密码 MD5 加密由 LoginAPI 内部完成）
        r1 = api.web_login(LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_APP_NAME)
        _login_step_ok(r1, "weblogin")
        assert r1.get("success") is True, \
            f"weblogin success 不为 True（凭据可能无效或账号锁定）, 接口返回={r1}"

        # 3. 从 weblogin 响应中提取 onceToken（可能落在 data.url 查询串或 data.onceToken）
        once_token = _extract_once_token(r1)
        assert once_token, f"weblogin 未返回 onceToken, 接口返回={r1}"

        # 4. 第二步 casTokenLogin：用 onceToken 换取业务 token
        r2 = api.cas_token_login(LOGIN_APP_NAME, once_token)
        _login_step_ok(r2, "casTokenLogin")

        # 5. 第三步 exchangetoken：用 onceToken 换取最终 token
        r3 = api.exchange_token(once_token)
        _login_step_ok(r3, "exchangetoken")

        # 6. 后置校验：session cookies 应已写入 token（CAS 通过 Set-Cookie 落地）
        session_token = api.session.cookies.get("token", "")
        assert session_token, \
            f"三步登录完成后 session.cookies 未拿到 token, cookies={dict(api.session.cookies)}, 三步响应={{'weblogin': {r1}, 'casTokenLogin': {r2}, 'exchangetoken': {r3}}}"

        # 7. 交叉验证：调用完整 login() 主流程应能同样拿到 token，且 details 三步响应齐全
        api_full = LoginAPI(base_url=login_base_url)
        token_full, details = api_full.login(LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_APP_NAME)
        assert token_full, f"完整 login() 主流程未获取到 token, details={details}"
        assert set(details.keys()) == {"weblogin", "casTokenLogin", "exchangetoken"}, \
            f"login() details 三步响应结构不完整, keys={list(details.keys())}"

    @allure.story("CAS 登录后自动回写 config.py token 字段")
    def test_public_LOGIN_cas_login_and_update_config(self, tmp_path, monkeypatch):
        """CAS 登录成功后自动回写 config.py 的 default_cookies.token 字段（tmp_path 隔离，不污染真实 config.py）"""
        # Author: Author
        # Create Date: 2026-10-20
        # IsAI: True

        # 1. 前置：凭据校验；login_and_update_config 内部自建 LoginAPI() 不接受 base_url 参数，
        #    需临时把 config.base_url 覆盖为 CAS 登录域名（IP 直连场景下 CAS 服务不可达）
        _require_credentials()
        monkeypatch.setattr(config, "base_url", CPSOL_BASE_URL)

        # 2. 前置：在 tmp_path 下构造一份含旧 token 字面量的 config.py 副本作为写入靶，
        #    避免真实项目 config.py 被本次用例改写
        fake_config = tmp_path / "config.py"
        fake_config.write_text(
            '# -*- coding: utf-8 -*-\n'
            'default_cookies = {"token": "OLD_TOKEN_BEFORE_LOGIN"}\n',
            encoding="utf-8",
        )

        # 3. 核心操作：调用 login_and_update_config，走完 CAS 三步登录后自动正则改写 fake_config
        new_token = login_and_update_config(
            LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_APP_NAME,
            config_path=str(fake_config),
        )

        # 4. 断言：返回的 token 非空且为 32 位十六进制字符串（CAS token 典型格式）
        assert new_token, "login_and_update_config 未返回 token，登录失败"
        assert re.fullmatch(r"[0-9a-f]{32}", new_token), \
            f"返回 token 不符合 32 位十六进制格式, token={new_token}"

        # 5. 断言：fake_config 已被真实改写，旧 token 字面量被替换为新 token
        updated_text = fake_config.read_text(encoding="utf-8")
        assert "OLD_TOKEN_BEFORE_LOGIN" not in updated_text, \
            f"临时 config.py 未更新，旧 token 仍存在, 内容={updated_text}"
        assert f'"token": "{new_token}"' in updated_text, \
            f"临时 config.py 未写入新 token, 内容={updated_text}"

        # 6. 后置校验：真实项目 config.py 未被本次用例污染（不含本次登录返回的 token）
        real_config_path = Path(config.base_dir) / "config.py"
        real_config_text = real_config_path.read_text(encoding="utf-8")
        assert new_token not in real_config_text, \
            f"真实项目 config.py 被污染，含本次登录 token={new_token}，请检查 config_path 传参是否生效"
