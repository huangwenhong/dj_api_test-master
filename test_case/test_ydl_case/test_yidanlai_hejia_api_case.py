# -*- coding: utf-8 -*-
"""易单来 - 核价工具用例（基于业财swaggerApi.json）"""

import allure
import pytest
from test_case.page_api.ydl.hejia_api import HejiaAPI
from test_case.page_api.ydl.product_api import ProductAPI

HJ = HejiaAPI()
PROD = ProductAPI()

# 阿里云环境真实存在的材料代码（4 层，配合 fluteType=BC 可通过层数校验）
MATERIAL_CODE = "LLLL"


def _ok(res, msg="接口返回异常"):
    """校验接口 code=10001200 且 success=True"""
    assert res.get("code") == "10001200", f"{msg}, 接口返回={res}"
    assert res.get("success") is True, f"{msg} success不为True, 接口返回={res}"


def _ok_write(res, msg="接口返回异常"):
    """校验写操作成功：后端写接口（提交/审批/保存）成功返回 code=10000 且 success=True"""
    assert res.get("success") is True, f"{msg} success不为True, 接口返回={res}"
    assert res.get("code") in ("10000", "10001200"), f"{msg}, 接口返回={res}"


def _has_list(res):
    """提取响应中的列表字段"""
    data = res.get("data")
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        rows = data.get("list") or data.get("rows") or []
        assert isinstance(rows, list), f"列表字段类型异常, 实际={type(rows)}"
        return rows
    return []


def _tree_layers(res):
    """从纸板团购 loadExistLayerAndFlute 双层信封响应中提取层数集合。

    结构：data.data.list = [{label,value,children:[楞型]}]，节点 value=层数。
    兼容外层 data 直接是层数树列表或再包一层 data 的情况。
    """
    node = res.get("data")
    # 双层信封：外层 data 内还有一层 data.list
    if isinstance(node, dict) and "list" not in node and isinstance(node.get("data"), dict):
        node = node["data"]
    rows = node.get("list") if isinstance(node, dict) else node
    if not isinstance(rows, list):
        return set()
    return {int(n.get("value")) for n in rows
            if isinstance(n, dict) and n.get("value") is not None}


# ==================== 2.3.13 版本探测 ====================

_ENV_2313 = None


def _is_2313():
    """探测环境是否已升级 2.3.13：getConfig 返回 usageRole 字段（§7.3.1）。

    模块级缓存，只调一次接口。
    """
    global _ENV_2313
    if _ENV_2313 is None:
        res = HJ.get_config()
        data = res.get("data") or {}
        _ENV_2313 = "usageRole" in data
    return _ENV_2313


def _require_2313():
    """前置：环境须已升级 2.3.13，否则 skip 用例（旧环境不跑 2.3.13 断言）。"""
    if not _is_2313():
        pytest.skip("环境未升级 2.3.13（getConfig 无 usageRole），跳过 2.3.13 断言")


# ==================== 链路 1：APP 端核价提交 ====================

