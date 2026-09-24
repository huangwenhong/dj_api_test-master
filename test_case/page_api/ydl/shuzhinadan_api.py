# -*- coding: utf-8 -*-
"""易单来 - 数智拿单接口"""

import allure
from test_case.page_api.public.base_api import BaseAPI

SZORDER_PREFIX = "/djsupplier/DJEASYORDER/szorder"
OMS_PREFIX = "/djsupplier/oms"


class ShuzhinadanAPI(BaseAPI):
    """易单来 数智拿单接口封装"""

    def __init__(self, base_url=None, headers=None, cookies=None):
        super().__init__(base_url, headers, cookies)

    @allure.step("作战看板-接单目标")
    def get_order_goal(self, date, supplierId, supplierName, dataOwnership="",
                       status_code=200, **kwargs):
        """接单目标（szorder/getOrderGoal.do）

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getOrderGoal.do"
        payload = {
            "date": date,
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
    def get_product_strategy(self, date, supplierId, supplierName, dataOwnership="",
                             pageNo=1, pageSize=15, sort="", sortType="",
                             activityProductId="", status_code=200, **kwargs):
        """产品策略（szorder/getProductStrategy.do）

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            dataOwnership: 数据归属（默认空串）
            pageNo: 页码（默认1）
            pageSize: 每页条数（默认15）
            sort: 排序字段（默认空串）
            sortType: 排序方式（默认空串）
            activityProductId: 活动产品ID（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getProductStrategy.do"
        payload = {
            "date": date,
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
            "pageNo": pageNo,
            "pageSize": pageSize,
            "sort": sort,
            "sortType": sortType,
            "activityProductId": activityProductId,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取产品策略失败")

    @allure.step("作战看板-客户销售列表")
    def get_customer_sales(self, date, supplierId, supplierName,
                           dimension="amount", sort="today_order_amount", sortType="desc",
                           dataOwnership="", pageNo=1, pageSize=100,
                           productId=None, status_code=200, **kwargs):
        """客户销售列表（szorder/getCustomerSales.do）

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
        url = f"{SZORDER_PREFIX}/getCustomerSales.do"
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
    def get_sale_strategy_list(self, supplierId, pageNo=1, pageSize=20, status_code=200, **kwargs):
        """获取销售策略列表（saleStrategy/getList.do）

        Args:
            supplierId: 供应商ID
            pageNo: 页码（默认1）
            pageSize: 每页条数（默认20）
        """
        url = f"{SZORDER_PREFIX}/saleStrategy/getList.do"
        payload = {
            "supplierId": supplierId,
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取销售策略列表失败")

    @allure.step("作战看板-利润目标")
    def get_profit_goal(self, date, supplierId, supplierName, dataOwnership="",
                        status_code=200, **kwargs):
        """利润目标（szorder/getProfitGoal.do）

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getProfitGoal.do"
        payload = {
            "date": date,
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取利润目标失败")

    @allure.step("作战看板-分时段接单利润趋势")
    def get_order_trend_by_time(self, date, supplierId, supplierName, dataOwnership="",
                                status_code=200, **kwargs):
        """分时段接单利润趋势（szorder/getOrderTrendByTime.do）

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getOrderTrendByTime.do"
        payload = {
            "date": date,
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取分时段接单利润趋势失败")

    @allure.step("作战看板-智能小结")
    def get_intelligence_summary(self, date, supplierId, supplierName, dataOwnership="",
                                 status_code=200, **kwargs):
        """智能小结（szorder/getIntelligenceSummary.do）

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getIntelligenceSummary.do"
        payload = {
            "date": date,
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
        """产品详情（szorder/getProductDetail.do）

        支持产品维度和用料代码维度两种调用方式。

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            productId: 产品ID（产品维度时传入）
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getProductDetail.do"
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
        """接单情况（szorder/getOrderSituation.do）

        支持产品维度和用料代码维度两种调用方式。

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            productId: 产品ID（产品维度时传入）
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getOrderSituation.do"
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
        """成本分析（szorder/getCostAnalysis.do）

        支持产品维度和用料代码维度两种调用方式。

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            productId: 产品ID（产品维度时传入）
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getCostAnalysis.do"
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
        """销售趋势（szorder/getSalesTrend.do）

        支持产品维度和用料代码维度两种调用方式。

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            productId: 产品ID（产品维度时传入）
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getSalesTrend.do"
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
    def get_customer_count(self, date, supplierId, supplierName, productId=None,
                           dataOwnership="", status_code=200, **kwargs):
        """客户数量（szorder/getCustomerCount.do）

        支持产品维度和用料代码维度两种调用方式。

        Args:
            date: 日期（如 "2026-04-15"）
            supplierId: 供应商ID
            supplierName: 供应商名称
            productId: 产品ID（产品维度时传入）
            dataOwnership: 数据归属（默认空串）
        """
        url = f"{SZORDER_PREFIX}/getCustomerCount.do"
        payload = {
            "date": date,
            "supplierId": supplierId,
            "supplierName": supplierName,
            "dataOwnership": dataOwnership,
        }
        if productId is not None:
            payload["productId"] = productId
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取客户数量失败")
