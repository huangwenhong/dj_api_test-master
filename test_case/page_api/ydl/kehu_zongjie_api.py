# -*- coding: utf-8 -*-
"""易单来 - APP 工作台-客户总结模块接口（基于 APP 抓包）"""

import allure
from test_case.page_api.public.base_api import BaseAPI

# APP 客户总结模块路径前缀（抓包）
APP_CUSTOMER_PREFIX = "/djsupplier/app/djcockpit/easyorder"


class KehuZongjieAPI(BaseAPI):
    """易单来 APP 客户总结模块接口封装"""

    def __init__(self, base_url=None, headers=None, cookies=None):
        super().__init__(base_url, headers, cookies)
        biz_headers = {
            "device": "app",
            "source": "easy_order",
            "version": "2.3.5",
            "Content-Type": "application/json",
        }
        if self.headers:
            self.headers.update(biz_headers)
        else:
            self.headers = biz_headers

    @allure.step("获取客户信息总览")
    def get_customer_info(self, orgId, supplierId, beginDate, endDate, type="1",
                          dataOwnership="", status_code=200, **kwargs):
        """获取客户信息总览（getCustomerInfo.do）

        抓包入参:
          orgId: 组织ID
          supplierId: 供应商ID
          beginDate: 开始日期
          endDate: 结束日期
          type: 类型（默认1）
          dataOwnership: 数据归属（默认空）
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{APP_CUSTOMER_PREFIX}/manage/getCustomerInfo.do"
        payload = {
            "orgId": orgId,
            "supplierId": supplierId,
            "beginDate": beginDate,
            "endDate": endDate,
            "type": type,
            "dataOwnership": dataOwnership,
        }
        error_msg = kwargs.pop("error_msg", "获取客户信息总览失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取重点关注客户列表")
    def get_customer_list(self, orgId, supplierId, status_code=200, **kwargs):
        """获取重点关注客户列表（getCustomerList.do）

        抓包入参:
          orgId: 组织ID
          supplierId: 供应商ID
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{APP_CUSTOMER_PREFIX}/keyAttention/getCustomerList.do"
        payload = {
            "orgId": orgId,
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "获取重点关注客户列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("根据ID获取客户详情")
    def get_customer_info_by_id(self, orgId, supplierId, customerId, dataOwnership="",
                                status_code=200, **kwargs):
        """根据ID获取客户详情（getCustomerInfoById.do）

        抓包入参:
          orgId: 组织ID
          supplierId: 供应商ID
          customerId: 客户ID
          dataOwnership: 数据归属（默认空）
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{APP_CUSTOMER_PREFIX}/salesman/getCustomerInfoById.do"
        payload = {
            "orgId": orgId,
            "supplierId": supplierId,
            "customerId": customerId,
            "dataOwnership": dataOwnership,
        }
        error_msg = kwargs.pop("error_msg", "根据ID获取客户详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户订单趋势")
    def get_customer_order_trend(self, orgId, supplierId, customerId, beginDate, endDate,
                                 type="3", dataOwnership="", status_code=200, **kwargs):
        """获取客户订单趋势（getCustomerOrderTrend.do）

        抓包入参:
          orgId: 组织ID
          supplierId: 供应商ID
          customerId: 客户ID
          beginDate: 开始日期
          endDate: 结束日期
          type: 类型（默认3）
          dataOwnership: 数据归属（默认空）
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{APP_CUSTOMER_PREFIX}/salesman/getCustomerOrderTrend.do"
        payload = {
            "orgId": orgId,
            "supplierId": supplierId,
            "customerId": customerId,
            "beginDate": beginDate,
            "endDate": endDate,
            "type": type,
            "dataOwnership": dataOwnership,
        }
        error_msg = kwargs.pop("error_msg", "获取客户订单趋势失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户视图")
    def get_customer_view(self, orgId, supplierId, customerId, beginDate, endDate,
                          type=3, productId="", dataOwnership="", status_code=200, **kwargs):
        """获取客户视图（getCustomerView.do）

        抓包入参:
          orgId: 组织ID
          supplierId: 供应商ID
          customerId: 客户ID
          beginDate: 开始日期
          endDate: 结束日期
          type: 类型（默认3）
          productId: 产品ID（默认空）
          dataOwnership: 数据归属（默认空）
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{APP_CUSTOMER_PREFIX}/salesman/getCustomerView.do"
        payload = {
            "orgId": orgId,
            "supplierId": supplierId,
            "customerId": customerId,
            "beginDate": beginDate,
            "endDate": endDate,
            "type": type,
            "productId": productId,
            "dataOwnership": dataOwnership,
        }
        error_msg = kwargs.pop("error_msg", "获取客户视图失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户预警概览数量")
    def get_customer_warn_overview_num(self, supplierId, beginDate, endDate,
                                       type="3", status_code=200, **kwargs):
        """获取客户预警概览数量（getCustomerWarnOverviewNum.do）

        抓包入参:
          supplierId: 供应商ID
          beginDate: 开始日期
          endDate: 结束日期
          type: 类型（默认3）
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{APP_CUSTOMER_PREFIX}/salesman/getCustomerWarnOverviewNum.do"
        payload = {
            "supplierId": supplierId,
            "beginDate": beginDate,
            "endDate": endDate,
            "type": type,
        }
        error_msg = kwargs.pop("error_msg", "获取客户预警概览数量失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取AI客户订单预测")
    def get_customer_order_prediction(self, supplierId, beginDate, endDate,
                                      predictionType="timeout_no_orders", type="1",
                                      pageNo=1, pageSize=9999, status_code=200, **kwargs):
        """获取AI客户订单预测（getCustomerOrderPrediction.do）

        抓包入参:
          supplierId: 供应商ID
          beginDate: 开始日期
          endDate: 结束日期
          predictionType: 预测类型（默认timeout_no_orders）
          type: 类型（默认1）
          pageNo: 页码（默认1）
          pageSize: 每页大小（默认9999）
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{APP_CUSTOMER_PREFIX}/ai/getCustomerOrderPrediction.do"
        payload = {
            "supplierId": supplierId,
            "beginDate": beginDate,
            "endDate": endDate,
            "predictionType": predictionType,
            "type": type,
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        error_msg = kwargs.pop("error_msg", "获取AI客户订单预测失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户预警概览列表")
    def get_customer_warn_overview(self, supplierId, beginDate, endDate, state,
                                   type="3", pageNo=1, pageSize=10, status_code=200, **kwargs):
        """获取客户预警概览列表（getCustomerWarnOverview.do）

        抓包入参:
          supplierId: 供应商ID
          beginDate: 开始日期
          endDate: 结束日期
          state: 状态（no_order未下单/loss流失/add新增/activate激活/active活跃）
          type: 类型（默认3）
          pageNo: 页码（默认1）
          pageSize: 每页大小（默认10）
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{APP_CUSTOMER_PREFIX}/salesman/getCustomerWarnOverview.do"
        payload = {
            "supplierId": supplierId,
            "beginDate": beginDate,
            "endDate": endDate,
            "state": state,
            "type": type,
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        error_msg = kwargs.pop("error_msg", "获取客户预警概览列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
