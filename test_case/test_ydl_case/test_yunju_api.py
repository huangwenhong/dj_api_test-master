# -*- coding: utf-8 -*-
"""易单来 - 客户运距配置用例"""

import allure
import pytest
from test_case.page_api.ydl.yunju_api import YdlAPI

YD = YdlAPI()


@allure.feature("客户运距配置")
class TestCustomerDeliveryDistance:

    @allure.story("客户运距配置 - 完整业务流")
    def test_ydl_AA_customer_delivery_distance_config(self):
        """客户运距配置：查询列表→获取理论距离→编辑距离→验证更新"""
        # Author: Author
        # Create Date: 2026-06-23
        # IsAI: True

        # 1. 查询客户运距配置列表（初始查询）
        res_list = YD.get_delivery_distance_config_list()
        assert res_list.get("code") == "10001200"
        assert res_list.get("success") is True
        assert res_list.get("data", {}).get("total", 0) >= 0
        assert isinstance(res_list.get("data", {}).get("list"), list)

        # 2. 从列表中取第一个客户ID，查询该客户详情
        first_customers = res_list.get("data", {}).get("list", [])
        if not first_customers:
            pytest.skip("列表为空，跳过后续步骤")

        # 从首次查询结果中找出一个有地址信息的客户
        target_customer = None
        for cust in first_customers:
            addr_list = cust.get("recivingInfoList", [])
            if addr_list and addr_list[0].get("id"):
                target_customer = cust
                break

        if not target_customer:
            # 没有找到有地址的客户，尝试用抓包中的客户ID
            customer_id = "56b531bfea744dc38819d7744d77bca1"
        else:
            customer_id = target_customer.get("customerId", "")

        # 3. 按客户ID查询详细信息
        res_detail = YD.get_delivery_distance_config_list(customerId=customer_id)
        assert res_detail.get("code") == "10001200"
        assert res_detail.get("success") is True
        detail_list = res_detail.get("data", {}).get("list", [])
        assert len(detail_list) > 0

        # 4. 获取该客户的地址信息
        detail_customer = detail_list[0]
        addr_list = detail_customer.get("recivingInfoList", [])
        if not addr_list or not addr_list[0].get("id"):
            pytest.skip("该客户没有收货地址信息，跳过后续步骤")

        address_info = addr_list[0]
        address_id = address_info.get("id")
        long_and_lat = address_info.get("longAndLat")
        distance_id = address_info.get("distanceId", "")

        # 5. 获取理论配送距离
        res_theory = YD.get_theoretical_delivery_distance(
            addressId=address_id,
            longAndLat=long_and_lat,
            id=distance_id or "",
        )
        assert res_theory.get("code") == "10001200"
        assert res_theory.get("success") is True
        theoretical_distance = res_theory.get("data")
        assert theoretical_distance is not None
        assert isinstance(theoretical_distance, (int, float))

        # 6. 再次查询确认distanceId已生成
        res_after_theory = YD.get_delivery_distance_config_list(customerId=customer_id)
        assert res_after_theory.get("code") == "10001200"
        after_list = res_after_theory.get("data", {}).get("list", [])
        if after_list:
            new_addr_list = after_list[0].get("recivingInfoList", [])
            if new_addr_list and new_addr_list[0].get("distanceId"):
                distance_id = new_addr_list[0]["distanceId"]

        # 7. 编辑配送距离
        new_distance = str(round(float(theoretical_distance) * 1.2, 0))  # 在理论距离基础上略微上调
        res_edit = YD.edit_delivery_distance(
            id=distance_id,
            addressId=address_id,
            deliveryDistance=new_distance,
        )
        assert res_edit.get("code") == "10001200"
        assert res_edit.get("success") is True

        # 8. 查询验证更新结果
        res_verify = YD.get_delivery_distance_config_list(customerId=customer_id)
        assert res_verify.get("code") == "10001200"
        verify_list = res_verify.get("data", {}).get("list", [])
        if verify_list:
            verify_addr = verify_list[0].get("recivingInfoList", [])
            if verify_addr:
                updated_distance = verify_addr[0].get("deliveryDistance", "")
                assert updated_distance == new_distance, \
                    f"配送距离未正确更新, 期望={new_distance}, 实际={updated_distance}"
