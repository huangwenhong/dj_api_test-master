# -*- coding: utf-8 -*-
"""易单来 - APP 订单查询用例"""

from datetime import datetime, timedelta

import allure
import pytest
from test_case.page_api.ydl.dingdan_chaxun_api import DingdanChaxunAPI

DD = DingdanChaxunAPI()

# 测试环境固定参数
ORG_ID = "400"
SUPPLIER_ID = "ee3b25465f0b11edb9b5000c29f98159"


def _date_range(days_back=30):
    """计算近 N 天的日期范围 (yyyy-M-dd)"""
    now = datetime.now()
    return (now - timedelta(days=days_back)).strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")


def _get_first_order_id():
    """从订单列表获取第一个订单ID，列表为空则跳过用例。"""
    res_list = DD.get_order_list(isManage=True, queryStatus="0", pageNo="1", pageSize="1")
    assert res_list.get("code") == "10001200", f"查询订单列表失败, 接口返回={res_list}"
    list_data = res_list.get("data", {})
    rows = list_data.get("list") or []
    if not rows:
        pytest.skip("订单列表为空，跳过依赖订单ID的步骤")
    first_customer = rows[0]
    order_list = first_customer.get("orderList") or []
    if not order_list:
        pytest.skip("订单列表首个客户无订单数据，跳过后续步骤")
    order_id = order_list[0].get("orderId")
    assert order_id, f"订单列表首条订单缺少orderId, item={order_list[0]}"
    return order_id


