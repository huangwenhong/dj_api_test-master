# -*- coding: utf-8 -*-
"""易单来 - APP 竞对模块接口（基于易单来swaggerApi.json）"""

import allure
from test_case.page_api.public.base_api import BaseAPI

# 来自 swagger 2.0 的 basePath，DJEASYORDER 路径统一加 /djsupplier 前缀
RIVAL_PREFIX = "/djsupplier/DJEASYORDER/rival"
RIVAL_PAPER_PREFIX = f"{RIVAL_PREFIX}/paper"
RIVAL_ARCHIVE_PREFIX = f"{RIVAL_PREFIX}/archive"
RIVAL_PRODUCT_PREFIX = f"{RIVAL_PREFIX}/product"


class JingduiAPI(BaseAPI):
    """易单来 APP 竞对模块接口封装"""

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

    @allure.step("查询竞对档案列表")
    def get_archive_list(self, pageNo=1, pageSize=15,
                         keyword=None, sort=None, sortType=None,
                         status_code=200, **kwargs):
        """查询竞对档案列表（app_getList.do）

        swagger 入参:
          必填: pageNo, pageSize
          可选: keyword(搜索关键字),
                sort(排序字段),
                sortType(desc降序/asc升序)
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{RIVAL_ARCHIVE_PREFIX}/app_getList.do"
        payload = {"pageNo": pageNo, "pageSize": pageSize}
        if keyword is not None:
            payload["keyword"] = keyword
        if sort is not None:
            payload["sort"] = sort
        if sortType is not None:
            payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "查询竞对档案列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("查询竞对原纸列表")
    def get_paper_list(self, pageNo=1, pageSize=15,
                       keyword=None, sort=None, sortType=None,
                       status_code=200, **kwargs):
        """查询竞对原纸列表（app_getList.do）

        swagger 入参:
          必填: pageNo, pageSize
          可选: keyword(搜索关键字),
                sort(company_name企业名称/base_paper_code原纸代码/gram_weight克重),
                sortType(desc降序/asc升序)
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{RIVAL_PAPER_PREFIX}/app_getList.do"
        payload = {"pageNo": pageNo, "pageSize": pageSize}
        if keyword is not None:
            payload["keyword"] = keyword
        if sort is not None:
            payload["sort"] = sort
        if sortType is not None:
            payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "查询竞对原纸列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)

    @allure.step("查询竞对产品列表")
    def get_product_list(self, pageNo=1, pageSize=15,
                         keyword=None, sort=None, sortType=None,
                         status_code=200, **kwargs):
        """查询竞对产品列表（app_getList.do）

        swagger 入参:
          必填: pageNo, pageSize
          可选: keyword(搜索关键字),
                sort(排序字段),
                sortType(desc降序/asc升序)
        """
        # Author: Author
        # Create Date: 2026-09-01
        # IsAI: True
        url = f"{RIVAL_PRODUCT_PREFIX}/app_getList.do"
        payload = {"pageNo": pageNo, "pageSize": pageSize}
        if keyword is not None:
            payload["keyword"] = keyword
        if sort is not None:
            payload["sort"] = sort
        if sortType is not None:
            payload["sortType"] = sortType
        error_msg = kwargs.pop("error_msg", "查询竞对产品列表失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
