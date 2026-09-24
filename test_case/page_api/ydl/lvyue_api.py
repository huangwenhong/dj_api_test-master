# -*- coding: utf-8 -*-
"""易单来 - APP 履约接口（基于驾驶舱swaggerApi.json）"""

import allure
import conftest
from test_case.page_api.public.base_api import BaseAPI

# APP 履约接口网关路径
FULFILLMENT_PREFIX = "/djsupplier/app/djcockpit/fulfillment"
# 履约模块使用 cpsol.net 域名
CPSOL_BASE_URL = "https://suppliertest.cpsol.net"


class LvyueAPI(BaseAPI):
    """易单来 APP 履约接口封装（使用 cpsol.net 域名）"""

    def __init__(self, base_url=None, headers=None, cookies=None):
        # 默认使用 cpsol.net 域名
        super().__init__(base_url or CPSOL_BASE_URL, headers, cookies)
        biz_headers = {
            "device": "app",
            "source": "easy_order",
            "version": "2.3.7",
            "Content-Type": "application/json",
        }
        if self.headers:
            self.headers.update(biz_headers)
        else:
            self.headers = biz_headers
        # 使用 cpsol.net 的 token
        cpsol_tok = conftest.cpsol_token.get("token", "")
        if cpsol_tok:
            self.cookies["token"] = cpsol_tok
            self._extra_cookies["token"] = cpsol_tok

    @allure.step("获取履约概览")
    def get_overview(self, salesmanName=None, customerName=None, orderId=None,
                     orgId=None, supplierId=None, dataOwnership=None,
                     dataType=None, type=None, beginDate=None, endDate=None,
                     pageNo=None, pageSize=None,
                     status_code=200, **kwargs):
        """获取履约概览

        swagger 入参:
          可选: salesmanName, customerName, orderId, orgId, supplierId,
                dataOwnership, dataType, type, beginDate, endDate,
                pageNo, pageSize
        swagger 返参 data: GetOverviewVo
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{FULFILLMENT_PREFIX}/getOverview.do"
        payload = {}
        if salesmanName is not None:
            payload["salesmanName"] = salesmanName
        if customerName is not None:
            payload["customerName"] = customerName
        if orderId is not None:
            payload["orderId"] = orderId
        if orgId is not None:
            payload["orgId"] = orgId
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if dataOwnership is not None:
            payload["dataOwnership"] = dataOwnership
        if dataType is not None:
            payload["dataType"] = dataType
        if type is not None:
            payload["type"] = type
        if beginDate is not None:
            payload["beginDate"] = beginDate
        if endDate is not None:
            payload["endDate"] = endDate
        if pageNo is not None:
            payload["pageNo"] = pageNo
        if pageSize is not None:
            payload["pageSize"] = pageSize
        error_msg = kwargs.pop("error_msg", "获取履约概览失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("按天汇总")
    def get_daily_summary(self, filterType=None, dimensionType=None,
                          salesmanName=None, customerName=None, orderId=None,
                          orgId=None, supplierId=None, dataOwnership=None,
                          dataType=None, type=None, beginDate=None,
                          endDate=None, pageNo=None, pageSize=None,
                          status_code=200, **kwargs):
        """按天汇总

        swagger 入参:
          可选: filterType(1:超24H,2:超48H,3:催单), dimensionType(1-送达,2-出库),
                salesmanName, customerName, orderId, orgId, supplierId,
                dataOwnership, dataType, type, beginDate, endDate,
                pageNo, pageSize
        swagger 返参 data: GetDailySummaryVo
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{FULFILLMENT_PREFIX}/getDailySummary.do"
        payload = {}
        if filterType is not None:
            payload["filterType"] = filterType
        if dimensionType is not None:
            payload["dimensionType"] = dimensionType
        if salesmanName is not None:
            payload["salesmanName"] = salesmanName
        if customerName is not None:
            payload["customerName"] = customerName
        if orderId is not None:
            payload["orderId"] = orderId
        if orgId is not None:
            payload["orgId"] = orgId
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if dataOwnership is not None:
            payload["dataOwnership"] = dataOwnership
        if dataType is not None:
            payload["dataType"] = dataType
        if type is not None:
            payload["type"] = type
        if beginDate is not None:
            payload["beginDate"] = beginDate
        if endDate is not None:
            payload["endDate"] = endDate
        if pageNo is not None:
            payload["pageNo"] = pageNo
        if pageSize is not None:
            payload["pageSize"] = pageSize
        error_msg = kwargs.pop("error_msg", "按天汇总查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("履约订单查询")
    def get_order_list(self, timeType, filterType, queryStatus=None,
                       notDelivered=None, customerName=None, orderId=None,
                       dimensionType=None, salesmanName=None, orgId=None,
                       supplierId=None, dataOwnership=None, dataType=None,
                       type=None, beginDate=None, endDate=None,
                       pageNo=None, pageSize=None,
                       status_code=200, **kwargs):
        """履约订单查询

        swagger 入参:
          必填: timeType(0:创建时间,1:支付时间), filterType(1:超24H,2:超48H,3:催单)
          可选: queryStatus, notDelivered, customerName, orderId,
                dimensionType(1-送达,2-出库), salesmanName, orgId,
                supplierId, dataOwnership, dataType, type, beginDate,
                endDate, pageNo, pageSize
        swagger 返参 data: FulfillmentOrderPageResult
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{FULFILLMENT_PREFIX}/getOrderList.do"
        payload = {"timeType": timeType, "filterType": filterType}
        if queryStatus is not None:
            payload["queryStatus"] = queryStatus
        if notDelivered is not None:
            payload["notDelivered"] = notDelivered
        if customerName is not None:
            payload["customerName"] = customerName
        if orderId is not None:
            payload["orderId"] = orderId
        if dimensionType is not None:
            payload["dimensionType"] = dimensionType
        if salesmanName is not None:
            payload["salesmanName"] = salesmanName
        if orgId is not None:
            payload["orgId"] = orgId
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if dataOwnership is not None:
            payload["dataOwnership"] = dataOwnership
        if dataType is not None:
            payload["dataType"] = dataType
        if type is not None:
            payload["type"] = type
        if beginDate is not None:
            payload["beginDate"] = beginDate
        if endDate is not None:
            payload["endDate"] = endDate
        if pageNo is not None:
            payload["pageNo"] = pageNo
        if pageSize is not None:
            payload["pageSize"] = pageSize
        error_msg = kwargs.pop("error_msg", "履约订单查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("履约订单查询数量")
    def get_order_number(self, queryStatus=None, notDelivered=None,
                         customerName=None, orderId=None, timeType=None,
                         filterType=None, dimensionType=None,
                         salesmanName=None, orgId=None, supplierId=None,
                         dataOwnership=None, dataType=None, type=None,
                         beginDate=None, endDate=None, pageNo=None,
                         pageSize=None,
                         status_code=200, **kwargs):
        """履约订单查询数量

        swagger 入参:
          可选: queryStatus, notDelivered, customerName, orderId, timeType,
                filterType(1:超24H,2:超48H,3:催单), dimensionType(1-送达,2-出库),
                salesmanName, orgId, supplierId, dataOwnership, dataType,
                type, beginDate, endDate, pageNo, pageSize
        swagger 返参 data: FulfillmentOrderNumberVo
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{FULFILLMENT_PREFIX}/getOrderNumber.do"
        payload = {}
        if queryStatus is not None:
            payload["queryStatus"] = queryStatus
        if notDelivered is not None:
            payload["notDelivered"] = notDelivered
        if customerName is not None:
            payload["customerName"] = customerName
        if orderId is not None:
            payload["orderId"] = orderId
        if timeType is not None:
            payload["timeType"] = timeType
        if filterType is not None:
            payload["filterType"] = filterType
        if dimensionType is not None:
            payload["dimensionType"] = dimensionType
        if salesmanName is not None:
            payload["salesmanName"] = salesmanName
        if orgId is not None:
            payload["orgId"] = orgId
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if dataOwnership is not None:
            payload["dataOwnership"] = dataOwnership
        if dataType is not None:
            payload["dataType"] = dataType
        if type is not None:
            payload["type"] = type
        if beginDate is not None:
            payload["beginDate"] = beginDate
        if endDate is not None:
            payload["endDate"] = endDate
        if pageNo is not None:
            payload["pageNo"] = pageNo
        if pageSize is not None:
            payload["pageSize"] = pageSize
        error_msg = kwargs.pop("error_msg", "履约订单查询数量失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取交付趋势")
    def get_delivery_trend(self, dimensionType, salesmanName=None,
                           customerName=None, orderId=None, orgId=None,
                           supplierId=None, dataOwnership=None,
                           dataType=None, type=None, beginDate=None,
                           endDate=None, pageNo=None, pageSize=None,
                           status_code=200, **kwargs):
        """获取交付趋势

        swagger 入参:
          必填: dimensionType(1-送达,2-出库)
          可选: salesmanName, customerName, orderId, orgId, supplierId,
                dataOwnership, dataType, type, beginDate, endDate,
                pageNo, pageSize
        swagger 返参 data: GetDeliveryTrendVo
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{FULFILLMENT_PREFIX}/getDeliveryTrend.do"
        payload = {"dimensionType": dimensionType}
        if salesmanName is not None:
            payload["salesmanName"] = salesmanName
        if customerName is not None:
            payload["customerName"] = customerName
        if orderId is not None:
            payload["orderId"] = orderId
        if orgId is not None:
            payload["orgId"] = orgId
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if dataOwnership is not None:
            payload["dataOwnership"] = dataOwnership
        if dataType is not None:
            payload["dataType"] = dataType
        if type is not None:
            payload["type"] = type
        if beginDate is not None:
            payload["beginDate"] = beginDate
        if endDate is not None:
            payload["endDate"] = endDate
        if pageNo is not None:
            payload["pageNo"] = pageNo
        if pageSize is not None:
            payload["pageSize"] = pageSize
        error_msg = kwargs.pop("error_msg", "获取交付趋势失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取区域交付")
    def get_regional_delivery(self, dimensionType=None, salesmanName=None,
                              customerName=None, orderId=None, filterType=None,
                              orgId=None, supplierId=None, dataOwnership=None,
                              dataType=None, type=None, beginDate=None,
                              endDate=None, pageNo=None, pageSize=None,
                              status_code=200, **kwargs):
        """获取区域交付

        swagger 入参:
          可选: dimensionType(1-送达,2-出库), salesmanName, customerName,
                orderId, filterType(1-24H,2-48H), orgId, supplierId,
                dataOwnership, dataType, type, beginDate, endDate,
                pageNo, pageSize
        swagger 返参 data: GetRegionalDeliveryVo
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{FULFILLMENT_PREFIX}/getRegionalDelivery.do"
        payload = {}
        if dimensionType is not None:
            payload["dimensionType"] = dimensionType
        if salesmanName is not None:
            payload["salesmanName"] = salesmanName
        if customerName is not None:
            payload["customerName"] = customerName
        if orderId is not None:
            payload["orderId"] = orderId
        if filterType is not None:
            payload["filterType"] = filterType
        if orgId is not None:
            payload["orgId"] = orgId
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if dataOwnership is not None:
            payload["dataOwnership"] = dataOwnership
        if dataType is not None:
            payload["dataType"] = dataType
        if type is not None:
            payload["type"] = type
        if beginDate is not None:
            payload["beginDate"] = beginDate
        if endDate is not None:
            payload["endDate"] = endDate
        if pageNo is not None:
            payload["pageNo"] = pageNo
        if pageSize is not None:
            payload["pageSize"] = pageSize
        error_msg = kwargs.pop("error_msg", "获取区域交付失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
