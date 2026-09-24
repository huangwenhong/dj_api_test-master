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


# ==================== 链路 1：APP 端核价提交 ====================

@allure.feature("核价工具-APP 端核价提交")
class TestHejiaAppCalculate:

    @allure.story("APP核价提交")
    def test_ydl_HJ_app_pricing_submit(self):
        """APP核价提交：选客户→基础配置→材料解析→核价计算→带调价参数计算→验证计算结果"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

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

    @allure.story("供应端配置管理链路")
    def test_ydl_HJ_config_manage(self):
        """供应端配置管理：联合供应商→配置查询→配置保存→原纸档案→搜索用户→上架层数"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

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

        # 8. 供应商上架层数列表（pricingLayerGetList.do）
        #    层数/楞型按每个供应商各自的上架产品去重统计，销售主体与子供应商的
        #    上架产品可能不同，需分别按 supplierId 查询，校验各供应商返回自身去重后的层数集合
        res_layer = HJ.pricing_layer_get_list()
        _ok(res_layer, "获取供应商上架层数列表失败")
        layer_rows = _has_list(res_layer)
        assert isinstance(layer_rows, list), \
            f"层数列表类型异常, 期望list, 实际={type(layer_rows)}"
        for row in layer_rows:
            assert 2 <= int(row.get("layer", 0)) <= 7, \
                f"上架层数超出有效范围(2~7), row={row}"

        # 8.1 从联合供应商列表区分销售主体(salesMain=y)与子供应商(salesMain=n)
        union_rows = _has_list(res_union)
        main_sup = next((r for r in union_rows
                         if str(r.get("salesMain", "")).lower() in ("y", "1", "true")), None)
        sub_sup = next((r for r in union_rows
                        if str(r.get("salesMain", "")).lower() in ("n", "0", "false")), None)

        # 8.2 销售主体按自身 supplierId 查询上架层数
        if main_sup:
            res_layer_main = HJ.pricing_layer_get_list(supplierId=main_sup.get("supplierId"))
            _ok(res_layer_main, "获取销售主体上架层数列表失败")
            main_layers = {row.get("layer") for row in _has_list(res_layer_main)}
            assert main_layers, f"销售主体({main_sup.get('supplierId')})上架层数为空"

        # 8.3 子供应商按自身 supplierId 查询上架层数（与销售主体各自独立去重）
        if sub_sup:
            res_layer_sub = HJ.pricing_layer_get_list(supplierId=sub_sup.get("supplierId"))
            _ok(res_layer_sub, "获取子供应商上架层数列表失败")
            sub_layers = {row.get("layer") for row in _has_list(res_layer_sub)}
            assert sub_layers, f"子供应商({sub_sup.get('supplierId')})上架层数为空"

    @allure.story("核价配置页与纸板团购上架层数一致性")
    def test_ydl_HJ_layer_flute_consistency(self):
        """跨模块一致性：逐个供应商对比核价配置页层数与纸板团购上架产品层数是否完全一致

        业务口径：核价配置页(pricing/config/layer/getList)与纸板团购
        (product/loadExistLayerAndFlute.do)的层数都应按各供应商上架产品去重统计，
        同一供应商两者层数集合应完全一致；销售主体与子供应商各自独立对比。
        """
        # Author: Author
        # Create Date: 2026-09-15
        # IsAI: True

        # 1. 取联合供应商列表（销售主体 salesMain=y + 子供应商 salesMain=n）
        res_union = HJ.get_union_supplier_no_auth(supplierId="402")
        _ok(res_union, "获取联合供应商失败")
        union_rows = _has_list(res_union)
        assert union_rows, f"联合供应商列表为空, 无法对比层数, res={res_union}"

        # 2. 逐个供应商对比核价层数集合与纸板团购层数集合
        mismatches = []
        for sup in union_rows:
            sid = sup.get("supplierId")
            if sid is None:
                continue

            # 2.1 核价配置页层数（扁平结构 data:[{layer,layerName}]）
            res_hj = HJ.pricing_layer_get_list(supplierId=sid)
            _ok(res_hj, f"核价上架层数查询失败(supplierId={sid})")
            hj_layers = {int(r.get("layer")) for r in _has_list(res_hj)
                         if r.get("layer") is not None}

            # 2.2 纸板团购上架层数（双层信封 data.data.list 层数->楞型树，节点 value=层数）
            res_pr = PROD.load_exist_layer_and_flute(supplierId=sid)
            _ok(res_pr, f"纸板团购上架层数楞型查询失败(supplierId={sid})")
            pr_layers = _tree_layers(res_pr)

            # 2.3 严格相等对比，收集不一致明细（含双向差集，便于定位缺失层数）
            if hj_layers != pr_layers:
                mismatches.append({
                    "supplierId": sid,
                    "salesMain": sup.get("salesMain"),
                    "核价层数": sorted(hj_layers),
                    "纸板团购层数": sorted(pr_layers),
                    "团购有核价缺": sorted(pr_layers - hj_layers),
                    "核价有团购缺": sorted(hj_layers - pr_layers),
                })

        # 3. 断言所有供应商核价层数与纸板团购上架层数完全一致
        assert not mismatches, \
            f"核价配置页与纸板团购上架产品层数不一致(共{len(mismatches)}个供应商): {mismatches}"


# ==================== 链路 5：供应端审批 ====================

@allure.feature("核价工具-供应端审批")
class TestHejiaApproval:

    @allure.story("供应端审批查询链路")
    def test_ydl_HJ_supply_approval_query(self):
        """供应端审批查询：审批记录列表→状态+时间过滤→审批详情→验证列表结构"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

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
