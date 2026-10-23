# -*- coding: utf-8 -*-
"""易单来 - APP 工作台-客户总结模块用例（基于 APP 抓包）"""

import allure
import pytest
from datetime import datetime, timedelta
from test_case.page_api.ydl.kehu_zongjie_api import KehuZongjieAPI
from test_case.page_api.ydl.mubiao_api import MubiaoAPI

KZ = KehuZongjieAPI()


def _ok(res, msg="接口返回异常"):
    """校验接口 code=10001200 且 success=True"""
    assert res.get("code") == "10001200", f"{msg}, 接口返回={res}"
    assert res.get("success") is True, f"{msg} success不为True, 接口返回={res}"


def _resolve_supplier_and_customer():
    """动态解析当前账号可访问的真实 supplierId 与 customerId。

    旧硬编码的示例供应商(ee3b...)/客户(026c...)在当前环境已失效：客户预警概览
    各状态均为空，getCustomerInfoById 返回 10001506。这里改为从目标管理供应商列表
    取账号自身联合供应商(unionSupplier=1)，再按客户预警状态取首个非空客户，
    确保使用账号真正有权限的数据。返回 (supplier_id, customer_id)；无数据时对应项为 None。
    """
    res = MubiaoAPI().get_supplier_info_no_auth()
    sup_list = (res.get("data") or {}).get("list", []) or []
    union = next((s for s in sup_list if str(s.get("unionSupplier")) == "1"), None)
    supplier_id = (union or (sup_list[0] if sup_list else {})).get("supplierId")
    if not supplier_id:
        return None, None
    end_m = datetime.now().strftime("%Y-%m")
    begin_m = (datetime.now() - timedelta(days=180)).strftime("%Y-%m")
    for state in ("loss", "active", "add", "activate", "no_order"):
        rw = KZ.get_customer_warn_overview(
            supplierId=supplier_id, beginDate=begin_m, endDate=end_m, state=state)
        wl = (rw.get("data") or {}).get("list", []) or []
        if wl:
            return supplier_id, (wl[0].get("customerId") or wl[0].get("id"))
    return supplier_id, None


# ==================== APP-客户总结 ====================

