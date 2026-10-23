# -*- coding: utf-8 -*-
"""易单来 - 数智拿单接口"""

import time
from datetime import datetime, timedelta

import allure
from test_case.page_api.public.base_api import BaseAPI

SZORDER_PREFIX = "/djsupplier/DJEASYORDER/szorder"
OMS_PREFIX = "/djsupplier/oms"
DJEASYORDER_PREFIX = "/djsupplier/DJEASYORDER"


def _today():
    """当天日期，格式 YYYY-MM-DD"""
    return time.strftime("%Y-%m-%d")


def _month_start():
    """当月第一天，格式 YYYY-MM-DD"""
    return time.strftime("%Y-%m-01")


def _shift_minutes(minutes):
    """当前时间偏移 minutes 分钟，格式 YYYY-MM-DD HH:MM:SS"""
    return (datetime.now() + timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")


# 抓包回放用的默认策略产品列表（测试环境已存在的稳定产品）
DEFAULT_STRATEGY_PRODUCT_LIST = [
    {
        "ynetProductId": "cfbd1e8c-68e0-42f8-97d9-5c79146643c1",
        "productId": "214",
        "materialCode": "A737J",
        "layer": "5",
        "productName": "东经2号(A737T)",
        "fluteTypeName": "BC瓦",
    },
    {
        "ynetProductId": "8d345cf0-64f3-4b16-9462-8df29faa3dbe",
        "productId": "41219",
        "materialCode": "K8C8A",
        "layer": "5",
        "productName": "K8C8A/5BC",
        "fluteTypeName": "BC瓦",
    },
]


class ShuzhinadanAPI(BaseAPI):
    """易单来 数智拿单接口封装"""

    def __init__(self, base_url=None, headers=None, cookies=None):
        super().__init__(base_url, headers, cookies)
        # 易单来默认业务头（应用级公共头，非账号/cookie/token）
        biz_headers = {
            "device": "web",
            "source": "easy_order",
            "version": "2.3.5",
            "Content-Type": "application/json",
        }
        self.headers.update(biz_headers)

    @allure.step("作战看板-接单目标")
    def get_order_goal(self, date=None, supplierId=None, supplierName=None, dataOwnership="",
                       status_code=200, **kwargs):
        """接单目标（szorder/getOrderGoal.do）

        Args:
            date: 日期（如 "2026-04-15"；缺省取当天）
            supplierId: 供应商ID
            supplierName: 供应商名称
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getOrderGoal.do"
        payload = {
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取接单目标失败")

    @allure.step("作战看板-今日接单时段趋势")
    def get_today_order_hour_trend(self, date, supplierId, supplierName, dataOwnership="",
                                   status_code=200, **kwargs):
        """今日接单时段趋势（szorder/getTodayOrderHourTrend.do）

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getTodayOrderHourTrend.do"
        payload = {
            "date": date,
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取今日接单时段趋势失败")

    @allure.step("作战看板-产品策略")
    def get_product_strategy(self, date=None, supplierId=None, supplierName=None, dataOwnership="",
                             pageNo=1, pageSize=15, sort="", sortType="",
                             activityProductId="", focusFlag=None, productType=None,
                             listDimension=None, productIdList=None, productLabelIdList=None,
                             status_code=200, **kwargs):
        """产品策略（szorder/getProductStrategy.do）

        支持看板默认查询，也支持关注产品/用料维度/标签筛选等增强入参。

        Args:
            date: 日期（如 "2026-04-15"；缺省取当天）
            supplierId: 供应商ID
            supplierName: 供应商名称
            dataOwnership: 数据归属（默认空串）
            pageNo: 页码（默认1）
            pageSize: 每页条数（默认15）
            sort: 排序字段（默认空串）
            sortType: 排序方式（默认空串）
            activityProductId: 活动产品ID（默认空串）
            focusFlag: 仅关注产品标记（不传则不携带，保持看板默认行为）
            productType: 产品类型（如 conventional）
            listDimension: 清单维度（product/material）
            productIdList: 指定产品ID列表（关注产品筛选来源）
            productLabelIdList: v2.3.12 按配置标签ID筛选
        """
        url = f"{SZORDER_PREFIX}/getProductStrategy.do"
        payload = {
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
            "pageNo": pageNo,
            "pageSize": pageSize,
            "sort": sort,
            "sortType": sortType,
            "activityProductId": activityProductId,
        }
        # 增强入参仅在显式传入时携带，保证既有看板用例请求体不变。
        if focusFlag is not None:
            payload["focusFlag"] = focusFlag
        if productType is not None:
            payload["productType"] = productType
        if listDimension is not None:
            payload["listDimension"] = listDimension
        if productIdList is not None:
            payload["productIdList"] = productIdList
        # v2.3.12 按配置 ID 筛选；不传时保持旧版本请求不变。
        if productLabelIdList is not None:
            payload["productLabelIdList"] = productLabelIdList
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取产品策略失败")

    @allure.step("作战看板-客户销售列表")
    def get_customer_sales(self, date, supplierId, supplierName,
                           dimension="amount", sort="today_order_amount", sortType="desc",
                           dataOwnership="", pageNo=1, pageSize=100,
                           productId=None, status_code=200, **kwargs):
        """客户销售列表（szorder/product/getCustomerSales.do）

        2026-10-23 web 抓包确认：产品详情页客户销售清单已迁移至 /szorder/product/ 端点，
        旧 /szorder/getCustomerSales.do 返回 10201011 公司无权限。

        支持产品维度和用料代码维度两种调用方式。

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            dimension: 维度（amount-金额/area-面积，默认amount）
            sort: 排序字段（默认today_order_amount）
            sortType: 排序方式（默认desc）
            dataOwnership: 数据归属（默认空串）
            pageNo: 页码（默认1）
            pageSize: 每页条数（默认100）
            productId: 产品ID（产品维度时传入）
        """
        url = f"{SZORDER_PREFIX}/product/getCustomerSales.do"
        payload = {
            "date": date,
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dimension": dimension,
            "sort": sort,
            "sortType": sortType,
            "dataOwnership": dataOwnership,
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        if productId is not None:
            payload["productId"] = productId
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取客户销售列表失败")

    @allure.step("作战看板-客户基础信息")
    def get_customer_base_info(self, customerInfoId, status_code=200, **kwargs):
        """客户基础信息（customer/getCustomerBaseInfo.do）

        Args:
            customerInfoId: 客户信息ID
        """
        url = f"{SZORDER_PREFIX}/customer/getCustomerBaseInfo.do"
        payload = {
            "customerInfoId": customerInfoId,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取客户基础信息失败")

    @allure.step("作战看板-客户需求信息")
    def get_demand_info(self, customerInfoId, status_code=200, **kwargs):
        """客户需求信息（customer/getDemandInfo.do）

        Args:
            customerInfoId: 客户信息ID
        """
        url = f"{SZORDER_PREFIX}/customer/getDemandInfo.do"
        payload = {
            "customerInfoId": customerInfoId,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取客户需求信息失败")

    @allure.step("作战看板-签到拜访记录")
    def get_sign_in_and_visit_record_list(self, customerInfoId, dutyManId="",
                                          startDate="", endDate="",
                                          pageNo=1, pageSize=15, status_code=200, **kwargs):
        """签到拜访记录（customer/getSignInAndVisitRecordList.do）

        Args:
            customerInfoId: 客户信息ID
            dutyManId: 责任人ID（默认空串）
            startDate: 开始日期（默认空串）
            endDate: 结束日期（默认空串）
            pageNo: 页码（默认1）
            pageSize: 每页条数（默认15）
        """
        url = f"{SZORDER_PREFIX}/customer/getSignInAndVisitRecordList.do"
        payload = {
            "customerInfoId": customerInfoId,
            "dutyManId": dutyManId,
            "startDate": startDate,
            "endDate": endDate,
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取签到拜访记录失败")

    @allure.step("作战看板-返利报表")
    def get_rebate_list(self, supplierId, startYearMonth, endYearMonth,
                        id="", type=0, pageNo=1, pageSize=100,
                        sortField="", sortType="", status_code=200, **kwargs):
        """返利报表（customer/getRebateList.do）

        Args:
            supplierId: 供应商ID
            startYearMonth: 开始年月（如 "2026-01"）
            endYearMonth: 结束年月（如 "2026-12"）
            id: 客户ID（默认空串，查全部）
            type: 类型（0-客户返利，默认0）
            pageNo: 页码（默认1）
            pageSize: 每页条数（默认100）
            sortField: 排序字段（默认空串）
            sortType: 排序方式（默认空串）
        """
        url = f"{SZORDER_PREFIX}/customer/getRebateList.do"
        payload = {
            "pageNo": pageNo, "pageSize": pageSize,
            "id": id, "supplierId": supplierId,
            "startYearMonth": startYearMonth, "endYearMonth": endYearMonth,
            "sortField": sortField, "sortType": sortType, "type": type,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取返利报表失败")

    # ==================== 策略详情-活动内容 ====================

    @allure.step("获取策略活动列表")
    def get_market_activity_list(self, supplierId, strategyId, status_code=200, **kwargs):
        """获取策略关联的营销活动列表（saleStrategy/productActivity/list.do）

        Args:
            supplierId: 供应商ID
            strategyId: 策略ID
        """
        url = f"{SZORDER_PREFIX}/saleStrategy/productActivity/list.do"
        payload = {
            "supplierId": supplierId,
            "strategyId": strategyId,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取策略活动列表失败")

    @allure.step("新增营销活动")
    def add_market_activity(self, supplierId, strategyId, marketingActivityName, activityStartTime,
                            activityEndTime, activityType="according_area",
                            usersParticipateType="all_user_participate",
                            activityGoodsList=None, preferenceThreshold=None,
                            priceTime=None, id="", status_code=200, **kwargs):
        """新增营销活动（saleStrategy/productActivity/add.do）

        Args:
            supplierId: 供应商ID
            strategyId: 策略ID
            marketingActivityName: 活动名称
            activityStartTime: 活动开始时间（如 "2026-09-01 00:00:00"）
            activityEndTime: 活动结束时间（如 "2026-09-02 23:59:59"）
            activityType: 活动类型（according_area-按面积）
            usersParticipateType: 参与用户类型（all_user_participate-全部用户）
            activityGoodsList: 活动商品列表
            preferenceThreshold: 优惠门槛
            priceTime: 价格时间
            id: 活动ID（编辑时使用）
        """
        url = f"{SZORDER_PREFIX}/saleStrategy/productActivity/add.do"
        payload = {
            "supplierId": supplierId,
            "strategyId": strategyId,
            "marketingActivityName": marketingActivityName,
            "activityStartTime": activityStartTime,
            "activityEndTime": activityEndTime,
            "activityType": activityType,
            "usersParticipateType": usersParticipateType,
            "id": id,
        }
        if activityGoodsList is not None:
            payload["activityGoodsList"] = activityGoodsList
        if preferenceThreshold is not None:
            payload["preferenceThreshold"] = preferenceThreshold
        if priceTime is not None:
            payload["priceTime"] = priceTime
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="新增营销活动失败")

    @allure.step("删除营销活动")
    def delete_market_activity(self, activityId, strategyId, status_code=200, **kwargs):
        """删除营销活动（saleStrategy/productActivity/delete.do）

        Args:
            activityId: 活动ID
            strategyId: 策略ID
        """
        url = f"{SZORDER_PREFIX}/saleStrategy/productActivity/delete.do"
        payload = {
            "activityId": activityId,
            "strategyId": strategyId,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="删除营销活动失败")

    @allure.step("获取营销活动详情")
    def get_market_activity_details(self, marketActivityId, status_code=200, **kwargs):
        """获取营销活动详情（marketingActivity/eo/findMarketActivityDetails.do）

        Args:
            marketActivityId: 营销活动ID
        """
        url = f"/djsupplier/marketingActivity/eo/findMarketActivityDetails.do"
        payload = {
            "marketActivityId": marketActivityId,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取营销活动详情失败")

    @allure.step("过滤活动商品")
    def filter_activity_product(self, supplierId, activityStartTime, activityEndTime,
                                productIds, marketActivityId="", status_code=200, **kwargs):
        """过滤活动商品（marketingActivity/eo/filterActivityProduct.do）

        Args:
            supplierId: 供应商ID
            activityStartTime: 活动开始时间
            activityEndTime: 活动结束时间
            productIds: 商品ID列表
            marketActivityId: 营销活动ID
        """
        url = f"/djsupplier/marketingActivity/eo/filterActivityProduct.do"
        payload = {
            "supplierId": supplierId,
            "activityStartTime": activityStartTime,
            "activityEndTime": activityEndTime,
            "productIds": productIds,
            "marketActivityId": marketActivityId,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="过滤活动商品失败")

    @allure.step("获取销售策略列表")
    def get_sale_strategy_list(self, supplierId=None, pageNo=1, pageSize=20, dataOwnership="",
                               strategyType="", productIdList=None, createStartDate="",
                               createEndDate="", status_code=200, **kwargs):
        """获取销售策略列表（saleStrategy/getList.do）

        Args:
            supplierId: 供应商ID
            pageNo: 页码（默认1）
            pageSize: 每页条数（默认20）
            dataOwnership: 数据归属（默认空串）
            strategyType: 策略类型（默认空串，全部）
            productIdList: 产品ID列表（默认空列表）
            createStartDate: 创建开始日期（默认空串）
            createEndDate: 创建结束日期（默认空串）
        """
        url = f"{SZORDER_PREFIX}/saleStrategy/getList.do"
        payload = {
            "supplierId": supplierId,
            "pageNo": pageNo,
            "pageSize": pageSize,
            "dataOwnership": dataOwnership,
            "strategyType": strategyType,
            "productIdList": productIdList if productIdList is not None else [],
            "createStartDate": createStartDate,
            "createEndDate": createEndDate,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取销售策略列表失败")

    @allure.step("作战看板-利润目标")
    def get_profit_goal(self, date=None, supplierId=None, supplierName=None, dataOwnership="",
                        status_code=200, **kwargs):
        """利润目标（szorder/getProfitGoal.do）

        Args:
            date: 日期（如 "2026-04-15"；缺省取当天）
            supplierId: 供应商ID
            supplierName: 供应商名称
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getProfitGoal.do"
        payload = {
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取利润目标失败")

    @allure.step("作战看板-分时段接单利润趋势")
    def get_order_trend_by_time(self, date=None, supplierId=None, supplierName=None, dataOwnership="",
                                status_code=200, **kwargs):
        """分时段接单利润趋势（szorder/getOrderTrendByTime.do）

        Args:
            date: 日期（如 "2026-04-15"；缺省取当天）
            supplierId: 供应商ID
            supplierName: 供应商名称
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getOrderTrendByTime.do"
        payload = {
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取分时段接单利润趋势失败")

    @allure.step("作战看板-智能小结")
    def get_intelligence_summary(self, date=None, supplierId=None, supplierName=None, dataOwnership="",
                                 status_code=200, **kwargs):
        """智能小结（szorder/getIntelligenceSummary.do）

        Args:
            date: 日期（如 "2026-04-15"；缺省取当天）
            supplierId: 供应商ID
            supplierName: 供应商名称
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getIntelligenceSummary.do"
        payload = {
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取智能小结失败")

    @allure.step("订单管理-在线纸板订单列表")
    def oms_load_online_paper_board(self, partnerId, partnerName,
                                    orderStartTime, orderEndTime,
                                    pageNum=1, pageSize=100, status_code=200, **kwargs):
        """在线纸板订单列表（oms/loadOnlinePaperBoard.do）

        Args:
            partnerId: 合作伙伴ID
            partnerName: 合作伙伴名称
            orderStartTime: 订单开始时间（如 "2026-04-15 00:00:00"）
            orderEndTime: 订单结束时间（如 "2026-04-15 23:59:59"）
            pageNum: 页码（默认1）
            pageSize: 每页条数（默认100）
        """
        url = f"{OMS_PREFIX}/loadOnlinePaperBoard.do"
        payload = {
            "partnerId": partnerId,
            "partnerName": partnerName,
            "orderStartTime": orderStartTime,
            "orderEndTime": orderEndTime,
            "pageNum": pageNum,
            "pageSize": pageSize,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取在线纸板订单列表失败")

    @allure.step("作战看板-产品详情")
    def get_product_detail(self, date, supplierId, supplierName, productId=None,
                           dataOwnership="", status_code=200, **kwargs):
        """产品详情（szorder/product/getProductDetail.do）

        2026-10-23 web 抓包确认：产品详情已迁移至 /szorder/product/ 端点，
        旧 /szorder/getProductDetail.do 返回 10201011 公司无权限。

        支持产品维度和用料代码维度两种调用方式。

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            productId: 产品ID（产品维度时传入）
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/product/getProductDetail.do"
        payload = {
            "date": date,
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        if productId is not None:
            payload["productId"] = productId
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取产品详情失败")

    @allure.step("作战看板-接单情况")
    def get_order_situation(self, date, supplierId, supplierName, productId=None,
                            dataOwnership="", status_code=200, **kwargs):
        """接单情况（szorder/product/getOrderSituation.do）

        2026-10-23 web 抓包确认：接单情况已迁移至 /szorder/product/ 端点，
        旧 /szorder/getOrderSituation.do 返回 10201011 公司无权限。

        支持产品维度和用料代码维度两种调用方式。

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            productId: 产品ID（产品维度时传入）
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/product/getOrderSituation.do"
        payload = {
            "date": date,
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        if productId is not None:
            payload["productId"] = productId
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取接单情况失败")

    @allure.step("作战看板-成本分析")
    def get_cost_analysis(self, date, supplierId, supplierName, productId=None,
                          dataOwnership="", status_code=200, **kwargs):
        """成本分析（szorder/product/getCostAnalysis.do）

        2026-10-23 web 抓包确认：成本分析已迁移至 /szorder/product/ 端点，
        旧 /szorder/getCostAnalysis.do 返回 10201011 公司无权限。

        支持产品维度和用料代码维度两种调用方式。

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            productId: 产品ID（产品维度时传入）
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/product/getCostAnalysis.do"
        payload = {
            "date": date,
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        if productId is not None:
            payload["productId"] = productId
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取成本分析失败")

    @allure.step("作战看板-销售趋势")
    def get_sales_trend(self, date, supplierId, supplierName, productId=None,
                        dataOwnership="", status_code=200, **kwargs):
        """销售趋势（szorder/product/getSalesTrend.do）

        2026-10-23 web 抓包确认：销售趋势已迁移至 /szorder/product/ 端点，
        旧 /szorder/getSalesTrend.do 返回 10201011 公司无权限。

        支持产品维度和用料代码维度两种调用方式。

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            productId: 产品ID（产品维度时传入）
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/product/getSalesTrend.do"
        payload = {
            "date": date,
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        if productId is not None:
            payload["productId"] = productId
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取销售趋势失败")

    @allure.step("作战看板-客户数量")
    def get_customer_count(self, date=None, supplierId=None, supplierName=None, productId=None,
                           dataOwnership="", status_code=200, **kwargs):
        """客户数量（szorder/getCustomerCount.do）

        支持产品维度和用料代码维度两种调用方式。

        Args:
            date: 日期（如 "2026-04-15"；缺省取当天）
            supplierId: 供应商ID
            supplierName: 供应商名称
            productId: 产品ID（产品维度时传入）
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getCustomerCount.do"
        payload = {
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        if productId is not None:
            payload["productId"] = productId
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取客户数量失败")

    # ==================== 公共选项/基础数据 ====================

    @allure.step("查询联合供应商选项")
    def get_union_options(self, status_code=200, **kwargs):
        """查询联合供应商选项列表（无需登录态字段）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{DJEASYORDER_PREFIX}/common/getUnionOptionsNoAuth.do"
        payload = {}
        error_msg = kwargs.pop("error_msg", "查询联合供应商选项失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询自有筛选方案")
    def get_own_filter_scheme(self, status_code=200, **kwargs):
        """查询当前账号自有的筛选方案配置"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{DJEASYORDER_PREFIX}/filterscheme/config/getOwnNoAuth.do"
        payload = {}
        error_msg = kwargs.pop("error_msg", "查询自有筛选方案失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询在售产品层数选项")
    def get_on_product_layer_list(self, supplierId, status_code=200, **kwargs):
        """查询在售产品层数/楞型选项列表"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{DJEASYORDER_PREFIX}/common/getOnProductLayerListNoAuth.do"
        payload = {
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "查询在售产品层数选项失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询产品列表选项")
    def get_product_list(self, supplierId, status_code=200, **kwargs):
        """查询供应商全量产品列表（productId/materialCode/productName）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{DJEASYORDER_PREFIX}/common/getProductListNoAuth.do"
        payload = {
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "查询产品列表选项失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询业务员列表")
    def get_salesman_list(self, status_code=200, **kwargs):
        """查询供应商业务员列表"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{DJEASYORDER_PREFIX}/customer/getSalesmanListNoAuth.do"
        payload = {}
        error_msg = kwargs.pop("error_msg", "查询业务员列表失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询竞对档案列表")
    def get_rival_archive(self, status_code=200, **kwargs):
        """查询竞争对手档案列表"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{DJEASYORDER_PREFIX}/rival/archive/getRivalArchiveNoAuth.do"
        payload = {}
        error_msg = kwargs.pop("error_msg", "查询竞对档案列表失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询供应商销售区域")
    def get_supplier_sales_region(self, supplierId, supplierName, date=None,
                                  dataOwnership="", status_code=200, **kwargs):
        """查询供应商销售区域（regionCode/regionName）列表"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{DJEASYORDER_PREFIX}/common/getSupplierSalesRegionNoAuth.do"
        payload = {
            "dataOwnership": dataOwnership,
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
        }
        error_msg = kwargs.pop("error_msg", "查询供应商销售区域失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    # ==================== 作战看板 KPI/趋势/清单 ====================

    @allure.step("查询关注产品数量")
    def get_focus_product_count(self, supplierId, supplierName, date=None,
                                dataOwnership="", status_code=200, **kwargs):
        """查询关注产品数量与关注产品ID列表"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/getFocusProductCount.do"
        payload = {
            "dataOwnership": dataOwnership,
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
        }
        error_msg = kwargs.pop("error_msg", "查询关注产品数量失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("分页查询客户策略清单")
    def get_customer_strategy(self, supplierId, supplierName, date=None, dataOwnership="",
                              pageNo=1, pageSize=15, dimension="amount",
                              sort="goal_amount_dif", sortType="desc",
                              status_code=200, customerLabelIdList=None, **kwargs):
        """分页查询作战看板客户策略清单"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/getCustomerStrategy.do"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "dimension": dimension,
            "productId": [],
            "regionCode": [],
            "customerType": [],
            "monthGap": {"type": "0", "min": "", "max": ""},
            "noOrderDays": {"min": "", "max": ""},
            "opportunityOrderVolume": {"min": "", "max": ""},
            "salesmanId": [],
            "customerName": "",
            "customerPhone": "",
            "rivalArchiveId": [],
            "gapReasons": [],
            "baseOrderCustomerFlag": "n",
            "opportunityCustomerFlag": "n",
            "monthGapMin": "",
            "monthGapMax": "",
            "dayGapMin": "",
            "dayGapMax": "",
            "noOrderDaysMin": "",
            "noOrderDaysMax": "",
            "opportunityOrderVolumeMin": "",
            "opportunityOrderVolumeMax": "",
            "infoIdList": [],
            "customerPhoneList": [],
            "dataOwnership": dataOwnership,
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
            "customerLabelList": [],
            "sort": sort,
            "sortType": sortType,
        }
        # 显式传入新字段时不再携带旧标签值字段，空数组表示不按标签过滤。
        if customerLabelIdList is not None:
            # 新契约不发送旧界面占位对象和空字符串数值；显式筛选值仍由 kwargs 提供。
            for key in ("customerLabelList", "supplierName", "monthGap", "noOrderDays",
                        "opportunityOrderVolume", "monthGapMin", "monthGapMax", "dayGapMin",
                        "dayGapMax", "noOrderDaysMin", "noOrderDaysMax",
                        "opportunityOrderVolumeMin", "opportunityOrderVolumeMax",
                        "baseOrderCustomerFlag", "opportunityCustomerFlag"):
                payload.pop(key, None)
            payload["customerLabelIdList"] = customerLabelIdList
        error_msg = kwargs.pop("error_msg", "分页查询客户策略清单失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    # ==================== 产品详情页（/szorder/product/ 端点） ====================
    # 注：以下 *_page 方法是产品详情页专属接口，与看板级 get_product_detail 等同名端点不同，
    # 为避免与看板方法命名冲突，统一以 _page / get_product_detail_ 前缀区分。

    @allure.step("查询产品详情选项")
    def get_product_option(self, supplierId, supplierName, date=None, dataOwnership="",
                           status_code=200, **kwargs):
        """查询产品详情页的产品下拉选项（productId/productName）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/product/getProductOptionNoAuth.do"
        payload = {
            "dataOwnership": dataOwnership,
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
        }
        error_msg = kwargs.pop("error_msg", "查询产品详情选项失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询产品详情(详情页)")
    def get_product_detail_page(self, productId, supplierId, supplierName, date=None,
                                dataOwnership="", status_code=200, **kwargs):
        """查询产品详情页基础信息（品名/材质/层数/楞型/克重）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/product/getProductDetail.do"
        payload = {
            "dataOwnership": dataOwnership,
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
            "productId": productId,
        }
        error_msg = kwargs.pop("error_msg", "查询产品详情失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("分页查询产品客户销售清单(详情页)")
    def get_product_detail_customer_sales(self, productId, supplierId, supplierName,
                                          date=None, dataOwnership="", pageNo=1, pageSize=15,
                                          dimension="amount", sort="today_order_amount",
                                          sortType="desc", status_code=200,
                                          customerLabelIdList=None, **kwargs):
        """分页查询产品详情页客户销售清单"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/product/getCustomerSales.do"
        payload = {
            "productId": productId,
            "pageNo": pageNo,
            "pageSize": pageSize,
            "dimension": dimension,
            "regionCode": [],
            "customerType": [],
            "noOrderDays": {"min": "", "max": ""},
            "opportunityOrderVolume": {"min": "", "max": ""},
            "salesmanId": [],
            "customerName": "",
            "customerPhone": "",
            "rivalArchiveId": [],
            "gapReasons": [],
            "baseOrderCustomerFlag": "n",
            "opportunityCustomerFlag": "n",
            "monthGapMin": "",
            "monthGapMax": "",
            "dayGapMin": "",
            "dayGapMax": "",
            "noOrderDaysMin": "",
            "noOrderDaysMax": "",
            "opportunityOrderVolumeMin": "",
            "opportunityOrderVolumeMax": "",
            "infoIdList": [],
            "customerPhoneList": [],
            "dataOwnership": dataOwnership,
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
            "customerLabelList": [],
            "sort": sort,
            "sortType": sortType,
        }
        # 待联调：导出文档仍是 customerLabelList，本次按技术方案预封装 ID 字段。
        if customerLabelIdList is not None:
            # 新契约不发送旧界面占位对象和空字符串数值；显式筛选值仍由 kwargs 提供。
            for key in ("customerLabelList", "supplierName", "monthGap", "noOrderDays",
                        "opportunityOrderVolume", "monthGapMin", "monthGapMax", "dayGapMin",
                        "dayGapMax", "noOrderDaysMin", "noOrderDaysMax",
                        "opportunityOrderVolumeMin", "opportunityOrderVolumeMax",
                        "baseOrderCustomerFlag", "opportunityCustomerFlag"):
                payload.pop(key, None)
            payload["customerLabelIdList"] = customerLabelIdList
            payload.pop("infoIdList")
            # 新契约使用文档中的排序字段，未传新标签参数时保留历史默认值。
            if sort == "today_order_amount":
                payload["sort"] = "order_amount"
        error_msg = kwargs.pop("error_msg", "分页查询产品客户销售清单失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询产品销售趋势(详情页)")
    def get_product_detail_sales_trend(self, productId, supplierId, supplierName, date=None,
                                       dataOwnership="", status_code=200, **kwargs):
        """查询产品详情页销售趋势"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/product/getSalesTrend.do"
        payload = {
            "dataOwnership": dataOwnership,
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
            "productId": productId,
        }
        error_msg = kwargs.pop("error_msg", "查询产品销售趋势失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询产品成本分析(详情页)")
    def get_product_detail_cost_analysis(self, productId, supplierId, supplierName, date=None,
                                         dataOwnership="", status_code=200, **kwargs):
        """查询产品详情页成本分析（单位边际贡献/折后单价/单位利润）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/product/getCostAnalysis.do"
        payload = {
            "dataOwnership": dataOwnership,
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
            "productId": productId,
        }
        error_msg = kwargs.pop("error_msg", "查询产品成本分析失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询产品接单情况(详情页)")
    def get_product_detail_order_situation(self, productId, supplierId, supplierName, date=None,
                                           dataOwnership="", status_code=200, **kwargs):
        """查询产品详情页接单情况（目标面积/差距/接单面积）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/product/getOrderSituation.do"
        payload = {
            "dataOwnership": dataOwnership,
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
            "productId": productId,
        }
        error_msg = kwargs.pop("error_msg", "查询产品接单情况失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    # ==================== 产品策略配置 CRUD ====================

    @allure.step("新增销售策略")
    def add_sale_strategy(self, supplierId, strategyName=None, productList=None,
                          strategyType="product", descr="", status_code=200, **kwargs):
        """新增产品/客户销售策略"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/add.do"
        payload = {
            "supplierId": supplierId,
            "strategyName": strategyName or "ai" + time.strftime("%Y%m%d%H%M%S"),
            "productList": productList if productList is not None else DEFAULT_STRATEGY_PRODUCT_LIST,
            "strategyType": strategyType,
            "descr": descr,
        }
        error_msg = kwargs.pop("error_msg", "新增销售策略失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询销售策略详情")
    def get_sale_strategy(self, id, status_code=200, **kwargs):
        """按策略ID查询销售策略详情"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/get.do"
        payload = {
            "id": id,
        }
        error_msg = kwargs.pop("error_msg", "查询销售策略详情失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("编辑销售策略")
    def edit_sale_strategy(self, id, supplierId, strategyName=None, productList=None,
                           strategyType="product", descr="", status_code=200, **kwargs):
        """编辑已有销售策略"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/edit.do"
        payload = {
            "supplierId": supplierId,
            "id": id,
            "strategyName": strategyName or "ai" + time.strftime("%Y%m%d%H%M%S"),
            "productList": productList if productList is not None else DEFAULT_STRATEGY_PRODUCT_LIST,
            "strategyType": strategyType,
            "descr": descr,
        }
        error_msg = kwargs.pop("error_msg", "编辑销售策略失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("删除销售策略")
    def delete_sale_strategy(self, id, status_code=200, **kwargs):
        """按策略ID删除销售策略"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/delete.do"
        payload = {
            "id": id,
        }
        error_msg = kwargs.pop("error_msg", "删除销售策略失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("导出销售策略列表")
    def export_sale_strategy(self, supplierId, dataOwnership="", ids=None,
                             strategyType="", productIdList=None, createStartDate="",
                             createEndDate="", status_code=200, **kwargs):
        """导出销售策略列表（返回 Excel 文件，使用 return_response 避免 JSON 解析）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/export.do"
        payload = {
            "supplierId": supplierId,
            "dataOwnership": dataOwnership,
            "ids": ids if ids is not None else [],
            "strategyType": strategyType,
            "productIdList": productIdList if productIdList is not None else [],
            "createStartDate": createStartDate,
            "createEndDate": createEndDate,
        }
        error_msg = kwargs.pop("error_msg", "导出销售策略列表失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg, return_response=True)
        return res

    @allure.step("查询策略产品选项")
    def get_strategy_product_option(self, supplierId, supplierName, date=None,
                                    dataOwnership="", status_code=200, **kwargs):
        """查询策略配置页的产品下拉选项"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/getProductOptionNoAuth.do"
        payload = {
            "dataOwnership": dataOwnership,
            "date": date or _today(),
            "supplierId": supplierId,
            "supplierName": supplierName,
        }
        error_msg = kwargs.pop("error_msg", "查询策略产品选项失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询策略下活动产品选项")
    def get_active_product(self, strategyId, status_code=200, **kwargs):
        """查询策略下可关联活动的产品选项（productId/productName）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/getActiveProductNoAuth.do"
        payload = {
            "strategyId": strategyId,
        }
        error_msg = kwargs.pop("error_msg", "查询策略下活动产品选项失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("分页查询产品策略接单情况")
    def get_product_strategy_order_situation(self, strategyId, startDate=None, endDate=None,
                                             activityProductId="", dataOwnership="",
                                             pageNo=1, pageSize=15, sort="", sortType="",
                                             status_code=200, **kwargs):
        """分页查询策略维度的产品接单情况"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/getProductStrategyOrderSituation.do"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "activityProductId": activityProductId,
            "dataOwnership": dataOwnership,
            "strategyId": strategyId,
            "startDate": startDate or _month_start(),
            "endDate": endDate or _today(),
            "sort": sort,
            "sortType": sortType,
        }
        error_msg = kwargs.pop("error_msg", "分页查询产品策略接单情况失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    # ==================== 策略下营销活动 ====================
    # 注：add/get/delete_strategy_activity 与看板已有的 add_market_activity/
    # get_market_activity_list/delete_market_activity 指向同一批 URL，因命名不同均保留，
    # 以免破坏现有（含 skip）用例的引用；详见交付说明的重复清单。

    @allure.step("新增策略营销活动")
    def add_strategy_activity(self, strategyId, activityGoodsList, marketingActivityName=None,
                              activityStartTime=None, activityEndTime=None, supplierId=None,
                              id="", activityType="according_area",
                              usersParticipateType="all_user_participate", isTop="n",
                              preferentialTypeList=None, status_code=200, **kwargs):
        """在销售策略下新增营销活动"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/productActivity/add.do"
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
        error_msg = kwargs.pop("error_msg", "新增策略营销活动失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询策略营销活动列表")
    def get_strategy_activity_list(self, strategyId, supplierId=None, status_code=200, **kwargs):
        """查询策略下的营销活动列表"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/productActivity/list.do"
        payload = {
            "supplierId": supplierId,
            "strategyId": strategyId,
        }
        error_msg = kwargs.pop("error_msg", "查询策略营销活动列表失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("删除策略营销活动")
    def delete_strategy_activity(self, activityId, strategyId, status_code=200, **kwargs):
        """删除策略下的营销活动"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/productActivity/delete.do"
        payload = {
            "activityId": activityId,
            "strategyId": strategyId,
        }
        error_msg = kwargs.pop("error_msg", "删除策略营销活动失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    # ==================== 策略效果分析 ====================

    @allure.step("查询策略效果总览")
    def get_strategy_effect_overview(self, supplierId, startDate=None, endDate=None, dateType="create_time",
                                     dataOwnership="", status_code=200, **kwargs):
        """查询策略效果总览（策略总数/日均面积/策略接单量）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/getStrategyEffectOverview.do"
        payload = {
            "dataOwnership": dataOwnership,
            "supplierId": supplierId,
            "dateType": dateType,
            "startDate": startDate or _month_start(),
            "endDate": endDate or _today(),
        }
        error_msg = kwargs.pop("error_msg", "查询策略效果总览失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询产品策略效果总览")
    def get_product_strategy_effect_overview(self, supplierId, startDate=None, endDate=None, dateType="create_time",
                                             dataOwnership="", status_code=200, **kwargs):
        """查询产品策略效果总览（活动产品数/参与客户数/优惠金额等）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/getProductStrategyEffectOverview.do"
        payload = {
            "dataOwnership": dataOwnership,
            "supplierId": supplierId,
            "dateType": dateType,
            "startDate": startDate or _month_start(),
            "endDate": endDate or _today(),
        }
        error_msg = kwargs.pop("error_msg", "查询产品策略效果总览失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询客户策略效果总览")
    def get_customer_strategy_effect_overview(self, supplierId, startDate=None, endDate=None, dateType="create_time",
                                              dataOwnership="", status_code=200, **kwargs):
        """查询客户策略效果总览（发券数/用券率/覆盖客户数等）"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/getCustomerStrategyEffectOverview.do"
        payload = {
            "dataOwnership": dataOwnership,
            "supplierId": supplierId,
            "dateType": dateType,
            "startDate": startDate or _month_start(),
            "endDate": endDate or _today(),
        }
        error_msg = kwargs.pop("error_msg", "查询客户策略效果总览失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询客户策略分段占比")
    def get_customer_strategy_segments_ratio(self, supplierId, startDate=None, endDate=None, dateType="create_time",
                                             dataOwnership="", status_code=200, **kwargs):
        """查询客户策略基本盘/机会单/其他单分段占比"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/getCustomerStrategySegmentsRatio.do"
        payload = {
            "dataOwnership": dataOwnership,
            "supplierId": supplierId,
            "dateType": dateType,
            "startDate": startDate or _month_start(),
            "endDate": endDate or _today(),
        }
        error_msg = kwargs.pop("error_msg", "查询客户策略分段占比失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询客户策略转化漏斗")
    def get_customer_strategy_conversion_funnel(self, supplierId, startDate=None, endDate=None, dateType="create_time",
                                                dataOwnership="", status_code=200, **kwargs):
        """查询客户策略覆盖-机会-下单转化漏斗"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/getCustomerStrategyConversionFunnel.do"
        payload = {
            "dataOwnership": dataOwnership,
            "supplierId": supplierId,
            "dateType": dateType,
            "startDate": startDate or _month_start(),
            "endDate": endDate or _today(),
        }
        error_msg = kwargs.pop("error_msg", "查询客户策略转化漏斗失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res

    @allure.step("查询产品接单表现")
    def get_product_order_performance(self, supplierId, startDate=None, endDate=None, dateType="create_time",
                                      dataOwnership="", status_code=200, **kwargs):
        """查询策略效果分析中的产品接单表现列表"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True
        url = f"{SZORDER_PREFIX}/saleStrategy/getProductOrderPerformance.do"
        payload = {
            "dataOwnership": dataOwnership,
            "supplierId": supplierId,
            "dateType": dateType,
            "startDate": startDate or _month_start(),
            "endDate": endDate or _today(),
        }
        error_msg = kwargs.pop("error_msg", "查询产品接单表现失败")
        payload.update(kwargs)
        res = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        return res
