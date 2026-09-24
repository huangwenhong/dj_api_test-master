# -*- coding: utf-8 -*-
"""市场分析智能体 - 并发测试用例"""

import allure
import json
import pytest
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from test_case.page_api.ydl.market_analysis_api import MarketAnalysisAPI

# 并发数
CONCURRENCY = 5


@allure.feature("市场分析智能体")
class TestMarketAnalysisConcurrency:
    """市场分析智能体并发测试类"""

    def _get_api(self):
        return MarketAnalysisAPI()

    # ==================== A: 会话列表并发 ====================

    @allure.story("并发测试")
    def test_concurrent_session_list(self):
        """会话列表接口 5 并发"""
        api = self._get_api()
        results = []

        def _call(idx):
            res, elapsed = api.session_list()
            return {"idx": idx, "res": res, "elapsed": elapsed}

        with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
            futures = [pool.submit(_call, i) for i in range(CONCURRENCY)]
            for f in as_completed(futures):
                results.append(f.result())

        self._assert_concurrent_results(results, "会话列表", "session/list")

    # ==================== B: 提交分析任务并发 ====================

    @allure.story("并发测试")
    def test_concurrent_market_analysis_overview(self):
        """提交分析任务接口 5 并发"""
        api = self._get_api()
        results = []

        def _call(idx):
            res, elapsed = api.market_analysis_overview()
            return {"idx": idx, "res": res, "elapsed": elapsed}

        with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
            futures = [pool.submit(_call, i) for i in range(CONCURRENCY)]
            for f in as_completed(futures):
                results.append(f.result())

        self._assert_concurrent_results(results, "提交分析任务", "market-analysis/overview")

    # ==================== C: 会话详情并发 ====================

    @allure.story("并发测试")
    def test_concurrent_session_detail(self):
        """会话详情接口 5 并发"""
        api = self._get_api()
        # 先获取一个有效的 threadId
        res, _ = api.session_list()
        thread_id = ""
        if res.get("success") and res.get("data", {}).get("list"):
            thread_id = res["data"]["list"][0].get("threadId", "")

        results = []

        def _call(idx):
            tid = thread_id or "00000000-0000-0000-0000-000000000000"
            res, elapsed = api.session_detail(tid)
            return {"idx": idx, "res": res, "elapsed": elapsed}

        with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
            futures = [pool.submit(_call, i) for i in range(CONCURRENCY)]
            for f in as_completed(futures):
                results.append(f.result())

        self._assert_concurrent_results(results, "会话详情", "session/detail")

    # ==================== D: 任务状态查询并发 ====================

    @allure.story("并发测试")
    def test_concurrent_task_status(self):
        """任务状态查询接口 5 并发"""
        api = self._get_api()
        # 先获取一个有效的 reportId
        res, _ = api.session_list()
        report_id = ""
        if res.get("success") and res.get("data", {}).get("list"):
            report_id = res["data"]["list"][0].get("currentReportId", "")

        results = []

        def _call(idx):
            rid = report_id or "00000000-0000-0000-0000-000000000000"
            res, elapsed = api.task_status(rid)
            return {"idx": idx, "res": res, "elapsed": elapsed}

        with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
            futures = [pool.submit(_call, i) for i in range(CONCURRENCY)]
            for f in as_completed(futures):
                results.append(f.result())

        self._assert_concurrent_results(results, "任务状态查询", "task/status")

    # ==================== E: 全接口混合并发 ====================

    @allure.story("并发测试")
    def test_concurrent_mixed_apis(self):
        """4 个接口混合 5 并发（每轮每接口各 1 请求，共 5 轮）"""
        api = self._get_api()
        results = []

        # 准备有效 ID
        res_list, _ = api.session_list()
        thread_id = ""
        report_id = ""
        if res_list.get("success") and res_list.get("data", {}).get("list"):
            thread_id = res_list["data"]["list"][0].get("threadId", "")
            report_id = res_list["data"]["list"][0].get("currentReportId", "")

        tasks = []
        for round_idx in range(CONCURRENCY):
            tasks.append(("session_list", round_idx, lambda: api.session_list()))
            tasks.append(("overview", round_idx, lambda: api.market_analysis_overview()))
            tasks.append(("session_detail", round_idx,
                          lambda tid=thread_id or "00000000-0000-0000-0000-000000000000": api.session_detail(tid)))
            tasks.append(("task_status", round_idx,
                          lambda rid=report_id or "00000000-0000-0000-0000-000000000000": api.task_status(rid)))

        def _call(name, idx, fn):
            res, elapsed = fn()
            return {"name": name, "idx": idx, "res": res, "elapsed": elapsed}

        with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
            futures = [pool.submit(_call, name, idx, fn) for name, idx, fn in tasks]
            for f in as_completed(futures):
                results.append(f.result())

        # 按接口分组统计
        groups = {}
        for r in results:
            groups.setdefault(r["name"], []).append(r)

        summary_lines = []
        all_pass = True
        for name, group_results in sorted(groups.items()):
            ok = sum(1 for r in group_results if r["res"].get("success") or r["res"].get("code") == "200")
            total = len(group_results)
            times = [r["elapsed"] for r in group_results]
            avg_t = round(sum(times) / len(times), 3)
            max_t = max(times)
            min_t = min(times)
            status = "PASS" if ok == total else "FAIL"
            if ok < total:
                all_pass = False
            summary_lines.append(f"  {name}: {ok}/{total} {status} | 耗时 avg={avg_t}s min={min_t}s max={max_t}s")

        summary = f"混合并发（{CONCURRENCY}并发 x 4接口 x 5轮 = {CONCURRENCY * 4}请求）:\n" + "\n".join(summary_lines)
        print(f"\n{summary}")
        allure.attach(summary, "并发统计", allure.attachment_type.TEXT)

        assert all_pass, f"混合并发存在失败请求:\n{summary}"

    # ==================== 公共断言方法 ====================

    def _assert_concurrent_results(self, results, api_name, api_path):
        """校验并发请求结果"""
        total = len(results)
        success_count = 0
        fail_details = []
        times = []

        for r in sorted(results, key=lambda x: x["idx"]):
            res = r["res"]
            elapsed = r["elapsed"]
            times.append(elapsed)
            is_ok = res.get("success") is True or res.get("code") == "200"
            if is_ok:
                success_count += 1
            else:
                fail_details.append(f"  请求{r['idx']}: code={res.get('code')}, msg={res.get('msg', '')[:100]}")

        avg_time = round(sum(times) / len(times), 3) if times else 0
        max_time = max(times) if times else 0
        min_time = min(times) if times else 0

        summary = (
            f"{api_name}（{CONCURRENCY}并发）:\n"
            f"  成功: {success_count}/{total}\n"
            f"  耗时: avg={avg_time}s, min={min_time}s, max={max_time}s"
        )
        if fail_details:
            summary += "\n  失败详情:\n" + "\n".join(fail_details)

        print(f"\n{summary}")
        allure.attach(summary, f"{api_name}并发统计", allure.attachment_type.TEXT)
        allure.attach(
            json.dumps([r["res"] for r in sorted(results, key=lambda x: x["idx"])],
                       ensure_ascii=False, indent=2)[:3000],
            f"{api_name}响应详情", allure.attachment_type.TEXT)

        assert success_count == total, (
            f"{api_name} {CONCURRENCY}并发未全部成功: {success_count}/{total}\n"
            + "\n".join(fail_details)
        )