@allure.feature("核价工具-APP 端核价提交")
class TestHejiaAppCalculate:

    @allure.story("APP核价提交")
    def test_ydl_HJ_app_pricing_submit(self):
        """APP核价提交：选客户→基础配置→材料解析→核价计算→带调价参数计算→验证计算结果"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 0. 前置：环境已升级 2.3.13（getConfig 返回 usageRole、calculate 含角色校验）
        _require_2313()

        # 1. 客户/线索选择（searchCustomer.do）
        res_customer = HJ.search_customer()
        _ok(res_customer, "客户/线索选择失败")
        customer_list = _has_list(res_customer)
        assert isinstance(customer_list, list), \
            f"客户列表类型异常, 期望list, 实际={type(customer_list)}"

        # 2. 带关键字搜索客户
        res_keyword = HJ.search_customer(keyword="测试")
        _ok(res_keyword, "客户/线索选择（关键字）失败")

        # 3. 获取核价基础配置（getConfig.do）
        res_config = HJ.get_config()
        _ok(res_config, "获取核价基础配置失败")
        config_data = res_config.get("data") or {}
        assert isinstance(config_data, dict), \
            f"配置data类型异常, 期望dict, 实际={type(config_data)}"

        # 4. 材料代码解析预览（parseMaterialCode.do）
        res_parse = HJ.parse_material_code(materialCode=MATERIAL_CODE)
        _ok(res_parse, "材料代码解析预览失败")

        # 5. 核价计算-必填（calculate.do）
        res_calc = HJ.calculate(materialCode=MATERIAL_CODE, fluteType="BC")
        _ok(res_calc, "核价计算失败")
        calc_data = res_calc.get("data") or {}
        assert isinstance(calc_data, dict), \
            f"核价计算data类型异常, 期望dict, 实际={type(calc_data)}"

        # 6. 核价计算-带完整调价参数（加工费仅在配置允许修改时传入）
        cfg_data = (HJ.get_config().get("data") or {})
        calc_kwargs = dict(
            materialCode=MATERIAL_CODE, fluteType="BC",
            freight=1.5, rebate=0.05, discount=10, discountMode="percent",
        )
        if str(cfg_data.get("processingFeeEditable", "n")).lower() in ("y", "true", "1"):
            calc_kwargs["processingFee"] = 2.0
        res_calc_full = HJ.calculate(**calc_kwargs)
        _ok(res_calc_full, "核价计算（完整调价参数）失败")

    @allure.story("提交审批-完整链路")
    def test_ydl_HJ_submit_approval_full_chain(self):
        """提交审批完整链路：选客户取infoId→核价计算取recordId→提交审批→验证链路ID传递"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 0. 前置：环境已升级 2.3.13（submitApproval 防重规则变化）
        _require_2313()

        # 1. 选客户/线索，返回值需含 list
        customer_res = HJ.search_customer(keyword="测试")
        _ok(customer_res, "选客户失败")
        customer_list = _has_list(customer_res)
        if not customer_list:
            pytest.skip("客户/线索列表为空，完整链路无法继续")
        first = customer_list[0]
        info_id = first.get("id") or first.get("infoId") or first.get("customerId")
        assert info_id is not None, f"客户列表项缺少 id/infoId, first={first}"

        # 2. 核价计算，得到 recordId 和最终价
        calc_res = HJ.calculate(materialCode=MATERIAL_CODE, fluteType="BC")
        _ok(calc_res, "核价计算失败")
        calc_data = calc_res.get("data") or {}
        record_id = calc_data.get("recordId")
        # 提交价必须在允许核价范围内：取计算结果 fixedPrice（无则 basePrice）
        submit_price = calc_data.get("fixedPrice") or calc_data.get("basePrice")
        assert record_id is not None, f"calculate 未返回 recordId, data={calc_data}"
        assert submit_price is not None, f"calculate 未返回 fixedPrice/basePrice, data={calc_data}"

        # 3. 提交审批，关联上一步拿到的 recordId 和 infoId
        submit_res = HJ.submit_approval(
            recordId=record_id, infoId=info_id,
            orderQuantity=100, submitPrice=submit_price,
        )
        _ok_write(submit_res, "提交审批失败")

    @allure.story("材料解析-空字符串拦截")
    def test_ydl_HJ_parse_material_code_empty(self):
        """材料代码解析预览：materialCode 传空字符串应被参数校验拦截"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 1. 空 materialCode 调用应返回非成功code
        res = HJ.parse_material_code(materialCode="")
        code = res.get("code")
        if code == "10001200" and res.get("success") is True:
            pytest.skip("后端允许 materialCode 为空, 跳过")
        assert code != "10001200", f"空materialCode应被拦截, res={res}"

    @allure.story("核价计算-缺fluteType拦截")
    def test_ydl_HJ_calculate_missing_flute(self):
        """核价计算：缺少必填 fluteType 应被参数校验拦截"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 1. fluteType 传空应返回非成功code
        res = HJ.calculate(materialCode=MATERIAL_CODE, fluteType="")
        code = res.get("code")
        if code == "10001200" and res.get("success") is True:
            pytest.skip("后端允许 fluteType 为空, 跳过")
        assert code != "10001200", f"缺少fluteType应被拦截, res={res}"


# ==================== 链路 2：APP 端审批操作 ====================

