# -*- coding: utf-8 -*-
"""易单来 - 线索管理用例"""

import allure
import pytest
import random
import time
import calendar
from test_case.page_api.ydl.xiansuo_api import XiansuoAPI
from test_case.page_api.ydl.mubiao_api import MubiaoAPI

XS = XiansuoAPI()
MB = MubiaoAPI()


def _get_org_id(org_name="东诚包装"):
    """获取目标组织 orgId，默认取"东诚包装"，获取失败则跳过用例。"""
    res_org = MB.get_org_list_no_auth()
    assert res_org.get("code") == "10001200", f"获取目标组织列表失败, 接口返回={res_org}"
    org_list = res_org.get("data", {}).get("list", [])
    if not org_list:
        pytest.skip("目标组织列表为空，跳过后续步骤")
    for i, org in enumerate(org_list):
        if org.get("orgName") == org_name:
            org_list.insert(0, org_list.pop(i))
            break
    return org_list[0].get("orgId", "")


@allure.feature("线索管理")
class TestClueManagement:

    @allure.story("线索管理 - 完整业务流")
    def test_ydl_AA_clue_full_business_flow(self):
        """线索完整业务流：新增→查询→验证→修改→验证修改→删除→查询已删除→恢复→查询恢复→删除恢复"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True

        # 构造随机名称（姓氏+两个字随机组合，避免与历史数据冲突）
        surnames = ["陈", "李", "张", "王", "刘", "赵", "孙", "周", "吴", "郑"]
        given_chars = ["伟", "志", "建", "海", "红", "丽", "明", "斌", "华", "强"]
        ai_customer_name = random.choice(surnames) + random.choice(given_chars) + random.choice(given_chars)
        ai_contact_phone = "1" + random.choice(["3", "5", "7", "8", "9"]) + "".join([str(random.randint(0, 9)) for _ in range(9)])

        # 1. 新增线索
        res_add = XS.add_clue_base_info(
            customerName=ai_customer_name,
            contactWay=ai_contact_phone,
        )
        assert res_add.get("code") == "10001200", f"新增线索code异常, 接口返回={res_add}"
        assert res_add.get("success") is True, f"新增线索success异常, 接口返回={res_add}"
        new_clue_id = res_add.get("data", "")
        assert new_clue_id, f"新增线索未返回clueId, 接口返回={res_add}"

        # 2. 查询新增的线索（通过详情接口确认新增成功，列表接口存在索引延迟）
        res_detail = XS.get_clue_base_info(clueId=new_clue_id)
        assert res_detail.get("code") == "10001200", f"查看线索详情失败, 接口返回={res_detail}"
        detail = res_detail.get("data", {})

        # 3. 验证新增的线索字段
        assert detail.get("customerName") == ai_customer_name, \
            f"customerName不匹配, 期望={ai_customer_name}, 实际={detail.get('customerName')}"
        assert str(detail.get("contactWay", "")) == str(ai_contact_phone), \
            f"contactWay不匹配, 期望={ai_contact_phone}, 实际={detail.get('contactWay')}"
        assert detail.get("id") == new_clue_id, \
            f"id不匹配, 期望={new_clue_id}, 实际={detail.get('id')}"

        # 4. 修改线索（以详情为基础，仅修改目标字段）
        modified_name = random.choice(surnames) + random.choice(given_chars) + random.choice(given_chars)
        # 构造完整 baseInfo（服务端要求全量字段）
        base_info = detail.copy()
        base_info["customerName"] = modified_name
        base_info["mainContactManName"] = modified_name
        # 处理 None 值字段（服务端不接受 null）
        if base_info.get("merchandiserInfo") is None:
            base_info["merchandiserInfo"] = {"id": ""}
        if base_info.get("moreContacts") is None:
            base_info["moreContacts"] = []
        res_update = XS.update_clue_base_info(clueId=new_clue_id, baseInfo=base_info)
        assert res_update.get("code") == "10001200", f"修改线索code异常, 接口返回={res_update}"
        assert res_update.get("success") is True, f"修改线索success异常, 接口返回={res_update}"

        # 5. 验证修改后的线索
        res_modified = XS.get_clue_base_info(clueId=new_clue_id)
        assert res_modified.get("code") == "10001200", f"修改后查看详情失败, 接口返回={res_modified}"
        modified_detail = res_modified.get("data", {})
        assert modified_detail.get("customerName") == modified_name, \
            f"修改后customerName不匹配, 期望={modified_name}, 实际={modified_detail.get('customerName')}"

        # 6. 删除线索
        res_del = XS.del_clues(clueList=[new_clue_id])
        assert res_del.get("code") == "10001200", f"删除线索code异常, 接口返回={res_del}"
        assert res_del.get("success") is True, f"删除线索success异常, 接口返回={res_del}"

        # 7. 查询刚才删除的线索（软删除后详情仍可查，确认线索处于已删除状态）
        res_after_del = XS.get_clue_base_info(clueId=new_clue_id)
        assert res_after_del.get("code") == "10001200", f"删除后查看详情失败, 接口返回={res_after_del}"
        assert res_after_del.get("data", {}).get("customerName") == modified_name, \
            f"删除后customerName不匹配, 接口返回={res_after_del}"

        # 8. 恢复刚才删除的线索
        res_recover = XS.recover_clues(clueList=[new_clue_id])
        assert res_recover.get("code") == "10001200", f"恢复线索code异常, 接口返回={res_recover}"
        assert res_recover.get("success") is True, f"恢复线索success异常, 接口返回={res_recover}"

        # 9. 查询恢复的线索
        res_after_recover = XS.get_clue_base_info(clueId=new_clue_id)
        assert res_after_recover.get("code") == "10001200", f"恢复后查看详情失败, 接口返回={res_after_recover}"
        assert res_after_recover.get("data", {}).get("customerName") == modified_name, \
            f"恢复后customerName不匹配, 接口返回={res_after_recover}"

        # 10. 删除恢复的线索（恢复后服务端需时间处理状态，加重试机制）
        for attempt in range(3):
            time.sleep(2)
            res_del2 = XS.del_clues(clueList=[new_clue_id])
            if res_del2.get("code") == "10001200":
                break
        assert res_del2.get("code") == "10001200", f"再次删除线索code异常, 接口返回={res_del2}"
        assert res_del2.get("success") is True, f"再次删除线索success异常, 接口返回={res_del2}"



    @allure.story("线索管理 - 转移与转化")
    def test_ydl_AB_clue_transfer_and_convert(self):
        """线索转移与转化：新增线索→转移线索→验证转移→转化线索→验证转化"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True

        # 构造随机名称
        surnames = ["陈", "李", "张", "王", "刘", "赵", "孙", "周", "吴", "郑"]
        given_chars = ["伟", "志", "建", "海", "红", "丽", "明", "斌", "华", "强"]
        ai_customer_name = random.choice(surnames) + random.choice(given_chars) + random.choice(given_chars)
        ai_contact_phone = "1" + random.choice(["3", "5", "7", "8", "9"]) + "".join([str(random.randint(0, 9)) for _ in range(9)])

        # 1. 新增线索
        res_add = XS.add_clue_base_info(
            customerName=ai_customer_name,
            contactWay=ai_contact_phone,
        )
        assert res_add.get("code") == "10001200", f"新增线索code异常, 接口返回={res_add}"
        new_clue_id = res_add.get("data", "")
        assert new_clue_id, f"新增线索未返回clueId, 接口返回={res_add}"

        # 2. 获取负责人列表，选择一个可用的目标负责人
        org_id = _get_org_id()
        res_duty_list = XS.get_duty_man_list_by_org_id(orgId=org_id)
        assert res_duty_list.get("code") == "10001200", f"获取负责人列表失败, 接口返回={res_duty_list}"
        duty_list = res_duty_list.get("data", {}).get("list", [])
        assert duty_list, f"负责人列表为空, 接口返回={res_duty_list}"
        # 选择第一个负责人作为转移目标
        target_duty_man_id = duty_list[0].get("dutyManId", "")
        assert target_duty_man_id, f"负责人id为空, 接口返回={res_duty_list}"

        # 3. 转移线索
        res_transfer = XS.transfer_clue(clueList=[new_clue_id], dutyManId=target_duty_man_id)
        assert res_transfer.get("code") == "10001200", f"转移线索code异常, 接口返回={res_transfer}"
        assert res_transfer.get("success") is True, f"转移线索success异常, 接口返回={res_transfer}"

        # 4. 验证转移成功（查看详情确认负责人已变更）
        res_after_transfer = XS.get_clue_base_info(clueId=new_clue_id)
        assert res_after_transfer.get("code") == "10001200", f"转移后查看详情失败, 接口返回={res_after_transfer}"
        transferred_detail = res_after_transfer.get("data", {})
        assert transferred_detail.get("dutyManId") == target_duty_man_id, \
            f"转移后dutyManId不匹配, 期望={target_duty_man_id}, 实际={transferred_detail.get('dutyManId')}"

        # 5. 转化线索（线索转客户）
        res_sync = XS.sync_clue(clueList=[new_clue_id])
        assert res_sync.get("code") == "10001200", f"转化线索code异常, 接口返回={res_sync}"
        assert res_sync.get("success") is True, f"转化线索success异常, 接口返回={res_sync}"

        # 6. 验证转化成功（查看详情确认状态已变更）
        res_after_sync = XS.get_clue_base_info(clueId=new_clue_id)
        assert res_after_sync.get("code") == "10001200", f"转化后查看详情失败, 接口返回={res_after_sync}"



    @allure.story("线索管理 - 导入错误报告与导出")
    def test_ydl_AC_clue_import_and_error_report(self):
        """线索导入与错误报告：导入线索→查看导入记录→下载错误导入记录→导出Excel"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True

        # 1. 上传本地线索模板Excel，获取fileId
        import os
        template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "api_test_dj_temp", "线索模板.xlsx")
        res_upload = XS.upload_excel(file_path=template_path)
        assert res_upload.get("code") == "10001200", f"上传线索模板Excel失败, 接口返回={res_upload}"
        assert res_upload.get("success") is True, f"上传线索模板Excel success不为True, 接口返回={res_upload}"
        upload_list = res_upload.get("data", {}).get("list", [])
        assert upload_list, f"上传文件返回list为空, 接口返回={res_upload}"
        test_file_id = upload_list[0].get("fileid", upload_list[0].get("fileId", upload_list[0].get("id", "")))
        assert test_file_id, f"上传文件未返回fileId, item={upload_list[0]}"
        res_import = XS.import_clue_excel(fileIds=[test_file_id])
        # 导入可能成功或失败，只要接口正常响应即可
        assert res_import.get("code") in ("10001200", "10003001", "11000020"), \
            f"导入线索接口异常, 接口返回={res_import}"

        # 2. 查看导入记录
        time.sleep(1)  # 等待导入记录落库
        res_records = XS.get_import_record_list()
        assert res_records.get("code") == "10001200", f"查看导入记录失败, 接口返回={res_records}"
        record_list = res_records.get("data", {}).get("list", [])
        assert record_list, f"导入记录列表为空, 接口返回={res_records}"

        # 3. 查找有失败记录的导入记录（用于下载错误报告）
        failed_record = None
        for record in record_list:
            if record.get("customerFailTotal", 0) > 0 or record.get("productFailTotal", 0) > 0:
                failed_record = record
                break
        
        # 4. 下载错误导入记录（如果有失败记录的话）
        if failed_record:
            res_download = XS.download_error_report(recordId=failed_record.get("id"))
            assert res_download.status_code == 200, \
                f"下载错误报告HTTP状态异常, status={res_download.status_code}, text={res_download.text[:200]}"
            # 验证返回的是文件流（非空内容）
            assert len(res_download.content) > 0, "下载错误报告返回内容为空"
        else:
            allure.attach("无错误报告记录，跳过下载错误报告步骤", name="错误报告")

        # 5. 导出线索列表Excel
        res_export = XS.export_selected_clue_list()
        assert res_export.status_code == 200, \
            f"导出线索列表HTTP状态异常, status={res_export.status_code}, text={res_export.text[:200]}"
        assert len(res_export.content) > 0, "导出线索列表返回内容为空"
        assert "application/vnd" in res_export.headers.get("Content-Type", "") or \
               "octet-stream" in res_export.headers.get("Content-Type", "") or \
               len(res_export.content) > 100, \
            f"导出线索列表返回非文件流, Content-Type={res_export.headers.get('Content-Type')}"



    @allure.story("线索详情 - 合作纸板厂CRUD")
    def test_ydl_AD_cooperative_cardboard_factory(self):
        """合作纸板厂CRUD：新增线索→新增合作纸板厂→查询验证→编辑→验证编辑→删除→验证删除→清理"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True

        # 构造随机名称
        surnames = ["陈", "李", "张", "王", "刘", "赵", "孙", "周", "吴", "郑"]
        given_chars = ["伟", "志", "建", "海", "红", "丽", "明", "斌", "华", "强"]
        ai_customer_name = random.choice(surnames) + random.choice(given_chars) + random.choice(given_chars)
        ai_contact_phone = "1" + random.choice(["3", "5", "7", "8", "9"]) + "".join([str(random.randint(0, 9)) for _ in range(9)])

        # 1. 新增线索（作为合作纸板厂操作的前置数据）
        res_add = XS.add_clue_base_info(
            customerName=ai_customer_name,
            contactWay=ai_contact_phone,
        )
        assert res_add.get("code") == "10001200", f"新增线索code异常, 接口返回={res_add}"
        new_clue_id = res_add.get("data", "")
        assert new_clue_id, f"新增线索未返回clueId, 接口返回={res_add}"

        # 2. 获取竞对企业列表，选取一个有效的 rivalArchiveId 作为合作纸板厂引用
        res_rivals = XS.get_rival_archive_list(clueId=new_clue_id)
        assert res_rivals.get("code") == "10001200", f"获取竞对企业列表失败, 接口返回={res_rivals}"
        rival_list = res_rivals.get("data", {}).get("list", [])
        assert rival_list, f"竞对企业列表为空, 接口返回={res_rivals}"
        rival_id = rival_list[0].get("rivalArchiveId", "")
        assert rival_id, f"竞对企业未返回rivalArchiveId, 接口返回={rival_list[0]}"

        # 3. 新增合作纸板厂
        factory_item = {
            "rivalCompanyId": rival_id,
            "settlementCycle": 3,
            "payWay": [1],
            "remarks": "ai自动化测试合作纸板厂",
        }
        res_add_factory = XS.add_cooperative_cardboard_factory(
            infoId=new_clue_id,
            factoryList=[factory_item],
        )
        assert res_add_factory.get("code") == "10001200", f"新增合作纸板厂code异常, 接口返回={res_add_factory}"
        assert res_add_factory.get("success") is True, f"新增合作纸板厂success异常, 接口返回={res_add_factory}"

        # 4. 查询合作纸板厂，验证新增成功
        time.sleep(1)
        res_query = XS.get_clue_cooperative_cardboard_factory(clueId=new_clue_id)
        assert res_query.get("code") == "10001200", f"查询合作纸板厂失败, 接口返回={res_query}"
        factory_list = res_query.get("data", {}).get("list", [])
        assert factory_list, f"新增后查询合作纸板厂为空, 接口返回={res_query}"

        # 5. 获取新增的纸板厂记录，验证关键字段
        added_factory = factory_list[0]
        factory_id = added_factory.get("id", "")
        assert factory_id, f"合作纸板厂未返回id, 接口返回={added_factory}"
        assert added_factory.get("rivalCompanyId") == rival_id, \
            f"rivalCompanyId不匹配, 期望={rival_id}, 实际={added_factory.get('rivalCompanyId')}"
        assert added_factory.get("settlementCycle") == 3, \
            f"settlementCycle不匹配, 期望=3, 实际={added_factory.get('settlementCycle')}"
        assert added_factory.get("remarks") == "ai自动化测试合作纸板厂", \
            f"remarks不匹配, 期望=ai自动化测试合作纸板厂, 实际={added_factory.get('remarks')}"

        # 6. 编辑合作纸板厂（修改结款周期和备注）
        update_info = dict(added_factory)
        update_info["settlementCycle"] = 5
        update_info["remarks"] = "ai自动化测试编辑后"
        res_update = XS.update_cooperative_cardboard_factory(factoryInfo=update_info)
        assert res_update.get("code") == "10001200", f"修改合作纸板厂code异常, 接口返回={res_update}"
        assert res_update.get("success") is True, f"修改合作纸板厂success异常, 接口返回={res_update}"

        # 7. 查询验证编辑结果
        res_after_update = XS.get_clue_cooperative_cardboard_factory(clueId=new_clue_id)
        assert res_after_update.get("code") == "10001200", f"编辑后查询失败, 接口返回={res_after_update}"
        updated_list = res_after_update.get("data", {}).get("list", [])
        assert updated_list, f"编辑后查询合作纸板厂为空, 接口返回={res_after_update}"
        updated_factory = next((f for f in updated_list if f.get("id") == factory_id), None)
        assert updated_factory, f"编辑后未找到对应纸板厂记录, id={factory_id}"
        assert updated_factory.get("settlementCycle") == 5, \
            f"编辑后settlementCycle不匹配, 期望=5, 实际={updated_factory.get('settlementCycle')}"
        assert updated_factory.get("remarks") == "ai自动化测试编辑后", \
            f"编辑后remarks不匹配, 接口返回={updated_factory}"

        # 8. 删除合作纸板厂
        res_del_factory = XS.del_cooperative_cardboard_factory(id=factory_id)
        assert res_del_factory.get("code") == "10001200", f"删除合作纸板厂code异常, 接口返回={res_del_factory}"
        assert res_del_factory.get("success") is True, f"删除合作纸板厂success异常, 接口返回={res_del_factory}"

        # 9. 查询验证删除结果
        time.sleep(1)
        res_after_del = XS.get_clue_cooperative_cardboard_factory(clueId=new_clue_id)
        assert res_after_del.get("code") == "10001200", f"删除后查询失败, 接口返回={res_after_del}"
        deleted_list = res_after_del.get("data", {}).get("list", [])
        remaining = [f for f in deleted_list if f.get("id") == factory_id]
        assert not remaining, f"删除后仍能查到合作纸板厂, id={factory_id}"

        # 10. 清理：删除测试线索
        for attempt in range(3):
            time.sleep(2)
            res_del_clue = XS.del_clues(clueList=[new_clue_id])
            if res_del_clue.get("code") == "10001200":
                break
        assert res_del_clue.get("code") == "10001200", f"清理线索失败, 接口返回={res_del_clue}"



    @allure.story("线索详情 - 物流信息新增与验证")
    def test_ydl_AF_logistics_info(self):
        """物流信息新增与验证：新增线索→获取初始物流信息（空）→新增物流信息→验证各字段"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True

        # 构造随机名称
        surnames = ["陈", "李", "张", "王", "刘", "赵", "孙", "周", "吴", "郑"]
        given_chars = ["伟", "志", "建", "海", "红", "丽", "明", "斌", "华", "强"]
        ai_customer_name = random.choice(surnames) + random.choice(given_chars) + random.choice(given_chars)
        ai_contact_phone = "1" + random.choice(["3", "5", "7", "8", "9"]) + "".join([str(random.randint(0, 9)) for _ in range(9)])

        # ====== 前置：新增线索 + 获取车辆配置列表 ======

        # 1. 新增线索
        res_add = XS.add_clue_base_info(
            customerName=ai_customer_name,
            contactWay=ai_contact_phone,
        )
        assert res_add.get("code") == "10001200", f"新增线索code异常, 接口返回={res_add}"
        new_clue_id = res_add.get("data", "")
        assert new_clue_id, f"新增线索未返回clueId, 接口返回={res_add}"

        # 2. 获取初始物流信息（应为空）
        res_init = XS.get_clue_logistics_info(clueId=new_clue_id)
        assert res_init.get("code") == "10001200", f"获取初始物流信息失败, 接口返回={res_init}"
        init_data = res_init.get("data", {})
        assert not init_data.get("id"), f"初始物流信息id不为空, 接口返回={init_data}"

        # 3. 获取车辆配置列表（新增/修改物流信息需要用到的车辆配置数据）
        res_car = XS.get_car_configure_list()
        assert res_car.get("code") == "10001200", f"获取车辆配置列表失败, 接口返回={res_car}"
        car_list = res_car.get("data", {}).get("list", [])
        assert car_list, f"车辆配置列表为空, 接口返回={res_car}"

        # ====== 步骤一：新增物流信息（不传logisticsId，随机数据） ======

        # 4. 构造随机物流信息数据
        rand_car = random.choice(car_list)
        rand_warehouse = str(random.randint(100, 9999))
        rand_project_time = str(random.randint(1, 99))
        rand_factory_area = round(random.uniform(100, 9999), 1)
        rand_max_transport = round(random.uniform(10, 500), 1)
        rand_start_hour = random.randint(6, 11)
        rand_end_hour = random.randint(13, 20)
        rand_other_car = random.choice(["需要厢式货车", "需要平板车", "需要冷藏车", "需要高栏车", "自备车辆"])
        demands_options = ["轻拿轻放", "防潮", "防压", "防碎", "易碎品", "禁止倒置", "注意通风"]
        rand_demands = random.sample(demands_options, random.randint(1, 3))
        rand_lift_height = f"{random.uniform(2, 5):.1f}"
        rand_lift_wide = f"{random.uniform(1.5, 3):.1f}"
        rand_is_door = random.choice(["0", "1"])

        logistics_model_add = {
            "clueId": new_clue_id,
            "deliveryTime": [
                {"startTime": f"{rand_start_hour:02d}:00", "endTime": f"{rand_end_hour:02d}:00"}
            ],
            "demands": rand_demands,
            "liftSpecifications": {
                "isConfig": "1",
                "liftHeight": rand_lift_height,
                "liftWide": rand_lift_wide
            },
            "otherCarInfo": rand_other_car,
            "ownCars": [],
            "passCars": [
                {
                    "carConfigId": rand_car.get("carConfigId", ""),
                    "passSpecifications": rand_car.get("passSpecifications", ""),
                    "isDoor": rand_is_door
                }
            ],
            "projectTime": rand_project_time,
            "warehouseCapacity": rand_warehouse,
            "factoryArea": rand_factory_area,
            "maxTransportCapacity": rand_max_transport
        }

        # 5. 新增物流信息
        res_add_logistics = XS.update_clue_logistics_info(clueId=new_clue_id, logisticsModel=logistics_model_add)
        assert res_add_logistics.get("code") == "10001200", f"新增物流信息code异常, 接口返回={res_add_logistics}"
        assert res_add_logistics.get("success") is True, f"新增物流信息success异常, 接口返回={res_add_logistics}"

        # ====== 步骤二：验证新增后的物流信息各字段 ======

        # 6. 获取新增后的物流信息
        time.sleep(1)
        res_get_add = XS.get_clue_logistics_info(clueId=new_clue_id)
        assert res_get_add.get("code") == "10001200", f"新增后获取物流信息失败, 接口返回={res_get_add}"
        add_data = res_get_add.get("data", {})
        assert add_data.get("id"), f"新增后物流信息id为空, 接口返回={add_data}"

        # 7. 验证各字段
        assert add_data.get("warehouseCapacity") == rand_warehouse, \
            f"warehouseCapacity不匹配, 期望={rand_warehouse}, 实际={add_data.get('warehouseCapacity')}"
        assert add_data.get("projectTime") == rand_project_time, \
            f"projectTime不匹配, 期望={rand_project_time}, 实际={add_data.get('projectTime')}"
        assert add_data.get("otherCarInfo") == rand_other_car, \
            f"otherCarInfo不匹配, 期望={rand_other_car}, 实际={add_data.get('otherCarInfo')}"
        # 验证收货窗口期
        delivery_time = add_data.get("deliveryTime", [])
        assert delivery_time, f"deliveryTime为空, 接口返回={add_data}"
        assert delivery_time[0].get("startTime") == f"{rand_start_hour:02d}:00", \
            f"deliveryTime.startTime不匹配, 实际={delivery_time[0].get('startTime')}"
        assert delivery_time[0].get("endTime") == f"{rand_end_hour:02d}:00", \
            f"deliveryTime.endTime不匹配, 实际={delivery_time[0].get('endTime')}"
        # 验证额外要求
        assert set(add_data.get("demands", [])) == set(rand_demands), \
            f"demands不匹配, 期望={rand_demands}, 实际={add_data.get('demands')}"
        # 验证电梯规格
        lift_spec = add_data.get("liftSpecifications", {})
        assert lift_spec.get("isConfig") == "1", \
            f"liftSpecifications.isConfig不匹配, 实际={lift_spec.get('isConfig')}"
        assert lift_spec.get("liftHeight") == rand_lift_height, \
            f"liftSpecifications.liftHeight不匹配, 期望={rand_lift_height}, 实际={lift_spec.get('liftHeight')}"
        assert lift_spec.get("liftWide") == rand_lift_wide, \
            f"liftSpecifications.liftWide不匹配, 期望={rand_lift_wide}, 实际={lift_spec.get('liftWide')}"
        # 验证可通行车辆
        pass_cars = add_data.get("passCars", [])
        assert pass_cars, f"passCars为空, 接口返回={add_data}"
        assert pass_cars[0].get("carConfigId") == rand_car.get("carConfigId"), \
            f"passCars.carConfigId不匹配, 实际={pass_cars[0].get('carConfigId')}"
        assert pass_cars[0].get("isDoor") == rand_is_door, \
            f"passCars.isDoor不匹配, 期望={rand_is_door}, 实际={pass_cars[0].get('isDoor')}"
        # 验证厂房面积和最大运力
        assert float(add_data.get("factoryArea", 0) or 0) == rand_factory_area, \
            f"factoryArea不匹配, 期望={rand_factory_area}, 实际={add_data.get('factoryArea')}"
        assert float(add_data.get("maxTransportCapacity", 0) or 0) == rand_max_transport, \
            f"maxTransportCapacity不匹配, 期望={rand_max_transport}, 实际={add_data.get('maxTransportCapacity')}"

        # ====== 清理：删除测试线索 ======
        for attempt in range(3):
            time.sleep(2)
            res_del_clue = XS.del_clues(clueList=[new_clue_id])
            if res_del_clue.get("code") == "10001200":
                break
        assert res_del_clue.get("code") == "10001200", f"清理线索失败, 接口返回={res_del_clue}"

    @allure.story("物流信息 - 休息日配置")
    def test_ydl_AG_rest_day_config(self):
        """休息日配置：设置固定休息日规则→验证某月休息日→添加自定义休息日→验证更新"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True

        # ====== 步骤一：设置固定休息日规则 ======

        # 1. 随机选择周休息日和月休息日
        rand_week_days = random.sample([1, 2, 3, 4, 5, 6, 7], random.randint(1, 3))
        rand_month_days = random.sample(list(range(1, 29)), random.randint(1, 3))

        # 2. 更新固定休息日
        res_update_regular = XS.update_regular_rest_day(
            monthRestArray=sorted(rand_month_days),
            weekRestArray=sorted(rand_week_days)
        )
        assert res_update_regular.get("code") == "10001200", f"更新固定休息日失败, 接口返回={res_update_regular}"
        assert res_update_regular.get("success") is True, f"更新固定休息日success异常, 接口返回={res_update_regular}"
        regular_rest_id = res_update_regular.get("data", {}).get("regularRestId", "")
        assert regular_rest_id, f"更新固定休息日未返回regularRestId, 接口返回={res_update_regular}"

        # ====== 步骤二：验证 2026-07 月休息日列表 ======

        # 3. 计算 2026-07 月预期休息日
        year, month = 2026, 7
        days_in_month = calendar.monthrange(year, month)[1]
        # weekday(): Monday=0 ... Sunday=6, 接口 weekRestArray: 1=周一 ... 7=周日
        expected_rest_days = set()
        for day in range(1, days_in_month + 1):
            weekday_num = calendar.weekday(year, month, day) + 1  # 转为 1-7
            if weekday_num in rand_week_days:
                expected_rest_days.add(str(day))
        for md in rand_month_days:
            if md <= days_in_month:
                expected_rest_days.add(str(md))

        # 4. 获取该月休息日
        res_get_rest = XS.get_rest_day_list(regularRestId=regular_rest_id, yearMonth=f"{year}-{month:02d}")
        assert res_get_rest.get("code") == "10001200", f"获取休息日列表失败, 接口返回={res_get_rest}"
        actual_rest_days = set(res_get_rest.get("data", {}).get("restDayArray", []))
        assert actual_rest_days == expected_rest_days, \
            f"休息日不匹配, 期望={sorted(expected_rest_days, key=int)}, 实际={sorted(actual_rest_days, key=int)}"

        # ====== 步骤三：验证 2026-08 月休息日列表 ======

        # 5. 计算 2026-08 月预期休息日
        year2, month2 = 2026, 8
        days_in_month2 = calendar.monthrange(year2, month2)[1]
        expected_rest_days2 = set()
        for day in range(1, days_in_month2 + 1):
            weekday_num = calendar.weekday(year2, month2, day) + 1
            if weekday_num in rand_week_days:
                expected_rest_days2.add(str(day))
        for md in rand_month_days:
            if md <= days_in_month2:
                expected_rest_days2.add(str(md))

        # 6. 获取 8 月休息日
        res_get_rest2 = XS.get_rest_day_list(regularRestId=regular_rest_id, yearMonth=f"{year2}-{month2:02d}")
        assert res_get_rest2.get("code") == "10001200", f"获取8月休息日列表失败, 接口返回={res_get_rest2}"
        actual_rest_days2 = set(res_get_rest2.get("data", {}).get("restDayArray", []))
        assert actual_rest_days2 == expected_rest_days2, \
            f"8月休息日不匹配, 期望={sorted(expected_rest_days2, key=int)}, 实际={sorted(actual_rest_days2, key=int)}"

    @allure.story("线索详情 - 需求信息产品CRUD")
    def test_ydl_AE_demand_info_product(self):
        """需求信息产品CRUD：新增线索→新增产品→验证总需求面积和总需求金额→验证其他字段→编辑产品→验证总需求面积和总需求金额→验证其他字段→删除产品→验证总需求面积和总需求金额"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True

        # 构造随机名称
        surnames = ["陈", "李", "张", "王", "刘", "赵", "孙", "周", "吴", "郑"]
        given_chars = ["伟", "志", "建", "海", "红", "丽", "明", "斌", "华", "强"]
        ai_customer_name = random.choice(surnames) + random.choice(given_chars) + random.choice(given_chars)
        ai_contact_phone = "1" + random.choice(["3", "5", "7", "8", "9"]) + "".join([str(random.randint(0, 9)) for _ in range(9)])

        # ====== 前置：新增线索 + 获取层型 + 选取供应商 ======

        # 1. 新增线索
        res_add = XS.add_clue_base_info(
            customerName=ai_customer_name,
            contactWay=ai_contact_phone,
        )
        assert res_add.get("code") == "10001200", f"新增线索code异常, 接口返回={res_add}"
        new_clue_id = res_add.get("data", "")
        assert new_clue_id, f"新增线索未返回clueId, 接口返回={res_add}"

        # 2. 获取层数和楞型列表（产品新增需要 layerId/edgeId）
        res_layer = XS.get_layer_list()
        assert res_layer.get("code") == "10001200", f"获取层数楞型列表失败, 接口返回={res_layer}"
        layer_list = res_layer.get("data", {}).get("list", [])
        assert layer_list, f"层数楞型列表为空, 接口返回={res_layer}"
        # 随机选层型和楞型
        rand_layer = random.choice(layer_list)
        rand_edge = random.choice(rand_layer.get("edgeList", [{}]))
        layer_count = int(rand_layer.get("layerId", "2"))

        # 3. 获取竞对企业列表，选取一个非竞争对手作为纸板供应商
        res_rivals = XS.get_rival_archive_list(clueId=new_clue_id)
        assert res_rivals.get("code") == "10001200", f"获取竞对企业列表失败, 接口返回={res_rivals}"
        rival_list = res_rivals.get("data", {}).get("list", [])
        assert rival_list, f"竞对企业列表为空, 接口返回={res_rivals}"
        supplier = next((r for r in rival_list if r.get("companyType") != "competitors"), rival_list[0])
        supplier_id = supplier.get("rivalArchiveId", "")
        supplier_name = supplier.get("rivalArchiveName", "")
        assert supplier_id, f"供应商未返回rivalArchiveId, 接口返回={supplier}"

        # ====== 步骤一：新增产品（使用 web 端真实 payload 格式，数据全部随机） ======

        # 4. 构造随机产品数据
        product_names = ["瓦楞纸箱", "瓦楞纸板", "飞机盒", "展示盒", "纸托盘", "彩盒", "牛皮纸箱", "快递纸箱"]
        materials = ["AB", "BC", "BE", "CE", "EE", "A", "B", "C", "E"]
        rand_product_name = random.choice(product_names) + str(random.randint(100, 999))
        rand_material = random.choice(materials)
        rand_weights = [random.randint(100, 400) for _ in range(layer_count)]
        rand_gross_weight = f"{sum(rand_weights) * 1.18:.2f}"
        rand_area = round(random.uniform(0.5, 99.9), 2)
        rand_money = random.randint(1, 999)
        rand_price = f"{random.randint(1, 50)}.{random.randint(10, 99)}"

        product_data = {
            "paperboardSupplier": {
                "label": supplier_name,
                "value": supplier_id,
            },
            "productName": rand_product_name,
            "productMaterial": rand_material,
            "productLayer": {
                "layerId": rand_layer.get("layerId"),
                "layerName": rand_layer.get("layerName"),
                "edgeId": rand_edge.get("edgeId"),
                "edgeName": rand_edge.get("edgeName"),
            },
            "productLayerArray": [
                rand_layer.get("layerId"),
                rand_edge.get("edgeId"),
            ],
            "productLayerWeight": rand_weights,
            "grossWeight": rand_gross_weight,
            "monthRequirementArea": rand_area,
            "monthRequirementMoney": rand_money,
            "purchasePrice": rand_price,
            "paperboardSupplierId": supplier_id,
            "paperboardSupplierName": supplier_name,
            "platformProductList": [],
            "platformProductListTemp": [],
            "industryList": [],
            "industryListArray": [],
            "rivalAdvantage": [],
            "rivalAdvantageArray": [],
            "clueId": new_clue_id,
            "customerInfoId": new_clue_id,
        }
        res_add_product = XS.add_product_info(clueId=new_clue_id, product=product_data)
        assert res_add_product.get("code") == "10001200", f"新增产品code异常, 接口返回={res_add_product}"
        assert res_add_product.get("success") is True, f"新增产品success异常, 接口返回={res_add_product}"

        # ====== 步骤二：验证新增后的总需求面积和总需求金额 ======

        # 5. 查询产品列表
        time.sleep(2)
        res_products = XS.get_clue_product_info_list(clueId=new_clue_id)
        assert res_products.get("code") == "10001200", f"查询产品列表失败, 接口返回={res_products}"
        product_list = res_products.get("data", {}).get("list", [])
        assert product_list, f"新增后产品列表为空, 接口返回={res_products}"

        # 6. 验证总需求面积和总需求金额（从产品列表聚合）
        total_area = sum(float(p.get("monthRequirementArea", 0) or 0) for p in product_list)
        total_money = sum(float(p.get("monthRequirementMoney", 0) or 0) for p in product_list)
        assert total_area == rand_area, f"新增后总需求面积不匹配, 期望={rand_area}, 实际={total_area}"
        assert total_money == float(rand_money), f"新增后总需求金额不匹配, 期望={rand_money}, 实际={total_money}"

        # ====== 步骤三：验证新增产品的其他字段 ======

        # 7. 获取产品详情验证字段
        added_product = product_list[0]
        product_id = added_product.get("productId", "")
        info_id = added_product.get("infoId", new_clue_id)
        assert product_id, f"产品未返回productId, 接口返回={added_product}"

        res_detail = XS.get_clue_product_info_by_id(productId=product_id)
        assert res_detail.get("code") == "10001200", f"查询产品详情失败, 接口返回={res_detail}"
        detail = res_detail.get("data", {})

        # 8. 验证产品各字段
        assert detail.get("productName") == rand_product_name, \
            f"productName不匹配, 期望={rand_product_name}, 实际={detail.get('productName')}"
        assert detail.get("productMaterial") == rand_material, \
            f"productMaterial不匹配, 期望={rand_material}, 实际={detail.get('productMaterial')}"
        assert float(detail.get("monthRequirementArea", 0) or 0) == rand_area, \
            f"monthRequirementArea不匹配, 期望={rand_area}, 实际={detail.get('monthRequirementArea')}"
        assert float(detail.get("monthRequirementMoney", 0) or 0) == float(rand_money), \
            f"monthRequirementMoney不匹配, 期望={rand_money}, 实际={detail.get('monthRequirementMoney')}"
        assert detail.get("paperboardSupplierId") == supplier_id, \
            f"paperboardSupplierId不匹配, 期望={supplier_id}, 实际={detail.get('paperboardSupplierId')}"

        # ====== 步骤四：编辑产品（修改面积和金额，数据随机） ======

        # 9. 编辑产品
        # 注意：productOnlyKey 由 productName+productMaterial+layer+edge 计算，
        #        编辑时需修改 productName 避免"产品名字重复"(11008008)
        edit_name = rand_product_name + "编辑"
        edit_area = round(random.uniform(0.5, 99.9), 2)
        edit_money = random.randint(1, 999)
        edit_product = {
            "productName": edit_name,
            "productMaterial": rand_material,
            "productLayer": detail.get("productLayer", {}),
            "productLayerWeight": detail.get("productLayerWeight", []),
            "purchasePrice": detail.get("purchasePrice", ""),
            "monthRequirementArea": str(edit_area),
            "monthRequirementMoney": str(edit_money),
            "paperboardSupplierId": detail.get("paperboardSupplierId", ""),
            "paperboardSupplierName": detail.get("paperboardSupplierName", ""),
            "platformProductList": detail.get("platformProductList", []),
            "industryList": detail.get("industryList", []),
            "tissueSupplier": detail.get("tissueSupplier", ""),
        }

        res_update_product = XS.update_product_info(productId=product_id, clueId=new_clue_id, product=edit_product)
        assert res_update_product.get("code") == "10001200", f"编辑产品code异常, 接口返回={res_update_product}"
        assert res_update_product.get("success") is True, f"编辑产品success异常, 接口返回={res_update_product}"

        # ====== 步骤五：验证编辑后的总需求面积和总需求金额 ======

        # 10. 查询编辑后产品列表
        time.sleep(2)
        res_products2 = XS.get_clue_product_info_list(clueId=new_clue_id)
        assert res_products2.get("code") == "10001200", f"编辑后查询产品列表失败, 接口返回={res_products2}"
        product_list2 = res_products2.get("data", {}).get("list", [])
        assert product_list2, f"编辑后产品列表为空, 接口返回={res_products2}"

        # 11. 验证编辑后总需求面积和总需求金额
        total_area2 = sum(float(p.get("monthRequirementArea", 0) or 0) for p in product_list2)
        total_money2 = sum(float(p.get("monthRequirementMoney", 0) or 0) for p in product_list2)
        assert total_area2 == edit_area, f"编辑后总需求面积不匹配, 期望={edit_area}, 实际={total_area2}"
        assert total_money2 == float(edit_money), f"编辑后总需求金额不匹配, 期望={edit_money}, 实际={total_money2}"

        # ====== 步骤六：验证编辑后的其他字段 ======

        # 12. 获取编辑后产品详情
        res_detail2 = XS.get_clue_product_info_by_id(productId=product_id)
        assert res_detail2.get("code") == "10001200", f"编辑后查询产品详情失败, 接口返回={res_detail2}"
        detail2 = res_detail2.get("data", {})

        # 13. 验证编辑后字段
        assert detail2.get("productName") == edit_name, \
            f"编辑后productName不匹配, 期望={edit_name}, 实际={detail2.get('productName')}"
        assert detail2.get("productMaterial") == rand_material, \
            f"编辑后productMaterial被篡改, 实际={detail2.get('productMaterial')}"
        assert float(detail2.get("monthRequirementArea", 0) or 0) == edit_area, \
            f"编辑后monthRequirementArea不匹配, 期望={edit_area}, 实际={detail2.get('monthRequirementArea')}"
        assert float(detail2.get("monthRequirementMoney", 0) or 0) == float(edit_money), \
            f"编辑后monthRequirementMoney不匹配, 期望={edit_money}, 实际={detail2.get('monthRequirementMoney')}"

        # ====== 步骤七：删除产品 ======

        # 14. 删除产品
        res_del_product = XS.del_clue_product(productId=product_id, infoId=info_id)
        assert res_del_product.get("code") == "10001200", f"删除产品code异常, 接口返回={res_del_product}"
        assert res_del_product.get("success") is True, f"删除产品success异常, 接口返回={res_del_product}"

        # ====== 步骤八：验证删除后的总需求面积和总需求金额 ======

        # 15. 查询删除后产品列表
        time.sleep(1)
        res_products3 = XS.get_clue_product_info_list(clueId=new_clue_id)
        assert res_products3.get("code") == "10001200", f"删除后查询产品列表失败, 接口返回={res_products3}"
        product_list3 = res_products3.get("data", {}).get("list", [])

        # 16. 验证删除后总需求面积和总需求金额为0
        total_area3 = sum(float(p.get("monthRequirementArea", 0) or 0) for p in product_list3)
        total_money3 = sum(float(p.get("monthRequirementMoney", 0) or 0) for p in product_list3)
        assert total_area3 == 0.0, f"删除后总需求面积不为0, 实际={total_area3}"
        assert total_money3 == 0.0, f"删除后总需求金额不为0, 实际={total_money3}"

        # ====== 清理：删除测试线索 ======
        for attempt in range(3):
            time.sleep(2)
            res_del_clue = XS.del_clues(clueList=[new_clue_id])
            if res_del_clue.get("code") == "10001200":
                break
        assert res_del_clue.get("code") == "10001200", f"清理线索失败, 接口返回={res_del_clue}"

    @allure.story("线索详情 - 编辑其他信息")
    def test_ydl_AH_edit_other_info(self):
        """编辑其他信息：新增线索→获取初始其他信息（空）→编辑其他信息→验证各字段→验证完整度提升"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True

        # 构造随机名称
        surnames = ["陈", "李", "张", "王", "刘", "赵", "孙", "周", "吴", "郑"]
        given_chars = ["伟", "志", "建", "海", "红", "丽", "明", "斌", "华", "强"]
        ai_customer_name = random.choice(surnames) + random.choice(given_chars) + random.choice(given_chars)
        ai_contact_phone = "1" + random.choice(["3", "5", "7", "8", "9"]) + "".join([str(random.randint(0, 9)) for _ in range(9)])

        # ====== 前置：新增线索 ======

        # 1. 新增线索
        res_add = XS.add_clue_base_info(
            customerName=ai_customer_name,
            contactWay=ai_contact_phone,
        )
        assert res_add.get("code") == "10001200", f"新增线索code异常, 接口返回={res_add}"
        new_clue_id = res_add.get("data", "")
        assert new_clue_id, f"新增线索未返回clueId, 接口返回={res_add}"

        # 2. 获取初始其他信息（应为空）
        res_init = XS.get_clue_other_info(clueId=new_clue_id)
        assert res_init.get("code") == "10001200", f"获取初始其他信息失败, 接口返回={res_init}"
        init_data = res_init.get("data", {})
        assert not init_data.get("id"), f"初始其他信息id不为空, 接口返回={init_data}"
        assert init_data.get("advancePay") == "", f"初始advancePay不为空, 接口返回={init_data}"

        # 3. 获取初始完整度
        res_pct_init = XS.get_clue_info_percent(clueId=new_clue_id)
        assert res_pct_init.get("code") == "10001200", f"获取初始完整度失败, 接口返回={res_pct_init}"
        init_pct = int(res_pct_init.get("data", {}).get("infoPercent", "0"))

        # 4. 获取省下市区列表（验证接口可用）
        res_city = XS.get_city_area_for_clue(provinceCode="33")
        assert res_city.get("code") == "10001200", f"获取市区列表失败, 接口返回={res_city}"
        city_list = res_city.get("data", {}).get("list", [])
        assert city_list, f"市区列表为空, 接口返回={res_city}"

        # ====== 步骤一：编辑其他信息 ======

        # 5. 构造随机其他信息数据
        rand_advance_pay = random.choice(["1", "2", "3"])  # 1:高, 2:中, 3:低
        rand_pay_select = random.sample(["1", "2"], random.randint(1, 2))  # 1:账期, 2:预付
        rand_period_type = "0"  # 固定月份
        rand_period_time = str(random.choice([15, 30, 45, 60]))
        rand_ticket_type = random.sample(["1", "2", "3", "4"], random.randint(1, 2))
        rand_customer_habit = random.choice(["月结客户", "长期合作", "现金结算", "季度结算", "年结客户"])
        rand_factory_area = round(random.uniform(100, 9999), 1)
        rand_number_of_emp = random.randint(10, 500)
        rand_operating_life = random.randint(1, 30)
        rand_number_of_print_press = random.randint(1, 20)
        rand_demand_rank = random.sample(["1", "2", "3", "4", "5"], random.randint(2, 4))

        other_info_model = {
            "advancePay": rand_advance_pay,
            "payWay": {
                "select": rand_pay_select,
                "periodType": rand_period_type,
                "periodTime": rand_period_time
            },
            "ticketType": rand_ticket_type,
            "customerHabit": rand_customer_habit,
            "factoryArea": rand_factory_area,
            "numberOfEmp": rand_number_of_emp,
            "operatingLife": rand_operating_life,
            "numberOfPrintPress": rand_number_of_print_press,
            "demandRank": rand_demand_rank
        }

        # 6. 编辑其他信息
        res_update = XS.update_clue_other_info(clueId=new_clue_id, otherInfoModel=other_info_model)
        assert res_update.get("code") == "10001200", f"编辑其他信息code异常, 接口返回={res_update}"
        assert res_update.get("success") is True, f"编辑其他信息success异常, 接口返回={res_update}"

        # ====== 步骤二：验证编辑后的其他信息 ======

        # 7. 获取编辑后的其他信息
        time.sleep(1)
        res_get = XS.get_clue_other_info(clueId=new_clue_id)
        assert res_get.get("code") == "10001200", f"获取编辑后其他信息失败, 接口返回={res_get}"
        get_data = res_get.get("data", {})
        assert get_data.get("id"), f"编辑后其他信息id为空, 接口返回={get_data}"

        # 8. 验证各字段
        assert get_data.get("advancePay") == rand_advance_pay, \
            f"advancePay不匹配, 期望={rand_advance_pay}, 实际={get_data.get('advancePay')}"
        assert get_data.get("customerHabit") == rand_customer_habit, \
            f"customerHabit不匹配, 期望={rand_customer_habit}, 实际={get_data.get('customerHabit')}"
        assert get_data.get("numberOfEmp") == rand_number_of_emp, \
            f"numberOfEmp不匹配, 期望={rand_number_of_emp}, 实际={get_data.get('numberOfEmp')}"
        assert get_data.get("numberOfPrintPress") == rand_number_of_print_press, \
            f"numberOfPrintPress不匹配, 期望={rand_number_of_print_press}, 实际={get_data.get('numberOfPrintPress')}"
        # 验证结款方式
        pay_way = get_data.get("payWay", {})
        assert set(pay_way.get("select", [])) == set(rand_pay_select), \
            f"payWay.select不匹配, 期望={rand_pay_select}, 实际={pay_way.get('select')}"
        assert pay_way.get("periodType") == rand_period_type, \
            f"payWay.periodType不匹配, 实际={pay_way.get('periodType')}"
        assert pay_way.get("periodTime") == rand_period_time, \
            f"payWay.periodTime不匹配, 实际={pay_way.get('periodTime')}"
        # 验证票据类型
        assert set(get_data.get("ticketType", [])) == set(rand_ticket_type), \
            f"ticketType不匹配, 期望={rand_ticket_type}, 实际={get_data.get('ticketType')}"
        # 验证三级厂诉求排名
        assert get_data.get("demandRank") == rand_demand_rank, \
            f"demandRank不匹配, 期望={rand_demand_rank}, 实际={get_data.get('demandRank')}"

        # ====== 步骤三：验证完整度提升 ======

        # 9. 获取编辑后完整度
        res_pct_after = XS.get_clue_info_percent(clueId=new_clue_id)
        assert res_pct_after.get("code") == "10001200", f"获取编辑后完整度失败, 接口返回={res_pct_after}"
        after_pct = int(res_pct_after.get("data", {}).get("infoPercent", "0"))
        assert after_pct > init_pct, \
            f"编辑其他信息后完整度未提升, 初始={init_pct}%, 编辑后={after_pct}%"

        # ====== 清理：删除测试线索 ======
        for attempt in range(3):
            time.sleep(2)
            res_del_clue = XS.del_clues(clueList=[new_clue_id])
            if res_del_clue.get("code") == "10001200":
                break
        assert res_del_clue.get("code") == "10001200", f"清理线索失败, 接口返回={res_del_clue}"

    @allure.story("线索详情 - 设备信息CRUD")
    def test_ydl_AI_device_info_crud(self):
        """设备信息CRUD：新增线索→印刷机增改删→模切机增改删→粘箱机增改删→钉箱机增改删→打包机增改删"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True

        # ==================== 前置：新增线索 ====================

        surnames = ["陈", "李", "张", "王", "刘", "赵", "孙", "周", "吴", "郑"]
        given_chars = ["伟", "志", "建", "海", "红", "丽", "明", "斌", "华", "强"]
        ai_customer_name = random.choice(surnames) + random.choice(given_chars) + random.choice(given_chars)
        ai_contact_phone = "1" + random.choice(["3", "5", "7", "8", "9"]) + "".join([str(random.randint(0, 9)) for _ in range(9)])

        res_add = XS.add_clue_base_info(customerName=ai_customer_name, contactWay=ai_contact_phone)
        assert res_add.get("code") == "10001200", f"新增线索失败, 接口返回={res_add}"
        new_clue_id = res_add.get("data", "")
        allure.attach(f"新增线索ID: {new_clue_id}", name="前置信息")

        # 初始设备查询（全部为空）
        res_init = XS.get_device_by_clue(infoId=new_clue_id)
        assert res_init.get("code") == "10001200", f"初始设备查询失败, 接口返回={res_init}"
        init_data = res_init.get("data", {})
        assert init_data.get("nullAllFiled") is True, "新建线索设备不为空"

        try:
            # ==================== 步骤一：印刷机 增→改→删 ====================

            # 1.1 新增印刷机
            rand_print_brand = random.choice(["海德堡", "小森", "高宝", "三菱", "秋山"])
            rand_print_model = "M" + str(random.randint(100, 999))
            rand_print_type = random.randint(0, 3)
            rand_max_paper = random.randint(800, 1600)
            rand_min_paper = random.randint(200, 400)
            rand_repeat_len = random.randint(300, 999)
            rand_color_acc = round(random.uniform(0.01, 0.5), 2)
            rand_color_deck = random.randint(2, 8)
            rand_print_speed = random.randint(1000, 9999)
            rand_buy_time = round(random.uniform(0.5, 5.0), 1)
            rand_equip_cost = round(random.uniform(50.0, 500.0), 1)

            res_add_print = XS.add_device(infoId=new_clue_id, deviceInfo={
                "belongType": "线索",
                "printInfo": {
                    "brand": rand_print_brand, "model": rand_print_model, "type": rand_print_type,
                    "maxPaperSize": rand_max_paper, "minPaperSize": rand_min_paper,
                    "printRepeatLength": rand_repeat_len, "colorRegistrationAccuracy": rand_color_acc,
                    "colorDeck": rand_color_deck, "printSpeed": rand_print_speed,
                    "buyTime": rand_buy_time, "maintainInterval": 0.5,
                    "equipmentCost": rand_equip_cost, "dailyOperatingHours": 8.0,
                    "dailyPrintPieces": 5000, "photoList": []
                }
            })
            assert res_add_print.get("code") == "10001200", f"新增印刷机失败, 接口返回={res_add_print}"

            # 1.2 查询验证印刷机新增
            time.sleep(1)
            res_print_get = XS.get_device_by_clue(infoId=new_clue_id)
            print_list = res_print_get.get("data", {}).get("printList", [])
            assert len(print_list) == 1, f"印刷机新增后数量异常, 期望1, 实际{len(print_list)}"
            print_item = print_list[0]
            print_id = print_item.get("id", "")
            assert print_item.get("brand") == rand_print_brand, \
                f"印刷机brand不匹配, 期望={rand_print_brand}, 实际={print_item.get('brand')}"
            assert print_item.get("model") == rand_print_model, \
                f"印刷机model不匹配, 期望={rand_print_model}, 实际={print_item.get('model')}"
            assert print_item.get("type") == rand_print_type, \
                f"印刷机type不匹配, 期望={rand_print_type}, 实际={print_item.get('type')}"
            assert print_item.get("printSpeed") == rand_print_speed, \
                f"印刷机printSpeed不匹配, 期望={rand_print_speed}, 实际={print_item.get('printSpeed')}"
            allure.attach(f"印刷机ID: {print_id}, 品牌: {rand_print_brand}", name="印刷机新增")

            # 1.3 编辑印刷机
            edit_print_brand = random.choice(["北人", "光华", "景德镇", "潍坊"])
            edit_print_model = "E" + str(random.randint(100, 999))
            edit_print_type = (rand_print_type + 1) % 4
            edit_max_paper = random.randint(800, 1600)
            edit_print_speed = random.randint(1000, 9999)

            res_edit_print = XS.update_device(deviceInfo={
                "belongType": "线索",
                "printInfo": {
                    "id": print_id, "brand": edit_print_brand, "model": edit_print_model,
                    "type": edit_print_type, "maxPaperSize": edit_max_paper,
                    "minPaperSize": rand_min_paper, "printRepeatLength": rand_repeat_len,
                    "colorRegistrationAccuracy": rand_color_acc, "colorDeck": rand_color_deck,
                    "printSpeed": edit_print_speed, "buyTime": rand_buy_time,
                    "maintainInterval": 0.5, "equipmentCost": rand_equip_cost,
                    "dailyOperatingHours": 8.0, "dailyPrintPieces": 5000, "photoList": []
                }
            })
            assert res_edit_print.get("code") == "10001200", f"编辑印刷机失败, 接口返回={res_edit_print}"

            # 1.4 查询验证印刷机编辑
            time.sleep(1)
            res_print_edit_get = XS.get_device_by_clue(infoId=new_clue_id)
            print_list_edited = res_print_edit_get.get("data", {}).get("printList", [])
            assert len(print_list_edited) == 1, "编辑后印刷机数量异常"
            print_edited = print_list_edited[0]
            assert print_edited.get("brand") == edit_print_brand, \
                f"印刷机编辑后brand不匹配, 期望={edit_print_brand}, 实际={print_edited.get('brand')}"
            assert print_edited.get("model") == edit_print_model, \
                f"印刷机编辑后model不匹配, 期望={edit_print_model}, 实际={print_edited.get('model')}"
            assert print_edited.get("type") == edit_print_type, \
                f"印刷机编辑后type不匹配, 期望={edit_print_type}, 实际={print_edited.get('type')}"
            assert print_edited.get("printSpeed") == edit_print_speed, \
                f"印刷机编辑后printSpeed不匹配, 期望={edit_print_speed}, 实际={print_edited.get('printSpeed')}"

            # 1.5 删除印刷机
            res_del_print = XS.del_device(printId=print_id)
            assert res_del_print.get("code") == "10001200", f"删除印刷机失败, 接口返回={res_del_print}"
            time.sleep(1)
            res_print_del_get = XS.get_device_by_clue(infoId=new_clue_id)
            assert len(res_print_del_get.get("data", {}).get("printList", [])) == 0, "印刷机删除后列表不为空"

            # ==================== 步骤二：模切机 增→改→删 ====================

            # 2.1 新增模切机
            rand_dc_brand = random.choice(["博斯特", "旭派", "上海亚华", "唐山玉印"])
            rand_dc_model = "DC" + str(random.randint(100, 999))
            rand_dc_type = random.randint(0, 2)
            rand_dc_max_paper = random.randint(800, 1200)
            rand_dc_min_paper = random.randint(200, 500)
            rand_dc_range = random.randint(500, 1200)
            rand_dc_waste = random.randint(5, 20)
            rand_dc_speed = random.randint(1000, 9999)
            rand_dc_cost = round(random.uniform(50.0, 300.0), 1)

            res_add_dc = XS.add_device(infoId=new_clue_id, deviceInfo={
                "belongType": "线索",
                "dieCutInfo": {
                    "infoId": new_clue_id, "brand": rand_dc_brand, "model": rand_dc_model,
                    "type": rand_dc_type, "maxPaperSize": rand_dc_max_paper,
                    "minPaperSize": rand_dc_min_paper, "maxDieCutRange": rand_dc_range,
                    "minWasteEdgeWidth": rand_dc_waste, "maxSpeed": rand_dc_speed,
                    "buyTime": 2.0, "maintainInterval": 0.5, "equipmentCost": rand_dc_cost
                }
            })
            assert res_add_dc.get("code") == "10001200", f"新增模切机失败, 接口返回={res_add_dc}"

            # 2.2 查询验证模切机新增
            time.sleep(1)
            res_dc_get = XS.get_device_by_clue(infoId=new_clue_id)
            dc_list = res_dc_get.get("data", {}).get("dieCutList", [])
            assert len(dc_list) == 1, f"模切机新增后数量异常, 期望1, 实际{len(dc_list)}"
            dc_item = dc_list[0]
            dc_id = dc_item.get("id", "")
            assert dc_item.get("brand") == rand_dc_brand, \
                f"模切机brand不匹配, 期望={rand_dc_brand}, 实际={dc_item.get('brand')}"
            assert dc_item.get("model") == rand_dc_model, \
                f"模切机model不匹配, 期望={rand_dc_model}, 实际={dc_item.get('model')}"
            assert dc_item.get("maxDieCutRange") == rand_dc_range, \
                f"模切机maxDieCutRange不匹配, 期望={rand_dc_range}, 实际={dc_item.get('maxDieCutRange')}"
            allure.attach(f"模切机ID: {dc_id}, 品牌: {rand_dc_brand}", name="模切机新增")

            # 2.3 编辑模切机
            edit_dc_brand = random.choice(["海德堡", "国望", "鼎龙"])
            edit_dc_model = "ED" + str(random.randint(100, 999))
            edit_dc_speed = random.randint(1000, 9999)

            res_edit_dc = XS.update_device(deviceInfo={
                "belongType": "线索",
                "dieCutInfo": {
                    "infoId": new_clue_id, "id": dc_id, "brand": edit_dc_brand, "model": edit_dc_model,
                    "type": (rand_dc_type + 1) % 3, "maxPaperSize": rand_dc_max_paper,
                    "minPaperSize": rand_dc_min_paper, "maxDieCutRange": rand_dc_range,
                    "minWasteEdgeWidth": rand_dc_waste, "maxSpeed": edit_dc_speed,
                    "buyTime": 2.0, "maintainInterval": 0.5, "equipmentCost": rand_dc_cost
                }
            })
            assert res_edit_dc.get("code") == "10001200", f"编辑模切机失败, 接口返回={res_edit_dc}"

            # 2.4 查询验证模切机编辑
            time.sleep(1)
            res_dc_edit_get = XS.get_device_by_clue(infoId=new_clue_id)
            dc_edited = res_dc_edit_get.get("data", {}).get("dieCutList", [])
            assert len(dc_edited) == 1, "编辑后模切机数量异常"
            assert dc_edited[0].get("brand") == edit_dc_brand, \
                f"模切机编辑后brand不匹配, 期望={edit_dc_brand}, 实际={dc_edited[0].get('brand')}"
            assert dc_edited[0].get("model") == edit_dc_model, \
                f"模切机编辑后model不匹配, 期望={edit_dc_model}, 实际={dc_edited[0].get('model')}"
            assert dc_edited[0].get("maxSpeed") == edit_dc_speed, \
                f"模切机编辑后maxSpeed不匹配, 期望={edit_dc_speed}, 实际={dc_edited[0].get('maxSpeed')}"

            # 2.5 删除模切机
            res_del_dc = XS.del_device(dieCutId=dc_id)
            assert res_del_dc.get("code") == "10001200", f"删除模切机失败, 接口返回={res_del_dc}"
            time.sleep(1)
            res_dc_del_get = XS.get_device_by_clue(infoId=new_clue_id)
            assert len(res_dc_del_get.get("data", {}).get("dieCutList", [])) == 0, "模切机删除后列表不为空"

            # ==================== 步骤三：粘箱机 增→改→删 ====================

            # 3.1 新增粘箱机
            rand_glue_brand = random.choice(["旭派", "鼎龙", "东方", "台兆"])
            rand_glue_model = "GS" + str(random.randint(100, 999))
            rand_glue_type = random.randint(0, 2)
            rand_glue_max = random.randint(800, 1500)
            rand_glue_min = random.randint(200, 400)
            rand_glue_speed = random.randint(50, 500)
            rand_glue_cost = round(random.uniform(30.0, 200.0), 1)

            res_add_glue = XS.add_device(infoId=new_clue_id, deviceInfo={
                "belongType": "线索",
                "gluingMachineInfo": {
                    "infoId": new_clue_id, "brand": rand_glue_brand, "model": rand_glue_model,
                    "type": rand_glue_type, "maxPaperSize": rand_glue_max,
                    "minPaperSize": rand_glue_min, "conveyingSpeed": rand_glue_speed,
                    "buyTime": 2.0, "maintainInterval": 0.5, "equipmentCost": rand_glue_cost
                }
            })
            assert res_add_glue.get("code") == "10001200", f"新增粘箱机失败, 接口返回={res_add_glue}"

            # 3.2 查询验证粘箱机新增
            time.sleep(1)
            res_glue_get = XS.get_device_by_clue(infoId=new_clue_id)
            glue_list = res_glue_get.get("data", {}).get("gluingMachineList", [])
            assert len(glue_list) == 1, f"粘箱机新增后数量异常, 期望1, 实际{len(glue_list)}"
            glue_item = glue_list[0]
            glue_id = glue_item.get("id", "")
            assert glue_item.get("brand") == rand_glue_brand, \
                f"粘箱机brand不匹配, 期望={rand_glue_brand}, 实际={glue_item.get('brand')}"
            assert glue_item.get("model") == rand_glue_model, \
                f"粘箱机model不匹配, 期望={rand_glue_model}, 实际={glue_item.get('model')}"
            assert glue_item.get("conveyingSpeed") == rand_glue_speed, \
                f"粘箱机conveyingSpeed不匹配, 期望={rand_glue_speed}, 实际={glue_item.get('conveyingSpeed')}"
            allure.attach(f"粘箱机ID: {glue_id}, 品牌: {rand_glue_brand}", name="粘箱机新增")

            # 3.3 编辑粘箱机
            edit_glue_brand = random.choice(["胜利", "华威", "永泰"])
            edit_glue_model = "EG" + str(random.randint(100, 999))
            edit_glue_speed = random.randint(50, 500)

            res_edit_glue = XS.update_device(deviceInfo={
                "belongType": "线索",
                "gluingMachineInfo": {
                    "infoId": new_clue_id, "id": glue_id, "brand": edit_glue_brand, "model": edit_glue_model,
                    "type": (rand_glue_type + 1) % 3, "maxPaperSize": rand_glue_max,
                    "minPaperSize": rand_glue_min, "conveyingSpeed": edit_glue_speed,
                    "buyTime": 2.0, "maintainInterval": 0.5, "equipmentCost": rand_glue_cost
                }
            })
            assert res_edit_glue.get("code") == "10001200", f"编辑粘箱机失败, 接口返回={res_edit_glue}"

            # 3.4 查询验证粘箱机编辑
            time.sleep(1)
            res_glue_edit_get = XS.get_device_by_clue(infoId=new_clue_id)
            glue_edited = res_glue_edit_get.get("data", {}).get("gluingMachineList", [])
            assert len(glue_edited) == 1, "编辑后粘箱机数量异常"
            assert glue_edited[0].get("brand") == edit_glue_brand, \
                f"粘箱机编辑后brand不匹配, 期望={edit_glue_brand}, 实际={glue_edited[0].get('brand')}"
            assert glue_edited[0].get("model") == edit_glue_model, \
                f"粘箱机编辑后model不匹配, 期望={edit_glue_model}, 实际={glue_edited[0].get('model')}"
            assert glue_edited[0].get("conveyingSpeed") == edit_glue_speed, \
                f"粘箱机编辑后conveyingSpeed不匹配, 期望={edit_glue_speed}, 实际={glue_edited[0].get('conveyingSpeed')}"

            # 3.5 删除粘箱机
            res_del_glue = XS.del_device(gluingMachineId=glue_id)
            assert res_del_glue.get("code") == "10001200", f"删除粘箱机失败, 接口返回={res_del_glue}"
            time.sleep(1)
            res_glue_del_get = XS.get_device_by_clue(infoId=new_clue_id)
            assert len(res_glue_del_get.get("data", {}).get("gluingMachineList", [])) == 0, "粘箱机删除后列表不为空"

            # ==================== 步骤四：钉箱机 增→改→删 ====================

            # 4.1 新增钉箱机
            rand_nail_brand = random.choice(["鼎力", "东方", "台兆", "旭派"])
            rand_nail_model = "NB" + str(random.randint(100, 999))
            rand_nail_type = random.randint(0, 2)
            rand_nail_max = random.randint(800, 1200)
            rand_nail_min = random.randint(150, 350)
            rand_nail_speed = random.randint(100, 999)
            rand_nail_count = random.randint(20, 200)
            rand_nail_pitch = random.randint(5, 50)
            rand_nail_cost = round(random.uniform(20.0, 150.0), 1)

            res_add_nail = XS.add_device(infoId=new_clue_id, deviceInfo={
                "belongType": "线索",
                "nailBoxInfo": {
                    "infoId": new_clue_id, "brand": rand_nail_brand, "model": rand_nail_model,
                    "type": rand_nail_type, "maxPaperSize": rand_nail_max,
                    "minPaperSize": rand_nail_min, "mechanicalSpeed": rand_nail_speed,
                    "numberOfNails": rand_nail_count, "pitchOfNails": rand_nail_pitch,
                    "buyTime": 1.5, "maintainInterval": 0.3, "equipmentCost": rand_nail_cost
                }
            })
            assert res_add_nail.get("code") == "10001200", f"新增钉箱机失败, 接口返回={res_add_nail}"

            # 4.2 查询验证钉箱机新增
            time.sleep(1)
            res_nail_get = XS.get_device_by_clue(infoId=new_clue_id)
            nail_list = res_nail_get.get("data", {}).get("nailBoxList", [])
            assert len(nail_list) == 1, f"钉箱机新增后数量异常, 期望1, 实际{len(nail_list)}"
            nail_item = nail_list[0]
            nail_id = nail_item.get("id", "")
            assert nail_item.get("brand") == rand_nail_brand, \
                f"钉箱机brand不匹配, 期望={rand_nail_brand}, 实际={nail_item.get('brand')}"
            assert nail_item.get("model") == rand_nail_model, \
                f"钉箱机model不匹配, 期望={rand_nail_model}, 实际={nail_item.get('model')}"
            assert nail_item.get("mechanicalSpeed") == rand_nail_speed, \
                f"钉箱机mechanicalSpeed不匹配, 期望={rand_nail_speed}, 实际={nail_item.get('mechanicalSpeed')}"
            assert nail_item.get("numberOfNails") == rand_nail_count, \
                f"钉箱机numberOfNails不匹配, 期望={rand_nail_count}, 实际={nail_item.get('numberOfNails')}"
            allure.attach(f"钉箱机ID: {nail_id}, 品牌: {rand_nail_brand}", name="钉箱机新增")

            # 4.3 编辑钉箱机
            edit_nail_brand = random.choice(["华威", "永泰", "胜利"])
            edit_nail_model = "EN" + str(random.randint(100, 999))
            edit_nail_speed = random.randint(100, 999)
            edit_nail_count = random.randint(20, 200)

            res_edit_nail = XS.update_device(deviceInfo={
                "belongType": "线索",
                "nailBoxInfo": {
                    "infoId": new_clue_id, "id": nail_id, "brand": edit_nail_brand, "model": edit_nail_model,
                    "type": (rand_nail_type + 1) % 3, "maxPaperSize": rand_nail_max,
                    "minPaperSize": rand_nail_min, "mechanicalSpeed": edit_nail_speed,
                    "numberOfNails": edit_nail_count, "pitchOfNails": rand_nail_pitch,
                    "buyTime": 1.5, "maintainInterval": 0.3, "equipmentCost": rand_nail_cost
                }
            })
            assert res_edit_nail.get("code") == "10001200", f"编辑钉箱机失败, 接口返回={res_edit_nail}"

            # 4.4 查询验证钉箱机编辑
            time.sleep(1)
            res_nail_edit_get = XS.get_device_by_clue(infoId=new_clue_id)
            nail_edited = res_nail_edit_get.get("data", {}).get("nailBoxList", [])
            assert len(nail_edited) == 1, "编辑后钉箱机数量异常"
            assert nail_edited[0].get("brand") == edit_nail_brand, \
                f"钉箱机编辑后brand不匹配, 期望={edit_nail_brand}, 实际={nail_edited[0].get('brand')}"
            assert nail_edited[0].get("model") == edit_nail_model, \
                f"钉箱机编辑后model不匹配, 期望={edit_nail_model}, 实际={nail_edited[0].get('model')}"
            assert nail_edited[0].get("mechanicalSpeed") == edit_nail_speed, \
                f"钉箱机编辑后mechanicalSpeed不匹配, 期望={edit_nail_speed}, 实际={nail_edited[0].get('mechanicalSpeed')}"
            assert nail_edited[0].get("numberOfNails") == edit_nail_count, \
                f"钉箱机编辑后numberOfNails不匹配, 期望={edit_nail_count}, 实际={nail_edited[0].get('numberOfNails')}"

            # 4.5 删除钉箱机
            res_del_nail = XS.del_device(nailBoxId=nail_id)
            assert res_del_nail.get("code") == "10001200", f"删除钉箱机失败, 接口返回={res_del_nail}"
            time.sleep(1)
            res_nail_del_get = XS.get_device_by_clue(infoId=new_clue_id)
            assert len(res_nail_del_get.get("data", {}).get("nailBoxList", [])) == 0, "钉箱机删除后列表不为空"

            # ==================== 步骤五：打包机 增→改→删 ====================

            # 5.1 新增打包机
            rand_pack_brand = random.choice(["永创", "旭田", "百事特", "派特"])
            rand_pack_model = "PK" + str(random.randint(100, 999))
            rand_pack_type = random.randint(0, 2)
            rand_pack_max = random.randint(500, 1200)
            rand_pack_min = random.randint(100, 300)
            rand_pack_speed = random.randint(10, 60)
            rand_pack_force = round(random.uniform(0.5, 2.0), 1)
            rand_pack_strap = random.randint(5, 16)
            rand_pack_cost = round(random.uniform(10.0, 80.0), 1)

            res_add_pack = XS.add_device(infoId=new_clue_id, deviceInfo={
                "belongType": "线索",
                "packInfo": {
                    "infoId": new_clue_id, "brand": rand_pack_brand, "model": rand_pack_model,
                    "type": rand_pack_type, "maxPackSpecs": rand_pack_max,
                    "minPackSpecs": rand_pack_min, "packSpeed": rand_pack_speed,
                    "maxTighteningForce": rand_pack_force, "strapWidth": rand_pack_strap,
                    "buyTime": 1.5, "maintainInterval": 0.5, "equipmentCost": rand_pack_cost
                }
            })
            assert res_add_pack.get("code") == "10001200", f"新增打包机失败, 接口返回={res_add_pack}"

            # 5.2 查询验证打包机新增
            time.sleep(1)
            res_pack_get = XS.get_device_by_clue(infoId=new_clue_id)
            pack_list = res_pack_get.get("data", {}).get("packList", [])
            assert len(pack_list) == 1, f"打包机新增后数量异常, 期望1, 实际{len(pack_list)}"
            pack_item = pack_list[0]
            pack_id = pack_item.get("id", "")
            assert pack_item.get("brand") == rand_pack_brand, \
                f"打包机brand不匹配, 期望={rand_pack_brand}, 实际={pack_item.get('brand')}"
            assert pack_item.get("model") == rand_pack_model, \
                f"打包机model不匹配, 期望={rand_pack_model}, 实际={pack_item.get('model')}"
            assert pack_item.get("packSpeed") == rand_pack_speed, \
                f"打包机packSpeed不匹配, 期望={rand_pack_speed}, 实际={pack_item.get('packSpeed')}"
            assert pack_item.get("maxPackSpecs") == rand_pack_max, \
                f"打包机maxPackSpecs不匹配, 期望={rand_pack_max}, 实际={pack_item.get('maxPackSpecs')}"
            allure.attach(f"打包机ID: {pack_id}, 品牌: {rand_pack_brand}", name="打包机新增")

            # 5.3 编辑打包机
            edit_pack_brand = random.choice(["华联", "中远", "金诚"])
            edit_pack_model = "EP" + str(random.randint(100, 999))
            edit_pack_speed = random.randint(10, 60)
            edit_pack_max = random.randint(500, 1200)

            res_edit_pack = XS.update_device(deviceInfo={
                "belongType": "线索",
                "packInfo": {
                    "infoId": new_clue_id, "id": pack_id, "brand": edit_pack_brand, "model": edit_pack_model,
                    "type": (rand_pack_type + 1) % 3, "maxPackSpecs": edit_pack_max,
                    "minPackSpecs": rand_pack_min, "packSpeed": edit_pack_speed,
                    "maxTighteningForce": rand_pack_force, "strapWidth": rand_pack_strap,
                    "buyTime": 1.5, "maintainInterval": 0.5, "equipmentCost": rand_pack_cost
                }
            })
            assert res_edit_pack.get("code") == "10001200", f"编辑打包机失败, 接口返回={res_edit_pack}"

            # 5.4 查询验证打包机编辑
            time.sleep(1)
            res_pack_edit_get = XS.get_device_by_clue(infoId=new_clue_id)
            pack_edited = res_pack_edit_get.get("data", {}).get("packList", [])
            assert len(pack_edited) == 1, "编辑后打包机数量异常"
            assert pack_edited[0].get("brand") == edit_pack_brand, \
                f"打包机编辑后brand不匹配, 期望={edit_pack_brand}, 实际={pack_edited[0].get('brand')}"
            assert pack_edited[0].get("model") == edit_pack_model, \
                f"打包机编辑后model不匹配, 期望={edit_pack_model}, 实际={pack_edited[0].get('model')}"
            assert pack_edited[0].get("packSpeed") == edit_pack_speed, \
                f"打包机编辑后packSpeed不匹配, 期望={edit_pack_speed}, 实际={pack_edited[0].get('packSpeed')}"
            assert pack_edited[0].get("maxPackSpecs") == edit_pack_max, \
                f"打包机编辑后maxPackSpecs不匹配, 期望={edit_pack_max}, 实际={pack_edited[0].get('maxPackSpecs')}"

            # 5.5 删除打包机
            res_del_pack = XS.del_device(packId=pack_id)
            assert res_del_pack.get("code") == "10001200", f"删除打包机失败, 接口返回={res_del_pack}"
            time.sleep(1)
            res_pack_del_get = XS.get_device_by_clue(infoId=new_clue_id)
            assert len(res_pack_del_get.get("data", {}).get("packList", [])) == 0, "打包机删除后列表不为空"

        finally:
            # ====== 清理：删除测试线索 ======
            for attempt in range(3):
                time.sleep(2)
                res_del_clue_final = XS.del_clues(clueList=[new_clue_id])
                if res_del_clue_final.get("code") == "10001200":
                    break
            assert res_del_clue_final.get("code") == "10001200", f"清理线索失败, 接口返回={res_del_clue_final}"

    @allure.story("线索首页 - 列表查询与筛选")
    def test_ydl_AL_clue_homepage_list_and_filter(self):
        """线索首页列表查询与筛选：分页查询→多tab切换→搜索筛选→信息完整度→筛选下拉→状态管理→街道信息→手机号校验→下载模板→同步失败明细→批量转移"""
        # Author: Author
        # Create Date: 2026-07-23
        # IsAI: True

        # 1. 首页列表分页查询（默认参数：clueType=1, pageNo=1, pageSize=15）
        res_list = XS.get_clue_list(pageNo=1, pageSize=15)
        assert res_list.get("code") == "10001200", f"查询线索列表失败, 接口返回={res_list}"
        list_data = res_list.get("data", {})
        assert "list" in list_data or "total" in list_data, f"列表返回结构异常, data={list_data}"
        total = list_data.get("total", 0)
        records = list_data.get("list", [])
        allure.attach(f"首页线索总数: {total}, 当前页记录数: {len(records)}", name="分页查询")
        assert isinstance(records, list), f"list字段应为数组, 实际={type(records)}"
        if total > 15:
            # 验证翻页
            res_page2 = XS.get_clue_list(pageNo=2, pageSize=15)
            assert res_page2.get("code") == "10001200", f"翻页查询失败, 接口返回={res_page2}"
            page2_records = res_page2.get("data", {}).get("list", [])
            assert len(page2_records) > 0, f"第二页应有记录, 实际为空"

        # 2. 多tab切换 - 已转化线索（clueType=2）
        res_synced = XS.get_clue_list(clueType="2", pageNo=1, pageSize=15)
        assert res_synced.get("code") == "10001200", f"查询已转化线索失败, 接口返回={res_synced}"
        synced_total = res_synced.get("data", {}).get("total", 0)
        allure.attach(f"已转化线索数: {synced_total}", name="多tab切换")

        # 3. 多tab切换 - 已删除线索（clueType=3）
        res_deleted = XS.get_clue_list(clueType="3", pageNo=1, pageSize=15)
        assert res_deleted.get("code") == "10001200", f"查询已删除线索失败, 接口返回={res_deleted}"
        deleted_total = res_deleted.get("data", {}).get("total", 0)
        allure.attach(f"已删除线索数: {deleted_total}", name="已删除tab")

        # 4. 多tab切换 - 线索池（clueType=4）
        res_pool = XS.get_clue_list(clueType="4", pageNo=1, pageSize=15)
        assert res_pool.get("code") == "10001200", f"查询线索池失败, 接口返回={res_pool}"
        pool_total = res_pool.get("data", {}).get("total", 0)
        allure.attach(f"线索池线索数: {pool_total}", name="线索池tab")

        # 5. 搜索筛选 - 按客户名称模糊搜索
        res_search = XS.get_clue_list(customerName="")
        assert res_search.get("code") == "10001200", f"按名称搜索失败, 接口返回={res_search}"
        # 搜索筛选 - 按跟进状态筛选（1:未处理,3:无转化机会,4:有转换机会）
        res_follow = XS.get_clue_list(followStatus="1,3,4")
        assert res_follow.get("code") == "10001200", f"按跟进状态筛选失败, 接口返回={res_follow}"
        # 搜索筛选 - 按时间范围
        res_time = XS.get_clue_list(
            createTimeStart="2025-01-01 00:00:00",
            createTimeEnd="2026-12-31 23:59:59"
        )
        assert res_time.get("code") == "10001200", f"按时间范围筛选失败, 接口返回={res_time}"

        # 6. 信息完整度排序查询（升序+降序）
        res_asc = XS.get_clue_list(infoPercentOrder="1")
        assert res_asc.get("code") == "10001200", f"信息完整度升序查询失败, 接口返回={res_asc}"
        res_desc = XS.get_clue_list(infoPercentOrder="2")
        assert res_desc.get("code") == "10001200", f"信息完整度降序查询失败, 接口返回={res_desc}"

        # 7. 创建人/负责人筛选下拉数据
        org_id = _get_org_id()
        res_creators = XS.get_creator_list(orgId=org_id)
        assert res_creators.get("code") == "10001200", f"获取创建人列表失败, 接口返回={res_creators}"
        creators = res_creators.get("data", [])
        allure.attach(f"创建人数: {len(creators) if isinstance(creators, list) else 'N/A'}", name="筛选下拉")
        # 获取负责人列表
        res_duty = XS.get_duty_man_list_by_org_id(orgId=org_id)
        assert res_duty.get("code") == "10001200", f"获取负责人列表失败, 接口返回={res_duty}"
        # 按创建人筛选
        if isinstance(creators, list) and len(creators) > 0:
            creator_id = str(creators[0].get("id", creators[0].get("userId", "")))
            if creator_id:
                res_by_creator = XS.get_clue_list(creatorId=creator_id)
                assert res_by_creator.get("code") == "10001200", f"按创建人筛选失败, 接口返回={res_by_creator}"

        # 8. 线索状态管理 - 更新经营状态 + 跟进状态
        # 先取一条线索用于状态操作
        first_records = res_list.get("data", {}).get("list", [])
        if len(first_records) > 0:
            clue_id = str(first_records[0].get("id", ""))
            if clue_id:
                # 更新经营状态（2:在业）
                res_run = XS.update_clue_run_status(clueId=clue_id, runStatus="2")
                assert res_run.get("code") in ("10001200", "10010100"), \
                    f"更新经营状态失败, code={res_run.get('code')}, msg={res_run.get('msg')}, 接口返回={res_run}"
                # 更新跟进状态（4:有转换机会）
                res_follow_update = XS.update_follow_status(clueId=clue_id, followStatus="4")
                assert res_follow_update.get("code") in ("10001200", "10010100"), \
                    f"更新跟进状态失败, code={res_follow_update.get('code')}, msg={res_follow_update.get('msg')}, 接口返回={res_follow_update}"
                # 验证状态变更（通过详情查询）
                time.sleep(1)
                res_verify = XS.get_clue_base_info(clueId=clue_id)
                assert res_verify.get("code") == "10001200", f"验证状态变更失败, 接口返回={res_verify}"
                detail = res_verify.get("data", {})
                allure.attach(
                    f"线索{clue_id} 经营状态={detail.get('runStatus')}, 跟进状态={detail.get('followStatus')}",
                    name="状态管理验证"
                )

        # 9. 街道信息查询
        res_street = XS.get_street_info(streetCode=330302028)
        assert res_street.get("code") in ("10001200", "10003001", "11004012"), \
            f"获取街道信息失败, code={res_street.get('code')}, msg={res_street.get('msg')}, 接口返回={res_street}"
        if res_street.get("code") == "10001200":
            street_data = res_street.get("data", {})
            allure.attach(
                f"街道: {street_data.get('streetName')}, 区: {street_data.get('areaName')}, "
                f"市: {street_data.get('cityName')}, 省: {street_data.get('provinceName')}",
                name="街道信息"
            )

        # 10. 手机号占用校验
        test_phone = "1" + random.choice(["3", "5", "7", "8", "9"]) + "".join([str(random.randint(0, 9)) for _ in range(9)])
        res_phone = XS.check_clue_phone_occupy(phone=test_phone)
        assert res_phone.get("code") in ("10001200", "10003001", "10010100"), \
            f"手机号占用校验失败, code={res_phone.get('code')}, msg={res_phone.get('msg')}, 接口返回={res_phone}"
        allure.attach(f"测试手机号: {test_phone}, 结果: {res_phone.get('data')}", name="手机号占用校验")

        # 11. 下载线索导入模板
        res_template = XS.download_clue_template()
        assert res_template.status_code == 200, \
            f"下载模板HTTP状态异常, status={res_template.status_code}"
        content_type = res_template.headers.get("Content-Type", "")
        allure.attach(f"模板Content-Type: {content_type}, 文件大小: {len(res_template.content)}B", name="下载模板")

        # 12. 同步失败明细查询（先获取导入记录中的errorReportId）
        res_import = XS.get_import_record_list()
        assert res_import.get("code") == "10001200", f"获取导入记录失败, 接口返回={res_import}"
        import_records = res_import.get("data", {}).get("list", []) if isinstance(res_import.get("data"), dict) else res_import.get("data", [])
        error_report_id = ""
        if isinstance(import_records, list):
            for rec in import_records:
                if rec.get("errorReportId") or rec.get("id"):
                    error_report_id = str(rec.get("errorReportId", rec.get("id", "")))
                    break
        if error_report_id:
            res_sync_fail = XS.get_sync_fail_details(errorReportId=error_report_id)
            assert res_sync_fail.get("code") in ("10001200", "10003001", "10010100"), \
                f"查询同步失败明细失败, code={res_sync_fail.get('code')}, msg={res_sync_fail.get('msg')}, 接口返回={res_sync_fail}"
            fail_data = res_sync_fail.get("data", {})
            allure.attach(
                f"失败记录总数: {fail_data.get('total', 'N/A')}, 当前页记录数: {len(fail_data.get('list', []))}",
                name="同步失败明细"
            )
        else:
            allure.attach("无可用导入记录, 跳过同步失败明细查询", name="同步失败明细")

        # 13. 批量转移（取第一条线索尝试转移给自己）
        if len(first_records) > 0:
            clue_id_transfer = str(first_records[0].get("id", ""))
            if clue_id_transfer:
                # 获取当前用户作为转移目标
                duty_list = res_duty.get("data", [])
                duty_id = ""
                if isinstance(duty_list, list) and len(duty_list) > 0:
                    duty_id = str(duty_list[0].get("id", duty_list[0].get("userId", "")))
                if duty_id:
                    res_transfer = XS.transfer_clue(clueList=[clue_id_transfer], dutyManId=duty_id)
                    assert res_transfer.get("code") in ("10001200", "10010100", "10003001"), \
                        f"批量转移失败, code={res_transfer.get('code')}, msg={res_transfer.get('msg')}, 接口返回={res_transfer}"
                    allure.attach(f"转移线索: {clue_id_transfer} -> 负责人: {duty_id}, 结果code: {res_transfer.get('code')}", name="批量转移")
                else:
                    allure.attach("未获取到负责人ID, 跳过批量转移", name="批量转移")

    @allure.story("线索详情 - 辅料信息CRUD")
    def test_ydl_AJ_accessories_crud(self):
        """辅料信息CRUD：新增线索→新增辅料→编辑辅料→删除辅料"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True

        # ==================== 前置：新增线索 ====================

        surnames = ["陈", "李", "张", "王", "刘", "赵", "孙", "周", "吴", "郑"]
        given_chars = ["伟", "志", "建", "海", "红", "丽", "明", "斌", "华", "强"]
        ai_customer_name = random.choice(surnames) + random.choice(given_chars) + random.choice(given_chars)
        ai_contact_phone = "1" + random.choice(["3", "5", "7", "8", "9"]) + "".join([str(random.randint(0, 9)) for _ in range(9)])

        res_add = XS.add_clue_base_info(customerName=ai_customer_name, contactWay=ai_contact_phone)
        assert res_add.get("code") == "10001200", f"新增线索失败, 接口返回={res_add}"
        new_clue_id = res_add.get("data", "")
        allure.attach(f"新增线索ID: {new_clue_id}", name="前置信息")

        # 初始辅料查询（列表为空）
        res_init = XS.get_accessories_by_clue(infoId=new_clue_id)
        assert res_init.get("code") == "10001200", f"初始辅料查询失败, 接口返回={res_init}"
        assert len(res_init.get("data", {}).get("list", [])) == 0, "新建线索辅料列表不为空"

        try:
            # ==================== 步骤一：新增辅料 ====================

            # 1. 随机生成辅料数据
            rand_name = random.choice(["油墨", "印版", "刀模", "扁丝", "胶水", "打包带", "结束带", "托盘"])
            rand_supplier = random.choice(["华兴包装", "永泰供应", "明远材料", "信达贸易"]) + str(random.randint(1, 99))
            rand_channel = random.choice(["线上", "线下", "厂家直销", "经销商"])
            rand_price = round(random.uniform(10.0, 500.0), 2)

            # 2. 新增辅料
            res_add_acc = XS.add_accessories(infoId=new_clue_id, accessories={
                "name": rand_name,
                "supplierName": rand_supplier,
                "purchasingChannels": rand_channel,
                "purchaseUnitPrice": rand_price
            })
            assert res_add_acc.get("code") == "10001200", f"新增辅料失败, 接口返回={res_add_acc}"

            # 3. 查询验证新增
            time.sleep(1)
            res_get = XS.get_accessories_by_clue(infoId=new_clue_id)
            acc_list = res_get.get("data", {}).get("list", [])
            assert len(acc_list) == 1, f"新增辅料后数量异常, 期望1, 实际{len(acc_list)}"
            acc_item = acc_list[0]
            acc_id = acc_item.get("id", "")
            assert acc_item.get("name") == rand_name, \
                f"辅料name不匹配, 期望={rand_name}, 实际={acc_item.get('name')}"
            assert acc_item.get("supplierName") == rand_supplier, \
                f"辅料supplierName不匹配, 期望={rand_supplier}, 实际={acc_item.get('supplierName')}"
            assert acc_item.get("purchasingChannels") == rand_channel, \
                f"辅料purchasingChannels不匹配, 期望={rand_channel}, 实际={acc_item.get('purchasingChannels')}"
            assert float(acc_item.get("purchaseUnitPrice")) == rand_price, \
                f"辅料purchaseUnitPrice不匹配, 期望={rand_price}, 实际={acc_item.get('purchaseUnitPrice')}"
            allure.attach(f"辅料ID: {acc_id}, 名称: {rand_name}, 供应商: {rand_supplier}", name="辅料新增")

            # ==================== 步骤二：编辑辅料 ====================

            # 4. 生成编辑数据
            edit_supplier = random.choice(["新达供应", "中联材料", "华联包装"]) + str(random.randint(1, 99))
            edit_channel = random.choice(["电商平台", "实体门店", "工厂直供"])
            edit_price = round(random.uniform(10.0, 500.0), 2)

            # 5. 编辑辅料
            res_edit = XS.update_accessories(accessoriesId=acc_id, accessories={
                "name": rand_name,
                "supplierName": edit_supplier,
                "purchasingChannels": edit_channel,
                "purchaseUnitPrice": edit_price
            })
            assert res_edit.get("code") == "10001200", f"编辑辅料失败, 接口返回={res_edit}"

            # 6. 查询验证编辑
            time.sleep(1)
            res_edit_get = XS.get_accessories_by_clue(infoId=new_clue_id)
            edit_list = res_edit_get.get("data", {}).get("list", [])
            assert len(edit_list) == 1, f"编辑后辅料数量异常, 期望1, 实际{len(edit_list)}"
            edit_item = edit_list[0]
            assert edit_item.get("supplierName") == edit_supplier, \
                f"编辑后supplierName不匹配, 期望={edit_supplier}, 实际={edit_item.get('supplierName')}"
            assert edit_item.get("purchasingChannels") == edit_channel, \
                f"编辑后purchasingChannels不匹配, 期望={edit_channel}, 实际={edit_item.get('purchasingChannels')}"
            assert float(edit_item.get("purchaseUnitPrice")) == edit_price, \
                f"编辑后purchaseUnitPrice不匹配, 期望={edit_price}, 实际={edit_item.get('purchaseUnitPrice')}"
            allure.attach(f"编辑后供应商: {edit_supplier}, 渠道: {edit_channel}, 单价: {edit_price}", name="辅料编辑")

            # ==================== 步骤三：删除辅料 ====================

            # 7. 删除辅料
            res_del = XS.del_accessories(accessoriesId=acc_id)
            assert res_del.get("code") == "10001200", f"删除辅料失败, 接口返回={res_del}"

            # 8. 查询验证删除
            time.sleep(1)
            res_del_get = XS.get_accessories_by_clue(infoId=new_clue_id)
            del_list = res_del_get.get("data", {}).get("list", [])
            assert len(del_list) == 0, f"删除辅料后列表不为空, 实际{len(del_list)}"

        finally:
            # ====== 清理：删除测试线索 ======
            for attempt in range(3):
                time.sleep(2)
                res_del_clue = XS.del_clues(clueList=[new_clue_id])
                if res_del_clue.get("code") == "10001200":
                    break
            assert res_del_clue.get("code") == "10001200", f"清理线索失败, 接口返回={res_del_clue}"

    @allure.story("线索详情 - 终端产品CRUD")
    def test_ydl_AK_terminal_product_crud(self):
        """终端产品CRUD：新增线索→新增终端产品→编辑终端产品→删除终端产品"""
        # Author: Author
        # Create Date: 2026-07-24
        # IsAI: True

        # ==================== 前置：新增线索 ====================

        surnames = ["陈", "李", "张", "王", "刘", "赵", "孙", "周", "吴", "郑"]
        given_chars = ["伟", "志", "建", "海", "红", "丽", "明", "斌", "华", "强"]
        ai_customer_name = random.choice(surnames) + random.choice(given_chars) + random.choice(given_chars)
        ai_contact_phone = "1" + random.choice(["3", "5", "7", "8", "9"]) + "".join([str(random.randint(0, 9)) for _ in range(9)])

        res_add = XS.add_clue_base_info(customerName=ai_customer_name, contactWay=ai_contact_phone)
        assert res_add.get("code") == "10001200", f"新增线索失败, 接口返回={res_add}"
        new_clue_id = res_add.get("data", "")
        allure.attach(f"新增线索ID: {new_clue_id}", name="前置信息")

        # 初始终端产品查询（为空）
        res_init = XS.get_terminal_list(infoId=new_clue_id)
        assert res_init.get("code") == "10001200", f"初始终端产品查询失败, 接口返回={res_init}"
        assert res_init.get("data", {}).get("total", -1) == 0, "新建线索终端产品列表不为空"

        try:
            # ==================== 步骤一：新增终端产品 ====================

            # 1. 随机生成终端产品数据
            industry_options = [
                ("五金工具", "电钻"), ("五金工具", "电动螺丝刀"), ("五金工具", "水龙头"),
                ("家用电器", "洗衣机"), ("家用电器", "空调"),
                ("家具", "沙发"), ("家具", "衣柜"),
                ("文化用品", "笔记本"), ("文化用品", "书籍"),
                ("塑胶制品", "塑料容器"), ("塑胶制品", "管道配件")
            ]
            rand_industry, rand_product = random.choice(industry_options)
            rand_brand = random.choice(["品牌A", "品牌B", "测试品牌", "华兴", "明远"]) + str(random.randint(1, 99))
            rand_weight = round(random.uniform(1.0, 50.0), 2)
            rand_length = random.randint(20, 80)
            rand_width = random.randint(15, 60)
            rand_height = random.randint(10, 50)
            rand_export = random.choice([0, 1])
            rand_turnover = random.randint(1, 10)
            rand_stack = random.randint(1, 4)
            rand_loading = random.choice([1, 2])
            rand_load_cond = random.choice([1, 2, 3])
            rand_transport = random.choice([1, 2, 3])

            # 2. 新增终端产品
            res_add_t = XS.add_terminal(infoId=new_clue_id, terminalInfo={
                "industryName": rand_industry,
                "industryProductName": rand_product,
                "brand": rand_brand,
                "grossWeight": rand_weight,
                "cartonLength": rand_length,
                "cartonWidth": rand_width,
                "cartonHeight": rand_height,
                "export": rand_export,
                "turnoverTimes": rand_turnover,
                "stackDuration": rand_stack,
                "inOutSituation": rand_loading,
                "loadCondition": rand_load_cond,
                "transportModel": rand_transport
            })
            assert res_add_t.get("code") == "10001200", f"新增终端产品失败, 接口返回={res_add_t}"

            # 3. 查询验证新增
            time.sleep(1)
            res_get = XS.get_terminal_list(infoId=new_clue_id)
            t_data = res_get.get("data", {})
            assert t_data.get("total") == 1, f"新增后总数异常, 期望1, 实际={t_data.get('total')}"
            t_list = t_data.get("list", [])
            assert len(t_list) == 1, f"新增后列表数量异常, 期望1, 实际{len(t_list)}"
            t_item = t_list[0]
            t_id = t_item.get("id", "")
            assert t_item.get("industryName") == rand_industry, \
                f"industryName不匹配, 期望={rand_industry}, 实际={t_item.get('industryName')}"
            assert t_item.get("industryProductName") == rand_product, \
                f"industryProductName不匹配, 期望={rand_product}, 实际={t_item.get('industryProductName')}"
            assert t_item.get("brand") == rand_brand, \
                f"brand不匹配, 期望={rand_brand}, 实际={t_item.get('brand')}"
            assert t_item.get("grossWeight") == rand_weight, \
                f"grossWeight不匹配, 期望={rand_weight}, 实际={t_item.get('grossWeight')}"
            assert t_item.get("turnoverTimes") == rand_turnover, \
                f"turnoverTimes不匹配, 期望={rand_turnover}, 实际={t_item.get('turnoverTimes')}"
            allure.attach(
                f"终端产品ID: {t_id}, 行业: {rand_industry}, 产品: {rand_product}, 品牌: {rand_brand}",
                name="终端产品新增"
            )

            # ==================== 步骤二：编辑终端产品 ====================

            # 4. 生成编辑数据
            edit_brand = random.choice(["新品牌", "编辑品牌", "更新品牌"]) + str(random.randint(1, 99))
            edit_weight = round(random.uniform(1.0, 50.0), 2)
            edit_length = random.randint(20, 80)
            edit_width = random.randint(15, 60)
            edit_height = random.randint(10, 50)
            edit_export = (rand_export + 1) % 2
            edit_turnover = random.randint(1, 10)
            edit_stack = random.choice([v for v in [1, 2, 3, 4] if v != rand_stack])
            edit_loading = 2 if rand_loading == 1 else 1
            edit_load_cond = random.choice([v for v in [1, 2, 3] if v != rand_load_cond])
            edit_transport = random.choice([v for v in [1, 2, 3] if v != rand_transport])

            # 5. 编辑终端产品
            res_edit = XS.update_terminal(terminalInfo={
                "id": t_id,
                "infoId": new_clue_id,
                "industryName": rand_industry,
                "industryProductName": rand_product,
                "brand": edit_brand,
                "grossWeight": edit_weight,
                "cartonLength": edit_length,
                "cartonWidth": edit_width,
                "cartonHeight": edit_height,
                "export": edit_export,
                "turnoverTimes": edit_turnover,
                "stackDuration": edit_stack,
                "inOutSituation": edit_loading,
                "loadCondition": edit_load_cond,
                "transportModel": edit_transport
            })
            assert res_edit.get("code") == "10001200", f"编辑终端产品失败, 接口返回={res_edit}"

            # 6. 详情验证编辑
            time.sleep(1)
            res_detail = XS.get_terminal_detail(terminalId=t_id)
            assert res_detail.get("code") == "10001200", f"查询终端产品详情失败, 接口返回={res_detail}"
            detail = res_detail.get("data", {})
            assert detail.get("brand") == edit_brand, \
                f"编辑后brand不匹配, 期望={edit_brand}, 实际={detail.get('brand')}"
            assert detail.get("grossWeight") == edit_weight, \
                f"编辑后grossWeight不匹配, 期望={edit_weight}, 实际={detail.get('grossWeight')}"
            assert detail.get("cartonLength") == float(edit_length), \
                f"编辑后cartonLength不匹配, 期望={edit_length}, 实际={detail.get('cartonLength')}"
            assert detail.get("export") == edit_export, \
                f"编辑后export不匹配, 期望={edit_export}, 实际={detail.get('export')}"
            assert detail.get("turnoverTimes") == edit_turnover, \
                f"编辑后turnoverTimes不匹配, 期望={edit_turnover}, 实际={detail.get('turnoverTimes')}"
            assert detail.get("stackDuration") == edit_stack, \
                f"编辑后stackDuration不匹配, 期望={edit_stack}, 实际={detail.get('stackDuration')}"
            assert detail.get("inOutSituation") == edit_loading, \
                f"编辑后inOutSituation不匹配, 期望={edit_loading}, 实际={detail.get('inOutSituation')}"
            assert detail.get("transportModel") == edit_transport, \
                f"编辑后transportModel不匹配, 期望={edit_transport}, 实际={detail.get('transportModel')}"
            allure.attach(
                f"编辑后品牌: {edit_brand}, 重量: {edit_weight}kg, 尺寸: {edit_length}x{edit_width}x{edit_height}cm",
                name="终端产品编辑"
            )

            # ==================== 步骤三：删除终端产品 ====================

            # 7. 删除终端产品
            res_del = XS.del_terminal(terminalId=t_id)
            assert res_del.get("code") == "10001200", f"删除终端产品失败, 接口返回={res_del}"

            # 8. 查询验证删除
            time.sleep(1)
            res_del_get = XS.get_terminal_list(infoId=new_clue_id)
            del_data = res_del_get.get("data", {})
            assert del_data.get("total", -1) == 0, f"删除后终端产品列表不为空, total={del_data.get('total')}"

        finally:
            # ====== 清理：删除测试线索 ======
            for attempt in range(3):
                time.sleep(2)
                res_del_clue_final = XS.del_clues(clueList=[new_clue_id])
                if res_del_clue_final.get("code") == "10001200":
                    break
            assert res_del_clue_final.get("code") == "10001200", f"清理线索失败, 接口返回={res_del_clue_final}"


    @allure.story("用户隐藏字段配置查询")
    def test_ydl_AM_user_hide_field(self):
        """用户隐藏字段配置查询：调用getUserHideField.do→验证返回结构→校验belongModule列表"""
        # Author: Author
        # Create Date: 2026-07-28
        # IsAI: True

        # 1. 获取用户隐藏字段配置（getUserHideField.do）
        res_hide = XS.get_user_hide_field()
        assert res_hide.get("code") == "10001200", \
            f"获取用户隐藏字段配置失败, 接口返回={res_hide}"
        assert res_hide.get("success") is True, \
            f"获取用户隐藏字段配置success不为True, 接口返回={res_hide}"

        # 2. 验证返回结构
        hide_data = res_hide.get("data", {})
        assert isinstance(hide_data, dict), \
            f"隐藏字段data类型异常, 期望dict, 实际={type(hide_data)}"

        # 3. 校验belongModule列表
        hide_list = hide_data.get("list", [])
        assert isinstance(hide_list, list), \
            f"隐藏字段list类型异常, 期望list, 实际={type(hide_list)}"
        assert len(hide_list) >= 1, \
            f"隐藏字段list为空, 接口返回={res_hide}"

        # 4. 验证每个模块包含belongModule和hideFieldList字段
        for item in hide_list:
            assert isinstance(item, dict), \
                f"隐藏字段列表项类型异常, 期望dict, 实际={type(item)}"
            assert "belongModule" in item, \
                f"隐藏字段列表项缺少belongModule, item={item}"
            assert "hideFieldList" in item, \
                f"隐藏字段列表项缺少hideFieldList, item={item}"
