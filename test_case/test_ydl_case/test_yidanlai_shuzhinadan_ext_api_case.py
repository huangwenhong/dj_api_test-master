# -*- coding: utf-8 -*-
"""易单来 - 数智拿单与营销活动模块接口用例（ydl1/test_ydl_case1 整合迁移版）

来源：由 test_ydl_case1/test_shuzhinadan_api.py 迁移；接口方法已合并至
test_case/page_api/ydl/ 下的 shuzhinadan_api 与 market_activity_api。
原产品详情页接口与看板同名方法冲突，迁移时统一改名为 get_product_detail_*；
v2.3.12 标签/预测相关用例（原 TestShuzhinadanV2312）依赖未定义的
v2312_client/v2312_data fixture，本次整合不纳入。

规范约定：
1. 前置条件直接写入各用例方法内，不在类级/模块级统一声明；
2. 仅编写正常成功流程的用例步骤，不单独编写异常分支用例；
3. 历史执行遇到的接口报错，错误原因与排查分析记录在对应步骤下方注释中，作为调试依据。
"""

import time
from datetime import datetime, timedelta

import allure
import pytest
from test_case.page_api.ydl.shuzhinadan_api import ShuzhinadanAPI
from test_case.page_api.ydl.market_activity_api import YdlAPI as MarketYdlAPI


shuzhinadan_api = ShuzhinadanAPI()
MK = MarketYdlAPI()

# 活动/策略名称最大长度（接口限制）
_MAX_NAME_LEN = 20


def _truncate_name(product_name, suffix):
    """按命名规范拼接名称，超长时截断产品名部分。"""
    max_product_len = _MAX_NAME_LEN - len(suffix)
    return product_name[:max_product_len] + suffix


