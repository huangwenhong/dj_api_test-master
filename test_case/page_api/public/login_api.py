# -*- coding: utf-8 -*-
"""CAS 单点登录接口封装。

登录流程（三步）：
1. weblogin.do       → 用账号密码换取 onceToken
2. casTokenLogin.do  → 用 onceToken 换取业务 token
3. exchangetoken.do  → 用 onceToken 换取最终 token（部分场景可选）
"""

import allure
import hashlib
import requests
import config


AUTH_PREFIX = "/djauth/cas"


class LoginAPI:
    """CAS 登录接口封装（不依赖 BaseAPI，避免循环依赖 config 中的 token）"""

    def __init__(self, base_url=None):
        self.base_url = (base_url or config.base_url).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(config.default_headers)
        # 登录接口关闭 SSL 验证，避免代理环境下证书错误
        self.session.verify = False
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @staticmethod
    def _md5(text):
        """MD5 加密"""
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    @allure.step("第一步：weblogin 获取 onceToken")
    def web_login(self, userName, password, appName="DJSUPPLIER"):
        """CAS weblogin：用账号密码换取 onceToken（密码需 MD5 加密）"""
        url = f"{self.base_url}{AUTH_PREFIX}/weblogin.do"
        payload = {
            "userName": userName,
            "password": self._md5(password),
            "appName": appName,
        }
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    @allure.step("第二步：casTokenLogin 获取业务 token")
    def cas_token_login(self, appName="DJSUPPLIER", onceToken=""):
        """CAS casTokenLogin：用 onceToken 换取业务 token"""
        url = f"{self.base_url}{AUTH_PREFIX}/casTokenLogin.do"
        payload = {
            "appName": appName,
            "onceToken": onceToken,
        }
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    @allure.step("第三步：exchangetoken 换取最终 token")
    def exchange_token(self, onceToken=""):
        """CAS exchangetoken：用 onceToken 换取最终 token"""
        url = f"{self.base_url}{AUTH_PREFIX}/exchangetoken.do"
        payload = {
            "onceToken": onceToken,
        }
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def login(self, userName, password, appName="DJSUPPLIER"):
        """完整登录流程，返回最终 token"""
        import re

        # 第一步：weblogin
        r1 = self.web_login(userName, password, appName)
        print(f"[登录] weblogin 响应码: {r1.get('code', '')}")

        # 从 weblogin 响应中提取 onceToken
        once_token = ""
        if isinstance(r1, dict) and r1.get("success"):
            data = r1.get("data", {})
            if isinstance(data, dict):
                # onceToken 可能在 URL 中: https://...?appName=...&onceToken=xxx
                url = data.get("url", "")
                m = re.search(r"onceToken=([^&]+)", url)
                if m:
                    once_token = m.group(1)
                if not once_token:
                    once_token = data.get("onceToken", "") or data.get("token", "")
            if not once_token:
                once_token = r1.get("onceToken", "") or r1.get("token", "")

        if not once_token:
            print(f"[登录] weblogin 未返回 onceToken，完整响应: {r1}")
            return None, r1

        print(f"[登录] onceToken: {once_token}")

        # 第二步：casTokenLogin
        r2 = self.cas_token_login(appName, once_token)
        print(f"[登录] casTokenLogin 响应码: {r2.get('code', '') if isinstance(r2, dict) else r2}")

        # 第三步：exchangetoken
        r3 = self.exchange_token(once_token)
        print(f"[登录] exchangetoken 响应码: {r3.get('code', '') if isinstance(r3, dict) else r3}")

        # 从 session cookies 中提取 token（登录流程通过 Set-Cookie 设置）
        token = self.session.cookies.get("token", "")

        # 备用：从响应体中提取
        if not token:
            for r in [r3, r2]:
                if isinstance(r, dict):
                    data = r.get("data")
                    if isinstance(data, dict):
                        token = data.get("token", "")
                    elif isinstance(data, str):
                        token = data
                    if not token:
                        token = r.get("token", "")
                if token:
                    break

        return token, {"weblogin": r1, "casTokenLogin": r2, "exchangetoken": r3}


def login_and_update_config(userName, password, appName="DJSUPPLIER", config_path=None):
    """登录获取 token，并自动更新 config.py 中的 default_cookies token。

    Args:
        userName: 登录用户名
        password: 登录密码
        appName: 应用名称
        config_path: config.py 路径，默认使用项目根目录的 config.py

    Returns:
        str: 新的 token 值
    """
    import re
    import os

    api = LoginAPI()
    token, details = api.login(userName, password, appName)

    if not token:
        print(f"[登录失败] 未能获取到有效 token")
        print(f"  weblogin: {details.get('weblogin', {})}")
        print(f"  casTokenLogin: {details.get('casTokenLogin', {})}")
        print(f"  exchangetoken: {details.get('exchangetoken', {})}")
        return None

    print(f"[登录成功] 新 token: {token}")

    # 更新 config.py 中的 token
    cfg_path = config_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "config.py")
    cfg_path = os.path.normpath(cfg_path)

    if not os.path.isfile(cfg_path):
        print(f"[警告] config.py 未找到: {cfg_path}，请手动更新 token")
        return token

    with open(cfg_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 替换 default_cookies 中的 token 值
    pattern = r'(default_cookies\s*=\s*\{[^}]*"token"\s*:\s*)"[^"]*"'
    replacement = rf'\1"{token}"'
    new_content, count = re.subn(pattern, replacement, content)

    if count == 0:
        print(f"[警告] 未匹配到 config.py 中的 token，请手动更新: {token}")
        return token

    with open(cfg_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[config.py 已更新] token = {token}")
    return token


if __name__ == "__main__":
    # 直接运行：python -m test_case.page_api.public.login_api
    # 或在命令行中调用 login_and_update_config()
    import sys

    user = sys.argv[1] if len(sys.argv) > 1 else ""
    pwd = sys.argv[2] if len(sys.argv) > 2 else ""
    app = sys.argv[3] if len(sys.argv) > 3 else "DJSUPPLIER"

    if not user or not pwd:
        print("用法: python login_api.py <用户名> <密码> [appName]")
        sys.exit(1)

    login_and_update_config(user, pwd, app)
