# -*- coding: utf-8 -*-
"""易单来 - 签到拜访接口测试用例"""

import allure
import pytest
from datetime import datetime
from test_case.page_api.ydl.qiandaobaifang_api import QiandaoBaifangAPI


# 固定参数
SUPPLIER_ID = "ee3b25465f0b11edb9b5000c29f98159"


@allure.feature("签到拜访")
class TestQiandaoBaifang:
    """签到拜访测试类"""

    def _get_api(self):
        """获取 API 实例"""
        return QiandaoBaifangAPI()

    def _today_str(self):
        """返回今日日期字符串（无前导零，如 2026-9-1）"""
        now = datetime.now()
        return f"{now.year}-{now.month}-{now.day}"

    # ==================== AA: 业务员拜访概览完整业务流 ====================

    @allure.story("签到拜访 - 业务员拜访概览")
    def test_ydl_AA_salesman_visit_overview(self):
        """业务员拜访概览：查询今日签到/拜访/超期未拜访统计，验证数据完整性"""
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

    # ==================== AB: 业务员工作台（/app/djcockpit/easyorder/salesman） ====================

    @allure.story("签到拜访 - 业务员工作台")
    def test_ydl_AB_salesman_workbench(self):
        """业务员工作台：判断合作业务员取supplierId→销售概览/订单产品数/购物车/待办/客户概览/今日产品"""
        # Author: Author
        # Create Date: 2026-10-22
        # IsAI: True
        api = self._get_api()
        today = datetime.now().strftime("%Y-%m-%d")

        # 1. 前置：判断合作业务员，动态获取 supplierId
        res_judge = api.salesman_judge_cooperation({})
        assert res_judge.get("success") is True, f"判断合作业务员失败, 返回={res_judge}"
        supplier_list = res_judge.get("data", {}).get("supplierList") or []
        assert supplier_list, f"supplierList不应为空, 返回={res_judge.get('data')}"
        supplier_id = supplier_list[0].get("supplierId")
        date_payload = {"supplierId": supplier_id, "beginDate": today, "endDate": today, "type": "1"}
        page_payload = {"supplierId": supplier_id, "pageNo": "1", "pageSize": "5"}

        # 2. 销售概览：包含目标/销售额/面积
        res_overview = api.salesman_get_sale_overview(date_payload)
        assert res_overview.get("code") == "10001200", f"销售概览失败, 返回={res_overview}"
        ov = res_overview.get("data", {})
        assert "saleAmount" in ov and "saleArea" in ov, f"销售概览应包含saleAmount/saleArea, data={ov}"

        # 3. 订单产品数量：data 为整型
        res_num = api.salesman_get_order_product_num(date_payload)
        assert res_num.get("code") == "10001200", f"订单产品数量失败, 返回={res_num}"
        assert isinstance(res_num.get("data"), int), f"订单产品数量data应为int, 实际={res_num.get('data')}"

        # 4. 购物车列表：list 结构
        res_cart = api.salesman_get_shopping_cart_list(page_payload)
        assert res_cart.get("code") == "10001200", f"购物车列表失败, 返回={res_cart}"
        assert isinstance(res_cart.get("data", {}).get("list"), list), f"购物车data.list应为list, 返回={res_cart.get('data')}"

        # 5. 待办列表：list 结构
        res_todo = api.salesman_get_to_be_completed_list(page_payload)
        assert res_todo.get("code") == "10001200", f"待办列表失败, 返回={res_todo}"
        assert isinstance(res_todo.get("data", {}).get("list"), list), f"待办data.list应为list, 返回={res_todo.get('data')}"

        # 6. 客户概览：包含 list
        res_cust = api.salesman_get_customer_overview({**date_payload, "pageNo": 1, "pageSize": 9999})
        assert res_cust.get("code") == "10001200", f"客户概览失败, 返回={res_cust}"
        assert "list" in res_cust.get("data", {}), f"客户概览应包含list, data={res_cust.get('data')}"

        # 7. 今日产品列表：list 结构
        res_prod = api.salesman_get_today_product_list({**date_payload, "dimension": "product", "pageNo": 1, "pageSize": 20})
        assert res_prod.get("code") == "10001200", f"今日产品列表失败, 返回={res_prod}"
        assert isinstance(res_prod.get("data", {}).get("list"), list), f"今日产品data.list应为list, 返回={res_prod.get('data')}"

        allure.attach(str(ov), "业务员销售概览", allure.attachment_type.TEXT)
