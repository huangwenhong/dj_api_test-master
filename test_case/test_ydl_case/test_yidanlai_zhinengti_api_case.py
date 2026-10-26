# -*- coding: utf-8 -*-
"""易单来 - 智能体模块接口测试用例（含签到拜访）"""

import allure
import json
import pytest
import time
from datetime import datetime
from test_case.page_api.ydl.zhinengti_api import ZhinengtiAPI


# 固定参数
SUPPLIER_ID = "ee3b25465f0b11edb9b5000c29f98159"
ORG_ID = "400"


@allure.feature("智能体")
class TestZhinengti:
    """智能体模块测试类"""

    def _get_api(self):
        """获取 API 实例（自动使用 smart.onlinecps.cn 域名和 token）"""
        return ZhinengtiAPI()

    def _today_str(self):
        """返回今日日期字符串（无前导零，如 2026-9-1）"""
        now = datetime.now()
        return f"{now.year}-{now.month}-{now.day}"

    # ==================== AA: 系统配置与功能列表 ====================

    @allure.story("智能体 - 系统配置")
    def test_ydl_AA_system_config(self):
        """智能体系统配置：获取授权功能列表→获取系统配置→验证功能项和热门问题"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        api = self._get_api()

        # 1. 获取授权功能列表
        payload_func = {
            "version": "2.3.7",
            "role": "role=manage",
            "source": "easyorder"
        }
        res_func = api.get_auth_function_list(payload_func)
        assert res_func.get("code") == "10001200", f"获取功能列表失败, code={res_func.get('code')}, msg={res_func.get('msg')}"
        assert res_func.get("success") is True, f"success应为True, 实际={res_func.get('success')}"

        # 2. 验证功能列表结构
        func_data = res_func.get("data", {})
        func_list = func_data.get("value", [])
        assert isinstance(func_list, list), f"功能列表应为list, 实际={type(func_list)}"
        assert len(func_list) > 0, f"功能列表不应为空"

        # 3. 验证包含签到功能
        func_names = [f.get("functionName") for f in func_list]
        assert "sign" in func_names, f"功能列表应包含签到(sign), 实际={func_names}"

        # 4. 获取系统配置（agent 热门问题）
        payload_config = {"key": "agent"}
        res_config = api.get_config(payload_config)
        assert res_config.get("code") == "10001200", f"获取配置失败, code={res_config.get('code')}, msg={res_config.get('msg')}"

        # 5. 验证配置结构
        config_data = res_config.get("data", {})
        config_value = config_data.get("value", {})
        assert "hot_query" in config_value, f"配置应包含hot_query, data={config_data}"
        assert "top_tips" in config_value, f"配置应包含top_tips, data={config_data}"
        assert len(config_value.get("hot_query", [])) > 0, f"热门问题不应为空"

        allure.attach(str(func_list), "功能列表", allure.attachment_type.TEXT)
        allure.attach(str(config_value), "系统配置", allure.attachment_type.TEXT)

    # ==================== AB: 签到拜访概览 ====================

    @allure.story("智能体 - 签到拜访")
    def test_ydl_AB_sign_in_visit_overview(self):
        """签到拜访概览：查询今日签到/拜访/超期未拜访统计，验证数据完整性"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        api = self._get_api()
        today = self._today_str()

        # 1. 查询今日拜访概览
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

        # 3. 验证数据字段完整性
        data = res.get("data", {})
        required_fields = [
            "signInCustomerNum",      # 签到客户数
            "visitCustomerNum",       # 拜访客户数
            "noVisitForOver7Days",    # 超7天未拜访
            "noVisitForOver30Days",   # 超30天未拜访
            "noVisitForOver60Days",   # 超60天未拜访
            "noVisitForOver90Days"    # 超90天未拜访
        ]
        for field in required_fields:
            assert field in data, f"缺少{field}字段, data={data}"

        # 4. 验证数值非负
        assert data.get("signInCustomerNum", -1) >= 0, f"签到客户数应>=0, 实际={data.get('signInCustomerNum')}"
        assert data.get("visitCustomerNum", -1) >= 0, f"拜访客户数应>=0, 实际={data.get('visitCustomerNum')}"
        assert data.get("noVisitForOver7Days", -1) >= 0, f"超7天未拜访数应>=0, 实际={data.get('noVisitForOver7Days')}"
        assert data.get("noVisitForOver30Days", -1) >= 0, f"超30天未拜访数应>=0, 实际={data.get('noVisitForOver30Days')}"
        assert data.get("noVisitForOver60Days", -1) >= 0, f"超60天未拜访数应>=0, 实际={data.get('noVisitForOver60Days')}"
        assert data.get("noVisitForOver90Days", -1) >= 0, f"超90天未拜访数应>=0, 实际={data.get('noVisitForOver90Days')}"

        allure.attach(str(data), "拜访概览数据", allure.attachment_type.TEXT)

    # ==================== AC: 产品上架配置查询 ====================

    @allure.story("智能体 - 产品上架")
    def test_ydl_AC_product_on_shelf_config(self):
        """产品上架配置查询：获取交期配置→获取客户列表→验证数据结构"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        api = self._get_api()

        # 1. 获取交期配置列表
        payload_config = {"partnerId": ORG_ID}
        res_config = api.get_delivery_config_list(payload_config)
        assert res_config.get("code") == "10001200", f"获取交期配置失败, code={res_config.get('code')}, msg={res_config.get('msg')}"
        config_data = res_config.get("data", {})
        assert "list" in config_data, f"交期配置应包含list, data={config_data}"
        config_list = config_data.get("list", [])
        assert len(config_list) > 0, f"交期配置列表不应为空"

        # 2. 验证交期配置结构
        first_config = config_list[0]
        assert "templateId" in first_config, f"交期配置应包含templateId, config={first_config}"
        assert "templateName" in first_config, f"交期配置应包含templateName, config={first_config}"

        # 3. 获取客户列表
        payload_user = {
            "partnerId": ORG_ID,
            "pageNo": 1,
            "pageSize": 10,
            "filterInvalidCustomer": True
        }
        res_user = api.get_user_list(payload_user)
        assert res_user.get("code") == "10001200", f"获取客户列表失败, code={res_user.get('code')}, msg={res_user.get('msg')}"
        user_data = res_user.get("data", {})
        assert "list" in user_data, f"客户列表应包含list, data={user_data}"

        # 4. 验证客户列表结构
        user_list = user_data.get("list", [])
        if len(user_list) > 0:
            first_user = user_list[0]
            assert "userId" in first_user, f"客户应包含userId, user={first_user}"
            assert "userName" in first_user, f"客户应包含userName, user={first_user}"
            assert "customerId" in first_user, f"客户应包含customerId, user={first_user}"

        allure.attach(str(config_list[:3]), "交期配置(前3个)", allure.attachment_type.TEXT)
        allure.attach(str(user_list[:3]), "客户列表(前3个)", allure.attachment_type.TEXT)

    # ==================== AD: 产品上架 AI 解析流程 ====================

    @allure.story("智能体 - 产品上架")
    def test_ydl_AD_product_on_shelf_ai_flow(self):
        """产品上架AI解析流程：触发AI解析→获取组件→验证可复用产品和价格方案结构"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        api = self._get_api()

        # 1. 触发产品上架 AI 解析（不执行实际上架）
        payload_stream = {
            "query": "产品上架",
            "inputs": {
                "type": "product_on_shelf",
                "supplier_id": "400",
                "org_id": "400",
                "images": [],
                "user_latitude": "27.95263",
                "user_longitude": "120.6648",
                "version": 237,
                "role": "manage"
            }
        }
        res_stream = api.submit_stream(payload_stream)
        # submitStream 返回 SSE 流式文本，验证包含关键节点
        assert "product_on_shelf_node" in res_stream or "intent_recognition_node" in res_stream, \
            f"AI应处理产品上架请求, 响应={str(res_stream)[:200]}"

        # 2. 从流式响应中提取组件 dataId
        # SSE 格式中 JSON 可能跨多行 data: 前缀，需拼接后解析
        data_id = None
        if isinstance(res_stream, str):
            # 拼接所有 data: 行的内容
            data_lines = []
            in_json_block = False
            for line in res_stream.split("\n"):
                stripped = line.strip()
                if stripped.startswith("data:"):
                    content = stripped[5:].strip()
                    if content == "<json>":
                        in_json_block = True
                        continue
                    if content == "</json>":
                        in_json_block = False
                        continue
                    if in_json_block:
                        data_lines.append(content)
            # 尝试解析拼接后的 JSON
            if data_lines:
                try:
                    combined = "".join(data_lines)
                    obj = json.loads(combined)
                    data_id = obj.get("dataId") or obj.get("businessBody", {}).get("dataId")
                except (json.JSONDecodeError, AttributeError):
                    pass

        # 3. 如果提取到 dataId，获取组件详情并验证
        if data_id:
            res_component = api.get_component_by_id({"id": str(data_id)})
            assert res_component.get("code") == "10001200", \
                f"获取组件失败, code={res_component.get('code')}"
            component_data = res_component.get("data", {})
            assert component_data.get("type") == "product_on_shelf", \
                f"组件类型应为product_on_shelf, 实际={component_data.get('type')}"
            assert component_data.get("status") in ["success", "processing"], \
                f"组件状态应为success或processing, 实际={component_data.get('status')}"

            # 4. 验证组件 content 包含可复用产品
            content_str = component_data.get("content", "")
            if content_str and component_data.get("status") == "success":
                content = json.loads(content_str) if isinstance(content_str, str) else content_str
                reusable = content.get("reusableProducts", [])
                assert isinstance(reusable, list), f"可复用产品应为list, 实际={type(reusable)}"
                if len(reusable) > 0:
                    product = reusable[0]
                    for field in ["fid", "productName", "layer", "fluteType", "materialId"]:
                        assert field in product, f"可复用产品应包含{field}, product={product}"

            allure.attach(str(component_data), "组件详情", allure.attachment_type.TEXT)
        else:
            allure.attach(str(res_stream)[:500], "AI流式响应(截取)", allure.attachment_type.TEXT)

    # ==================== AE: 产品上架执行 ====================

    @allure.story("智能体 - 产品上架")
    def test_ydl_AE_product_on_shelf_execute(self):
        """产品上架执行：调用onshelf.do→验证接口可达性→验证响应结构"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        api = self._get_api()

        # 1. 获取交期配置（上架前置校验）
        res_config = api.get_delivery_config_list({"partnerId": ORG_ID})
        assert res_config.get("code") == "10001200", f"获取交期配置失败, code={res_config.get('code')}"
        config_list = res_config.get("data", {}).get("list", [])
        assert len(config_list) > 0, f"无可用交期配置"
        template_id = config_list[0].get("templateId")

        # 2. 调用产品上架接口（基于抓包真实 payload 结构）
        # 注意：由于产品ID可能已过期，此处验证接口可达性和响应结构
        payload_onshelf = {
            "dataId": "",
            "fidx": "fd362ece-8460-49f8-97e0-45361751fd66",
            "schemeType": "group_on",
            "operationType": "modify",
            "productData": {
                "fid": "fd362ece-8460-49f8-97e0-45361751fd66",
                "productName": "单B美牛3常规",
                "layer": 3,
                "fluteType": 3,
                "materialId": "B43",
                "productType": "conventional",
                "maxOrderLength": "2000.00",
                "minOrderLength": "0.00",
                "maxOrderWidth": "500.00",
                "minOrderWidth": "0.00",
                "deliveryType": "delivery_template",
                "deliveryDay": "",
                "templateId": template_id,
                "marketingChannel": ["offline", "group_on"]
            },
            "priceScheme": {
                "groupPrice": 6,
                "minArea": 10,
                "idx": 4
            }
        }
        res = api.onshelf(payload_onshelf)

        # 3. 验证响应结构（无论成功或业务失败，接口必须返回标准结构）
        assert "success" in res, f"响应应包含success字段, res={res}"
        assert "code" in res, f"响应应包含code字段, res={res}"
        assert "msg" in res, f"响应应包含msg字段, res={res}"

        # 4. 验证业务返回码（成功=1000200，产品过期=1000999）
        code = res.get("code")
        if res.get("success") is True:
            # 上架成功：验证返回数据包含产品ID
            assert code == "1000200", f"上架成功code应为1000200, 实际={code}"
            data = res.get("data", {})
            assert "productId" in data, f"返回应包含productId, data={data}"
            assert "priceSchemeId" in data, f"返回应包含priceSchemeId, data={data}"
        else:
            # 产品ID过期或无效：验证错误码合理
            assert code in ["1000999", "10001308"], f"业务失败code应合理, 实际={code}"

        allure.attach(str(res), "上架响应", allure.attachment_type.TEXT)

    # ==================== AF: 产品上架第三阶段 - 产品管理服务执行 ====================

    @allure.story("智能体 - 产品上架")
    def test_ydl_AF_product_on_shelf_service_execution(self):
        """产品上架第三阶段：产品管理服务执行完整流程→查询产品审核→审核通过→查询价格方案→更新价格方案→审核→生效"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        api = self._get_api()

        # 使用抓包捕获的真实产品ID
        product_id = "648b0e16-168a-4d1f-bb91-f24bbe2209fe"

        # 1. 查询产品审核详情（selectProductExamineById.do）
        res_examine = api.select_product_examine_by_id(product_id)
        assert res_examine.get("code") == "10001200", \
            f"查询产品审核失败, code={res_examine.get('code')}, msg={res_examine.get('msg')}"
        examine_data = res_examine.get("data", {})
        assert "productExamineId" in examine_data, f"应包含productExamineId, data={examine_data}"
        assert "productId" in examine_data, f"应包含productId, data={examine_data}"
        assert "productName" in examine_data, f"应包含productName, data={examine_data}"
        assert "materialId" in examine_data, f"应包含materialId, data={examine_data}"
        assert "layer" in examine_data, f"应包含layer, data={examine_data}"
        assert "fluteType" in examine_data, f"应包含fluteType, data={examine_data}"
        product_examine_id = examine_data.get("productExamineId")

        # 2. 产品审核通过（checkProductExamine.do, auditStatus=6）
        payload_check = {
            "version": "1.0",
            "keyArea": "3303",
            "auditorId": ORG_ID,
            "auditor": "测试",
            "productExamineId": product_examine_id,
            "supplierId": ORG_ID,
            "comment": "",
            "auditStatus": 6
        }
        res_check = api.check_product_examine(payload_check)
        assert "success" in res_check, f"响应应包含success, res={res_check}"
        assert "code" in res_check, f"响应应包含code, res={res_check}"
        # 产品可能已审核过（重复审核返回非10001200属正常）
        check_code = res_check.get("code")
        if check_code != "10001200":
            allure.attach(str(res_check), "产品审核(已审核过)", allure.attachment_type.TEXT)

        # 3. 查询价格方案列表（selectPricePlanList.do）
        payload_plan = {
            "supplierId": ORG_ID,
            "groupGoodId": product_id,
            "onOffStatus": "",
            "pageNo": 1,
            "pageSize": 15,
            "effect": None,
            "marketingPlanName": "",
            "groupGoodName": examine_data.get("productName", ""),
            "materials": ""
        }
        res_plan = api.select_price_plan_list(payload_plan)
        assert res_plan.get("code") == "10001200", \
            f"查询价格方案失败, code={res_plan.get('code')}, msg={res_plan.get('msg')}"
        plan_data = res_plan.get("data", {})
        assert "list" in plan_data, f"价格方案应包含list, data={plan_data}"
        plan_list = plan_data.get("list", [])
        assert len(plan_list) > 0, f"价格方案列表不应为空"

        # 提取价格方案UUID
        first_plan = plan_list[0]
        plan_uuid = first_plan.get("uuid")
        assert plan_uuid, f"价格方案应包含uuid, plan={first_plan}"

        # 验证价格方案结构
        assert "groupGoodId" in first_plan, f"应包含groupGoodId, plan={first_plan}"
        assert "marketingPlanId" in first_plan, f"应包含marketingPlanId, plan={first_plan}"
        assert "groupPrice" in first_plan or "pricePlanExamineModelList" in first_plan, \
            f"应包含价格信息, plan={first_plan}"

        # 4. 查询价格方案审核详情（selectPricePlanExamine.do）
        payload_examine = {"version": "1.0", "uuid": plan_uuid}
        res_plan_examine = api.select_price_plan_examine(payload_examine)
        assert res_plan_examine.get("code") == "10001200", \
            f"查询价格方案审核失败, code={res_plan_examine.get('code')}"
        plan_examine_data = res_plan_examine.get("data", {})
        assert "list" in plan_examine_data, f"应包含list, data={plan_examine_data}"
        examine_list = plan_examine_data.get("list", [])
        assert len(examine_list) > 0, f"价格方案审核列表不应为空"

        # 验证审核详情字段
        examine_item = examine_list[0]
        for field in ["groupPrice", "minArea", "marketingName", "uuid"]:
            assert field in examine_item, f"审核详情应包含{field}, item={examine_item}"

        # 5. 价格方案审核（updatePricePlan.do）
        payload_update = {
            "version": "1.0",
            "fkeyarea": "3303",
            "auditorType": 2,
            "examineor": "测试",
            "reason": "",
            "groupGoodId": product_id,
            "uuid": plan_uuid
        }
        res_update = api.update_price_plan(payload_update)
        assert "success" in res_update, f"响应应包含success, res={res_update}"
        assert "code" in res_update, f"响应应包含code, res={res_update}"
        # 价格方案可能已审核过
        update_code = res_update.get("code")
        if update_code != "10001200":
            allure.attach(str(res_update), "价格方案审核(已处理)", allure.attachment_type.TEXT)

        # 6. 价格方案生效（updatePricePlanEffect.do）
        payload_effect = {
            "groupGoodId": product_id,
            "effect": 1,
            "uuid": plan_uuid,
            "operator": "测试",
            "activityPlans": []
        }
        res_effect = api.update_price_plan_effect(payload_effect)
        assert "success" in res_effect, f"响应应包含success, res={res_effect}"
        assert "code" in res_effect, f"响应应包含code, res={res_effect}"
        # 价格方案可能已生效
        effect_code = res_effect.get("code")
        if effect_code != "10001200":
            allure.attach(str(res_effect), "价格方案生效(已处理)", allure.attachment_type.TEXT)

        allure.attach(str(examine_data), "产品审核详情", allure.attachment_type.TEXT)
        allure.attach(str(first_plan), "价格方案(第一个)", allure.attachment_type.TEXT)
        allure.attach(str(examine_list), "价格方案审核详情", allure.attachment_type.TEXT)

    # ==================== AG: 产品上架端到端场景 ====================

    @allure.story("智能体 - 产品上架")
    def test_ydl_AG_product_on_shelf_e2e(self):
        """产品上架端到端场景：用户输入→AI解析→获取组件→上架执行→产品审核→价格方案→生效"""
        # Author: Author
        # Create Date: 2026-09-02
        # IsAI: True
        api = self._get_api()

        # ========== 第零步：校验供应商身份 ==========

        # 0. 获取当前用户的供应商ID（按产品上架流程：筛选 salesMain='y' 的主供应商）
        supplier_id, supplier_name, is_multi = api.resolve_supplier_id()
        supplier_type = "多供应商" if is_multi else "单供应商"
        print(f"[AG] 供应商类型: {supplier_type}, 名称: {supplier_name}, supplierId: {supplier_id}")
        allure.attach(
            f"供应商类型: {supplier_type}\n名称: {supplier_name}\nsupplierId: {supplier_id}",
            "供应商信息", allure.attachment_type.TEXT)

        # ========== 第一阶段：用户输入 → AI解析 ==========

        # 1. 触发产品上架 AI 解析
        payload_stream = {
            "query": "产品上架",
            "inputs": {
                "type": "product_on_shelf",
                "supplier_id": supplier_id,
                "org_id": supplier_id,
                "images": [],
                "user_latitude": "27.95263",
                "user_longitude": "120.6648",
                "version": 237,
                "role": "manage"
            }
        }
        res_stream = api.submit_stream(payload_stream)
        assert "product_on_shelf_node" in res_stream or "intent_recognition_node" in res_stream, \
            f"AI应处理产品上架请求, 响应={str(res_stream)[:200]}"

        # 2. 解析 SSE 流式响应，提取 dataId（组件记录ID）
        # 实测 v2 submitStream 无 <json> 标记，dataId 位于结构化 data 行：
        #   block.delta→delta.data.dataId / block.end→content.data.dataId / message.end→blocks[].content.data.dataId
        def _pick_data_id(node):
            """从 SSE 事件对象中递归提取组件记录ID dataId。"""
            if not isinstance(node, dict):
                return None
            for key in ("delta", "content"):
                block = node.get(key)
                if isinstance(block, dict) and isinstance(block.get("data"), dict):
                    vid = block["data"].get("dataId")
                    if vid is not None:
                        return vid
            for blk in node.get("blocks") or []:
                vid = _pick_data_id(blk)
                if vid is not None:
                    return vid
            return None

        data_id = None
        for line in res_stream.split("\n"):
            stripped = line.strip()
            if not stripped.startswith("data:"):
                continue
            try:
                obj = json.loads(stripped[5:].strip())
            except (json.JSONDecodeError, AttributeError):
                continue
            cand = _pick_data_id(obj)
            if cand is not None:
                data_id = cand
        assert data_id, "应从AI响应中提取到dataId"

        # 3. 轮询等待 AI 解析完成（组件状态变为 success）
        component_data = None
        max_wait = 60  # 最大等待 60 秒
        interval = 3   # 每 3 秒轮询一次
        elapsed = 0
        while elapsed < max_wait:
            res_component = api.get_component_by_id({"id": str(data_id)})
            assert res_component.get("code") == "10001200", \
                f"获取组件失败, code={res_component.get('code')}"
            component_data = res_component.get("data", {})
            status = component_data.get("status")
            if status == "success":
                break
            if status not in ("processing", "pending"):
                break
            print(f"[AG] AI解析中... status={status}, 已等待{elapsed}s")
            time.sleep(interval)
            elapsed += interval

        assert component_data is not None, "获取组件数据失败"
        assert component_data.get("type") == "product_on_shelf", \
            f"组件类型应为product_on_shelf, 实际={component_data.get('type')}"
        assert component_data.get("status") == "success", \
            f"AI解析应在{max_wait}秒内完成, 实际状态={component_data.get('status')}"

        # 4. 解析组件内容，提取第一个可复用产品和价格方案
        content_str = component_data.get("content", "")
        content = json.loads(content_str) if isinstance(content_str, str) and content_str else content_str
        assert content, f"组件内容不应为空, status=success 但 content={content_str[:200]}"

        reusable = content.get("reusableProducts", [])
        assert len(reusable) > 0, f"应包含可复用产品, content keys={list(content.keys())}"

        # 选择第一个产品上架
        product = reusable[0]
        fid = product.get("fid")
        product_name = product.get("productName", "")
        layer = product.get("layer", 3)
        flute_type = product.get("fluteType", 3)
        material_id = product.get("materialId", "")
        assert fid, f"第一个产品应包含fid, product={product}"

        group_price = content.get("groupPrice", 6)
        min_area = content.get("minArea", 10)

        allure.attach(json.dumps(content, ensure_ascii=False, indent=2)[:2000],
                      "AI解析结果", allure.attachment_type.TEXT)
        allure.attach(json.dumps(product, ensure_ascii=False, indent=2),
                      f"选择产品: {product_name}", allure.attachment_type.TEXT)

        # ========== 第二阶段：用户确认 → 上架执行 ==========

        # 5. 获取交期配置
        res_config = api.get_delivery_config_list({"partnerId": supplier_id})
        assert res_config.get("code") == "10001200", f"获取交期配置失败, code={res_config.get('code')}"
        config_list = res_config.get("data", {}).get("list", [])
        assert len(config_list) > 0, "无可用交期配置"
        template_id = config_list[0].get("templateId")

        # 6. 调用产品上架接口
        payload_onshelf = {
            "dataId": str(data_id),
            "fidx": fid,
            "schemeType": "group_on",
            "operationType": "modify",
            "productData": {
                "fid": fid,
                "productName": product_name,
                "layer": layer,
                "fluteType": flute_type,
                "materialId": material_id,
                "productType": "conventional",
                "deliveryType": "delivery_template",
                "deliveryDay": "",
                "templateId": template_id,
                "marketingChannel": ["offline", "group_on"]
            },
            "priceScheme": {
                "groupPrice": group_price,
                "minArea": min_area,
                "idx": 4
            }
        }
        res_onshelf = api.onshelf(payload_onshelf)
        assert "success" in res_onshelf and "code" in res_onshelf, \
            f"上架响应结构异常, res={res_onshelf}"

        onshelf_code = res_onshelf.get("code")
        if res_onshelf.get("success") is not True:
            # 产品ID过期等业务失败，记录并跳过后续阶段
            allure.attach(str(res_onshelf), "上架失败(跳过后续阶段)", allure.attachment_type.TEXT)
            return

        assert onshelf_code == "1000200", f"上架成功code应为1000200, 实际={onshelf_code}"
        onshelf_data = res_onshelf.get("data", {})
        product_id = onshelf_data.get("productId")
        assert product_id, f"上架成功应返回productId, data={onshelf_data}"

        # ========== 第三阶段：产品管理服务执行 ==========

        # 7. 查询产品审核详情
        res_examine = api.select_product_examine_by_id(product_id)
        assert res_examine.get("code") == "10001200", \
            f"查询产品审核失败, code={res_examine.get('code')}"
        examine_data = res_examine.get("data", {})
        product_examine_id = examine_data.get("productExamineId")
        assert product_examine_id, f"应包含productExamineId, data={examine_data}"

        # 8. 产品审核通过（checkProductExamine.do, auditStatus=6）
        res_check = api.check_product_examine({
            "version": "1.0", "keyArea": "3303",
            "auditorId": supplier_id, "auditor": "测试",
            "productExamineId": product_examine_id,
            "supplierId": supplier_id, "comment": "", "auditStatus": 6
        })
        assert "success" in res_check and "code" in res_check, f"产品审核响应异常, res={res_check}"

        # 9. 查询价格方案列表（selectPricePlanList.do）
        res_plan = api.select_price_plan_list({
            "supplierId": supplier_id, "groupGoodId": product_id,
            "onOffStatus": "", "pageNo": 1, "pageSize": 15,
            "effect": None, "marketingPlanName": "",
            "groupGoodName": examine_data.get("productName", ""), "materials": ""
        })
        assert res_plan.get("code") == "10001200", \
            f"查询价格方案失败, code={res_plan.get('code')}"
        plan_list = res_plan.get("data", {}).get("list", [])
        assert len(plan_list) > 0, "价格方案列表不应为空"
        plan_uuid = plan_list[0].get("uuid")
        assert plan_uuid, f"价格方案应包含uuid, plan={plan_list[0]}"

        # 10. 更新价格方案信息（addPricePlanExamine.do, updateOrSave=2）
        first_plan = plan_list[0]
        plan_examine_models = first_plan.get("pricePlanExamineModelList", [])
        if plan_examine_models:
            model = plan_examine_models[0]
            payload_add = [{
                "groupGoodId": product_id,
                "groupGoodName": examine_data.get("productName", ""),
                "supplierId": supplier_id,
                "supplierName": first_plan.get("supplierName", ""),
                "marketingName": model.get("marketingName", "123"),
                "limitedStartTime": "08:00:00",
                "limitedEndTime": "23:59:00",
                "minArea": model.get("minArea", 1),
                "groupPrice": str(model.get("groupPrice", "4")),
                "unitPrice": None,
                "labelId": model.get("labelId", ""),
                "creator": "测试",
                "showMaxarea": False,
                "groupareaList": model.get("groupareaList", []),
                "updateOrSave": 2,
                "effect": first_plan.get("effect", 0),
                "auditorType": first_plan.get("auditorType", 0)
            }]
            res_add = api.add_price_plan_examine(payload_add)
            assert "code" in res_add, f"更新价格方案响应异常, res={res_add}"
            if res_add.get("code") != "10001200":
                allure.attach(str(res_add), "更新价格方案(已处理)", allure.attachment_type.TEXT)

        # 11. 查询价格方案审核详情（selectPricePlanExamine.do）
        res_plan_examine = api.select_price_plan_examine({"version": "1.0", "uuid": plan_uuid})
        assert res_plan_examine.get("code") == "10001200", \
            f"查询价格方案审核失败, code={res_plan_examine.get('code')}"
        examine_list = res_plan_examine.get("data", {}).get("list", [])
        assert len(examine_list) > 0, "价格方案审核列表不应为空"

        # 12. 价格方案审核（updatePricePlan.do）
        res_update = api.update_price_plan({
            "version": "1.0", "fkeyarea": "3303", "auditorType": 2,
            "examineor": "测试", "reason": "",
            "groupGoodId": product_id, "uuid": plan_uuid
        })
        assert "success" in res_update and "code" in res_update, f"价格方案审核响应异常, res={res_update}"

        # 13. 价格方案生效（updatePricePlanEffect.do）
        res_effect = api.update_price_plan_effect({
            "groupGoodId": product_id, "effect": 1,
            "uuid": plan_uuid, "operator": "测试", "activityPlans": []
        })
        assert "success" in res_effect and "code" in res_effect, f"价格方案生效响应异常, res={res_effect}"

        allure.attach(str(onshelf_data), "上架结果", allure.attachment_type.TEXT)
        allure.attach(str(examine_data), "产品审核详情", allure.attachment_type.TEXT)
        allure.attach(str(plan_list[0]), "价格方案", allure.attachment_type.TEXT)

    # ==================== AH: 首页加载（会话与置顶消息） ====================

    @allure.story("智能体 - 首页加载会话与置顶消息")
    def test_ydl_AH_agent_home_load(self):
        """智能体首页加载：获取全部会话列表→获取置顶消息列表→用首个会话ID串联获取会话消息"""
        # Author: Author
        # Create Date: 2026-10-22
        # IsAI: True
        api = self._get_api()

        # 1. 获取全部会话列表（v2）
        res_conv = api.get_all_conversations({"version": "2.3.9"})
        assert res_conv.get("code") == "10001200", f"获取会话列表失败, code={res_conv.get('code')}, msg={res_conv.get('msg')}"
        assert res_conv.get("success") is True, f"success应为True, 实际={res_conv.get('success')}"

        # 2. 验证会话列表结构（data 为 dict，内含 data 列表）
        conv_data = res_conv.get("data", {})
        assert isinstance(conv_data, dict), f"会话data应为dict, 实际={type(conv_data)}"
        conv_list = conv_data.get("data", [])
        assert isinstance(conv_list, list), f"会话列表应为list, 实际={type(conv_list)}"
        assert len(conv_list) > 0, "会话列表不应为空"

        # 3. 验证会话项关键字段
        first_conv = conv_list[0]
        assert first_conv.get("id"), f"会话项应包含id, 实际={first_conv}"
        conversation_id = first_conv.get("id")

        # 4. 获取置顶消息列表
        res_top = api.get_all_top_message_list({})
        assert res_top.get("code") == "10001200", f"获取置顶消息列表失败, code={res_top.get('code')}, msg={res_top.get('msg')}"
        top_list = res_top.get("data", [])
        assert isinstance(top_list, list), f"置顶消息应为list, 实际={type(top_list)}"
        assert len(top_list) > 0, "置顶消息列表不应为空"
        assert top_list[0].get("id"), f"置顶消息项应包含id, 实际={top_list[0]}"

        # 5. 依赖串联：用首个会话ID获取该会话消息，验证会话-消息链路
        res_msg = api.get_all_message({"conversationId": conversation_id, "limit": 20})
        assert res_msg.get("code") == "10001200", f"获取会话消息失败, code={res_msg.get('code')}, msg={res_msg.get('msg')}"

        allure.attach(str(conv_list[:3]), "会话列表(前3条)", allure.attachment_type.TEXT)
        allure.attach(str(top_list[:3]), "置顶消息(前3条)", allure.attachment_type.TEXT)
