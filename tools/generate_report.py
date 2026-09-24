"""
自定义接口测试报告生成器
运行 pytest 并生成美观的单文件 HTML 报告
"""
import ast
import glob
import json
import os
import subprocess
import sys
from datetime import datetime


def run_pytest_and_collect(case_path="test_case", json_path="report/.report_data.json"):
    """运行 pytest 并生成 JSON 报告和 Allure 原始数据"""
    allure_dir = "report/.allure-results"
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    os.makedirs(allure_dir, exist_ok=True)
    cmd = [
        sys.executable, "-m", "pytest", case_path,
        f"--json-report", f"--json-report-file={json_path}",
        f"--alluredir={allure_dir}", "--clean-alluredir",
        "-v", "--no-header", "--tb=short",
    ]
    result = subprocess.run(cmd, capture_output=False)
    return json_path, result.returncode


def _parse_allure_results(allure_dir="report/.allure-results"):
    """解析 Allure 结果 JSON，返回 {nodeid: allure_test_data} 映射"""
    mapping = {}
    # 1. 解析 result 文件
    pattern = os.path.join(allure_dir, "*-result.json")
    for fpath in glob.glob(pattern):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            full_name = data.get("fullName", "")
            if full_name:
                parts = full_name.rsplit("#", 1)
                if len(parts) == 2:
                    module_class, method = parts
                    dot_parts = module_class.rsplit(".", 1)
                    if len(dot_parts) == 2:
                        module_path, class_name = dot_parts
                        file_path = module_path.replace(".", "/") + ".py"
                        nodeid = f"{file_path}::{class_name}::{method}"
                        mapping[nodeid] = data
                        data["_nodeid"] = nodeid
        except Exception:
            pass
    # 2. 解析 container 文件，提取 fixture 前置步骤
    container_pattern = os.path.join(allure_dir, "*-container.json")
    for fpath in glob.glob(container_pattern):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                cdata = json.load(f)
            children = cdata.get("children", [])
            befores = cdata.get("befores", [])
            if not befores or not children:
                continue
            # 通过 children UUID 关联到 test result
            for child_uuid in children:
                for nodeid, rdata in mapping.items():
                    if rdata.get("uuid") == child_uuid:
                        rdata["befores"] = befores
                        break
        except Exception:
            pass
    return mapping


def load_report_data(json_path):
    """加载 pytest JSON 报告数据"""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _status_class(status):
    return {
        "passed": "pass",
        "failed": "fail",
        "skipped": "skip",
        "error": "fail",
    }.get(status, "")


def _status_text(status):
    return {"passed": "通过", "failed": "失败", "skipped": "跳过", "error": "错误"}.get(status, status)


def _format_duration(seconds):
    if seconds < 1:
        return f"{seconds*1000:.0f} ms"
    return f"{seconds:.2f} s"


def _extract_test_id(nodeid):
    """从 pytest nodeid 提取可读用例名"""
    # e.g. test_case/test_ydl_case/test_xxx.py::TestClass::test_method -> test_method
    parts = nodeid.split("::")
    return parts[-1] if parts else nodeid


def _extract_module(nodeid):
    """从 pytest nodeid 提取模块路径"""
    parts = nodeid.split("::")
    return parts[0].replace("test_case/", "").replace(".py", "") if parts else ""


def _build_docstring_map(case_dir="test_case"):
    """扫描测试文件，用 AST 构建 {函数名: docstring} 映射"""
    mapping = {}
    for root, dirs, files in os.walk(case_dir):
        for fn in files:
            if fn.startswith("test_") and fn.endswith(".py"):
                fpath = os.path.join(root, fn)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=fpath)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                            doc = ast.get_docstring(node)
                            if doc:
                                # 取 docstring 第一行（去掉多余空白）
                                mapping[node.name] = doc.split("\n")[0].strip()
                except Exception:
                    pass
    return mapping


