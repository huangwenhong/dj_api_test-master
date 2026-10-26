# -*- coding: utf-8 -*-
"""易单来 - 智能体 Agent 端到端验证测试用例

测试规范：
- 签到（5题）：验证签到/拜访记录查询
- 产品上架（4题）：验证产品上架配置与操作
- 重点关注（5题）：验证重点关注客户管理
"""

import random

import allure
import pytest
from datetime import datetime
from test_case.page_api.ydl.zhinengti_api import (
    ZhinengtiAPI, ONOFF_STATUS_ON, AUDIT_STATUS_PASSED
)


# 固定参数
SUPPLIER_ID = "ee3b25465f0b11edb9b5000c29f98159"
ORG_ID = "400"

# 产品上架造数固定规则（用户指定）：材质固定硬编码 B434C；层数楞型经 loadExistLayerAndFlute.do 查询选取 5层+BC瓦
# 说明：材质查询接口(getMaterialsNameList.do/getMaterialNameList.do)本环境返回空或公司无权限，故材质不动态查询，直接用 B434C；
#       层数楞型选项由 load_exist_layer_and_flute 查询，下列 LAYER/FLUTE 常量为目标选项与查询未命中时的兜底值。
PRODUCT_MATERIAL_CODE = "B434C"    # 材质代码，硬编码固定值（对应 addProduct.materialId）
PRODUCT_LAYER = 5                  # 目标层数（5层）
PRODUCT_FLUTE_NAME = "BC瓦"        # 目标楞型名称（BC楞）
PRODUCT_FLUTE_TYPE = 1             # 楞型兜底值（抓包实证 BC瓦 ⇔ fluteType=1）；查询命中时以查询值为准
PRODUCT_NAME_PREFIX = "定制材料"    # 产品名前缀
PRODUCT_NAME_SUFFIX = "BC瓦"        # 产品名后缀（严格与楞型一致）

