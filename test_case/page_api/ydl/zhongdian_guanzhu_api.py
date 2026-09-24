# -*- coding: utf-8 -*-
"""易单来 - APP 工作台-AI重点关注公共模块接口（基于易单来swaggerApi.json）"""

import allure
from test_case.page_api.public.base_api import BaseAPI

# 来自 swagger 2.0 的 basePath，DJEASYORDER 路径统一加 /djsupplier 前缀
KEY_ATTENTION_PREFIX = "/djsupplier/DJEASYORDER/keyAttention/common"

# APP 实际路径（抓包）
APP_KEY_ATTENTION_PREFIX = "/djsupplier/app/djcockpit/easyorder/keyAttention"

# AI 重点关注确认接口（独立域名）
AI_KEY_ATTENTION_URL = "https://smart.onlinecps.cn/djintelligent/ai-backend/keyAttention/confirm.do"


class ZhongdianGuanzhuAPI(BaseAPI):
    """易单来 APP AI重点关注公共模块接口封装"""

    def __init__(self, base_url=None, headers=None, cookies=None):
        super().__init__(base_url, headers, cookies)
        biz_headers = {
            "device": "app",
            "source": "easy_order",
            "version": "2.3.5",
            "Content-Type": "application/json",
        }
        if self.headers:
            self.headers.update(biz_headers)
        else:
            self.headers = biz_headers

    @allure.step("获取用户的重点关注")
    def get_user_common(self, type, appRole, status_code=200, **kwargs):
        """获取用户的重点关注（getUserCommon.do）

        swagger 入参:
          必填: type(关注类型:customer客户/order订单),
                appRole(应用角色:manage管理员/salesman业务员)
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{KEY_ATTENTION_PREFIX}/getUserCommon.do"
        payload = {"type": type, "appRole": appRole}
        error_msg = kwargs.pop("error_msg", "获取用户的重点关注失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("通过业务Id获取重点关注")
    def get_by_business_common(self, businessIdList, userId, appRole, companyId,
                               status_code=200, **kwargs):
        """通过业务Id获取重点关注（getByBusinessCommon.do）

        swagger 入参:
          必填: businessIdList(业务ID集合), userId(用户id),
                appRole(应用角色:manage管理员/salesman业务员), companyId(公司id)
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{KEY_ATTENTION_PREFIX}/getByBusinessCommon.do"
        payload = {
            "businessIdList": businessIdList,
            "userId": userId,
            "appRole": appRole,
            "companyId": companyId,
        }
        error_msg = kwargs.pop("error_msg", "通过业务Id获取重点关注失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("批量增加重点关注")
    def batch_add_common(self, businessIdList, userId, appRole, companyId,
                         status_code=200, **kwargs):
        """批量增加重点关注（与通过业务Id获取同URL：getByBusinessCommon.do）

        用户确认批量增加与 getByBusinessCommon.do 同路径，payload 通过 kwargs 扩展；
        swagger 未定义批量操作专属字段，联调后按真实 payload 补齐。
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{KEY_ATTENTION_PREFIX}/getByBusinessCommon.do"
        payload = {
            "businessIdList": businessIdList,
            "userId": userId,
            "appRole": appRole,
            "companyId": companyId,
        }
        error_msg = kwargs.pop("error_msg", "批量增加重点关注失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("批量取消重点关注")
    def batch_cancel_common(self, businessIdList, userId, appRole, companyId,
                            status_code=200, **kwargs):
        """批量取消重点关注（与通过业务Id获取同URL：getByBusinessCommon.do）

        用户确认批量取消与 getByBusinessCommon.do 同路径，payload 通过 kwargs 扩展；
        swagger 未定义批量操作专属字段，联调后按真实 payload 补齐。
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True
        url = f"{KEY_ATTENTION_PREFIX}/getByBusinessCommon.do"
        payload = {
            "businessIdList": businessIdList,
            "userId": userId,
            "appRole": appRole,
            "companyId": companyId,
        }
        error_msg = kwargs.pop("error_msg", "批量取消重点关注失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    # ==================== APP 实际接口（抓包） ====================

    @allure.step("获取重点关注订单列表")
    def get_order_list(self, orgId, supplierId, status_code=200, **kwargs):
        """获取重点关注订单列表（APP 抓包）

        入参:
          orgId: 组织ID
          supplierId: 供应商ID
        """
        url = f"{APP_KEY_ATTENTION_PREFIX}/getOrderList.do"
        payload = {"orgId": orgId, "supplierId": supplierId}
        error_msg = kwargs.pop("error_msg", "获取重点关注订单列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取重点关注客户列表")
    def get_customer_list(self, orgId, supplierId, status_code=200, **kwargs):
        """获取重点关注客户列表（APP 抓包）

        入参:
          orgId: 组织ID
          supplierId: 供应商ID
        """
        url = f"{APP_KEY_ATTENTION_PREFIX}/getCustomerList.do"
        payload = {"orgId": orgId, "supplierId": supplierId}
        error_msg = kwargs.pop("error_msg", "获取重点关注客户列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("设置/取消重点关注")
    def set_key_attention(self, type, attention, businessId, status_code=200, **kwargs):
        """设置/取消重点关注（APP 抓包）

        入参:
          type: 关注类型 (customer/order)
          attention: 是否关注 (1=关注, 0=取消)
          businessId: 业务ID
        """
        url = f"{APP_KEY_ATTENTION_PREFIX}.do"
        payload = {"type": type, "attention": attention, "businessId": businessId}
        error_msg = kwargs.pop("error_msg", "设置/取消重点关注失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("AI确认重点关注")
    def ai_confirm_key_attention(self, attentionBo, appRole, operate, dataId, content,
                                  status_code=200, **kwargs):
        """AI确认重点关注（独立域名 smart.onlinecps.cn）

        入参:
          attentionBo: 关注业务对象 {businessIdList, type, attention, appRole}
          appRole: 应用角色
          operate: 是否操作
          dataId: 数据ID
          content: 内容
        """
        payload = {
            "attentionBo": attentionBo,
            "appRole": appRole,
            "operate": operate,
            "dataId": dataId,
            "content": content,
        }
        error_msg = kwargs.pop("error_msg", "AI确认重点关注失败")
        payload.update(kwargs)
        # 使用完整 URL 请求独立域名
        return self.post(AI_KEY_ATTENTION_URL, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("获取订单列表")
    def get_today_order_list(self, orgId, supplierId, beginDate, endDate,
                             customerId="", isManage=False, pageDate="",
                             orderMarkList=None, status_code=200, **kwargs):
        """获取订单列表（APP 抓包）

        入参:
          orgId: 组织ID
          supplierId: 供应商ID
          beginDate: 开始日期 (yyyy-MM-dd 或 yyyy-M)
          endDate: 结束日期 (yyyy-MM-dd 或 yyyy-M)
          customerId: 客户ID（可选）
          isManage: 是否管理员视角
          pageDate: 分页日期
          orderMarkList: 订单标记列表
        """
        url = "/djsupplier/app/djcockpit/easyorder/salesman/getTodayOrderList.do"
        payload = {
            "orgId": orgId,
            "supplierId": supplierId,
            "beginDate": beginDate,
            "endDate": endDate,
            "customerId": customerId,
            "isManage": isManage,
            "pageDate": pageDate,
            "orderMarkList": orderMarkList or [],
        }
        error_msg = kwargs.pop("error_msg", "获取订单列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
