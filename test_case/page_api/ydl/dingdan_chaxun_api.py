# -*- coding: utf-8 -*-
"""易单来 - APP 订单查询接口（基于驾驶舱swaggerApi.json）"""

import allure
from test_case.page_api.public.base_api import BaseAPI

# APP 订单查询接口网关路径
SALESMAN_PREFIX = "/djsupplier/app/djcockpit/easyorder/salesman"


class DingdanChaxunAPI(BaseAPI):
    """易单来 APP 订单查询接口封装"""

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

    @allure.step("客户订单搜索-今日订单列表")
    def get_today_order_list(self, customerId, orderStatus=None, orderId=None,
                             productName=None, productId=None, cartonLength=None,
                             cartonWidth=None, cartonHeight=None, materialLength=None,
                             materialWidth=None, timeType=None, pageDate=None,
                             beginDate=None, endDate=None, orderMarkList=None,
                             receiver=None, materialName=None, layerId=None,
                             fluteType=None, orgId=None, supplierId=None,
                             dataOwnership=None, dataType=None, type=None,
                             pageNo=None, pageSize=None,
                             status_code=200, **kwargs):
        """客户订单搜索-今日订单列表

        swagger 入参:
          必填: customerId
          可选: orderStatus, orderId, productName, productId, cartonLength,
                cartonWidth, cartonHeight, materialLength, materialWidth,
                timeType, pageDate, beginDate, endDate, orderMarkList,
                receiver, materialName, layerId, fluteType, orgId,
                supplierId, dataOwnership, dataType, type, pageNo, pageSize
        swagger 返参 data: {list, total}
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getTodayOrderList.do"
        payload = {"customerId": customerId}
        if orderStatus is not None:
            payload["orderStatus"] = orderStatus
        if orderId is not None:
            payload["orderId"] = orderId
        if productName is not None:
            payload["productName"] = productName
        if productId is not None:
            payload["productId"] = productId
        if cartonLength is not None:
            payload["cartonLength"] = cartonLength
        if cartonWidth is not None:
            payload["cartonWidth"] = cartonWidth
        if cartonHeight is not None:
            payload["cartonHeight"] = cartonHeight
        if materialLength is not None:
            payload["materialLength"] = materialLength
        if materialWidth is not None:
            payload["materialWidth"] = materialWidth
        if timeType is not None:
            payload["timeType"] = timeType
        if pageDate is not None:
            payload["pageDate"] = pageDate
        if beginDate is not None:
            payload["beginDate"] = beginDate
        if endDate is not None:
            payload["endDate"] = endDate
        if orderMarkList is not None:
            payload["orderMarkList"] = orderMarkList
        if receiver is not None:
            payload["receiver"] = receiver
        if materialName is not None:
            payload["materialName"] = materialName
        if layerId is not None:
            payload["layerId"] = layerId
        if fluteType is not None:
            payload["fluteType"] = fluteType
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
        if pageNo is not None:
            payload["pageNo"] = pageNo
        if pageSize is not None:
            payload["pageSize"] = pageSize
        error_msg = kwargs.pop("error_msg", "客户订单搜索-今日订单列表查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("订单查询搜索")
    def get_order_list_search(self, beginDate, endDate, isManage=None,
                              customerName=None, queryStatus=None,
                              orderStatus=None, orderId=None,
                              productName=None, cartonLength=None,
                              cartonWidth=None, cartonHeight=None,
                              materialLength=None, materialWidth=None,
                              timeType=None, orderMarkList=None,
                              receiver=None, materialName=None,
                              layerId=None, fluteType=None, orgId=None,
                              supplierId=None, dataOwnership=None,
                              dataType=None, type=None, pageNo=None,
                              pageSize=None,
                              status_code=200, **kwargs):
        """订单查询搜索

        swagger 入参:
          必填: beginDate, endDate
          可选: isManage, customerName, queryStatus, orderStatus, orderId,
                productName, cartonLength, cartonWidth, cartonHeight,
                materialLength, materialWidth, timeType, orderMarkList,
                receiver, materialName, layerId, fluteType, orgId,
                supplierId, dataOwnership, dataType, type, pageNo, pageSize
        swagger 返参 data: {list, total}
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getOrderListSearch.do"
        payload = {"beginDate": beginDate, "endDate": endDate}
        if isManage is not None:
            payload["isManage"] = isManage
        if customerName is not None:
            payload["customerName"] = customerName
        if queryStatus is not None:
            payload["queryStatus"] = queryStatus
        if orderStatus is not None:
            payload["orderStatus"] = orderStatus
        if orderId is not None:
            payload["orderId"] = orderId
        if productName is not None:
            payload["productName"] = productName
        if cartonLength is not None:
            payload["cartonLength"] = cartonLength
        if cartonWidth is not None:
            payload["cartonWidth"] = cartonWidth
        if cartonHeight is not None:
            payload["cartonHeight"] = cartonHeight
        if materialLength is not None:
            payload["materialLength"] = materialLength
        if materialWidth is not None:
            payload["materialWidth"] = materialWidth
        if timeType is not None:
            payload["timeType"] = timeType
        if orderMarkList is not None:
            payload["orderMarkList"] = orderMarkList
        if receiver is not None:
            payload["receiver"] = receiver
        if materialName is not None:
            payload["materialName"] = materialName
        if layerId is not None:
            payload["layerId"] = layerId
        if fluteType is not None:
            payload["fluteType"] = fluteType
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
        if pageNo is not None:
            payload["pageNo"] = pageNo
        if pageSize is not None:
            payload["pageSize"] = pageSize
        error_msg = kwargs.pop("error_msg", "订单查询搜索失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("查询订单列表")
    def get_order_list(self, isManage=True, queryStatus="0", dataOwnership="",
                       pageNo="1", pageSize="20", status_code=200, **kwargs):
        """查询订单列表（按客户分组）

        抓包入参:
          isManage: 是否管理员视角（默认True）
          queryStatus: 查询状态（默认0）
          dataOwnership: 数据归属（默认空）
          pageNo: 页码（默认1）
          pageSize: 每页大小（默认20）
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getOrderList.do"
        payload = {
            "isManage": isManage,
            "queryStatus": queryStatus,
            "dataOwnership": dataOwnership,
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        error_msg = kwargs.pop("error_msg", "查询订单列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("查询订单详情")
    def get_order_info(self, orderId, groupImportSign="1", orderType="1",
                       status_code=200, **kwargs):
        """查询订单详情

        抓包入参:
          orderId: 订单ID
          groupImportSign: 分组导入标识（默认1）
          orderType: 订单类型（默认1）
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getOrderInfo.do"
        payload = {
            "orderId": orderId,
            "groupImportSign": groupImportSign,
            "orderType": orderType,
        }
        error_msg = kwargs.pop("error_msg", "查询订单详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("查询订单进度")
    def get_order_info_schedule(self, orderId, status_code=200, **kwargs):
        """查询订单进度（生产/支付）

        抓包入参:
          orderId: 订单ID
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getOrderInfoSchedule.do"
        payload = {"orderId": orderId}
        error_msg = kwargs.pop("error_msg", "查询订单进度失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取层列表")
    def get_layer_list(self, status_code=200, **kwargs):
        """获取层列表（筛选项）

        抓包入参: 无必填参数
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getLayerList.do"
        payload = {}
        error_msg = kwargs.pop("error_msg", "获取层列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