@allure.feature("APP订单查询")
class TestDingdanChaxun:

    @allure.story("订单查询 - 完整业务流")
    def test_ydl_AA_order_query_full_flow(self):
        """订单查询完整业务流：查询列表→查看详情→查看进度→验证数据一致性"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        # 1. 查询订单列表（默认分页）
        res_list = DD.get_order_list(isManage=True, queryStatus="0", pageNo="1", pageSize="20")
        assert res_list.get("code") == "10001200", f"查询订单列表失败, 接口返回={res_list}"
        list_data = res_list.get("data", {})
        assert isinstance(list_data, dict), f"订单列表data类型异常, 期望dict, 实际={type(list_data)}"
        rows = list_data.get("list") or []
        assert isinstance(rows, list), f"订单列表list类型异常, 期望list, 实际={type(rows)}"

        # 2. 获取第一个订单ID用于后续查询
        if not rows:
            allure.attach("订单列表为空，跳过详情和进度查询", name="提示")
            return
        order_id = rows[0].get("orderList", [{}])[0].get("orderId")
        if not order_id:
            allure.attach("首个客户无订单数据，跳过详情和进度查询", name="提示")
            return

        # 3. 查询订单详情
        res_detail = DD.get_order_info(orderId=order_id)
        assert res_detail.get("code") in ["10001200", "10001201"], f"查询订单详情失败, 接口返回={res_detail}"
        detail_data = res_detail.get("data", {})
        assert isinstance(detail_data, dict), f"订单详情data类型异常, 期望dict, 实际={type(detail_data)}"

        # 4. 验证详情关键字段
        assert detail_data.get("orderId") == order_id, \
            f"orderId不匹配, 期望={order_id}, 实际={detail_data.get('orderId')}"

        # 5. 查询订单进度
        res_schedule = DD.get_order_info_schedule(orderId=order_id)
        assert res_schedule.get("code") == "10001200", f"查询订单进度失败, 接口返回={res_schedule}"
        schedule_data = res_schedule.get("data", {})
        assert isinstance(schedule_data, dict), f"订单进度data类型异常, 期望dict, 实际={type(schedule_data)}"

        # 6. 验证进度数据结构
        assert "productionInfoModel" in schedule_data or "payInfoModel" in schedule_data, \
            f"订单进度缺少关键字段, data={schedule_data}"

    @allure.story("订单查询 - 搜索与筛选")
    def test_ydl_AB_order_search_and_filter(self):
        """订单搜索与筛选：日期范围查询→状态筛选→层列表获取→组合条件搜索"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        # 1. 计算日期范围
        begin_date, end_date = _date_range()

        # 2. 按日期范围搜索订单
        res_search = DD.get_order_list_search(
            beginDate=begin_date,
            endDate=end_date,
            isManage=True,
            pageNo=1,
            pageSize=20
        )
        assert res_search.get("code") == "10001200", f"订单搜索失败, 接口返回={res_search}"
        search_data = res_search.get("data", {})
        assert isinstance(search_data, dict), f"搜索data类型异常, 期望dict, 实际={type(search_data)}"
        search_rows = search_data.get("list") or []
        assert isinstance(search_rows, list), f"搜索list类型异常, 期望list, 实际={type(search_rows)}"

        # 3. 获取层列表（筛选项）
        res_layer = DD.get_layer_list()
        assert res_layer.get("code") == "10001200", f"获取层列表失败, 接口返回={res_layer}"
        layer_data = res_layer.get("data", {})
        layer_list = layer_data.get("list") or []
        assert isinstance(layer_list, list), f"层列表类型异常, 期望list, 实际={type(layer_list)}"

        # 4. 按订单状态筛选（queryStatus: 0全部 1待排产 2生产中 3已入库 4已提货 5运输中 6已送达）
        res_status = DD.get_order_list_search(
            beginDate=begin_date,
            endDate=end_date,
            queryStatus="0",
            pageNo=1,
            pageSize=20
        )
        assert res_status.get("code") == "10001200", f"按状态筛选失败, 接口返回={res_status}"

        # 5. 组合条件搜索（如有层数据，使用第一层作为筛选条件）
        if layer_list:
            first_layer_id = layer_list[0].get("layerId")
            if first_layer_id:
                res_combo = DD.get_order_list_search(
                    beginDate=begin_date,
                    endDate=end_date,
                    layerId=first_layer_id,
                    pageNo=1,
                    pageSize=20
                )
                assert res_combo.get("code") == "10001200", f"组合条件搜索失败, 接口返回={res_combo}"

    @allure.story("订单查询 - 今日订单")
    def test_ydl_AC_today_order_list(self):
        """今日订单列表：按客户查询→带日期范围查询→验证列表结构"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        # 使用抓包中的示例客户ID
        customer_id = "026c28a8c4004d119c1778fca646d61e"
        begin_date, end_date = _date_range()

        # 1. 按客户查询今日订单列表
        res_today = DD.get_today_order_list(
            customerId=customer_id,
            beginDate=begin_date,
            endDate=end_date,
            orgId=ORG_ID,
            supplierId=SUPPLIER_ID
        )
        assert res_today.get("code") == "10001200", f"今日订单列表查询失败, 接口返回={res_today}"
        today_data = res_today.get("data", {})
        assert isinstance(today_data, dict), f"今日订单data类型异常, 期望dict, 实际={type(today_data)}"

        # 2. 验证列表结构
        today_rows = today_data.get("list") or []
        assert isinstance(today_rows, list), f"今日订单list类型异常, 期望list, 实际={type(today_rows)}"

        # 3. 带分页参数查询
        res_page = DD.get_today_order_list(
            customerId=customer_id,
            beginDate=begin_date,
            endDate=end_date,
            orgId=ORG_ID,
            supplierId=SUPPLIER_ID,
            pageNo=1,
            pageSize=10
        )
        assert res_page.get("code") == "10001200", f"今日订单分页查询失败, 接口返回={res_page}"

        # 4. 验证分页数据结构
        page_data = res_page.get("data", {})
        assert isinstance(page_data, dict), f"分页data类型异常, 期望dict, 实际={type(page_data)}"
        page_rows = page_data.get("list") or []
        assert isinstance(page_rows, list), f"分页list类型异常, 期望list, 实际={type(page_rows)}"

    @allure.story("订单查询 - 状态筛选")
    def test_ydl_AD_order_status_filter(self):
        """订单状态筛选：遍历各状态查询→验证各状态返回正常"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        # 定义订单状态：0全部 1待排产 2生产中 3已入库 4已提货 5运输中 6已送达
        status_list = [
            ("0", "全部"),
            ("1", "待排产"),
            ("2", "生产中"),
            ("3", "已入库"),
            ("4", "已提货"),
            ("5", "运输中"),
            ("6", "已送达"),
        ]

        for status_code, status_name in status_list:
            # 按状态查询订单列表
            res = DD.get_order_list(isManage=True, queryStatus=status_code, pageNo="1", pageSize="10")
            assert res.get("code") == "10001200", \
                f"查询{status_name}状态订单失败, 接口返回={res}"
            data = res.get("data", {})
            assert isinstance(data, dict), \
                f"{status_name}状态data类型异常, 期望dict, 实际={type(data)}"
