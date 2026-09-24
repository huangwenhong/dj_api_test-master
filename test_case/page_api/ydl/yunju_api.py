# -*- coding: utf-8 -*-
"""易单来 - 运距配置相关接口"""

import allure
from test_case.page_api.public.base_api import BaseAPI


class YdlAPI(BaseAPI):
    """易单来接口封装"""

    def __init__(self, base_url=None, headers=None, cookies=None):
        super().__init__(base_url, headers, cookies)
        # 易单来默认业务头
        biz_headers = {
            "device": "web",
            "source": "easy_order",
            "version": "2.3.5",
            "Content-Type": "application/json",
        }
        self.headers.update(biz_headers)

    @allure.step("查询运距配置列表")
    def get_delivery_distance_config_list(self, customerId="", customerPhone="",
                                          consignee="", consigneePhone="",
                                          pageNo=1, pageSize=15,
                                          status_code=200, **kwargs):
        """查询客户运距配置列表"""
        # Author: Author
        # Create Date: 2026-06-23
        # IsAI: True
        url = "/djsupplier/DJEASYORDER/customer/getDeliveryDistanceConfigList.do"
        payload = {
            "customerId": customerId,
            "customerPhone": customerPhone,
            "consignee": consignee,
            "consigneePhone": consigneePhone,
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        error_msg = kwargs.pop("error_msg", "查询运距配置列表失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("获取理论配送距离")
    def get_theoretical_delivery_distance(self, addressId, longAndLat, id="", status_code=200, **kwargs):
        """根据地址ID和经纬度计算理论配送距离"""
        # Author: Author
        # Create Date: 2026-06-23
        # IsAI: True
        url = "/djsupplier/DJEASYORDER/customer/getTheoreticalDeliveryDistance.do"
        payload = {
            "id": id,
            "addressId": addressId,
            "longAndLat": longAndLat,
        }
        error_msg = kwargs.pop("error_msg", "获取理论配送距离失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("编辑配送距离")
    def edit_delivery_distance(self, id, addressId, deliveryDistance, status_code=200, **kwargs):
        """编辑/保存客户配送距离配置"""
        # Author: Author
        # Create Date: 2026-06-23
        # IsAI: True
        url = "/djsupplier/DJEASYORDER/customer/editDeliveryDistance.do"
        payload = {
            "id": id,
            "addressId": addressId,
            "deliveryDistance": deliveryDistance,
        }
        error_msg = kwargs.pop("error_msg", "编辑配送距离失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res