def _parse_api_steps(stdout):
    """从 pytest stdout 解析接口调用步骤列表"""
    if not stdout:
        return []
    steps = []
    blocks = stdout.split("--[接口异常信息开始]--")
    for block in blocks[1:]:  # 跳过第一段（标记前的内容）
        end = block.split("--[接口异常信息结束]--")
        content = end[0] if end else block
        step = {}
        for line in content.split(";"):
            line = line.strip()
            if line.startswith("--url:"):
                step["url"] = line[6:].strip().rstrip(";")
            elif line.startswith("--body:"):
                step["body"] = line[7:].strip()
            elif line.startswith("--response:"):
                step["response"] = line[11:].strip()
            elif line.startswith("接口响应时间:"):
                step["time"] = line.replace("接口响应时间:", "").strip()
        if step.get("url"):
            # 提取接口名（最后一段路径）
            url = step["url"]
            path = url.split("?")[0]
            step["api"] = path.rsplit("/", 1)[-1] if "/" in path else path
            steps.append(step)
    return steps


def _build_befores_html(befores, idx):
    """构建前置 fixture 区域的 HTML"""
    if not befores:
        return ""
    sections = []
    for fi, fixture in enumerate(befores):
        f_name = fixture.get("name", "")
        f_status = fixture.get("status", "")
        f_steps = fixture.get("steps", [])
        if not f_name:
            continue
        # 渲染 fixture 内部的步骤（可展开查看参数）
        step_items = []
        for si, s in enumerate(f_steps):
            s_name = s.get("name", "")
            s_params = s.get("parameters", [])
            sid = f"before-{idx}-{fi}-{si}"
            # 参数展示（放在可展开区域内）
            detail_html = ""
            for p in s_params:
                p_name = p.get("name", "")
                p_val = str(p.get("value", ""))
                if len(p_val) > 120:
                    p_val = p_val[:120] + "..."
                p_val_esc = p_val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                detail_html += f'<div class="allure-param"><span class="allure-pk">{p_name}:</span><span class="allure-pv">{p_val_esc}</span></div>'
            has_detail = bool(detail_html)
            onclick = f'onclick="toggleAllureStep(\'{sid}\')"' if has_detail else ''
            body_html = f'<div class="allure-step-body" id="body-{sid}" style="display:none">{detail_html}</div>' if has_detail else ''
            step_items.append(f'''
              <div class="allure-step">
                <div class="allure-step-header" {onclick}>
                  <span class="allure-arrow" id="arrow-{sid}">›</span>
                  <span class="allure-step-name">{s_name}</span>
                </div>
                {body_html}
              </div>''')
        steps_inner = "\n".join(step_items)
        section_id = f"before-{idx}-{fi}"
        sections.append(f'''
            <div class="dp-section">
              <div class="dp-section-title dp-collapsible" onclick="toggleSection('{section_id}')">
                <span class="dp-sec-arrow" id="sec-arrow-{section_id}">›</span>
                前置 {f_name}
              </div>
              <div class="dp-section-body" id="{section_id}">
                {steps_inner}
              </div>
            </div>''')
    return "\n".join(sections)


def _flatten_allure_steps(steps):
    """将 Allure 嵌套步骤展平为列表，提取每层步骤名称和参数"""
    result = []
    for s in steps:
        name = s.get("name", "")
        params = s.get("parameters", [])
        result.append({"name": name, "params": params})
        # 递归展开子步骤
        for sub in s.get("steps", []):
            sub_name = sub.get("name", "")
            sub_params = sub.get("parameters", [])
            result.append({"name": sub_name, "params": sub_params})
    return result


