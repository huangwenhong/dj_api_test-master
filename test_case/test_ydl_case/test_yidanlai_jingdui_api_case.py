# -*- coding: utf-8 -*-
"""易单来 - APP 竞对模块用例（基于易单来swaggerApi.json）"""

import allure
import pytest
from test_case.page_api.ydl.jingdui_api import JingduiAPI

JD = JingduiAPI()


def _ok(res, msg="接口返回异常"):
    """校验接口 code=10001200 且 success=True"""
    assert res.get("code") == "10001200", f"{msg}, 接口返回={res}"
    assert res.get("success") is True, f"{msg} success不为True, 接口返回={res}"


# ==================== APP-竞对模块 ====================

@allure.feature("APP-竞对模块")
class TestJingdui:

    @allure.story("查询竞对档案")
    def test_ydl_JD_query_archive(self):
        """查询竞对档案：默认分页查询→结构校验"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        # 1. 默认分页查询竞对档案列表
        res = JD.get_archive_list(pageNo=1, pageSize=15)
        _ok(res, "查询竞对档案列表失败")

        # 2. 断言返回结构
        data = res.get("data", {})
        assert isinstance(data, dict), f"返回data不是字典类型, data={data}"
        assert "list" in data or "total" in data, f"缺少list或total字段, data={data}"

        # 3. 验证列表结构
        rows = data.get("list") or []
        assert isinstance(rows, list), f"list字段不是列表类型, rows={rows}"

    @allure.story("查询竞对原纸")
    def test_ydl_JD_query_paper(self):
        """查询竞对原纸：默认分页查询→关键字搜索→排序查询"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        # 1. 默认分页查询竞对原纸列表
        res = JD.get_paper_list(pageNo=1, pageSize=15)
        _ok(res, "查询竞对原纸列表失败")

        # 2. 断言返回结构
        data = res.get("data", {})
        assert isinstance(data, dict), f"返回data不是字典类型, data={data}"
        rows = data.get("list") or []
        assert isinstance(rows, list), f"list字段不是列表类型, rows={rows}"

        # 3. 关键字搜索
        res_keyword = JD.get_paper_list(pageNo=1, pageSize=15, keyword="纸")
        _ok(res_keyword, "竞对原纸-关键字搜索失败")

        # 4. 排序查询（按企业名称降序）
        res_sort = JD.get_paper_list(pageNo=1, pageSize=15, sort="company_name", sortType="desc")
        _ok(res_sort, "竞对原纸-排序查询失败")

    @allure.story("查询竞对产品")
    def test_ydl_JD_query_product(self):
        """查询竞对产品：默认分页查询→结构校验"""
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True

        # 1. 默认分页查询竞对产品列表
        res = JD.get_product_list(pageNo=1, pageSize=15)
        _ok(res, "查询竞对产品列表失败")

        # 2. 断言返回结构
        data = res.get("data", {})
        assert isinstance(data, dict), f"返回data不是字典类型, data={data}"
        assert "list" in data or "total" in data, f"缺少list或total字段, data={data}"

        # 3. 验证列表结构
        rows = data.get("list") or []
        assert isinstance(rows, list), f"list字段不是列表类型, rows={rows}"
