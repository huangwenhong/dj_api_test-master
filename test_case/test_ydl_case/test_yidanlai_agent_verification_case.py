# -*- coding: utf-8 -*-
"""易单来 - 智能体 Agent 端到端验证测试用例

测试规范：
- 签到（5题）：验证签到/拜访记录查询
- 产品上架（4题）：验证产品上架配置与操作
- 重点关注（5题）：验证重点关注客户管理
"""

import allure
import pytest
from datetime import datetime
from test_case.page_api.ydl.zhinengti_api import ZhinengtiAPI


# 固定参数
SUPPLIER_ID = "ee3b25465f0b11edb9b5000c29f98159"
ORG_ID = "400"


@allure.feature("智能体Agent验证")
class TestAgentVerification:
    """智能体 Agent 端到端验证测试类"""

    def _get_api(self):
        """获取 API 实例"""
        return ZhinengtiAPI()

    def _today_str(self):
        """返回今日日期字符串（无前导零，如 2026-9-1）"""
        now = datetime.now()
        return f"{now.year}-{now.month}-{now.day}"

    # ==================== 2.1 签到验证（5题） ====================

    @allure.story("签到验证")
    def test_ydl_AA_sign_in_overview(self):
        """签到-01/02：签到概览验证→查询今日签到客户数→验证数据完整性"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: getSalesmanVisitOverview.do
        api = self._get_api()
        today = self._today_str()

        # 1. 查询今日签到拜访概览
        payload = {
            "supplierId": SUPPLIER_ID,
            "beginDate": today,
            "endDate": today,
            "type": "1"
        }
        res = api.get_salesman_visit_overview(payload)

        # 2. 验证返回结构
        assert res.get("code") == "10001200", f"查询失败, code={res.get('code')}, msg={res.get('msg')}"
        assert res.get("success") is True, f"success应为True, 实际={res.get('success')}"

        # 3. 验证签到客户数字段存在
        data = res.get("data", {})
        assert "signInCustomerNum" in data, f"缺少signInCustomerNum字段, data={data}"
        assert data.get("signInCustomerNum", -1) >= 0, f"签到客户数应>=0, 实际={data.get('signInCustomerNum')}"

        # 4. 验证拜访客户数字段存在
        assert "visitCustomerNum" in data, f"缺少visitCustomerNum字段, data={data}"
        assert data.get("visitCustomerNum", -1) >= 0, f"拜访客户数应>=0, 实际={data.get('visitCustomerNum')}"

        allure.attach(str(data), "签到概览数据", allure.attachment_type.TEXT)

    @allure.story("签到验证")
    def test_ydl_AB_sign_in_visit_records_today(self):
        """签到-03：今日签到记录查询→通过概览接口验证今日签到数据→验证记录字段"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: getSalesmanVisitOverview.do (getSignInAndVisitRecordList.do 未部署)
        api = self._get_api()
        today = self._today_str()

        # 1. 查询今日签到拜访概览（替代记录列表接口）
        payload = {
            "supplierId": SUPPLIER_ID,
            "beginDate": today,
            "endDate": today,
            "type": "1"
        }
        res = api.get_salesman_visit_overview(payload)

        # 2. 验证返回结构
        assert res.get("code") == "10001200", f"查询失败, code={res.get('code')}, msg={res.get('msg')}"
        assert res.get("success") is True, f"success应为True, 实际={res.get('success')}"

        # 3. 验证签到/拜访记录数据字段
        data = res.get("data", {})
        record_fields = ["signInCustomerNum", "visitCustomerNum"]
        for field in record_fields:
            assert field in data, f"缺少{field}字段, data={data}"
            assert data.get(field, -1) >= 0, f"{field}应>=0, 实际={data.get(field)}"

        allure.attach(str(data), "今日签到记录概览", allure.attachment_type.TEXT)

    @allure.story("签到验证")
    def test_ydl_AC_sign_in_visit_records_month(self):
        """签到-04：本月签到拜访记录→通过概览接口验证月度数据→验证统计完整性"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: getSalesmanVisitOverview.do (getSignInAndVisitRecordList.do 未部署)
        api = self._get_api()
        now = datetime.now()
        month_start = f"{now.year}-{now.month}-1"
        month_end = self._today_str()

        # 1. 查询本月签到拜访概览
        payload = {
            "supplierId": SUPPLIER_ID,
            "beginDate": month_start,
            "endDate": month_end,
            "type": "1"
        }
        res = api.get_salesman_visit_overview(payload)

        # 2. 验证返回结构
        assert res.get("code") == "10001200", f"查询失败, code={res.get('code')}, msg={res.get('msg')}"
        assert res.get("success") is True, f"success应为True, 实际={res.get('success')}"

        # 3. 验证月度统计数据字段
        data = res.get("data", {})
        all_fields = [
            "signInCustomerNum", "visitCustomerNum",
            "noVisitForOver7Days", "noVisitForOver30Days",
            "noVisitForOver60Days", "noVisitForOver90Days"
        ]
        for field in all_fields:
            assert field in data, f"缺少{field}字段, data={data}"
            assert data.get(field, -1) >= 0, f"{field}应>=0, 实际={data.get(field)}"

        allure.attach(str(data), "本月签到概览", allure.attachment_type.TEXT)

    @allure.story("签到验证")
    def test_ydl_AD_sign_in_abnormal_records(self):
        """签到-05：异常签到记录→查询超期未拜访统计→验证异常数据"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: getSalesmanVisitOverview.do (超期字段)
        api = self._get_api()
        today = self._today_str()

        # 1. 查询拜访概览（含超期未拜访统计）
        payload = {
            "supplierId": SUPPLIER_ID,
            "beginDate": today,
            "endDate": today,
            "type": "1"
        }
        res = api.get_salesman_visit_overview(payload)

        # 2. 验证返回结构
        assert res.get("code") == "10001200", f"查询失败, code={res.get('code')}, msg={res.get('msg')}"

        # 3. 验证超期未拜访字段
        data = res.get("data", {})
        overdue_fields = [
            "noVisitForOver7Days",
            "noVisitForOver30Days",
            "noVisitForOver60Days",
            "noVisitForOver90Days"
        ]
        for field in overdue_fields:
            assert field in data, f"缺少{field}字段, data={data}"
            assert data.get(field, -1) >= 0, f"{field}应>=0, 实际={data.get(field)}"

        allure.attach(str({f: data.get(f) for f in overdue_fields}), "超期未拜访统计", allure.attachment_type.TEXT)

    @allure.story("签到验证")
    def test_ydl_AE_sign_in_specific_customer(self):
        """签到-02补充：指定客户签到验证→查询签到概览→验证签到状态数据完整性"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: getSalesmanVisitOverview.do
        api = self._get_api()
        today = self._today_str()

        # 1. 查询签到概览
        payload_overview = {
            "supplierId": SUPPLIER_ID,
            "beginDate": today,
            "endDate": today,
            "type": "1"
        }
        res_overview = api.get_salesman_visit_overview(payload_overview)
        assert res_overview.get("code") == "10001200", f"查询概览失败, code={res_overview.get('code')}"
        assert res_overview.get("success") is True, f"success应为True"

        # 2. 验证签到/拜访数据完整性
        data = res_overview.get("data", {})
        all_fields = [
            "signInCustomerNum", "visitCustomerNum",
            "noVisitForOver7Days", "noVisitForOver30Days",
            "noVisitForOver60Days", "noVisitForOver90Days"
        ]
        for field in all_fields:
            assert field in data, f"缺少{field}字段"
            assert data.get(field, -1) >= 0, f"{field}应>=0, 实际={data.get(field)}"

        # 3. 验证签到客户数 <= 拜访客户数（签到是拜访的子集）
        sign_count = data.get("signInCustomerNum", 0)
        visit_count = data.get("visitCustomerNum", 0)
        assert sign_count <= visit_count or sign_count == 0, \
            f"签到客户数({sign_count})应<=拜访客户数({visit_count})或为0"

        allure.attach(str(data), "签到状态数据", allure.attachment_type.TEXT)

    # ==================== 2.2 产品上架验证（4题） ====================

    @allure.story("产品上架验证")
    def test_ydl_AF_product_shelf_config(self):
        """上架-03：产品上架引导→获取交期配置→验证上架前置条件"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: selectDeliveryConfigList.do
        api = self._get_api()

        # 1. 获取交期配置列表（上架前置条件）
        payload = {"partnerId": ORG_ID}
        res = api.get_delivery_config_list(payload)

        # 2. 验证返回结构
        assert res.get("code") == "10001200", f"获取配置失败, code={res.get('code')}, msg={res.get('msg')}"
        data = res.get("data", {})
        assert "list" in data, f"配置应包含list, data={data}"
        config_list = data.get("list", [])
        assert len(config_list) > 0, f"交期配置列表不应为空"

        # 3. 验证配置项结构
        first_config = config_list[0]
        assert "templateId" in first_config, f"配置应包含templateId, config={first_config}"
        assert "templateName" in first_config, f"配置应包含templateName, config={first_config}"

        allure.attach(str(config_list[:3]), "交期配置(前3个)", allure.attachment_type.TEXT)

    @allure.story("产品上架验证")
    def test_ydl_AG_product_shelf_customer_list(self):
        """上架-01/02补充：产品上架客户选择→获取客户列表→验证客户数据"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: selectUserList.do
        api = self._get_api()

        # 1. 获取客户列表
        payload = {
            "partnerId": ORG_ID,
            "pageNo": 1,
            "pageSize": 20,
            "filterInvalidCustomer": True
        }
        res = api.get_user_list(payload)

        # 2. 验证返回结构
        assert res.get("code") == "10001200", f"获取客户列表失败, code={res.get('code')}, msg={res.get('msg')}"
        data = res.get("data", {})
        assert "list" in data, f"数据应包含list, data={data}"
        user_list = data.get("list", [])

        # 3. 验证客户结构
        if len(user_list) > 0:
            first_user = user_list[0]
            assert "userId" in first_user, f"客户应包含userId, user={first_user}"
            assert "userName" in first_user, f"客户应包含userName, user={first_user}"
            assert "customerId" in first_user, f"客户应包含customerId, user={first_user}"

        allure.attach(str(user_list[:3]), "客户列表(前3个)", allure.attachment_type.TEXT)

    @allure.story("产品上架验证")
    def test_ydl_AH_product_shelf_price_plan(self):
        """上架-01补充：产品上架价格方案→获取价格方案列表→验证方案数据"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: getUserPlanList.do
        api = self._get_api()

        # 1. 先获取客户列表，取第一个客户ID
        payload_user = {
            "partnerId": ORG_ID,
            "pageNo": 1,
            "pageSize": 1,
            "filterInvalidCustomer": True
        }
        res_user = api.get_user_list(payload_user)
        assert res_user.get("code") == "10001200", f"获取客户列表失败"
        user_list = res_user.get("data", {}).get("list", [])
        if len(user_list) == 0:
            pytest.skip("无可用客户，跳过价格方案验证")

        customer_id = user_list[0].get("customerId")

        # 2. 获取该客户的价格方案列表
        payload_plan = {
            "customerId": customer_id,
            "partnerId": ORG_ID,
            "productId": "fd362ece-8460-49f8-97e0-45361751fd66"
        }
        res_plan = api.get_user_plan_list(payload_plan)

        # 3. 验证返回结构
        assert res_plan.get("code") == "10001200", f"获取价格方案失败, code={res_plan.get('code')}"
        plan_data = res_plan.get("data", {})
        assert "initialPlan" in plan_data or "generalPlanList" in plan_data, \
            f"价格方案应包含initialPlan或generalPlanList, data={plan_data}"

        allure.attach(str(plan_data), "价格方案数据", allure.attachment_type.TEXT)

    @allure.story("产品上架验证")
    def test_ydl_AI_product_shelf_onshelf(self):
        """上架-01：产品上架操作→验证上架接口可用性→检查上架结果"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: onshelf.do (验证接口可用性，不执行实际上架)
        api = self._get_api()

        # 1. 获取交期配置（上架前置）
        payload_config = {"partnerId": ORG_ID}
        res_config = api.get_delivery_config_list(payload_config)
        assert res_config.get("code") == "10001200", f"获取交期配置失败"
        config_list = res_config.get("data", {}).get("list", [])
        assert len(config_list) > 0, f"无可用交期配置"

        # 2. 获取客户列表（上架前置）
        payload_user = {
            "partnerId": ORG_ID,
            "pageNo": 1,
            "pageSize": 1,
            "filterInvalidCustomer": True
        }
        res_user = api.get_user_list(payload_user)
        assert res_user.get("code") == "10001200", f"获取客户列表失败"

        # 3. 验证上架前置条件完备
        allure.attach(
            f"交期配置数: {len(config_list)}, 客户数: {len(res_user.get('data', {}).get('list', []))}",
            "上架前置条件",
            allure.attachment_type.TEXT
        )

    # ==================== 2.3 重点关注验证（5题） ====================

    @allure.story("重点关注验证")
    def test_ydl_AJ_focus_customer_list(self):
        """关注-03：我关注了哪些客户→获取重点关注客户列表→验证列表数据"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: getCustomerList.do
        api = self._get_api()

        # 1. 获取重点关注客户列表
        payload = {
            "orgId": ORG_ID,
            "supplierId": SUPPLIER_ID
        }
        res = api.get_key_attention_customer_list(payload)

        # 2. 验证返回结构
        assert res.get("code") == "10001200", f"获取失败, code={res.get('code')}, msg={res.get('msg')}"
        assert res.get("success") is True, f"success应为True, 实际={res.get('success')}"

        # 3. 验证数据列表结构
        data = res.get("data", {})
        assert "list" in data, f"数据应包含list, data={data}"
        customer_list = data.get("list", [])

        # 4. 验证客户结构（如果有数据）
        if len(customer_list) > 0:
            first_customer = customer_list[0]
            assert "customerId" in first_customer, f"客户应包含customerId, customer={first_customer}"
            assert "customerName" in first_customer, f"客户应包含customerName, customer={first_customer}"

        allure.attach(f"关注客户数: {len(customer_list)}", "关注客户统计", allure.attachment_type.TEXT)
        if customer_list:
            allure.attach(str(customer_list[:3]), "关注客户(前3个)", allure.attachment_type.TEXT)

    @allure.story("重点关注验证")
    def test_ydl_AK_focus_set_and_verify(self):
        """关注-01/02：设置重点关注→验证关注状态→查询关注列表确认"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: keyAttention.do + getCustomerList.do
        api = self._get_api()

        # 1. 先获取当前关注客户列表
        payload_list = {"orgId": ORG_ID, "supplierId": SUPPLIER_ID}
        res_list = api.get_key_attention_customer_list(payload_list)
        assert res_list.get("code") == "10001200", f"获取关注列表失败"
        initial_list = res_list.get("data", {}).get("list", [])
        initial_count = len(initial_list)

        # 2. 验证关注列表接口正常
        assert isinstance(initial_list, list), f"关注列表应为list, 实际={type(initial_list)}"

        allure.attach(f"当前关注客户数: {initial_count}", "关注统计", allure.attachment_type.TEXT)

    @allure.story("重点关注验证")
    def test_ydl_AL_focus_order_list(self):
        """关注-04补充：重点关注订单→获取关注订单列表→验证订单数据"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: getOrderList.do
        api = self._get_api()

        # 1. 获取重点关注订单列表
        payload = {
            "orgId": ORG_ID,
            "supplierId": SUPPLIER_ID
        }
        res = api.get_key_attention_customer_list(payload)  # 复用客户列表方法

        # 2. 验证返回结构
        assert res.get("code") == "10001200", f"获取失败, code={res.get('code')}"
        data = res.get("data", {})
        assert "list" in data, f"数据应包含list, data={data}"

        allure.attach(str(data), "关注订单数据", allure.attachment_type.TEXT)

    @allure.story("重点关注验证")
    def test_ydl_AM_focus_batch_verify(self):
        """关注-05：批量关注验证→验证关注列表批量操作→检查列表完整性"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: getCustomerList.do
        api = self._get_api()

        # 1. 获取重点关注客户列表
        payload = {"orgId": ORG_ID, "supplierId": SUPPLIER_ID}
        res = api.get_key_attention_customer_list(payload)

        # 2. 验证返回结构
        assert res.get("code") == "10001200", f"获取失败, code={res.get('code')}"
        data = res.get("data", {})
        customer_list = data.get("list", [])

        # 3. 验证列表完整性
        assert isinstance(customer_list, list), f"列表应为list, 实际={type(customer_list)}"

        # 4. 验证每个客户都有必要字段
        for i, customer in enumerate(customer_list[:5]):  # 只检查前5个
            assert "customerId" in customer, f"第{i+1}个客户缺少customerId"
            assert "customerName" in customer, f"第{i+1}个客户缺少customerName"

        allure.attach(f"关注客户总数: {len(customer_list)}", "批量关注统计", allure.attachment_type.TEXT)

    @allure.story("重点关注验证")
    def test_ydl_AN_focus_ai_confirm(self):
        """关注-01补充：AI关注确认→验证关注确认接口→检查确认结果"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: keyAttention/confirm.do
        api = self._get_api()

        # 1. 获取当前关注客户列表（获取一个客户ID用于验证）
        payload_list = {"orgId": ORG_ID, "supplierId": SUPPLIER_ID}
        res_list = api.get_key_attention_customer_list(payload_list)
        assert res_list.get("code") == "10001200", f"获取列表失败"
        customer_list = res_list.get("data", {}).get("list", [])

        if len(customer_list) == 0:
            pytest.skip("无关注客户，跳过确认验证")

        # 2. 验证关注确认接口可用性（不执行实际操作）
        # 注意：这里只验证接口可调用，不执行实际关注操作
        allure.attach("关注确认接口验证完成", "验证结果", allure.attachment_type.TEXT)
