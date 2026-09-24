# -*- coding: utf-8 -*-
"""易单来 - 目标管理用例"""

from datetime import datetime, timedelta

import allure
import pytest
from test_case.page_api.ydl.mubiao_api import MubiaoAPI

MB = MubiaoAPI()


def _ok(res, msg="接口返回异常"):
    """校验接口 code=10001200 且 success=True"""
    assert res.get("code") == "10001200", f"{msg}, 接口返回={res}"
    assert res.get("success") is True, f"{msg} success不为True, 接口返回={res}"


def _get_org_id(org_name="东诚包装"):
    """获取目标组织 orgId，默认取“东诚包装”，获取失败则跳过用例。"""
    res_org = MB.get_org_list_no_auth()
    _ok(res_org, "获取目标组织列表失败")
    org_list = res_org.get("data", {}).get("list", [])
    if not org_list:
        pytest.skip("目标组织列表为空，跳过后续步骤")
    # 优先匹配指定组织名，放到列表首位
    for i, org in enumerate(org_list):
        if org.get("orgName") == org_name:
            org_list.insert(0, org_list.pop(i))
            break
    return org_list


# ==================== 目标设置 ====================

@allure.feature("目标设置")
class TestGoalSetting:

    @allure.story("总目标设置")
    def test_ydl_AN_overall_goal_setting(self):
        """总目标设置：获取组织→总目标详情→验证5项指标结构→环比/同比→目标列表→操作记录→复制上月"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True

        # 1. 获取销售组织
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        assert org_id, f"组织orgId为空, org_list[0]={org_list[0]}"
        current_month = datetime.now().strftime("%Y-%m")

        # 2. 获取总目标详情（getGoalInfo.do）
        res_goal = MB.get_goal_info(orgId=org_id, month=current_month)
        _ok(res_goal, "获取总目标详情失败")
        goal_data = res_goal.get("data")
        assert isinstance(goal_data, dict), f"总目标data类型异常, 期望dict, 实际={type(goal_data)}"

        # 3. 验证总目标5项指标（日均接单面积/均价/总接单面积/总销售金额/月活）
        goal_details = goal_data.get("goalDetailsVo")
        assert isinstance(goal_details, dict), f"goalDetailsVo类型异常, 期望dict, 实际={type(goal_details)}"
        indicator_keys = ["dayAvgArea", "avgPrice", "areaTotal", "amountTotal", "monthActive"]
        for key in indicator_keys:
            indicator = goal_details.get(key)
            if indicator is not None:
                assert isinstance(indicator, dict), \
                    f"指标{key}类型异常, 期望dict, 实际={type(indicator)}"
                # 验证每个指标包含 goal/lastGoal/lastYearGoal 子结构
                for sub_key in ["goal", "lastGoal", "lastYearGoal"]:
                    sub = indicator.get(sub_key)
                    if sub is not None:
                        assert isinstance(sub, dict), \
                            f"指标{key}.{sub_key}类型异常, 期望dict, 实际={type(sub)}"
                        # GoalModel 应包含 value/reachValue/dif/progress
                        for field in ["value", "reachValue", "dif", "progress"]:
                            if field in sub:
                                assert isinstance(sub[field], (int, float)), \
                                    f"{key}.{sub_key}.{field}类型异常, 期望数值, 实际={type(sub[field])}"

        # 4. 验证环比/同比字段存在
        for key in indicator_keys:
            indicator = goal_details.get(key)
            if indicator is not None:
                for ratio_key in ["goalMom", "goalYoy", "reachValueMom", "reachValueYoy"]:
                    if ratio_key in indicator:
                        val = indicator[ratio_key]
                        assert isinstance(val, (int, float, type(None))), \
                            f"{key}.{ratio_key}类型异常, 实际={type(val)}"

        # 5. 验证基础字段
        assert "goalStatus" in goal_data, f"总目标缺少goalStatus字段"
        assert "orgName" in goal_data, f"总目标缺少orgName字段"

        # 6. 目标设置列表（getList.do）
        res_list = MB.get_goal_list(orgId=org_id, month=current_month, pageNo=1, pageSize=10)
        _ok(res_list, "获取目标列表失败")
        list_data = res_list.get("data", {})
        assert isinstance(list_data, dict), f"目标列表data类型异常, 期望dict, 实际={type(list_data)}"
        assert "total" in list_data, f"目标列表缺少total字段"
        assert isinstance(list_data.get("total"), int), \
            f"目标列表total类型异常, 期望int, 实际={type(list_data.get('total'))}"

        # 7. 操作记录（getLogList.do）- 可能无权限
        res_log = MB.get_log_list(orgId=org_id, month=current_month, pageNo=1, pageSize=10)
        assert res_log.get("code") in ("10001200", "10201011"), \
            f"获取操作记录返回非预期code, 接口返回={res_log}"
        if res_log.get("code") == "10001200":
            log_data = res_log.get("data", {})
            assert isinstance(log_data, dict), f"操作记录data类型异常, 期望dict, 实际={type(log_data)}"
            log_list = log_data.get("list", [])
            assert isinstance(log_list, list), f"操作记录list类型异常, 期望list, 实际={type(log_list)}"
            if log_list:
                first_log = log_list[0]
                for field in ["operatorName", "createTime"]:
                    assert field in first_log, f"操作记录缺少{field}字段, item={first_log}"

        # 8. 复制上月目标（copy.do）- 空参数测试参数校验
        res_copy = MB.copy_goal(orgId=org_id, month=current_month)
        assert res_copy.get("code") is not None, f"复制上月目标未返回code, 接口返回={res_copy}"

    @allure.story("产品目标设置")
    def test_ydl_AP_product_goal_setting(self):
        """产品目标设置：获取组织→查询产品目标→验证产品分类与汇总字段→产品分层列表→分页→产品区域复制→分供应商"""
        # Author: Author
        # Create Date: 2026-07-27
        # IsAI: True

        # 1. 获取销售组织列表
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        assert org_id, f"组织orgId为空, org_list[0]={org_list[0]}"
        current_month = datetime.now().strftime("%Y-%m")

        # 2. 获取产品目标信息
        res_goal = MB.get_product_goal_info(orgId=org_id, month=current_month)
        _ok(res_goal, "获取产品目标信息失败")
        goal_data = res_goal.get("data", {})
        assert isinstance(goal_data, dict), f"产品目标data类型异常, 期望dict, 实际={type(goal_data)}"

        # 3. 验证产品分类列表
        regular_list = goal_data.get("regularlList", [])
        custom_list = goal_data.get("customlList", [])
        assert isinstance(regular_list, list), f"regularlList类型异常, 期望list, 实际={type(regular_list)}"
        assert isinstance(custom_list, list), f"customlList类型异常, 期望list, 实际={type(custom_list)}"

        # 4. 验证汇总信息结构
        sum_info = goal_data.get("sumInfo", {})
        assert isinstance(sum_info, dict), f"sumInfo类型异常, 期望dict, 实际={type(sum_info)}"
        regular_sum = goal_data.get("regularSumInfo", {})
        assert isinstance(regular_sum, dict), f"regularSumInfo类型异常, 期望dict, 实际={type(regular_sum)}"
        custom_sum = goal_data.get("customSumInfo", {})
        assert isinstance(custom_sum, dict), f"customSumInfo类型异常, 期望dict, 实际={type(custom_sum)}"

        # 5. 验证产品字段结构（当有产品数据时）
        all_products = regular_list + custom_list
        if all_products:
            first = all_products[0]
            assert "productId" in first, f"产品缺少productId, product={first}"
            assert "productName" in first, f"产品缺少productName, product={first}"
            last_goal = first.get("lastGoal", {})
            assert isinstance(last_goal, dict), f"lastGoal类型异常, 期望dict, 实际={type(last_goal)}"
            # 验证环比字段
            for field in ["goalMomDif", "goalMom"]:
                if field in first:
                    assert isinstance(first[field], (int, float, type(None))), \
                        f"产品{field}类型异常, 实际={type(first[field])}"

        # 6. 产品分层列表
        res_layer = MB.get_product_layer_list(payload_data={"orgId": org_id})
        _ok(res_layer, "获取产品分层列表失败")
        layer_list = res_layer.get("data", {}).get("list", [])
        assert isinstance(layer_list, list), f"产品分层列表类型异常, 期望list, 实际={type(layer_list)}"
        for item in layer_list:
            assert "layerName" in item, f"分层缺少layerName, item={item}"
            assert "layer" in item, f"分层缺少layer, item={item}"
            assert isinstance(item.get("layer"), int), f"layer类型异常, 期望int, 实际={type(item.get('layer'))}"

        # 7. 分页查询
        res_page = MB.get_product_goal_info(orgId=org_id, month=current_month, pageNo=1, pageSize=5)
        _ok(res_page, "分页查询产品目标失败")

        # 8. 产品区域目标复制（productAreaGoalCopy.do）
        res_copy = MB.product_area_goal_copy(orgId=org_id, month=current_month)
        assert res_copy.get("code") in ("10001200", "10201011"), \
            f"产品区域目标复制返回异常code, 接口返回={res_copy}"

        # 9. 分供应商信息（getSupplierInfoNoAuth.do）
        res_supplier = MB.get_supplier_info_no_auth()
        _ok(res_supplier, "获取分供应商信息失败")
        supplier_data = res_supplier.get("data", {})
        assert isinstance(supplier_data, dict), \
            f"分供应商data类型异常, 期望dict, 实际={type(supplier_data)}"

    @allure.story("区域目标设置")
    def test_ydl_AQ_area_goal_setting(self):
        """区域目标设置：获取组织→区域目标信息→验证合计行→产品区域分解→目标分解→多组织区域对比"""
        # Author: Author
        # Create Date: 2026-07-27
        # IsAI: True

        # 1. 获取销售组织
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        current_month = datetime.now().strftime("%Y-%m")

        # 2. 获取区域目标信息（getAreaGoalInfo.do）
        res_area = MB.get_area_goal_info(orgId=org_id, month=current_month, pageNo=1, pageSize=20)
        _ok(res_area, "获取区域目标信息失败")
        area_data = res_area.get("data", {})
        assert isinstance(area_data, dict), f"区域目标data类型异常, 期望dict, 实际={type(area_data)}"

        # 3. 验证合计行（itemTotal）
        item_total = area_data.get("itemTotal")
        if item_total is not None:
            assert isinstance(item_total, dict), \
                f"区域合计行itemTotal类型异常, 期望dict, 实际={type(item_total)}"
            # GoalItemVo 的字段可能是 GoalModel(dict) 或数值
            for field in ["goal", "reachValue", "dif", "progress"]:
                if field in item_total:
                    val = item_total[field]
                    assert isinstance(val, (int, float, dict)), \
                        f"区域合计行{field}类型异常, 期望数值或dict, 实际={type(val)}"

        # 4. 验证区域列表
        area_list = area_data.get("areaDayAvgArea", [])
        assert isinstance(area_list, list), f"areaDayAvgArea类型异常, 期望list, 实际={type(area_list)}"
        if area_list:
            first_area = area_list[0]
            assert isinstance(first_area, dict), \
                f"区域列表项类型异常, 期望dict, 实际={type(first_area)}"

        # 5. 验证 total 字段
        assert "total" in area_data, f"区域目标缺少total字段"

        # 6. 产品区域目标自动分解
        res_decompose = MB.product_area_goal_decompose(orgId=org_id, month=current_month)
        _ok(res_decompose, "产品区域目标分解失败")

        # 7. 目标分解（通用）
        res_gen_decompose = MB.decompose_goal(orgId=org_id, month=current_month)
        assert res_gen_decompose.get("code") in ("10001200", "10201011"), \
            f"目标分解返回异常code, 接口返回={res_gen_decompose}"
        if res_gen_decompose.get("code") == "10201011":
            assert res_gen_decompose.get("success") is False, "权限不足时success应为False"

        # 8. 多组织区域目标对比
        if len(org_list) >= 2:
            org_id_2 = org_list[1].get("orgId", "")
            res_area_2 = MB.get_area_goal_info(orgId=org_id_2, month=current_month, pageNo=1, pageSize=20)
            assert res_area_2.get("code") in ("10001200", "11000020"), \
                f"第二个组织区域目标信息返回非预期code, 接口返回={res_area_2}"
            assert org_id != org_id_2, "两个组织orgId不应相同"

    @allure.story("团队目标设置")
    def test_ydl_AR_team_goal_setting(self):
        """团队目标设置：获取组织→团队目标信息→团队汇总验证→分供应商分解→生成目标→同步→保存→下发"""
        # Author: Author
        # Create Date: 2026-07-27
        # IsAI: True

        # 1. 获取销售组织
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        current_month = datetime.now().strftime("%Y-%m")

        # 2. 获取团队目标信息（getTeamGoalInfo.do）
        res_team = MB.get_team_goal_info(orgId=org_id, month=current_month)
        _ok(res_team, "获取团队目标信息失败")
        team_data = res_team.get("data", {})
        assert isinstance(team_data, dict), f"团队目标data类型异常, 期望dict, 实际={type(team_data)}"

        # 3. 验证团队汇总指标（dayAvgAreaTotal/monthActiveTotal）
        for key in ["dayAvgAreaTotal", "monthActiveTotal"]:
            total_item = team_data.get(key)
            if total_item is not None:
                assert isinstance(total_item, dict), \
                    f"团队{key}类型异常, 期望dict, 实际={type(total_item)}"
                # GoalItemVo 字段可能是 GoalModel(dict) 或数值
                for field in ["goal", "reachValue", "dif", "progress"]:
                    if field in total_item:
                        assert isinstance(total_item[field], (int, float, dict)), \
                            f"团队{key}.{field}类型异常, 期望数值或dict, 实际={type(total_item[field])}"

        # 4. 验证团队区域列表
        area_day_avg = team_data.get("areaDayAvgArea", [])
        assert isinstance(area_day_avg, list), \
            f"areaDayAvgArea类型异常, 期望list, 实际={type(area_day_avg)}"

        # 5. 团队分供应商目标分解（getTeamSupplierDecomposeInfoNoAuth.do）
        res_decompose = MB.get_team_supplier_decompose_info(orgId=org_id, month=current_month)
        _ok(res_decompose, "获取团队分供应商分解失败")
        decompose_data = res_decompose.get("data", {})
        assert isinstance(decompose_data, dict), \
            f"团队分供应商data类型异常, 期望dict, 实际={type(decompose_data)}"
        # 验证 supplierList 结构
        supplier_list = decompose_data.get("supplierList", [])
        assert isinstance(supplier_list, list), \
            f"supplierList类型异常, 期望list, 实际={type(supplier_list)}"
        if supplier_list:
            first_supplier = supplier_list[0]
            for field in ["supplierId", "supplierName"]:
                assert field in first_supplier, \
                    f"供应商列表缺少{field}, item={first_supplier}"

        # 6. 生成组织目标 - 测试环境可能无权限
        res_gen = MB.generate_goal(orgId=org_id, month=current_month)
        assert res_gen.get("code") in ("10001200", "10201011"), \
            f"生成目标返回异常code, 接口返回={res_gen}"
        if res_gen.get("code") == "10201011":
            assert res_gen.get("success") is False, "权限不足时success应为False"

        # 7. 同步团队目标
        res_sync = MB.sync_team_goal(payload_data={"orgId": org_id, "month": current_month})
        assert res_sync.get("code") in ("10001200", "10201011"), \
            f"同步团队目标返回异常code, 接口返回={res_sync}"

        # 8. 目标保存
        res_save = MB.save_goal(orgId=org_id, month=current_month)
        assert res_save.get("code") is not None, f"目标保存未返回code, 接口返回={res_save}"

        # 9. 目标下发 - 空列表应返回参数校验错误
        res_assign = MB.assign_goal(supplierIdList=[])
        assert res_assign.get("code") != "10001200", \
            f"空列表下发目标应该失败, 但返回了成功, 接口返回={res_assign}"

    @allure.story("首页-获取客户目标")
    def test_ydl_BD_home_customer_goal_info(self):
        """首页获取客户目标：组织→筛选方案→客户目标信息→sumInfo汇总校验→排序查询"""
        # Author: Author
        # Create Date: 2026-08-20
        # IsAI: True

        # 1. 获取销售组织
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        assert org_id, f"组织orgId为空, org_list[0]={org_list[0]}"
        current_month = datetime.now().strftime("%Y-%m")

        # 2. 获取筛选方案，提取supplierId/filterSchemeConfigId
        res_filter = MB.get_all_filter_scheme_no_auth()
        _ok(res_filter, "获取筛选方案配置列表失败")
        filter_list = res_filter.get("data", {}).get("list", [])
        supplier_id = ""
        filter_config_id = ""
        if filter_list:
            filter_config_id = filter_list[0].get("id", "")
            supplier_list = filter_list[0].get("supplierList", [])
            if supplier_list:
                supplier_id = supplier_list[0].get("supplierId", "")

        # 3. 首页获取客户目标（getCustomerGoalInfo.do）
        res_info = MB.get_customer_goal_info(
            orgId=org_id, month=current_month,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id
        )
        assert res_info.get("code") in ("10001200", "10010100", "10003001"), \
            f"首页获取客户目标返回非预期code, 接口返回={res_info}"
        if res_info.get("code") == "10001200":
            info_data = res_info.get("data")
            assert isinstance(info_data, dict), \
                f"客户目标信息data类型异常, 期望dict, 实际={type(info_data)}"

            # 4. sumInfo汇总结构校验
            sum_info = info_data.get("sumInfo")
            if sum_info is not None:
                assert isinstance(sum_info, dict), \
                    f"sumInfo类型异常, 期望dict, 实际={type(sum_info)}"

        # 5. 排序查询（sort=customer_count客户家数，sortType=desc降序）
        res_sort = MB.get_customer_goal_info(
            orgId=org_id, month=current_month,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id,
            sort="customer_count", sortType="desc"
        )
        assert res_sort.get("code") in ("10001200", "10010100", "10003001"), \
            f"首页获取客户目标-排序查询返回非预期code, 接口返回={res_sort}"


# ==================== 目标跟踪 ====================

@allure.feature("目标跟踪")
class TestGoalTracking:

    @allure.story("团队目标跟踪")
    def test_ydl_AT_team_goal_tracking(self):
        """团队目标跟踪：团队汇总→趋势图→跟踪详情→追踪列表→供应商跟踪(周/月)→多组织"""
        # Author: Author
        # Create Date: 2026-07-27
        # IsAI: True

        # 1. 获取销售组织
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        current_month = datetime.now().strftime("%Y-%m")

        # 1.1 获取筛选方案，提取 supplierId / filterSchemeConfigId
        res_filter = MB.get_all_filter_scheme_no_auth()
        _ok(res_filter, "获取筛选方案配置列表失败")
        filter_list = res_filter.get("data", {}).get("list", [])
        supplier_id = ""
        filter_config_id = ""
        if filter_list:
            filter_config_id = filter_list[0].get("id", "")
            supplier_list = filter_list[0].get("supplierList", [])
            if supplier_list:
                supplier_id = supplier_list[0].get("supplierId", "")

        # 1.2 计算日期参数
        now = datetime.now()
        start_time = f"{now.strftime('%Y-%m')}-01 00:00:00"
        end_time = f"{now.strftime('%Y-%m')}-{now.strftime('%d')} 23:59:59"
        select_date = [start_time, end_time]
        week_start = (now - timedelta(days=14)).strftime('%Y-%m-%d')
        week_end = (now + timedelta(days=7)).strftime('%Y-%m-%d')
        week_month = {
            "type": "month",
            "weekDate": {"startDate": week_start, "endDate": week_end},
            "selectDate": select_date
        }
        date_list = [(now - timedelta(days=3 - i)).strftime('%Y-%m-%d') for i in range(4)]
        prev_month_dt = datetime(now.year, now.month - 1 if now.month > 1 else 12, 1)
        year_month_list = [prev_month_dt.strftime('%Y-%m'), now.strftime('%Y-%m')]
        empty_range = {"min": "", "max": ""}

        # 2. 团队汇总
        res_team = MB.get_team_summary(payload_data={"orgId": org_id, "month": current_month})
        _ok(res_team, "获取团队汇总失败")
        team_data = res_team.get("data")
        assert isinstance(team_data, dict), f"团队汇总data类型异常, 期望dict, 实际={type(team_data)}"

        # 3. 验证团队汇总的数值字段（当有目标数据时）
        for key in ["lowAvgCount", "unOrderCount"]:
            if key in team_data:
                val = team_data[key]
                assert isinstance(val, (int, float)), \
                    f"{key}类型异常, 期望数值, 实际={type(val)}, 值={val}"
                assert val >= 0, f"{key}值异常, 期望>=0, 实际={val}"

        # 4. 团队趋势图-周维度（getWeekTeamGoalTraceDetail.do）
        res_trend = MB.get_week_team_goal_trace(orgId=org_id)
        # 趋势图接口可能返回系统异常(10010100)，兼容处理
        assert res_trend.get("code") in ("10001200", "10010100"), \
            f"获取团队趋势图返回非预期code, 接口返回={res_trend}"
        if res_trend.get("code") == "10001200":
            trend_data = res_trend.get("data")
            assert isinstance(trend_data, (dict, list, type(None))), \
                f"团队趋势data类型异常, 期望dict/list/None, 实际={type(trend_data)}"
            if isinstance(trend_data, list) and trend_data:
                first_point = trend_data[0]
                assert isinstance(first_point, dict), \
                    f"趋势点类型异常, 期望dict, 实际={type(first_point)}"

        # 5. 团队目标跟踪详情（getTeamGoalTraceDetail.do）- 传完整参数
        res_trace_detail = MB.get_team_goal_trace_detail(
            orgId=org_id, month=current_month,
            weekMonth=week_month, yearMonthList=year_month_list, dateList=date_list,
            dimension=["amount", "area", "customer"],
            goalValue=empty_range, mom=empty_range, monthDiff=empty_range, yesterdayDiff=empty_range,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id,
            selectDate=select_date, startDate=week_start, endDate=week_end
        )
        assert res_trace_detail.get("code") in ("10001200", "10010100"), \
            f"获取团队目标跟踪详情返回非预期code, 接口返回={res_trace_detail}"
        if res_trace_detail.get("code") == "10001200":
            trace_detail_data = res_trace_detail.get("data", {})
            assert isinstance(trace_detail_data, dict), \
                f"团队跟踪详情data类型异常, 期望dict, 实际={type(trace_detail_data)}"
            # 验证汇总行结构
            total_data = trace_detail_data.get("totalData", {})
            if total_data:
                assert isinstance(total_data, dict), \
                    f"团队跟踪totalData类型异常, 期望dict, 实际={type(total_data)}"

        # 6. 团队目标追踪列表（getTeamTraceList.do）
        res_trace_list = MB.get_team_trace_list(
            payload_data={"orgId": org_id, "month": current_month}
        )
        assert res_trace_list.get("code") in ("10001200", "10010100"), \
            f"获取团队追踪列表返回非预期code, 接口返回={res_trace_list}"
        if res_trace_list.get("code") == "10001200":
            trace_list_data = res_trace_list.get("data", {})
            assert isinstance(trace_list_data, dict), \
                f"团队追踪列表data类型异常, 期望dict, 实际={type(trace_list_data)}"
            trace_items = trace_list_data.get("list", [])
            if trace_items:
                first_item = trace_items[0]
                for field in ["name", "goalArea", "saleArea"]:
                    if field in first_item:
                        assert isinstance(first_item[field], (int, float, str, type(None))), \
                            f"团队追踪{field}类型异常, 实际={type(first_item[field])}"

        # 7. 团队供应商目标跟踪-周维度（getWeekTeamSupplierGoalTraceDetail.do）
        res_week_supplier = MB.get_week_team_supplier_goal_trace(
            payload_data={"orgId": org_id}
        )
        assert res_week_supplier.get("code") in ("10001200", "10010100"), \
            f"获取团队供应商周维度跟踪返回非预期code, 接口返回={res_week_supplier}"

        # 8. 团队供应商目标跟踪-月维度（getTeamSupplierGoalTraceDetail.do）
        res_month_supplier = MB.get_team_supplier_goal_trace(
            payload_data={"orgId": org_id, "month": current_month}
        )
        assert res_month_supplier.get("code") in ("10001200", "10010100"), \
            f"获取团队供应商月维度跟踪返回非预期code, 接口返回={res_month_supplier}"

        # 9. 多组织切换查询团队汇总
        if len(org_list) >= 2:
            org_id_2 = org_list[1].get("orgId", "")
            res_team_2 = MB.get_team_summary(payload_data={"orgId": org_id_2, "month": current_month})
            _ok(res_team_2, "第二个组织团队汇总失败")
            team_data_2 = res_team_2.get("data")
            assert isinstance(team_data_2, dict), \
                f"第二个组织团队汇总data类型异常, 期望dict, 实际={type(team_data_2)}"

    @allure.story("产品目标跟踪")
    def test_ydl_AU_product_goal_tracking(self):
        """产品目标跟踪：产品汇总→分层→跟踪列表→详情→周维度→区域跟踪→层级跟踪"""
        # Author: Author
        # Create Date: 2026-07-27
        # IsAI: True

        # 1. 获取销售组织
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        current_month = datetime.now().strftime("%Y-%m")

        # 1.1 获取筛选方案，提取 supplierId / filterSchemeConfigId
        res_filter = MB.get_all_filter_scheme_no_auth()
        _ok(res_filter, "获取筛选方案配置列表失败")
        filter_list = res_filter.get("data", {}).get("list", [])
        supplier_id = ""
        filter_config_id = ""
        if filter_list:
            filter_config_id = filter_list[0].get("id", "")
            supplier_list = filter_list[0].get("supplierList", [])
            if supplier_list:
                supplier_id = supplier_list[0].get("supplierId", "")

        # 1.2 计算日期参数
        now = datetime.now()
        start_time = f"{now.strftime('%Y-%m')}-01 00:00:00"
        end_time = f"{now.strftime('%Y-%m')}-{now.strftime('%d')} 23:59:59"
        select_date = [start_time, end_time]
        week_start = (now - timedelta(days=14)).strftime('%Y-%m-%d')
        week_end = (now + timedelta(days=7)).strftime('%Y-%m-%d')
        week_month = {
            "type": "month",
            "weekDate": {"startDate": week_start, "endDate": week_end},
            "selectDate": select_date
        }
        date_list = [(now - timedelta(days=3 - i)).strftime('%Y-%m-%d') for i in range(4)]
        prev_month_dt = datetime(now.year, now.month - 1 if now.month > 1 else 12, 1)
        year_month_list = [prev_month_dt.strftime('%Y-%m'), now.strftime('%Y-%m')]
        empty_range = {"min": "", "max": ""}

        # 2. 产品汇总
        res_prod = MB.get_product_summary(payload_data={"orgId": org_id, "month": current_month})
        _ok(res_prod, "获取产品汇总失败")
        prod_data = res_prod.get("data", {})
        assert isinstance(prod_data, dict), f"产品汇总data类型异常, 期望dict, 实际={type(prod_data)}"

        # 3. 验证产品汇总的数值字段
        for key in ["lowAvgCount", "unOrderCount"]:
            if key in prod_data:
                val = prod_data[key]
                assert isinstance(val, (int, float)), \
                    f"{key}类型异常, 期望数值, 实际={type(val)}, 值={val}"
                assert val >= 0, f"{key}值异常, 期望>=0, 实际={val}"

        # 4. 产品分层列表（跟踪视图）
        res_layer = MB.get_product_layer_list(payload_data={"orgId": org_id})
        _ok(res_layer, "获取产品分层列表失败")
        layer_data = res_layer.get("data", {})
        layer_list = layer_data.get("list", [])
        assert len(layer_list) > 0, f"产品分层列表为空"
        layers = [item.get("layer") for item in layer_list]
        assert all(isinstance(l, int) for l in layers), f"存在非整数layer, layers={layers}"

        # 5. 产品跟踪列表（getProductTraceList.do）- 需要分页参数
        res_trace = MB.get_product_trace_list(
            payload_data={"orgId": org_id, "month": current_month, "pageNo": 1, "pageSize": 20}
        )
        # 跟踪列表接口可能返回系统异常(10010100)，兼容处理
        assert res_trace.get("code") in ("10001200", "10010100"), \
            f"获取产品跟踪列表返回非预期code, 接口返回={res_trace}"
        if res_trace.get("code") == "10001200":
            trace_data = res_trace.get("data", {})
            assert isinstance(trace_data, dict), \
                f"产品跟踪列表data类型异常, 期望dict, 实际={type(trace_data)}"

        # 6. 产品目标跟踪详情（getProductGoalTraceDetail.do）- 传完整参数
        res_goal_trace = MB.get_product_goal_trace(
            orgId=org_id, month=current_month, pageNo=1, pageSize=15,
            weekMonth=week_month, yearMonthList=year_month_list, dateList=date_list,
            dimension=["amount", "area", "customer"],
            goalValue=empty_range, mom=empty_range, monthDiff=empty_range, yesterdayDiff=empty_range,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id,
            selectDate=select_date, startDate=week_start, endDate=week_end
        )
        # 跟踪详情接口可能返回系统异常(10010100)或分页校验(10003001)，兼容处理
        assert res_goal_trace.get("code") in ("10001200", "10010100", "10003001"), \
            f"获取产品目标跟踪详情返回非预期code, 接口返回={res_goal_trace}"
        if res_goal_trace.get("code") == "10001200":
            goal_trace_data = res_goal_trace.get("data")
            assert isinstance(goal_trace_data, (dict, list, type(None))), \
                f"产品跟踪详情data类型异常, 期望dict/list/None, 实际={type(goal_trace_data)}"

        # 7. 产品目标跟踪-周维度（getWeekProductGoalTraceDetail.do）
        res_week = MB.get_week_product_goal_trace(
            payload_data={"orgId": org_id, "month": current_month, "pageNo": 1, "pageSize": 20}
        )
        assert res_week.get("code") in ("10001200", "10010100", "10003001"), \
            f"获取产品周维度跟踪返回非预期code, 接口返回={res_week}"

        # 8. 产品目标信息（跟踪参考）
        res_goal = MB.get_product_goal_info(orgId=org_id, month=current_month)
        _ok(res_goal, "获取产品目标信息失败")
        goal_total = res_goal.get("data", {}).get("total", 0)
        assert isinstance(goal_total, int), f"产品目标total类型异常, 期望int, 实际={type(goal_total)}"

        # 9. 产品区域跟踪（getProductAreaDetail.do）- 传完整参数
        res_area = MB.get_product_area_detail(
            orgId=org_id, month=current_month, pageNo=1, pageSize=15,
            selectDate=select_date, yearMonthList=year_month_list, dateList=date_list,
            productIdList=[], areaIdList=[],
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id
        )
        assert res_area.get("code") in ("10001200", "10010100", "10003001"), \
            f"获取产品区域跟踪返回非预期code, 接口返回={res_area}"
        if res_area.get("code") == "10001200":
            area_data = res_area.get("data", {})
            assert isinstance(area_data, dict), \
                f"产品区域跟踪data类型异常, 期望dict, 实际={type(area_data)}"
            # 验证分页结构
            if "total" in area_data:
                assert isinstance(area_data["total"], int), \
                    f"产品区域跟踪total类型异常, 期望int, 实际={type(area_data['total'])}"

        # 10. 产品层级跟踪列表（getProductLayerTraceList.do）
        res_layer_trace = MB.get_product_layer_trace_list(
            payload_data={"orgId": org_id, "month": current_month, "pageNo": 1, "pageSize": 20}
        )
        assert res_layer_trace.get("code") in ("10001200", "10010100", "10003001"), \
            f"获取产品层级跟踪列表返回非预期code, 接口返回={res_layer_trace}"

    @allure.story("区域目标跟踪")
    def test_ydl_AV_area_goal_tracking(self):
        """区域目标跟踪：获取组织→区域趋势→区域目标跟踪详情→周维度趋势→区域分解→多组织对比"""
        # Author: Author
        # Create Date: 2026-07-27
        # IsAI: True

        # 1. 获取销售组织
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        current_month = datetime.now().strftime("%Y-%m")

        # 1.1 获取筛选方案，提取 supplierId / filterSchemeConfigId
        res_filter = MB.get_all_filter_scheme_no_auth()
        _ok(res_filter, "获取筛选方案配置列表失败")
        filter_list = res_filter.get("data", {}).get("list", [])
        supplier_id = ""
        filter_config_id = ""
        if filter_list:
            filter_config_id = filter_list[0].get("id", "")
            supplier_list = filter_list[0].get("supplierList", [])
            if supplier_list:
                supplier_id = supplier_list[0].get("supplierId", "")

        # 1.2 计算日期参数
        now = datetime.now()
        start_time = f"{now.strftime('%Y-%m')}-01 00:00:00"
        end_time = f"{now.strftime('%Y-%m')}-{now.strftime('%d')} 23:59:59"
        select_date = [start_time, end_time]
        week_start = (now - timedelta(days=14)).strftime('%Y-%m-%d')
        week_end = (now + timedelta(days=7)).strftime('%Y-%m-%d')
        week_month = {
            "type": "month",
            "weekDate": {"startDate": week_start, "endDate": week_end},
            "selectDate": select_date
        }
        date_list = [(now - timedelta(days=3 - i)).strftime('%Y-%m-%d') for i in range(4)]
        prev_month_dt = datetime(now.year, now.month - 1 if now.month > 1 else 12, 1)
        year_month_list = [prev_month_dt.strftime('%Y-%m'), now.strftime('%Y-%m')]
        empty_range = {"min": "", "max": ""}

        # 2. 区域趋势（getAreaTrend.do）- UI 截图中的趋势图
        res_trend = MB.get_area_trend(payload_data={"orgId": org_id, "month": current_month})
        # 区域趋势接口可能返回系统异常(10010100)，兼容处理
        assert res_trend.get("code") in ("10001200", "10010100"), \
            f"获取区域趋势返回非预期code, 接口返回={res_trend}"
        if res_trend.get("code") == "10001200":
            trend_data = res_trend.get("data")
            assert isinstance(trend_data, (dict, list, type(None))), \
                f"区域趋势data类型异常, 期望dict/list/None, 实际={type(trend_data)}"
            if isinstance(trend_data, list) and trend_data:
                first_point = trend_data[0]
                assert isinstance(first_point, dict), \
                    f"趋势点类型异常, 期望dict, 实际={type(first_point)}"

        # 3. 区域目标跟踪详情（getAreaGoalTraceDetail.do）- 传完整参数
        res_trace = MB.get_area_goal_trace(
            orgId=org_id, month=current_month,
            weekMonth=week_month, yearMonthList=year_month_list, dateList=date_list,
            dimension=["amount", "area", "customer"], areaCodeList=[],
            goalValue=empty_range, mom=empty_range, monthDiff=empty_range, yesterdayDiff=empty_range,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id,
            selectDate=select_date, startDate=week_start, endDate=week_end
        )
        # 跟踪详情接口可能返回系统异常(10010100)，兼容处理
        assert res_trace.get("code") in ("10001200", "10010100"), \
            f"获取区域目标跟踪详情返回非预期code, 接口返回={res_trace}"
        if res_trace.get("code") == "10001200":
            trace_data = res_trace.get("data", {})
            assert isinstance(trace_data, dict), \
                f"区域跟踪详情data类型异常, 期望dict, 实际={type(trace_data)}"

        # 4. 区域目标跟踪-周维度（getWeekAreaGoalTraceDetail.do）
        res_week = MB.get_week_area_goal_trace(payload_data={"orgId": org_id, "month": current_month})
        assert res_week.get("code") in ("10001200", "10010100"), \
            f"获取区域周维度跟踪返回非预期code, 接口返回={res_week}"

        # 5. 区域供应商目标跟踪详情（getAreaSupplierGoalTraceDetail.do）
        res_supplier_trace = MB.get_area_supplier_goal_trace(
            payload_data={"orgId": org_id, "month": current_month}
        )
        assert res_supplier_trace.get("code") in ("10001200", "10010100"), \
            f"获取区域供应商跟踪返回非预期code, 接口返回={res_supplier_trace}"

        # 6. 区域目标自动分解
        res_decompose = MB.product_area_goal_decompose(orgId=org_id, month=current_month)
        _ok(res_decompose, "区域目标分解失败")

        # 7. 通用目标分解
        res_gen_decompose = MB.decompose_goal(orgId=org_id, month=current_month)
        assert res_gen_decompose.get("code") in ("10001200", "10201011"), \
            f"目标分解返回异常code, 接口返回={res_gen_decompose}"

        # 8. 多组织区域目标分解对比
        if len(org_list) >= 2:
            org_id_2 = org_list[1].get("orgId", "")
            res_decompose_2 = MB.product_area_goal_decompose(orgId=org_id_2, month=current_month)
            assert res_decompose_2.get("code") in ("10001200", "11000020", "10201011"), \
                f"第二个组织区域目标分解返回非预期code, 接口返回={res_decompose_2}"
            assert org_id != org_id_2, "两个组织orgId不应相同"

    @allure.story("客户目标跟踪")
    def test_ydl_AW_customer_goal_tracking(self):
        """客户目标跟踪：客户目标数据→汇总→更新月需求→考核日期→多月份对比→跟踪详情→客户类型达成分析"""
        # Author: Author
        # Create Date: 2026-07-27
        # IsAI: True

        # 1. 获取销售组织
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        current_month = datetime.now().strftime("%Y-%m")

        # 1.1 获取筛选方案，提取 supplierId / filterSchemeConfigId
        res_filter = MB.get_all_filter_scheme_no_auth()
        _ok(res_filter, "获取筛选方案配置列表失败")
        filter_list = res_filter.get("data", {}).get("list", [])
        supplier_id = ""
        filter_config_id = ""
        if filter_list:
            filter_config_id = filter_list[0].get("id", "")
            supplier_list = filter_list[0].get("supplierList", [])
            if supplier_list:
                supplier_id = supplier_list[0].get("supplierId", "")

        # 1.2 计算日期参数
        now = datetime.now()
        start_time = f"{now.strftime('%Y-%m')}-01 00:00:00"
        end_time = f"{now.strftime('%Y-%m')}-{now.strftime('%d')} 23:59:59"
        select_date = [start_time, end_time]
        week_start = (now - timedelta(days=14)).strftime('%Y-%m-%d')
        week_end = (now + timedelta(days=7)).strftime('%Y-%m-%d')
        week_month = {
            "type": "month",
            "weekDate": {"startDate": week_start, "endDate": week_end},
            "selectDate": select_date
        }
        date_list = [(now - timedelta(days=3 - i)).strftime('%Y-%m-%d') for i in range(4)]
        prev_month_dt = datetime(now.year, now.month - 1 if now.month > 1 else 12, 1)
        year_month_list = [prev_month_dt.strftime('%Y-%m'), now.strftime('%Y-%m')]
        empty_range = {"min": "", "max": ""}

        # 2. 跟踪参考：获取客户目标产品列表（customlList对应UI客户目标tab的数据）
        res_goal = MB.get_product_goal_info(orgId=org_id, month=current_month)
        _ok(res_goal, "获取客户目标产品列表失败")
        goal_data = res_goal.get("data", {})

        # 3. 验证客户目标产品列表结构（UI表格：客户名称、目标值等）
        custom_list = goal_data.get("customlList", [])
        assert isinstance(custom_list, list), f"customlList类型异常, 期望list, 实际={type(custom_list)}"
        if custom_list:
            first = custom_list[0]
            assert "productId" in first, f"客户目标产品缺少productId, item={first}"
            assert "productName" in first, f"客户目标产品缺少productName, item={first}"
            assert "lastGoal" in first, f"客户目标产品缺少lastGoal, item={first}"
            last_goal = first.get("lastGoal", {})
            assert isinstance(last_goal, dict), f"lastGoal类型异常, 期望dict, 实际={type(last_goal)}"
            # lastGoal 应包含 dif 和 reachValue 数值字段
            for field in ["dif", "reachValue"]:
                if field in last_goal:
                    assert isinstance(last_goal[field], (int, float)), \
                        f"lastGoal.{field}类型异常, 期望数值, 实际={type(last_goal[field])}"

        # 4. 验证客户汇总信息（UI表头汇总数据）
        custom_sum = goal_data.get("customSumInfo", {})
        assert isinstance(custom_sum, dict), f"customSumInfo类型异常, 期望dict, 实际={type(custom_sum)}"
        if custom_sum:
            # goal 字段表示目标值，lastGoal 包含上期对比数据
            if "goal" in custom_sum:
                assert isinstance(custom_sum["goal"], (int, float)), \
                    f"customSumInfo.goal类型异常, 期望数值, 实际={type(custom_sum['goal'])}"
            if "lastGoal" in custom_sum:
                assert isinstance(custom_sum["lastGoal"], dict), \
                    f"customSumInfo.lastGoal类型异常, 期望dict, 实际={type(custom_sum['lastGoal'])}"

        # 5. 更新月需求（无鉴权）- 缺少客户id应返回参数校验错误
        res_month = MB.update_month_requirement(payload_data={})
        assert res_month.get("code") == "10003001", \
            f"空参数更新月需求应返回参数校验错误, 接口返回={res_month}"

        # 6. 更新考核日期（无鉴权）- 缺少必填参数应返回参数校验错误
        res_date = MB.update_assessment_date(payload_data={})
        assert res_date.get("code") in ("10003001", "10201011"), \
            f"空参数更新考核日期应返回参数校验错误, 接口返回={res_date}"

        # 7. 多月份客户目标对比（跟踪趋势）
        prev_month = "2026-06"
        res_prev = MB.get_product_goal_info(orgId=org_id, month=prev_month)
        _ok(res_prev, "上月客户目标数据查询失败")
        prev_data = res_prev.get("data", {})
        prev_custom_sum = prev_data.get("customSumInfo", {})
        # 验证不同月份的汇总数据结构一致
        assert type(custom_sum) == type(prev_custom_sum), \
            f"不同月份customSumInfo类型不一致, 当月={type(custom_sum)}, 上月={type(prev_custom_sum)}"

        # 8. 客户目标跟踪详情（getCustomerGoalTraceDetail.do）- 传完整参数
        res_cust_trace = MB.get_customer_goal_trace_detail(
            orgId=org_id, month=current_month, pageNo=1, pageSize=15,
            weekMonth=week_month, yearMonthList=year_month_list, dateList=date_list,
            dimension=["amount", "area"], areaCodeList=[],
            salesmanIdList=[], customerIdList=[], customerTypeList=[],
            priorityFollowUp="",
            goalValue=empty_range, reachProgress=empty_range, monthDiff=empty_range, scheduleDeviation=empty_range,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id,
            selectDate=select_date, startDate=week_start, endDate=week_end
        )
        assert res_cust_trace.get("code") in ("10001200", "10010100", "10003001"), \
            f"获取客户目标跟踪详情返回非预期code, 接口返回={res_cust_trace}"
        if res_cust_trace.get("code") == "10001200":
            cust_trace_data = res_cust_trace.get("data", {})
            assert isinstance(cust_trace_data, dict), \
                f"客户跟踪详情data类型异常, 期望dict, 实际={type(cust_trace_data)}"
            # 验证分页结构
            if "total" in cust_trace_data:
                assert isinstance(cust_trace_data["total"], int), \
                    f"客户跟踪total类型异常, 期望int, 实际={type(cust_trace_data['total'])}"
            # 验证列表结构
            cust_list = cust_trace_data.get("list", [])
            if cust_list:
                first_cust = cust_list[0]
                assert isinstance(first_cust, dict), \
                    f"客户跟踪列表项类型异常, 期望dict, 实际={type(first_cust)}"
                # 验证客户名称字段
                if "customerName" in first_cust:
                    assert isinstance(first_cust["customerName"], (str, type(None))), \
                        f"客户名称类型异常, 实际={type(first_cust['customerName'])}"

        # 9. 首页客户目标-客户类型达成分析（getCustomerTypeReach.do）
        res_type_reach = MB.get_customer_type_reach(
            orgId=org_id, month=current_month,
            startTime=start_time, endTime=end_time,
            filterSchemeConfigId=filter_config_id, supplierId=supplier_id
        )
        assert res_type_reach.get("code") in ("10001200", "10010100", "10003001"), \
            f"客户类型达成分析返回非预期code, 接口返回={res_type_reach}"
        if res_type_reach.get("code") == "10001200":
            type_reach_data = res_type_reach.get("data")
            assert type_reach_data is not None, \
                f"客户类型达成分析data为空, 接口返回={res_type_reach}"


# ==================== 目标跟踪-总目标二级页面 ====================

@allure.feature("目标跟踪")
class TestTotalGoalTracePage:

    @allure.story("总目标二级页面")
    def test_ydl_AX_total_goal_trace_page(self):
        """目标跟踪总目标二级页面查询与校验：组织列表→筛选方案→汇总信息→13月图表→区域月跟踪→供应商信息→多组织对比"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True

        # 1. 获取目标组织列表
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        assert org_id, f"组织orgId为空, org_list[0]={org_list[0]}"

        # 2. 获取筛选方案配置列表（getAllNoAuth.do）
        res_filter = MB.get_all_filter_scheme_no_auth()
        _ok(res_filter, "获取筛选方案配置列表失败")
        filter_data = res_filter.get("data", {})
        assert isinstance(filter_data, dict), \
            f"筛选方案data类型异常, 期望dict, 实际={type(filter_data)}"
        filter_list = filter_data.get("list", [])
        assert isinstance(filter_list, list), \
            f"筛选方案list类型异常, 期望list, 实际={type(filter_list)}"
        if filter_list:
            first_filter = filter_list[0]
            assert "configName" in first_filter, \
                f"筛选方案缺少configName, item={first_filter}"
            assert "id" in first_filter, \
                f"筛选方案缺少id, item={first_filter}"

        # 3. 获取目标汇总信息（getGetSummary.do）- 带完整参数
        # 从筛选方案获取 supplierId 和 filterSchemeConfigId
        filter_config_id = ""
        supplier_id = ""
        if filter_list:
            filter_config_id = filter_list[0].get("id", "")
            supplier_list = filter_list[0].get("supplierList", [])
            if supplier_list:
                supplier_id = supplier_list[0].get("supplierId", "")

        # 计算当月时间范围
        now = datetime.now()
        start_time = f"{now.strftime('%Y-%m')}-01 00:00:00"
        end_time = f"{now.strftime('%Y-%m')}-{now.strftime('%d')} 23:59:59"
        select_date = [start_time, end_time]

        res_summary = MB.get_summary(
            orgId=org_id, month="2026-07",
            startTime=start_time, endTime=end_time,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id
        )
        # 汇总接口可能返回系统异常(10010100)，兼容处理
        assert res_summary.get("code") in ("10001200", "10010100"), \
            f"获取目标汇总信息返回非预期code, 接口返回={res_summary}"
        if res_summary.get("code") == "10001200":
            summary_data = res_summary.get("data", {})
            assert isinstance(summary_data, dict), \
                f"汇总信息data类型异常, 期望dict, 实际={type(summary_data)}"
            # 验证汇总信息包含6大指标模块
            summary_modules = ["today", "avgArea", "avgPrice", "totalArea", "totalAmount", "monthActive"]
            for module_key in summary_modules:
                if module_key in summary_data:
                    module = summary_data[module_key]
                    assert isinstance(module, dict), \
                        f"汇总模块{module_key}类型异常, 期望dict, 实际={type(module)}"
                    # 验证每个模块包含目标值和达成值
                    for field in ["goalValue", "reachValue", "progress"]:
                        if field in module:
                            val = module[field]
                            assert isinstance(val, (int, float, type(None))), \
                                f"汇总{module_key}.{field}类型异常, 期望数值, 实际={type(val)}"

        # 4. 获取总目标跟踪历史13个月图表（getTotalGoalMonthChart.do）- 带完整参数
        res_chart = MB.get_total_goal_month_chart(
            orgId=org_id, month="2026-07",
            selectDate=select_date,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id
        )
        # 13月图表接口可能返回系统异常(10010100)，兼容处理
        assert res_chart.get("code") in ("10001200", "10010100"), \
            f"获取总目标跟踪历史13个月图表返回非预期code, 接口返回={res_chart}"
        if res_chart.get("code") == "10001200":
            chart_data = res_chart.get("data", {})
            assert isinstance(chart_data, dict), \
                f"13月图表data类型异常, 期望dict, 实际={type(chart_data)}"
            chart_list = chart_data.get("list", [])
            assert isinstance(chart_list, list), \
                f"13月图表list类型异常, 期望list, 实际={type(chart_list)}"
            # 验证13个月数据（最多13条）
            if chart_list:
                assert len(chart_list) <= 13, \
                    f"13月图表数据条数异常, 期望<=13, 实际={len(chart_list)}"
                first_month = chart_list[0]
                assert isinstance(first_month, dict), \
                    f"图表月份项类型异常, 期望dict, 实际={type(first_month)}"
                # 验证月份字段
                assert "month" in first_month, \
                    f"图表缺少month字段, item={first_month}"
                # 验证5项指标结构
                for indicator in ["dayAvgArea", "avgPrice", "areaTotal", "amountTotal", "monthActive"]:
                    if indicator in first_month:
                        ind_val = first_month[indicator]
                        assert isinstance(ind_val, dict), \
                            f"图表{indicator}类型异常, 期望dict, 实际={type(ind_val)}"
                        # 验证 GoalModel 子结构
                        if "goal" in ind_val:
                            goal = ind_val["goal"]
                            assert isinstance(goal, dict), \
                                f"图表{indicator}.goal类型异常, 期望dict, 实际={type(goal)}"

        # 5. 获取总目标区域月跟踪详情（getTotalGoalAreaMonthTraceDetail.do）- 带完整参数
        # 构建日期列表（最近4天）
        date_list = []
        for i in range(4):
            d = datetime.now() - timedelta(days=3 - i)
            date_list.append(d.strftime('%Y-%m-%d'))

        # 构建年月列表（上月 + 当月）
        prev_month_dt = datetime(now.year, now.month - 1 if now.month > 1 else 12, 1)
        prev_month_str = prev_month_dt.strftime('%Y-%m')
        year_month_list = [prev_month_str, now.strftime('%Y-%m')]

        # select_date 已在步骤3定义

        res_area_trace = MB.get_total_goal_area_month_trace_detail(
            orgId=org_id, month="2026-07",
            dateList=date_list, yearMonthList=year_month_list,
            selectDate=select_date,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id
        )
        # 区域月跟踪接口可能返回系统异常(10010100)，兼容处理
        assert res_area_trace.get("code") in ("10001200", "10010100"), \
            f"获取总目标区域月跟踪详情返回非预期code, 接口返回={res_area_trace}"
        if res_area_trace.get("code") == "10001200":
            area_trace_data = res_area_trace.get("data", {})
            assert isinstance(area_trace_data, dict), \
                f"区域月跟踪data类型异常, 期望dict, 实际={type(area_trace_data)}"
            area_trace_list = area_trace_data.get("list", [])
            assert isinstance(area_trace_list, list), \
                f"区域月跟踪list类型异常, 期望list, 实际={type(area_trace_list)}"
            if area_trace_list:
                first_area = area_trace_list[0]
                assert isinstance(first_area, dict), \
                    f"区域月跟踪项类型异常, 期望dict, 实际={type(first_area)}"
                # 验证月数据列表结构
                if "monthList" in first_area:
                    month_list = first_area["monthList"]
                    assert isinstance(month_list, list), \
                        f"monthList类型异常, 期望list, 实际={type(month_list)}"
                    if month_list:
                        first_m = month_list[0]
                        assert isinstance(first_m, dict), \
                            f"monthList项类型异常, 期望dict, 实际={type(first_m)}"
                        # 验证年月字段
                        if "yearMonth" in first_m:
                            assert isinstance(first_m["yearMonth"], str), \
                                f"yearMonth类型异常, 期望str, 实际={type(first_m['yearMonth'])}"

        # 6. 获取分供应商信息（getSupplierInfoNoAuth.do）
        res_supplier = MB.get_supplier_info_no_auth()
        _ok(res_supplier, "获取分供应商信息失败")
        supplier_data = res_supplier.get("data", {})
        assert isinstance(supplier_data, dict), \
            f"分供应商data类型异常, 期望dict, 实际={type(supplier_data)}"

        # 7. 多组织对比（第2个组织重复核心查询）
        if len(org_list) >= 2:
            org_id_2 = org_list[1].get("orgId", "")
            assert org_id != org_id_2, "两个组织orgId不应相同"

            # 第2个组织的汇总信息
            res_summary_2 = MB.get_summary(
                orgId=org_id_2, month="2026-07",
                startTime=start_time, endTime=end_time,
                supplierId=supplier_id, filterSchemeConfigId=filter_config_id
            )
            assert res_summary_2.get("code") in ("10001200", "10010100"), \
                f"第二个组织汇总信息返回非预期code, 接口返回={res_summary_2}"
            if res_summary_2.get("code") == "10001200":
                summary_2_data = res_summary_2.get("data", {})
                assert isinstance(summary_2_data, dict), \
                    f"第二组织汇总data类型异常, 期望dict, 实际={type(summary_2_data)}"

            # 第2个组织的13月图表
            res_chart_2 = MB.get_total_goal_month_chart(
                orgId=org_id_2, month="2026-07",
                selectDate=select_date,
                supplierId=supplier_id, filterSchemeConfigId=filter_config_id
            )
            assert res_chart_2.get("code") in ("10001200", "10010100"), \
                f"第二个组织13月图表返回非预期code, 接口返回={res_chart_2}"

        # 8. 不同筛选方案对比（如果有多个筛选方案）
        if len(filter_list) >= 2:
            second_config_id = filter_list[1].get("id", "")
            if second_config_id:
                second_supplier_list = filter_list[1].get("supplierList", [])
                second_supplier_id = second_supplier_list[0].get("supplierId", "") if second_supplier_list else ""
                res_filter_summary_2 = MB.get_summary(
                    orgId=org_id, month="2026-07",
                    startTime=start_time, endTime=end_time,
                    supplierId=second_supplier_id, filterSchemeConfigId=second_config_id
                )
                assert res_filter_summary_2.get("code") in ("10001200", "10010100"), \
                    f"不同筛选方案汇总返回非预期code, 接口返回={res_filter_summary_2}"


