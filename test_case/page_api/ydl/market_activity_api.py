# -*- coding: utf-8 -*-
"""易单来 - 营销活动模块相关接口（系统级公共功能，跨业务域复用）"""

import time
from datetime import datetime, timedelta

import allure
from test_case.page_api.public.base_api import BaseAPI


def _shift_minutes(minutes):
    """当前时间偏移 minutes 分钟，格式 YYYY-MM-DD HH:MM:SS"""
    return (datetime.now() + timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")


class YdlAPI(BaseAPI):
    """易单来营销活动接口封装"""

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

    @allure.step("过滤活动产品")
    def filter_activity_product(self, productIds, supplierId=None,
                                activityStartTime=None, activityEndTime=None,
                                status_code=200, **kwargs):
        """按活动时间过滤已存在活动的产品（productIds 为易网产品UUID列表）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = "/djsupplier/marketingActivity/eo/filterActivityProduct.do"
        payload = {
            "supplierId": supplierId,
            "activityStartTime": activityStartTime or _shift_minutes(10),
            "activityEndTime": activityEndTime or _shift_minutes(180),
            "productIds": productIds,
        }
        error_msg = kwargs.pop("error_msg", "过滤活动产品失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询供应商销售区域列表")
    def find_supplier_sales_area_list(self, supplierId=None, status_code=200, **kwargs):
        """查询供应商可选销售区域（省/市/县三级）列表"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = "/djsupplier/marketingActivity/eo/findSupplierSalesAreaList.do"
        payload = {
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "查询供应商销售区域列表失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询营销活动详情")
    def find_market_activity_details(self, marketActivityId, status_code=200, **kwargs):
        """按活动ID查询营销活动详情"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = "/djsupplier/marketingActivity/eo/findMarketActivityDetails.do"
        payload = {
            "marketActivityId": marketActivityId,
        }
        error_msg = kwargs.pop("error_msg", "查询营销活动详情失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("更新营销活动")
    def update_market_activity(self, id, activityGoodsList, marketingActivityName=None,
                               activityStartTime=None, activityEndTime=None, supplierId=None,
                               strategyId="", activityType="according_area",
                               usersParticipateType="all_user_participate", isTop="n",
                               preferentialTypeList=None, status_code=200, **kwargs):
        """更新已有营销活动"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = "/djsupplier/marketingActivity/eo/updateMarketActivity.do"
        payload = {
            "id": id,
            "marketingActivityName": marketingActivityName or "ai" + time.strftime("%Y%m%d%H%M%S"),
            "activityStartTime": activityStartTime or _shift_minutes(10),
            "activityEndTime": activityEndTime or _shift_minutes(180),
            "activityType": activityType,
            "usersParticipateType": usersParticipateType,
            "isTop": isTop,
            "preferentialTypeList": preferentialTypeList if preferentialTypeList is not None else [4, 3, 2],
            "activityGoodsList": activityGoodsList,
            "supplierId": supplierId,
            "strategyId": strategyId,
        }
        error_msg = kwargs.pop("error_msg", "更新营销活动失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询已有层数楞型选项")
    def load_exist_layer_and_flute(self, supplierId=None, status_code=200, **kwargs):
        """查询活动选品用的已有层数/楞型级联选项"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = "/djsupplier/marketingActivity/eo/loadExistLayerAndFlute.do"
        payload = {
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "查询已有层数楞型选项失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("分页查询团购产品列表")
    def select_group_product_page_list(self, supplierId=None, pageNo=1, pageSize=15,
                                       productIdList=None, activityStartTime=None,
                                       activityEndTime=None, marketActivityId="",
                                       status_code=200, **kwargs):
        """分页查询可参加团购活动的产品列表（productId 为易网产品UUID）

        返回参数说明：list 行内 ifChoose (Integer) 表示产品是否可选，
        取值 0=可选（可加入活动），1=不可选（已参与活动或不满足活动条件）。
        """
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = "/djsupplier/marketingActivity/eo/selectGroupProductPageList.do"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "productIdList": productIdList if productIdList is not None else [],
            "activityStartTime": activityStartTime or _shift_minutes(10),
            "activityEndTime": activityEndTime or _shift_minutes(180),
            "marketActivityId": marketActivityId,
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "分页查询团购产品列表失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询产品名称选项")
    def find_product_names(self, supplierId=None, onoffStatus=2, status_code=200, **kwargs):
        """查询活动选品用的产品名称选项（fid 为易网产品UUID）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = "/djsupplier/marketingActivity/eo/findProductNames.do"
        payload = {
            "onoffStatus": onoffStatus,
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "查询产品名称选项失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("分页查询营销活动列表")
    def find_market_activity_page_list(self, supplierId=None, supplierIdOb=None,
                                       pageNo=1, pageSize=15, status_code=200, **kwargs):
        """分页查询营销活动列表（返回 marketActivityId/activityStatus 等）"""
        # Author: Author
        # Create Date: 2026-09-21
        # IsAI: True
        url = "/djsupplier/marketingActivity/findMarketActivityPageList.do"
        payload = {
            "supplierIdOb": supplierIdOb if supplierIdOb is not None else {"supplierId": supplierId},
            "pageNo": pageNo,
            "pageSize": pageSize,
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "分页查询营销活动列表失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res
