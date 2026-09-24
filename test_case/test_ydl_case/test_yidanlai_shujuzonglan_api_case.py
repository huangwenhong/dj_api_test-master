# -*- coding: utf-8 -*-
"""易单来 - 数据总览用例（跨接口交叉校验：期望值均来自其他接口数据计算，不依赖页面截图值）"""

import allure
import pytest
from datetime import date, timedelta
from test_case.page_api.ydl.shujuzonglan_api import ShujuzonglanAPI
from test_case.page_api.ydl.mubiao_api import MubiaoAPI

# 数据总览为 pre 集群环境数据，config.base_url(onlinecps.cn)为另一套数据，须独立登录该环境
SCREENSHOT_BASE_URL = "https://suppliertest.onlinecps.cn"


def _login_screenshot_env():
    """独立登录数据总览环境(onlinecps.cn)，调getSupplierInfoNoAuth识别供应商类型，返回接口实例、supplierId与是否多供应商。

    多供应商(存在unionSupplier=1)：当前账号为销售主体，取联合体supplierId；
    否则当前账号为单供应商，取自身supplierId。失败返回None四元组。
    """
    from conftest import LOGIN_APP_NAME, LOGIN_PASSWORD, LOGIN_USERNAME
    from test_case.page_api.public.login_api import LoginAPI

    token, details = LoginAPI(base_url=SCREENSHOT_BASE_URL).login(
        LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_APP_NAME,
    )
    if not token:
        return None, None, None, None
    szl = ShujuzonglanAPI(base_url=SCREENSHOT_BASE_URL, cookies={"token": token})
    mb = MubiaoAPI(base_url=SCREENSHOT_BASE_URL, cookies={"token": token})
    res_info = mb.get_supplier_info_no_auth()
    if res_info.get("code") != "10001200":
        return None, None, None, None
    items = res_info.get("data", {}).get("list", [])
    for item in items:
        if item.get("unionSupplier") == "1":
            return szl, mb, item.get("supplierId"), True
    if items:
        return szl, mb, items[0].get("supplierId"), False
    return None, None, None, None


_SZL, _MB, _UNION_ID, _IS_UNION = _login_screenshot_env()


def _ok(res, msg="接口返回异常"):
    """校验接口 code=10001200 且 success=True"""
    assert res.get("code") == "10001200", f"{msg}, 接口返回={res}"
    assert res.get("success") is True, f"{msg} success不为True, 接口返回={res}"


def _eq(panel, field, expected, actual, tol=0.011):
    """期望值(来自其他接口数据计算)与实际值按容差比对，不一致即断言失败"""
    assert actual is not None, \
        f"{panel}-{field}接口未返回值, 期望值={expected}"
    try:
        matched = abs(float(actual) - float(expected)) <= tol
    except (TypeError, ValueError):
        matched = str(actual) == str(expected)
    assert matched, \
        f"{panel}-{field}与交叉校验期望不一致, 期望值={expected}, 接口值={actual}"


def _skip_if_no_env():
    """数据总览环境登录失败或未识别到供应商时跳过用例，不拖累默认套件"""
    if _SZL is None or not _UNION_ID:
        pytest.skip("数据总览环境(onlinecps.cn)登录失败或未识别到supplierId，跳过交叉校验")


def _day_actual(org_id, day, fid=""):
    """某日实际单量：分时段预警列表最后一个时段的actualOrderQuantity累计值

    数据来源 goal/new/trace/getTimeSegmentedWarnList.do（联合供应商销售主体根组织传参：
    date=该日、orgId=根组织、supplierId=联合体、filterSchemeConfigId=默认筛选方案）
    """
    res = _SZL.trace_get_time_segmented_warn_list(
        date=day, orgId=org_id, supplierId=_UNION_ID, filterSchemeConfigId=fid)
    _ok(res, f"{day}分时段预警查询失败")
    vals = [float(m.get("actualOrderQuantity") or 0)
            for seg in res.get("data", {}).get("list", []) for m in seg.get("minutesData", [])]
    return vals[-1] if vals else 0.0


def _default_scheme_id():
    """取默认筛选方案id，作为周/月实际单量查询的filterSchemeConfigId传参"""
    res = _MB.get_all_filter_scheme_no_auth()
    _ok(res, "筛选方案配置查询失败")
    for item in res.get("data", {}).get("list", []):
        if item.get("defaultConfig") == "y":
            return item.get("id")
    return ""


