# -*- coding: utf-8 -*-
"""易单来 - 签到拜访相关接口（基于 Swagger 文档生成）"""

import allure
from test_case.page_api.public.base_api import BaseAPI

SIGNIN_PREFIX = "/djsupplier/DJEASYORDER/signIn"
VISIT_PREFIX = "/djsupplier/DJEASYORDER/visit"
VISIT_CONFIG_PREFIX = "/djsupplier/DJEASYORDER/visitConfig"
CUSTOMER_VISIT_TASK_PREFIX = "/djsupplier/DJEASYORDER/customerVisitTask"
SALESMAN_PREFIX = "/djsupplier/app/djcockpit/easyorder/salesman"


class QiandaoBaifangAPI(BaseAPI):
    """易单来签到拜访接口封装"""

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

    # ==================== 签到记录 ====================

    @allure.step("获取所有业务员签到日历")
    def get_all_salesman_sign_in_calendar(self, payload_data, status_code=200, **kwargs):
        """获取所有业务员签到日历"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/getAllSalesmanSignInCalendar.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取所有业务员签到日历失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取异常签到列表")
    def get_abnormal_sign_in_list(self, payload_data, status_code=200, **kwargs):
        """获取异常签到列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/getAbnormalSignInList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取异常签到列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("导出所有签到记录")
    def export_all_sign_in_list(self, payload_data, status_code=200, **kwargs):
        """导出所有签到记录"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/exportAllSignInList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "导出所有签到记录失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP异常签到")
    def app_abnormal_sign_in(self, payload_data, status_code=200, **kwargs):
        """APP异常签到"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/app_abnormalSignIn.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP异常签到失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP签到")
    def app_sign_in(self, payload_data, status_code=200, **kwargs):
        """APP签到"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/app_signIn.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP签到失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP我的签到列表检查")
    def app_my_sign_in_list_check(self, payload_data, status_code=200, **kwargs):
        """APP我的签到列表检查"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/app_mySignInListCheck.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP我的签到列表检查失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP获取我的签到列表")
    def app_get_my_sign_in_list(self, payload_data, status_code=200, **kwargs):
        """APP获取我的签到列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/app_getMySignInList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP获取我的签到列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP获取所有业务员异常签到")
    def app_get_all_salesman_abnormal_sign_in(self, payload_data, status_code=200, **kwargs):
        """APP获取所有业务员异常签到"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/app_getAllSalesmanAbnormalSignIn.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP获取所有业务员异常签到失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP获取客户地址变更记录")
    def app_get_customer_address_update_record(self, payload_data, status_code=200, **kwargs):
        """APP获取客户地址变更记录"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/app_getCustomerAddressUpdateRecord.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP获取客户地址变更记录失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP获取所有业务员签到日历")
    def app_get_all_salesman_sign_in_calendar(self, payload_data, status_code=200, **kwargs):
        """APP获取所有业务员签到日历"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/app_getAllSalesmanSignInCalendar.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP获取所有业务员签到日历失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP获取所有业务员签到记录")
    def app_get_all_salesman_sign_in(self, time, orgId, status_code=200, **kwargs):
        """APP获取所有业务员签到记录"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/app_getAllSalesmanSignIn.do"
        payload = {"time": time, "orgId": orgId}
        error_msg = kwargs.pop("error_msg", "APP获取所有业务员签到记录失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取所有签到记录")
    def get_all_sign_in_list(self, pageNo, pageSize, status_code=200, **kwargs):
        """获取所有签到记录"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/getAllSignInList.do"
        payload = {"pageNo": pageNo, "pageSize": pageSize}
        error_msg = kwargs.pop("error_msg", "获取所有签到记录失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("签到记录排查定时任务")
    def sign_in_record_check_task(self, status_code=200, **kwargs):
        """签到记录排查定时任务"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = "/djsupplier/DJEASYORDER/common/signInRecordCheckTaskCommon"
        error_msg = kwargs.pop("error_msg", "签到记录排查定时任务失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    # ==================== 签到报表模块 ====================

    @allure.step("获取组织下业务员选项")
    def report_get_salesman_options_by_org(self, payload_data, status_code=200, **kwargs):
        """获取组织下业务员选项"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/report/getSalesmanOptionsByOrg.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取组织下业务员选项失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取日业务员签到列表")
    def report_get_day_salesman_sign_in_list(self, payload_data, status_code=200, **kwargs):
        """获取日业务员签到列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/report/getDaySalesmanSignInList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取日业务员签到列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("编辑首次签到时间")
    def report_edit_first_sign_in_time(self, payload_data, status_code=200, **kwargs):
        """编辑首次签到时间"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/report/editFirstSignInTime.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "编辑首次签到时间失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取首次签到时间")
    def report_get_first_sign_in_time(self, payload_data, status_code=200, **kwargs):
        """获取首次签到时间"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/report/getFirstSignInTime.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取首次签到时间失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取月业务员签到列表")
    def report_get_month_salesman_sign_in_list(self, payload_data, status_code=200, **kwargs):
        """获取月业务员签到列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/report/getMonthSalesmanSignInList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取月业务员签到列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("编辑签到目标")
    def report_edit_sign_in_goals(self, payload_data, status_code=200, **kwargs):
        """编辑签到目标"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/report/editSignInGoals.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "编辑签到目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取签到目标")
    def report_get_sign_in_goals(self, payload_data, status_code=200, **kwargs):
        """获取签到目标"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/report/getSignInGoals.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取签到目标失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取签到柱状图")
    def report_get_sign_in_bar_chart(self, payload_data, status_code=200, **kwargs):
        """获取签到柱状图"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/report/getSignInBarChart.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取签到柱状图失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取组织选项")
    def report_get_org_option(self, status_code=200, **kwargs):
        """获取组织选项"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/report/getOrgOption.do"
        error_msg = kwargs.pop("error_msg", "获取组织选项失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    # ==================== 签到配置 ====================

    @allure.step("获取AI签到拍照权限(通用)")
    def config_get_ai_sign_in_photo_per(self, status_code=200, **kwargs):
        """获取AI签到拍照权限(通用)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/config/getAISignInPhotoPerCommon.do"
        error_msg = kwargs.pop("error_msg", "获取AI签到拍照权限失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    @allure.step("编辑签到拍照权限")
    def config_edit_sign_in_photo_per(self, payload_data, status_code=200, **kwargs):
        """编辑签到拍照权限"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/config/editSignInPhotoPer.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "编辑签到拍照权限失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取签到拍照权限")
    def config_get_sign_in_photo_per(self, status_code=200, **kwargs):
        """获取签到拍照权限"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{SIGNIN_PREFIX}/config/getSignInPhotoPer.do"
        error_msg = kwargs.pop("error_msg", "获取签到拍照权限失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    # ==================== 拜访记录 ====================

    @allure.step("获取业务员地图列表")
    def get_salesman_list_for_map(self, payload_data, status_code=200, **kwargs):
        """获取业务员地图列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getSalesmanListForMap.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取业务员地图列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取业务员未拜访分析")
    def get_salesman_not_visit_analysis(self, payload_data, status_code=200, **kwargs):
        """获取业务员未拜访分析"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getSalesmanNotVisitAnalysis.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取业务员未拜访分析失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取所有不良类型")
    def get_all_bad_type(self, status_code=200, **kwargs):
        """获取所有不良类型"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getAllBadType.do"
        error_msg = kwargs.pop("error_msg", "获取所有不良类型失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    @allure.step("获取业务员列表(拜访)")
    def get_salesman_list(self, payload_data, status_code=200, **kwargs):
        """获取业务员列表(拜访)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getSalesmanList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取业务员列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取业务员列表(无鉴权)")
    def get_salesman_list_no_auth(self, payload_data, status_code=200, **kwargs):
        """获取业务员列表(无鉴权)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getSalesmanListNoAuth.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取业务员列表(无鉴权)失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取签到记录趋势")
    def get_sign_in_record_trend(self, payload_data, status_code=200, **kwargs):
        """获取签到记录趋势"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getSignInRecordTrend.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取签到记录趋势失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取业务员分析列表")
    def get_salesman_analysis_list(self, payload_data, status_code=200, **kwargs):
        """获取业务员分析列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getSalesmanAnalysisList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取业务员分析列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("导出业务员分析列表")
    def export_salesman_analysis_list(self, payload_data, status_code=200, **kwargs):
        """导出业务员分析列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/exprotSalesmanAnalysisList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "导出业务员分析列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("更新拜访记录(web)")
    def update_visit_record(self, payload_data, status_code=200, **kwargs):
        """更新拜访记录(web)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/updateVisitRecord.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "更新拜访记录失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("更新拜访记录(app)")
    def app_update_visit_record(self, payload_data, status_code=200, **kwargs):
        """更新拜访记录(app)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/app_updateVisitRecord.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP更新拜访记录失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("删除拜访记录")
    def del_visit_record(self, payload_data, status_code=200, **kwargs):
        """删除拜访记录"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/delRecord.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "删除拜访记录失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP删除拜访订单记录")
    def app_del_visit_order_record(self, payload_data, status_code=200, **kwargs):
        """APP删除拜访订单记录"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/app_delVisitOrderRecord.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP删除拜访订单记录失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP获取已拜访信息")
    def app_get_already_visited(self, payload_data, status_code=200, **kwargs):
        """APP获取已拜访信息"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/app_getAlreadyVisited.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP获取已拜访信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户分析列表")
    def get_customer_analysis_list(self, payload_data, status_code=200, **kwargs):
        """获取客户分析列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getCustomerAnalysisList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取客户分析列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("导出客户分析列表")
    def export_customer_analysis_list(self, payload_data, status_code=200, **kwargs):
        """导出客户分析列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/exportCustomerAnalysisList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "导出客户分析列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("导出拜访记录")
    def export_visit_record(self, payload_data, status_code=200, **kwargs):
        """导出拜访记录"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/exportVisitRecord.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "导出拜访记录失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP搜索订单记录")
    def app_search_order_record(self, customerId, status_code=200, **kwargs):
        """APP搜索订单记录"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/app_searchOrderRecord.do"
        payload = {"customerId": customerId}
        error_msg = kwargs.pop("error_msg", "APP搜索订单记录失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("新增拜访记录(app)")
    def app_add_visit_record(self, payload_data, status_code=200, **kwargs):
        """新增拜访记录(app)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/app_addVisitRecord.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP新增拜访记录失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP获取所有负责人信息")
    def app_get_all_duty_info(self, payload_data, status_code=200, **kwargs):
        """APP获取所有负责人信息"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/app_getAllDutyInfo.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP获取所有负责人信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取区域业务员")
    def get_area_sale_man(self, payload_data, status_code=200, **kwargs):
        """获取区域业务员"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getAreaSaleMan.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取区域业务员失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP获取客户线索拜访信息")
    def app_get_customer_clue_visit_info(self, payload_data, status_code=200, **kwargs):
        """APP获取客户线索拜访信息"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/app_getCustomerClueVisitInfo.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP获取客户线索拜访信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户拜访记录")
    def get_customer_visit_record(self, payload_data, status_code=200, **kwargs):
        """获取客户拜访记录"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getCustomerVisitRecord.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取客户拜访记录失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客户拜访记录列表")
    def get_customer_visit_record_list(self, payload_data, status_code=200, **kwargs):
        """获取客户拜访记录列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getCustomerVisitRecordList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取客户拜访记录列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取所有客诉类型")
    def get_all_complaint(self, status_code=200, **kwargs):
        """获取所有客诉类型"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getAllComplaint.do"
        error_msg = kwargs.pop("error_msg", "获取所有客诉类型失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    @allure.step("获取所有拜访目的")
    def get_all_purpose(self, status_code=200, **kwargs):
        """获取所有拜访目的"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getAllPurpose.do"
        error_msg = kwargs.pop("error_msg", "获取所有拜访目的失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    @allure.step("获取所有城市")
    def get_all_city(self, status_code=200, **kwargs):
        """获取所有城市"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getAllCity.do"
        error_msg = kwargs.pop("error_msg", "获取所有城市失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    @allure.step("获取拜访记录列表(web)")
    def get_visit_record_list(self, payload_data, status_code=200, **kwargs):
        """获取拜访记录列表(web)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/getVisitRecordList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取拜访记录列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP获取客户产品列表")
    def app_get_customer_product_list(self, payload_data, status_code=200, **kwargs):
        """APP获取客户产品列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/app_getCustomerProductList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP获取客户产品列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP获取平台产品列表")
    def app_get_platform_product_list(self, payload_data, status_code=200, **kwargs):
        """APP获取平台产品列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/app_getPlatformProductList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP获取平台产品列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP获取用户拜访记录列表")
    def app_get_user_visit_record_list(self, payload_data, status_code=200, **kwargs):
        """APP获取用户拜访记录列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/app_getUserVisitRecordList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP获取用户拜访记录列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("APP获取竞对产品列表")
    def app_get_rival_product_list(self, payload_data, status_code=200, **kwargs):
        """APP获取竞对产品列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_PREFIX}/app_getRivalProductList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "APP获取竞对产品列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 拜访记录_基础设置 ====================

    @allure.step("更新拜访目的状态")
    def config_update_purpose_status(self, payload_data, status_code=200, **kwargs):
        """更新拜访目的状态"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_CONFIG_PREFIX}/updatePurposeStatus.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "更新拜访目的状态失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("更新客诉")
    def config_update_complaint(self, payload_data, status_code=200, **kwargs):
        """更新客诉"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_CONFIG_PREFIX}/updateComplaint.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "更新客诉失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("更新拜访目的")
    def config_update_purpose(self, payload_data, status_code=200, **kwargs):
        """更新拜访目的"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_CONFIG_PREFIX}/updatePurpose.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "更新拜访目的失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("更新客诉状态")
    def config_update_complaint_status(self, payload_data, status_code=200, **kwargs):
        """更新客诉状态"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_CONFIG_PREFIX}/updateComplaintStatus.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "更新客诉状态失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取拜访目的列表")
    def config_get_purpose_list(self, status_code=200, **kwargs):
        """获取拜访目的列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_CONFIG_PREFIX}/getPurposeList.do"
        error_msg = kwargs.pop("error_msg", "获取拜访目的列表失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    @allure.step("新增客诉")
    def config_add_complaint(self, payload_data, status_code=200, **kwargs):
        """新增客诉"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_CONFIG_PREFIX}/addComplaint.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "新增客诉失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("新增拜访目的")
    def config_add_purpose(self, payload_data, status_code=200, **kwargs):
        """新增拜访目的"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_CONFIG_PREFIX}/addPurpose.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "新增拜访目的失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取客诉列表")
    def config_get_complaint_list(self, status_code=200, **kwargs):
        """获取客诉列表"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{VISIT_CONFIG_PREFIX}/getComplaintList.do"
        error_msg = kwargs.pop("error_msg", "获取客诉列表失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg)

    # ==================== 客户拜访任务 ====================

    @allure.step("客户拜访任务校验(无鉴权)")
    def task_valid_no_auth(self, payload_data, status_code=200, **kwargs):
        """客户拜访任务校验(无鉴权)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{CUSTOMER_VISIT_TASK_PREFIX}/taskValidNoAuth.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "客户拜访任务校验失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("新增客户拜访任务")
    def add_customer_visit_task(self, payload_data, status_code=200, **kwargs):
        """新增客户拜访任务"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{CUSTOMER_VISIT_TASK_PREFIX}/add.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "新增客户拜访任务失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("新增客户拜访任务(深圳订单)")
    def add_customer_visit_task_for_sz_order(self, payload_data, status_code=200, **kwargs):
        """新增客户拜访任务(深圳订单)"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{CUSTOMER_VISIT_TASK_PREFIX}/addForSzOrder.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "新增客户拜访任务(深圳订单)失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 业务员拜访概览 ====================

    @allure.step("获取业务员拜访概览")
    def get_salesman_visit_overview(self, payload_data, status_code=200, **kwargs):
        """获取业务员拜访概览（签到客户数/拜访客户数/超期未拜访统计）"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getSalesmanVisitOverview.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取业务员拜访概览失败")
        payload.update(kwargs)
        # 保存原 headers，添加 app-role
        original_headers = self.headers.copy() if self.headers else {}
        self.headers = self.headers or {}
        self.headers["app-role"] = "salesman"
        try:
            result = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        finally:
            self.headers = original_headers
        return result

    # ==================== APP 业务员工作台（/app/djcockpit/easyorder/salesman） ====================

    def _post_app_salesman(self, url, payload_data, status_code, error_msg, **kwargs):
        """APP 业务员工作台接口统一发送：补充 app-role=salesman 请求头。"""
        payload = dict(payload_data)
        payload.update(kwargs)
        original_headers = self.headers.copy() if self.headers else {}
        self.headers = self.headers or {}
        self.headers["app-role"] = "salesman"
        try:
            return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        finally:
            self.headers = original_headers

    @allure.step("业务员工作台-判断合作业务员")
    def salesman_judge_cooperation(self, payload_data, status_code=200, **kwargs):
        """判断是否合作业务员/供应商及组织列表"""
        # Author: Author
        # Create Date: 2026-10-22
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/judgeCooperationSalesman.do"
        error_msg = kwargs.pop("error_msg", "判断合作业务员失败")
        return self._post_app_salesman(url, payload_data, status_code, error_msg, **kwargs)

    @allure.step("业务员工作台-订单产品数量")
    def salesman_get_order_product_num(self, payload_data, status_code=200, **kwargs):
        """获取订单产品数量"""
        # Author: Author
        # Create Date: 2026-10-22
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getOrderProductNum.do"
        error_msg = kwargs.pop("error_msg", "获取订单产品数量失败")
        return self._post_app_salesman(url, payload_data, status_code, error_msg, **kwargs)

    @allure.step("业务员工作台-购物车列表")
    def salesman_get_shopping_cart_list(self, payload_data, status_code=200, **kwargs):
        """获取购物车列表（金额/面积/分页）"""
        # Author: Author
        # Create Date: 2026-10-22
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getShoppingCartList.do"
        error_msg = kwargs.pop("error_msg", "获取购物车列表失败")
        return self._post_app_salesman(url, payload_data, status_code, error_msg, **kwargs)

    @allure.step("业务员工作台-销售概览")
    def salesman_get_sale_overview(self, payload_data, status_code=200, **kwargs):
        """获取业务员销售概览（目标/进度/销售额/面积）"""
        # Author: Author
        # Create Date: 2026-10-22
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getSaleOverview.do"
        error_msg = kwargs.pop("error_msg", "获取业务员销售概览失败")
        return self._post_app_salesman(url, payload_data, status_code, error_msg, **kwargs)

    @allure.step("业务员工作台-客户概览")
    def salesman_get_customer_overview(self, payload_data, status_code=200, **kwargs):
        """获取业务员客户概览（活跃客户数/列表）"""
        # Author: Author
        # Create Date: 2026-10-22
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getSalesmanCustomerOverview.do"
        error_msg = kwargs.pop("error_msg", "获取业务员客户概览失败")
        return self._post_app_salesman(url, payload_data, status_code, error_msg, **kwargs)

    @allure.step("业务员工作台-待办列表")
    def salesman_get_to_be_completed_list(self, payload_data, status_code=200, **kwargs):
        """获取待办列表（金额/面积/分页）"""
        # Author: Author
        # Create Date: 2026-10-22
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getToBeCompletedList.do"
        error_msg = kwargs.pop("error_msg", "获取待办列表失败")
        return self._post_app_salesman(url, payload_data, status_code, error_msg, **kwargs)

    @allure.step("业务员工作台-今日产品列表")
    def salesman_get_today_product_list(self, payload_data, status_code=200, **kwargs):
        """获取今日产品列表（v1）"""
        # Author: Author
        # Create Date: 2026-10-22
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/v1/getTodayProductList.do"
        error_msg = kwargs.pop("error_msg", "获取今日产品列表失败")
        return self._post_app_salesman(url, payload_data, status_code, error_msg, **kwargs)
