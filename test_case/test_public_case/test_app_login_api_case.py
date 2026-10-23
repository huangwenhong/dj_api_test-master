# -*- coding: utf-8 -*-
"""公共模块 - APP 端易单来单步登录接口用例（复用 test_case/page_api/public/login_api.py）

APP 登录与 Web 端 CAS 三步登录不同：
- 域名：oatest.cpsol.net（不是 suppliertest.cpsol.net）
- 接口：/DJEASYORDER/easyorderlogin.do（单步，非 CAS 三步）
- 字段：name/appname/version（不是 userName/appName）
- 响应：data 是数组（不是对象），不返回 token（token 在 Set-Cookie）
"""

import re

import allure
import pytest

from conftest import LOGIN_PASSWORD, LOGIN_USERNAME
from test_case.page_api.public.login_api import LoginAPI

# APP 端登录域名（与 Web 端 CPSOL_BASE_URL 不同）
OATEST_BASE_URL = "https://oatest.cpsol.net"


def _require_credentials():
    """前置：账号密码必须就绪，否则跳过（conftest.auto_login 已在会话级兜底 exit）。"""
    if not LOGIN_USERNAME or not LOGIN_PASSWORD:
        pytest.skip("未设置 API_TEST_USERNAME / API_TEST_PASSWORD 环境变量，跳过 APP 登录用例")


@allure.feature("公共-APP登录")
class TestAppLogin:
    """APP 端易单来登录接口用例集。"""

    @allure.story("APP 单步登录成功获取用户信息")
    def test_public_LOGIN_app_easyorder_success(self):
        """APP 单步登录成功获取用户信息：easyorderlogin.do → code=10001200 + data 数组含 userid/userName"""
        # Author: Author
        # Create Date: 2026-10-20
        # IsAI: True

        # 1. 前置：凭据校验
        _require_credentials()

        # 2. 核心操作：调用 APP 登录接口（域名 oatest.cpsol.net）
        api = LoginAPI(base_url=OATEST_BASE_URL)
        resp = api.app_easyorder_login(LOGIN_USERNAME, LOGIN_PASSWORD)

        # 3. 断言：code=10001200 + success=True（基于真实响应体）
        assert resp.get("code") == "10001200", \
            f"APP 登录失败, code={resp.get('code')}, 完整响应={resp}"
        assert resp.get("success") is True, \
            f"APP 登录 success 不为 True, 完整响应={resp}"

        # 4. 断言：data 是数组且非空（APP 端 data 结构与 Web 端不同）
        data = resp.get("data")
        assert isinstance(data, list), \
            f"data 不是数组, 实际类型={type(data).__name__}, 完整响应={resp}"
        assert len(data) > 0, \
            f"data 数组为空, 完整响应={resp}"

        # 5. 断言：data[0] 包含关键字段（基于真实响应体）
        user_info = data[0]
        assert isinstance(user_info, dict), \
            f"data[0] 不是 dict, 实际类型={type(user_info).__name__}, data={data}"
        for key in ("userid", "userName", "pushID", "userIco"):
            assert key in user_info, \
                f"data[0] 缺少字段 {key}, 实际字段={list(user_info.keys())}, data[0]={user_info}"

        # 6. 断言：msg="请求成功！"（基于完整响应体）
        assert resp.get("msg") == "请求成功！", \
            f"msg 不等于'请求成功！', 实际 msg={resp.get('msg')}, 完整响应={resp}"

        # 7. 断言：session.cookies 应已写入 token（从 Set-Cookie header）
        session_token = api.session.cookies.get("token", "")
        assert session_token, \
            f"APP 登录后 session.cookies 未拿到 token, cookies={dict(api.session.cookies)}, 响应={resp}"
        assert re.fullmatch(r"[0-9a-f]{32}", session_token), \
            f"token 不符合 32 位十六进制格式, token={session_token}"