@allure.feature("APP-客户总结")
class TestKehuZongjie:

    @allure.story("客户信息总览")
    def test_ydl_KZ_customer_info_overview(self):
        """客户信息总览：获取活跃/新增/总客户数"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        org_id = "400"
        supplier_id = "ee3b25465f0b11edb9b5000c29f98159"
        end_date = datetime.now().strftime("%Y-%m-%d")
        begin_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        # 1. 获取客户信息总览
        res = KZ.get_customer_info(
            orgId=org_id,
            supplierId=supplier_id,
            beginDate=begin_date,
            endDate=end_date
        )
        # 该接口成功时返回 code=10001201
        assert res.get("code") in ["10001200", "10001201"], f"获取客户信息总览失败, 接口返回={res}"
        assert res.get("success") is True, f"获取客户信息总览 success不为True, 接口返回={res}"

        # 2. 断言返回结构
        data = res.get("data", {})
        assert isinstance(data, dict), f"返回data不是字典类型, data={data}"
        # 验证关键字段存在
        assert "totalCustomer" in data or "total" in data, f"缺少总客户数字段, data={data}"

    @allure.story("重点关注客户列表")
    def test_ydl_KZ_key_attention_customer_list(self):
        """重点关注客户列表：获取已关注的客户列表"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        org_id = "400"
        supplier_id = "ee3b25465f0b11edb9b5000c29f98159"

        # 1. 获取重点关注客户列表
        res = KZ.get_customer_list(orgId=org_id, supplierId=supplier_id)
        _ok(res, "获取重点关注客户列表失败")

        # 2. 断言返回结构
        data = res.get("data", {})
        assert isinstance(data, dict), f"返回data不是字典类型, data={data}"
        assert "list" in data or "total" in data, f"缺少list或total字段, data={data}"

    @allure.story("客户详情查询")
    def test_ydl_KZ_customer_detail_by_id(self):
        """客户详情查询：根据客户ID获取客户详细信息"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        org_id = "400"
        # 动态解析账号自身联合供应商及其一个真实客户ID（硬编码示例供应商/客户已失效，返回 10001506）
        supplier_id, customer_id = _resolve_supplier_and_customer()
        assert customer_id, "当前账号无可用客户数据, 无法校验客户详情"

        # 1. 根据ID获取客户详情
        res = KZ.get_customer_info_by_id(
            orgId=org_id,
            supplierId=supplier_id,
            customerId=customer_id
        )
        _ok(res, "根据ID获取客户详情失败")

        # 2. 断言返回结构
        data = res.get("data", {})
        assert isinstance(data, dict), f"返回data不是字典类型, data={data}"

    @allure.story("客户订单趋势")
    def test_ydl_KZ_customer_order_trend(self):
        """客户订单趋势：获取指定客户的订单趋势数据"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        org_id = "400"
        supplier_id = "ee3b25465f0b11edb9b5000c29f98159"
        customer_id = "026c28a8c4004d119c1778fca646d61e"
        end_date = datetime.now().strftime("%Y-%m")
        begin_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m")

        # 1. 获取客户订单趋势
        res = KZ.get_customer_order_trend(
            orgId=org_id,
            supplierId=supplier_id,
            customerId=customer_id,
            beginDate=begin_date,
            endDate=end_date
        )
        _ok(res, "获取客户订单趋势失败")

        # 2. 断言返回结构
        data = res.get("data", {})
        assert isinstance(data, dict), f"返回data不是字典类型, data={data}"
        assert "list" in data, f"缺少list字段, data={data}"

    @allure.story("客户视图")
    def test_ydl_KZ_customer_view(self):
        """客户视图：获取客户今日金额/面积/订单数等汇总数据"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        org_id = "400"
        # 动态解析账号自身联合供应商及其一个真实客户ID（硬编码示例供应商/客户已失效）
        supplier_id, customer_id = _resolve_supplier_and_customer()
        assert customer_id, "当前账号无可用客户数据, 无法校验客户视图"
        end_date = datetime.now().strftime("%Y-%m")
        begin_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m")

        # 1. 获取客户视图
        res = KZ.get_customer_view(
            orgId=org_id,
            supplierId=supplier_id,
            customerId=customer_id,
            beginDate=begin_date,
            endDate=end_date
        )
        _ok(res, "获取客户视图失败")

        # 2. 断言返回结构
        data = res.get("data", {})
        assert isinstance(data, dict), f"返回data不是字典类型, data={data}"
        # 验证关键字段
        assert "todayAmount" in data or "orderNumber" in data, f"缺少关键字段, data={data}"

    @allure.story("客户预警概览数量")
    def test_ydl_KZ_customer_warn_overview_num(self):
        """客户预警概览数量：获取各状态客户数量（未下单/流失/新增/激活/活跃）"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        supplier_id = "ee3b25465f0b11edb9b5000c29f98159"
        end_date = datetime.now().strftime("%Y-%m")
        begin_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m")

        # 1. 获取客户预警概览数量
        res = KZ.get_customer_warn_overview_num(
            supplierId=supplier_id,
            beginDate=begin_date,
            endDate=end_date
        )
        _ok(res, "获取客户预警概览数量失败")

        # 2. 断言返回结构
        data = res.get("data", {})
        assert isinstance(data, dict), f"返回data不是字典类型, data={data}"
        assert "list" in data, f"缺少list字段, data={data}"

        # 3. 验证状态列表结构
        state_list = data.get("list", [])
        if state_list:
            first_item = state_list[0]
            assert "state" in first_item, f"状态项缺少state字段, item={first_item}"
            assert "num" in first_item, f"状态项缺少num字段, item={first_item}"

    @allure.story("AI客户订单预测")
    def test_ydl_KZ_customer_order_prediction(self):
        """AI客户订单预测：获取AI预测的客户订单数据"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        supplier_id = "ee3b25465f0b11edb9b5000c29f98159"
        end_date = datetime.now().strftime("%Y-%m-%d")
        begin_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        # 1. 获取AI客户订单预测
        res = KZ.get_customer_order_prediction(
            supplierId=supplier_id,
            beginDate=begin_date,
            endDate=end_date
        )
        _ok(res, "获取AI客户订单预测失败")

        # 2. 断言返回结构
        data = res.get("data", {})
        assert isinstance(data, dict), f"返回data不是字典类型, data={data}"

    @allure.story("客户预警概览列表")
    @pytest.mark.parametrize(
        "state, state_desc",
        (
            ("no_order", "未下单"),
            ("loss", "流失"),
            ("add", "新增"),
            ("activate", "激活"),
            ("active", "活跃"),
        ),
        ids=("no_order", "loss", "add", "activate", "active")
    )
    def test_ydl_KZ_customer_warn_overview_list(self, state, state_desc):
        """客户预警概览列表：按状态获取预警客户列表"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        supplier_id = "ee3b25465f0b11edb9b5000c29f98159"
        end_date = datetime.now().strftime("%Y-%m")
        begin_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m")

        # 1. 获取客户预警概览列表
        res = KZ.get_customer_warn_overview(
            supplierId=supplier_id,
            beginDate=begin_date,
            endDate=end_date,
            state=state
        )
        _ok(res, f"获取客户预警概览列表-{state_desc}失败")

        # 2. 断言返回结构
        data = res.get("data", {})
        assert isinstance(data, dict), f"返回data不是字典类型, data={data}"
        assert "list" in data or "total" in data, f"缺少list或total字段, data={data}"
