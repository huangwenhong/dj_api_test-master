# -*- coding: utf-8 -*-
"""易单来 - 纸板厂诊断用例（基于易单来swaggerApi.json）"""

import os
from datetime import datetime, timedelta

import allure
import pytest
import config
from test_case.page_api.ydl.zhenduan_api import ZhenduanAPI, ZHENDUAN_BASE_URL


def _login_zhenduan():
    """诊断模块使用独立域名 intelligenttest.onlinecps.cn 的 token。"""
    token = os.getenv("API_TEST_ZHENDUAN_TOKEN", "")
    if not token:
        pytest.fail("请先设置诊断模块独立认证环境变量 API_TEST_ZHENDUAN_TOKEN。")
    return ZhenduanAPI(cookies={"token": token})


@pytest.fixture(scope="module")
def zd_env():
    """模块级 fixture：诊断模块独立登录后返回 ZhenduanAPI 实例"""
    return _login_zhenduan()


ZD = ZhenduanAPI()


def _ok(res, msg="接口返回异常"):
    """校验接口 code=10001200 且 success=True"""
    assert res.get("code") == "10001200", f"{msg}, 接口返回={res}"
    assert res.get("success") is True, f"{msg} success不为True, 接口返回={res}"


def _get_report_id(zd):
    """获取诊断报告 reportId，列表为空则跳过用例。"""
    res_list = zd.get_page_list(pageNo=1, pageSize=10)
    _ok(res_list, "获取诊断报告列表失败")
    list_data = res_list.get("data", {})
    rows = list_data.get("list") or []
    if not rows:
        pytest.skip("诊断报告列表为空，跳过依赖 reportId 的步骤")
    report_id = rows[0].get("reportId") or rows[0].get("id")
    assert report_id, f"报告列表首行缺少 reportId, item={rows[0]}"
    return report_id


def _date_range(days_back=20):
    """计算近 N 天的日期范围 (yyyy-MM-dd)"""
    now = datetime.now()
    return (now - timedelta(days=days_back)).strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")


# ==================== 纸板厂诊断 ====================