@allure.feature("数智拿单")
class TestShuzhinadanBoardInit:

    @allure.story("作战看板 - 页面初始化选项链路")
    def test_ydl_AA_board_init_option_chain(self):
        """作战看板初始化：联合供应商→筛选方案→层数→产品→业务员→竞对→销售区域→策略产品选项"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 1. 前置内联：查询联合供应商选项，动态获取供应商信息（避免硬编码业务常量）
        # 报错记录(排查依据): 若返回 code=10001302 "用户未登录"，为 config.py default_cookies
        # 中 token 失效所致，重新获取有效 token 更新配置即可，非接口代码问题
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")
        supplier_name = union_rows[0].get("supplierName")
        assert supplier_id, "联合供应商选项行缺少 supplierId"

        # 2. 查询自有筛选方案
        res_scheme = shuzhinadan_api.get_own_filter_scheme()
        assert res_scheme.get("code") == "10001200", f"查询自有筛选方案, 接口异常{res_scheme}"
        assert isinstance(res_scheme.get("data", {}).get("list"), list)

        # 3. 查询在售产品层数选项
        res_layer = shuzhinadan_api.get_on_product_layer_list(supplierId=supplier_id)
        assert res_layer.get("code") == "10001200", f"查询在售产品层数选项, 接口异常{res_layer}"
        layer_rows = res_layer.get("data", {}).get("list", [])
        assert isinstance(layer_rows, list)
        if layer_rows:
            assert layer_rows[0].get("layerId"), f"层数选项行缺少 layerId, 接口异常{res_layer}"

        # 4. 查询产品列表选项
        res_product = shuzhinadan_api.get_product_list(supplierId=supplier_id)
        assert res_product.get("code") == "10001200", f"查询产品列表选项, 接口异常{res_product}"
        product_rows = res_product.get("data", {}).get("list", [])
        assert product_rows, f"产品列表为空, 接口异常{res_product}"
        assert product_rows[0].get("productId"), f"产品行缺少 productId, 接口异常{res_product}"

        # 5. 查询业务员列表
        res_salesman = shuzhinadan_api.get_salesman_list()
        assert res_salesman.get("code") == "10001200", f"查询业务员列表, 接口异常{res_salesman}"
        assert isinstance(res_salesman.get("data", {}).get("list"), list)

        # 6. 查询竞对档案列表
        res_rival = shuzhinadan_api.get_rival_archive()
        assert res_rival.get("code") == "10001200", f"查询竞对档案列表, 接口异常{res_rival}"
        assert isinstance(res_rival.get("data", {}).get("list"), list)

        # 7. 查询供应商销售区域
        res_region = shuzhinadan_api.get_supplier_sales_region(supplierId=supplier_id, supplierName=supplier_name)
        assert res_region.get("code") == "10001200", f"查询供应商销售区域, 接口异常{res_region}"
        region_rows = res_region.get("data", {}).get("list", [])
        assert isinstance(region_rows, list)
        if region_rows:
            assert "regionCode" in region_rows[0], f"销售区域行缺少 regionCode, 接口异常{res_region}"

        # 8. 查询策略产品下拉选项
        res_option = shuzhinadan_api.get_strategy_product_option(supplierId=supplier_id, supplierName=supplier_name)
        assert res_option.get("code") == "10001200", f"查询策略产品选项, 接口异常{res_option}"
        assert isinstance(res_option.get("data", {}).get("list"), list)

    @allure.story("作战看板 - KPI/数智摘要/接单趋势")
    def test_ydl_AB_board_kpi_summary_trend(self):
        """作战看板KPI：接单目标→利润目标→关注产品→数智摘要→接单趋势"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 前置内联：查询联合供应商选项，动态获取 supplierId/supplierName
        # 报错记录(排查依据): code=10001302 "用户未登录" = config.py token 失效，更新即可
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")
        supplier_name = union_rows[0].get("supplierName")

        # 1. 查询今日接单目标
        res_goal = shuzhinadan_api.get_order_goal(supplierId=supplier_id, supplierName=supplier_name)
        assert res_goal.get("code") == "10001200", f"查询今日接单目标, 接口异常{res_goal}"
        goal_data = res_goal.get("data", {})
        for key in ("todayGoal", "baseOrder", "opportunityOrders", "orderArea"):
            assert key in goal_data, f"接单目标缺少字段 {key}, 接口异常{res_goal}"

        # 2. 查询利润目标
        res_profit = shuzhinadan_api.get_profit_goal(supplierId=supplier_id, supplierName=supplier_name)
        assert res_profit.get("code") == "10001200", f"查询利润目标, 接口异常{res_profit}"
        profit_data = res_profit.get("data", {})
        for key in ("todayGoal", "baseProfit", "opportunityProfit", "profit"):
            assert key in profit_data, f"利润目标缺少字段 {key}, 接口异常{res_profit}"

        # 3. 查询关注产品数量
        res_focus = shuzhinadan_api.get_focus_product_count(supplierId=supplier_id, supplierName=supplier_name)
        assert res_focus.get("code") == "10001200", f"查询关注产品数量, 接口异常{res_focus}"
        focus_data = res_focus.get("data", {})
        assert isinstance(focus_data.get("productIdList"), list), f"关注产品ID列表结构异常{res_focus}"
        assert isinstance(focus_data.get("productCount"), int), f"关注产品数量结构异常{res_focus}"

        # 4. 查询数智摘要
        res_summary = shuzhinadan_api.get_intelligence_summary(supplierId=supplier_id, supplierName=supplier_name)
        assert res_summary.get("code") == "10001200", f"查询数智摘要, 接口异常{res_summary}"
        summary_data = res_summary.get("data", {})
        for key in ("summary", "gapProducts", "orderGaps", "progress"):
            assert key in summary_data, f"数智摘要缺少字段 {key}, 接口异常{res_summary}"

        # 5. 查询按时间接单趋势
        res_trend = shuzhinadan_api.get_order_trend_by_time(supplierId=supplier_id, supplierName=supplier_name)
        assert res_trend.get("code") == "10001200", f"查询接单趋势, 接口异常{res_trend}"
        trend_rows = res_trend.get("data", {}).get("list", [])
        assert isinstance(trend_rows, list)
        if trend_rows:
            assert "time" in trend_rows[0], f"接单趋势行缺少 time, 接口异常{res_trend}"
            assert "orderArea" in trend_rows[0], f"接单趋势行缺少 orderArea, 接口异常{res_trend}"

    @allure.story("作战看板 - 产品/客户策略清单")
    def test_ydl_AC_product_and_customer_strategy_list(self):
        """策略清单：关注产品ID→产品策略清单→客户策略清单→客户数量统计"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 前置内联：查询联合供应商选项，动态获取 supplierId/supplierName
        # 报错记录(排查依据): code=10001302 "用户未登录" = config.py token 失效，更新即可
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")
        supplier_name = union_rows[0].get("supplierName")

        # 1. 查询关注产品ID列表（产品策略清单的入参来源）
        res_focus = shuzhinadan_api.get_focus_product_count(supplierId=supplier_id, supplierName=supplier_name)
        assert res_focus.get("code") == "10001200", f"查询关注产品数量, 接口异常{res_focus}"
        product_ids = res_focus.get("data", {}).get("productIdList", [])
        assert isinstance(product_ids, list)

        # 2. 按关注产品ID分页查询产品策略清单
        res_ps = shuzhinadan_api.get_product_strategy(supplierId=supplier_id, supplierName=supplier_name,
                                         productIdList=product_ids)
        assert res_ps.get("code") == "10001200", f"分页查询产品策略清单, 接口异常{res_ps}"
        ps_data = res_ps.get("data", {})
        assert ps_data.get("total", -1) >= 0, f"产品策略清单 total 异常{res_ps}"
        ps_rows = ps_data.get("list", [])
        assert isinstance(ps_rows, list)
        for row in ps_rows:
            assert row.get("productId") in product_ids, \
                f"产品策略清单出现未关注产品 {row.get('productId')}, 期望范围{product_ids}"

        # 3. 分页查询客户策略清单
        res_cs = shuzhinadan_api.get_customer_strategy(supplierId=supplier_id, supplierName=supplier_name)
        assert res_cs.get("code") == "10001200", f"分页查询客户策略清单, 接口异常{res_cs}"
        assert res_cs.get("data", {}).get("total", -1) >= 0, f"客户策略清单 total 异常{res_cs}"
        assert isinstance(res_cs.get("data", {}).get("list"), list)

        # 4. 按首个关注产品查询客户数量统计
        assert product_ids, f"关注产品ID列表为空, 无法查询客户数量统计, 接口异常{res_focus}"
        res_count = shuzhinadan_api.get_customer_count(productId=product_ids[0],
                                          supplierId=supplier_id, supplierName=supplier_name)
        assert res_count.get("code") == "10001200", f"查询客户数量统计, 接口异常{res_count}"
        count_data = res_count.get("data", {})
        for key in ("opportunityCustomerCount", "baseOrderCustomerCount"):
            assert key in count_data, f"客户数量统计缺少字段 {key}, 接口异常{res_count}"


@allure.feature("数智拿单")
class TestShuzhinadanProductDetail:

    @allure.story("产品详情页 - 完整查询链路")
    def test_ydl_AA_product_detail_full_chain(self):
        """产品详情：产品选项→详情→客户数→销售趋势→成本分析→接单情况→客户销售清单"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 前置内联：查询联合供应商选项，动态获取 supplierId/supplierName
        # 报错记录(排查依据): code=10001302 "用户未登录" = config.py token 失效，更新即可
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")
        supplier_name = union_rows[0].get("supplierName")

        # 1. 查询关注产品，取第一个产品ID作为详情页入参
        res_focus = shuzhinadan_api.get_focus_product_count(supplierId=supplier_id, supplierName=supplier_name)
        assert res_focus.get("code") == "10001200", f"查询关注产品数量, 接口异常{res_focus}"
        product_ids = res_focus.get("data", {}).get("productIdList", [])
        assert product_ids, f"关注产品ID列表为空, 无法执行产品详情链路, 接口异常{res_focus}"
        product_id = product_ids[0]

        # 2. 查询产品详情选项，确认目标产品在选项中
        res_option = shuzhinadan_api.get_product_option(supplierId=supplier_id, supplierName=supplier_name)
        assert res_option.get("code") == "10001200", f"查询产品详情选项, 接口异常{res_option}"
        assert isinstance(res_option.get("data", {}).get("list"), list)

        # 3. 查询产品详情基础信息
        res_detail = shuzhinadan_api.get_product_detail_page(productId=product_id,
                                           supplierId=supplier_id, supplierName=supplier_name)
        assert res_detail.get("code") == "10001200", f"查询产品详情, 接口异常{res_detail}"
        detail = res_detail.get("data", {})
        assert detail.get("productId") == product_id, \
            f"产品详情ID不一致, 期望={product_id}, 实际={detail.get('productId')}, 接口异常{res_detail}"
        assert detail.get("productName"), f"产品详情缺少 productName, 接口异常{res_detail}"

        # 4. 查询该产品客户数量统计
        res_count = shuzhinadan_api.get_customer_count(productId=product_id,
                                          supplierId=supplier_id, supplierName=supplier_name)
        assert res_count.get("code") == "10001200", f"查询客户数量统计, 接口异常{res_count}"

        # 5. 查询产品销售趋势
        res_trend = shuzhinadan_api.get_product_detail_sales_trend(productId=product_id,
                                       supplierId=supplier_id, supplierName=supplier_name)
        assert res_trend.get("code") == "10001200", f"查询产品销售趋势, 接口异常{res_trend}"
        assert isinstance(res_trend.get("data", {}).get("list"), list)

        # 6. 查询产品成本分析
        res_cost = shuzhinadan_api.get_product_detail_cost_analysis(productId=product_id,
                                        supplierId=supplier_id, supplierName=supplier_name)
        assert res_cost.get("code") == "10001200", f"查询产品成本分析, 接口异常{res_cost}"
        cost_data = res_cost.get("data", {})
        for key in ("unitMarginalContribution", "discountUnitPrice", "unitProfit"):
            assert key in cost_data, f"成本分析缺少字段 {key}, 接口异常{res_cost}"

        # 7. 查询产品接单情况
        res_situation = shuzhinadan_api.get_product_detail_order_situation(productId=product_id,
                                               supplierId=supplier_id, supplierName=supplier_name)
        assert res_situation.get("code") == "10001200", f"查询产品接单情况, 接口异常{res_situation}"
        situation = res_situation.get("data", {})
        for key in ("goalArea", "goalDif", "orderArea"):
            assert key in situation, f"接单情况缺少字段 {key}, 接口异常{res_situation}"

        # 8. 分页查询产品客户销售清单
        res_sales = shuzhinadan_api.get_product_detail_customer_sales(productId=product_id,
                                          supplierId=supplier_id, supplierName=supplier_name)
        assert res_sales.get("code") == "10001200", f"分页查询产品客户销售清单, 接口异常{res_sales}"
        assert res_sales.get("data", {}).get("total", -1) >= 0, f"客户销售清单 total 异常{res_sales}"
        assert isinstance(res_sales.get("data", {}).get("list"), list)


