# -*- coding: utf-8 -*-
"""易单来 - 纸板团购产品接口（供应端 product 模块，走 cpsol.net 网关域名）

product 服务不在业财后端 IP(djfinancemanage) 上，只能通过 cpsol.net 网关访问，
因此本类默认 base_url 使用网关域名，模式与 lvyue_api.LvyueAPI 保持一致。
"""

import allure
import conftest
from test_case.page_api.public.base_api import BaseAPI

# 纸板团购产品接口网关路径前缀
PRODUCT_PREFIX = "/djsupplier/product"
# 产品模块使用 cpsol.net 网关域名
CPSOL_BASE_URL = "https://suppliertest.cpsol.net"


class ProductAPI(BaseAPI):
    """易单来纸板团购产品接口封装（使用 cpsol.net 网关域名）"""

    def __init__(self, base_url=None, headers=None, cookies=None):
        # 默认使用 cpsol.net 网关域名
        super().__init__(base_url or CPSOL_BASE_URL, headers, cookies)
        biz_headers = {
            "device": "web",
            "source": "easy_order",
            "version": "2.3.5",
            "Content-Type": "application/json",
        }
        if self.headers:
            self.headers.update(biz_headers)
        else:
            self.headers = biz_headers
        # 使用 cpsol.net 的 token（未填充时由 BaseAPI 回退到 config.default_cookies 的 token）
        cpsol_tok = conftest.cpsol_token.get("token", "")
        if cpsol_tok:
            self.cookies["token"] = cpsol_tok
            self._extra_cookies["token"] = cpsol_tok

    @allure.step("加载纸板团购上架层数楞型")
    def load_exist_layer_and_flute(self, supplierId=None, status_code=200, **kwargs):
        """加载供应商纸板团购上架产品已存在的层数与楞型（供应端）

        实测入参:
          可选: supplierId（不传时返回登录供应商自身）
        实测返参 data: 双层信封 data.data.list，为"层数->楞型"树
          [{label:"2层", value:2, children:[{label:"BE楞", value:2}, ...]}, ...]
          节点 value=层数，children=该层下的楞型列表
        """
        # Author: Author
        # Create Date: 2026-09-15
        # IsAI: True
        url = f"{PRODUCT_PREFIX}/loadExistLayerAndFlute.do"
        payload = {}
        if supplierId is not None:
            payload["supplierId"] = supplierId
        error_msg = kwargs.pop("error_msg", "加载纸板团购上架层数楞型失败")
        payload.update(kwargs)
        return self.post(url, json=payload, status_code=status_code, error_msg=error_msg)