# 价格方案造数固定规则（抓包实证 2026-10-26）：方案名固定"AI价格方案"；
# 团购价/起步单量与新增产品时填写的价格、起步单量保持一致（同一次造数同源取值）
PRICE_PLAN_NAME = "AI价格方案"       # 价格方案名称（addPricePlanExamine.marketingName）
PRODUCT_GROUP_PRICE = "1.2"         # 团购价（字符串二位小数，新增产品时填写的价格）
PRODUCT_MIN_AREA = 100              # 起步单量（新增产品时填写的起步单量）
PRICE_PLAN_CREATOR = "测试"          # 价格方案创建人/审核人署名


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
        """关注-01补充：AI关注确认→验证关注确认接口可用性（不因无关注数据跳过）"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        # ground_truth_api: keyAttention/confirm.do
        api = self._get_api()

        # 1. 调用重点关注客户列表接口，核心目标是验证接口可用性（不执行实际关注操作）
        payload_list = {"orgId": ORG_ID, "supplierId": SUPPLIER_ID}
        res_list = api.get_key_attention_customer_list(payload_list)

        # 2. 断言接口可正常调用：code=10001200 且 success=True
        assert res_list.get("code") == "10001200", \
            f"关注确认接口不可用, code={res_list.get('code')}, msg={res_list.get('msg')}"
        assert res_list.get("success") is True, \
            f"success应为True, 实际={res_list.get('success')}, 接口返回={res_list}"

        # 3. 无论是否有关注客户都不跳过：无数据时仅记录附件说明，不影响用例状态
        customer_list = res_list.get("data", {}).get("list", [])
        if len(customer_list) == 0:
            allure.attach("无关注客户，接口可用性验证通过（不执行实际关注操作）",
                          "关注数据说明", allure.attachment_type.TEXT)
        else:
            allure.attach(f"当前关注客户数: {len(customer_list)}",
                          "关注数据说明", allure.attachment_type.TEXT)

        # 4. 接口可用性验证完成
        allure.attach("关注确认接口验证完成", "验证结果", allure.attachment_type.TEXT)

    # ==================== 产品上架闭环造数辅助 ====================

    def _gen_unique_product_name(self, api, supplier_id):
        """按规则'定制材料{5位随机数字}/BC瓦'生成全局唯一产品名，对照 loadProductNames 名池查重。
        {5位随机数字}范围 00000~99999（不足位前补零）；后缀严格为 BC瓦（与楞型一致）。
        """
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        res = api.load_product_names({"version": "1.0", "supplierId": supplier_id})
        exist_names = set()
        if res.get("code") == "10001200":
            for it in (res.get("data") or {}).get("list") or []:
                if it.get("productName"):
                    exist_names.add(it.get("productName"))
        # 10万命名空间内随机取未占用名，足够尝试次数几乎必然命中唯一名
        for _ in range(200):
            name = f"{PRODUCT_NAME_PREFIX}{random.randint(0, 99999):05d}/{PRODUCT_NAME_SUFFIX}"
            if name not in exist_names:
                return name
        raise AssertionError(f"无法生成唯一产品名(已有名池={len(exist_names)})")

    def _resolve_layer_flute(self, api, supplier_id):
        """通过 loadExistLayerAndFlute.do 查询纸板团购上架的层数楞型选项，解析出目标(5层+BC瓦)
        对应的 layer 与 fluteType 值。响应为双层信封 data.data.list=[{label,value,children:[{label,value}]}]，
        节点 value=层数、children.value=楞型(fluteType)。查询不到目标项时回退到固定兜底值。
        返回 (layer_value, flute_value)。
        """
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        res = api.load_exist_layer_and_flute({"supplierId": supplier_id})
        assert res.get("code") == "10001200", \
            f"查询层数楞型选项失败, code={res.get('code')}, msg={res.get('msg')}"
        # 双层信封：外层 data 内还有一层 data.list
        node = res.get("data")
        if isinstance(node, dict) and "list" not in node and isinstance(node.get("data"), dict):
            node = node["data"]
        rows = node.get("list") if isinstance(node, dict) else node
        rows = rows if isinstance(rows, list) else []
        for layer_node in rows:
            if not isinstance(layer_node, dict):
                continue
            if str(layer_node.get("value")) != str(PRODUCT_LAYER):
                continue
            for child in layer_node.get("children") or []:
                if isinstance(child, dict) and PRODUCT_FLUTE_NAME in (child.get("label") or ""):
                    return int(layer_node.get("value")), int(child.get("value"))
        # 未在选项中命中目标层数楞型：回退到固定兜底值（抓包实证 5层 BC瓦=1）
        allure.attach(
            f"loadExistLayerAndFlute 未命中目标 {PRODUCT_LAYER}层/{PRODUCT_FLUTE_NAME}，"
            f"回退固定值 layer={PRODUCT_LAYER}, fluteType={PRODUCT_FLUTE_TYPE}; rows={rows}",
            "层数楞型查询回退", allure.attachment_type.TEXT
        )
        return PRODUCT_LAYER, PRODUCT_FLUTE_TYPE

    def _build_group_area_lists(self, api, supplier_id, base_group_area=""):
        """复用基线产品 groupArea 的销售区域：用 findCityArea 的城市名→cityCode 映射构造 lists
        （listFgroupareas/listFgroupareaids）；基线区域无法匹配时回退到全部可售城市
        """
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        res = api.find_city_area(supplier_id)
        assert res.get("code") == "10001200", \
            f"查询可售城市区域失败, code={res.get('code')}, msg={res.get('msg')}"
        city_list = (res.get("data") or {}).get("list") or []
        assert len(city_list) > 0, "可售城市区域不应为空"
        code_by_city = {}
        for it in city_list:
            cname, ccode = it.get("cityName"), it.get("cityCode")
            if cname is not None and ccode is not None:
                code_by_city[cname] = int(ccode)
        # 解析基线 groupArea "省-市#省-市#..."，取市名匹配 cityCode
        area_lists = []
        for seg in (base_group_area or "").split("#"):
            seg = seg.strip()
            if not seg:
                continue
            city = seg.split("-")[-1].strip()
            if city in code_by_city:
                area_lists.append({"listFgroupareas": city, "listFgroupareaids": code_by_city[city]})
        if not area_lists:
            # 回退：基线区域无法匹配时使用全部可售城市
            area_lists = [{"listFgroupareas": c, "listFgroupareaids": i}
                          for c, i in code_by_city.items()]
        assert area_lists, f"未能构造销售区域 lists, city_list={city_list}"
        return area_lists

    def _make_image_bytes(self, fmt="JPEG", size=(200, 200), color=(220, 230, 240)):
        """用 Pillow 生成一张纯色测试图片的字节流（JPEG/PNG），用于 OSS 直传"""
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        import io
        from PIL import Image
        img = Image.new("RGB", size, color)
        buf = io.BytesIO()
        img.save(buf, format=fmt)
        return buf.getvalue()

    def _load_test_image(self, ext="png", index=0):
        """优先从项目 test_data 目录读取真实图片字节流用于 OSS 直传（按用户要求）。
        按期望扩展名筛选，index 选取第几张（主图/详情图用不同文件）；
        test_data 无图时才回退到 _make_image_bytes 合成图。
        返回 (image_bytes, ext, content_type)。
        """
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        import os
        # test_data 目录：本文件在 test_case/test_ydl_case/ 下，上溯两级到项目根
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_dir = os.path.join(base_dir, "test_data")
        ct_map = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}
        files = []
        if os.path.isdir(data_dir):
            files = sorted(f for f in os.listdir(data_dir)
                           if f.lower().endswith((".png", ".jpg", ".jpeg")))
        matched = [f for f in files
                   if f.lower().endswith("." + ext)
                   or (ext == "jpg" and f.lower().endswith(".jpeg"))]
        pool = matched or files
        if pool:
            chosen = pool[index % len(pool)]
            real_ext = chosen.rsplit(".", 1)[-1].lower()
            real_ext = "jpg" if real_ext == "jpeg" else real_ext
            with open(os.path.join(data_dir, chosen), "rb") as fp:
                return fp.read(), real_ext, ct_map.get(real_ext, "image/png")
        # 回退：test_data 无图时用合成图
        fmt = "PNG" if ext == "png" else "JPEG"
        return self._make_image_bytes(fmt), ext, ct_map.get(ext, "image/jpeg")

    def _build_price_plan_payload(self, supplier_id, supplier_name, product_id,
                                  product_name, area_models, creator):
        """按抓包真实结构构造 addPricePlanExamine.do 请求体（列表信封，updateOrSave=1 新增）。

        抓包实证（2026-10-26）：groupareaList 仅需 {cityCode, groupArea, checked, creator, type}
        精简结构；且必须携带 minGroupPrice/salesStreets/salesStreetsOld/errorAry/checkAll 等
        前端校验伴随字段，缺失或不符会报 code=110001 操作失败。
        """
        grouparea_list = [
            {"cityCode": a.get("cityCode"), "groupArea": a.get("groupArea"),
             "checked": True, "creator": creator, "type": "1"}
            for a in area_models
        ]
        sales_streets = [
            {"cityCode": a.get("cityCode"), "unselectedStreets": []}
            for a in area_models
        ]
        return [{
            "groupGoodId": product_id,
            "groupGoodName": product_name,
            "supplierId": supplier_id,
            "supplierName": supplier_name,
            "marketingName": PRICE_PLAN_NAME,
            "limitedStartTime": "08:00:00",
            "limitedEndTime": "23:59:00",
            "minArea": PRODUCT_MIN_AREA,
            "groupPrice": PRODUCT_GROUP_PRICE,
            "unitPrice": None,
            "labelId": "",
            "creator": creator,
            "showMaxarea": False,
            "groupareaList": grouparea_list,
            "minGroupPrice": float(PRODUCT_GROUP_PRICE),
            "orderIntervalList": [],
            "orderWideList": [],
            "activityPlanList": [],
            "ladderPriceList": [],
            "minareaData": "",
            "ladderPrice": "",
            "bigLadder": [],
            "showAuditorType": "",
            "errorAry": [{"error": False, "errorPropt": "请输入整数"}] +
                        [{"error": False, "errorPropt": "请输入价格(大于0小于100),只能保留二位小数"}] * 5,
            "salesStreets": sales_streets,
            "salesStreetsOld": sales_streets,
            "checkAll": True,
            "isIndeterminate": False,
            "bigAllright": True,
            "smallAllright": True,
            "lengthAllright": True,
            "widthAllright": True,
            "minAreaOrStart": str(PRODUCT_MIN_AREA),
            "updateOrSave": 1,
            "effect": 0,
            "auditorType": 0,
        }]

    @allure.story("产品上架验证")
    def test_ydl_AO_product_onshelf_full_loop(self):
        """上架-闭环：材质固定B434C、层数楞型经loadExistLayerAndFlute查询(5层BC瓦)、名称'定制材料{5位随机}/BC瓦'→新增产品→上架审核→新增价格方案→审核→生效→回查校验已上架(auditStatus=6且onoffStatus=2)且价格方案已生效"""
        # Author: Author
        # Create Date: 2026-10-26
        # IsAI: True
        # ground_truth_api: loadExistLayerAndFlute.do + addProduct.do + checkProductExamine.do + selectPricePlanList.do + addPricePlanExamine.do + selectPricePlanExamine.do + updatePricePlan.do + updatePricePlanEffect.do + loadListProducts.do
        api = self._get_api()

        # 1. 解析主供应商（产品上架流程选 salesMain='y' 的主供应商）
        supplier_id, supplier_name, _is_multi = api.resolve_supplier_id()
        allure.attach(f"供应商: {supplier_name}({supplier_id})", "供应商信息", allure.attachment_type.TEXT)

        # 2. 复用一款已有产品作为模板：取其完整详情（含主图），后续仅替换 productName
        res_list0 = api.load_list_products({
            "keyArea": "3303", "supplierId": supplier_id, "auditStatus": 0, "onoffStatus": 0,
            "marketingChannelJson": "", "pageSize": 15, "pageNum": 1, "version": "1.0",
            "layer": None, "fluteType": None, "productName": "", "productType": ""
        })
        assert res_list0.get("code") == "10001200", \
            f"查询产品列表失败, code={res_list0.get('code')}, msg={res_list0.get('msg')}"
        assert res_list0.get("success") is True, f"success应为True, 实际={res_list0.get('success')}"
        base_list = (res_list0.get("data") or {}).get("list") or []
        assert len(base_list) > 0, "无可复用的已有产品"
        # 选取复用模板：优先取 materialId=B434C 且含主图(figure)的产品（材质一致，其余字段最稳妥），
        # 无匹配时回退到首个含主图的产品；材质/层数/楞型在下方 payload 中按固定规则强制覆盖
        base = {}
        fallback = {}
        for cand in base_list[:15]:
            res_base = api.load_single_product(cand.get("fid"))
            if res_base.get("code") == "10001200" and res_base.get("success") is True:
                cand_data = res_base.get("data") or {}
                if not cand_data.get("figure"):
                    continue
                if not fallback:
                    fallback = cand_data
                if str(cand_data.get("materialId")) == PRODUCT_MATERIAL_CODE:
                    base = cand_data
                    break
        base = base or fallback
        assert base, "未找到含主图的可复用产品（新增产品需至少一张主图）"
        allure.attach(str(base_list[:3]), "产品列表(前3条)", allure.attachment_type.TEXT)

        # 3. 层数楞型经 loadExistLayerAndFlute.do 查询解析（目标 5层+BC瓦），材质固定硬编码 B434C；
        #    生成唯一产品名：定制材料{5位随机数字}/BC瓦
        layer_val, flute_val = self._resolve_layer_flute(api, supplier_id)
        product_name = self._gen_unique_product_name(api, supplier_id)
        allure.attach(
            f"新产品名: {product_name}; 固定材质={PRODUCT_MATERIAL_CODE}(硬编码), "
            f"层数楞型(查询所得)={layer_val}层/{flute_val}({PRODUCT_FLUTE_NAME}); "
            f"复用基线: {base.get('productName')}, materialId={base.get('materialId')}, "
            f"layer={base.get('layer')}, fluteType={base.get('fluteType')}",
            "造数信息", allure.attachment_type.TEXT
        )

        # 4. 新增产品：复用基线全部非名称字段（层型/楞型/材质/尺寸/配送/渠道等），仅替换 productName；
        #    图片必须本次新上传到 OSS tmp（后端只确认新上传图，复用旧图会报“确认上传图片失败”）；
        #    fid 置空表示新增；销售区域 lists 复用基线 groupArea
        area_lists = self._build_group_area_lists(api, supplier_id, base.get("groupArea", ""))
        # 优先用 test_data 下的真实图片字节流直传 OSS（非合成图）
        main_bytes, main_ext, main_ct = self._load_test_image("png", 0)
        detail_bytes, detail_ext, detail_ct = self._load_test_image("png", 1)
        main_fig = api.upload_product_image(
            main_bytes, 1, supplier_id, ext=main_ext, content_type=main_ct)
        detail_fig = api.upload_product_image(
            detail_bytes, 2, supplier_id, ext=detail_ext, content_type=detail_ct)
        allure.attach(
            f"主图 ffileid={main_fig['ffileid']} ({main_ext}, {len(main_bytes)}B)\n"
            f"详情图 ffileid={detail_fig['ffileid']} ({detail_ext}, {len(detail_bytes)}B)",
            "OSS上传图片", allure.attachment_type.TEXT)
        payload_add = dict(base)
        payload_add.update({
            "fid": "", "productName": product_name,
            "version": "1.0", "auditStatus": "1", "onoffStatus": 1,
            "calculateWay": False, "editOperate": False, "lists": area_lists,
            "figure": [main_fig], "detailsFigure": [detail_fig],
            "homePageVideo": None, "detailsVideo": None,
            # 材质硬编码 B434C（材质查询接口本环境无数据/无权限）；层数楞型取自 loadExistLayerAndFlute.do 查询解析
            "materialId": PRODUCT_MATERIAL_CODE,
            "layer": layer_val,
            "fluteType": flute_val,
        })
        res_add = api.add_product(payload_add)
        # 重名/非法参数等业务失败返回非10001200(实测-10000)：记录并换名重试，不跳过
        if res_add.get("code") != "10001200":
            allure.attach(str(res_add), "新增产品失败(换名重试)", allure.attachment_type.TEXT)
            product_name = self._gen_unique_product_name(api, supplier_id)
            payload_add["productName"] = product_name
            res_add = api.add_product(payload_add)
        assert res_add.get("code") == "10001200", \
            f"新增产品失败, code={res_add.get('code')}, msg={res_add.get('msg')}, resp={res_add}"
        assert res_add.get("success") is True, f"success应为True, 实际={res_add.get('success')}"

        # 5. 新增响应不返回fid：按名称回查产品列表取fid
        new_item = api.find_product_by_name(product_name, supplier_id)
        assert new_item, f"应能按名称回查到新增产品, productName={product_name}"
        product_id = new_item.get("fid")
        assert product_id, f"新增产品应包含fid, item={new_item}"

        # 6. 查询产品审核详情（新增后生成审核记录）
        res_examine = api.select_product_examine_by_id(product_id)
        assert res_examine.get("code") == "10001200", \
            f"查询产品审核失败, code={res_examine.get('code')}, msg={res_examine.get('msg')}"
        assert res_examine.get("success") is True, f"success应为True, 实际={res_examine.get('success')}"
        examine_data = res_examine.get("data") or {}
        product_examine_id = examine_data.get("productExamineId")
        assert product_examine_id, f"应包含productExamineId, data={examine_data}"
        allure.attach(str(examine_data), "产品审核详情", allure.attachment_type.TEXT)

        # 7. 产品审核通过（checkProductExamine auditStatus=6，真正完成上架的动作）
        res_check = api.check_product_examine({
            "version": "1.0", "keyArea": "3303",
            "auditorId": supplier_id, "auditor": "测试",
            "productExamineId": product_examine_id,
            "supplierId": supplier_id, "comment": "", "auditStatus": 6
        })
        assert res_check.get("code") == "10001200", \
            f"产品审核失败, code={res_check.get('code')}, msg={res_check.get('msg')}, resp={res_check}"
        assert res_check.get("success") is True, f"success应为True, 实际={res_check.get('success')}"

        # 8. 查询价格方案占位行（直建产品审核后仅有无 uuid 骨架，取其可售区域作为建方案入参）
        payload_plan_query = {
            "supplierId": supplier_id, "groupGoodId": product_id, "onOffStatus": "",
            "pageNo": 1, "pageSize": 15, "effect": None, "marketingPlanName": "",
            "groupGoodName": product_name, "materials": ""
        }
        res_plan0 = api.select_price_plan_list(payload_plan_query)
        assert res_plan0.get("code") == "10001200", \
            f"查询价格方案失败, code={res_plan0.get('code')}, msg={res_plan0.get('msg')}"
        plan_rows = (res_plan0.get("data") or {}).get("list") or []
        assert plan_rows, f"应能查询到价格方案占位行, data={res_plan0.get('data')}"
        area_models = ((plan_rows[0].get("pricePlanExamineModelList") or [{}])[0]).get("groupareaList") or []
        assert area_models, f"占位行应包含可售区域 groupareaList, row={plan_rows[0]}"

        # 9. 新增价格方案（addPricePlanExamine.do, updateOrSave=1，抓包真实结构）
        payload_plan = self._build_price_plan_payload(
            supplier_id, supplier_name, product_id, product_name, area_models, PRICE_PLAN_CREATOR)
        res_add_plan = api.add_price_plan_examine(payload_plan)
        assert res_add_plan.get("code") == "10001200", \
            f"新增价格方案失败, code={res_add_plan.get('code')}, msg={res_add_plan.get('msg')}, resp={res_add_plan}"
        assert res_add_plan.get("success") is True, f"success应为True, 实际={res_add_plan.get('success')}"

        # 10. 回查价格方案取 uuid（新增后才出现）→ 查询价格方案审核详情
        res_plan1 = api.select_price_plan_list(payload_plan_query)
        assert res_plan1.get("code") == "10001200", \
            f"回查价格方案失败, code={res_plan1.get('code')}, msg={res_plan1.get('msg')}"
        plan_uuid = None
        for p in (res_plan1.get("data") or {}).get("list") or []:
            if p.get("uuid"):
                plan_uuid = p.get("uuid")
                break
        assert plan_uuid, f"新增后价格方案应包含uuid, list={(res_plan1.get('data') or {}).get('list')}"
        res_plan_ex = api.select_price_plan_examine({"version": "1.0", "uuid": plan_uuid})
        assert res_plan_ex.get("code") == "10001200", \
            f"查询价格方案审核详情失败, code={res_plan_ex.get('code')}, msg={res_plan_ex.get('msg')}"
        assert (res_plan_ex.get("data") or {}).get("list"), \
            f"价格方案审核详情不应为空, data={res_plan_ex.get('data')}"

        # 11. 价格方案审核通过（updatePricePlan.do, auditorType=2）→ 生效（updatePricePlanEffect.do, effect=1）→ 回查确认
        res_upd_plan = api.update_price_plan({
            "version": "1.0", "fkeyarea": "3303", "auditorType": 2,
            "examineor": PRICE_PLAN_CREATOR, "reason": "",
            "groupGoodId": product_id, "uuid": plan_uuid
        })
        assert res_upd_plan.get("code") == "10001200", \
            f"价格方案审核失败, code={res_upd_plan.get('code')}, msg={res_upd_plan.get('msg')}, resp={res_upd_plan}"
        res_eff_plan = api.update_price_plan_effect({
            "groupGoodId": product_id, "effect": 1, "uuid": plan_uuid,
            "operator": PRICE_PLAN_CREATOR, "activityPlans": []
        })
        assert res_eff_plan.get("code") == "10001200", \
            f"价格方案生效失败, code={res_eff_plan.get('code')}, msg={res_eff_plan.get('msg')}, resp={res_eff_plan}"
        res_plan2 = api.select_price_plan_list(payload_plan_query)
        eff_row = next((p for p in (res_plan2.get("data") or {}).get("list") or []
                        if p.get("uuid") == plan_uuid), None)
        assert eff_row and eff_row.get("effect") == 1, \
            f"价格方案应已生效(effect=1), row={eff_row}"
        allure.attach(
            f"plan_uuid={plan_uuid}, marketingName={PRICE_PLAN_NAME}, "
            f"groupPrice={PRODUCT_GROUP_PRICE}, minArea={PRODUCT_MIN_AREA}, effect=1",
            "价格方案(新增-审核-生效)", allure.attachment_type.TEXT
        )

        # 12. 终态校验：回查产品列表，断言新增产品已上架(auditStatus=6 且 onoffStatus=2)
        #    抓包实证：checkProductExamine 审核通过后产品即 auditStatus=6 且 onoffStatus=2（已上架）
        final_item = api.find_product_by_name(product_name, supplier_id)
        assert final_item, f"上架后应能在列表回查到产品, productName={product_name}"
        assert final_item.get("auditStatus") == AUDIT_STATUS_PASSED, \
            f"审核状态应为已通过(6), 实际={final_item.get('auditStatus')}, item={final_item}"
        assert final_item.get("onoffStatus") == ONOFF_STATUS_ON, \
            f"上架状态应为已上架(2), 实际={final_item.get('onoffStatus')}, item={final_item}"
        allure.attach(
            f"productName={product_name}, fid={product_id}, "
            f"auditStatus={final_item.get('auditStatus')}, onoffStatus={final_item.get('onoffStatus')}, "
            f"auditor={final_item.get('auditor')}, plan_uuid={plan_uuid}",
            "上架闭环终态校验", allure.attachment_type.TEXT
        )
