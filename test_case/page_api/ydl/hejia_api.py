# -*- coding: utf-8 -*-
"""易单来 - 核价工具接口（基于业财swaggerApi.json）"""

import allure
from urllib.parse import urlparse
from test_case.page_api.public.base_api import BaseAPI

# APP 核价接口网关路径
HEJIA_APP_PREFIX = "/djsupplier/app/djfinancemanage/app/pricing"
HEJIA_APP_APPROVAL_PREFIX = "/djsupplier/app/djfinancemanage/app/pricing/approval"
HEJIA_CONFIG_PREFIX = "/djsupplier/djfinancemanage/pricing/config"
HEJIA_APPROVAL_PREFIX = "/djsupplier/djfinancemanage/pricing/approval"
# 联合供应商
HEJIA_UNION_PREFIX = "/djsupplier/djfinancemanage/union"


class HejiaAPI(BaseAPI):
    """易单来核价工具接口封装（APP 端 + 供应端）"""

    # 直连业财服务时的路径映射：APP 端审批查询接口在后端合并到供应端审批控制器
    _DIRECT_PATH_MAP = {
        "/djsupplier/app/djfinancemanage/app/pricing/getApprovalList": "/djfinancemanage/pricing/approval/getList",
        "/djsupplier/app/djfinancemanage/app/pricing/getApprovalDetail": "/djfinancemanage/pricing/approval/getDetail",
    }

    def __init__(self, base_url=None, headers=None, cookies=None):
        super().__init__(base_url, headers, cookies)
        # 后端 IP 直连业财服务时不经过 /djsupplier 网关，需剥离网关前缀
        host = urlparse(self.base_url).hostname or ""
        self.direct_service = bool(host) and host.replace(".", "").isdigit()
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

    def build_url(self, path_or_url):
        """直连业财服务时剥离 /djsupplier[/app] 网关前缀，保留 djfinancemanage 上下文路径。"""
        path = str(path_or_url)
        if self.direct_service:
            if path in self._DIRECT_PATH_MAP:
                return super().build_url(self._DIRECT_PATH_MAP[path])
            if path.startswith("/djsupplier"):
                idx = path.find("/djfinancemanage/")
                if idx >= 0:
                    path = path[idx:]
        return super().build_url(path)

    # ==================== 链路 1：APP 端核价提交 ====================

    @allure.step("材料代码解析预览")
    def parse_material_code(self, materialCode, supplierId=None,
                            status_code=200, **kwargs):
        """材料代码解析预览（APP 端）

        swagger 入参:
          必填: materialCode
          可选: supplierId
        swagger 返参 data: {layers, layerInfoList, fluteTypeList}
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_PREFIX}/parseMaterialCode"
        payload = {"materialCode": materialCode}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        error_msg = kwargs.pop("error_msg", "材料代码解析预览失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取核价基础配置")
    def get_config(self, supplierId=None, status_code=200, **kwargs):
        """获取核价基础配置（APP 端）

        swagger 入参:
          可选: supplierId
        swagger 返参 data: {utilizationRate, paperPriceSource, freightVisible,
          freightDefault, rebateVisible, rebateDefault, discountVisible,
          discountDefaultMode, discountPercentValue, discountFixedValue,
          needApproval, allowPriceAdjust, adjustSpace, processingFeeEditable,
          processingFees, rolePrices}
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_PREFIX}/getConfig"
        payload = {}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        error_msg = kwargs.pop("error_msg", "获取核价基础配置失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("核价计算")
    def calculate(self, materialCode, fluteType, processingFee=None, freight=None,
                  rebate=None, discount=None, discountMode=None,
                  status_code=200, **kwargs):
        """核价计算（APP 端）

        swagger 入参:
          必填: materialCode, fluteType
          可选: processingFee, freight, rebate(0-1), discount, discountMode
        swagger 返参 data: {recordId, breakdown{eachLayerCost, paperCostSum,
          paperCostWithUtil, processingFee, freight, subtotal, rebateAmount,
          discountAmount}, basePrice, listPrice, fixedPrice, finalPrice,
          hasRebate, rebate, discount, discountMode}
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_PREFIX}/calculate"
        payload = {
            "materialCode": materialCode,
            "fluteType": fluteType,
        }
        if processingFee is not None:
            payload["processingFee"] = processingFee
        if freight is not None:
            payload["freight"] = freight
        if rebate is not None:
            payload["rebate"] = rebate
        if discount is not None:
            payload["discount"] = discount
        if discountMode is not None:
            payload["discountMode"] = discountMode
        error_msg = kwargs.pop("error_msg", "核价计算失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("提交审批")
    def submit_approval(self, recordId=None, infoId=None, orderQuantity=None,
                        remark=None, submitPrice=None,
                        status_code=200, **kwargs):
        """提交审批（APP 端）

        swagger 入参 (body):
          可选: recordId, infoId, orderQuantity, remark, submitPrice
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_PREFIX}/submitApproval"
        payload = {}
        if recordId is not None:
            payload["recordId"] = recordId
        if infoId is not None:
            payload["infoId"] = infoId
        if orderQuantity is not None:
            payload["orderQuantity"] = orderQuantity
        if remark is not None:
            payload["remark"] = remark
        if submitPrice is not None:
            payload["submitPrice"] = submitPrice
        error_msg = kwargs.pop("error_msg", "提交审批失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("客户/线索选择")
    def search_customer(self, keyword=None, pageNo=1, pageSize=10,
                        status_code=200, **kwargs):
        """客户/线索选择（APP 端）

        swagger 入参:
          可选: keyword
        后端实际必填: pageNo, pageSize
        swagger 返参 data: array<object>
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_PREFIX}/searchCustomer"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        if keyword:
            payload["keyword"] = keyword
        error_msg = kwargs.pop("error_msg", "客户/线索选择失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 链路 2：APP 端审批操作 ====================

    @allure.step("审批列表(APP)")
    def get_approval_list_app(self, status=None, pageNo=1, pageSize=10,
                              status_code=200, **kwargs):
        """审批列表(APP)

        swagger 入参:
          可选: status(pending/approved/rejected/cancel/空=全部), pageNo, pageSize
        swagger 返参 data: array<object>
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_PREFIX}/getApprovalList"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        if status:
            payload["status"] = status
        error_msg = kwargs.pop("error_msg", "获取 APP 端审批列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("审批详情(APP)")
    def get_approval_detail_app(self, id, status_code=200, **kwargs):
        """审批详情(APP)

        swagger 入参:
          必填: id
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_PREFIX}/getApprovalDetail"
        payload = {"id": id}
        error_msg = kwargs.pop("error_msg", "获取 APP 端审批详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("审批通过")
    def approval_approve(self, approvalId, comment=None, afterPrice=None,
                         status_code=200, **kwargs):
        """审批通过

        swagger 入参:
          必填: approvalId
          可选: comment, afterPrice
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_APPROVAL_PREFIX}/approve"
        payload = {"approvalId": approvalId}
        if comment is not None:
            payload["comment"] = comment
        if afterPrice is not None:
            payload["afterPrice"] = afterPrice
        error_msg = kwargs.pop("error_msg", "审批通过失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("审批驳回")
    def approval_reject(self, approvalId, rejectReason=None,
                        status_code=200, **kwargs):
        """审批驳回

        swagger 入参:
          必填: approvalId
          可选: rejectReason
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_APPROVAL_PREFIX}/reject"
        payload = {"approvalId": approvalId}
        if rejectReason is not None:
            payload["rejectReason"] = rejectReason
        error_msg = kwargs.pop("error_msg", "审批驳回失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("撤回审批")
    def approval_cancel(self, recordId=None, approvalId=None, revokeReason=None,
                        status_code=200, **kwargs):
        """撤回审批

        swagger 入参:
          必填: approvalId
          可选: revokeReason
        后端实际: 直连业财服务按 recordId(核价记录id) 撤回，传 approvalId 会被判为“核价记录id不能为空”
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_APPROVAL_PREFIX}/cancel"
        payload = {}
        if recordId is not None:
            payload["recordId"] = recordId
        if approvalId is not None:
            payload["approvalId"] = approvalId
        if revokeReason is not None:
            payload["revokeReason"] = revokeReason
        error_msg = kwargs.pop("error_msg", "撤回审批失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("再次提交审批")
    def resubmit_approval(self, recordId=None, infoId=None, orderQuantity=None,
                          remark=None, submitPrice=None,
                          status_code=200, **kwargs):
        """再次提交审批

        swagger 入参 (body):
          可选: recordId, infoId, orderQuantity, remark, submitPrice
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_PREFIX}/resubmitApproval"
        payload = {}
        if recordId is not None:
            payload["recordId"] = recordId
        if infoId is not None:
            payload["infoId"] = infoId
        if orderQuantity is not None:
            payload["orderQuantity"] = orderQuantity
        if remark is not None:
            payload["remark"] = remark
        if submitPrice is not None:
            payload["submitPrice"] = submitPrice
        error_msg = kwargs.pop("error_msg", "再次提交审批失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 链路 3：APP 端历史核价 ====================

    @allure.step("历史核价记录列表")
    def get_history(self, keyword=None, startTime=None, endTime=None,
                    pageNo=1, pageSize=10, status_code=200, **kwargs):
        """历史核价记录列表

        swagger 入参:
          可选: keyword, startTime(yyyy-MM-dd), endTime(yyyy-MM-dd),
                pageNo, pageSize
        swagger 返参 data: array<object>
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_PREFIX}/getHistory"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        if keyword:
            payload["keyword"] = keyword
        if startTime:
            payload["startTime"] = startTime
        if endTime:
            payload["endTime"] = endTime
        error_msg = kwargs.pop("error_msg", "获取历史核价记录列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("历史核价详情")
    def get_history_detail(self, id, status_code=200, **kwargs):
        """历史核价详情

        swagger 入参:
          必填: id
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APP_PREFIX}/getHistoryDetail"
        payload = {"id": id}
        error_msg = kwargs.pop("error_msg", "获取历史核价详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 链路 4：供应端核价配置 ====================

    @allure.step("根据供应商取联合供应商")
    def get_union_supplier_no_auth(self, supplierId, status_code=200, **kwargs):
        """根据供应商取联合供应商（无 Auth，GET 查询）

        注: 后端实际路径为 union-supplier/getUnionSupplierListNoAuth，仅接受 GET
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_UNION_PREFIX}-supplier/getUnionSupplierListNoAuth"
        error_msg = kwargs.pop("error_msg", "获取联合供应商失败")
        return self.get(url, params={"supplierId": supplierId},
                        status_code=status_code, error_msg=error_msg)

    @allure.step("核价配置查询")
    def pricing_config_get(self, supplierId=None, status_code=200, **kwargs):
        """核价配置查询（供应端）

        swagger 入参:
          可选: supplierId
        swagger 返参 data: {freightVisible, freightDefault, rebateVisible,
          rebateDefault, discountVisible, discountDefaultMode,
          discountPercentValue, discountFixedValue, paperPriceSource,
          needApproval, allowPriceAdjust, adjustSpace, processingFeeEditable,
          rolePrices, processingFees, approvalFlowNodes}
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_CONFIG_PREFIX}/get"
        payload = {}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        error_msg = kwargs.pop("error_msg", "核价配置查询失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("核价配置保存")
    def pricing_config_save(self, supplierId=None, paperPriceSource=None,
                            freightVisible=None, freightDefault=None,
                            rebateVisible=None, rebateDefault=None,
                            discountVisible=None, discountDefaultMode=None,
                            discountPercentValue=None, discountFixedValue=None,
                            needApproval=None, allowPriceAdjust=None,
                            adjustSpace=None, processingFeeEditable=None,
                            rolePrices=None, processingFees=None,
                            approvalFlowNodes=None,
                            usageRoles=None, fluteOptions=None,
                            status_code=200, **kwargs):
        """核价配置保存（供应端）

        swagger 入参 (body): supplierId, paperPriceSource, freightVisible,
          freightDefault, rebateVisible, rebateDefault, discountVisible,
          discountDefaultMode, discountPercentValue, discountFixedValue,
          needApproval, allowPriceAdjust, adjustSpace, processingFeeEditable,
          rolePrices（2.3.13 废弃）, processingFees, approvalFlowNodes
        2.3.13 新增: usageRoles, fluteOptions（§7.1.2）
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_CONFIG_PREFIX}/save"
        payload = {}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if paperPriceSource is not None:
            payload["paperPriceSource"] = paperPriceSource
        if freightVisible is not None:
            payload["freightVisible"] = freightVisible
        if freightDefault is not None:
            payload["freightDefault"] = freightDefault
        if rebateVisible is not None:
            payload["rebateVisible"] = rebateVisible
        if rebateDefault is not None:
            payload["rebateDefault"] = rebateDefault
        if discountVisible is not None:
            payload["discountVisible"] = discountVisible
        if discountDefaultMode is not None:
            payload["discountDefaultMode"] = discountDefaultMode
        if discountPercentValue is not None:
            payload["discountPercentValue"] = discountPercentValue
        if discountFixedValue is not None:
            payload["discountFixedValue"] = discountFixedValue
        if needApproval is not None:
            payload["needApproval"] = needApproval
        if allowPriceAdjust is not None:
            payload["allowPriceAdjust"] = allowPriceAdjust
        if adjustSpace is not None:
            payload["adjustSpace"] = adjustSpace
        if processingFeeEditable is not None:
            payload["processingFeeEditable"] = processingFeeEditable
        if rolePrices is not None:
            payload["rolePrices"] = rolePrices
        if processingFees is not None:
            payload["processingFees"] = processingFees
        if approvalFlowNodes is not None:
            payload["approvalFlowNodes"] = approvalFlowNodes
        if usageRoles is not None:
            payload["usageRoles"] = usageRoles
        if fluteOptions is not None:
            payload["fluteOptions"] = fluteOptions
        error_msg = kwargs.pop("error_msg", "核价配置保存失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("原纸代码档案列表")
    def pricing_paper_get_list(self, supplierId=None, status_code=200, **kwargs):
        """原纸代码档案列表（供应端）

        swagger 入参:
          可选: supplierId
        swagger 返参 data: array<object>
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_CONFIG_PREFIX}/paper/getList"
        payload = {}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        error_msg = kwargs.pop("error_msg", "获取原纸代码档案列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("搜索用户")
    def pricing_user_search(self, keyword=None, status_code=200, **kwargs):
        """搜索用户（供应端，审批节点选择用户）

        swagger 入参:
          可选: keyword(用户名称)
        swagger 返参 data: array<object>
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_CONFIG_PREFIX}/user/search"
        payload = {}
        if keyword:
            payload["keyword"] = keyword
        error_msg = kwargs.pop("error_msg", "搜索用户失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("供应商上架层数列表")
    def pricing_layer_get_list(self, supplierId=None, status_code=200, **kwargs):
        """供应商上架层数列表（供应端）

        swagger 入参:
          可选: supplierId
        swagger 返参 data: array<object>
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_CONFIG_PREFIX}/layer/getList"
        payload = {}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        error_msg = kwargs.pop("error_msg", "获取供应商上架层数列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 链路 5：供应端审批 ====================

    @allure.step("审批记录列表(供应端)")
    def pricing_approval_get_list(self, status=None, supplierId=None, keyword=None,
                                  startTime=None, endTime=None,
                                  pageNo=1, pageSize=10,
                                  status_code=200, **kwargs):
        """审批记录列表(供应端)

        swagger 入参:
          可选: status, supplierId, keyword, startTime, endTime, pageNo, pageSize
        swagger 返参 data: array<object>
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APPROVAL_PREFIX}/getList"
        payload = {
            "pageNo": pageNo,
            "pageSize": pageSize,
        }
        if status:
            payload["status"] = status
        if supplierId is not None:
            payload["supplierId"] = supplierId
        if keyword:
            payload["keyword"] = keyword
        if startTime:
            payload["startTime"] = startTime
        if endTime:
            payload["endTime"] = endTime
        error_msg = kwargs.pop("error_msg", "获取供应端审批记录列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("审批详情(供应端)")
    def pricing_approval_get_detail(self, id, status_code=200, **kwargs):
        """审批详情(供应端)

        swagger 入参:
          必填: id
        """
        # Author: Author
        # Create Date: 2026-08-19
        # IsAI: True
        url = f"{HEJIA_APPROVAL_PREFIX}/getDetail"
        payload = {"id": id}
        error_msg = kwargs.pop("error_msg", "获取供应端审批详情失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 2.3.13 新增接口 ====================

    @allure.step("楞型选项列表（2.3.13）")
    def pricing_flute_option_get_options(self, supplierId=None, status_code=200, **kwargs):
        """楞型选项列表（供应端，2.3.13 新增）

        §7.1.4：供应商维护楞型选项，默认全选 E/B/C/A/EB/BC/AC/AAB 七种；
        非全选时校验楞率必须手动填写；核价解析材料代码时仅对已启用楞型计算纸板价。
        swagger 入参:
          可选: supplierId
        swagger 返参 data: array<object> [{fluteCode, defaultRate, editable}]
        """
        # Author: Author
        # Create Date: 2026-10-20
        # IsAI: True
        url = f"{HEJIA_CONFIG_PREFIX}/fluteOption/getOptions"
        params = {}
        if supplierId is not None:
            params["supplierId"] = supplierId
        error_msg = kwargs.pop("error_msg", "获取楞型选项列表失败")
        return self.get(url, params=params, status_code=status_code, error_msg=error_msg, **kwargs)

    @allure.step("试算加工费（2.3.13）")
    def calc_processing_fee(self, recordId, approvalId=None, price=None, priceType=None, status_code=200, **kwargs):
        """试算加工费与最终价（APP 端，2.3.13 新增）

        §7.3.5：销售调价时实时试算加工费与最终价格；
        priceType=external 最终价四舍五入到 2 位小数，其他保留完整精度。
        swagger 入参 (body):
          必填: recordId（报价明细记录ID）
          可选: approvalId（审批单ID，审批页试算时传）、price（新单价）、priceType（价格类型）
        swagger 返参 data: {processingFee, finalPrice, originalProcessingFee}
        """
        # Author: Author
        # Create Date: 2026-10-20
        # IsAI: True
        url = f"{HEJIA_APP_PREFIX}/calcProcessingFee"
        payload = {"recordId": recordId}
        if approvalId is not None:
            payload["approvalId"] = approvalId
        if price is not None:
            payload["price"] = price
        if priceType is not None:
            payload["priceType"] = priceType
        error_msg = kwargs.pop("error_msg", "试算加工费失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("审批记录导出 Excel（2.3.13）")
    def pricing_approval_export(self, supplierName=None, approvalStatus=None, startTime=None, endTime=None, status_code=200, **kwargs):
        """审批记录导出 Excel（供应端，2.3.13 新增）

        §7.2.2：按审批状态和时间范围导出，忽略分页参数。
        返回二进制文件流，需用 return_response=True 获取原始 Response。
        swagger 入参 (body):
          可选: supplierName, approvalStatus, startTime, endTime
        Returns:
            requests.Response: 原始响应（Excel 二进制流），调用方用 .content 取字节。
        """
        # Author: Author
        # Create Date: 2026-10-20
        # IsAI: True
        url = f"{HEJIA_APPROVAL_PREFIX}/export"
        payload = {}
        if supplierName is not None:
            payload["supplierName"] = supplierName
        if approvalStatus is not None:
            payload["approvalStatus"] = approvalStatus
        if startTime is not None:
            payload["startTime"] = startTime
        if endTime is not None:
            payload["endTime"] = endTime
        error_msg = kwargs.pop("error_msg", "审批记录导出失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg, return_response=True)
