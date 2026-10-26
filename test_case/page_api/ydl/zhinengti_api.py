# -*- coding: utf-8 -*-
"""易单来 - 智能体模块接口（基于 APP 抓包）
域名支持：
- smart.onlinecps.cn：智能体对话、消息、组件、关注等
- smart.cpsol.net：产品上架相关接口
"""

import allure
import conftest
from test_case.page_api.public.base_api import BaseAPI

# 智能体接口路径前缀
AI_PREFIX = "/djintelligent/ai-backend/ai"
SYSTEM_PREFIX = "/djintelligent/ai-backend/system"
COMPONENT_PREFIX = "/djintelligent/ai-backend/component"
KEY_ATTENTION_PREFIX = "/djintelligent/ai-backend/keyAttention"
# 签到拜访接口路径前缀（在 suppliertest.onlinecps.cn 上）
SALESMAN_PREFIX = "/djsupplier/app/djcockpit/easyorder/salesman"
# 产品上架接口路径前缀（在 smart.cpsol.net 上）
ONSHELF_PREFIX = "/djintelligent/ai-autoonshelf/api"
# 产品管理服务路径前缀（在 suppliertest.cpsol.net 上，第三阶段上架执行）
PRODUCT_PREFIX = "/djsupplier/product"
# 智能体域名
SMART_BASE_URL = "https://smart.onlinecps.cn"
# 产品上架域名
SMART_CPSOL_BASE_URL = "https://smart.cpsol.net"
# 产品管理服务域名（阿里云环境）
SUPPLIER_CPSOL_BASE_URL = "https://suppliertest.cpsol.net"
# 产品上架状态标识（抓包实证：onoffStatus=2 且 auditStatus=6 ⇔ 已上架+审核通过，严格1:1）
ONOFF_STATUS_ON = 2
AUDIT_STATUS_PASSED = 6


