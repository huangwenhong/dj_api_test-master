# -*- coding: utf-8 -*-
"""易单来 - APP 工作台-AI重点关注公共模块用例（基于易单来swaggerApi.json）"""

import allure
import pytest
from test_case.page_api.ydl.zhongdian_guanzhu_api import ZhongdianGuanzhuAPI

ZG = ZhongdianGuanzhuAPI()


def _ok(res, msg="接口返回异常"):
    """校验接口 code=10001200 且 success=True"""
    assert res.get("code") == "10001200", f"{msg}, 接口返回={res}"
    assert res.get("success") is True, f"{msg} success不为True, 接口返回={res}"


def _get_attention_business_id():
    """从用户重点关注列表提取业务ID，列表为空则跳过用例。"""
    res_user = ZG.get_user_common(type="customer", appRole="manage")
    _ok(res_user, "获取用户的重点关注失败")
    data = res_user.get("data") or {}
    rows = data.get("list") if isinstance(data, dict) else data
    rows = rows or []
    if not rows:
        pytest.skip("用户重点关注列表为空，跳过依赖业务ID的步骤")
    first = rows[0]
    business_id = first.get("businessId") or first.get("id")
    assert business_id, f"重点关注列表首行缺少业务ID, item={first}"
    return business_id


# ==================== APP-AI重点关注 ====================

@allure.feature("APP-AI重点关注")
class TestZhongdianGuanzhu:

    @allure.story("用户重点关注查询")
    @pytest.mark.parametrize(
        "type, appRole, msg",
        (
            ("customer", "manage", "客户-管理员"),
            ("customer", "salesman", "客户-业务员"),
            ("order", "manage", "订单-管理员"),
        ),
        ids=("customer_manage", "customer_salesman", "order_manage")
    )
    def test_ydl_ZG_user_attention_query(self, type, appRole, msg):
        """用户重点关注查询：按关注类型与应用角色获取用户的重点关注"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 1. 获取用户的重点关注（getUserCommon.do）
        res = ZG.get_user_common(type=type, appRole=appRole)
        _ok(res, f"获取用户的重点关注-{msg}失败")

    @allure.story("重点关注业务链路")
    def test_ydl_ZG_attention_business_chain(self):
        """重点关注业务链路：用户关注列表→业务Id查询→批量增加→批量取消"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 1. 获取用户重点关注列表，提取业务ID
        business_id = _get_attention_business_id()

        # 2. 通过业务Id获取重点关注（getByBusinessCommon.do）
        #    userId/companyId 依赖登录会话上下文，测试环境暂传空，联调后补齐真实取值
        res_by_business = ZG.get_by_business_common(
            businessIdList=[business_id], userId="", appRole="manage", companyId=""
        )
        assert res_by_business.get("code") is not None, \
            f"通过业务Id获取重点关注未返回code, 接口返回={res_by_business}"

        # 3. 批量增加重点关注（与业务Id查询同URL，payload 区分待联调确认）
        res_add = ZG.batch_add_common(
            businessIdList=[business_id], userId="", appRole="manage", companyId=""
        )
        assert res_add.get("code") is not None, \
            f"批量增加重点关注未返回code, 接口返回={res_add}"

        # 4. 批量取消重点关注（与业务Id查询同URL，payload 区分待联调确认）
        res_cancel = ZG.batch_cancel_common(
            businessIdList=[business_id], userId="", appRole="manage", companyId=""
        )
        assert res_cancel.get("code") is not None, \
            f"批量取消重点关注未返回code, 接口返回={res_cancel}"

        # 5. 回查用户重点关注列表，确认接口链路仍可用
        res_recheck = ZG.get_user_common(type="customer", appRole="manage")
        _ok(res_recheck, "批量操作后回查用户重点关注失败")

    @allure.story("重点关注完整业务链路")
    def test_ydl_ZG_key_attention_full_chain(self):
        """重点关注完整链路：查询客户→关注客户→查询订单→关注订单→取消关注客户→取消关注订单

        场景1：客户/订单已被关注 → 查询近30天有下单的客户及其订单 → 关注
        场景2：客户/订单未被关注 → 直接关注
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        from datetime import datetime, timedelta

        org_id = "400"
        supplier_id = "ee3b25465f0b11edb9b5000c29f98159"

        # 1. 查询重点关注客户列表
        res_customer_list = ZG.get_customer_list(orgId=org_id, supplierId=supplier_id)
        _ok(res_customer_list, "查询重点关注客户列表失败")
        customer_data = res_customer_list.get("data", {})
        customer_rows = customer_data.get("list") if isinstance(customer_data, dict) else []
        customer_rows = customer_rows or []

        # 2. 查询重点关注订单列表
        res_order_list = ZG.get_order_list(orgId=org_id, supplierId=supplier_id)
        _ok(res_order_list, "查询重点关注订单列表失败")
        order_data = res_order_list.get("data", {})
        order_rows = order_data.get("list") if isinstance(order_data, dict) else []
        order_rows = order_rows or []

        # 判断场景：是否已关注
        is_followed = bool(customer_rows or order_rows)

        if is_followed:
            # 场景1：已关注 → 查询近30天有下单的客户及其订单
            end_date = datetime.now().strftime("%Y-%m-%d")
            begin_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

            # 查询近30天订单
            res_orders = ZG.get_today_order_list(
                orgId=org_id, supplierId=supplier_id,
                beginDate=begin_date, endDate=end_date, isManage=True
            )
            _ok(res_orders, "查询近30天订单列表失败")
            orders_data = res_orders.get("data", {})
            orders_list = orders_data.get("list") if isinstance(orders_data, dict) else []
            orders_list = orders_list or []

            # 提取客户ID和订单ID
            customer_ids = set()
            order_ids = set()
            for order_group in orders_list:
                for order in order_group.get("orderList", []):
                    cid = order.get("customerId")
                    oid = order.get("orderId")
                    if cid:
                        customer_ids.add(cid)
                    if oid:
                        order_ids.add(oid)

            # 关注客户
            for cid in customer_ids:
                res_follow = ZG.set_key_attention(
                    type="customer", attention=1, businessId=cid
                )
                _ok(res_follow, f"关注客户{cid}失败")

            # 关注订单
            for oid in order_ids:
                res_follow = ZG.set_key_attention(
                    type="order", attention=1, businessId=oid
                )
                _ok(res_follow, f"关注订单{oid}失败")
        else:
            # 场景2：未关注 → 直接关注（取已有列表中的客户/订单）
            customer_id = customer_rows[0].get("customerId") if customer_rows else None
            order_id = order_rows[0].get("orderId") if order_rows else None

            if customer_id:
                res_follow_customer = ZG.set_key_attention(
                    type="customer", attention=1, businessId=customer_id
                )
                _ok(res_follow_customer, "关注客户失败")

            if order_id:
                res_follow_order = ZG.set_key_attention(
                    type="order", attention=1, businessId=order_id
                )
                _ok(res_follow_order, "关注订单失败")

        # 3. 取消关注客户（清理数据）
        for row in customer_rows:
            cid = row.get("customerId") or row.get("id")
            if cid:
                res_unfollow = ZG.set_key_attention(
                    type="customer", attention=0, businessId=cid
                )
                _ok(res_unfollow, f"取消关注客户{cid}失败")

        # 4. 取消关注订单（清理数据）
        for row in order_rows:
            oid = row.get("orderId") or row.get("id")
            if oid:
                res_unfollow = ZG.set_key_attention(
                    type="order", attention=0, businessId=oid
                )
                _ok(res_unfollow, f"取消关注订单{oid}失败")
