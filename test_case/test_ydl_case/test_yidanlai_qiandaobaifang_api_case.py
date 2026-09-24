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