class ZhinengtiAPI(BaseAPI):
    """易单来智能体模块接口封装（使用 smart.onlinecps.cn 域名）"""

    def __init__(self, base_url=None, headers=None, cookies=None):
        super().__init__(base_url or SMART_BASE_URL, headers, cookies)
        biz_headers = {
            "device": "web",
            "source": "easyorder",
            "version": "2.3.7",
            "Content-Type": "application/json",
        }
        if self.headers:
            self.headers.update(biz_headers)
        else:
            self.headers = biz_headers
        # 使用 smart.onlinecps.cn 的 token
        smart_tok = conftest.smart_token.get("token", "")
        if smart_tok:
            self.cookies["token"] = smart_tok
            self._extra_cookies["token"] = smart_tok

    # ==================== 系统配置 ====================

    @allure.step("获取授权功能列表")
    def get_auth_function_list(self, payload_data, status_code=200, **kwargs):
        """获取授权功能列表（签到/数据查询/智能简报/产品上架/问答助理等）"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SYSTEM_PREFIX}/v2/getAuthFunctionList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取授权功能列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取系统配置")
    def get_config(self, payload_data, status_code=200, **kwargs):
        """获取系统配置（热门问题/提示语等）"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SYSTEM_PREFIX}/config.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取系统配置失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== AI 对话 ====================

    @allure.step("提交流式请求")
    def submit_stream(self, payload_data, status_code=200, **kwargs):
        """提交 AI 流式请求（对话/签到/关注等操作）
        返回 SSE 文本字符串（非 JSON），调用方需自行解析。
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{AI_PREFIX}/v2/submitStream.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "提交流式请求失败")
        payload.update(kwargs)
        # submitStream 返回 SSE 流式文本，不是 JSON，用 return_response 拿原始响应
        resp = self.post(url, json=payload, status_code=status_code,
                         error_msg=error_msg, return_response=True)
        return resp.text

    @allure.step("获取所有消息")
    def get_all_message(self, payload_data, status_code=200, **kwargs):
        """获取会话中的所有消息"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{AI_PREFIX}/getAllMessage.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取所有消息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("删除消息")
    def delete_message(self, payload_data, status_code=200, **kwargs):
        """删除指定会话中的消息"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{AI_PREFIX}/deleteMessage.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "删除消息失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 组件管理 ====================

    @allure.step("根据ID获取组件")
    def get_component_by_id(self, payload_data, status_code=200, **kwargs):
        """根据ID获取组件信息"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{COMPONENT_PREFIX}/getById.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取组件失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("保存组件")
    def save_component(self, payload_data, status_code=200, **kwargs):
        """保存组件（如关注确认结果）"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{AI_PREFIX}/component/save.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "保存组件失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 关注操作 ====================

    @allure.step("确认关注")
    def confirm_attention(self, payload_data, status_code=200, **kwargs):
        """确认关注操作（客户/订单关注）"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{KEY_ATTENTION_PREFIX}/confirm.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "确认关注失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 签到拜访 ====================

    @allure.step("获取业务员拜访概览")
    def get_salesman_visit_overview(self, payload_data, status_code=200, **kwargs):
        """获取业务员拜访概览（签到客户数/拜访客户数/超期未拜访统计）
        注意：此接口在 suppliertest.onlinecps.cn 域名上
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # 签到拜访接口在 suppliertest.onlinecps.cn 上，需要使用主域名的 base_url
        import config
        original_base_url = self.base_url
        self.base_url = config.base_url.rstrip("/")
        # 保存原 headers，添加 app-role
        original_headers = self.headers.copy() if self.headers else {}
        self.headers = self.headers or {}
        self.headers["app-role"] = "salesman"
        # 使用主域名的 token
        original_token = self.cookies.get("token", "")
        original_extra_token = self._extra_cookies.get("token", "")
        main_token = config.default_cookies.get("token", "")
        if main_token:
            self.cookies["token"] = main_token
            # BaseAPI.get_base_request() 每次请求前会用 _extra_cookies 重同步 cookies，
            # 必须同步覆盖 _extra_cookies，否则 token 会被还原成 __init__ 里的 smart_token，
            # 导致主域名 djcockpit 接口鉴权失败（10001504 获取用户信息失败）。
            self._extra_cookies["token"] = main_token
        try:
            url = f"{SALESMAN_PREFIX}/getSalesmanVisitOverview.do"
            payload = dict(payload_data)
            error_msg = kwargs.pop("error_msg", "获取业务员拜访概览失败")
            payload.update(kwargs)
            result = self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
        finally:
            self.base_url = original_base_url
            self.headers = original_headers
            self.cookies["token"] = original_token
            self._extra_cookies["token"] = original_extra_token
        return result

    # ==================== 产品上架（smart.cpsol.net） ====================

    def _get_cpsol_session(self):
        """获取 smart.cpsol.net 的 session（使用独立 token）"""
        import requests
        session = requests.Session()
        session.headers.update(self.headers)
        cpsol_tok = conftest.smart_cpsol_token.get("token", "")
        if cpsol_tok:
            session.cookies.set("token", cpsol_tok)
        return session

    @allure.step("获取交期配置列表")
    def get_delivery_config_list(self, payload_data, status_code=200, **kwargs):
        """获取交期配置列表"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SMART_CPSOL_BASE_URL}{ONSHELF_PREFIX}/proxy/supplierConfig/selectDeliveryConfigList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取交期配置列表失败")
        payload.update(kwargs)
        session = self._get_cpsol_session()
        resp = session.post(url, json=payload)
        return resp.json()

    @allure.step("产品上架")
    def onshelf(self, payload_data, status_code=200, **kwargs):
        """产品上架接口"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SMART_CPSOL_BASE_URL}{ONSHELF_PREFIX}/onshelf.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "产品上架失败")
        payload.update(kwargs)
        session = self._get_cpsol_session()
        resp = session.post(url, json=payload)
        return resp.json()

    @allure.step("获取客户列表")
    def get_user_list(self, payload_data, status_code=200, **kwargs):
        """获取客户列表（用于产品上架选择客户）"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SMART_CPSOL_BASE_URL}{ONSHELF_PREFIX}/proxy/paymentDay/selectUserList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取客户列表失败")
        payload.update(kwargs)
        session = self._get_cpsol_session()
        resp = session.post(url, json=payload)
        return resp.json()

    @allure.step("获取价格方案列表")
    def get_user_plan_list(self, payload_data, status_code=200, **kwargs):
        """获取客户价格方案列表"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SMART_CPSOL_BASE_URL}{ONSHELF_PREFIX}/proxy/paymentDay/getUserPlanList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取价格方案列表失败")
        payload.update(kwargs)
        session = self._get_cpsol_session()
        resp = session.post(url, json=payload)
        return resp.json()

    @allure.step("获取客户产品价格方案详情")
    def find_user_product_plan_details(self, payload_data, status_code=200, **kwargs):
        """获取客户产品价格方案详情"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SMART_CPSOL_BASE_URL}{ONSHELF_PREFIX}/proxy/paymentDay/findUserProductPlanDetails.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取客户产品价格方案详情失败")
        payload.update(kwargs)
        session = self._get_cpsol_session()
        resp = session.post(url, json=payload)
        return resp.json()

    # ==================== 签到验证（suppliertest.onlinecps.cn） ====================

    def _call_main_domain(self, url_path, payload, status_code=200, error_msg=""):
        """在 suppliertest.onlinecps.cn 域名上调用接口（临时切换）"""
        import config
        original_base_url = self.base_url
        self.base_url = config.base_url.rstrip("/")
        original_headers = self.headers.copy() if self.headers else {}
        self.headers = self.headers or {}
        self.headers["app-role"] = "salesman"
        original_token = self.cookies.get("token", "")
        original_extra_token = self._extra_cookies.get("token", "")
        main_token = config.default_cookies.get("token", "")
        if main_token:
            self.cookies["token"] = main_token
            # BaseAPI.get_base_request() 每次请求前会用 _extra_cookies 重同步 cookies，
            # 必须同步覆盖 _extra_cookies，否则 token 会被还原成 __init__ 里的 smart_token，
            # 导致主域名 djcockpit 接口鉴权失败（10001504 获取用户信息失败）。
            self._extra_cookies["token"] = main_token
        try:
            result = self.post(url_path, json=payload, status_code=status_code, error_msg=error_msg)
        finally:
            self.base_url = original_base_url
            self.headers = original_headers
            self.cookies["token"] = original_token
            self._extra_cookies["token"] = original_extra_token
        return result

    @allure.step("获取供应商信息")
    def get_supplier_info_no_auth(self, status_code=200):
        """获取供应商列表，用于产品上架供应商选择"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        url = "/djsupplier/DJEASYORDER/goal/new/getSupplierInfoNoAuth.do"
        session = self._get_cpsol_session()
        resp = session.post(f"{SMART_CPSOL_BASE_URL}{url}", json={})
        return resp.json()

    def resolve_supplier_id(self):
        """解析当前用户的产品上架供应商ID
        按产品上架流程文档：筛选 salesMain='y' 的主供应商
        Returns: (supplier_id, supplier_name, is_multi_supplier)
        """
        res = self.get_supplier_info_no_auth()
        assert res.get("code") == "10001200", \
            f"获取供应商信息失败, code={res.get('code')}, msg={res.get('msg')}"
        supplier_list = res.get("data", {}).get("list", [])
        assert len(supplier_list) > 0, "供应商列表不应为空"
        # 判断多/单供应商
        is_multi = any(s.get("unionSupplier") == "1" for s in supplier_list)
        # 产品上架流程：筛选 salesMain='y' 的主供应商
        main_supplier = None
        for s in supplier_list:
            if s.get("salesMain") == "y":
                main_supplier = s
                break
        if main_supplier:
            return str(main_supplier.get("supplierId")), main_supplier.get("supplierName", ""), is_multi
        # 无 salesMain='y' 时取首条
        return str(supplier_list[0].get("supplierId")), supplier_list[0].get("supplierName", ""), is_multi

    @allure.step("获取签到拜访记录列表")
    def get_sign_in_visit_record_list(self, payload_data, status_code=200, **kwargs):
        """获取签到和拜访记录列表（ground_truth 验证接口）"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{SALESMAN_PREFIX}/getSignInAndVisitRecordList.do"
        error_msg = kwargs.pop("error_msg", "获取签到拜访记录列表失败")
        return self._call_main_domain(url, payload_data, status_code, error_msg)

    # ==================== 重点关注验证（suppliertest.onlinecps.cn） ====================

    @allure.step("设置重点关注")
    def set_key_attention(self, payload_data, status_code=200, **kwargs):
        """设置/取消重点关注（ground_truth 验证接口）"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = "/djsupplier/app/djcockpit/easyorder/keyAttention.do"
        error_msg = kwargs.pop("error_msg", "设置重点关注失败")
        return self._call_main_domain(url, payload_data, status_code, error_msg)

    @allure.step("获取重点关注客户列表")
    def get_key_attention_customer_list(self, payload_data, status_code=200, **kwargs):
        """获取重点关注客户列表（ground_truth 验证接口）"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        url = "/djsupplier/app/djcockpit/easyorder/keyAttention/getCustomerList.do"
        error_msg = kwargs.pop("error_msg", "获取重点关注客户列表失败")
        return self._call_main_domain(url, payload_data, status_code, error_msg)

    # ==================== 产品上架第三阶段（suppliertest.cpsol.net） ====================

    def _call_supplier_cpsol(self, url_path, payload, status_code=200, error_msg="",
                             as_form_data=False):
        """在 suppliertest.cpsol.net 域名上调用接口（使用独立 session）"""
        import requests
        url = f"{SUPPLIER_CPSOL_BASE_URL}{url_path}"
        session = requests.Session()
        session.trust_env = False
        session.verify = False
        session.headers.update(self.headers)
        cpsol_tok = conftest.cpsol_token.get("token", "")
        if cpsol_tok:
            session.cookies.set("token", cpsol_tok)
        if as_form_data:
            # form-data 请求需要移除 Content-Type，让 requests 自动设置 multipart boundary
            session.headers.pop("Content-Type", None)
            resp = session.post(url, data=payload)
        else:
            resp = session.post(url, json=payload)
        return resp.json()

    @allure.step("查询产品审核详情")
    def select_product_examine_by_id(self, fid, status_code=200):
        """根据产品ID查询产品审核详情（form-data 请求）"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        url = f"{PRODUCT_PREFIX}/selectProductExamineById.do"
        return self._call_supplier_cpsol(url, {"fid": fid}, status_code,
                                         "查询产品审核详情失败", as_form_data=True)

    @allure.step("产品审核")
    def check_product_examine(self, payload_data, status_code=200, **kwargs):
        """产品审核通过/驳回（auditStatus=6 表示上架审核通过）"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        url = f"{PRODUCT_PREFIX}/checkProductExamine.do"
        error_msg = kwargs.pop("error_msg", "产品审核失败")
        return self._call_supplier_cpsol(url, payload_data, status_code, error_msg)

    @allure.step("查询价格方案列表")
    def select_price_plan_list(self, payload_data, status_code=200, **kwargs):
        """查询产品价格方案列表"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        url = f"{PRODUCT_PREFIX}/selectPricePlanList.do"
        error_msg = kwargs.pop("error_msg", "查询价格方案列表失败")
        return self._call_supplier_cpsol(url, payload_data, status_code, error_msg)

    @allure.step("新增/更新价格方案审核")
    def add_price_plan_examine(self, payload_data, status_code=200, **kwargs):
        """新增或更新价格方案（updateOrSave=1 新增，=2 更新）。

        入参为"模型列表"（list of models），抓包实证（2026-10-26）每个模型必含：
        groupGoodId/groupGoodName/supplierId/supplierName/marketingName(方案名)/
        groupPrice(字符串)/minArea/minGroupPrice/groupareaList([{cityCode,groupArea,
        checked,creator,type}])/salesStreets 与 salesStreetsOld([{cityCode,
        unselectedStreets}])/errorAry/checkAll/isIndeterminate/bigAllright/
        smallAllright/lengthAllright/widthAllright/minAreaOrStart/updateOrSave/
        effect/auditorType；缺失伴随字段报 code=110001 操作失败，
        groupPrice/minArea 为空报 code=10003001。
        """
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        url = f"{PRODUCT_PREFIX}/addPricePlanExamine.do"
        error_msg = kwargs.pop("error_msg", "新增/更新价格方案失败")
        return self._call_supplier_cpsol(url, payload_data, status_code, error_msg)

    @allure.step("查询价格方案审核详情")
    def select_price_plan_examine(self, payload_data, status_code=200, **kwargs):
        """根据UUID查询价格方案审核详情"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        url = f"{PRODUCT_PREFIX}/selectPricePlanExamine.do"
        error_msg = kwargs.pop("error_msg", "查询价格方案审核详情失败")
        return self._call_supplier_cpsol(url, payload_data, status_code, error_msg)

    @allure.step("价格方案审核")
    def update_price_plan(self, payload_data, status_code=200, **kwargs):
        """价格方案审核通过"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        url = f"{PRODUCT_PREFIX}/updatePricePlan.do"
        error_msg = kwargs.pop("error_msg", "价格方案审核失败")
        return self._call_supplier_cpsol(url, payload_data, status_code, error_msg)

    @allure.step("价格方案生效")
    def update_price_plan_effect(self, payload_data, status_code=200, **kwargs):
        """使价格方案生效（effect=1）"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        url = f"{PRODUCT_PREFIX}/updatePricePlanEffect.do"
        error_msg = kwargs.pop("error_msg", "价格方案生效失败")
        return self._call_supplier_cpsol(url, payload_data, status_code, error_msg)

    # ==================== 会话与置顶消息（首页加载） ====================

    @allure.step("获取全部会话列表")
    def get_all_conversations(self, payload_data, status_code=200, **kwargs):
        """获取当前用户的全部 AI 会话列表（v2）"""
        # Author: Author
        # Create Date: 2026-10-22
        # IsAI: True
        url = f"{AI_PREFIX}/v2/getAllConversations.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取全部会话列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取置顶消息列表")
    def get_all_top_message_list(self, payload_data, status_code=200, **kwargs):
        """获取智能体置顶消息列表（首页加载）"""
        # Author: Author
        # Create Date: 2026-10-22
        # IsAI: True
        url = f"{AI_PREFIX}/getAllTopMessageList.do"
        payload = dict(payload_data)
        error_msg = kwargs.pop("error_msg", "获取置顶消息列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== 产品上架闭环补充（suppliertest.cpsol.net） ====================

    @allure.step("查询产品列表")
    def load_list_products(self, payload_data, status_code=200, **kwargs):
        """查询产品列表（支持按 productName 精确过滤，用于复用选品与上架后终态校验）"""
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        url = f"{PRODUCT_PREFIX}/loadListProducts.do"
        error_msg = kwargs.pop("error_msg", "查询产品列表失败")
        return self._call_supplier_cpsol(url, payload_data, status_code, error_msg)

    @allure.step("查询已有层型楞型列表")
    def load_exist_layer_and_flute(self, payload_data, status_code=200, **kwargs):
        """查询纸板团购上架的层数/楞型配置选项（产品上架造数的层数楞型来源）。
        入参（抓包实证）：{"supplierId": "400"}；路径 /djsupplier/product/loadExistLayerAndFlute.do。
        响应为双层信封：data.data.list = [{label:"5层", value:5, children:[{label:"BC瓦", value:1}, ...]}]，
        节点 value=层数，children.value=楞型(fluteType)，实证 BC瓦 ⇔ value=1。
        """
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        url = f"{PRODUCT_PREFIX}/loadExistLayerAndFlute.do"
        error_msg = kwargs.pop("error_msg", "查询层型楞型列表失败")
        return self._call_supplier_cpsol(url, payload_data, status_code, error_msg)

    @allure.step("新增产品")
    def add_product(self, payload_data, status_code=200, **kwargs):
        """新增产品（fid 为空串；带 fid 则为编辑态；响应不返回 fid，需回查列表取 fid）"""
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        url = f"{PRODUCT_PREFIX}/addProduct.do"
        error_msg = kwargs.pop("error_msg", "新增产品失败")
        return self._call_supplier_cpsol(url, payload_data, status_code, error_msg)

    @allure.step("查询单个产品详情")
    def load_single_product(self, fid, status_code=200):
        """根据产品ID查询单个产品详情（form-data 请求，复用产品规格的取数源）"""
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        url = f"{PRODUCT_PREFIX}/loadSingleProduct.do"
        return self._call_supplier_cpsol(url, {"fid": fid}, status_code,
                                         "查询单个产品详情失败", as_form_data=True)

    @allure.step("查询全部产品名称池")
    def load_product_names(self, payload_data, status_code=200, **kwargs):
        """查询供应商全部已有产品名称（用于产品命名查重）"""
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        url = "/djsupplier/productManage/loadProductNames.do"
        error_msg = kwargs.pop("error_msg", "查询产品名称池失败")
        return self._call_supplier_cpsol(url, payload_data, status_code, error_msg)

    @allure.step("查询材质名称列表")
    def get_materials_name_list(self, payload_data, status_code=200, **kwargs):
        """查询材质名称列表（抓包实证：本环境 data.list 返回 null，且部分公司无权限）。
        因此产品上架造数不依赖本接口动态取材质，改为直接硬编码固定材质代码 B434C（见用例 PRODUCT_MATERIAL_CODE）。
        入参使用 partnerId（非 supplierId），如 {"partnerId": "400"}。
        """
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        url = "/djsupplier/supplierConfig/getMaterialsNameList.do"
        error_msg = kwargs.pop("error_msg", "查询材质名称列表失败")
        return self._call_supplier_cpsol(url, payload_data, status_code, error_msg)

    def find_product_by_name(self, product_name, supplier_id, key_area="3303", status_code=200):
        """按产品名称精确回查产品列表，返回匹配的产品项；未找到返回 None"""
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        payload = {
            "keyArea": key_area, "supplierId": supplier_id,
            "auditStatus": 0, "onoffStatus": 0, "marketingChannelJson": "",
            "pageSize": 15, "pageNum": 1, "version": "1.0",
            "layer": None, "fluteType": None,
            "productName": product_name, "productType": ""
        }
        res = self.load_list_products(payload, status_code)
        if res.get("code") != "10001200":
            return None
        for item in (res.get("data") or {}).get("list") or []:
            if item.get("productName") == product_name:
                return item
        return None

    @allure.step("查询供应商可售城市区域")
    def find_city_area(self, oa_id, key_area="3303", status_code=200):
        """查询供应商可售城市区域列表（form-data 请求 oaId=supplierId, keyArea）
        返回 data.list 每项含 cityName/cityCode，cityCode 即新增产品 lists 的 listFgroupareaids
        """
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        url = "/djsupplier/productManage/findCityArea.do"
        return self._call_supplier_cpsol(url, {"oaId": oa_id, "keyArea": key_area}, status_code,
                                         "查询可售城市区域失败", as_form_data=True)

    # ==================== OSS 图片直传（产品主图/详情图上传） ====================

    @allure.step("获取OSS上传临时凭证")
    def get_security_token(self, status_code=200):
        """获取阿里云 OSS 直传的 STS 临时凭证（空 body POST）
        返回 data 含 accessKeyId/accessKeySecret/securityToken/bucketName/tmpDir/expiration
        """
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        url = "/djsupplier/saveFile/getSecurityToken.do"
        return self._call_supplier_cpsol(url, {}, status_code,
                                         "获取OSS上传凭证失败", as_form_data=True)

    def _oss_v1_sign(self, access_key_secret, string_to_sign):
        """OSS V1 签名：base64(hmac-sha1(accessKeySecret, stringToSign))"""
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        import hmac
        import hashlib
        import base64
        digest = hmac.new(access_key_secret.encode("utf-8"),
                          string_to_sign.encode("utf-8"), hashlib.sha1).digest()
        return base64.b64encode(digest).decode("utf-8")

    @allure.step("上传图片到OSS并构造figure")
    def upload_product_image(self, image_bytes, ftype, supplier_id, key_area="3303",
                             ext="jpg", content_type="image/jpeg", status_code=200):
        """上传图片到阿里云 OSS tmp 目录，构造产品 figure 条目。
        链路（拓包实证）：getSecurityToken(STS) → PUT 直传 OSS tmp → 生成带签名 GET URL(furl)。
        后端 addProduct/editProduct 会将 tmp 图确认并移动到正式目录；复用旧图(save/目录)会报“确认上传图片失败”。
        返回 figure dict：{ftype, fuserid, fkeyarea, ffileid(tmp对象键), furl(带签名 GET URL)}。
        ftype：1=主图，2=详情图。
        """
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        import time
        import random
        from email.utils import formatdate
        from urllib.parse import quote
        import requests

        # 1. 获取 STS 临时凭证
        tok_res = self.get_security_token(status_code)
        assert tok_res.get("code") == "10001200", \
            f"获取OSS上传凭证失败, resp={tok_res}"
        assert tok_res.get("success") is True, f"success应为True, 实际={tok_res.get('success')}"
        d = tok_res.get("data") or {}
        ak = d["accessKeyId"]
        sk = d["accessKeySecret"]
        token = d["securityToken"]
        bucket = d.get("bucketName", "djcps")
        tmp_dir = d.get("tmpDir", "aliyun-test/fileserver/tmp/")
        host = f"{bucket}.oss-cn-hangzhou.aliyuncs.com"

        # 2. 生成对象键：tmpDir + {epoch毫秒}{5位随机}.{ext}（与 APP 命名规则一致）
        filename = f"{int(time.time() * 1000)}{random.randint(10000, 99999)}.{ext}"
        object_key = f"{tmp_dir}{filename}"

        # 3. PUT 直传（OSS V1 header 签名，使用 x-oss-date；Date 位置置空）
        oss_date = formatdate(timeval=None, localtime=False, usegmt=True)
        canon_headers = f"x-oss-date:{oss_date}\nx-oss-security-token:{token}\n"
        canon_resource = f"/{bucket}/{object_key}"
        # Date 位取 x-oss-date 的值（OSS 规范：使用 x-oss-date 时 StringToSign 的 Date 字段填其值，非置空）
        string_to_sign = f"PUT\n\n{content_type}\n{oss_date}\n{canon_headers}{canon_resource}"
        put_sig = self._oss_v1_sign(sk, string_to_sign)
        put_url = f"https://{host}/{object_key}"
        put_headers = {
            "Content-Type": content_type,
            "x-oss-date": oss_date,
            "x-oss-security-token": token,
            "Authorization": f"OSS {ak}:{put_sig}",
        }
        sess = requests.Session()
        sess.trust_env = False
        sess.verify = False
        r = sess.put(put_url, data=image_bytes, headers=put_headers, timeout=30)
        assert r.status_code == 200, \
            f"OSS图片直传失败, status={r.status_code}, url={put_url}, resp={r.text[:300]}"

        # 4. 生成带签名的 GET URL 作为 furl（30 分钟有效期；security-token 作为子资源参与签名）
        expires = str(int(time.time()) + 1800)
        get_canon = f"/{bucket}/{object_key}?security-token={token}"
        get_string_to_sign = f"GET\n\n\n{expires}\n{get_canon}"
        get_sig = self._oss_v1_sign(sk, get_string_to_sign)
        furl = (f"https://{host}/{object_key}?OSSAccessKeyId={quote(ak, safe='')}"
                f"&Expires={expires}&Signature={quote(get_sig, safe='')}"
                f"&security-token={quote(token, safe='')}")

        # 5. 构造 figure 条目
        return {
            "ftype": ftype, "fuserid": str(supplier_id), "fkeyarea": key_area,
            "ffileid": object_key, "furl": furl,
        }
