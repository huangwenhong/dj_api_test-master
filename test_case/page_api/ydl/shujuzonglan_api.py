# -*- coding: utf-8 -*-
"""易单来 - 数据总览接口（基于 web 抓包：总经理驾驶舱/产能记录/目标追踪/交付率看板/经营分析）"""

import allure
from test_case.page_api.public.base_api import BaseAPI

# 总经理驾驶舱看板
BOARD_PREFIX = "/djsupplier/djcockpit/easyorder/generalmanager/board"
# 产能记录
CAPACITY_PREFIX = "/djsupplier/DJEASYORDER/capacityrecord"
# 目标追踪
TRACE_PREFIX = "/djsupplier/DJEASYORDER/goal/new/trace"
# 通用选项
COMMON_PREFIX = "/djsupplier/DJEASYORDER/common"
# 竞对产品层级
RIVAL_PRODUCT_PREFIX = "/djsupplier/DJEASYORDER/rival/product"
# 订单互联审核
ORDER_MANAGER_PREFIX = "/djsupplier/orderManager"
# 财务-联合体供应商
UNION_SUPPLIER_PREFIX = "/djsupplier/djfinancemanage/union-supplier"
# 财务-毛利分析
GROSS_PROFIT_PREFIX = "/djsupplier/djfinancemanage/grossProfit-supplier"
# 交付率看板
KANBAN_PREFIX = "/djsupplier/DJEASYORDER/delivery/rate/kanban"
# 经营分析-全景
PANDECT_PREFIX = "/djsupplier/analysis/pandect"
# 经营分析-售后
AFTERMARKET_PREFIX = "/djsupplier/analysis/aftermarket"
# 市场目标
MARKET_PREFIX = "/djsupplier/DJEASYORDER/goal/market"

# 财务类接口使用的业务请求头（抓包 source=easy_mes）
EASY_MES_HEADERS = {
    "device": "web",
    "source": "easy_mes",
    "version": "1.10.1",
    "Content-Type": "application/json",
}