@allure.feature("纸板厂诊断")
class TestZhenduan:

    @allure.story("诊断报告列表查询")
    def test_ydl_ZD_report_list_query(self, zd_env):
        """诊断报告列表：默认分页→按企业名称→按注册手机号→按时间范围→验证列表结构"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        ZD = zd_env
        assert ZD, "诊断模块登录失败"

        # 1. 默认分页查询（pageNo/pageSize 必填）
        res_list = ZD.get_page_list(pageNo=1, pageSize=10)
        _ok(res_list, "获取诊断报告列表失败")
        list_data = res_list.get("data", {})
        assert isinstance(list_data, dict), \
            f"报告列表data类型异常, 期望dict, 实际={type(list_data)}"
        assert "total" in list_data, f"报告列表缺少total字段, data={list_data}"
        rows = list_data.get("list") or []
        assert isinstance(rows, list), \
            f"报告列表list类型异常, 期望list, 实际={type(rows)}"

        # 2. 按企业名称过滤
        res_company = ZD.get_page_list(pageNo=1, pageSize=10, companyName="测试纸板厂")
        _ok(res_company, "报告列表-企业名称过滤失败")

        # 3. 按注册手机号过滤
        res_phone = ZD.get_page_list(pageNo=1, pageSize=10, registeredPhone="13800138000")
        _ok(res_phone, "报告列表-注册手机号过滤失败")

        # 4. 按时间范围过滤
        start_time, end_time = _date_range()
        res_time = ZD.get_page_list(pageNo=1, pageSize=10, startTime=start_time, endTime=end_time)
        _ok(res_time, "报告列表-时间范围过滤失败")

    @allure.story("报告分析链路")
    def test_ydl_ZD_report_analysis_chain(self, zd_env):
        """报告分析链路：取报告ID→企业基础画像→核心诉求→市场洞察→业务机会→分析报告详情"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        ZD = zd_env
        assert ZD, "诊断模块登录失败"

        # 1. 获取报告ID（列表为空则跳过）
        report_id = _get_report_id(ZD)

        # 2. 企业基础画像（getCompanyBaseProfile.do）
        res_profile = ZD.get_company_base_profile(reportId=report_id)
        _ok(res_profile, "企业基础画像查询失败")
        profile_data = res_profile.get("data")
        assert isinstance(profile_data, dict), \
            f"企业基础画像data类型异常, 期望dict, 实际={type(profile_data)}"

        # 3. 核心诉求（getCoreDemand.do）
        res_demand = ZD.get_core_demand(reportId=report_id)
        _ok(res_demand, "核心诉求查询失败")

        # 4. 市场洞察（getMarketInsight.do）
        res_insight = ZD.get_market_insight(reportId=report_id)
        _ok(res_insight, "市场洞察查询失败")

        # 5. 业务机会（getBusinessOpportunity.do）
        res_opportunity = ZD.get_business_opportunity(reportId=report_id)
        _ok(res_opportunity, "业务机会查询失败")

        # 6. 分析报告详情（getReportsDetail.do）- 汇总以上各模块
        res_detail = ZD.get_reports_detail(reportId=report_id)
        _ok(res_detail, "获取分析报告详情失败")
        detail_data = res_detail.get("data")
        assert isinstance(detail_data, dict), \
            f"分析报告详情data类型异常, 期望dict, 实际={type(detail_data)}"

    @allure.story("保存合作评估报告")
    def test_ydl_ZD_save_cooperation_evaluation(self, zd_env):
        """保存合作评估报告：取报告ID→最小必填保存→完整字段保存→详情回查"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        ZD = zd_env
        assert ZD, "诊断模块登录失败"

        # 1. 获取报告ID（列表为空则跳过）
        report_id = _get_report_id(ZD)

        # 2. 最小必填保存（仅 reportId）
        res_min = ZD.save_cooperation_evaluation_report(reportId=report_id)
        _ok(res_min, "保存合作评估报告（最小必填）失败")

        # 3. 完整字段保存（saveCooperationEvaluationReport.do）
        res_full = ZD.save_cooperation_evaluation_report(
            reportId=report_id,
            salesRadius=321,
            mainCoverage="321",
            mainPillarIndustry="321",
            cooperationModeList=["other", "yft_pre_purchase_post_pay", "raw_paper_procurement"],
            cooperationAgreementSignTime="2026-09-18",
            budgetGoalItemList=[
                {"period": "1", "gmv": "1", "revenue": "1", "profit": "1", "remark": "1", "id": "08ca5065e6b5440381fcbbcbc64dcb95"},
                {"period": "1", "gmv": "1", "revenue": "1", "profit": "1", "remark": "1", "id": "f6f8231804724f33b436026c825f94af"}
            ],
        )
        _ok(res_full, "保存合作评估报告（完整字段）失败")

        # 4. 详情回查，确认保存后报告仍可正常读取
        res_detail = ZD.get_reports_detail(reportId=report_id)
        _ok(res_detail, "保存后详情回查失败")

    @allure.story("空reportId参数校验")
    def test_ydl_ZD_empty_report_id_blocked(self, zd_env):
        """空reportId参数校验：reportId 传空字符串应被参数校验拦截"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        ZD = zd_env
        assert ZD, "诊断模块登录失败"

        methods = [
            (ZD.get_company_base_profile, "企业基础画像"),
            (ZD.get_core_demand, "核心诉求"),
            (ZD.get_market_insight, "市场洞察"),
            (ZD.get_business_opportunity, "业务机会"),
            (ZD.save_cooperation_evaluation_report, "保存合作评估报告"),
            (ZD.get_reports_detail, "获取分析报告详情"),
        ]
        for method, msg in methods:
            # 1. 空 reportId 调用应返回非成功code
            res = method(reportId="")
            assert res.get("code") != "10001200", \
                f"{msg}空reportId应被拦截, 但返回了成功, 接口返回={res}"