@allure.feature("数智拿单")
class TestShuzhinadanSaleStrategy:

    @allure.story("策略配置 - 新增/查询/编辑/删除完整链路")
    def test_ydl_AA_strategy_crud_flow(self):
        """策略CRUD：新增→详情回显→编辑→详情验证→列表存在→删除→列表不存在"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 前置内联：查询联合供应商选项，动态获取 supplierId
        # 报错记录(排查依据): code=10001302 "用户未登录" = config.py token 失效，更新即可
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")

        # 前置内联：查询产品列表，动态获取产品名称用于构建策略名称
        res_product = shuzhinadan_api.get_product_list(supplierId=supplier_id)
        assert res_product.get("code") == "10001200", f"查询产品列表选项, 接口异常{res_product}"
        product_rows = res_product.get("data", {}).get("list", [])
        assert product_rows, f"产品列表为空, 无法构建策略名称, 接口异常{res_product}"
        product_name = product_rows[0].get("productName")
        assert product_name, f"产品行缺少 productName, 接口异常{res_product}"

        strategy_name = _truncate_name(product_name, "的策略")
        edited_name = _truncate_name(product_name, "的策略编辑")

        # 1. 新增销售策略（产品列表默认取抓包回放数据）
        res_add = shuzhinadan_api.add_sale_strategy(supplierId=supplier_id, strategyName=strategy_name, descr="ai自动化策略")
        assert res_add.get("code") == "10001200", f"新增销售策略, 接口异常{res_add}"
        assert res_add.get("success") is True, f"新增销售策略 success 异常{res_add}"
        strategy_id = res_add.get("data", {}).get("id")
        assert strategy_id, f"新增销售策略未返回策略ID, 接口异常{res_add}"

        # 2. 查询策略详情，验证名称回显
        res_get = shuzhinadan_api.get_sale_strategy(id=strategy_id)
        assert res_get.get("code") == "10001200", f"查询销售策略详情, 接口异常{res_get}"
        detail = res_get.get("data", {})
        assert detail.get("strategyName") == strategy_name, \
            f"策略名称回显不一致, 期望={strategy_name}, 实际={detail.get('strategyName')}"
        assert detail.get("productList"), f"策略详情产品列表为空, 接口异常{res_get}"

        # 3. 编辑策略名称
        res_edit = shuzhinadan_api.edit_sale_strategy(id=strategy_id, supplierId=supplier_id, strategyName=edited_name, descr="ai自动化编辑")
        assert res_edit.get("code") == "10001200", f"编辑销售策略, 接口异常{res_edit}"
        assert res_edit.get("success") is True, f"编辑销售策略 success 异常{res_edit}"

        # 4. 再次查询详情验证编辑生效
        res_after = shuzhinadan_api.get_sale_strategy(id=strategy_id)
        assert res_after.get("code") == "10001200", f"查询销售策略详情, 接口异常{res_after}"
        assert res_after.get("data", {}).get("strategyName") == edited_name, \
            f"策略名称未更新, 期望={edited_name}, 实际={res_after.get('data', {}).get('strategyName')}"

        # 5. 列表查询确认策略存在
        res_list = shuzhinadan_api.get_sale_strategy_list(supplierId=supplier_id, pageSize=50)
        assert res_list.get("code") == "10001200", f"分页查询销售策略列表, 接口异常{res_list}"
        list_ids = [row.get("id") for row in res_list.get("data", {}).get("list", [])]
        assert strategy_id in list_ids, f"新增策略未出现在列表中, 策略ID={strategy_id}, 列表={list_ids}"

        # 6. 删除策略
        res_del = shuzhinadan_api.delete_sale_strategy(id=strategy_id)
        assert res_del.get("code") == "10001200", f"删除销售策略, 接口异常{res_del}"
        assert res_del.get("success") is True, f"删除销售策略 success 异常{res_del}"

        # 7. 列表查询确认策略已删除
        res_list_after = shuzhinadan_api.get_sale_strategy_list(supplierId=supplier_id, pageSize=50)
        assert res_list_after.get("code") == "10001200", f"分页查询销售策略列表, 接口异常{res_list_after}"
        after_ids = [row.get("id") for row in res_list_after.get("data", {}).get("list", [])]
        assert strategy_id not in after_ids, f"删除后策略仍在列表中, 策略ID={strategy_id}"

    @allure.story("策略配置 - 导出")
    def test_ydl_AB_strategy_export(self):
        """策略导出：策略列表查询→按ID列表导出→导出结果核验"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 前置内联：查询联合供应商选项，动态获取 supplierId（迁移后 get_sale_strategy_list/export
        # 不再内置 supplierId="400" 默认值，改为显式传入，避免硬编码业务常量）
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")

        # 1. 查询列表取第一个策略ID
        res_list = shuzhinadan_api.get_sale_strategy_list(supplierId=supplier_id, pageSize=15)
        assert res_list.get("code") == "10001200", f"分页查询销售策略列表, 接口异常{res_list}"
        rows = res_list.get("data", {}).get("list", [])
        if not rows:
            pytest.skip("销售策略列表为空，跳过导出")

        # 2. 按ID导出（返回 Excel 文件，验证响应为二进制内容）
        res_export = shuzhinadan_api.export_sale_strategy(supplierId=supplier_id, ids=[rows[0].get("id")])
        assert res_export is not None, "导出销售策略无返回"
        assert res_export.status_code == 200, f"导出接口HTTP状态异常: {res_export.status_code}"
        # Excel 文件以 PK 开头（ZIP 格式）
        assert res_export.content[:2] == b"PK", f"导出内容非 Excel 文件, 前2字节={res_export.content[:2]}"


