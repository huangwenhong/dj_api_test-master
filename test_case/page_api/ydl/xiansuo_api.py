# -*- coding: utf-8 -*-
"""易单来 - 线索管理相关接口（基于抓包数据生成）"""

import allure
from test_case.page_api.public.base_api import BaseAPI

CLUE_PREFIX = "/djsupplier/DJEASYORDER/clue"
ADDRESS_PREFIX = "/djsupplier/DJEASYORDER/address"
FIELD_CONFIG_PREFIX = "/djsupplier/DJEASYORDER/fieldconfig"
FILE_PREFIX = "/djsupplier/DJEASYORDER/file"


class XiansuoAPI(BaseAPI):
    """易单来线索管理接口封装"""

    def __init__(self, base_url=None, headers=None, cookies=None):
        super().__init__(base_url, headers, cookies)
        biz_headers = {
            "device": "web",
            "source": "easy_order",
            "version": "2.3.5",
            "Content-Type": "application/json",
        }
        self.headers.update(biz_headers)

    # ==================== 线索基础操作 ====================

    @allure.step("查询线索列表")
    def get_clue_list(self, clueType="1", pageNo=1, pageSize=15, orgId="400", sort="1", status_code=200, **kwargs):
        """查询线索列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getClueList.do"
        payload = {
            "clueType": clueType, "pageNo": pageNo, "pageSize": pageSize,
            "orgId": orgId, "sort": sort,
        }
        error_msg = kwargs.pop("error_msg", "查询线索列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("查看线索基本信息")
    def get_clue_base_info(self, clueId, status_code=200, **kwargs):
        """根据线索编号查看线索基本信息（详情）"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getClueBaseInfo.do"
        payload = {"clueId": clueId}
        error_msg = kwargs.pop("error_msg", "查看线索基本信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("新增线索基本信息")
    def add_clue_base_info(self, customerName, contactWay, addressInfo=None, status_code=200, **kwargs):
        """新增线索基本信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/addBaseInfo.do"
        if addressInfo is None:
            addressInfo = {
                "customerAddress": "浙江省温州市瓯海区梧田街道",
                "provinceCode": "33", "cityCode": "3303",
                "areaCode": "330302", "streetCode": "330302028",
                "detailAddress": "浙江省温州市瓯海区梧田街道",
                "longitudeAndLatitude": [120.670051, 27.988146],
            }
        payload = {
            "gender": kwargs.pop("gender", ""),
            "customerAge": kwargs.pop("customerAge", "1"),
            "dateOfBirth": kwargs.pop("dateOfBirth", ""),
            "education": kwargs.pop("education", 0),
            "address": kwargs.pop("address", "浙江省温州市瓯海区梧田街道"),
            "location": kwargs.pop("location", [120.670051, 27.988146]),
            "authenticationType": kwargs.pop("authenticationType", "personal"),
            "authenticationImg": kwargs.pop("authenticationImg", []),
            "contractImg": kwargs.pop("contractImg", []),
            "customerAbbreviations": kwargs.pop("customerAbbreviations", ""),
            "dutyManId": kwargs.pop("dutyManId", ""),
            "placeOrigin": kwargs.pop("placeOrigin", {
                "provinceCode": 11, "cityCode": 1101, "areaCode": 110101,
                "provinceName": "北京市", "cityName": "北京市", "areaName": "东城区",
            }),
            "placeOriginCodes": kwargs.pop("placeOriginCodes", ["11", "1101", "110101"]),
            "customerAreas": kwargs.pop("customerAreas", ["33", "3303", "330302", "330302028"]),
            "addressInfo": addressInfo,
            "customerNo": kwargs.pop("customerNo", ""),
            "monthRequirementMoney": kwargs.pop("monthRequirementMoney", ""),
            "monthRequirementArea": kwargs.pop("monthRequirementArea", ""),
            "customerName": customerName,
            "mainContactManName": kwargs.pop("mainContactManName", customerName),
            "contactWay": contactWay,
            "moreContacts": kwargs.pop("moreContacts", []),
            "merchandiserInfo": kwargs.pop("merchandiserInfo", {"id": ""}),
        }
        error_msg = kwargs.pop("error_msg", "新增线索基本信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("修改线索基本信息")
    def update_clue_base_info(self, clueId, baseInfo, status_code=200, **kwargs):
        """修改线索基本信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/updateClueBaseInfo.do"
        payload = {"id": clueId, "baseInfo": baseInfo}
        error_msg = kwargs.pop("error_msg", "修改线索基本信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("修改线索标签")
    def update_clue_label(self, clueId, followStatus="", runStatus=2, customerAttribute=1, status_code=200, **kwargs):
        """修改线索的跟进状态、经营状态、客户属性等标签"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/updateClueLabel.do"
        payload = {"clueId": clueId, "followStatus": followStatus, "runStatus": runStatus, "customerAttribute": customerAttribute}
        error_msg = kwargs.pop("error_msg", "修改线索标签失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("转移线索")
    def transfer_clue(self, clueList, dutyManId, status_code=200, **kwargs):
        """转移线索给指定负责人"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/transferClue.do"
        payload = {"clueList": clueList, "dutyManId": dutyManId}
        error_msg = kwargs.pop("error_msg", "转移线索失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取线索信息完整度")
    def get_clue_info_percent(self, clueId, status_code=200, **kwargs):
        """获取线索信息完整度百分比"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getClueInfoPercent.do"
        payload = {"clueId": clueId}
        error_msg = kwargs.pop("error_msg", "获取线索信息完整度失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 线索辅助数据 ====================

    @allure.step("获取当前用户组织列表")
    def get_current_user_org_list(self, status_code=200, **kwargs):
        """获取当前用户所在的组织列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getCurrentUserOrgListNoAuth.do"
        payload = {}
        error_msg = kwargs.pop("error_msg", "获取当前用户组织列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取创建人列表")
    def get_creator_list(self, orgId="", clueType="1", status_code=200, **kwargs):
        """获取线索的创建人列表（筛选）"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getCreatorList.do"
        payload = {"orgId": orgId, "clueType": clueType}
        error_msg = kwargs.pop("error_msg", "获取创建人列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取线索绑定的负责人列表")
    def get_clue_binding_duty_list(self, orgId="", clueType="1", status_code=200, **kwargs):
        """获取线索绑定的负责人列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getClueBindingDutyList.do"
        payload = {"orgId": orgId, "clueType": clueType}
        error_msg = kwargs.pop("error_msg", "获取线索绑定的负责人列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取组织下负责人列表")
    def get_duty_man_list_by_org_id(self, orgId="", clueType="1", status_code=200, **kwargs):
        """获取某个组织下负责线索的负责人列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getDutyManListByOrgId.do"
        payload = {"orgId": orgId, "clueType": clueType}
        error_msg = kwargs.pop("error_msg", "获取组织下负责人列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取全国省份")
    def get_all_province(self, status_code=200, **kwargs):
        """查询全国省份列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getAllProvince.do"
        payload = {}
        error_msg = kwargs.pop("error_msg", "获取全国省份失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取城市列表")
    def get_all_city(self, code, status_code=200, **kwargs):
        """通过省份code获取城市列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getAllCity.do"
        payload = {"code": code}
        error_msg = kwargs.pop("error_msg", "获取城市列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取区县列表")
    def get_all_area(self, code, status_code=200, **kwargs):
        """根据城市code获取区县列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getAllArea.do"
        payload = {"code": code}
        error_msg = kwargs.pop("error_msg", "获取区县列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取街道列表")
    def get_all_street(self, code, status_code=200, **kwargs):
        """根据区县code获取街道列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getAllStreet.do"
        payload = {"code": code}
        error_msg = kwargs.pop("error_msg", "获取街道列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取省下所有市区")
    def get_city_area_for_clue(self, provinceCode, status_code=200, **kwargs):
        """根据省份code获取省下所有市区及区县"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True
        url = f"{ADDRESS_PREFIX}/getCityAreaForClue.do"
        payload = {"provinceCode": provinceCode}
        error_msg = kwargs.pop("error_msg", "获取省下所有市区失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取层数和楞型列表")
    def get_layer_list(self, status_code=200, **kwargs):
        """获取层数和楞型列表（由产品服务提供）"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getLayerList.do"
        payload = {}
        error_msg = kwargs.pop("error_msg", "获取层数和楞型列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取纸板供应商列表")
    def get_paperboard_supplier_list(self, status_code=200, **kwargs):
        """获取纸板供应商列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getPaperboardSupplierList"
        payload = {}
        error_msg = kwargs.pop("error_msg", "获取纸板供应商列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取竞对企业列表")
    def get_rival_archive_list(self, clueId, status_code=200, **kwargs):
        """获取线索的竞对企业列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getRivalArchiveList.do"
        payload = {"clueId": clueId}
        error_msg = kwargs.pop("error_msg", "获取竞对企业列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 线索产品信息 ====================

    @allure.step("查询线索产品列表")
    def get_clue_product_info_list(self, clueId, productType="0", status_code=200, **kwargs):
        """查询线索的产品信息列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getClueProductInfoList.do"
        payload = {"clueId": clueId, "productType": productType}
        error_msg = kwargs.pop("error_msg", "查询线索产品列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("查询某个产品详情")
    def get_clue_product_info_by_id(self, productId, status_code=200, **kwargs):
        """查看某个产品的详细信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getClueProductInfoById.do"
        payload = {"productId": productId}
        error_msg = kwargs.pop("error_msg", "查询产品详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("新增线索产品信息")
    def add_product_info(self, clueId, product, status_code=200, **kwargs):
        """新增线索的产品信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/addProductInfo.do"
        payload = {"id": clueId, "product": product}
        error_msg = kwargs.pop("error_msg", "新增线索产品信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("编辑线索产品信息")
    def update_product_info(self, productId, clueId, product, status_code=200, **kwargs):
        """编辑线索的产品信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/updateProductInfo.do"
        payload = {"productId": productId, "clueId": clueId, **product}
        error_msg = kwargs.pop("error_msg", "编辑线索产品信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("删除线索产品")
    def del_clue_product(self, productId, infoId, status_code=200, **kwargs):
        """删除线索下的产品"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/delClueProduct.do"
        payload = {"productId": productId, "infoId": infoId}
        error_msg = kwargs.pop("error_msg", "删除线索产品失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取区域上月均价")
    def get_area_price_last_month(self, rivalProductId, status_code=200, **kwargs):
        """获取区域上月平均价格"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getAreaPriceLastMonth.do"
        payload = {"rivalProductId": rivalProductId}
        error_msg = kwargs.pop("error_msg", "获取区域上月均价失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("查询线索需求信息")
    def get_demand_info(self, clueId, status_code=200, **kwargs):
        """查询线索需求信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getDemandInfo.do"
        payload = {"clueId": clueId}
        error_msg = kwargs.pop("error_msg", "查询线索需求信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("修改线索需求信息")
    def update_demand_info(self, clueId, status_code=200, **kwargs):
        """修改线索需求信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/updateDemandInfo.do"
        payload = {"clueId": clueId}
        error_msg = kwargs.pop("error_msg", "修改线索需求信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 线索物流信息 ====================

    @allure.step("获取线索物流信息")
    def get_clue_logistics_info(self, clueId, status_code=200, **kwargs):
        """获取线索物流信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getClueLogisticsInfo.do"
        payload = {"clueId": clueId}
        error_msg = kwargs.pop("error_msg", "获取线索物流信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("修改线索物流信息")
    def update_clue_logistics_info(self, clueId, logisticsModel, status_code=200, **kwargs):
        """修改线索物流信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/updateClueLogisticsInfo.do"
        payload = {"id": clueId, "logisticsModel": logisticsModel}
        error_msg = kwargs.pop("error_msg", "修改线索物流信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取车辆配置列表")
    def get_car_configure_list(self, status_code=200, **kwargs):
        """获取所有车辆配置列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getCarConfigureList.do"
        payload = {}
        error_msg = kwargs.pop("error_msg", "获取车辆配置列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取固定休息日列表")
    def get_regular_rest_day_list(self, status_code=200, **kwargs):
        """获取固定休息日配置"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getRegularRestDayList.do"
        payload = {}
        error_msg = kwargs.pop("error_msg", "获取固定休息日列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("更新固定休息日")
    def update_regular_rest_day(self, monthRestArray=None, weekRestArray=None, status_code=200, **kwargs):
        """更新固定休息日配置"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/updateRegularRestDay.do"
        payload = {"monthRestArray": monthRestArray or [], "weekRestArray": weekRestArray or []}
        error_msg = kwargs.pop("error_msg", "更新固定休息日失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取休息日列表")
    def get_rest_day_list(self, regularRestId, yearMonth, status_code=200, **kwargs):
        """获取指定月份的休息日列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getRestDayList.do"
        payload = {"regularRestId": regularRestId, "yearMonth": yearMonth}
        error_msg = kwargs.pop("error_msg", "获取休息日列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("更新休息日")
    def update_rest_day(self, regularRestId, yearMonth, restDayArray=None, status_code=200, **kwargs):
        """更新指定月份的休息日"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/updateRestDay.do"
        payload = {"regularRestId": regularRestId, "yearMonth": yearMonth, "restDayArray": restDayArray or []}
        error_msg = kwargs.pop("error_msg", "更新休息日失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 线索其它信息 ====================

    @allure.step("查看线索其它信息")
    def get_clue_other_info(self, clueId, status_code=200, **kwargs):
        """查看线索其它信息（淡旺季、预付、习惯等）"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getClueOtherInfo.do"
        payload = {"clueId": clueId}
        error_msg = kwargs.pop("error_msg", "查看线索其它信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("编辑线索其它信息")
    def update_clue_other_info(self, clueId, otherInfoModel, status_code=200, **kwargs):
        """编辑线索其它信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/updateClueOtherInfo.do"
        payload = {"id": clueId, "otherInfoModel": otherInfoModel}
        error_msg = kwargs.pop("error_msg", "编辑线索其它信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取线索操作日志")
    def get_operate_log_list(self, clueId, pageNo=1, pageSize=10, status_code=200, **kwargs):
        """获取指定线索的操作日志"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getOperateLogListByClueId.do"
        payload = {"clueId": clueId, "id": clueId, "pageNo": pageNo, "pageSize": pageSize}
        error_msg = kwargs.pop("error_msg", "获取线索操作日志失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 线索合作纸板厂 ====================

    @allure.step("查看线索合作纸板厂")
    def get_clue_cooperative_cardboard_factory(self, clueId, status_code=200, **kwargs):
        """查看线索的合作纸板厂信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getClueCooperativeCardboardFactory.do"
        payload = {"clueId": clueId}
        error_msg = kwargs.pop("error_msg", "查看线索合作纸板厂失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("新增合作纸板厂")
    def add_cooperative_cardboard_factory(self, infoId, factoryList, status_code=200, **kwargs):
        """新增线索的合作纸板厂"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/addCooperativeCardboardFactory.do"
        payload = {"infoId": infoId, "factoryList": factoryList}
        error_msg = kwargs.pop("error_msg", "新增合作纸板厂失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("修改合作纸板厂")
    def update_cooperative_cardboard_factory(self, factoryInfo, status_code=200, **kwargs):
        """修改线索的合作纸板厂"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/updateCooperativeCardboardFactory.do"
        payload = dict(factoryInfo)
        error_msg = kwargs.pop("error_msg", "修改合作纸板厂失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("删除合作纸板厂")
    def del_cooperative_cardboard_factory(self, id, status_code=200, **kwargs):
        """删除线索的合作纸板厂"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/delCooperativeCardboardFactory.do"
        payload = {"id": id}
        error_msg = kwargs.pop("error_msg", "删除合作纸板厂失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 线索设备信息 ====================

    @allure.step("查询线索设备信息")
    def get_device_by_clue(self, infoId, status_code=200, **kwargs):
        """查询线索的设备信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/device/getByClue.do"
        payload = {"infoId": infoId}
        error_msg = kwargs.pop("error_msg", "查询线索设备信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("查询选择设备信息")
    def get_choice_device(self, deviceType="1", pageNo=1, pageSize=15, status_code=200, **kwargs):
        """查询可选设备信息列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/device/getChoiceDevice.do"
        payload = {"deviceType": deviceType, "pageNo": pageNo, "pageSize": pageSize}
        error_msg = kwargs.pop("error_msg", "查询选择设备信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("新增线索设备信息")
    def add_device(self, infoId, deviceInfo, status_code=200, **kwargs):
        """新增线索设备信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/device/add.do"
        payload = {"infoId": infoId, **deviceInfo}
        error_msg = kwargs.pop("error_msg", "新增线索设备信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("修改线索设备信息")
    def update_device(self, deviceInfo, status_code=200, **kwargs):
        """修改线索设备信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/device/update.do"
        payload = dict(deviceInfo)
        error_msg = kwargs.pop("error_msg", "修改线索设备信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("删除线索设备信息")
    def del_device(self, printId=None, status_code=200, **kwargs):
        """删除线索设备信息（印刷机传printId, 模切机传dieCutId, 粘箱机传gluingMachineId, 钉箱机传nailBoxId, 打包机传packId）"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/device/del.do"
        error_msg = kwargs.pop("error_msg", "删除线索设备信息失败")
        payload = {}
        if printId is not None:
            payload["printId"] = printId
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 线索辅料信息 ====================

    @allure.step("获取线索辅料信息")
    def get_accessories_by_clue(self, infoId, status_code=200, **kwargs):
        """获取线索辅料信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/accessories/getByClue.do"
        payload = {"infoId": infoId}
        error_msg = kwargs.pop("error_msg", "获取线索辅料信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("新增线索辅料信息")
    def add_accessories(self, infoId, accessories, status_code=200, **kwargs):
        """新增线索辅料信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/accessories/add.do"
        payload = {"id": infoId, "accessories": accessories}
        error_msg = kwargs.pop("error_msg", "新增线索辅料信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("修改线索辅料信息")
    def update_accessories(self, accessoriesId, accessories, status_code=200, **kwargs):
        """修改线索辅料信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/accessories/update.do"
        payload = {"id": accessoriesId, **accessories}
        error_msg = kwargs.pop("error_msg", "修改线索辅料信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("删除线索辅料信息")
    def del_accessories(self, accessoriesId, status_code=200, **kwargs):
        """删除线索辅料信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/accessories/del.do"
        payload = {"id": accessoriesId}
        error_msg = kwargs.pop("error_msg", "删除线索辅料信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 终端产品信息 ====================

    @allure.step("查询终端产品列表")
    def get_terminal_list(self, infoId, status_code=200, **kwargs):
        """查询线索的终端产品列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/terminal/getList.do"
        payload = {"infoId": infoId}
        error_msg = kwargs.pop("error_msg", "查询终端产品列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("查询终端产品详情")
    def get_terminal_detail(self, terminalId, status_code=200, **kwargs):
        """查询终端产品详情"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/terminal/getDetail.do"
        payload = {"id": terminalId}
        error_msg = kwargs.pop("error_msg", "查询终端产品详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("新增终端产品信息")
    def add_terminal(self, infoId, terminalInfo, status_code=200, **kwargs):
        """新增线索终端产品信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/terminal/add.do"
        payload = {"infoId": infoId, **terminalInfo}
        error_msg = kwargs.pop("error_msg", "新增终端产品信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("修改终端产品信息")
    def update_terminal(self, terminalInfo, status_code=200, **kwargs):
        """修改终端产品信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/terminal/update.do"
        payload = dict(terminalInfo)
        error_msg = kwargs.pop("error_msg", "修改终端产品信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("删除终端产品信息")
    def del_terminal(self, terminalId, status_code=200, **kwargs):
        """删除终端产品信息"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/terminal/delete.do"
        payload = {"id": terminalId}
        error_msg = kwargs.pop("error_msg", "删除终端产品信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 线索删除 ====================

    @allure.step("删除线索")
    def del_clues(self, clueList, status_code=200, **kwargs):
        """批量删除线索"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/delClues.do"
        payload = {"clueList": clueList}
        error_msg = kwargs.pop("error_msg", "删除线索失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("恢复线索")
    def recover_clues(self, clueList, status_code=200, **kwargs):
        """从回收站恢复已删除的线索"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/recoverClues.do"
        payload = {"clueList": clueList}
        error_msg = kwargs.pop("error_msg", "恢复线索失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 线索转化 ====================

    @allure.step("同步/转化线索")
    def sync_clue(self, clueList, syncType="1", status_code=200, **kwargs):
        """同步/转化线索（线索转客户）"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/syncClue.do"
        payload = {"clueList": clueList, "syncType": syncType}
        error_msg = kwargs.pop("error_msg", "同步转化线索失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 线索导入导出 ====================

    @allure.step("导入线索Excel")
    def import_clue_excel(self, fileIds, clueSourceType="1", status_code=200, **kwargs):
        """导入线索Excel文件"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/importClueExcel.do"
        payload = {"clueSourceType": clueSourceType, "fileIds": fileIds}
        error_msg = kwargs.pop("error_msg", "导入线索Excel失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("查看导入记录列表")
    def get_import_record_list(self, status_code=200, **kwargs):
        """查看线索导入记录列表"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getImportRecordList.do"
        payload = {}
        error_msg = kwargs.pop("error_msg", "查看导入记录列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("下载导入错误报告")
    def download_error_report(self, recordId, status_code=200, **kwargs):
        """下载线索导入错误报告（返回文件流）"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/downloadErrorReport.do"
        payload = {"id": recordId}
        error_msg = kwargs.pop("error_msg", "下载导入错误报告失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg, return_response=True)

    @allure.step("导出线索列表Excel")
    def export_selected_clue_list(self, orgId="400", clueType="1", status_code=200, **kwargs):
        """导出选中线索列表为Excel（返回文件流）"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/exportSelectedClueList.do"
        payload = {
            "searchTime": [], "dutyManId": "", "creatorId": "",
            "orgId": orgId, "sort": "1", "selected": [],
            "runStatus": "2", "followStatus": "1,3,4",
            "customerAttributeList": [1, 2, 3, 8, 9, 5, 4],
            "clueType": clueType, "clueIds": [],
        }
        error_msg = kwargs.pop("error_msg", "导出线索列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg, return_response=True)

    # ==================== 线索首页补充接口 ====================

    @allure.step("更新线索经营状态")
    def update_clue_run_status(self, clueId, runStatus, status_code=200, **kwargs):
        """修改线索经营状态（1:存续 2:在业 3:注销 4:迁入 5:签出 6:停业）"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/updateClueRunStatus.do"
        payload = {"clueId": clueId, "runStatus": runStatus}
        error_msg = kwargs.pop("error_msg", "更新线索经营状态失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("更新跟进状态")
    def update_follow_status(self, clueId, followStatus, status_code=200, **kwargs):
        """修改跟进状态（1:未处理 2:无效信息 3:无转化机会 4:有转换机会）"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/updateFollowStatus.do"
        payload = {"clueId": clueId, "followStatus": followStatus}
        error_msg = kwargs.pop("error_msg", "更新跟进状态失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取街道信息")
    def get_street_info(self, streetCode, status_code=200, **kwargs):
        """根据街道code获取街道详情"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getStreetInfo.do"
        payload = {"streetCode": streetCode}
        error_msg = kwargs.pop("error_msg", "获取街道信息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("下载线索导入模板")
    def download_clue_template(self, status_code=200, **kwargs):
        """下载线索导入模板（GET请求，返回文件流）"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/downloadClueTemplate.do"
        error_msg = kwargs.pop("error_msg", "下载线索导入模板失败")
        return self.get(url, status_code=status_code, error_msg=error_msg, return_response=True)

    @allure.step("校验手机号是否被线索占用")
    def check_clue_phone_occupy(self, phone, status_code=200, **kwargs):
        """校验手机号码是否被线索占用"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/checkCluePhoneOccupy.do"
        payload = {"phone": phone}
        error_msg = kwargs.pop("error_msg", "校验手机号占用失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("查看同步失败明细")
    def get_sync_fail_details(self, errorReportId, pageNo=1, pageSize=15, status_code=200, **kwargs):
        """查看同步失败明细（按错误批次编号查询）"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True
        url = f"{CLUE_PREFIX}/getSyncFailDetails.do"
        payload = {"errorReportId": errorReportId, "pageNo": pageNo, "pageSize": pageSize}
        error_msg = kwargs.pop("error_msg", "查看同步失败明细失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取用户隐藏字段配置")
    def get_user_hide_field(self, status_code=200, **kwargs):
        """获取用户隐藏字段配置"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        url = f"{FIELD_CONFIG_PREFIX}/getUserHideField.do"
        error_msg = kwargs.pop("error_msg", "获取用户隐藏字段配置失败")
        return self.post(url, json="", status_code=status_code, error_msg=error_msg, **kwargs)

    @allure.step("上传Excel文件")
    def upload_excel(self, file_path, status_code=200, **kwargs):
        """上传Excel文件，返回文件记录（含fileId等）"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True
        import os
        from curl_cffi.curl import CurlMime
        from curl_cffi import requests as cffi_requests
        url = self.build_url(f"{FILE_PREFIX}/uploadExcelNoAuth.do")
        file_name = os.path.basename(file_path)
        mime = CurlMime()
        mime.addpart(
            name="file",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=file_name,
            local_path=file_path,
        )
        # 复用当前 session cookies 保持登录态，但单独构造请求避免 Content-Type 冲突
        self.get_base_request()  # 确保 cookies 已同步最新 token
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
            "device": "web",
            "source": "easy_order",
            "version": "2.3.5",
        }
        error_msg = kwargs.pop("error_msg", "上传Excel文件失败")
        response = cffi_requests.request(
            "POST", url, multipart=mime, headers=headers,
            cookies=self.cookies, timeout=self.timeout,
            impersonate="chrome", verify=False,
        )
        message = error_msg
        if status_code != 0:
            assert response.status_code == status_code, (
                f"{message},接口<{url}>报错-{response.status_code},"
                f"reason:{response.reason},text:{response.text}"
            )
        return response.json()