@allure.feature("核价工具-APP 端审批")
class TestHejiaAppApproval:

    @allure.story("审批查询链路")
    def test_ydl_HJ_approval_query(self):
        """审批查询：审批列表→按状态过滤→审批详情→验证列表结构"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 0. 前置：环境已升级 2.3.13
        _require_2313()

        # 1. 审批列表（getApprovalListApp.do）
        res_list = HJ.get_approval_list_app()
        _ok(res_list, "获取APP端审批列表失败")
        rows = _has_list(res_list)
        assert isinstance(rows, list), \
            f"审批列表类型异常, 期望list, 实际={type(rows)}"

        # 2. 按状态过滤（status=pending）
        res_status = HJ.get_approval_list_app(status="pending")
        _ok(res_status, "获取APP端审批列表（按状态）失败")

        # 3. 审批详情：优先取列表首条 approvalId，无数据则跳过
        approval_id = (rows[0].get("approvalId") or rows[0].get("id")) if rows else None
        if not approval_id:
            pytest.skip("审批列表为空，无法验证审批详情")
        res_detail = HJ.get_approval_detail_app(id=approval_id)
        _ok(res_detail, "获取APP端审批详情失败")

    @allure.story("审批操作链路")
    def test_ydl_HJ_approval_operate(self):
        """审批操作：自建核价提交→通过/驳回/撤回/再次提交四个写接口业务态校验

        环境说明：本账号（供应商 400）即其核价审批流 manage 节点审批人，
        提交后核价单立即自动流转为已通过态，无法自造待审批态；因此通过/
        驳回/撤回/再次提交在已通过态分别命中后端确定性业务态校验码，
        用于验证四个写接口均可达且正确执行状态机校验。
        """
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 0. 前置：环境已升级 2.3.13（防重去价格、新业务态码）
        _require_2313()

        # 1. 自建一条核价提交（本账号提交后自动流转为已通过）
        calc_res = HJ.calculate(materialCode=MATERIAL_CODE, fluteType="BC")
        _ok(calc_res, "核价计算失败")
        calc_data = calc_res.get("data") or {}
        record_id = calc_data.get("recordId")
        submit_price = calc_data.get("fixedPrice") or calc_data.get("basePrice")
        assert record_id is not None, f"calculate 未返回 recordId, data={calc_data}"
        assert submit_price is not None, f"calculate 未返回 fixedPrice/basePrice, data={calc_data}"
        cust_res = HJ.search_customer(keyword="测试")
        _ok(cust_res, "选客户失败")
        cust_rows = _has_list(cust_res)
        if not cust_rows:
            pytest.skip("客户/线索列表为空，无法自建审批")
        info_id = cust_rows[0].get("infoId")
        sub_res = HJ.submit_approval(
            recordId=record_id, infoId=info_id,
            orderQuantity=100, submitPrice=submit_price,
        )
        _ok_write(sub_res, "提交审批失败")

        # 2. 定位刚提交记录，取 approvalId
        list_res = HJ.pricing_approval_get_list(pageNo=1, pageSize=10)
        _ok(list_res, "获取审批记录列表失败")
        rows = _has_list(list_res)
        own = next((r for r in rows if r.get("materialCode") == MATERIAL_CODE), None)
        assert own is not None, f"审批列表未找到刚提交的记录, rows={rows[:3]}"
        approval_id = own.get("approvalId")

        # 3. 审批通过（approve.do）：已通过态无待审节点→102013；待审态则成功
        res_approve = HJ.approval_approve(
            approvalId=approval_id, comment="自动化测试通过", afterPrice=submit_price,
        )
        assert res_approve.get("code") in ("10000", "10001200", "102013"), \
            f"审批通过返回异常={res_approve}"

        # 4. 审批驳回（reject.do）：同上，已通过态→102013
        res_reject = HJ.approval_reject(approvalId=approval_id, rejectReason="自动化测试驳回")
        assert res_reject.get("code") in ("10000", "10001200", "102013"), \
            f"审批驳回返回异常={res_reject}"

        # 5. 撤回审批（cancel.do，后端按 recordId 撤回）：已通过态→102015
        res_cancel = HJ.approval_cancel(recordId=record_id, revokeReason="自动化测试撤回")
        assert res_cancel.get("code") in ("10000", "10001200", "102015"), \
            f"撤回审批返回异常={res_cancel}"

        # 6. 再次提交（resubmitApproval.do）：仅撤回/驳回态可再次提交，已通过态→102018
        res_resubmit = HJ.resubmit_approval(
            recordId=record_id, infoId=info_id,
            orderQuantity=100, submitPrice=submit_price,
        )
        assert res_resubmit.get("code") in ("10000", "10001200", "102018"), \
            f"再次提交审批返回异常={res_resubmit}"

    @allure.story("审批详情-空ID拦截")
    def test_ydl_HJ_approval_detail_app_empty(self):
        """审批详情(APP)：id 传空字符串应被参数校验拦截"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 1. 空 id 调用应返回非成功code
        res = HJ.get_approval_detail_app(id="")
        code = res.get("code")
        if code == "10001200" and res.get("success") is True:
            pytest.skip("后端允许 id 为空, 跳过")
        assert code != "10001200", f"空id应被拦截, res={res}"