@allure.feature("数智拿单")
class TestShuzhinadanStrategyEffect:

    @allure.story("策略效果 - 总览/占比/漏斗/接单表现")
    def test_ydl_AA_strategy_effect_overview_chain(self):
        """效果分析：策略效果总览→产品策略总览→客户策略总览→分段占比→转化漏斗→产品接单表现"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 前置内联：查询联合供应商选项，动态获取 supplierId
        # 报错记录(排查依据): code=10001302 "用户未登录" = config.py token 失效，更新即可
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")
        start_date = time.strftime("%Y-%m-01")
        end_date = time.strftime("%Y-%m-%d")

        # 1. 查询策略效果总览
        res_overview = shuzhinadan_api.get_strategy_effect_overview(supplierId=supplier_id,
                                                       startDate=start_date, endDate=end_date)
        assert res_overview.get("code") == "10001200", f"查询策略效果总览, 接口异常{res_overview}"
        overview = res_overview.get("data", {})
        for key in ("totalStrategyCount", "productStrategyCount", "customerStrategyCount",
                    "strategyOrderVolume", "dayAvgArea"):
            assert key in overview, f"策略效果总览缺少字段 {key}, 接口异常{res_overview}"

        # 2. 查询产品策略效果总览
        res_product = shuzhinadan_api.get_product_strategy_effect_overview(supplierId=supplier_id,
                                                              startDate=start_date, endDate=end_date)
        assert res_product.get("code") == "10001200", f"查询产品策略效果总览, 接口异常{res_product}"
        product_data = res_product.get("data", {})
        for key in ("activityProductCount", "participantCustomerCount", "discountAmount",
                    "strategyOrderAmount"):
            assert key in product_data, f"产品策略效果总览缺少字段 {key}, 接口异常{res_product}"

        # 3. 查询客户策略效果总览
        res_customer = shuzhinadan_api.get_customer_strategy_effect_overview(supplierId=supplier_id,
                                                                startDate=start_date, endDate=end_date)
        assert res_customer.get("code") == "10001200", f"查询客户策略效果总览, 接口异常{res_customer}"
        customer_data = res_customer.get("data", {})
        for key in ("couponIssuedCount", "coveredCustomerCount", "orderCustomerCount", "couponUsedRate"):
            assert key in customer_data, f"客户策略效果总览缺少字段 {key}, 接口异常{res_customer}"

        # 4. 查询客户策略分段占比
        res_ratio = shuzhinadan_api.get_customer_strategy_segments_ratio(supplierId=supplier_id,
                                                            startDate=start_date, endDate=end_date)
        assert res_ratio.get("code") == "10001200", f"查询客户策略分段占比, 接口异常{res_ratio}"
        ratio_data = res_ratio.get("data", {})
        for key in ("baseOrderRatio", "opportunityOrderRatio", "otherOrderRatio", "totalOrder"):
            assert key in ratio_data, f"客户策略分段占比缺少字段 {key}, 接口异常{res_ratio}"

        # 5. 查询客户策略转化漏斗
        res_funnel = shuzhinadan_api.get_customer_strategy_conversion_funnel(supplierId=supplier_id,
                                                                startDate=start_date, endDate=end_date)
        assert res_funnel.get("code") == "10001200", f"查询客户策略转化漏斗, 接口异常{res_funnel}"
        funnel = res_funnel.get("data", {})
        for key in ("coverCustomerCount", "opportunityCustomerCount", "orderCustomerCount",
                    "reachRate", "conversionRate"):
            assert key in funnel, f"客户策略转化漏斗缺少字段 {key}, 接口异常{res_funnel}"

        # 6. 查询产品接单表现
        res_performance = shuzhinadan_api.get_product_order_performance(supplierId=supplier_id,
                                                           startDate=start_date, endDate=end_date)
        assert res_performance.get("code") == "10001200", f"查询产品接单表现, 接口异常{res_performance}"
        performance_rows = res_performance.get("data", {}).get("list", [])
        assert isinstance(performance_rows, list)
        for row in performance_rows:
            assert row.get("productId"), f"产品接单表现行缺少 productId, 接口异常{res_performance}"

    @allure.story("策略效果 - 策略维度接单情况")
    def test_ydl_AB_strategy_order_situation_chain(self):
        """策略维度：策略列表→活动产品选项→产品策略接单情况→策略活动列表"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 前置内联：查询联合供应商选项，动态获取 supplierId
        # 报错记录(排查依据): code=10001302 "用户未登录" = config.py token 失效，更新即可
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")

        # 1. 查询销售策略列表，取第一条策略ID
        res_list = shuzhinadan_api.get_sale_strategy_list(supplierId=supplier_id, pageSize=15)
        assert res_list.get("code") == "10001200", f"分页查询销售策略列表, 接口异常{res_list}"
        rows = res_list.get("data", {}).get("list", [])
        assert rows, f"销售策略列表为空, 无法执行策略维度查询, 接口异常{res_list}"
        strategy_id = rows[0].get("id")
        assert strategy_id, f"策略列表行缺少 id, 接口异常{res_list}"

        # 2. 查询策略下活动产品选项
        res_active = shuzhinadan_api.get_active_product(strategyId=strategy_id)
        assert res_active.get("code") == "10001200", f"查询策略下活动产品选项, 接口异常{res_active}"
        active_rows = res_active.get("data", {}).get("list", [])
        assert isinstance(active_rows, list)

        # 3. 分页查询产品策略接单情况
        res_situation = shuzhinadan_api.get_product_strategy_order_situation(
            strategyId=strategy_id,
            startDate=time.strftime("%Y-%m-01"),
            endDate=time.strftime("%Y-%m-%d"),
        )
        assert res_situation.get("code") == "10001200", f"分页查询产品策略接单情况, 接口异常{res_situation}"
        assert res_situation.get("data", {}).get("total", -1) >= 0, \
            f"产品策略接单情况 total 异常{res_situation}"
        assert isinstance(res_situation.get("data", {}).get("list"), list)

        # 4. 查询策略下营销活动列表
        res_activity = shuzhinadan_api.get_strategy_activity_list(strategyId=strategy_id, supplierId=supplier_id)
        assert res_activity.get("code") == "10001200", f"查询策略营销活动列表, 接口异常{res_activity}"
        activity_rows = res_activity.get("data", {}).get("list", [])
        assert isinstance(activity_rows, list)
        for row in activity_rows:
            assert row.get("marketActivityId"), \
                f"策略活动行缺少 marketActivityId, 接口异常{res_activity}"


