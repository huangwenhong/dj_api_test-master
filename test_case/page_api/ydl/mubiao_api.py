# -*- coding: utf-8 -*-
"""易单来 - 目标管理相关接口（基于 Swagger 文档生成）"""

from datetime import datetime

import allure
from test_case.page_api.public.base_api import BaseAPI

GOAL_PREFIX = "/djsupplier/DJEASYORDER/goal"
FILTER_PREFIX = "/djsupplier/DJEASYORDER/filterscheme"
MANAGE_PREFIX = "/djsupplier/DJEASYORDER/manage"
COCKPIT_MANAGE_PREFIX = "/djsupplier/app/djcockpit/easyorder/manage"
COMMON_PREFIX = "/djsupplier/DJEASYORDER/common"
CREDIT_PREFIX = "/djsupplier/DJEASYORDER/credit"


class MubiaoAPI(BaseAPI):
    """易单来目标管理接口封装"""

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

    # ==================== 目标模块(新) ====================

    @allure.step("获取产品目标信息")
    def get_product_goal_info(self, orgId, month, pageNo=1, pageSize=2000,
                               supplierId=None, filterSchemeConfigId=None,
                               sort="", sortType="",
                               status_code=200, **kwargs):
        """获取产品目标信息"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getProductGoalInfo.do"
        payload = {
            "orgId": orgId,
            "month": month,
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取产品目标信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("下载导入客户目标的错误报告")
    def download_error_report(self, id, status_code=200, **kwargs):
        """下载导入客户目标的错误报告"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/downloadErrorReportNoAuth.do"
        payload = {"id": id}
        error_msg = kwargs.pop("error_msg", "下载导入客户目标的错误报告失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产品区域目标自动分解")
    def product_area_goal_decompose(self, orgId, month, status_code=200, **kwargs):
        """产品区域目标自动分解"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/productAreaGoalDecompose.do"
        payload = {"orgId": orgId, "month": month}
        error_msg = kwargs.pop("error_msg", "产品区域目标自动分解失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("更新客户汇总(无鉴权)")
    def update_customer_summary(self, payload_data, status_code=200, **kwargs):
        """更新客户汇总(无鉴权)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/updateCustomerSummaryNoAuth.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "更新客户汇总失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("更新月需求(无鉴权)")
    def update_month_requirement(self, payload_data, status_code=200, **kwargs):
        """更新月需求(无鉴权)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/updateMonthRequirementNoAuth.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "更新月需求失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("更新考核日期(无鉴权)")
    def update_assessment_date(self, payload_data, status_code=200, **kwargs):
        """更新考核日期(无鉴权)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/updateAssessmentDateNoAuth.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "更新考核日期失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("同步团队目标")
    def sync_team_goal(self, payload_data, status_code=200, **kwargs):
        """同步团队目标"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/syncTeamGoal.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "同步团队目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("导入客户目标")
    def import_customer_goal(self, payload_data, status_code=200, **kwargs):
        """导入客户目标"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/importCustomerGoal.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "导入客户目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("下载客户目标模板(无鉴权)")
    def download_customer_goal_template_no_auth(self, payload_data, status_code=200, return_response=False, **kwargs):
        """下载客户目标模板(无鉴权)，返回 Excel 二进制文件，需要 return_response=True"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/downloadCustomerGoalTemplateNoAuth.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "下载客户目标模板(无鉴权)失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg, return_response=return_response)

    @allure.step("生成组织目标")
    def generate_goal(self, orgId, month, status_code=200, **kwargs):
        """生成组织目标"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/generate.do"
        payload = {"orgId": orgId, "month": month}
        error_msg = kwargs.pop("error_msg", "生成组织目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("目标下发")
    def assign_goal(self, supplierIdList, status_code=200, **kwargs):
        """目标下发"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/assignGoal.do"
        payload = {"supplierIdList": supplierIdList}
        error_msg = kwargs.pop("error_msg", "目标下发失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("目标保存")
    def save_goal(self, orgId, month, status_code=200, **kwargs):
        """目标保存（目标设置-编辑目标）"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/save.do"
        payload = {"orgId": orgId, "month": month}
        error_msg = kwargs.pop("error_msg", "目标保存失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("目标分解")
    def decompose_goal(self, orgId, month,
                        supplierId=None, filterSchemeConfigId=None,
                        team=None,
                        status_code=200, **kwargs):
        """目标分解"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/decompose.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if team is not None: payload["team"] = team
        error_msg = kwargs.pop("error_msg", "目标分解失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 目标设置-二级页面 ====================

    @allure.step("获取总目标详情")
    def get_goal_info(self, orgId, month,
                       supplierId=None, filterSchemeConfigId=None,
                       status_code=200, **kwargs):
        """目标设置-总目标详情（getGoalInfo.do）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getGoalInfo.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        # filterSchemeConfigId 允许传空字符串，用 is not None 判断
        if filterSchemeConfigId is not None: payload["filterSchemeConfigId"] = filterSchemeConfigId
        error_msg = kwargs.pop("error_msg", "获取总目标详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("目标设置列表")
    def get_goal_list(self, orgId=None, month=None,
                       pageNo=1, pageSize=15,
                       supplierIdList=None, monthList=None,
                       goalStatus="", filterSchemeConfigId=None,
                       sort="", sortType="",
                       status_code=200, **kwargs):
        """目标设置-列表（getList.do），支持13月趋势、排序、筛选"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getList.do"
        payload = {"pageNo": pageNo, "pageSize": pageSize}
        if orgId: payload["orgId"] = orgId
        if month: payload["month"] = month
        if supplierIdList is not None: payload["supplierIdList"] = supplierIdList
        if monthList is not None: payload["monthList"] = monthList
        if goalStatus is not None: payload["goalStatus"] = goalStatus
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取目标设置列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取区域目标信息")
    def get_area_goal_info(self, orgId, month, pageNo=1, pageSize=2000,
                            supplierId=None, filterSchemeConfigId=None,
                            sort="", sortType="",
                            status_code=200, **kwargs):
        """目标设置-区域目标信息（getAreaGoalInfo.do）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getAreaGoalInfo.do"
        payload = {"orgId": orgId, "month": month, "pageNo": pageNo, "pageSize": pageSize}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取区域目标信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取团队目标信息")
    def get_team_goal_info(self, orgId, month,
                            supplierId=None, filterSchemeConfigId=None,
                            sort="", sortType="",
                            status_code=200, **kwargs):
        """目标设置-团队目标信息（getTeamGoalInfo.do）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getTeamGoalInfo.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取团队目标信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户目标信息")
    def get_customer_goal_info(self, orgId, month,
                                supplierId=None, filterSchemeConfigId=None,
                                sort="", sortType="",
                                status_code=200, **kwargs):
        """目标设置-客户目标信息（getCustomerGoalInfo.do），含sumInfo汇总"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getCustomerGoalInfo.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取客户目标信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("复制上月目标")
    def copy_goal(self, orgId, month,
                    supplierId=None, filterSchemeConfigId=None,
                    goal=None, area=None, team=None,
                    product=None, customer=None,
                    status_code=200, **kwargs):
        """目标设置-复制上月目标（copy.do），支持选择性复制：goal/area/team/product/customer"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/copy.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if goal is not None: payload["goal"] = goal
        if area is not None: payload["area"] = area
        if team is not None: payload["team"] = team
        if product is not None: payload["product"] = product
        if customer is not None: payload["customer"] = customer
        error_msg = kwargs.pop("error_msg", "复制上月目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产品区域目标复制")
    def product_area_goal_copy(self, orgId, month, status_code=200, **kwargs):
        """目标设置-产品区域目标复制（productAreaGoalCopy.do）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/productAreaGoalCopy.do"
        payload = {"orgId": orgId, "month": month}
        error_msg = kwargs.pop("error_msg", "产品区域目标复制失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取分供应商信息")
    def get_supplier_info_no_auth(self, status_code=200, **kwargs):
        """目标设置-获取分供应商信息（getSupplierInfoNoAuth.do），无请求body"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getSupplierInfoNoAuth.do"
        error_msg = kwargs.pop("error_msg", "获取分供应商信息失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    @allure.step("获取团队分供应商目标分解信息")
    def get_team_supplier_decompose_info(self, orgId, month, status_code=200, **kwargs):
        """目标设置-团队分供应商目标分解（getTeamSupplierDecomposeInfoNoAuth.do）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getTeamSupplierDecomposeInfoNoAuth.do"
        payload = {"orgId": orgId, "month": month}
        error_msg = kwargs.pop("error_msg", "获取团队分供应商目标分解信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取操作记录列表")
    def get_log_list(self, orgId, month, pageNo=1, pageSize=20, status_code=200, **kwargs):
        """目标设置-操作记录（getLogList.do）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getLogList.do"
        payload = {"orgId": orgId, "month": month, "pageNo": pageNo, "pageSize": pageSize}
        error_msg = kwargs.pop("error_msg", "获取操作记录列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 目标模块(旧) ====================

    @allure.step("下载客户目标模板")
    def download_customer_goal_template(self, yearMonth, pageNo=1, pageSize=20, status_code=200, return_response=False, **kwargs):
        """下载客户目标模板"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/downloadCustomerGoalTemplate.do"
        payload = {
            "yearMonth": yearMonth,
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        error_msg = kwargs.pop("error_msg", "下载客户目标模板失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg, return_response=return_response)

    @allure.step("导入客户目标(判断)")
    def import_customer_goal_judge(self, payload_data, status_code=200, **kwargs):
        """导入客户目标(判断)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/ImportCustomerGoalJudge.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "导入客户目标(判断)失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取销售组织信息集合")
    def get_sales_org_info_list(self, status_code=200, **kwargs):
        """获取销售组织信息集合（异动组织列表）"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/getSalesOrgInfoList.do"
        error_msg = kwargs.pop("error_msg", "获取销售组织信息集合失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    @allure.step("获取销售组织集合")
    def get_sales_org_list(self, status_code=200, **kwargs):
        """获取销售组织集合（异动组织列表）"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/getSalesOrgList.do"
        error_msg = kwargs.pop("error_msg", "获取销售组织集合失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    @allure.step("获取目标组织列表")
    def get_org_list_no_auth(self, month=None, status_code=200, **kwargs):
        """获取目标组织（目标设置-列表/分解/详情-选择组织）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getOrgListNoAuth.do"
        if not month:
            month = datetime.now().strftime("%Y-%m")
        payload = {"month": month}
        error_msg = kwargs.pop("error_msg", "获取目标组织列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 目标跟踪 ====================

    @allure.step("团队目标跟踪-周维度")
    def get_week_team_goal_trace(self, orgId, status_code=200, **kwargs):
        """团队目标跟踪-周维度"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getWeekTeamGoalTraceDetail.do"
        payload = {"orgId": orgId}
        error_msg = kwargs.pop("error_msg", "团队目标跟踪-周维度失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("业务员跟踪列表")
    def get_salesman_trace_list(self, payload_data, status_code=200, **kwargs):
        """业务员跟踪列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getSalesmanTraceList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取业务员跟踪列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产品客户详情")
    def get_product_customer_detail(self, orgId, month,
                                      pageNo=1, pageSize=15,
                                      selectDate=None, yearMonthList=None, dateList=None,
                                      productIdList=None, customerIdList=None,
                                      supplierId=None, filterSchemeConfigId=None,
                                      sort="", sortType="",
                                      status_code=200, **kwargs):
        """产品客户详情"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getProductCustomerDetail.do"
        payload = {"orgId": orgId, "month": month, "pageNo": pageNo, "pageSize": pageSize}
        if selectDate: payload["selectDate"] = selectDate
        if yearMonthList: payload["yearMonthList"] = yearMonthList
        if dateList: payload["dateList"] = dateList
        if productIdList is not None: payload["productIdList"] = productIdList
        if customerIdList is not None: payload["customerIdList"] = customerIdList
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取产品客户详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产品层级列表")
    def get_product_layer_list(self, payload_data, status_code=200, **kwargs):
        """产品层级列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getProductLayerList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取产品层级列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产品汇总")
    def get_product_summary(self, payload_data, status_code=200, **kwargs):
        """产品汇总"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getProductSummary.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取产品汇总失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产品层级跟踪列表")
    def get_product_layer_trace_list(self, payload_data, status_code=200, **kwargs):
        """产品层级跟踪列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getProductLayerTraceList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取产品层级跟踪列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产品目标跟踪详情")
    def get_product_goal_trace(self, orgId, month,
                                pageNo=1, pageSize=20,
                                weekMonth=None, yearMonthList=None, dateList=None,
                                dimension=None,
                                goalValue=None, mom=None, monthDiff=None, yesterdayDiff=None,
                                supplierId=None, filterSchemeConfigId=None,
                                selectDate=None, startDate=None, endDate=None,
                                sort="", sortType="",
                                status_code=200, **kwargs):
        """产品目标跟踪详情"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getProductGoalTraceDetail.do"
        payload = {"orgId": orgId, "month": month, "pageNo": pageNo, "pageSize": pageSize}
        if weekMonth: payload["weekMonth"] = weekMonth
        if yearMonthList: payload["yearMonthList"] = yearMonthList
        if dateList: payload["dateList"] = dateList
        if dimension: payload["dimension"] = dimension
        if goalValue: payload["goalValue"] = goalValue
        if mom: payload["mom"] = mom
        if monthDiff: payload["monthDiff"] = monthDiff
        if yesterdayDiff: payload["yesterdayDiff"] = yesterdayDiff
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if selectDate: payload["selectDate"] = selectDate
        if startDate: payload["startDate"] = startDate
        if endDate: payload["endDate"] = endDate
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取产品目标跟踪详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产品目标跟踪-周维度")
    def get_week_product_goal_trace(self, payload_data, status_code=200, **kwargs):
        """产品目标跟踪-周维度"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getWeekProductGoalTraceDetail.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取产品目标跟踪-周维度失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产品跟踪列表")
    def get_product_trace_list(self, payload_data, status_code=200, **kwargs):
        """产品跟踪列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getProductTraceList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取产品跟踪列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("区域趋势")
    def get_area_trend(self, payload_data, status_code=200, **kwargs):
        """区域趋势"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getAreaTrend.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取区域趋势失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("区域目标跟踪详情")
    def get_area_goal_trace(self, orgId, month,
                            weekMonth=None, yearMonthList=None, dateList=None,
                            dimension=None, areaCodeList=None,
                            goalValue=None, mom=None, monthDiff=None, yesterdayDiff=None,
                            supplierId=None, filterSchemeConfigId=None,
                            selectDate=None, startDate=None, endDate=None,
                            sort="", sortType="",
                            status_code=200, **kwargs):
        """区域目标跟踪详情"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getAreaGoalTraceDetail.do"
        payload = {"orgId": orgId, "month": month}
        if weekMonth: payload["weekMonth"] = weekMonth
        if yearMonthList: payload["yearMonthList"] = yearMonthList
        if dateList: payload["dateList"] = dateList
        if dimension: payload["dimension"] = dimension
        if areaCodeList is not None: payload["areaCodeList"] = areaCodeList
        if goalValue: payload["goalValue"] = goalValue
        if mom: payload["mom"] = mom
        if monthDiff: payload["monthDiff"] = monthDiff
        if yesterdayDiff: payload["yesterdayDiff"] = yesterdayDiff
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if selectDate: payload["selectDate"] = selectDate
        if startDate: payload["startDate"] = startDate
        if endDate: payload["endDate"] = endDate
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取区域目标跟踪详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("区域供应商目标跟踪-周维度")
    def get_week_area_supplier_goal_trace(self, payload_data, status_code=200, **kwargs):
        """区域供应商目标跟踪-周维度"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getWeekAreaSupplierGoalTraceDetail.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取区域供应商目标跟踪-周维度失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("区域供应商目标跟踪详情")
    def get_area_supplier_goal_trace(self, payload_data, status_code=200, **kwargs):
        """区域供应商目标跟踪详情"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getAreaSupplierGoalTraceDetail.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取区域供应商目标跟踪详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("区域目标跟踪-周维度")
    def get_week_area_goal_trace(self, payload_data, status_code=200, **kwargs):
        """区域目标跟踪-周维度"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getWeekAreaGoalTraceDetail.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取区域目标跟踪-周维度失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("团队汇总")
    def get_team_summary(self, payload_data, status_code=200, **kwargs):
        """团队汇总"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getTeamSummary.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取团队汇总失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("团队目标跟踪详情")
    def get_team_goal_trace_detail(self, orgId, month,
                                     weekMonth=None, yearMonthList=None, dateList=None,
                                     dimension=None,
                                     goalValue=None, mom=None, monthDiff=None, yesterdayDiff=None,
                                     supplierId=None, filterSchemeConfigId=None,
                                     selectDate=None, startDate=None, endDate=None,
                                     status_code=200, **kwargs):
        """团队目标跟踪详情"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getTeamGoalTraceDetail.do"
        payload = {"orgId": orgId, "month": month}
        if weekMonth: payload["weekMonth"] = weekMonth
        if yearMonthList: payload["yearMonthList"] = yearMonthList
        if dateList: payload["dateList"] = dateList
        if dimension: payload["dimension"] = dimension
        if goalValue: payload["goalValue"] = goalValue
        if mom: payload["mom"] = mom
        if monthDiff: payload["monthDiff"] = monthDiff
        if yesterdayDiff: payload["yesterdayDiff"] = yesterdayDiff
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if selectDate: payload["selectDate"] = selectDate
        if startDate: payload["startDate"] = startDate
        if endDate: payload["endDate"] = endDate
        error_msg = kwargs.pop("error_msg", "获取团队目标跟踪详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("团队供应商目标跟踪-周维度")
    def get_week_team_supplier_goal_trace(self, payload_data, status_code=200, **kwargs):
        """团队供应商目标跟踪-周维度"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getWeekTeamSupplierGoalTraceDetail.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取团队供应商目标跟踪-周维度失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("团队供应商目标跟踪-月维度")
    def get_team_supplier_goal_trace(self, payload_data, status_code=200, **kwargs):
        """团队供应商目标跟踪-月维度"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getTeamSupplierGoalTraceDetail.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取团队供应商目标跟踪-月维度失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产品区域跟踪")
    def get_product_area_detail(self, orgId, month,
                                  pageNo=1, pageSize=15,
                                  selectDate=None, yearMonthList=None, dateList=None,
                                  productIdList=None, areaIdList=None,
                                  supplierId=None, filterSchemeConfigId=None,
                                  sort="", sortType="",
                                  status_code=200, **kwargs):
        """产品区域跟踪"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getProductAreaDetail.do"
        payload = {"orgId": orgId, "month": month, "pageNo": pageNo, "pageSize": pageSize}
        if selectDate: payload["selectDate"] = selectDate
        if yearMonthList: payload["yearMonthList"] = yearMonthList
        if dateList: payload["dateList"] = dateList
        if productIdList is not None: payload["productIdList"] = productIdList
        if areaIdList is not None: payload["areaIdList"] = areaIdList
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取产品区域跟踪详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("团队目标追踪列表")
    def get_team_trace_list(self, payload_data, status_code=200, **kwargs):
        """团队目标追踪列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getTeamTraceList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取团队目标追踪列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("客户目标跟踪详情")
    def get_customer_goal_trace_detail(self, orgId, month,
                                        pageNo=1, pageSize=15,
                                        weekMonth=None, yearMonthList=None, dateList=None,
                                        dimension=None, areaCodeList=None,
                                        salesmanIdList=None, customerIdList=None, customerTypeList=None,
                                        priorityFollowUp="",
                                        goalValue=None, reachProgress=None, monthDiff=None, scheduleDeviation=None,
                                        supplierId=None, filterSchemeConfigId=None,
                                        selectDate=None, startDate=None, endDate=None,
                                        sort="", sortType="", pageJump=False,
                                        status_code=200, **kwargs):
        """客户目标跟踪详情"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getCustomerGoalTraceDetail.do"
        payload = {"orgId": orgId, "month": month, "pageNo": pageNo, "pageSize": pageSize}
        if weekMonth: payload["weekMonth"] = weekMonth
        if yearMonthList: payload["yearMonthList"] = yearMonthList
        if dateList: payload["dateList"] = dateList
        if dimension: payload["dimension"] = dimension
        if areaCodeList is not None: payload["areaCodeList"] = areaCodeList
        if salesmanIdList is not None: payload["salesmanIdList"] = salesmanIdList
        if customerIdList is not None: payload["customerIdList"] = customerIdList
        if customerTypeList is not None: payload["customerTypeList"] = customerTypeList
        if priorityFollowUp: payload["priorityFollowUp"] = priorityFollowUp
        if goalValue: payload["goalValue"] = goalValue
        if reachProgress: payload["reachProgress"] = reachProgress
        if monthDiff: payload["monthDiff"] = monthDiff
        if scheduleDeviation: payload["scheduleDeviation"] = scheduleDeviation
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if selectDate: payload["selectDate"] = selectDate
        if startDate: payload["startDate"] = startDate
        if endDate: payload["endDate"] = endDate
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        if pageJump: payload["pageJump"] = pageJump
        error_msg = kwargs.pop("error_msg", "获取客户目标跟踪详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 目标跟踪-总目标二级页面 ====================

    @allure.step("获取筛选方案配置列表")
    def get_all_filter_scheme_no_auth(self, status_code=200, **kwargs):
        """获取筛选方案配置列表（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{FILTER_PREFIX}/config/getAllNoAuth.do"
        error_msg = kwargs.pop("error_msg", "获取筛选方案配置列表失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    @allure.step("获取总目标跟踪汇总信息")
    def get_summary(self, orgId, month, startTime=None, endTime=None,
                    supplierId=None, filterSchemeConfigId=None,
                    status_code=200, **kwargs):
        """获取目标汇总信息（今日接单/日均面积/均价/总面积/总金额/月活）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getGetSummary.do"
        payload = {"orgId": orgId, "month": month}
        if startTime:
            payload["startTime"] = startTime
        if endTime:
            payload["endTime"] = endTime
        if supplierId:
            payload["supplierId"] = supplierId
        if filterSchemeConfigId:
            payload["filterSchemeConfigId"] = filterSchemeConfigId
        error_msg = kwargs.pop("error_msg", "获取目标汇总信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取总目标跟踪历史13个月图表")
    def get_total_goal_month_chart(self, orgId, month,
                                    selectDate=None,
                                    supplierId=None, filterSchemeConfigId=None,
                                    status_code=200, **kwargs):
        """总目标跟踪-历史13个月图表（日均面积/均价/总面积/总金额/月活）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getTotalGoalMonthChart.do"
        payload = {"orgId": orgId, "month": month}
        if selectDate:
            payload["selectDate"] = selectDate
        if supplierId:
            payload["supplierId"] = supplierId
        if filterSchemeConfigId:
            payload["filterSchemeConfigId"] = filterSchemeConfigId
        error_msg = kwargs.pop("error_msg", "获取总目标跟踪历史13个月图表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取总目标区域月跟踪详情")
    def get_total_goal_area_month_trace_detail(self, orgId, month,
                                                dateList=None, yearMonthList=None,
                                                selectDate=None,
                                                supplierId=None, filterSchemeConfigId=None,
                                                status_code=200, **kwargs):
        """总目标跟踪-接单面积-月跟踪表格"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getTotalGoalAreaMonthTraceDetail.do"
        payload = {"orgId": orgId, "month": month}
        if dateList:
            payload["dateList"] = dateList
        if yearMonthList:
            payload["yearMonthList"] = yearMonthList
        if selectDate:
            payload["selectDate"] = selectDate
        if supplierId:
            payload["supplierId"] = supplierId
        if filterSchemeConfigId:
            payload["filterSchemeConfigId"] = filterSchemeConfigId
        error_msg = kwargs.pop("error_msg", "获取总目标区域月跟踪详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取子组织列表")
    def get_sub_org_no_auth(self, orgId, monthList=None, supplierId=None,
                            status_code=200, **kwargs):
        """获取子组织列表（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getSubOrgNoAuth.do"
        payload = {"orgId": orgId}
        if monthList:
            payload["monthList"] = monthList
        if supplierId:
            payload["supplierId"] = supplierId
        error_msg = kwargs.pop("error_msg", "获取子组织列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户看板状态数量")
    def get_customer_board_state_num(self, orgId, month,
                                      supplierId=None, state="", dimension=None,
                                      salesmanIdList=None, customerId="", areaCodeList=None,
                                      subOrgId="", noOrderDays="", lossDays="", activeRingGrowth="",
                                      lastMonth=1, filterSchemeConfigId=None,
                                      ringGrowthType="amount", ringGrowthMin="", ringGrowthMax="",
                                      monthRequirementAreaMin="", monthRequirementAreaMax="",
                                      status_code=200, **kwargs):
        """获取客户看板状态数量（目标跟踪）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{MANAGE_PREFIX}/getCustomerBoardStateNumForGoalTrace.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if state is not None: payload["state"] = state
        if dimension: payload["dimension"] = dimension
        if salesmanIdList is not None: payload["salesmanIdList"] = salesmanIdList
        if customerId is not None: payload["customerId"] = customerId
        if areaCodeList is not None: payload["areaCodeList"] = areaCodeList
        if subOrgId is not None: payload["subOrgId"] = subOrgId
        if noOrderDays is not None: payload["noOrderDays"] = noOrderDays
        if lossDays is not None: payload["lossDays"] = lossDays
        if activeRingGrowth is not None: payload["activeRingGrowth"] = activeRingGrowth
        payload["lastMonth"] = lastMonth
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if ringGrowthType: payload["ringGrowthType"] = ringGrowthType
        if ringGrowthMin is not None: payload["ringGrowthMin"] = ringGrowthMin
        if ringGrowthMax is not None: payload["ringGrowthMax"] = ringGrowthMax
        if monthRequirementAreaMin is not None: payload["monthRequirementAreaMin"] = monthRequirementAreaMin
        if monthRequirementAreaMax is not None: payload["monthRequirementAreaMax"] = monthRequirementAreaMax
        error_msg = kwargs.pop("error_msg", "获取客户看板状态数量失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取产品列表-历史无数据")
    def get_product_list_history_null_no_auth(self, orgId, month,
                                              startTime=None, endTime=None,
                                              supplierId=None, filterSchemeConfigId=None,
                                              dateType=None,
                                              status_code=200, **kwargs):
        """获取产品列表-历史无数据（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getProductListHistoryNullNoAuth.do"
        payload = {"orgId": orgId, "month": month}
        if startTime:
            payload["startTime"] = startTime
        if endTime:
            payload["endTime"] = endTime
        if supplierId:
            payload["supplierId"] = supplierId
        if filterSchemeConfigId:
            payload["filterSchemeConfigId"] = filterSchemeConfigId
        if dateType:
            payload["dateType"] = dateType
        error_msg = kwargs.pop("error_msg", "获取产品列表-历史无数据失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户列表-按组织")
    def get_customer_by_org_no_auth(self, pageNo=1, pageSize=100, keyword="",
                                     status_code=200, **kwargs):
        """获取客户列表-按组织（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getCustomerByOrgNoAuth.do"
        payload = {"pageNo": pageNo, "pageSize": pageSize, "keyword": keyword}
        error_msg = kwargs.pop("error_msg", "获取客户列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取区域列表-按组织")
    def get_area_by_org_no_auth(self, orgId, status_code=200, **kwargs):
        """获取区域列表-按组织（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getAreaByOrgNoAuth.do"
        payload = {"orgId": orgId}
        error_msg = kwargs.pop("error_msg", "获取区域列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取组织区域列表")
    def get_org_region_list_no_auth(self, orgId, month,
                                     startTime=None, endTime=None,
                                     supplierId=None, filterSchemeConfigId=None,
                                     status_code=200, **kwargs):
        """获取组织区域列表（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{MANAGE_PREFIX}/getOrgRegionListNoAuth.do"
        payload = {"orgId": orgId, "month": month}
        if startTime:
            payload["startTime"] = startTime
        if endTime:
            payload["endTime"] = endTime
        if supplierId:
            payload["supplierId"] = supplierId
        if filterSchemeConfigId:
            payload["filterSchemeConfigId"] = filterSchemeConfigId
        error_msg = kwargs.pop("error_msg", "获取组织区域列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取子组织列表-manage")
    def get_sub_org_no_auth_by_manage(self, orgId, month,
                                       startTime=None, endTime=None,
                                       supplierId=None, filterSchemeConfigId=None,
                                       status_code=200, **kwargs):
        """获取子组织列表-manage模块（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{COCKPIT_MANAGE_PREFIX}/getSubOrgNoAuth.do"
        payload = {"orgId": orgId, "month": month}
        if startTime:
            payload["startTime"] = startTime
        if endTime:
            payload["endTime"] = endTime
        if supplierId:
            payload["supplierId"] = supplierId
        if filterSchemeConfigId:
            payload["filterSchemeConfigId"] = filterSchemeConfigId
        error_msg = kwargs.pop("error_msg", "获取子组织列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户看板列表")
    def get_customer_board_list(self, orgId, month,
                                 pageNo=1, pageSize=15,
                                 supplierId=None, state="", dimension=None,
                                 salesmanIdList=None, customerId="", areaCodeList=None,
                                 subOrgId="", noOrderDays="", lossDays="", activeRingGrowth="",
                                 lastMonth=1, filterSchemeConfigId=None,
                                 ringGrowthType="amount", ringGrowthMin="", ringGrowthMax="",
                                 monthRequirementAreaMin="", monthRequirementAreaMax="",
                                 sort="", sortType="",
                                 status_code=200, **kwargs):
        """获取客户看板列表（目标跟踪）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{MANAGE_PREFIX}/getCustomerBoardListForGoalTrace.do"
        payload = {"orgId": orgId, "month": month, "pageNo": pageNo, "pageSize": pageSize}
        if supplierId: payload["supplierId"] = supplierId
        if state is not None: payload["state"] = state
        if dimension: payload["dimension"] = dimension
        if salesmanIdList is not None: payload["salesmanIdList"] = salesmanIdList
        if customerId is not None: payload["customerId"] = customerId
        if areaCodeList is not None: payload["areaCodeList"] = areaCodeList
        if subOrgId is not None: payload["subOrgId"] = subOrgId
        if noOrderDays is not None: payload["noOrderDays"] = noOrderDays
        if lossDays is not None: payload["lossDays"] = lossDays
        if activeRingGrowth is not None: payload["activeRingGrowth"] = activeRingGrowth
        payload["lastMonth"] = lastMonth
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if ringGrowthType: payload["ringGrowthType"] = ringGrowthType
        if ringGrowthMin is not None: payload["ringGrowthMin"] = ringGrowthMin
        if ringGrowthMax is not None: payload["ringGrowthMax"] = ringGrowthMax
        if monthRequirementAreaMin is not None: payload["monthRequirementAreaMin"] = monthRequirementAreaMin
        if monthRequirementAreaMax is not None: payload["monthRequirementAreaMax"] = monthRequirementAreaMax
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取客户看板列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取用户CRM权限")
    def get_user_crm_auth(self, status_code=200, **kwargs):
        """获取用户CRM权限"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{COMMON_PREFIX}/getUserCrmAuth.do"
        error_msg = kwargs.pop("error_msg", "获取用户CRM权限失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg, **kwargs)

    @allure.step("获取子组织目标")
    def get_sub_org_goal_no_auth(self, orgId, month,
                                  supplierId=None, filterSchemeConfigId=None,
                                  status_code=200, **kwargs):
        """获取子组织目标（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getSubOrgGoalNoAuth.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        error_msg = kwargs.pop("error_msg", "获取子组织目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取区域日均")
    def get_day_avg_area(self, orgId, month,
                          supplierId=None, filterSchemeConfigId=None,
                          status_code=200, **kwargs):
        """获取区域日均（历史参考）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getDayAvgArea.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        error_msg = kwargs.pop("error_msg", "获取区域日均失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取去年同期目标")
    def get_last_year_goal_info(self, orgId, month,
                                 supplierId=None, filterSchemeConfigId=None,
                                 status_code=200, **kwargs):
        """获取去年同期目标（历史参考）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getLastYearGoalInfo.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        error_msg = kwargs.pop("error_msg", "获取去年同期目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取历史区域目标")
    def get_history_area_goal(self, orgId, month,
                               supplierId=None, filterSchemeConfigId=None,
                               areaCodeList=None, sort="", sortType="",
                               status_code=200, **kwargs):
        """获取历史区域目标"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getAreaGoal.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if areaCodeList is not None: payload["areaCodeList"] = areaCodeList
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取历史区域目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取区域供应商目标")
    def get_area_supplier_goal_no_auth(self, orgId, month,
                                        supplierId=None, filterSchemeConfigId=None,
                                        areaCodeList=None, sort="", sortType="",
                                        status_code=200, **kwargs):
        """获取区域供应商目标（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getAreaSupplierGoalNoAuth.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if areaCodeList is not None: payload["areaCodeList"] = areaCodeList
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取区域供应商目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取历史团队目标")
    def get_history_team_goal(self, orgId, month,
                               supplierId=None, supplierID=None,
                               filterSchemeConfigId=None,
                               orgIdList=None, sort="", sortType="",
                               status_code=200, **kwargs):
        """获取历史团队目标"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getTeamGoal.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if supplierID: payload["supplierID"] = supplierID
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if orgIdList is not None: payload["orgIdList"] = orgIdList
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取历史团队目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取团队供应商目标")
    def get_team_supplier_goal_no_auth(self, orgId, month,
                                        supplierId=None, supplierID=None,
                                        filterSchemeConfigId=None,
                                        orgIdList=None, sort="", sortType="",
                                        status_code=200, **kwargs):
        """获取团队供应商目标（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getTeamSupplierGoalNoAuth.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if supplierID: payload["supplierID"] = supplierID
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if orgIdList is not None: payload["orgIdList"] = orgIdList
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "获取团队供应商目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取历史产品目标")
    def get_history_product_goal(self, orgId, month,
                                  pageNo=1, pageSize=15,
                                  supplierId=None, filterSchemeConfigId=None,
                                  productIdList=None, type="area",
                                  sort="", sortType="", sortMonth="",
                                  status_code=200, **kwargs):
        """获取历史产品目标"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getProductGoal.do"
        payload = {"orgId": orgId, "month": month, "pageNo": pageNo, "pageSize": pageSize}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if productIdList is not None: payload["productIdList"] = productIdList
        if type: payload["type"] = type
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        if sortMonth: payload["sortMonth"] = sortMonth
        error_msg = kwargs.pop("error_msg", "获取历史产品目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取产品列表")
    def get_product_list_no_auth(self, orgId, month,
                                  supplierId=None, filterSchemeConfigId=None,
                                  status_code=200, **kwargs):
        """获取产品列表（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getProductListNoAuth.do"
        payload = {"orgId": orgId, "month": month}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        error_msg = kwargs.pop("error_msg", "获取产品列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取分层产品列表")
    def get_layer_product_list(self, supplierId=None, filterSchemeConfigId=None,
                                status_code=200, **kwargs):
        """获取分层产品列表"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/product/getLayerProductList.do"
        payload = {}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        error_msg = kwargs.pop("error_msg", "获取分层产品列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取产品区域目标列表")
    def get_region_goal_list(self, orgId, goalMonth, productId,
                              supplierId=None, filterSchemeConfigId=None,
                              status_code=200, **kwargs):
        """获取产品区域目标列表"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/product/getRegionGoalList.do"
        payload = {"orgId": orgId, "goalMonth": goalMonth, "productId": productId}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        error_msg = kwargs.pop("error_msg", "获取产品区域目标列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户编辑数据权限")
    def get_customer_edit_data_per_no_auth(self, status_code=200, **kwargs):
        """获取客户编辑数据权限（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/getCustomerEditDataPerNoAuth.do"
        error_msg = kwargs.pop("error_msg", "获取客户编辑数据权限失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg, **kwargs)

    @allure.step("获取竞争对手档案列表")
    def get_rival_archive_list_no_auth(self, pageNo=1, pageSize=9999,
                                        ignoredTypeList=None,
                                        status_code=200, **kwargs):
        """获取竞争对手档案列表（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getRivalArchiveListNoAuth.do"
        payload = {"pageNo": pageNo, "pageSize": pageSize}
        if ignoredTypeList is not None: payload["ignoredTypeList"] = ignoredTypeList
        error_msg = kwargs.pop("error_msg", "获取竞争对手档案列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取业务员列表")
    def get_salesman_by_org_no_auth(self, status_code=200, **kwargs):
        """获取业务员列表（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getSalesmanByOrgNoAuth.do"
        error_msg = kwargs.pop("error_msg", "获取业务员列表失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg, **kwargs)

    @allure.step("获取历史客户目标")
    def get_history_customer_goal(self, orgId, month,
                                   pageNo=1, pageSize=15,
                                   supplierId=None, filterSchemeConfigId=None,
                                   type=None, customerIdList=None,
                                   salesmanIdList=None, goalValue=None,
                                   priorityFollowUp="", goalMinimum="", goalMaximum="",
                                   dataType="order_area", sort="", sortType="", sortMonth="",
                                   status_code=200, **kwargs):
        """获取历史客户目标"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getCustomerGoal.do"
        payload = {"orgId": orgId, "month": month, "pageNo": pageNo, "pageSize": pageSize}
        if supplierId: payload["supplierId"] = supplierId
        if filterSchemeConfigId: payload["filterSchemeConfigId"] = filterSchemeConfigId
        if type is not None: payload["type"] = type
        if customerIdList is not None: payload["customerIdList"] = customerIdList
        if salesmanIdList is not None: payload["salesmanIdList"] = salesmanIdList
        if goalValue is not None: payload["goalValue"] = goalValue
        if priorityFollowUp is not None: payload["priorityFollowUp"] = priorityFollowUp
        if goalMinimum is not None: payload["goalMinimum"] = goalMinimum
        if goalMaximum is not None: payload["goalMaximum"] = goalMaximum
        if dataType: payload["dataType"] = dataType
        if sort: payload["sort"] = sort
        if sortType: payload["sortType"] = sortType
        if sortMonth: payload["sortMonth"] = sortMonth
        error_msg = kwargs.pop("error_msg", "获取历史客户目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取信用配置")
    def get_credit_config_no_auth(self, status_code=200, **kwargs):
        """获取信用配置（无鉴权）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{CREDIT_PREFIX}/getCreditConfigNoAuth.do"
        error_msg = kwargs.pop("error_msg", "获取信用配置失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg, **kwargs)

    @allure.step("客户类型达成分析")
    def get_customer_type_reach(self, orgId, month,
                                startTime=None, endTime=None,
                                filterSchemeConfigId=None, supplierId=None,
                                status_code=200, **kwargs):
        """目标跟踪-首页客户目标：客户类型达成分析（getCustomerTypeReach.do）

        swagger 入参:
          必填: orgId(组织id), month(月份 yyyy-MM)
          可选: startTime(开始时间), endTime(结束时间),
                filterSchemeConfigId(筛选方案配置id), supplierId(供应商id)
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/trace/getCustomerTypeReach.do"
        payload = {"orgId": orgId, "month": month}
        if startTime is not None:
            payload["startTime"] = startTime
        if endTime is not None:
            payload["endTime"] = endTime
        if filterSchemeConfigId is not None:
            payload["filterSchemeConfigId"] = filterSchemeConfigId
        if supplierId is not None:
            payload["supplierId"] = supplierId
        error_msg = kwargs.pop("error_msg", "获取客户类型达成分析失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 产品目标(历史) ====================

    @allure.step("目标管理-产品目标查询")
    def get_product_goal(self, orgId, month, supplierId, filterSchemeConfigId="",
                         pageNo=1, pageSize=15, type="area", sort="", sortType="",
                         sortMonth="", productIdList=None, status_code=200, **kwargs):
        """产品目标查询（goal/new/history/getProductGoal.do）

        返参 data: total / regularGoalList各产品目标 / dayAvgArea日均面积
        每产品: productId/productName/productDayAvgArea.goal.dif日均目标/
               marketRate/marketRequiredAreaTotal/rivalArchiveList
        """
        # Author: Author
        # Create Date: 2026-08-28
        # IsAI: True
        url = f"{GOAL_PREFIX}/new/history/getProductGoal.do"
        payload = {
            "orgId": orgId,
            "month": month,
            "supplierId": supplierId,
            "filterSchemeConfigId": filterSchemeConfigId,
            "pageNo": pageNo,
            "pageSize": pageSize,
            "productIdList": productIdList or [],
            "type": type,
            "sort": sort,
            "sortType": sortType,
            "sortMonth": sortMonth,
        }
        error_msg = kwargs.pop("error_msg", "产品目标查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)