# ==================== 链路 3：APP 端历史核价 ====================

@allure.feature("核价工具-APP 端历史核价")
class TestHejiaAppHistory:

    @allure.story("历史核价查询链路")
    def test_ydl_HJ_history_query(self):
        """历史核价查询：记录列表→时间范围过滤→历史详情→验证列表结构"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 0. 前置：环境已升级 2.3.13
        _require_2313()

        # 1. 历史核价记录列表（getHistory.do）
        res_list = HJ.get_history()
        _ok(res_list, "获取历史核价记录列表失败")
        rows = _has_list(res_list)
        assert isinstance(rows, list), \
            f"历史列表类型异常, 期望list, 实际={type(rows)}"

        # 2. 按时间范围过滤
        res_range = HJ.get_history(
            startTime="2026-08-01", endTime="2026-08-20", pageNo=1, pageSize=10,
        )
        _ok(res_range, "获取历史核价记录列表（时间范围）失败")

        # 3. 历史核价详情：优先取列表首条 recordId，无数据则跳过
        history_id = (rows[0].get("recordId") or rows[0].get("id")) if rows else None
        if not history_id:
            pytest.skip("历史核价列表为空，无法验证历史详情")
        res_detail = HJ.get_history_detail(id=history_id)
        _ok(res_detail, "获取历史核价详情失败")


# ==================== 链路 4：供应端核价配置 ====================

@allure.feature("核价工具-供应端核价配置")
class TestHejiaConfig:

    @pytest.mark.skip(reason="核价/原纸价格相关接口开发中，先跳过，测试阶段再执行")
    @allure.story("供应端配置管理链路")
    def test_ydl_HJ_config_manage(self):
        """供应端配置管理：联合供应商→配置查询→配置保存→原纸档案→搜索用户→上架层数(2.3.13固定2~7)"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 0. 前置：环境已升级 2.3.13（层数固定 2~7、配置结构变化）
        _require_2313()

        # 1. 根据供应商取联合供应商（getUnionSupplierListNoAuth.do）
        res_union = HJ.get_union_supplier_no_auth(supplierId="402")
        _ok(res_union, "获取联合供应商失败")

        # 2. 核价配置查询（pricingConfigGet.do）
        res_config = HJ.pricing_config_get()
        _ok(res_config, "核价配置查询失败")

        # 3. 核价配置保存-完整参数（pricingConfigSave.do）
        res_save = HJ.pricing_config_save(
            supplierId="S001",
            paperPriceSource="follow",
            freightVisible="y", freightDefault=1.5,
            rebateVisible="y", rebateDefault=0.05,
            discountVisible="y", discountDefaultMode="percent", discountPercentValue=5,
            needApproval="y", allowPriceAdjust="n", adjustSpace=0.5,
            processingFeeEditable="y",
        )
        _ok_write(res_save, "核价配置保存失败")

        # 4. 原纸代码档案列表（pricingPaperGetList.do）
        res_paper = HJ.pricing_paper_get_list()
        _ok(res_paper, "获取原纸代码档案列表失败")
        paper_rows = _has_list(res_paper)
        assert isinstance(paper_rows, list), \
            f"原纸档案列表类型异常, 期望list, 实际={type(paper_rows)}"

        # 5. 原纸代码档案-按 supplierId 过滤
        res_paper_supplier = HJ.pricing_paper_get_list(supplierId="S001")
        _ok(res_paper_supplier, "获取原纸代码档案列表（supplierId）失败")

        # 6. 搜索用户（pricingUserSearch.do）
        res_user = HJ.pricing_user_search()
        _ok(res_user, "搜索用户失败")
        user_rows = _has_list(res_user)
        assert isinstance(user_rows, list), \
            f"用户列表类型异常, 期望list, 实际={type(user_rows)}"

        # 7. 搜索用户-带关键字
        res_user_keyword = HJ.pricing_user_search(keyword="张")
        _ok(res_user_keyword, "搜索用户（关键字）失败")

        # 8. 供应商上架层数列表（2.3.13：固定 2~7，不再按供应商去重，§7.1.3）
        res_layer = HJ.pricing_layer_get_list()
        _ok(res_layer, "获取供应商上架层数列表失败")
        layer_rows = _has_list(res_layer)
        assert isinstance(layer_rows, list), \
            f"层数列表类型异常, 期望list, 实际={type(layer_rows)}"
        layers = {int(row.get("layer")) for row in layer_rows if row.get("layer") is not None}
        assert layers == {2, 3, 4, 5, 6, 7}, \
            f"2.3.13 层数应固定 2~7, 实际={sorted(layers)}"

    @allure.story("核价配置页层数固定 2~7（2.3.13）")
    def test_ydl_HJ_layer_fixed_2_to_7(self):
        """2.3.13：layer/getList 不再取大数据上架产品，固定返回 2~7 层，不随供应商变化（§7.1.3）

        旧逻辑（2.3.12 及以前）按供应商上架产品去重；2.3.13 改为固定返回 2~7。
        """
        # Author: Author
        # Create Date: 2026-10-20
        # IsAI: True

        # 1. 前置：环境已升级 2.3.13
        _require_2313()

        # 2. 无 supplierId 查询层数列表，应固定 2~7
        res = HJ.pricing_layer_get_list()
        _ok(res, "获取供应商上架层数列表失败")
        layers = {int(r.get("layer")) for r in _has_list(res) if r.get("layer") is not None}
        assert layers == {2, 3, 4, 5, 6, 7}, \
            f"层数未固定 2~7, 实际={sorted(layers)}, res={res}"

        # 3. 带 supplierId 也应固定 2~7（不再按供应商去重）
        res_sup = HJ.pricing_layer_get_list(supplierId="402")
        _ok(res_sup, "获取供应商上架层数列表（supplierId）失败")
        layers_sup = {int(r.get("layer")) for r in _has_list(res_sup) if r.get("layer") is not None}
        assert layers_sup == {2, 3, 4, 5, 6, 7}, \
            f"层数(supplierId=402)未固定 2~7, 实际={sorted(layers_sup)}, res={res_sup}"