@allure.feature("营销活动")
class TestShuzhinadanMarketingActivity:

    @allure.story("活动选品选项查询")
    def test_ydl_AA_activity_option_query_chain(self):
        """选品选项链路：产品名称→层数楞型→销售区域→团购产品列表"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 前置内联：查询联合供应商选项，动态获取 supplierId（避免硬编码业务常量）
        # 报错记录(排查依据): code=10001302 "用户未登录" = config.py token 失效，更新即可
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")

        # 前置内联：生成活动时间窗口（当前+10分钟 ~ +3小时，避开与存量活动时间冲突）
        start_time = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        end_time = (datetime.now() + timedelta(minutes=180)).strftime("%Y-%m-%d %H:%M:%S")

        # 1. 查询产品名称选项
        res_names = MK.find_product_names(supplierId=supplier_id)
        assert res_names.get("code") == "10001200", f"查询产品名称选项, 接口异常{res_names}"
        name_rows = res_names.get("data", {}).get("list", [])
        assert name_rows, f"产品名称选项为空, 接口异常{res_names}"
        assert name_rows[0].get("fid"), f"产品名称行缺少 fid, 接口异常{res_names}"
        assert name_rows[0].get("productName"), f"产品名称行缺少 productName, 接口异常{res_names}"

        # 2. 查询层数楞型选项（多层级嵌套结构）
        res_layer = MK.load_exist_layer_and_flute(supplierId=supplier_id)
        assert res_layer.get("code") == "10001200", f"查询层数楞型选项, 接口异常{res_layer}"
        layer_rows = res_layer.get("data", {}).get("list", [])
        assert layer_rows, f"层数楞型选项为空, 接口异常{res_layer}"
        assert layer_rows[0].get("label"), f"层数楞型行缺少 label, 接口异常{res_layer}"
        assert isinstance(layer_rows[0].get("children"), list), f"层数楞型行 children 结构异常{res_layer}"

        # 3. 查询供应商销售区域（省市区三级结构）
        res_area = MK.find_supplier_sales_area_list(supplierId=supplier_id)
        assert res_area.get("code") == "10001200", f"查询供应商销售区域, 接口异常{res_area}"
        area_rows = res_area.get("data", {}).get("list", [])
        assert area_rows, f"供应商销售区域为空, 接口异常{res_area}"
        assert area_rows[0].get("provinceCode"), f"销售区域行缺少 provinceCode, 接口异常{res_area}"
        assert isinstance(area_rows[0].get("saleAreaCityList"), list), \
            f"销售区域行 saleAreaCityList 结构异常{res_area}"

        # 4. 分页查询可参加团购活动的产品列表
        # 返回参数 ifChoose (Integer): 产品是否可选，0=可选，1=不可选
        res_group = MK.select_group_product_page_list(
            supplierId=supplier_id, activityStartTime=start_time, activityEndTime=end_time)
        assert res_group.get("code") == "10001200", f"分页查询团购产品列表, 接口异常{res_group}"
        group_data = res_group.get("data", {})
        assert group_data.get("total", -1) >= 0, f"团购产品列表 total 异常{res_group}"
        group_rows = group_data.get("list", [])
        assert group_rows, f"团购产品列表为空, 接口异常{res_group}"

    @allure.story("活动产品过滤")
    def test_ydl_AB_activity_product_filter(self):
        """活动产品过滤：团购产品→按活动时间窗口过滤已参与活动产品"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 前置内联：查询联合供应商选项，动态获取 supplierId
        # 报错记录(排查依据): code=10001302 "用户未登录" = config.py token 失效，更新即可
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")

        # 前置内联：生成活动时间窗口（当前+10分钟 ~ +3小时）
        start_time = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        end_time = (datetime.now() + timedelta(minutes=180)).strftime("%Y-%m-%d %H:%M:%S")

        # 1. 分页查询团购产品列表，取第一个产品UUID
        res_group = MK.select_group_product_page_list(
            supplierId=supplier_id, activityStartTime=start_time, activityEndTime=end_time)
        assert res_group.get("code") == "10001200", f"分页查询团购产品列表, 接口异常{res_group}"
        group_rows = res_group.get("data", {}).get("list", [])
        assert group_rows, f"团购产品列表为空, 无法执行活动产品过滤, 接口异常{res_group}"
        goods_id = group_rows[0].get("productId")
        assert goods_id, f"团购产品行缺少 productId, 接口异常{res_group}"

        # 2. 按活动时间窗口过滤已参与活动产品
        res_filter = MK.filter_activity_product(
            productIds=[goods_id], supplierId=supplier_id,
            activityStartTime=start_time, activityEndTime=end_time)
        assert res_filter.get("code") == "10001200", f"活动产品过滤, 接口异常{res_filter}"
        filter_ids = res_filter.get("data", {}).get("productIds", [])
        assert isinstance(filter_ids, list), f"活动产品过滤 productIds 结构异常{res_filter}"

    @allure.story("新增活动")
    def test_ydl_AC_activity_add(self):
        """新增活动：建策略挂载点→选品选区域→创建活动→列表回显→详情回显→清理"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 前置内联：查询联合供应商选项，动态获取 supplierId
        # 报错记录(排查依据): code=10001302 "用户未登录" = config.py token 失效，更新即可
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")

        # 前置内联：查询产品列表，动态获取产品名称用于构建策略和活动名称
        res_product = shuzhinadan_api.get_product_list(supplierId=supplier_id)
        assert res_product.get("code") == "10001200", f"查询产品列表选项, 接口异常{res_product}"
        product_rows = res_product.get("data", {}).get("list", [])
        assert product_rows, f"产品列表为空, 无法构建策略/活动名称, 接口异常{res_product}"
        product_name = product_rows[0].get("productName")
        assert product_name, f"产品行缺少 productName, 接口异常{res_product}"

        # 前置内联：生成活动时间窗口（当前+10分钟 ~ +3小时，避开与存量活动时间冲突）
        start_time = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        end_time = (datetime.now() + timedelta(minutes=180)).strftime("%Y-%m-%d %H:%M:%S")
        activity_name = _truncate_name(product_name, "满减")

        # 1. 前置选品：查询团购产品候选（正常流程要求有可选品数据）
        res_group = MK.select_group_product_page_list(
            supplierId=supplier_id, activityStartTime=start_time, activityEndTime=end_time)
        assert res_group.get("code") == "10001200", f"分页查询团购产品列表, 接口异常{res_group}"
        group_rows = res_group.get("data", {}).get("list", [])
        assert group_rows, f"团购产品列表为空, 无法创建活动, 接口异常{res_group}"

        # 2. 前置选区域：销售区域（省市区三级）取首个省/市下全部县区
        res_area = MK.find_supplier_sales_area_list(supplierId=supplier_id)
        assert res_area.get("code") == "10001200", f"查询供应商销售区域, 接口异常{res_area}"
        partner_areas = []
        for province in res_area.get("data", {}).get("list", []):
            for city in province.get("saleAreaCityList", []):
                for county in city.get("salesAreaCountyList", []):
                    partner_areas.append({
                        "provinceCode": province.get("provinceCode"),
                        "cityCode": city.get("cityCode"),
                        "countyCode": county.get("countyCode"),
                    })
                if partner_areas:
                    break
            if partner_areas:
                break
        assert partner_areas, f"供应商销售区域无县区数据, 无法创建活动, 接口异常{res_area}"

        # 3. 新增销售策略作为活动挂载点
        strategy_name = _truncate_name(product_name, "的策略")
        res_strategy = shuzhinadan_api.add_sale_strategy(supplierId=supplier_id,
                                            strategyName=strategy_name, descr="ai自动化活动链路")
        assert res_strategy.get("code") == "10001200", f"新增销售策略, 接口异常{res_strategy}"
        strategy_id = res_strategy.get("data", {}).get("id")
        assert strategy_id, f"新增销售策略未返回策略ID, 接口异常{res_strategy}"

        activity_id = None
        try:
            # 4. 策略下新增营销活动（逐个候选产品尝试直至成功）
            # 报错记录(排查依据):
            # 1) code=001 "所选产品已参与其他活动": 首个团购产品时间窗与存量活动冲突,
            #    属环境数据问题, 更换候选产品重试创建即可解决;
            # 2) code=11000020 "请勿快速点击,请等待2秒后操作!": 写接口防重复提交限流(2秒),
            #    重试前必须 time.sleep(2.5) 等待, 否则被限流直接拦截
            res_add = None
            goods_list = None
            for index, row in enumerate(group_rows[:5]):
                goods_id = row.get("productId")
                if not goods_id:
                    continue
                if index > 0:
                    time.sleep(2.5)
                goods_list = [{
                    "activityGoodsId": goods_id,
                    "partnerSalesAreaList": partner_areas,
                    "materialDiscountsList": [{"thresholdArea": "111", "unitPriceDiscount": 0.1}],
                }]
                res_add = shuzhinadan_api.add_strategy_activity(
                    strategyId=strategy_id,
                    supplierId=supplier_id,
                    marketingActivityName=activity_name,
                    activityStartTime=start_time,
                    activityEndTime=end_time,
                    activityGoodsList=goods_list,
                )
                if res_add.get("code") == "10001200":
                    activity_id = res_add.get("data", {}).get("activityId")
                    break
            assert activity_id, f"候选产品均创建策略营销活动失败, 最后一次接口异常{res_add}"

            # 5. 活动列表回显新活动
            res_list = shuzhinadan_api.get_strategy_activity_list(strategyId=strategy_id, supplierId=supplier_id)
            assert res_list.get("code") == "10001200", f"查询策略营销活动列表, 接口异常{res_list}"
            list_ids = [str(row.get("marketActivityId")) for row in res_list.get("data", {}).get("list", [])]
            assert str(activity_id) in list_ids, \
                f"新增活动未出现在列表中, 活动ID={activity_id}, 列表={list_ids}"

            # 6. 查询活动详情，验证名称与类型回显
            res_detail = MK.find_market_activity_details(marketActivityId=activity_id)
            assert res_detail.get("code") == "10001200", f"查询营销活动详情, 接口异常{res_detail}"
            detail = res_detail.get("data", {})
            assert detail.get("marketingActivityName") == activity_name, \
                f"活动名称回显不一致, 期望={activity_name}, 实际={detail.get('marketingActivityName')}"
            assert detail.get("activityType") == "according_area", \
                f"活动类型不一致, 期望=according_area, 实际={detail.get('activityType')}"
        finally:
            # 7. 清理临时活动与策略（清理失败不阻断用例）
            # 报错记录(排查依据): 清理写操作同样受 11000020 限流约束,
            # 删活动→删策略→后续步骤之间需 time.sleep(2.5) 等待
            if activity_id:
                shuzhinadan_api.delete_strategy_activity(activityId=activity_id, strategyId=strategy_id,
                                            status_code=0, error_msg="清理活动失败(不阻断用例)")
                time.sleep(2.5)
            shuzhinadan_api.delete_sale_strategy(id=strategy_id, status_code=0,
                                    error_msg="清理临时策略失败(不阻断用例)")
            time.sleep(2.5)

    @allure.story("编辑活动")
    def test_ydl_AD_activity_edit(self):
        """编辑活动：建策略→建活动→更新名称→详情验证更新生效→清理"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 前置内联：查询联合供应商选项，动态获取 supplierId
        # 报错记录(排查依据): code=10001302 "用户未登录" = config.py token 失效，更新即可
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")

        # 前置内联：查询产品列表，动态获取产品名称用于构建策略和活动名称
        res_product = shuzhinadan_api.get_product_list(supplierId=supplier_id)
        assert res_product.get("code") == "10001200", f"查询产品列表选项, 接口异常{res_product}"
        product_rows = res_product.get("data", {}).get("list", [])
        assert product_rows, f"产品列表为空, 无法构建策略/活动名称, 接口异常{res_product}"
        product_name = product_rows[0].get("productName")
        assert product_name, f"产品行缺少 productName, 接口异常{res_product}"

        # 前置内联：生成活动时间窗口（当前+10分钟 ~ +3小时，避开与存量活动时间冲突）
        start_time = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        end_time = (datetime.now() + timedelta(minutes=180)).strftime("%Y-%m-%d %H:%M:%S")
        activity_name = _truncate_name(product_name, "满减")
        edited_name = _truncate_name(product_name, "满减编辑")

        # 1. 前置选品：查询团购产品候选（正常流程要求有可选品数据）
        res_group = MK.select_group_product_page_list(
            supplierId=supplier_id, activityStartTime=start_time, activityEndTime=end_time)
        assert res_group.get("code") == "10001200", f"分页查询团购产品列表, 接口异常{res_group}"
        group_rows = res_group.get("data", {}).get("list", [])
        assert group_rows, f"团购产品列表为空, 无法创建活动, 接口异常{res_group}"

        # 2. 前置选区域：销售区域（省市区三级）取首个省/市下全部县区
        res_area = MK.find_supplier_sales_area_list(supplierId=supplier_id)
        assert res_area.get("code") == "10001200", f"查询供应商销售区域, 接口异常{res_area}"
        partner_areas = []
        for province in res_area.get("data", {}).get("list", []):
            for city in province.get("saleAreaCityList", []):
                for county in city.get("salesAreaCountyList", []):
                    partner_areas.append({
                        "provinceCode": province.get("provinceCode"),
                        "cityCode": city.get("cityCode"),
                        "countyCode": county.get("countyCode"),
                    })
                if partner_areas:
                    break
            if partner_areas:
                break
        assert partner_areas, f"供应商销售区域无县区数据, 无法创建活动, 接口异常{res_area}"

        # 3. 新增销售策略作为活动挂载点
        strategy_name = _truncate_name(product_name, "的策略")
        res_strategy = shuzhinadan_api.add_sale_strategy(supplierId=supplier_id,
                                            strategyName=strategy_name, descr="ai自动化活动链路")
        assert res_strategy.get("code") == "10001200", f"新增销售策略, 接口异常{res_strategy}"
        strategy_id = res_strategy.get("data", {}).get("id")
        assert strategy_id, f"新增销售策略未返回策略ID, 接口异常{res_strategy}"

        activity_id = None
        try:
            # 4. 策略下新增营销活动（逐个候选产品尝试直至成功）
            # 报错记录(排查依据):
            # 1) code=001 "所选产品已参与其他活动": 属环境数据问题, 更换候选产品重试;
            # 2) code=11000020 "请勿快速点击,请等待2秒后操作!": 写接口限流(2秒),
            #    重试前必须 time.sleep(2.5) 等待
            res_add = None
            goods_list = None
            for index, row in enumerate(group_rows[:5]):
                goods_id = row.get("productId")
                if not goods_id:
                    continue
                if index > 0:
                    time.sleep(2.5)
                goods_list = [{
                    "activityGoodsId": goods_id,
                    "partnerSalesAreaList": partner_areas,
                    "materialDiscountsList": [{"thresholdArea": "111", "unitPriceDiscount": 0.1}],
                }]
                res_add = shuzhinadan_api.add_strategy_activity(
                    strategyId=strategy_id,
                    supplierId=supplier_id,
                    marketingActivityName=activity_name,
                    activityStartTime=start_time,
                    activityEndTime=end_time,
                    activityGoodsList=goods_list,
                )
                if res_add.get("code") == "10001200":
                    activity_id = res_add.get("data", {}).get("activityId")
                    break
            assert activity_id, f"候选产品均创建策略营销活动失败, 最后一次接口异常{res_add}"

            # 5. 更新活动名称（编辑需回传完整活动商品列表）
            # 报错记录(排查依据): 更新也是写接口, 紧跟创建后直接调用会触发
            # code=11000020 限流, 执行前需 time.sleep(2.5) 等待
            time.sleep(2.5)
            res_update = MK.update_market_activity(
                id=activity_id,
                supplierId=supplier_id,
                strategyId=strategy_id,
                marketingActivityName=edited_name,
                activityStartTime=start_time,
                activityEndTime=end_time,
                activityGoodsList=goods_list,
            )
            assert res_update.get("code") == "10001200", f"更新营销活动, 接口异常{res_update}"
            assert res_update.get("success") is True, f"更新营销活动 success 异常{res_update}"

            # 6. 再次查询详情验证更新生效
            res_detail_after = MK.find_market_activity_details(marketActivityId=activity_id)
            assert res_detail_after.get("code") == "10001200", f"查询营销活动详情, 接口异常{res_detail_after}"
            assert res_detail_after.get("data", {}).get("marketingActivityName") == edited_name, \
                f"活动名称未更新, 期望={edited_name}, 实际={res_detail_after.get('data', {}).get('marketingActivityName')}"
        finally:
            # 7. 清理临时活动与策略（清理失败不阻断用例，写操作间需等待限流窗口）
            if activity_id:
                shuzhinadan_api.delete_strategy_activity(activityId=activity_id, strategyId=strategy_id,
                                            status_code=0, error_msg="清理活动失败(不阻断用例)")
                time.sleep(2.5)
            shuzhinadan_api.delete_sale_strategy(id=strategy_id, status_code=0,
                                    error_msg="清理临时策略失败(不阻断用例)")
            time.sleep(2.5)

    @allure.story("删除活动")
    def test_ydl_AE_activity_delete(self):
        """删除活动：建策略→建活动→删除活动→列表确认已删除→清理策略"""
        # Author: Author
        # Create Date: 2026-09-20
        # IsAI: True

        # 前置内联：查询联合供应商选项，动态获取 supplierId
        # 报错记录(排查依据): code=10001302 "用户未登录" = config.py token 失效，更新即可
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")

        # 前置内联：查询产品列表，动态获取产品名称用于构建策略和活动名称
        res_product = shuzhinadan_api.get_product_list(supplierId=supplier_id)
        assert res_product.get("code") == "10001200", f"查询产品列表选项, 接口异常{res_product}"
        product_rows = res_product.get("data", {}).get("list", [])
        assert product_rows, f"产品列表为空, 无法构建策略/活动名称, 接口异常{res_product}"
        product_name = product_rows[0].get("productName")
        assert product_name, f"产品行缺少 productName, 接口异常{res_product}"

        # 前置内联：生成活动时间窗口（当前+10分钟 ~ +3小时，避开与存量活动时间冲突）
        start_time = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        end_time = (datetime.now() + timedelta(minutes=180)).strftime("%Y-%m-%d %H:%M:%S")
        activity_name = _truncate_name(product_name, "满减")

        # 1. 前置选品：查询团购产品候选（正常流程要求有可选品数据）
        res_group = MK.select_group_product_page_list(
            supplierId=supplier_id, activityStartTime=start_time, activityEndTime=end_time)
        assert res_group.get("code") == "10001200", f"分页查询团购产品列表, 接口异常{res_group}"
        group_rows = res_group.get("data", {}).get("list", [])
        assert group_rows, f"团购产品列表为空, 无法创建活动, 接口异常{res_group}"

        # 2. 前置选区域：销售区域（省市区三级）取首个省/市下全部县区
        res_area = MK.find_supplier_sales_area_list(supplierId=supplier_id)
        assert res_area.get("code") == "10001200", f"查询供应商销售区域, 接口异常{res_area}"
        partner_areas = []
        for province in res_area.get("data", {}).get("list", []):
            for city in province.get("saleAreaCityList", []):
                for county in city.get("salesAreaCountyList", []):
                    partner_areas.append({
                        "provinceCode": province.get("provinceCode"),
                        "cityCode": city.get("cityCode"),
                        "countyCode": county.get("countyCode"),
                    })
                if partner_areas:
                    break
            if partner_areas:
                break
        assert partner_areas, f"供应商销售区域无县区数据, 无法创建活动, 接口异常{res_area}"

        # 3. 新增销售策略作为活动挂载点
        strategy_name = _truncate_name(product_name, "的策略")
        res_strategy = shuzhinadan_api.add_sale_strategy(supplierId=supplier_id,
                                            strategyName=strategy_name, descr="ai自动化活动链路")
        assert res_strategy.get("code") == "10001200", f"新增销售策略, 接口异常{res_strategy}"
        strategy_id = res_strategy.get("data", {}).get("id")
        assert strategy_id, f"新增销售策略未返回策略ID, 接口异常{res_strategy}"

        activity_id = None
        try:
            # 4. 策略下新增营销活动（逐个候选产品尝试直至成功）
            # 报错记录(排查依据):
            # 1) code=001 "所选产品已参与其他活动": 属环境数据问题, 更换候选产品重试;
            # 2) code=11000020 "请勿快速点击,请等待2秒后操作!": 写接口限流(2秒),
            #    重试前必须 time.sleep(2.5) 等待
            res_add = None
            for index, row in enumerate(group_rows[:5]):
                goods_id = row.get("productId")
                if not goods_id:
                    continue
                if index > 0:
                    time.sleep(2.5)
                goods_list = [{
                    "activityGoodsId": goods_id,
                    "partnerSalesAreaList": partner_areas,
                    "materialDiscountsList": [{"thresholdArea": "111", "unitPriceDiscount": 0.1}],
                }]
                res_add = shuzhinadan_api.add_strategy_activity(
                    strategyId=strategy_id,
                    supplierId=supplier_id,
                    marketingActivityName=activity_name,
                    activityStartTime=start_time,
                    activityEndTime=end_time,
                    activityGoodsList=goods_list,
                )
                if res_add.get("code") == "10001200":
                    activity_id = res_add.get("data", {}).get("activityId")
                    break
            assert activity_id, f"候选产品均创建策略营销活动失败, 最后一次接口异常{res_add}"

            # 5. 删除活动
            # 报错记录(排查依据): 创建成功后紧跟删除会触发 code=11000020 限流,
            # 执行前需 time.sleep(2.5) 等待
            time.sleep(2.5)
            res_del = shuzhinadan_api.delete_strategy_activity(activityId=activity_id, strategyId=strategy_id)
            assert res_del.get("code") == "10001200", f"删除策略营销活动, 接口异常{res_del}"
            assert res_del.get("success") is True, f"删除策略营销活动 success 异常{res_del}"

            # 6. 活动列表确认已删除
            # 报错记录(排查依据): 删除后紧跟查询同样受 11000020 限流拦截,
            # 需 time.sleep(2.5) 等待限流窗口通过后再复查列表
            time.sleep(2.5)
            res_list_after = shuzhinadan_api.get_strategy_activity_list(strategyId=strategy_id, supplierId=supplier_id)
            assert res_list_after.get("code") == "10001200", f"查询策略营销活动列表, 接口异常{res_list_after}"
            after_ids = [str(row.get("marketActivityId")) for row in res_list_after.get("data", {}).get("list", [])]
            assert str(activity_id) not in after_ids, f"删除后活动仍在列表中, 活动ID={activity_id}"

            # 活动已删除，置空避免 finally 重复删除
            activity_id = None
        finally:
            # 7. 清理临时策略（清理失败不阻断用例，写操作间需等待限流窗口）
            if activity_id:
                shuzhinadan_api.delete_strategy_activity(activityId=activity_id, strategyId=strategy_id,
                                            status_code=0, error_msg="清理活动失败(不阻断用例)")
                time.sleep(2.5)
            shuzhinadan_api.delete_sale_strategy(id=strategy_id, status_code=0,
                                    error_msg="清理临时策略失败(不阻断用例)")
            time.sleep(2.5)

    @allure.story("营销活动 - 分页列表查询")
    def test_ydl_AF_activity_page_list(self):
        """营销活动分页列表：动态取供应商→分页查询活动列表→校验分页结构与关键字段"""
        # Author: Author
        # Create Date: 2026-09-21
        # IsAI: True

        # 1. 前置内联：查询联合供应商选项，动态获取 supplierId（避免硬编码）
        res_union = shuzhinadan_api.get_union_options()
        assert res_union.get("code") == "10001200", f"查询联合供应商选项, 接口异常{res_union}"
        union_rows = res_union.get("data", {}).get("list", [])
        assert union_rows, f"联合供应商选项为空, 接口异常{res_union}"
        supplier_id = union_rows[0].get("supplierId")
        supplier_name = union_rows[0].get("supplierName")

        # 2. 分页查询营销活动列表
        res_page = MK.find_market_activity_page_list(
            supplierId=supplier_id,
            supplierIdOb={"supplierId": supplier_id, "supplierName": supplier_name},
            pageNo=1,
            pageSize=15,
        )
        assert res_page.get("code") == "10001200", f"分页查询营销活动列表, 接口异常{res_page}"
        page_data = res_page.get("data", {})
        assert "total" in page_data, f"活动列表缺少 total 字段, 接口异常{res_page}"
        activity_rows = page_data.get("list", [])
        assert isinstance(activity_rows, list), f"活动列表 list 结构异常, 接口异常{res_page}"

        # 3. 校验活动行关键字段与供应商归属
        for row in activity_rows:
            assert row.get("marketActivityId"), f"活动行缺少 marketActivityId, 接口异常{res_page}"
            assert row.get("activityStatus"), f"活动行缺少 activityStatus, 接口异常{res_page}"