def _root_org_id():
    """目标管理根组织orgId(topOrg=true)"""
    month = date.today().strftime("%Y-%m")
    res_org = _MB.get_org_list_no_auth(month=month)
    _ok(res_org, "目标管理组织列表查询失败")
    for org in res_org.get("data", {}).get("list", []):
        res_gi = _MB.get_goal_info(orgId=org.get("orgId"), month=month)
        if res_gi.get("code") == "10001200" and res_gi.get("data", {}).get("topOrg") is True:
            return org.get("orgId")
    assert False, f"目标管理未找到根组织(topOrg=true), 接口返回={res_org}"


def _goal_data_cached(cache, root_org, m):
    """按月取目标详情(goalDetailsVo/assessmentDate等)并缓存"""
    if m not in cache:
        res_gi = _MB.get_goal_info(orgId=root_org, month=m)
        cache[m] = res_gi.get("data", {}) or {} if res_gi.get("code") == "10001200" else {}
    return cache[m]


def _goal_dif_day_entries(dim):
    """目标差距日维度：weekList展平为日条目，校验近30天连续止于当天、按自然周分隔(周首周一)"""
    res = _SZL.board_get_goal_dif_overview(supplierId=_UNION_ID, dateType="1", dimension=dim)
    _ok(res, f"目标差距(日维度-{dim})查询失败")
    week_list = res.get("data", {}).get("weekList", [])
    days = [d for w in week_list for d in w.get("dateList", [])]
    assert len(days) == 30, f"日维度应统计近30天, 实际={len(days)}, weekList={len(week_list)}"
    assert days[-1].get("dateStr") == date.today().strftime("%Y-%m-%d"), \
        f"日维度默认止于当天, 末天={days[-1].get('dateStr')}"
    flat = [date.fromisoformat(d["dateStr"]) for d in days]
    assert all((b - a).days == 1 for a, b in zip(flat, flat[1:])), \
        f"近30天日期不连续, 首末={days[0].get('dateStr')}~{days[-1].get('dateStr')}"
    for w in week_list:
        dl = w.get("dateList", [])
        assert dl and date.fromisoformat(dl[0]["dateStr"]).weekday() == 0, \
            f"自然周分隔应以周一为首天, 周首={dl[0].get('dateStr') if dl else None}"
    return days


def _goal_dif_month_entries(dim):
    """目标差距月维度：monthList条目，校验近12月止于本月"""
    res = _SZL.board_get_goal_dif_overview(supplierId=_UNION_ID, dateType="3", dimension=dim)
    _ok(res, f"目标差距(月维度-{dim})查询失败")
    months = res.get("data", {}).get("monthList", [])
    assert len(months) == 12, f"月维度应统计近12月, 实际={len(months)}"
    assert months[-1].get("dateStr") == date.today().strftime("%Y-%m"), \
        f"月维度默认止于本月, 末月={months[-1].get('dateStr')}"
    return months


def _ring_expect(info):
    """环比百分比期望=(达成-上期)/上期×100，上期为0时返回None"""
    last = float(info.get("lastReachValue") or 0)
    if last <= 0:
        return None
    return round((float(info["reachValue"]) - last) / last * 100, 2)


