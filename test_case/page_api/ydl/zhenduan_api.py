# -*- coding: utf-8 -*-
"""易单来 - 纸板厂诊断接口（基于易单来swaggerApi.json）"""

import allure
from test_case.page_api.public.base_api import BaseAPI

# 诊断模块使用独立域名 intelligenttest.onlinecps.cn，路径前缀为 /djintelligent/
ZHENDUAN_BASE_URL = "https://intelligenttest.onlinecps.cn"
PAPER_REPORT_PREFIX = "/djintelligent/DJEASYORDER/paper-report"


class ZhenduanAPI(BaseAPI):
    """易单来纸板厂诊断接口封装"""

    def __init__(self, base_url=None, headers=None, cookies=None):
        super().__init__(base_url=base_url or ZHENDUAN_BASE_URL, headers=headers, cookies=cookies)
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

    @allure.step("获取诊断报告列表")
    def get_page_list(self, pageNo, pageSize, startTime=None, endTime=None,
                      registeredPhone=None, companyName=None,
                      status_code=200, **kwargs):
        """获取诊断报告列表

        swagger 入参:
          必填: pageNo, pageSize
          可选: startTime(yyyy-MM-dd), endTime(yyyy-MM-dd),
                registeredPhone(注册手机号), companyName(企业名称)
        swagger 返参 data: {list, total}
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{PAPER_REPORT_PREFIX}/getPageList.do"
        payload = {"pageNo": pageNo, "pageSize": pageSize}
        if startTime is not None:
            payload["startTime"] = startTime
        if endTime is not None:
            payload["endTime"] = endTime
        if registeredPhone is not None:
            payload["registeredPhone"] = registeredPhone
        if companyName is not None:
            payload["companyName"] = companyName
        error_msg = kwargs.pop("error_msg", "获取诊断报告列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("企业基础画像")
    def get_company_base_profile(self, reportId, status_code=200, **kwargs):
        """企业基础画像

        swagger 入参:
          必填: reportId
        swagger 返参 data: 企业基础画像信息
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{PAPER_REPORT_PREFIX}/getCompanyBaseProfile.do"
        payload = {"reportId": reportId}
        error_msg = kwargs.pop("error_msg", "企业基础画像查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("核心诉求")
    def get_core_demand(self, reportId, status_code=200, **kwargs):
        """核心诉求

        swagger 入参:
          必填: reportId
        swagger 返参 data: 核心诉求信息
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{PAPER_REPORT_PREFIX}/getCoreDemand.do"
        payload = {"reportId": reportId}
        error_msg = kwargs.pop("error_msg", "核心诉求查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("市场洞察")
    def get_market_insight(self, reportId, status_code=200, **kwargs):
        """市场洞察

        swagger 入参:
          必填: reportId
        swagger 返参 data: 市场洞察信息
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{PAPER_REPORT_PREFIX}/getMarketInsight.do"
        payload = {"reportId": reportId}
        error_msg = kwargs.pop("error_msg", "市场洞察查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("业务机会")
    def get_business_opportunity(self, reportId, status_code=200, **kwargs):
        """业务机会

        swagger 入参:
          必填: reportId
        swagger 返参 data: 业务机会信息
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{PAPER_REPORT_PREFIX}/getBusinessOpportunity.do"
        payload = {"reportId": reportId}
        error_msg = kwargs.pop("error_msg", "业务机会查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("保存合作评估报告")
    def save_cooperation_evaluation_report(self, reportId, salesRadius=None,
                                           mainCoverage=None,
                                           mainPillarIndustry=None,
                                           cardboardFactoryCount=None,
                                           cartonFactoryCount=None,
                                           productionEquipmentCount=None,
                                           marketCompetitionDegree=None,
                                           currentMarketShare=None,
                                           cooperationModeList=None,
                                           budgetGoalItemList=None,
                                           cooperationAgreementSignTime=None,
                                           projectKickoffTime=None,
                                           systemImplementationTime=None,
                                           clearFields=None,
                                           status_code=200, **kwargs):
        """保存合作评估报告

        swagger 入参:
          必填: reportId
          可选: salesRadius(销售半径,公里,最多2位小数),
                mainCoverage(主要覆盖,最多200字),
                mainPillarIndustry(主要支柱产业),
                cardboardFactoryCount(纸板厂数量,正整数),
                cartonFactoryCount(纸箱厂数量,正整数),
                productionEquipmentCount(生产设备数量,正整数),
                marketCompetitionDegree(市场竞争程度: EXTREMELY_STRONG/STRONG/MEDIUM),
                currentMarketShare(当前市占率%,最多2位小数),
                cooperationModeList(合作模式集合,多选),
                budgetGoalItemList(目标预算集合,可多条),
                cooperationAgreementSignTime(合作协议签订时间,yyyy-MM-dd),
                projectKickoffTime(项目启动会时间,yyyy-MM-dd),
                systemImplementationTime(系统实施时间,yyyy-MM-dd),
                clearFields(需显式清空的字段名列表)
        swagger 返参 data: 保存结果
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{PAPER_REPORT_PREFIX}/saveCooperationEvaluationReport.do"
        payload = {"reportId": reportId}
        if salesRadius is not None:
            payload["salesRadius"] = salesRadius
        if mainCoverage is not None:
            payload["mainCoverage"] = mainCoverage
        if mainPillarIndustry is not None:
            payload["mainPillarIndustry"] = mainPillarIndustry
        if cardboardFactoryCount is not None:
            payload["cardboardFactoryCount"] = cardboardFactoryCount
        if cartonFactoryCount is not None:
            payload["cartonFactoryCount"] = cartonFactoryCount
        if productionEquipmentCount is not None:
            payload["productionEquipmentCount"] = productionEquipmentCount
        if marketCompetitionDegree is not None:
            payload["marketCompetitionDegree"] = marketCompetitionDegree
        if currentMarketShare is not None:
            payload["currentMarketShare"] = currentMarketShare
        if cooperationModeList is not None:
            payload["cooperationModeList"] = cooperationModeList
        if budgetGoalItemList is not None:
            payload["budgetGoalItemList"] = budgetGoalItemList
        if cooperationAgreementSignTime is not None:
            payload["cooperationAgreementSignTime"] = cooperationAgreementSignTime
        if projectKickoffTime is not None:
            payload["projectKickoffTime"] = projectKickoffTime
        if systemImplementationTime is not None:
            payload["systemImplementationTime"] = systemImplementationTime
        if clearFields is not None:
            payload["clearFields"] = clearFields
        error_msg = kwargs.pop("error_msg", "保存合作评估报告失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取分析报告详情")
    def get_reports_detail(self, reportId, status_code=200, **kwargs):
        """获取分析报告详情

        swagger 入参:
          必填: reportId
        swagger 返参 data: 分析报告详情信息
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{PAPER_REPORT_PREFIX}/getReportsDetail.do"
        payload = {"reportId": reportId}
        error_msg = kwargs.pop("error_msg", "获取分析报告详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
