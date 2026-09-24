# -*- coding: utf-8 -*-
import json
import time

import allure
import requests

import conftest

AIAGENT_BASE_URL = conftest.AIAGENT_BASE_URL
PREFIX = "/paper-report/CorruSenseAI"


class MarketAnalysisAPI:
    """市场分析智能体接口封装（aiagent.djcps.com）"""

    def __init__(self):
        self.base_url = AIAGENT_BASE_URL

    def _get_session(self):
        """创建独立 session，携带 corrusense_token"""
        session = requests.Session()
        session.trust_env = False
        session.verify = False
        session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
            "Referer": f"{self.base_url}/paper-report/",
        })
        token = conftest.corrusense_token.get("token", "")
        if token:
            session.cookies.set("corrusense_token", token)
        return session

    def _post(self, url_path, payload, error_msg="请求失败"):
        """通用 POST 请求，返回 (response_json, elapsed_seconds)"""
        session = self._get_session()
        url = f"{self.base_url}{url_path}"
        start = time.time()
        resp = session.post(url, json=payload)
        elapsed = round(time.time() - start, 3)
        try:
            data = resp.json()
        except (json.JSONDecodeError, ValueError):
            data = {"raw": resp.text[:500]}
        return data, elapsed

    # ==================== 接口方法 ====================

    @allure.step("会话列表 session/list")
    def session_list(self, payload=None, **kwargs):
        """查询会话列表"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        if payload is None:
            payload = {"pageNo": 1, "pageSize": 20, "reportType": 2}
        payload.update(kwargs)
        return self._post(f"{PREFIX}/agent/session/list", payload, "查询会话列表失败")

    @allure.step("提交分析任务 market-analysis/overview")
    def market_analysis_overview(self, payload=None, **kwargs):
        """提交市场分析任务"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        if payload is None:
            payload = {
                "factoryName": "宏达新型建材有限公司",
                "location": "浙江省温州市鹿城区蒲鞋市街道芳园社区上陡门住宅区六组团",
                "salesRadiusKm": 26,
                "salesAreas": ["2", "3", "4", "5", "4", "6", "7", "8", "9", "1", "2", "3"],
                "equipment": "全自动切割机组",
                "productStructures": ["5层", "3层"],
                "mainCity": {
                    "provinceName": "浙江省", "cityName": "温州市",
                    "cityCode": "", "longitude": "120.697402", "latitude": "28.005561"
                },
                "surroundingCities": [
                    {"provinceName": "浙江省", "cityName": "绍兴市", "cityCode": ""},
                    {"provinceName": "浙江省", "cityName": "杭州市", "cityCode": ""},
                    {"provinceName": "浙江省", "cityName": "宁波市", "cityCode": ""},
                    {"provinceName": "浙江省", "cityName": "台州市", "cityCode": ""},
                ],
                "threadId": ""
            }
        payload.update(kwargs)
        return self._post(f"{PREFIX}/reports/market-analysis/overview", payload, "提交分析任务失败")

    @allure.step("会话详情 session/detail")
    def session_detail(self, thread_id, **kwargs):
        """查询会话详情"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        payload = {"threadId": thread_id}
        payload.update(kwargs)
        return self._post(f"{PREFIX}/agent/session/detail", payload, "查询会话详情失败")

    @allure.step("任务状态查询 task/status")
    def task_status(self, report_id, **kwargs):
        """查询分析任务状态"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        payload = {"reportId": report_id}
        payload.update(kwargs)
        return self._post(f"{PREFIX}/reports/market-analysis/task/status", payload, "查询任务状态失败")