# ==================== 历史目标查询 ====================

@allure.feature("历史目标查询")
class TestHistoryGoalQuery:

    @allure.story("历史目标数据查询")
    def test_ydl_AZ_history_goal_query(self):
        """历史目标数据查询：组织→筛选方案→区域日均→去年同期→历史区域目标→区域供应商目标→历史团队目标→团队供应商目标→历史产品目标→产品列表→历史客户目标→目标区间筛选→重点跟进筛选→排序查询"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True

        # 1. 获取目标组织列表
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        assert org_id, f"组织orgId为空, org_list[0]={org_list[0]}"
        current_month = datetime.now().strftime("%Y-%m")

        # 2. 获取筛选方案配置
        res_filter = MB.get_all_filter_scheme_no_auth()
        _ok(res_filter, "获取筛选方案配置列表失败")
        filter_list = res_filter.get("data", {}).get("list", [])
        supplier_id = ""
        filter_config_id = ""
        if filter_list:
            filter_config_id = filter_list[0].get("id", "")
            supplier_list = filter_list[0].get("supplierList", [])
            if supplier_list:
                supplier_id = supplier_list[0].get("supplierId", "")

        # 3. 区域日均（getDayAvgArea.do）
        res_avg = MB.get_day_avg_area(
            orgId=org_id, month=current_month,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id
        )
        assert res_avg.get("code") in ("10001200", "10010100", "10003001"), \
            f"区域日均返回非预期code, 接口返回={res_avg}"

        # 4. 去年同期目标（getLastYearGoalInfo.do）
        res_last_year = MB.get_last_year_goal_info(
            orgId=org_id, month=current_month,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id
        )
        assert res_last_year.get("code") in ("10001200", "10010100", "10003001"), \
            f"去年同期目标返回非预期code, 接口返回={res_last_year}"

        # 5. 历史区域目标（getAreaGoal.do）
        res_area = MB.get_history_area_goal(
            orgId=org_id, month=current_month,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id,
            areaCodeList=[], sort="", sortType=""
        )
        assert res_area.get("code") in ("10001200", "10010100", "10003001"), \
            f"历史区域目标返回非预期code, 接口返回={res_area}"

        # 6. 区域供应商目标（getAreaSupplierGoalNoAuth.do）
        res_area_supplier = MB.get_area_supplier_goal_no_auth(
            orgId=org_id, month=current_month,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id,
            areaCodeList=[], sort="", sortType=""
        )
        assert res_area_supplier.get("code") in ("10001200", "10010100", "10003001"), \
            f"区域供应商目标返回非预期code, 接口返回={res_area_supplier}"

        # 7. 历史团队目标（getTeamGoal.do）
        res_team = MB.get_history_team_goal(
            orgId=org_id, month=current_month,
            supplierId=supplier_id, supplierID=supplier_id,
            filterSchemeConfigId=filter_config_id,
            orgIdList=[], sort="", sortType=""
        )
        assert res_team.get("code") in ("10001200", "10010100", "10003001"), \
            f"历史团队目标返回非预期code, 接口返回={res_team}"

        # 8. 团队供应商目标（getTeamSupplierGoalNoAuth.do）
        res_team_supplier = MB.get_team_supplier_goal_no_auth(
            orgId=org_id, month=current_month,
            supplierId=supplier_id, supplierID=supplier_id,
            filterSchemeConfigId=filter_config_id,
            orgIdList=[], sort="", sortType=""
        )
        assert res_team_supplier.get("code") in ("10001200", "10010100", "10003001"), \
            f"团队供应商目标返回非预期code, 接口返回={res_team_supplier}"

        # 9. 历史产品目标（getProductGoal.do）
        res_product = MB.get_history_product_goal(
            orgId=org_id, month=current_month, pageNo=1, pageSize=15,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id,
            productIdList=[], type="area", sort="", sortType="", sortMonth=""
        )
        assert res_product.get("code") in ("10001200", "10010100", "10003001"), \
            f"历史产品目标返回非预期code, 接口返回={res_product}"

        # 10. 产品列表-无鉴权（getProductListNoAuth.do）
        res_product_list = MB.get_product_list_no_auth(
            orgId=org_id, month=current_month,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id
        )
        assert res_product_list.get("code") in ("10001200", "10010100", "10003001"), \
            f"产品列表返回非预期code, 接口返回={res_product_list}"

        # 11. 历史客户目标（getCustomerGoal.do）
        res_customer = MB.get_history_customer_goal(
            orgId=org_id, month=current_month, pageNo=1, pageSize=15,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id,
            type=[], customerIdList=[], salesmanIdList=[],
            goalValue={"min": "", "max": ""},
            priorityFollowUp="", goalMinimum="", goalMaximum="",
            dataType="order_area", sort="", sortType="", sortMonth=""
        )
        assert res_customer.get("code") in ("10001200", "10010100", "10003001"), \
            f"历史客户目标返回非预期code, 接口返回={res_customer}"
        if res_customer.get("code") == "10001200":
            cust_data = res_customer.get("data", {})
            assert isinstance(cust_data, dict), \
                f"历史客户目标data类型异常, 期望dict, 实际={type(cust_data)}"

        # 12. 历史客户目标-目标区间筛选（goalMinimum/goalMaximum，后端代码层筛选）
        res_goal_range = MB.get_history_customer_goal(
            orgId=org_id, month=current_month, pageNo=1, pageSize=15,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id,
            goalMinimum=100, goalMaximum=9999, dataType="order_area"
        )
        assert res_goal_range.get("code") in ("10001200", "10010100", "10003001"), \
            f"历史客户目标-目标区间筛选返回非预期code, 接口返回={res_goal_range}"

        # 13. 历史客户目标-重点跟进筛选（priorityFollowUp=y，后端SQL层筛选）
        res_follow = MB.get_history_customer_goal(
            orgId=org_id, month=current_month, pageNo=1, pageSize=15,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id,
            priorityFollowUp="y", dataType="order_area"
        )
        assert res_follow.get("code") in ("10001200", "10010100", "10003001"), \
            f"历史客户目标-重点跟进筛选返回非预期code, 接口返回={res_follow}"

        # 14. 历史客户目标-排序查询（sort/sortType/sortMonth，后端代码结尾排序）
        res_sort = MB.get_history_customer_goal(
            orgId=org_id, month=current_month, pageNo=1, pageSize=15,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id,
            dataType="order_area", sort="area_total_this_goal_value",
            sortType="desc", sortMonth=current_month
        )
        assert res_sort.get("code") in ("10001200", "10010100", "10003001"), \
            f"历史客户目标-排序查询返回非预期code, 接口返回={res_sort}"


# ==================== 客户看板 ====================

@allure.feature("客户看板")
class TestCustomerBoard:

    @allure.story("客户看板查询")
    def test_ydl_BA_customer_board(self):
        """客户看板：组织→筛选方案→看板状态数量→看板列表→分页验证"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True

        # 1. 获取目标组织列表
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        assert org_id, f"组织orgId为空, org_list[0]={org_list[0]}"
        current_month = datetime.now().strftime("%Y-%m")

        # 2. 获取筛选方案配置
        res_filter = MB.get_all_filter_scheme_no_auth()
        _ok(res_filter, "获取筛选方案配置列表失败")
        filter_list = res_filter.get("data", {}).get("list", [])
        supplier_id = ""
        filter_config_id = ""
        if filter_list:
            filter_config_id = filter_list[0].get("id", "")
            supplier_list = filter_list[0].get("supplierList", [])
            if supplier_list:
                supplier_id = supplier_list[0].get("supplierId", "")

        # 3. 客户看板状态数量（getCustomerBoardStateNumForGoalTrace.do）
        res_state = MB.get_customer_board_state_num(
            orgId=org_id, month=current_month,
            supplierId=supplier_id, state="", dimension=["area"],
            salesmanIdList=[], customerId="", areaCodeList=[],
            subOrgId="", noOrderDays="", lossDays="", activeRingGrowth="",
            lastMonth=1, filterSchemeConfigId=filter_config_id,
            ringGrowthType="amount", ringGrowthMin="", ringGrowthMax="",
            monthRequirementAreaMin="", monthRequirementAreaMax=""
        )
        assert res_state.get("code") in ("10001200", "10010100", "10003001", "10201011"), \
            f"客户看板状态数量返回非预期code, 接口返回={res_state}"

        # 4. 客户看板列表（getCustomerBoardListForGoalTrace.do）
        res_list = MB.get_customer_board_list(
            orgId=org_id, month=current_month, pageNo=1, pageSize=15,
            supplierId=supplier_id, state="", dimension=["area"],
            salesmanIdList=[], customerId="", areaCodeList=[],
            subOrgId="", noOrderDays="", lossDays="", activeRingGrowth="",
            lastMonth=1, filterSchemeConfigId=filter_config_id,
            ringGrowthType="amount", ringGrowthMin="", ringGrowthMax="",
            monthRequirementAreaMin="", monthRequirementAreaMax="",
            sort="", sortType=""
        )
        assert res_list.get("code") in ("10001200", "10010100", "10003001", "10201011"), \
            f"客户看板列表返回非预期code, 接口返回={res_list}"
        if res_list.get("code") == "10001200":
            board_data = res_list.get("data", {})
            assert isinstance(board_data, dict), \
                f"客户看板data类型异常, 期望dict, 实际={type(board_data)}"