def _build_steps_html(api_steps, allure_steps, idx):
    """构建 Allure 风格的可折叠步骤组，优先使用 Allure 中文步骤名称"""
    if not api_steps and not allure_steps:
        return '<div class="no-steps">无接口调用记录</div>'

    # 构建 Allure 步骤列表（仅用顶层步骤作为显示名称）
    allure_top = []
    for s in (allure_steps or []):
        name = s.get("name", "")
        params = s.get("parameters", [])
        # 从子步骤提取 URL、method、status_code 用于匹配和展示
        sub_urls = []
        sub_method = ""
        sub_path = ""
        sub_status_code = ""
        for sub in s.get("steps", []):
            for p in sub.get("parameters", []):
                pn = p.get("name", "")
                pv = str(p.get("value", "")).strip("'\"")
                if pn == "path_or_url":
                    sub_urls.append(pv)
                    sub_path = pv
                elif pn == "method":
                    sub_method = pv
                elif pn == "status_code":
                    sub_status_code = pv
        allure_top.append({"name": name, "params": params, "urls": sub_urls,
                           "method": sub_method, "path": sub_path,
                           "status_code": sub_status_code})

    # 匹配策略：每个 API 步骤对应一个 Allure 顶层步骤（通过 URL 匹配）
    merged = []
    used_allure = set()
    step_status_code = ""  # 初始化状态码变量

    for i, api_s in enumerate(api_steps):
        api_name = api_s.get("api", "")  # e.g. getOrgListNoAuth.do
        url = api_s.get("url", "")
        body = api_s.get("body", "")
        resp = api_s.get("response", "")
        time_val = api_s.get("time", "")

        # 尝试在 Allure 顶层步骤中找到匹配项
        step_name = api_name  # 默认用 API 名
        step_params = []
        step_method = ""
        step_path = ""
        for j, a_s in enumerate(allure_top):
            if j in used_allure:
                continue
            # 通过子步骤的 URL 匹配
            matched = False
            for sub_url in a_s["urls"]:
                if api_name in sub_url or sub_url in url:
                    matched = True
                    break
            if not matched:
                # 通过参数字符串匹配
                param_str = str(a_s["params"])
                if api_name in param_str or url in param_str:
                    matched = True
            if matched:
                step_name = a_s["name"]
                step_params = a_s["params"]
                step_method = a_s.get("method", "")
                step_path = a_s.get("path", "")
                step_status_code = a_s.get("status_code", "")
                used_allure.add(j)
                break

        merged.append({
            "name": step_name,
            "api": api_name,
            "url": url,
            "body": body,
            "resp": resp,
            "time": time_val,
            "params": step_params,
            "method": step_method,
            "path": step_path,
            "status_code": step_status_code,
        })

    # 添加未匹配的 Allure 顶层步骤（前置步骤等）
    for j, a_s in enumerate(allure_top):
        if j not in used_allure:
            # 插入到第一个未匹配的 API 步骤之前
            inserted = False
            for mi, m in enumerate(merged):
                if m["name"] == m["api"]:  # 未匹配的 API 步骤
                    merged.insert(mi, {
                        "name": a_s["name"],
                        "api": "",
                        "url": "",
                        "body": "",
                        "resp": "",
                        "time": "",
                        "params": a_s["params"],
                    })
                    inserted = True
                    break
            if not inserted:
                merged.append({
                    "name": a_s["name"],
                    "api": "",
                    "url": "",
                    "body": "",
                    "resp": "",
                    "time": "",
                    "params": a_s["params"],
                })

    items = []
    for i, s in enumerate(merged, 1):
        step_name = s["name"]
        url = s["url"]
        body = s["body"]
        resp = s["resp"]
        time_val = s["time"]
        params = s["params"]

        # 格式化请求/响应
        body_fmt, resp_fmt = body, resp
        for key, val in [("body", body), ("response", resp)]:
            try:
                parsed = json.loads(val)
                formatted = json.dumps(parsed, ensure_ascii=False, indent=2)
                if key == "body":
                    body_fmt = formatted
                else:
                    resp_fmt = formatted
            except Exception:
                pass
        if len(body_fmt) > 500:
            body_fmt = body_fmt[:500] + "\n..."
        if len(resp_fmt) > 800:
            resp_fmt = resp_fmt[:800] + "\n..."
        body_esc = body_fmt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        resp_esc = resp_fmt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        time_ms = ""
        if time_val:
            try:
                sec = float(time_val.replace("秒", ""))
                time_ms = f"{int(sec*1000)}ms" if sec < 1 else f"{sec:.1f}s"
            except Exception:
                time_ms = time_val

        sid = f"step-{idx}-{i}"

        # 构建详情区（method + status_code 在 URL 上方）
        detail_html = ""
        req_method = s.get("method", "")
        req_status_code = s.get("status_code", "")
        if req_method:
            detail_html += f'<div class="allure-kv"><span class="allure-k">method</span><span class="allure-v">{req_method}</span></div>'
        if req_status_code:
            detail_html += f'<div class="allure-kv"><span class="allure-k">status_code</span><span class="allure-v">{req_status_code}</span></div>'
        if url:
            detail_html += f'<div class="allure-kv"><span class="allure-k">url</span><span class="allure-v">{url}</span></div>'
        if body:
            detail_html += f'<div class="allure-kv"><span class="allure-k">请求体</span><pre class="allure-pre">{body_esc}</pre></div>'
        if resp:
            detail_html += f'<div class="allure-kv"><span class="allure-k">响应</span><pre class="allure-pre">{resp_esc}</pre></div>'

        has_detail = bool(detail_html)
        onclick = f"onclick=\"toggleAllureStep('{sid}')\"" if has_detail else ""

        items.append(f'''
          <div class="allure-step">
            <div class="allure-step-header" {onclick}>
              <span class="allure-arrow" id="arrow-{sid}">›</span>
              <span class="allure-step-name">{step_name}</span>
              <span class="allure-step-time">{time_ms}</span>
            </div>
            {"<div class='allure-step-body' id='body-" + sid + "' style='display:none'>" + detail_html + "</div>" if has_detail else ""}
          </div>''')
    return "\n".join(items)


