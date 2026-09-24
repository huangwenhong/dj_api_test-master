# -*- coding: utf-8 -*-
"""易单来 - 数智拿单-销售策略/策略效果接口（基于易单来swaggerApi.json）"""

import allure
from test_case.page_api.public.base_api import BaseAPI

# 来自 swagger 2.0 的 basePath，DJEASYORDER 路径统一加 /djsupplier 前缀
SALE_STRATEGY_PREFIX = "/djsupplier/DJEASYORDER/szorder/saleStrategy"


class CelueAPI(BaseAPI):
    """易单来数智拿单-销售策略接口封装"""

    def __init__(self, base_url=None, headers=None, cookies=None):
        super().__init__(base_url, headers, cookies)
        biz_headers = {
            "device": "web",
            "source": "easy_order",
            "version": "2.3.5",
            "Content-Type": "application/json",
        }
        if self.headers:
            self.headers.update(biz_headers)
        else:
            self.headers = biz_headers

    @allure.step("销售策略列表")
    def get_list(self, pageNo=1, pageSize=15,
                 operatorId=None, operatorName=None, companyId=None,
                 realCompanyId=None, supplierId=None, strategyName=None,
                 strategyType=None, productIdList=None,
                 createStartDate=None, createEndDate=None,
                 status_code=200, **kwargs):
        """销售策略列表（getList.do）

        swagger 入参:
          必填: pageNo, pageSize
          可选: operatorId(操作人id), operatorName(操作人名字),
                companyId(公司id/联合供应商id), realCompanyId(真实公司id),
                supplierId(供应商id), strategyName(策略名称), strategyType(策略类型),
                productIdList(产品id列表), createStartDate/createEndDate(yyyy-MM-dd)
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{SALE_STRATEGY_PREFIX}/getList.do"
        payload = {"pageNo": pageNo, "pageSize": pageSize}
        if operatorId is not None:
            payload["operatorId"] = operatorId
        if operatorName is not None:
            payload["operatorName"] = operatorName
        if companyId is not None:
            payload["companyId"] = companyId
        if realCompanyId is not None:
            payload["realCompanyId"] = realCompanyId
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if strategyName is not None:
            payload["strategyName"] = strategyName
        if strategyType is not None:
            payload["strategyType"] = strategyType
        if productIdList is not None:
            payload["productIdList"] = productIdList
        if createStartDate is not None:
            payload["createStartDate"] = createStartDate
        if createEndDate is not None:
            payload["createEndDate"] = createEndDate
        error_msg = kwargs.pop("error_msg", "获取销售策略列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取优惠券使用情况")
    def get_coupon_usage_list(self, strategyId, startDate, endDate,
                              pageNo=1, pageSize=15,
                              state=None, customerName=None, phone=None,
                              couponName=None, status_code=200, **kwargs):
        """获取优惠券使用情况（getCouponUsageList.do），大数据返回结果

        swagger 入参:
          必填: pageNo, pageSize, strategyId, startDate(yyyy-MM-dd), endDate(yyyy-MM-dd)
          可选: state(使用情况:1未领取/2未使用/3已使用/4已过期),
                customerName(客户名称模糊搜索), phone(手机号模糊搜索),
                couponName(优惠券名称模糊搜索)
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{SALE_STRATEGY_PREFIX}/getCouponUsageList.do"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "strategyId": strategyId,
            "startDate": startDate,
            "endDate": endDate,
        }
        if state is not None:
            payload["state"] = state
        if customerName is not None:
            payload["customerName"] = customerName
        if phone is not None:
            payload["phone"] = phone
        if couponName is not None:
            payload["couponName"] = couponName
        error_msg = kwargs.pop("error_msg", "获取优惠券使用情况失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取策略效果概览")
    def get_strategy_effect_overview(self, supplierId=None, dataOwnership=None,
                                     startDate=None, endDate=None,
                                     status_code=200, **kwargs):
        """获取策略效果概览（getStrategyEffectOverview.do）

        swagger 入参:
          可选: supplierId(供应商Id), dataOwnership(数据归属:platform平台/own自有),
                startDate(yyyy-MM-dd), endDate(yyyy-MM-dd)
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{SALE_STRATEGY_PREFIX}/getStrategyEffectOverview.do"
        payload = {}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if dataOwnership is not None:
            payload["dataOwnership"] = dataOwnership
        if startDate is not None:
            payload["startDate"] = startDate
        if endDate is not None:
            payload["endDate"] = endDate
        error_msg = kwargs.pop("error_msg", "获取策略效果概览失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户策略的下单客户分布")
    def get_customer_strategy_segments_ratio(self, supplierId=None, dataOwnership=None,
                                             startDate=None, endDate=None,
                                             status_code=200, **kwargs):
        """获取客户策略的下单客户分布（getCustomerStrategySegmentsRatio.do）

        swagger 入参:
          可选: supplierId(供应商Id), dataOwnership(数据归属:platform平台/own自有),
                startDate(yyyy-MM-dd), endDate(yyyy-MM-dd)
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{SALE_STRATEGY_PREFIX}/getCustomerStrategySegmentsRatio.do"
        payload = {}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if dataOwnership is not None:
            payload["dataOwnership"] = dataOwnership
        if startDate is not None:
            payload["startDate"] = startDate
        if endDate is not None:
            payload["endDate"] = endDate
        error_msg = kwargs.pop("error_msg", "获取客户策略的下单客户分布失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户策略转化")
    def get_customer_strategy_conversion_funnel(self, supplierId=None, dataOwnership=None,
                                                startDate=None, endDate=None,
                                                status_code=200, **kwargs):
        """获取客户策略转化（getCustomerStrategyConversionFunnel.do）

        swagger 入参:
          可选: supplierId(供应商Id), dataOwnership(数据归属:platform平台/own自有),
                startDate(yyyy-MM-dd), endDate(yyyy-MM-dd)
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{SALE_STRATEGY_PREFIX}/getCustomerStrategyConversionFunnel.do"
        payload = {}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if dataOwnership is not None:
            payload["dataOwnership"] = dataOwnership
        if startDate is not None:
            payload["startDate"] = startDate
        if endDate is not None:
            payload["endDate"] = endDate
        error_msg = kwargs.pop("error_msg", "获取客户策略转化失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取活动产品接单情况")
    def get_product_order_performance(self, supplierId=None, dataOwnership=None,
                                      startDate=None, endDate=None,
                                      status_code=200, **kwargs):
        """获取活动产品接单情况（getProductOrderPerformance.do）

        swagger 入参:
          可选: supplierId(供应商Id), dataOwnership(数据归属:platform平台/own自有),
                startDate(yyyy-MM-dd), endDate(yyyy-MM-dd)
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{SALE_STRATEGY_PREFIX}/getProductOrderPerformance.do"
        payload = {}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if dataOwnership is not None:
            payload["dataOwnership"] = dataOwnership
        if startDate is not None:
            payload["startDate"] = startDate
        if endDate is not None:
            payload["endDate"] = endDate
        error_msg = kwargs.pop("error_msg", "获取活动产品接单情况失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户策略效果概览")
    def get_customer_strategy_effect_overview(self, strategyId, startDate, endDate,
                                              supplierId=None, dataOwnership=None,
                                              status_code=200, **kwargs):
        """获取客户策略效果概览（getCustomerStrategyEffectOverview.do）

        swagger 入参:
          必填: strategyId, startDate(yyyy-MM-dd), endDate(yyyy-MM-dd)
          可选: supplierId(供应商id), dataOwnership(数据归属:platform平台/own自有)
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{SALE_STRATEGY_PREFIX}/getCustomerStrategyEffectOverview.do"
        payload = {"strategyId": strategyId, "startDate": startDate, "endDate": endDate}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if dataOwnership is not None:
            payload["dataOwnership"] = dataOwnership
        error_msg = kwargs.pop("error_msg", "获取客户策略效果概览失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取产品策略效果概览")
    def get_product_strategy_effect_overview(self, strategyId, startDate, endDate,
                                             supplierId=None, dataOwnership=None,
                                             status_code=200, **kwargs):
        """获取产品策略效果概览（getProductStrategyEffectOverview.do）

        swagger 入参:
          必填: strategyId, startDate(yyyy-MM-dd), endDate(yyyy-MM-dd)
          可选: supplierId(供应商id), dataOwnership(数据归属:platform平台/own自有)
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{SALE_STRATEGY_PREFIX}/getProductStrategyEffectOverview.do"
        payload = {"strategyId": strategyId, "startDate": startDate, "endDate": endDate}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if dataOwnership is not None:
            payload["dataOwnership"] = dataOwnership
        error_msg = kwargs.pop("error_msg", "获取产品策略效果概览失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