class ShujuzonglanAPI(BaseAPI):
    """易单来数据总览接口封装"""

    def __init__(self, base_url=None, headers=None, cookies=None):
        super().__init__(base_url, headers, cookies)
        biz_headers = {
            "device": "web",
            "source": "easy_order",
            "version": "2.3.7",
            "Content-Type": "application/json",
        }
        if self.headers:
            self.headers.update(biz_headers)
        else:
            self.headers = biz_headers

    # ==================== 总经理驾驶舱看板 ====================

    @allure.step("驾驶舱-目标差异总览")
    def board_get_goal_dif_overview(self, supplierId, dateType="3", dimension="area",
                                    status_code=200, **kwargs):
        """驾驶舱-目标差异总览（近12个月目标/达成/环比）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{BOARD_PREFIX}/getGoalDifOverview.do"
        payload = {
            "dateType": dateType,
            "dimension": dimension,
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "驾驶舱目标差异总览查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("驾驶舱-投诉分析总览")
    def board_get_complaint_analysis_overview(self, supplierId, status_code=200, **kwargs):
        """驾驶舱-投诉分析总览（投诉数量/投诉率/不良原因列表）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{BOARD_PREFIX}/getComplaintAnalysisOverview.do"
        payload = {
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "驾驶舱投诉分析总览查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("驾驶舱-利润分析总览")
    def board_get_profit_analysis_overview(self, supplierId, status_code=200, **kwargs):
        """驾驶舱-利润分析总览（供销价差/均价/利润）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{BOARD_PREFIX}/getProfitAnalysisOverview.do"
        payload = {
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "驾驶舱利润分析总览查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("驾驶舱-市场分析总览")
    def board_get_market_analysis_overview(self, supplierId, status_code=200, **kwargs):
        """驾驶舱-市场分析总览（月活/人均接单）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{BOARD_PREFIX}/getMarketAnalysisOverview.do"
        payload = {
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "驾驶舱市场分析总览查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("驾驶舱-订单总览")
    def board_get_order_overview(self, supplierId, dateType="3", status_code=200, **kwargs):
        """驾驶舱-订单总览（理论/实际日均、日均面积与总面积目标达成）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{BOARD_PREFIX}/getOrderOverview.do"
        payload = {
            "dateType": dateType,
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "驾驶舱订单总览查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("驾驶舱-交付分析总览")
    def board_get_delivery_analysis_overview(self, supplierId, status_code=200, **kwargs):
        """驾驶舱-交付分析总览（24h/48h交付率与分区域交付率）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{BOARD_PREFIX}/getDeliveryAnalysisOverview.do"
        payload = {
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "驾驶舱交付分析总览查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 产能记录 ====================

    @allure.step("产能记录-列表查询")
    def capacity_record_get_list(self, supplierId, startTime, endTime,
                                 pageNo=1, pageSize=15, status_code=200, **kwargs):
        """产能记录-分页列表查询"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{CAPACITY_PREFIX}/getList.do"
        payload = {
            "supplierId": supplierId,
            "pageNo": pageNo,
            "pageSize": pageSize,
            "startTime": startTime,
            "endTime": endTime,
        }
        error_msg = kwargs.pop("error_msg", "产能记录列表查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产能记录-趋势查询")
    def capacity_record_get_trend(self, supplierId, startTime, endTime,
                                  status_code=200, **kwargs):
        """产能记录-按日趋势查询（产能与销售面积）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{CAPACITY_PREFIX}/getTrend.do"
        payload = {
            "supplierId": supplierId,
            "startTime": startTime,
            "endTime": endTime,
        }
        error_msg = kwargs.pop("error_msg", "产能记录趋势查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产能记录-新增")
    def capacity_record_add(self, supplierId, recordDate, supplyCapacity,
                            capacityTarget, remarks="", status_code=200, **kwargs):
        """产能记录-新增/更新某日产能记录"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{CAPACITY_PREFIX}/add.do"
        payload = {
            "supplierId": supplierId,
            "recordDate": recordDate,
            "supplyCapacity": supplyCapacity,
            "capacityTarget": capacityTarget,
            "remarks": remarks,
        }
        error_msg = kwargs.pop("error_msg", "产能记录新增失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 目标追踪（数据总览新接口） ====================

    @allure.step("目标追踪-获取组织列表")
    def trace_get_org_list_no_auth(self, status_code=200, **kwargs):
        """目标追踪-获取组织列表（无鉴权）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{TRACE_PREFIX}/getOrgListNoAuth.do"
        error_msg = kwargs.pop("error_msg", "目标追踪组织列表查询失败")
        return self.post(url, json={}, status_code=status_code, error_msg=error_msg)

    @allure.step("目标追踪-滚动目标")
    def trace_get_rolling_goal(self, date, orgId, supplierId,
                               filterSchemeConfigId="", status_code=200, **kwargs):
        """目标追踪-当日滚动目标"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{TRACE_PREFIX}/getRollingGoal.do"
        payload = {
            "date": date,
            "orgId": orgId,
            "supplierId": supplierId,
            "filterSchemeConfigId": filterSchemeConfigId,
        }
        error_msg = kwargs.pop("error_msg", "目标追踪滚动目标查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("目标追踪-分时段预警列表")
    def trace_get_time_segmented_warn_list(self, date, orgId, supplierId,
                                           filterSchemeConfigId="", status_code=200, **kwargs):
        """目标追踪-分时段接单预警列表"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{TRACE_PREFIX}/getTimeSegmentedWarnList.do"
        payload = {
            "date": date,
            "orgId": orgId,
            "supplierId": supplierId,
            "filterSchemeConfigId": filterSchemeConfigId,
        }
        error_msg = kwargs.pop("error_msg", "目标追踪分时段预警查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("目标追踪-重点关注Top")
    def trace_get_focus_top(self, date, orgId, supplierId,
                            filterSchemeConfigId="", status_code=200, **kwargs):
        """目标追踪-重点关注Top（区域/产品/业务员/客户）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{TRACE_PREFIX}/getFocusTop.do"
        payload = {
            "date": date,
            "orgId": orgId,
            "supplierId": supplierId,
            "filterSchemeConfigId": filterSchemeConfigId,
        }
        error_msg = kwargs.pop("error_msg", "目标追踪重点关注Top查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("目标追踪-客户目标达成")
    def trace_get_customer_goal(self, orgId, month, startTime, endTime, supplierId,
                                filterSchemeConfigId="", status_code=200, **kwargs):
        """目标追踪-客户目标达成统计"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{TRACE_PREFIX}/getCustomerGoal.do"
        payload = {
            "orgId": orgId,
            "month": month,
            "startTime": startTime,
            "endTime": endTime,
            "supplierId": supplierId,
            "filterSchemeConfigId": filterSchemeConfigId,
        }
        error_msg = kwargs.pop("error_msg", "目标追踪客户目标达成查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("目标追踪-客户流失")
    def trace_get_customer_lost(self, orgId, month, startTime, endTime, supplierId,
                                filterSchemeConfigId="", status_code=200, **kwargs):
        """目标追踪-客户流失列表"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{TRACE_PREFIX}/getCustomerLost.do"
        payload = {
            "orgId": orgId,
            "month": month,
            "startTime": startTime,
            "endTime": endTime,
            "supplierId": supplierId,
            "filterSchemeConfigId": filterSchemeConfigId,
        }
        error_msg = kwargs.pop("error_msg", "目标追踪客户流失查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("目标追踪-订单日趋势")
    def trace_get_order_trend_day(self, orgId, month, startTime, endTime, supplierId,
                                  filterSchemeConfigId="", status_code=200, **kwargs):
        """目标追踪-订单按日趋势"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{TRACE_PREFIX}/getOrderTrendDay.do"
        payload = {
            "orgId": orgId,
            "month": month,
            "startTime": startTime,
            "endTime": endTime,
            "supplierId": supplierId,
            "filterSchemeConfigId": filterSchemeConfigId,
        }
        error_msg = kwargs.pop("error_msg", "目标追踪订单日趋势查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 通用/基础字典 ====================

    @allure.step("通用-联合体供应商选项")
    def common_get_union_options_no_auth(self, containsUnion=False, status_code=200, **kwargs):
        """通用-获取供应商选项列表（无鉴权）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{COMMON_PREFIX}/getUnionOptionsNoAuth.do"
        payload = {
            "containsUnion": containsUnion,
        }
        error_msg = kwargs.pop("error_msg", "供应商选项列表查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("竞对产品-层级列表")
    def rival_product_get_layer_list_no_auth(self, status_code=200, **kwargs):
        """竞对产品-纸板层级/楞型字典（无鉴权）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{RIVAL_PRODUCT_PREFIX}/getLayerListNoAuth.do"
        error_msg = kwargs.pop("error_msg", "纸板层级字典查询失败")
        return self.post(url, json={}, status_code=status_code, error_msg=error_msg)

    @allure.step("订单互联-按ID查询审核权限")
    def order_manager_get_connect_audit_by_id(self, connectId, status_code=200, **kwargs):
        """订单互联-按互联ID批量查询审核展示权限（source=easy_mes）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{ORDER_MANAGER_PREFIX}/getConnectAuditById.do"
        payload = {
            "connectId": connectId,
        }
        error_msg = kwargs.pop("error_msg", "订单互联审核权限查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, headers=EASY_MES_HEADERS,
                         status_code=status_code, error_msg=error_msg)

    @allure.step("财务-联合体供应商列表")
    def finance_get_union_supplier_list_no_auth(self, status_code=200, **kwargs):
        """财务-获取联合体供应商列表（GET，无鉴权，source=easy_mes）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{UNION_SUPPLIER_PREFIX}/getUnionSupplierListNoAuth.do"
        error_msg = kwargs.pop("error_msg", "联合体供应商列表查询失败")
        return self.get(url, headers=EASY_MES_HEADERS,
                        status_code=status_code, error_msg=error_msg)

    @allure.step("财务-毛利分析分页")
    def finance_get_gross_profit_analysis_page(self, supplierId, pageNo=1, pageSize=15,
                                               status_code=200, **kwargs):
        """财务-供应商毛利分析分页查询（source=easy_mes）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{GROSS_PROFIT_PREFIX}/getAnalysisPage.do"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "毛利分析分页查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, headers=EASY_MES_HEADERS,
                         status_code=status_code, error_msg=error_msg)

    @allure.step("财务-毛利分析经营详情")
    def finance_get_operate_detail(self, supplierId, startTime, endTime,
                                   status_code=200, **kwargs):
        """财务-毛利分析经营详情（source=easy_mes）

        返参 data: netProfit.goalValue本月净利额目标 / onlineCardboardRevenue.assessmentDays考核天数
        """
        # Author: Author
        # Create Date: 2026-08-25
        # IsAI: True
        url = f"{GROSS_PROFIT_PREFIX}/getOperateDetail.do"
        payload = {
            "supplierId": supplierId,
            "startTime": startTime,
            "endTime": endTime,
        }
        error_msg = kwargs.pop("error_msg", "毛利分析经营详情查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, headers=EASY_MES_HEADERS,
                         status_code=status_code, error_msg=error_msg)

    # ==================== 交付率看板 ====================

    @allure.step("交付看板-供应商选项")
    def kanban_get_supplier_options(self, status_code=200, **kwargs):
        """交付看板-获取供应商选项（含联合体标识）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{KANBAN_PREFIX}/getSupplierOptions.do"
        error_msg = kwargs.pop("error_msg", "交付看板供应商选项查询失败")
        return self.post(url, json={}, status_code=status_code, error_msg=error_msg)

    @allure.step("交付看板-交付率趋势线")
    def kanban_get_delivery_overview_line(self, supplierId, beginDate, endDate,
                                          type="3", status_code=200, **kwargs):
        """交付看板-交付率按日趋势线（24/48/72/96小时）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{KANBAN_PREFIX}/getDeliveryOverviewLine.do"
        payload = {
            "type": type,
            "beginDate": beginDate,
            "endDate": endDate,
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "交付率趋势线查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("交付看板-出货率趋势线")
    def kanban_get_out_overview_line(self, supplierId, beginDate, endDate,
                                     type="3", status_code=200, **kwargs):
        """交付看板-出货率按日趋势线（24/48/72/96小时）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{KANBAN_PREFIX}/getOutOverviewLine.do"
        payload = {
            "type": type,
            "beginDate": beginDate,
            "endDate": endDate,
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "出货率趋势线查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("交付看板-交付总览")
    def kanban_get_delivery_overview(self, supplierId, beginDate, endDate,
                                     type="3", status_code=200, **kwargs):
        """交付看板-交付率总览（各时效交付率与达标标识）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{KANBAN_PREFIX}/getDeliveryOverview.do"
        payload = {
            "type": type,
            "beginDate": beginDate,
            "endDate": endDate,
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "交付率总览查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("交付看板-出货总览")
    def kanban_get_out_overview(self, supplierId, beginDate, endDate,
                                type="3", status_code=200, **kwargs):
        """交付看板-出货率总览（各时效出货率与达标标识）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{KANBAN_PREFIX}/getOutOverview.do"
        payload = {
            "type": type,
            "beginDate": beginDate,
            "endDate": endDate,
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "出货率总览查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("交付看板-区域简表")
    def kanban_get_simple_area_list(self, supplierId, beginDate, endDate,
                                    dataType="1", timeType="1", type="3",
                                    sortField="", sortType="",
                                    pageNum=1, pageSize=15, status_code=200, **kwargs):
        """交付看板-按区域维度交付率简表"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{KANBAN_PREFIX}/getSimpleAreaList.do"
        payload = {
            "dataType": dataType,
            "timeType": timeType,
            "type": type,
            "beginDate": beginDate,
            "endDate": endDate,
            "supplierId": supplierId,
            "sortField": sortField,
            "sortType": sortType,
            "pageNum": pageNum,
            "pageSize": pageSize,
        }
        error_msg = kwargs.pop("error_msg", "区域交付率简表查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("交付看板-产品简表")
    def kanban_get_simple_product_list(self, supplierId, beginDate, endDate,
                                       dataType="1", timeType="1", type="3",
                                       sortField="", sortType="",
                                       pageNum=1, pageSize=15, status_code=200, **kwargs):
        """交付看板-按产品维度交付率简表"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{KANBAN_PREFIX}/getSimpleProductList.do"
        payload = {
            "dataType": dataType,
            "timeType": timeType,
            "type": type,
            "beginDate": beginDate,
            "endDate": endDate,
            "supplierId": supplierId,
            "sortField": sortField,
            "sortType": sortType,
            "pageNum": pageNum,
            "pageSize": pageSize,
        }
        error_msg = kwargs.pop("error_msg", "产品交付率简表查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("交付看板-客户简表")
    def kanban_get_simple_customer_list(self, supplierId, beginDate, endDate,
                                        dataType="1", timeType="1", type="3",
                                        sortField="", sortType="",
                                        pageNum=1, pageSize=15, status_code=200, **kwargs):
        """交付看板-按客户维度交付率简表"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{KANBAN_PREFIX}/getSimpleCustomerList.do"
        payload = {
            "dataType": dataType,
            "timeType": timeType,
            "type": type,
            "beginDate": beginDate,
            "endDate": endDate,
            "supplierId": supplierId,
            "sortField": sortField,
            "sortType": sortType,
            "pageNum": pageNum,
            "pageSize": pageSize,
        }
        error_msg = kwargs.pop("error_msg", "客户交付率简表查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("交付看板-业务员简表")
    def kanban_get_simple_salesman_list(self, supplierId, beginDate, endDate,
                                        dataType="1", timeType="1", type="3",
                                        sortField="", sortType="",
                                        pageNum=1, pageSize=15, status_code=200, **kwargs):
        """交付看板-按业务员维度交付率简表"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{KANBAN_PREFIX}/getSimpleSalesmanList.do"
        payload = {
            "dataType": dataType,
            "timeType": timeType,
            "type": type,
            "beginDate": beginDate,
            "endDate": endDate,
            "supplierId": supplierId,
            "sortField": sortField,
            "sortType": sortType,
            "pageNum": pageNum,
            "pageSize": pageSize,
        }
        error_msg = kwargs.pop("error_msg", "业务员交付率简表查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("交付看板-订单交付状态列表")
    def kanban_get_order_delivery_status_list(self, supplierId, beginDate, endDate,
                                              status_code=200, **kwargs):
        """交付看板-按日订单交付状态汇总列表"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{KANBAN_PREFIX}/getOrderDeliveryStatusList.do"
        payload = {
            "supplierId": supplierId,
            "beginDate": beginDate,
            "endDate": endDate,
        }
        error_msg = kwargs.pop("error_msg", "订单交付状态列表查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 经营分析 ====================

    @allure.step("经营分析-重点客户")
    def pandect_find_key_customer(self, startTime, endTime, rangeType,
                                  supplierList, decide, status_code=200, **kwargs):
        """经营分析-重点客户统计（重要/重复/迭代客户金额）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{PANDECT_PREFIX}/findKeyCustomer.do"
        payload = {
            "startTime": startTime,
            "endTime": endTime,
            "rangeType": rangeType,
            "supplierList": supplierList,
            "decide": decide,
        }
        error_msg = kwargs.pop("error_msg", "经营分析重点客户查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("经营分析-目标数据")
    def pandect_target_data(self, startTime, endTime, rangeType,
                            supplierList, decideList, status_code=200, **kwargs):
        """经营分析-目标数据统计（按 dataType 分组的占比与环比）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{PANDECT_PREFIX}/targetData.do"
        payload = {
            "startTime": startTime,
            "endTime": endTime,
            "rangeType": rangeType,
            "supplierList": supplierList,
            "decideList": decideList,
        }
        error_msg = kwargs.pop("error_msg", "经营分析目标数据查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("经营分析-售后供应商列表")
    def aftermarket_find_supplier_list(self, status_code=200, **kwargs):
        """经营分析-售后供应商列表"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{AFTERMARKET_PREFIX}/findSupplierList.do"
        error_msg = kwargs.pop("error_msg", "售后供应商列表查询失败")
        return self.post(url, json={}, status_code=status_code, error_msg=error_msg)

    @allure.step("经营分析-售后处理时长")
    def aftermarket_select_duration(self, startTime, endTime, rangeType,
                                    supplierList, decideList, status_code=200, **kwargs):
        """经营分析-售后处理时长统计（平均/标准/超时率）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        url = f"{AFTERMARKET_PREFIX}/selectDuration.do"
        payload = {
            "startTime": startTime,
            "endTime": endTime,
            "rangeType": rangeType,
            "supplierList": supplierList,
            "decideList": decideList,
        }
        error_msg = kwargs.pop("error_msg", "售后处理时长查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 竞对产品列表 ====================

    @allure.step("竞对产品-列表查询")
    def rival_product_get_list(self, pageNo=1, pageSize=15,
                                companyTypeList=None, productLayerList=None,
                                minGramWeight="", maxGramWeight="",
                                sort="", sortType="",
                                status_code=200, **kwargs):
        """竞对产品列表（rival/product/getList.do），产品策略克重等级数据源

        返参 data: total / list各竞对产品数据
        每产品: materialName/totalGramWeight/productGramWeight/productLayer等
        """
        # Author: Author
        # Create Date: 2026-08-28
        # IsAI: True
        url = f"{RIVAL_PRODUCT_PREFIX}/getList.do"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "companyTypeList": companyTypeList or [],
            "productLayerList": productLayerList or [],
            "minGramWeight": minGramWeight,
            "maxGramWeight": maxGramWeight,
            "sort": sort,
            "sortType": sortType,
        }
        error_msg = kwargs.pop("error_msg", "竞对产品列表查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 市场目标 ====================

    @allure.step("市场目标-产品市场需求")
    def get_product_market(self, pageNo=1, pageSize=15, status_code=200, **kwargs):
        """产品市场需求（goal/market/getProductMarket.do），产品策略市场需求数据源

        返参 data: total / list各产品市场需求
        每产品: productId/productName/goalAvailableMarket(人工设置)/totalAvailableMarket(系统计算)
        """
        # Author: Author
        # Create Date: 2026-08-28
        # IsAI: True
        url = f"{MARKET_PREFIX}/getProductMarket.do"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        error_msg = kwargs.pop("error_msg", "产品市场需求查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
