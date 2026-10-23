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
        main_token = config.default_cookies.get("token", "")
        if main_token:
            self.cookies["token"] = main_token
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
        main_token = config.default_cookies.get("token", "")
        if main_token:
            self.cookies["token"] = main_token
        try:
            result = self.post(url_path, json=payload, status_code=status_code, error_msg=error_msg)
        finally:
            self.base_url = original_base_url
            self.headers = original_headers
            self.cookies["token"] = original_token
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
        """新增或更新价格方案（updateOrSave=1 新增，=2 更新）"""
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