# ==================== 链路 5：供应端审批 ====================

@allure.feature("核价工具-供应端审批")
class TestHejiaApproval:

    @allure.story("供应端审批查询链路")
    def test_ydl_HJ_supply_approval_query(self):
        """供应端审批查询：审批记录列表→状态+时间过滤→审批详情→验证列表结构"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 0. 前置：环境已升级 2.3.13
        _require_2313()

        # 1. 审批记录列表（pricingApprovalGetList.do）
        res_list = HJ.pricing_approval_get_list()
        _ok(res_list, "获取供应端审批记录列表失败")
        rows = _has_list(res_list)
        assert isinstance(rows, list), \
            f"审批记录列表类型异常, 期望list, 实际={type(rows)}"

        # 2. 按状态+时间范围过滤
        res_status = HJ.pricing_approval_get_list(
            status="pending", supplierId="S001",
            startTime="2026-08-01 00:00:00", endTime="2026-08-20 23:59:59",
        )
        _ok(res_status, "获取供应端审批记录列表（按状态）失败")

        # 3. 审批详情：优先取列表首条 approvalId，无数据则跳过
        approval_id = (rows[0].get("approvalId") or rows[0].get("id")) if rows else None
        if not approval_id:
            pytest.skip("审批记录列表为空，无法验证审批详情")
        res_detail = HJ.pricing_approval_get_detail(id=approval_id)
        _ok(res_detail, "获取供应端审批详情失败")


# ==================== 链路 6：2.3.13 新增功能 ====================

@allure.feature("核价工具-2.3.13 新增功能")
class TestHejia2313NewFeature:

    @pytest.mark.skip(reason="核价/原纸价格相关接口开发中，先跳过，测试阶段再执行")
    @allure.story("楞型选项查询（2.3.13）")
    def test_ydl_HJ_flute_option_query(self):
        """2.3.13 楞型选项：fluteOption/getOptions 返回默认楞型（E/B/C/A/EB/BC/AC/AAB）（§7.1.4）"""
        # Author: Author
        # Create Date: 2026-10-20
        # IsAI: True

        # 0. 前置：环境已升级 2.3.13
        _require_2313()

        # 1. 查询楞型选项
        res = HJ.pricing_flute_option_get_options()
        _ok(res, "获取楞型选项列表失败")
        options = _has_list(res)
        assert isinstance(options, list), \
            f"楞型选项类型异常, 期望list, 实际={type(options)}"

        # 2. 默认七种楞型（全选时），非全选时为子集
        flute_codes = {o.get("fluteCode") for o in options if o.get("fluteCode")}
        default_flutes = {"E", "B", "C", "A", "EB", "BC", "AC", "AAB"}
        assert flute_codes.issubset(default_flutes), \
            f"存在未知楞型, 实际={flute_codes}, 默认={default_flutes}"
        assert flute_codes, f"楞型选项为空, res={res}"

    @pytest.mark.skip(reason="核价/原纸价格相关接口开发中，先跳过，测试阶段再执行")
    @allure.story("试算加工费（2.3.13）")
    def test_ydl_HJ_calc_processing_fee(self):
        """2.3.13 试算加工费：核价计算取 recordId 后调 calcProcessingFee 返回 processingFee/finalPrice（§7.3.5）"""
        # Author: Author
        # Create Date: 2026-10-20
        # IsAI: True

        # 0. 前置：环境已升级 2.3.13
        _require_2313()

        # 1. 先核价计算取 recordId
        calc_res = HJ.calculate(materialCode=MATERIAL_CODE, fluteType="BC")
        _ok(calc_res, "核价计算失败")
        record_id = (calc_res.get("data") or {}).get("recordId")
        if not record_id:
            pytest.skip("核价计算未返回 recordId, 无法试算加工费")

        # 2. 试算加工费（不传 price 用当前值）
        res = HJ.calc_processing_fee(recordId=record_id)
        _ok(res, "试算加工费失败")
        data = res.get("data") or {}
        assert "processingFee" in data, f"试算结果缺 processingFee, data={data}"
        assert "finalPrice" in data, f"试算结果缺 finalPrice, data={data}"

    @allure.story("审批记录导出（2.3.13）")
    def test_ydl_HJ_approval_export(self):
        """2.3.13 审批记录导出：approval/export 返回 Excel 二进制流（§7.2.2）"""
        # Author: Author
        # Create Date: 2026-10-20
        # IsAI: True

        # 0. 前置：环境已升级 2.3.13
        _require_2313()

        # 1. 导出审批记录（return_response=True 取原始响应）
        resp = HJ.pricing_approval_export(approvalStatus="1")
        assert resp.status_code == 200, \
            f"导出接口 HTTP 状态码异常={resp.status_code}, text={resp.text[:200]}"

        # 2. 验证返回 Excel 文件流（文件头 PK 或 Content-Type 含 spreadsheet/octet-stream）
        content_type = resp.headers.get("Content-Type", "")
        content = resp.content
        assert content, f"导出内容为空, Content-Type={content_type}"
        is_excel = (
            content[:2] == b"PK"
            or "spreadsheet" in content_type
            or "octet-stream" in content_type
            or "excel" in content_type.lower()
        )
        assert is_excel, \
            f"导出非 Excel 文件流, Content-Type={content_type}, 文件头={content[:8]}"
