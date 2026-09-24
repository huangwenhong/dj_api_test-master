# -*- coding: utf-8 -*-
"""易单来 - APP 履约用例（基于驾驶舱swaggerApi.json）"""

from datetime import datetime, timedelta

import allure
from test_case.page_api.ydl.lvyue_api import LvyueAPI


def _ok(res, msg="接口返回异常"):
    """校验接口 code=10001200 且 success=True"""
    assert res.get("code") == "10001200", f"{msg}, 接口返回={res}"
    assert res.get("success") is True, f"{msg} success不为True, 接口返回={res}"


def _date_range(days_back=20):
    """计算近 N 天的日期范围 (yyyy-MM-dd)"""
    now = datetime.now()
    return (now - timedelta(days=days_back)).strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")


# ==================== APP 履约 ====================

@allure.feature("APP履约")
class TestLvyue:

    def _get_api(self):
        """获取 API 实例（自动使用 cpsol.net 域名和 token）"""
        return LvyueAPI()

    @allure.story("履约总览")
    def test_ydl_LY_overview_daily_summary(self):
        """履约总览：获取概览→按天汇总(过滤类型/统计维度)→日期范围→验证数据结构"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        LY = self._get_api()

        # 1. 计算日期范围
        begin_date, end_date = _date_range()

        # 2. 获取履约概览（getOverview.do）
        res_overview = LY.get_overview(beginDate=begin_date, endDate=end_date)
        _ok(res_overview, "获取履约概览失败")
        overview_data = res_overview.get("data")
        assert isinstance(overview_data, dict), \
            f"履约概览data类型异常, 期望dict, 实际={type(overview_data)}"

        # 3. 按天汇总-默认（getDailySummary.do）
        res_summary = LY.get_daily_summary(beginDate=begin_date, endDate=end_date)
        _ok(res_summary, "按天汇总查询失败")
        summary_data = res_summary.get("data")
        assert isinstance(summary_data, (dict, list)), \
            f"按天汇总data类型异常, 期望dict/list, 实际={type(summary_data)}"

        # 4. 按天汇总-过滤类型（filterType: 1超24H 2超48H 3催单）
        res_filter = LY.get_daily_summary(
            filterType=1, beginDate=begin_date, endDate=end_date,
        )
        _ok(res_filter, "按天汇总-过滤类型失败")

        # 5. 按天汇总-统计维度（dimensionType: 1送达 2出库）
        res_dimension = LY.get_daily_summary(
            dimensionType=1, beginDate=begin_date, endDate=end_date,
        )
        _ok(res_dimension, "按天汇总-统计维度失败")

    @allure.story("履约订单查询")
    def test_ydl_LY_order_query(self):
        """履约订单查询：订单列表→只查未送达→订单数量统计→按过滤类型→验证列表结构"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        LY = self._get_api()

        # 1. 计算日期范围
        begin_date, end_date = _date_range()

        # 2. 履约订单查询（getOrderList.do, 必填 timeType+filterType）
        res_list = LY.get_order_list(
            timeType="0", filterType=1, beginDate=begin_date, endDate=end_date,
        )
        _ok(res_list, "履约订单查询失败")
        list_data = res_list.get("data", {})
        assert isinstance(list_data, dict), \
            f"履约订单data类型异常, 期望dict, 实际={type(list_data)}"
        rows = list_data.get("list") or []
        assert isinstance(rows, list), \
            f"履约订单list类型异常, 期望list, 实际={type(rows)}"

        # 3. 只查未送达订单（notDelivered=True）
        res_not_delivered = LY.get_order_list(
            timeType="0", filterType=1, notDelivered=True,
            beginDate=begin_date, endDate=end_date,
        )
        _ok(res_not_delivered, "履约订单查询-只查未送达失败")

        # 4. 履约订单查询数量（getOrderNumber.do）
        res_number = LY.get_order_number(beginDate=begin_date, endDate=end_date)
        _ok(res_number, "履约订单查询数量失败")
        number_data = res_number.get("data")
        assert isinstance(number_data, dict), \
            f"订单数量data类型异常, 期望dict, 实际={type(number_data)}"
        # 数量统计字段应为非负数值
        for key, val in number_data.items():
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                assert val >= 0, f"订单数量{key}异常, 期望>=0, 实际={val}"

        # 5. 订单数量-按过滤类型（filterType=2 超48H）
        res_number_filter = LY.get_order_number(
            filterType=2, beginDate=begin_date, endDate=end_date,
        )
        _ok(res_number_filter, "履约订单查询数量-过滤类型失败")

    @allure.story("履约交付分析")
    def test_ydl_LY_delivery_analysis(self):
        """履约交付分析：交付趋势(送达)→交付趋势(出库)→区域交付→区域交付过滤→验证数据结构"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        LY = self._get_api()

        # 1. 计算日期范围
        begin_date, end_date = _date_range()

        # 2. 获取交付趋势-送达维度（getDeliveryTrend.do, 必填 dimensionType）
        res_trend = LY.get_delivery_trend(
            dimensionType=1, beginDate=begin_date, endDate=end_date,
        )
        _ok(res_trend, "获取交付趋势失败")
        trend_data = res_trend.get("data")
        assert isinstance(trend_data, (dict, list)), \
            f"交付趋势data类型异常, 期望dict/list, 实际={type(trend_data)}"

        # 3. 获取交付趋势-出库维度（dimensionType=2）
        res_trend_out = LY.get_delivery_trend(
            dimensionType=2, beginDate=begin_date, endDate=end_date,
        )
        _ok(res_trend_out, "获取交付趋势-出库维度失败")

        # 4. 获取区域交付（getRegionalDelivery.do）
        res_region = LY.get_regional_delivery(beginDate=begin_date, endDate=end_date)
        _ok(res_region, "获取区域交付失败")
        region_data = res_region.get("data")
        assert isinstance(region_data, (dict, list)), \
            f"区域交付data类型异常, 期望dict/list, 实际={type(region_data)}"

        # 5. 区域交付-按过滤类型（filterType: 1超24H 2超48H）
        res_region_filter = LY.get_regional_delivery(
            filterType=1, beginDate=begin_date, endDate=end_date,
        )
        _ok(res_region_filter, "获取区域交付-过滤类型失败")