def generate_html(data, output_path="report/接口测试报告.html", allure_map=None):
    """生成 Allure 风格的 HTML 报告（左右分栏布局）"""
    summary = data.get("summary", {})
    tests = data.get("tests", [])
    created = data.get("created", datetime.now().isoformat())
    duration = data.get("duration", 0)

    total = summary.get("total", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    skipped = summary.get("skipped", 0)
    error = summary.get("error", 0)
    pass_rate = (passed / total * 100) if total > 0 else 0

    # 按模块分组
    modules = {}
    for t in tests:
        mod = _extract_module(t.get("nodeid", ""))
        modules.setdefault(mod, []).append(t)

    # 构建中文名称映射
    docstring_map = _build_docstring_map("test_case")

    # 生成时间
    try:
        gen_time = datetime.fromisoformat(created.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        gen_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 构建左侧边栏 + 右侧详情
    sidebar_items = []
    detail_panels = []
    idx = 0
    for mod_name, mod_tests in modules.items():
        mod_label = mod_name.split("/")[-1] if "/" in mod_name else mod_name
        mod_pass = sum(1 for t in mod_tests if t.get("outcome") == "passed")
        mod_fail = sum(1 for t in mod_tests if t.get("outcome") == "failed")
        mod_skip = sum(1 for t in mod_tests if t.get("outcome") == "skipped")
        sidebar_items.append(f'''
        <div class="mod-group">
          <div class="mod-header" onclick="toggleMod(this)">
            <span class="mod-arrow">▶</span>
            <span class="mod-label">{mod_label}</span>
            <span class="mod-count">
              <span class="mc-pass">{mod_pass}</span>
              {"<span class='mc-fail'>" + str(mod_fail) + "</span>" if mod_fail else ""}
              {"<span class='mc-skip'>" + str(mod_skip) + "</span>" if mod_skip else ""}
            </span>
          </div>
          <div class="mod-body">''')
        for t in mod_tests:
            idx += 1
            outcome = t.get("outcome", "unknown")
            func_name = _extract_test_id(t.get("nodeid", ""))
            cn_name = docstring_map.get(func_name, func_name)
            dur = _format_duration(t.get("call", {}).get("duration", 0) or 0)
            status_cls = _status_class(outcome)
            status_txt = _status_text(outcome)
            status_icon = {"pass": "✅", "fail": "❌", "skip": "⏭️"}.get(status_cls, "⚪")
            # 解析步骤
            stdout = t.get("call", {}).get("stdout", "") or ""
            api_steps = _parse_api_steps(stdout)
            # 查找 Allure 步骤
            nodeid = t.get("nodeid", "")
            allure_data = (allure_map or {}).get(nodeid, {})
            allure_steps = allure_data.get("steps", []) if allure_data else []
            allure_befores = allure_data.get("befores", []) if allure_data else []
            steps_html = _build_steps_html(api_steps, allure_steps, idx)
            befores_html = _build_befores_html(allure_befores, idx)
            # 失败原因
            fail_reason = ""
            if outcome == "failed" and t.get("call", {}).get("longrepr"):
                fr = t["call"]["longrepr"]
                fail_reason = fr[:300] + "..." if len(fr) > 300 else fr
            fail_esc = fail_reason.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            # 左侧边栏项
            sidebar_items.append(f'''
            <div class="sidebar-item {status_cls} {'active' if idx == 1 else ''}" data-idx="{idx}" onclick="selectTest({idx})">
              <span class="si-icon">{status_icon}</span>
              <span class="si-name">{cn_name}</span>
              <span class="si-dur">{dur}</span>
            </div>''')
            # 右侧详情面板
            desc_text = cn_name if cn_name != func_name else ""
            dur_ms = dur  # 已经是格式化后的
            detail_panels.append(f'''
        <div class="detail-panel" id="panel-{idx}" {'style="display:block"' if idx == 1 else 'style="display:none"'}>
          <div class="dp-header">
            <h2 class="dp-title">{cn_name}</h2>
            <span class="dp-status {status_cls}">{status_txt}</span>
          </div>
          <div class="dp-tabs">
            <span class="dp-tab active" onclick="switchTab(this,'overview-{idx}')">总览</span>
            <span class="dp-tab" onclick="switchTab(this,'history-{idx}')">历史</span>
            <span class="dp-tab" onclick="switchTab(this,'retry-{idx}')">重试次数</span>
          </div>
          <div class="dp-tab-content" id="overview-{idx}">
          <div class="dp-body">
            <div class="dp-info">
              <div class="dp-info-row"><span class="dp-info-k">Priority</span><span class="dp-info-v">normal</span></div>
              <div class="dp-info-row"><span class="dp-info-k">Duration</span><span class="dp-info-v">{dur_ms}</span></div>
              {"<div class='dp-info-row'><span class='dp-info-k'>函数</span><span class='dp-info-v dp-func'>" + func_name + "</span></div>" if desc_text else ""}
            </div>
            {"<div class='dp-section'><div class='dp-section-title'>描述</div><p class='dp-desc-text'>" + desc_text + "</p></div>" if desc_text else ""}
            {"<div class='dp-section dp-fail-section'><div class='dp-section-title'>❌ 失败原因</div><pre class='dp-fail-pre'>" + fail_esc + "</pre></div>" if fail_reason else ""}
            {befores_html}
            <div class="dp-section">
              <div class="dp-section-title dp-collapsible" onclick="toggleSection('exec-{idx}')">
                <span class="dp-sec-arrow" id="sec-arrow-exec-{idx}">›</span>
                执行
              </div>
              <div class="dp-section-body" id="exec-{idx}">
                {steps_html}
              </div>
            </div>
          </div>
          </div>
          <div class="dp-tab-content" id="history-{idx}" style="display:none">
            <div class="dp-empty">暂无历史执行记录</div>
          </div>
          <div class="dp-tab-content" id="retry-{idx}" style="display:none">
            <div class="dp-empty">暂无重试记录</div>
          </div>
        </div>''')
        sidebar_items.append('</div></div>')

    sidebar_html = "\n".join(sidebar_items)
    panels_html = "\n".join(detail_panels)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>接口自动化测试报告</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
      background: #f0f2f5; color: #333; line-height: 1.6;
    }}
    /* 头部 */
    .header {{
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 24px 32px; color: #fff; position: relative; overflow: hidden;
    }}
    .header::before {{
      content: ""; position: absolute; top: -60%; right: -10%;
      width: 400px; height: 400px;
      background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
      border-radius: 50%;
    }}
    .header-inner {{ position: relative; z-index: 1; display: flex; align-items: center; justify-content: space-between; max-width: 1400px; margin: 0 auto; }}
    .header h1 {{ font-size: 22px; font-weight: 700; }}
    .header .meta {{ font-size: 13px; opacity: 0.85; margin-top: 4px; }}
    .header .meta span {{ margin-right: 16px; }}
    /* 统计栏 */
    .stats-bar {{
      display: flex; gap: 0; max-width: 1400px; margin: 0 auto;
      background: #fff; border-bottom: 1px solid #e8e8e8;
    }}
    .sb-item {{
      flex: 1; padding: 16px 20px; text-align: center;
      border-right: 1px solid #f0f0f0; transition: background 0.2s;
    }}
    .sb-item:last-child {{ border-right: none; }}
    .sb-item:hover {{ background: #fafafa; }}
    .sb-label {{ font-size: 12px; color: #999; text-transform: uppercase; letter-spacing: 1px; }}
    .sb-val {{ font-size: 28px; font-weight: 800; margin-top: 2px; }}
    .sb-val.total {{ color: #667eea; }}
    .sb-val.pass {{ color: #52c41a; }}
    .sb-val.fail {{ color: #ff4d4f; }}
    .sb-val.skip {{ color: #faad14; }}
    .sb-val.rate {{ color: #52c41a; font-size: 24px; }}
    /* 主体布局 */
    .main {{ display: flex; max-width: 1400px; margin: 0 auto; min-height: calc(100vh - 200px); }}
    /* 左侧边栏 */
    .sidebar {{
      width: 360px; min-width: 360px; background: #fff;
      border-right: 1px solid #e8e8e8; overflow-y: auto;
      max-height: calc(100vh - 160px); position: sticky; top: 0;
    }}
    .mod-group {{ border-bottom: 1px solid #f0f0f0; }}
    .mod-header {{
      display: flex; align-items: center; gap: 8px;
      padding: 12px 16px; cursor: pointer; font-weight: 600; font-size: 14px;
      background: #fafafa; transition: background 0.2s;
    }}
    .mod-header:hover {{ background: #f0f0f0; }}
    .mod-arrow {{ font-size: 10px; color: #999; transition: transform 0.2s; }}
    .mod-arrow.open {{ transform: rotate(90deg); }}
    .mod-label {{ flex: 1; }}
    .mod-count {{ display: flex; gap: 4px; }}
    .mc-pass, .mc-fail, .mc-skip {{
      font-size: 11px; padding: 1px 8px; border-radius: 8px; font-weight: 600;
    }}
    .mc-pass {{ background: #f6ffed; color: #52c41a; }}
    .mc-fail {{ background: #fff2f0; color: #ff4d4f; }}
    .mc-skip {{ background: #fffbe6; color: #faad14; }}
    .mod-body {{ }}
    .sidebar-item {{
      display: flex; align-items: flex-start; gap: 8px;
      padding: 10px 16px 10px 32px; cursor: pointer;
      border-bottom: 1px solid #f8f8f8; transition: all 0.15s;
    }}
    .sidebar-item:hover {{ background: #f5f3ff; }}
    .sidebar-item.active {{ background: #ede9fe; border-left: 3px solid #667eea; padding-left: 29px; }}
    .si-icon {{ flex-shrink: 0; font-size: 14px; margin-top: 2px; }}
    .si-name {{
      flex: 1; font-size: 13px; color: #333; line-height: 1.5;
      display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
    }}
    .si-dur {{ flex-shrink: 0; font-size: 11px; color: #bbb; white-space: nowrap; margin-top: 2px; }}
    /* 右侧详情 */
    .detail {{
      flex: 1; background: #f8f9fa; overflow-y: auto;
      max-height: calc(100vh - 160px); padding: 0;
    }}
    .detail-panel {{ display: none; }}
    .dp-header {{
      display: flex; justify-content: space-between; align-items: center;
      padding: 20px 24px 0; background: #fff;
    }}
    .dp-title {{
      font-size: 18px; font-weight: 700; color: #222; margin: 0;
    }}
    .dp-status {{
      display: inline-block; padding: 4px 14px; border-radius: 12px;
      font-size: 13px; font-weight: 600;
    }}
    .dp-status.pass {{ background: #f6ffed; color: #52c41a; }}
    .dp-status.fail {{ background: #fff2f0; color: #ff4d4f; }}
    .dp-status.skip {{ background: #fffbe6; color: #faad14; }}
    .dp-tabs {{
      display: flex; gap: 0; border-bottom: 1px solid #e8e8e8;
      padding: 12px 24px 0; background: #fff;
    }}
    .dp-tab {{
      padding: 8px 16px; font-size: 13px; color: #999; cursor: pointer;
      border-bottom: 2px solid transparent; transition: all 0.2s;
    }}
    .dp-tab.active {{ color: #667eea; border-bottom-color: #667eea; font-weight: 600; }}
    .dp-tab:hover {{ color: #555; cursor: pointer; }}
    .dp-tab-content {{ }}
    .dp-empty {{
      padding: 40px 24px; text-align: center; color: #bbb;
      font-size: 14px; font-style: italic;
    }}
    .dp-body {{ padding: 0; background: #fff; }}
    .dp-info {{
      padding: 16px 24px; border-bottom: 1px solid #f0f0f0;
    }}
    .dp-info-row {{
      display: flex; align-items: center; gap: 12px;
      padding: 4px 0; font-size: 13px;
    }}
    .dp-info-k {{ color: #999; min-width: 70px; }}
    .dp-info-v {{ color: #333; }}
    .dp-func {{ font-family: "SF Mono", Consolas, monospace; font-size: 12px; color: #666; }}
    .dp-section {{
      border-bottom: 1px solid #f0f0f0; padding: 16px 24px;
    }}
    .dp-section-title {{
      font-size: 14px; font-weight: 600; color: #333; margin-bottom: 10px;
    }}
    .dp-collapsible {{
      cursor: pointer; display: flex; align-items: center; gap: 6px;
      user-select: none; padding: 8px 4px; border-radius: 4px;
    }}
    .dp-collapsible:hover {{ color: #667eea; background: #f5f3ff; }}
    .dp-sec-arrow {{
      font-size: 14px; color: #667eea; transition: transform 0.2s;
      display: inline-flex; align-items: center; justify-content: center;
      width: 20px; height: 20px; border-radius: 4px;
    }}
    .dp-sec-arrow.open {{ transform: rotate(90deg); }}
    .dp-section-body {{ padding-top: 8px; }}
    .dp-desc-text {{ font-size: 13px; color: #444; line-height: 1.6; }}
    .dp-fail-section {{ background: #fff8f8; }}
    .dp-fail-pre {{
      background: #fff1f0; color: #cf1322; padding: 12px;
      border-radius: 8px; font-size: 12px; white-space: pre-wrap;
      word-break: break-all; border: 1px solid #ffa39e;
    }}
    .no-steps {{ color: #ccc; font-size: 13px; font-style: italic; padding: 8px 0; }}
    /* Allure 风格步骤 */
    .allure-step {{
      border-bottom: 1px solid #f5f5f5;
    }}
    .allure-step:last-child {{ border-bottom: none; }}
    .allure-step-header {{
      display: flex; align-items: center; gap: 8px;
      padding: 10px 8px; cursor: pointer; font-size: 13px;
      transition: background 0.15s;
    }}
    .allure-step-header:hover {{ background: #fafafa; }}
    .allure-arrow {{
      color: #667eea; font-size: 16px; font-weight: 600;
      width: 20px; height: 20px; text-align: center; flex-shrink: 0;
      transition: transform 0.2s; display: inline-flex;
      align-items: center; justify-content: center; border-radius: 4px;
    }}
    .allure-arrow.open {{ transform: rotate(90deg); }}
    .allure-step-name {{
      flex: 1; color: #333; font-weight: 500;
      font-family: "SF Mono", Consolas, "Microsoft YaHei", monospace;
    }}
    .allure-step-time {{
      color: #999; font-size: 12px; white-space: nowrap;
      font-family: "SF Mono", Consolas, monospace;
    }}
    .allure-step-body {{
      padding: 8px 12px 12px 28px; border-left: 2px solid #e8e8e8;
      margin-left: 12px; margin-bottom: 4px;
    }}
    .allure-kv {{ margin-bottom: 8px; }}
    .allure-kv:last-child {{ margin-bottom: 0; }}
    .allure-k {{
      display: inline-block; background: #f0f0f0; color: #555;
      font-size: 11px; font-weight: 600; padding: 2px 8px;
      border-radius: 4px; margin-bottom: 4px;
    }}
    .allure-v {{
      display: block; font-size: 12px; color: #444;
      word-break: break-all; font-family: "SF Mono", Consolas, monospace;
      background: #f8f8f8; padding: 6px 10px; border-radius: 6px;
    }}
    .allure-pre {{
      background: #f8f8f8; padding: 8px 10px; border-radius: 6px;
      font-size: 11px; color: #444; white-space: pre-wrap;
      word-break: break-all; max-height: 200px; overflow-y: auto; margin: 0;
    }}
    .allure-param {{
      padding: 2px 28px 2px 36px; font-size: 12px;
      display: flex; gap: 4px; color: #666;
    }}
    .allure-pk {{
      color: #999; white-space: nowrap;
    }}
    .allure-pv {{
      color: #555; font-family: "SF Mono", Consolas, monospace;
      word-break: break-all;
    }}
    .footer {{
      text-align: center; padding: 20px; color: #bbb; font-size: 12px;
      max-width: 1400px; margin: 0 auto;
    }}
    @media (max-width: 900px) {{
      .main {{ flex-direction: column; }}
      .sidebar {{ width: 100%; min-width: 100%; max-height: 300px; }}
      .detail {{ max-height: none; }}
    }}
  </style>
</head>
<body>
  <div class="header">
    <div class="header-inner">
      <div>
        <h1>📋 接口自动化测试报告</h1>
        <div class="meta">
          <span>📅 {gen_time}</span>
          <span>⏱️ 总耗时 {_format_duration(duration)}</span>
        </div>
      </div>
    </div>
  </div>

  <div class="stats-bar">
    <div class="sb-item"><div class="sb-label">总计</div><div class="sb-val total">{total}</div></div>
    <div class="sb-item"><div class="sb-label">通过</div><div class="sb-val pass">{passed}</div></div>
    <div class="sb-item"><div class="sb-label">失败</div><div class="sb-val fail">{failed + error}</div></div>
    <div class="sb-item"><div class="sb-label">跳过</div><div class="sb-val skip">{skipped}</div></div>
    <div class="sb-item"><div class="sb-label">通过率</div><div class="sb-val rate">{pass_rate:.1f}%</div></div>
  </div>

  <div class="main">
    <div class="sidebar">
      {sidebar_html}
    </div>
    <div class="detail">
      {panels_html}
    </div>
  </div>

  <div class="footer">接口自动化测试报告 · pytest + generate_report.py</div>

  <script>
    function selectTest(idx) {{
      document.querySelectorAll('.sidebar-item').forEach(el => el.classList.remove('active'));
      document.querySelector('.sidebar-item[data-idx="' + idx + '"]').classList.add('active');
      document.querySelectorAll('.detail-panel').forEach(el => el.style.display = 'none');
      var panel = document.getElementById('panel-' + idx);
      if (panel) panel.style.display = 'block';
    }}
    function toggleMod(el) {{
      var body = el.nextElementSibling;
      var arrow = el.querySelector('.mod-arrow');
      if (body.style.display === 'none') {{
        body.style.display = '';
        arrow.classList.add('open');
      }} else {{
        body.style.display = 'none';
        arrow.classList.remove('open');
      }}
    }}
    function toggleAllureStep(sid) {{
      var body = document.getElementById('body-' + sid);
      var arrow = document.getElementById('arrow-' + sid);
      if (!body) return;
      if (body.style.display === 'none') {{
        body.style.display = 'block';
        if (arrow) arrow.classList.add('open');
      }} else {{
        body.style.display = 'none';
        if (arrow) arrow.classList.remove('open');
      }}
    }}
    function toggleSection(sid) {{
      var body = document.getElementById(sid);
      var arrow = document.getElementById('sec-arrow-' + sid);
      if (!body) return;
      if (body.style.display === 'none') {{
        body.style.display = 'block';
        if (arrow) arrow.classList.add('open');
      }} else {{
        body.style.display = 'none';
        if (arrow) arrow.classList.remove('open');
      }}
    }}
    function switchTab(el, contentId) {{
      var panel = el.closest('.detail-panel');
      if (!panel) return;
      panel.querySelectorAll('.dp-tab').forEach(t => t.classList.remove('active'));
      el.classList.add('active');
      panel.querySelectorAll('.dp-tab-content').forEach(c => c.style.display = 'none');
      var target = document.getElementById(contentId);
      if (target) target.style.display = 'block';
    }}
  </script>
</body>
</html>'''

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def main():
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    case_path = sys.argv[1] if len(sys.argv) > 1 else "test_case"
    output = sys.argv[2] if len(sys.argv) > 2 else "report/接口测试报告.html"
    json_path = "report/.report_data.json"

    print("=" * 50)
    print("  接口自动化测试报告生成器")
    print("=" * 50)
    print(f"\n用例目录: {case_path}")
    print(f"输出文件: {output}\n")

    # 运行 pytest 收集结果
    run_pytest_and_collect(case_path, json_path)

    if not os.path.exists(json_path):
        print("❌ 未生成测试结果文件，请检查 pytest 配置")
        sys.exit(1)

    # 解析 Allure 原始数据
    allure_map = _parse_allure_results()
    print(f"📊 解析到 {len(allure_map)} 个 Allure 结果文件")

    # 生成 HTML
    data = load_report_data(json_path)
    path = generate_html(data, output, allure_map=allure_map)
    size_kb = os.path.getsize(path) / 1024
    print(f"\n✅ 报告已生成: {path} ({size_kb:.1f} KB)")
    print(f"   双击即可在浏览器中打开查看")


if __name__ == "__main__":
    main()
