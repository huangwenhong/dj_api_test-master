# -*- coding: utf-8 -*-
"""易单来 - 量价利模块-人工测算表接口（基于业财swaggerApi.json）"""

import allure
from test_case.page_api.public.base_api import BaseAPI

# APP 量价利接口网关路径
VPP_PREFIX = "/djsupplier/djfinancemanage/vpp"


class LiangbenliAPI(BaseAPI):
    """易单来量价利模块-人工测算表接口封装"""

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

    # ==================== 人工测算表 ====================

    @allure.step("人工测算表列表查询")
    def get_manual_calculate_page(self, pageNo=1, pageSize=10, date=None,
                                   keyword="", id=None, supplierId=None,
                                   paperType=None, paperCode=None,
                                   status_code=200, **kwargs):
        """人工测算表列表查询

        swagger 入参:
          必填: pageNo, pageSize, date
          可选: keyword, id, supplierId, paperType, paperCode
        swagger 返参 data.list: [{id, paperCode, paperType, gramWeight,
          unitPrice, marketPaperPrice, externalPaperPrice}]
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{VPP_PREFIX}/getManualCalculatePage"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "date": date,
        }
        if keyword:
            payload["keyword"] = keyword
        if id is not None:
            payload["id"] = id
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if paperType is not None:
            payload["paperType"] = paperType
        if paperCode is not None:
            payload["paperCode"] = paperCode
        error_msg = kwargs.pop("error_msg", "人工测算表列表查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("人工测算表编辑保存")
    def edit_manual_calculate(self, id=None, gramWeight=None, unitPrice=None,
                              marketPaperPrice=None, supplierId=None,
                              paperType=None, externalPaperPrice=None,
                              status_code=200, **kwargs):
        """人工测算表编辑保存

        swagger 入参:
          必填: id, gramWeight, unitPrice, marketPaperPrice
          可选: supplierId, paperType, externalPaperPrice
            externalPaperPrice 即"外部报价"字段（外部纸价）
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{VPP_PREFIX}/editManualCalculate"
        payload = {}
        if id is not None:
            payload["id"] = id
        if gramWeight is not None:
            payload["gramWeight"] = gramWeight
        if unitPrice is not None:
            payload["unitPrice"] = unitPrice
        if marketPaperPrice is not None:
            payload["marketPaperPrice"] = marketPaperPrice
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if paperType is not None:
            payload["paperType"] = paperType
        if externalPaperPrice is not None:
            payload["externalPaperPrice"] = externalPaperPrice
        error_msg = kwargs.pop("error_msg", "人工测算表编辑保存失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("人工测算表批量导入")
    def import_manual_calculate(self, file=None, supplierId=None, date=None,
                                 status_code=200, **kwargs):
        """人工测算表批量导入

        swagger 入参:
          query: supplierId, date
          formData: file (上传文件二进制)
        注: 此接口为 multipart/form-data，非 application/json
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{VPP_PREFIX}/importManualCalculate"
        params = {}
        if supplierId is not None:
            params["supplierId"] = supplierId
        if date is not None:
            params["date"] = date
        files = None
        if file is not None:
            files = {"file": file}
        error_msg = kwargs.pop("error_msg", "人工测算表批量导入失败")
        return self.post(url, params=params, files=files,
                         status_code=status_code, error_msg=error_msg)

    @allure.step("人工测算表导出")
    def export_manual_calculate(self, supplierId=None, date=None,
                                 paperType=None, paperCode=None,
                                 status_code=200, **kwargs):
        """人工测算表导出

        swagger 入参 (body):
          可选: supplierId, date, paperType, paperCode
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{VPP_PREFIX}/exportManualCalculate"
        payload = {}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if date is not None:
            payload["date"] = date
        if paperType is not None:
            payload["paperType"] = paperType
        if paperCode is not None:
            payload["paperCode"] = paperCode
        error_msg = kwargs.pop("error_msg", "人工测算表导出失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("下载人工测算表导入模板")
    def get_manual_calculate_template(self, supplierId=None, status_code=200, **kwargs):
        """下载人工测算表导入模板

        swagger 入参 (body):
          可选: supplierId
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{VPP_PREFIX}/getManualCalculateTemplate"
        payload = {}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        error_msg = kwargs.pop("error_msg", "下载人工测算表导入模板失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 产品量价利 ====================

    @allure.step("产品量价利汇总")
    def get_product_vpp_summary(self, startTime, endTime, supplierId,
                                dimension="order", dateType="day",
                                pageNo=1, pageSize=15,
                                sortField="sale_area", sortType="desc",
                                productTypeList=None, layerList=None, fluteTypeList=None,
                                status_code=200, **kwargs):
        """产品量价利汇总（getProductVppSummary.do），作战看板实时利润数据源

        返参 data: saleArea销售面积 / grossProfit毛利额 / netProfit净利额 等，均含value/mom
        """
        # Author: Author
        # Create Date: 2026-08-25
        # IsAI: True
        url = "/djsupplier/djfinancemanage/vpp/getProductVppSummary.do"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "productTypeList": productTypeList or [],
            "layerList": layerList or [],
            "fluteTypeList": fluteTypeList or [],
            "dimension": dimension,
            "dateType": dateType,
            "startTime": startTime,
            "endTime": endTime,
            "sortField": sortField,
            "sortType": sortType,
            "supplierId": supplierId,
        }
        error_msg = kwargs.pop("error_msg", "产品量价利汇总查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产品量价利分页")
    def get_product_vpp_page(self, startTime, endTime, supplierId,
                             dimension="order", dateType="day", priceType="stock_price",
                             pageNo=1, pageSize=15,
                             sortField="sale_area", sortType="desc",
                             listDimension="product_name",
                             productTypeList=None, layerList=None, fluteTypeList=None,
                             productName="", materialCode="", orderSource="",
                             productProfitList=None, productLossList=None,
                             status_code=200, **kwargs):
        """产品量价利分页（getProductVppPage.do），作战看板产品牌价/单位毛利/毛利额数据源

        返参 data: total / list各产品数据
        每产品: productName/materialCode/salePrice牌价/unitGrossProfit单位毛利/
               grossProfit毛利额/saleArea/customerCount等
        """
        # Author: Author
        # Create Date: 2026-08-28
        # IsAI: True
        url = "/djsupplier/djfinancemanage/vpp/getProductVppPage.do"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
            "productTypeList": productTypeList or [],
            "layerList": layerList or [],
            "fluteTypeList": fluteTypeList or [],
            "productName": productName,
            "materialCode": materialCode,
            "orderSource": orderSource,
            "dimension": dimension,
            "priceType": priceType,
            "dateType": dateType,
            "startTime": startTime,
            "endTime": endTime,
            "sortField": sortField,
            "sortType": sortType,
            "supplierId": supplierId,
            "productProfitList": productProfitList,
            "productLossList": productLossList,
            "listDimension": listDimension,
        }
        error_msg = kwargs.pop("error_msg", "产品量价利分页查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("产品量价利-纸层代码")
    def get_paper_layer_codes(self, materialCode, supplierId, status_code=200, **kwargs):
        """纸层代码（vpp/getPaperLayerCodes.do），供产品画像 paperCodeList 入参

        返参 data: 纸层字符数组（如 ["C","H","9","W","8"]）
        """
        # Author: Author
        # Create Date: 2026-08-31
        # IsAI: True
        url = "/djsupplier/djfinancemanage/vpp/getPaperLayerCodes.do"
        payload = {"materialCode": materialCode, "supplierId": supplierId}
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg="获取纸层代码失败")

    @allure.step("产品量价利-产品画像")
    def get_product_portrait(self, materialCode, productName, startTime, endTime, supplierId,
                             paperCodeList=None, dimension="order", dateType="day", priceType="",
                             layerFluteType=None, status_code=200, **kwargs):
        """产品画像/详情（vpp/getProductPortrait.do），成本分析/销售趋势交叉校验源

        返参 data: couponPrice券后单价/unitContributionMargin单位边际贡献/grossProfit单位毛利/
                  saleArea销售面积 等(均含value/mom)，及 saleAreaAndPriceTrend{saleArea[],price[]}
        """
        # Author: Author
        # Create Date: 2026-08-31
        # IsAI: True
        url = "/djsupplier/djfinancemanage/vpp/getProductPortrait.do"
        payload = {
            "dimension": dimension,
            "priceType": priceType,
            "dateType": dateType,
            "startTime": startTime,
            "endTime": endTime,
            "supplierId": supplierId,
            "materialCode": materialCode,
            "layerFluteType": layerFluteType,
            "productName": productName,
            "paperCodeList": paperCodeList or [],
        }
        error_msg = kwargs.pop("error_msg", "产品量价利画像查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