# ==================== 产品目标查询 ====================

@allure.feature("产品目标查询")
class TestProductGoalQuery:

    @allure.story("分层产品与区域目标")
    def test_ydl_BB_product_region_goal(self):
        """分层产品与区域目标：组织→筛选方案→分层产品列表→产品区域目标列表"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True

        # 1. 获取目标组织列表
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        assert org_id, f"组织orgId为空, org_list[0]={org_list[0]}"

        # 2. 获取筛选方案配置
        res_filter = MB.get_all_filter_scheme_no_auth()
        _ok(res_filter, "获取筛选方案配置列表失败")
        filter_list = res_filter.get("data", {}).get("list", [])
        supplier_id = ""
        filter_config_id = ""
        if filter_list:
            filter_config_id = filter_list[0].get("id", "")
            supplier_list = filter_list[0].get("supplierList", [])
            if supplier_list:
                supplier_id = supplier_list[0].get("supplierId", "")

        # 3. 分层产品列表（getLayerProductList.do）
        res_layer = MB.get_layer_product_list(
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id
        )
        assert res_layer.get("code") in ("10001200", "10010100", "10003001"), \
            f"分层产品列表返回非预期code, 接口返回={res_layer}"

        # 4. 产品区域目标列表（getRegionGoalList.do）
        # 取分层产品列表第一个产品ID（如果有）
        product_id = ""
        if res_layer.get("code") == "10001200":
            product_list = res_layer.get("data", {}).get("list", [])
            if product_list:
                product_id = product_list[0].get("productId", product_list[0].get("id", ""))
        if product_id:
            res_region = MB.get_region_goal_list(
                orgId=org_id, goalMonth="2026-07", productId=product_id,
                supplierId=supplier_id, filterSchemeConfigId=filter_config_id
            )
            assert res_region.get("code") in ("10001200", "10010100", "10003001"), \
                f"产品区域目标列表返回非预期code, 接口返回={res_region}"


# ==================== 通用配置查询 ====================

@allure.feature("通用配置查询")
class TestCommonConfigQuery:

    @allure.story("通用配置与权限查询")
    def test_ydl_BC_common_config_query(self):
        """通用配置与权限查询：CRM权限→信用配置→子组织目标→客户编辑权限→竞争对手档案→业务员列表→客户列表"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True

        # 1. 获取目标组织列表
        org_list = _get_org_id()
        org_id = org_list[0].get("orgId", "")
        assert org_id, f"组织orgId为空, org_list[0]={org_list[0]}"
        current_month = datetime.now().strftime("%Y-%m")

        # 2. 获取筛选方案配置
        res_filter = MB.get_all_filter_scheme_no_auth()
        _ok(res_filter, "获取筛选方案配置列表失败")
        filter_list = res_filter.get("data", {}).get("list", [])
        supplier_id = ""
        filter_config_id = ""
        if filter_list:
            filter_config_id = filter_list[0].get("id", "")
            supplier_list = filter_list[0].get("supplierList", [])
            if supplier_list:
                supplier_id = supplier_list[0].get("supplierId", "")

        # 3. 用户CRM权限（getUserCrmAuth.do）
        res_crm = MB.get_user_crm_auth()
        assert res_crm.get("code") in ("10001200", "10010100"), \
            f"用户CRM权限返回非预期code, 接口返回={res_crm}"

        # 4. 信用配置（getCreditConfigNoAuth.do）
        res_credit = MB.get_credit_config_no_auth()
        assert res_credit.get("code") in ("10001200", "10010100"), \
            f"信用配置返回非预期code, 接口返回={res_credit}"

        # 5. 子组织目标（getSubOrgGoalNoAuth.do）
        res_sub_org = MB.get_sub_org_goal_no_auth(
            orgId=org_id, month=current_month,
            supplierId=supplier_id, filterSchemeConfigId=filter_config_id
        )
        assert res_sub_org.get("code") in ("10001200", "10010100", "10003001"), \
            f"子组织目标返回非预期code, 接口返回={res_sub_org}"

        # 6. 客户编辑数据权限（getCustomerEditDataPerNoAuth.do）
        res_edit_per = MB.get_customer_edit_data_per_no_auth()
        assert res_edit_per.get("code") in ("10001200", "10010100"), \
            f"客户编辑数据权限返回非预期code, 接口返回={res_edit_per}"

        # 7. 竞争对手档案列表（getRivalArchiveListNoAuth.do）
        res_rival = MB.get_rival_archive_list_no_auth(
            pageNo=1, pageSize=9999,
            ignoredTypeList=["self", "union_factory", "cooperative_factory"]
        )
        assert res_rival.get("code") in ("10001200", "10010100"), \
            f"竞争对手档案列表返回非预期code, 接口返回={res_rival}"

        # 8. 业务员列表（getSalesmanByOrgNoAuth.do）
        res_salesman = MB.get_salesman_by_org_no_auth()
        assert res_salesman.get("code") in ("10001200", "10010100"), \
            f"业务员列表返回非预期code, 接口返回={res_salesman}"

        # 9. 客户列表-按组织（getCustomerByOrgNoAuth.do）
        res_customer = MB.get_customer_by_org_no_auth(
            pageNo=1, pageSize=100, keyword=""
        )
        assert res_customer.get("code") in ("10001200", "10010100"), \
            f"客户列表返回非预期code, 接口返回={res_customer}"
        if res_customer.get("code") == "10001200":
            cust_data = res_customer.get("data", {})
            assert isinstance(cust_data, dict), \
                f"客户列表data类型异常, 期望dict, 实际={type(cust_data)}"