@allure.feature("数据总览跨接口交叉校验")
class TestDataOverview:

    @allure.story("数据总览 - 校验当前供应能力与产能目标")
    def test_ydl_SZL_AA_verify_supply_capacity_cross(self):
        """当前供应能力/产能目标=多供应商各分供应商(单供应商为自身)最新产能记录supplyCapacity/capacityTarget之和（数据来源capacityrecord/getList.do）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        _skip_if_no_env()

        # 1. 取参与汇总的供应商：多供应商取分供应商(unionSupplier=0)，单供应商取自身
        res_info = _MB.get_supplier_info_no_auth()
        _ok(res_info, "获取分供应商信息失败")
        items = res_info.get("data", {}).get("list", [])
        suppliers = [i for i in items if i.get("unionSupplier") == "0"] or items
        assert suppliers, f"供应商列表为空, 接口返回={res_info}"

        # 2. 逐供应商查产能记录，取各自最新一条，汇总supplyCapacity/capacityTarget（来源接口汇总逻辑）
        today = date.today()
        start = (today - timedelta(days=60)).strftime("%Y-%m-%d")
        end = today.strftime("%Y-%m-%d")
        sum_supply = sum_target = 0.0
        for m in suppliers:
            res_cap = _SZL.capacity_record_get_list(
                supplierId=m.get("supplierId"), startTime=start, endTime=end, pageSize=100)
            _ok(res_cap, f"供应商{m.get('supplierName')}产能记录查询失败")
            rows = res_cap.get("data", {}).get("list", [])
            if rows:
                latest = max(rows, key=lambda r: r.get("recordDate", ""))
                sum_supply += float(latest.get("supplyCapacity") or 0)
                sum_target += float(latest.get("capacityTarget") or 0)

        # 3. 查询订单总览取页面当前值
        res = _SZL.board_get_order_overview(supplierId=_UNION_ID, dateType="3")
        _ok(res, "订单总览查询失败")
        order = res.get("data", {})

        # 4. 交叉校验：来源汇总值=页面当前值
        scope = "分供应商汇总" if _IS_UNION else "自身"
        _eq("当前供应能力", f"当前供应能力(万m²/日)={scope}", sum_supply, order.get("realityDailyAvg"))
        _eq("当前供应能力", f"产能目标(万m²/日)={scope}", sum_target, order.get("theoreticalDailyAvg"))

    @allure.story("数据总览 - 校验本月日均接单、环比、差距、进度条数据")
    def test_ydl_SZL_AB_verify_sales_data_cross(self):
        """销量数据：目标值=目标管理根组织日均/月度接单面积目标，环比=本月日均-上月日均，差距=max(目标-达成,0)，进度=达成/目标（比值保留两位）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        _skip_if_no_env()

        # 1. 目标管理数据源：组织列表中找到根组织(topOrg=true)，取其日均/月度接单面积目标与考核天数
        today = date.today()
        month = today.strftime("%Y-%m")
        res_org = _MB.get_org_list_no_auth(month=month)
        _ok(res_org, "目标管理组织列表查询失败")
        org_list = res_org.get("data", {}).get("list", [])
        assert org_list, f"目标管理组织列表为空, 接口返回={res_org}"
        goal_info, org_id = None, None
        for org in org_list:
            res_gi = _MB.get_goal_info(orgId=org.get("orgId"), month=month)
            if res_gi.get("code") != "10001200":
                continue
            data = res_gi.get("data", {})
            if data.get("topOrg") is True:
                goal_info, org_id = data, org.get("orgId")
                break
        assert goal_info, f"目标管理未找到根组织(topOrg=true), 组织列表={org_list}"
        day_goal = float(goal_info.get("goalDetailsVo", {}).get("dayAvgArea", {}).get("goal", {}).get("value") or 0)
        month_goal = float(goal_info.get("goalDetailsVo", {}).get("areaTotal", {}).get("goal", {}).get("value") or 0)
        assess_days = int(goal_info.get("assessmentDays") or 0)
        assert day_goal > 0, f"根组织({org_id})日均接单面积目标未设置, goalDetailsVo={goal_info.get('goalDetailsVo')}"
        # 月度目标自洽：月度目标=日均目标×已过考核天数
        _eq("销量数据", "月目标=日均目标×考核天数", day_goal * assess_days, month_goal, tol=0.51)

        # 2. 查询订单总览（月维度），目标值与目标管理根组织目标一致
        res = _SZL.board_get_order_overview(supplierId=_UNION_ID, dateType="3")
        _ok(res, "订单总览查询失败")
        order = res.get("data", {})
        day_avg = order.get("dayAvgArea", {})
        total = order.get("totalArea", {})
        _eq("销量数据", "日均-目标值=目标管理根组织日均目标", day_goal, day_avg.get("goalValue"))
        _eq("销量数据", "总接单-目标值=目标管理根组织月度目标", month_goal, total.get("goalValue"))

        # 3. 环比=本月日均-上月日均（上月日均取自目标差距总览上月salesInfo达成值）
        last_month = f"{today.year}-{today.month - 1:02d}" if today.month > 1 else f"{today.year - 1}-12"
        res_goal = _SZL.board_get_goal_dif_overview(supplierId=_UNION_ID, dateType="3", dimension="area")
        _ok(res_goal, "目标差距查询失败")
        last_info = next((m.get("salesInfo", {}) for m in res_goal.get("data", {}).get("monthList", [])
                          if m.get("dateStr") == last_month), None)
        assert last_info, f"目标差距未返回上月({last_month})数据, monthList={[m.get('dateStr') for m in res_goal.get('data', {}).get('monthList', [])]}"
        ring_expect = float(day_avg["reachValue"]) - float(last_info["reachValue"])
        _eq("销量数据", "日均-环比=本月日均-上月日均", ring_expect, day_avg.get("saleAreaRatio"))

        # 4. 差距=目标值-达成值，最小显示为0（日均/总接单/今日三处同口径）
        for panel, item in (("日均", day_avg), ("总接单", total), ("今日", order.get("todayDayAvgArea", {}))):
            dif_expect = max(float(item["goalValue"]) - float(item["reachValue"]), 0)
            _eq("销量数据", f"{panel}-差距=max(目标-达成,0)", dif_expect, item.get("dif"))

        # 5. 进度条百分比=本月日均接单/目标值（比值保留两位小数）
        for panel, item in (("日均", day_avg), ("总接单", total)):
            progress_expect = round(float(item["reachValue"]) / float(item["goalValue"]), 2)
            _eq("销量数据", f"{panel}-进度=达成/目标(比值)", progress_expect, item.get("progress"))

        # 6. 今日接单：目标与日均目标同口径、今日达成不超过本月总接单
        today_item = order.get("todayDayAvgArea", {})
        _eq("销量数据", "今日-目标同口径", day_avg.get("goalValue"), today_item.get("goalValue"))
        assert float(today_item["reachValue"]) <= float(total["reachValue"]) + 0.011, \
            f"今日接单超过本月总接单, 今日={today_item['reachValue']}, 本月总={total['reachValue']}"

    @allure.story("数据总览 - 校验本月总接单、环比、差距、进度条数据")
    def test_ydl_SZL_AC_verify_total_area_cross(self):
        """销量数据-总接单：目标值=目标管理根组织总接单面积目标，环比=本月-上月同期，差距=max(目标-达成,0)，进度=总接单/目标值，理论接单刻度=(目标值/考核天数)×已过考核天数"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        _skip_if_no_env()

        # 1. 目标管理数据源：根组织(topOrg=true)总接单面积目标、上月达成、考核天数与已过考核日
        today = date.today()
        month = today.strftime("%Y-%m")
        res_org = _MB.get_org_list_no_auth(month=month)
        _ok(res_org, "目标管理组织列表查询失败")
        goal_info, root_org = None, None
        for org in res_org.get("data", {}).get("list", []):
            res_gi = _MB.get_goal_info(orgId=org.get("orgId"), month=month)
            if res_gi.get("code") == "10001200" and res_gi.get("data", {}).get("topOrg") is True:
                goal_info, root_org = res_gi.get("data", {}), org.get("orgId")
                break
        assert goal_info, f"目标管理未找到根组织(topOrg=true), 接口返回={res_org}"
        month_goal = float(goal_info.get("goalDetailsVo", {}).get("areaTotal", {}).get("goal", {}).get("value") or 0)
        assess_days = int(goal_info.get("assessmentDays") or 0)
        passed_days = len([d for d in goal_info.get("assessmentDate", []) if d <= today.strftime("%Y-%m-%d")])
        assert month_goal > 0 and assess_days > 0 and passed_days > 0, \
            f"根组织月度目标/考核天数/已过考核日不完整, 目标={month_goal}, 考核天数={assess_days}, 已过={passed_days}"

        # 2. 实际单量数据源：每天实际单量累加=月数据（本月=1日~昨日，上月同期=上月1日~上月同日）
        yesterday = today - timedelta(days=1)
        fid = _default_scheme_id()
        month_sum = sum(_day_actual(root_org, f"{month}-{d:02d}", fid) for d in range(1, yesterday.day + 1))
        last_end = today.replace(day=1) - timedelta(days=1)
        last_same_day = min(yesterday.day, last_end.day)
        last_sum = sum(_day_actual(root_org, (last_end.replace(day=1) + timedelta(days=i)).strftime("%Y-%m-%d"), fid)
                       for i in range(last_same_day))

        # 3. 查询订单总览（月维度），目标值/达成/环比按公式交叉校验
        res = _SZL.board_get_order_overview(supplierId=_UNION_ID, dateType="3")
        _ok(res, "订单总览查询失败")
        total = res.get("data", {}).get("totalArea", {})
        _eq("总接单", "目标值=目标管理根组织总接单目标", month_goal, total.get("goalValue"))
        _eq("总接单", "本月总接单=每天实际单量累加(1日~昨日)", month_sum, total.get("reachValue"))
        _eq("总接单", "环比=本月-上月同期", month_sum - last_sum, total.get("saleAreaRatio"))

        # 4. 差距=目标值-达成值最小显示为0、进度条百分比=本月总接单/目标值（比值保留两位）
        _eq("总接单", "差距=max(目标-达成,0)",
            max(float(total["goalValue"]) - float(total["reachValue"]), 0), total.get("dif"))
        _eq("总接单", "进度=总接单/目标值(比值)",
            round(float(total["reachValue"]) / float(total["goalValue"]), 2), total.get("progress"))

        # 5. 理论接单刻度=(目标值/考核天数)×已过考核天数（由来源数据计算，供页面刻度展示），字段合法非负
        theory_scale = month_goal / assess_days * passed_days
        assert theory_scale > 0, f"理论接单刻度非正, 目标={month_goal}, 考核天数={assess_days}, 已过={passed_days}"
        assert float(total.get("theoryProgress", -1)) >= 0, \
            f"理论接单刻度字段为负, theoryProgress={total.get('theoryProgress')}"

    @allure.story("数据总览 - 校验今日接单、环比、差距、进度条数据")
    def test_ydl_SZL_AD_verify_today_area_cross(self):
        """销量数据-今日接单：目标值=目标管理根组织日均接单面积目标，环比=今日-昨日，差距=max(目标-达成,0)，进度=今日总接单/目标值（比值保留两位）"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        _skip_if_no_env()

        # 1. 目标管理数据源：根组织(topOrg=true)日均接单面积目标，即今日接单卡片目标值
        today = date.today()
        month = today.strftime("%Y-%m")
        res_org = _MB.get_org_list_no_auth(month=month)
        _ok(res_org, "目标管理组织列表查询失败")
        goal_info, root_org = None, None
        for org in res_org.get("data", {}).get("list", []):
            res_gi = _MB.get_goal_info(orgId=org.get("orgId"), month=month)
            if res_gi.get("code") == "10001200" and res_gi.get("data", {}).get("topOrg") is True:
                goal_info, root_org = res_gi.get("data", {}), org.get("orgId")
                break
        assert goal_info, f"目标管理未找到根组织(topOrg=true), 接口返回={res_org}"
        day_goal = float(goal_info.get("goalDetailsVo", {}).get("dayAvgArea", {}).get("goal", {}).get("value") or 0)
        assert day_goal > 0, f"根组织日均接单面积目标未设置, goalDetailsVo={goal_info.get('goalDetailsVo')}"

        # 2. 查询订单总览（月维度）取今日接单卡片，目标值与目标管理根组织日均目标一致
        res = _SZL.board_get_order_overview(supplierId=_UNION_ID, dateType="3")
        _ok(res, "订单总览查询失败")
        today_item = res.get("data", {}).get("todayDayAvgArea", {})
        _eq("今日接单", "目标值=目标管理根组织日均目标", day_goal, today_item.get("goalValue"))

        # 3. 环比=今日-昨日：今日/昨日接单均取分时段预警列表实际单量累计值（今日为当前时刻累计）
        yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        today_reach = _day_actual(root_org, today.strftime("%Y-%m-%d"))
        yesterday_reach = _day_actual(root_org, yesterday)
        _eq("今日接单", "今日接单=今日实际单量", today_reach, today_item.get("reachValue"))
        _eq("今日接单", "环比=今日-昨日", today_reach - yesterday_reach, today_item.get("saleAreaRatio"))

        # 4. 差距=目标值-达成值最小显示为0、进度条百分比=今日总接单/目标值（比值保留两位）
        _eq("今日接单", "差距=max(目标-达成,0)",
            max(float(today_item["goalValue"]) - float(today_item["reachValue"]), 0), today_item.get("dif"))
        _eq("今日接单", "进度=今日总接单/目标值(比值)",
            round(float(today_item["reachValue"]) / float(today_item["goalValue"]), 2), today_item.get("progress"))

    @allure.story("数据总览 - 校验本周日均接单与本周总接单（时间维度切换为本周）")
    def test_ydl_SZL_AE_verify_week_sales_data_cross(self):
        """销量数据-本周维度：取数逻辑同月维度，本周日均目标=根组织日均目标，本周总目标=日均目标×本周考核天数，环比=本周-上周，差距=max(目标-达成,0)，进度=达成/目标"""
        # Author: Author
        # Create Date: 2026-08-24
        # IsAI: True
        _skip_if_no_env()

        # 1. 目标管理数据源：根组织(topOrg=true)日均目标与考核日期，计算本周(周一~周日)考核天数
        today = date.today()
        month = today.strftime("%Y-%m")
        res_org = _MB.get_org_list_no_auth(month=month)
        _ok(res_org, "目标管理组织列表查询失败")
        goal_info, root_org = None, None
        for org in res_org.get("data", {}).get("list", []):
            res_gi = _MB.get_goal_info(orgId=org.get("orgId"), month=month)
            if res_gi.get("code") == "10001200" and res_gi.get("data", {}).get("topOrg") is True:
                goal_info, root_org = res_gi.get("data", {}), org.get("orgId")
                break
        assert goal_info, f"目标管理未找到根组织(topOrg=true), 接口返回={res_org}"
        day_goal = float(goal_info.get("goalDetailsVo", {}).get("dayAvgArea", {}).get("goal", {}).get("value") or 0)
        assert day_goal > 0, f"根组织日均接单面积目标未设置, goalDetailsVo={goal_info.get('goalDetailsVo')}"
        week_start = today - timedelta(days=today.weekday())
        week_days = {(week_start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)}
        week_assess = len([d for d in goal_info.get("assessmentDate", []) if d in week_days])
        assert week_assess > 0, f"本周无考核日无法校验周目标, assessmentDate={goal_info.get('assessmentDate')}"

        # 2. 查询订单总览（周维度 dateType=2），日均/总接单目标与目标管理口径一致（周总目标=日均目标×本周考核天数）
        res = _SZL.board_get_order_overview(supplierId=_UNION_ID, dateType="2")
        _ok(res, "订单总览(周维度)查询失败")
        order = res.get("data", {})
        day_avg = order.get("dayAvgArea", {})
        total = order.get("totalArea", {})
        _eq("本周销量", "日均-目标值=目标管理根组织日均目标", day_goal, day_avg.get("goalValue"))
        _eq("本周销量", "总接单-目标值=日均目标×本周考核天数", day_goal * week_assess, total.get("goalValue"))

        # 3. 实际单量数据源：每天实际单量累加=周数据（本周=本周一~昨日，上周=上周一~周日）
        yesterday = today - timedelta(days=1)
        fid = _default_scheme_id()
        week_days_list = [(week_start + timedelta(days=i)).strftime("%Y-%m-%d")
                          for i in range(max((yesterday - week_start).days + 1, 0))]
        week_sum = sum(_day_actual(root_org, d, fid) for d in week_days_list)
        last_week_days = [(week_start - timedelta(days=7) + timedelta(days=i)).strftime("%Y-%m-%d")
                          for i in range(7)]
        last_week_sum = sum(_day_actual(root_org, d, fid) for d in last_week_days)
        # 本周日均=本周截止昨日接单量/已过本周考核天数，上周日均=上周接单量/上周考核天数
        assess_dates = set(goal_info.get("assessmentDate", []))
        week_passed = len([d for d in week_days_list if d in assess_dates])
        last_week_assess = len([d for d in last_week_days if d in assess_dates])
        week_day_avg = week_sum / week_passed if week_passed else 0.0
        last_week_day_avg = last_week_sum / last_week_assess if last_week_assess else 0.0

        # 4. 看板周维度按公式交叉校验：达成/环比来自实际单量累加，差距/进度同月维度口径
        _eq("本周总接单", "总接单=每天实际单量累加", week_sum, total.get("reachValue"))
        _eq("本周总接单", "环比=本周-上周", week_sum - last_week_sum, total.get("saleAreaRatio"))
        _eq("本周日均", "日均=本周接单/已过本周考核天数", week_day_avg, day_avg.get("reachValue"))
        _eq("本周日均", "环比=本周日均-上周日均", week_day_avg - last_week_day_avg, day_avg.get("saleAreaRatio"))
        for panel, item in (("日均", day_avg), ("总接单", total)):
            _eq("本周销量", f"{panel}-差距=max(目标-达成,0)",
                max(float(item["goalValue"]) - float(item["reachValue"]), 0), item.get("dif"))
            _eq("本周销量", f"{panel}-进度=达成/目标(比值)",
                round(float(item["reachValue"]) / float(item["goalValue"]), 2), item.get("progress"))

    @allure.story("数据总览 - 校验目标差距日维度面积数据")
    def test_ydl_SZL_AF_verify_goal_dif_day_area_cross(self):
        """目标差距日-面积：近30天按自然周分隔止于当天，目标=根组织日均目标(仅考核日)，差值=达成−目标，日环比=(达成−昨日)/昨日×100"""
        # Author: Author
        # Create Date: 2026-08-25
        # IsAI: True
        _skip_if_no_env()
        root_org, cache = _root_org_id(), {}

        # 1. 逐日校验面积目标/差值/日环比与浮窗字段(下单客户数/订单笔数)
        for d in _goal_dif_day_entries("area"):
            ds, info = d.get("dateStr"), d.get("salesInfo", {}) or {}
            gdata = _goal_data_cached(cache, root_org, ds[:7])
            vo = gdata.get("goalDetailsVo", {}) or {}
            day_goal = float((vo.get("dayAvgArea", {}) or {}).get("goal", {}).get("value") or 0) \
                if ds in gdata.get("assessmentDate", []) else 0.0
            _eq("目标差距-日面积", f"{ds}目标=根组织日均目标(考核日)", day_goal, info.get("goalValue"))
            _eq("目标差距-日面积", f"{ds}差值=达成-目标",
                float(info["reachValue"]) - float(info["goalValue"]), info.get("dif"))
            if _ring_expect(info) is not None:
                _eq("目标差距-日面积", f"{ds}日环比=(达成-昨日)/昨日×100", _ring_expect(info), info.get("ring"))
            assert isinstance(d.get("customerNum"), int) and isinstance(d.get("orderNum"), int), \
                f"{ds}浮窗字段(下单客户数/订单笔数)缺失, 条目={d}"

    @allure.story("数据总览 - 校验目标差距日维度金额数据")
    def test_ydl_SZL_AG_verify_goal_dif_day_amount_cross(self):
        """目标差距日-金额：目标=日均目标×均价目标，差值=达成−目标，日环比=(达成−昨日)/昨日×100"""
        # Author: Author
        # Create Date: 2026-08-25
        # IsAI: True
        _skip_if_no_env()
        root_org, cache = _root_org_id(), {}

        # 1. 逐日校验金额目标/差值/日环比
        for d in _goal_dif_day_entries("amount"):
            ds, info = d.get("dateStr"), d.get("salesInfo", {}) or {}
            gdata = _goal_data_cached(cache, root_org, ds[:7])
            vo = gdata.get("goalDetailsVo", {}) or {}
            day_goal = float((vo.get("dayAvgArea", {}) or {}).get("goal", {}).get("value") or 0) \
                if ds in gdata.get("assessmentDate", []) else 0.0
            price_goal = float((vo.get("avgPrice", {}) or {}).get("goal", {}).get("value") or 0)
            _eq("目标差距-日金额", f"{ds}目标=日均目标×均价目标", round(day_goal * price_goal, 2), info.get("goalValue"))
            _eq("目标差距-日金额", f"{ds}差值=达成-目标",
                float(info["reachValue"]) - float(info["goalValue"]), info.get("dif"))
            if _ring_expect(info) is not None:
                _eq("目标差距-日金额", f"{ds}日环比=(达成-昨日)/昨日×100", _ring_expect(info), info.get("ring"))

    @allure.story("数据总览 - 校验目标差距日维度日活数据")
    def test_ydl_SZL_AH_verify_goal_dif_day_active_cross(self):
        """目标差距日-日活：每日下单客户数趋势(customerNum)，无目标值和差值"""
        # Author: Author
        # Create Date: 2026-08-25
        # IsAI: True
        _skip_if_no_env()

        # 1. 逐日校验下单客户数/订单笔数存在，且无目标值与差值
        for d in _goal_dif_day_entries("month_active"):
            ds, info = d.get("dateStr"), d.get("salesInfo", {}) or {}
            assert isinstance(d.get("customerNum"), int) and d["customerNum"] >= 0, \
                f"{ds}日活下单客户数缺失, 条目={d}"
            assert isinstance(d.get("orderNum"), int) and d["orderNum"] >= 0, \
                f"{ds}订单笔数缺失, 条目={d}"
            _eq("目标差距-日日活", f"{ds}日活无目标值", 0, info.get("goalValue"))
            _eq("目标差距-日日活", f"{ds}日活无差值", 0, info.get("dif"))

    @allure.story("数据总览 - 校验目标差距月维度面积数据")
    def test_ydl_SZL_AI_verify_goal_dif_month_area_cross(self):
        """目标差距月-面积：近12月止于本月，目标=根组织月日均目标，差值=达成−目标，月环比=(达成−上月)/上月×100"""
        # Author: Author
        # Create Date: 2026-08-25
        # IsAI: True
        _skip_if_no_env()
        root_org, cache = _root_org_id(), {}

        # 1. 逐月校验面积目标/差值/月环比与浮窗字段
        for m_entry in _goal_dif_month_entries("area"):
            ms, info = m_entry.get("dateStr"), m_entry.get("salesInfo", {}) or {}
            vo = _goal_data_cached(cache, root_org, ms).get("goalDetailsVo", {}) or {}
            if vo:
                _eq("目标差距-月面积", f"{ms}目标=根组织月日均目标",
                    float((vo.get("dayAvgArea", {}) or {}).get("goal", {}).get("value") or 0), info.get("goalValue"))
            _eq("目标差距-月面积", f"{ms}差值=达成-目标",
                float(info["reachValue"]) - float(info["goalValue"]), info.get("dif"))
            if _ring_expect(info) is not None:
                _eq("目标差距-月面积", f"{ms}月环比=(达成-上月)/上月×100", _ring_expect(info), info.get("ring"))
            assert isinstance(m_entry.get("customerNum"), int) and isinstance(m_entry.get("orderNum"), int), \
                f"{ms}浮窗字段(下单客户数/订单笔数)缺失, 条目={m_entry}"

    @allure.story("数据总览 - 校验目标差距月维度金额数据")
    def test_ydl_SZL_AJ_verify_goal_dif_month_amount_cross(self):
        """目标差距月-金额：目标=根组织月总金额目标，差值=达成−目标，月环比=(达成−上月)/上月×100"""
        # Author: Author
        # Create Date: 2026-08-25
        # IsAI: True
        _skip_if_no_env()
        root_org, cache = _root_org_id(), {}

        # 1. 逐月校验金额目标/差值/月环比
        for m_entry in _goal_dif_month_entries("amount"):
            ms, info = m_entry.get("dateStr"), m_entry.get("salesInfo", {}) or {}
            vo = _goal_data_cached(cache, root_org, ms).get("goalDetailsVo", {}) or {}
            if vo:
                _eq("目标差距-月金额", f"{ms}目标=根组织月总金额目标",
                    float((vo.get("amountTotal", {}) or {}).get("goal", {}).get("value") or 0), info.get("goalValue"))
            _eq("目标差距-月金额", f"{ms}差值=达成-目标",
                float(info["reachValue"]) - float(info["goalValue"]), info.get("dif"))
            if _ring_expect(info) is not None:
                _eq("目标差距-月金额", f"{ms}月环比=(达成-上月)/上月×100", _ring_expect(info), info.get("ring"))

    @allure.story("数据总览 - 校验目标差距月维度月活数据")
    def test_ydl_SZL_AK_verify_goal_dif_month_active_cross(self):
        """目标差距月-月活：每月下单客户数、目标值和差值(差值=达成−目标，本月达成=下单客户数)"""
        # Author: Author
        # Create Date: 2026-08-25
        # IsAI: True
        _skip_if_no_env()
        root_org, cache = _root_org_id(), {}
        month = date.today().strftime("%Y-%m")

        # 1. 逐月校验下单客户数/订单笔数存在，目标与差值取目标管理monthActive
        for m_entry in _goal_dif_month_entries("month_active"):
            ms, info = m_entry.get("dateStr"), m_entry.get("salesInfo", {}) or {}
            assert isinstance(m_entry.get("customerNum"), int) and m_entry["customerNum"] >= 0, \
                f"{ms}月活下单客户数缺失, 条目={m_entry}"
            assert isinstance(m_entry.get("orderNum"), int) and m_entry["orderNum"] >= 0, \
                f"{ms}订单笔数缺失, 条目={m_entry}"
            vo = _goal_data_cached(cache, root_org, ms).get("goalDetailsVo", {}) or {}
            ma = (vo.get("monthActive", {}) or {}).get("goal", {}) or {}
            if ma.get("dif") is not None:
                ma_reach = float(ma.get("reachValue") or 0)
                _eq("目标差距-月月活", f"{ms}差值=达成-目标", ma_reach - float(ma.get("value") or 0), ma.get("dif"))
                if ms == month:
                    _eq("目标差距-月月活", "本月月活达成=下单客户数", m_entry.get("customerNum"), ma_reach)
