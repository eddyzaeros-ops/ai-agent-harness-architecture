#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
將對話記錄匯出至 docx 文件
對話名稱：AI Service Chain Summary Report
輸出路徑：D:\JavaDO\對話紀錄\AI Service Chain Summary Report.docx
"""

import json
import os
import sys
import re
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# 1. 確保輸出目錄存在
output_dir = r"D:\JavaDO\對話紀錄"
os.makedirs(output_dir, exist_ok=True)
doc_name = "AI Service Chain Summary Report.docx"
output_path = os.path.join(output_dir, doc_name)

# 2. 讀取 transcript_full.jsonl
transcript_path = r"C:\Users\calsa\.gemini\antigravity\brain\4be13bbb-2ae7-4c18-938f-a204665099e4\.system_generated\logs\transcript_full.jsonl"
if not os.path.exists(transcript_path):
    transcript_path = r"C:\Users\calsa\.gemini\antigravity\brain\4be13bbb-2ae7-4c18-938f-a204665099e4\.system_generated\logs\transcript.jsonl"

turns = []
current_user = None
current_assistant_texts = []

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        stype = data.get("type")
        
        if stype == "USER_INPUT":
            if current_user is not None:
                turns.append({
                    "user": current_user,
                    "assistant": "\n\n".join(current_assistant_texts).strip()
                })
            current_user = {
                "step": data.get("step_index"),
                "time": data.get("created_at"),
                "content": data.get("content", "").strip()
            }
            current_assistant_texts = []
        elif stype == "PLANNER_RESPONSE":
            content = data.get("content", "").strip()
            if content:
                current_assistant_texts.append(content)

if current_user is not None:
    turns.append({
        "user": current_user,
        "assistant": "\n\n".join(current_assistant_texts).strip()
    })

print(f"成功解析對話輪次：{len(turns)} 輪")

# 3. 初始化 Word 文件
doc = Document()

# 頁面邊界設定 (標準 A4, 2.2 cm 邊距)
for section in doc.sections:
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)

# 字型設定
style_normal = doc.styles['Normal']
style_normal.font.name = '微軟正黑體'
style_normal.font.size = Pt(10.5)
style_normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
style_normal.element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')

# 色彩定義
COLOR_NAVY   = RGBColor(0x0A, 0x0F, 0x1E)
COLOR_CYAN   = RGBColor(0x00, 0x83, 0x8F)
COLOR_BLUE   = RGBColor(0x15, 0x65, 0xC0)
COLOR_USER   = RGBColor(0x2E, 0x7D, 0x32) # 綠色代表使用者
COLOR_GRAY   = RGBColor(0x55, 0x55, 0x55)
COLOR_LGRAY  = RGBColor(0x88, 0x88, 0x88)
COLOR_RED    = RGBColor(0xC6, 0x28, 0x28)

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_styled_paragraph(doc, text, bold=False, size=10.5, color=None, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4, line_spacing=1.3):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    run = p.add_run(text)
    run.font.name = '微軟正黑體'
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = color
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
    return p

# ─── 封面與文件標題 ───
add_styled_paragraph(doc, "Antigravity 對話完整紀錄", bold=True, size=24, color=COLOR_NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=20, space_after=6)
add_styled_paragraph(doc, "AI Service Chain Summary Report", bold=True, size=18, color=COLOR_CYAN, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)

# 資訊摘要表格
info_table = doc.add_table(rows=6, cols=2)
info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
info_data = [
    ("對話主題 (Title)", "AI Service Chain Summary Report"),
    ("對話識別碼 (ID)", "4be13bbb-2ae7-4c18-938f-a204665099e4"),
    ("工作目錄 (Workspace)", r"D:\JavaDO"),
    ("對話時段", f"{turns[0]['user']['time'][:10]} ~ {turns[-1]['user']['time'][:10]} (共 21 輪交互)"),
    ("主要成果產出", "1. 總結報告 (v2 / v4補充版 / 最終版 / 科技感版.pptx)\n2. Deep Agents 16章心得報告 (v1 / v2.pptx)\n3. 國防AI服務鏈建置Proposal_草稿版.docx"),
    ("匯出時間", "2026-09-14 (自動匯出紀錄)")
]
for idx, (label, val) in enumerate(info_data):
    row = info_table.rows[idx]
    c0 = row.cells[0]
    c1 = row.cells[1]
    c0.width = Cm(4.5)
    c1.width = Cm(12.0)
    set_cell_shading(c0, "F0F4F8")
    set_cell_margins(c0, 80, 80, 120, 120)
    set_cell_margins(c1, 80, 80, 120, 120)
    
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_after = Pt(2)
    r0 = p0.add_run(label)
    r0.bold = True
    r0.font.name = '微軟正黑體'
    r0.font.size = Pt(9.5)
    r0.font.color.rgb = COLOR_NAVY
    r0._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
    
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_after = Pt(2)
    p1.paragraph_format.line_spacing = 1.2
    r1 = p1.add_run(val)
    r1.font.name = '微軟正黑體'
    r1.font.size = Pt(9.5)
    r1._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# ─── 輔助解析 Markdown 內容到 Word ───
def render_markdown_block(container, md_text):
    """
    將 Markdown 格式的字串逐段解析並寫入 container (doc 或 table cell)
    """
    lines = md_text.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 處理 Code Block
        if stripped.startswith("```"):
            if in_code_block:
                # 結束 code block
                code_text = "\n".join(code_lines)
                table = container.add_table(rows=1, cols=1)
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                cell = table.rows[0].cells[0]
                cell.width = Cm(16.5)
                set_cell_shading(cell, "F5F5F5")
                set_cell_margins(cell, 80, 80, 120, 120)
                cp = cell.paragraphs[0]
                cp.paragraph_format.space_after = Pt(2)
                cp.paragraph_format.line_spacing = 1.15
                cr = cp.add_run(code_text)
                cr.font.name = 'Consolas'
                cr.font.size = Pt(8.5)
                cr.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                cr._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
                container.add_paragraph().paragraph_format.space_after = Pt(2)
                in_code_block = False
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            i += 1
            continue
            
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
            
        # 處理 Markdown 表格 (| col1 | col2 |)
        if stripped.startswith("|") and stripped.endswith("|") and i + 1 < len(lines) and ("---" in lines[i+1] or "|:" in lines[i+1] or ":|" in lines[i+1]):
            # 讀取完整表格
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            
            # 解析 table_lines
            raw_rows = []
            for tl in table_lines:
                cols = [c.strip() for c in tl.strip("|").split("|")]
                raw_rows.append(cols)
            
            if len(raw_rows) >= 2:
                header_cols = raw_rows[0]
                data_rows = [r for r in raw_rows[2:] if any(c for c in r)]
                
                t = container.add_table(rows=1+len(data_rows), cols=len(header_cols))
                t.alignment = WD_TABLE_ALIGNMENT.CENTER
                t.style = 'Table Grid'
                
                # 表頭
                for ci, hc in enumerate(header_cols):
                    cell = t.rows[0].cells[ci]
                    cell.text = hc
                    set_cell_shading(cell, "0A0F1E")
                    set_cell_margins(cell, 60, 60, 100, 100)
                    for p in cell.paragraphs:
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        p.paragraph_format.space_after = Pt(2)
                        for r in p.runs:
                            r.bold = True
                            r.font.size = Pt(9)
                            r.font.name = '微軟正黑體'
                            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                            r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
                
                # 資料行
                for ri, drow in enumerate(data_rows):
                    for ci, val in enumerate(drow):
                        if ci < len(t.rows[ri+1].cells):
                            cell = t.rows[ri+1].cells[ci]
                            cell.text = val
                            set_cell_margins(cell, 50, 50, 80, 80)
                            if ri % 2 == 0:
                                set_cell_shading(cell, "F8F9FA")
                            for p in cell.paragraphs:
                                p.paragraph_format.space_after = Pt(2)
                                p.paragraph_format.line_spacing = 1.15
                                for r in p.runs:
                                    r.font.size = Pt(8.5)
                                    r.font.name = '微軟正黑體'
                                    r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
                
                container.add_paragraph().paragraph_format.space_after = Pt(3)
            continue

        # 處理標題 (#, ##, ###, ####)
        header_match = re.match(r'^(#{1,4})\s+(.*)$', stripped)
        if header_match:
            level = len(header_match.group(1))
            htext = header_match.group(2).strip()
            # 依 level 決定樣式
            if level == 1:
                p = container.add_paragraph()
                p.paragraph_format.space_before = Pt(10)
                p.paragraph_format.space_after = Pt(4)
                r = p.add_run(htext)
                r.bold = True
                r.font.size = Pt(13)
                r.font.color.rgb = COLOR_NAVY
                r.font.name = '微軟正黑體'
                r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
            elif level == 2:
                p = container.add_paragraph()
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(3)
                r = p.add_run(htext)
                r.bold = True
                r.font.size = Pt(11.5)
                r.font.color.rgb = COLOR_BLUE
                r.font.name = '微軟正黑體'
                r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
            else:
                p = container.add_paragraph()
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(2)
                r = p.add_run(htext)
                r.bold = True
                r.font.size = Pt(10.5)
                r.font.color.rgb = COLOR_CYAN
                r.font.name = '微軟正黑體'
                r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
            i += 1
            continue

        # 處理引用塊 (> text)
        if stripped.startswith(">"):
            quote_text = stripped.lstrip("> ").strip()
            p = container.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.8)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.2
            r = p.add_run("▌ " + quote_text)
            r.font.name = '微軟正黑體'
            r.font.size = Pt(9.5)
            r.font.color.rgb = COLOR_GRAY
            r.italic = True
            r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
            i += 1
            continue

        # 處理水平分隔線 (--- or ***)
        if re.match(r'^[-\*_]{3,}$', stripped):
            p = container.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run("―" * 50)
            r.font.size = Pt(6)
            r.font.color.rgb = RGBColor(0xDD, 0xDD, 0xDD)
            i += 1
            continue

        # 處理清單 (- , * , 1. )
        bullet_match = re.match(r'^([-*]|\d+\.)\s+(.*)$', stripped)
        if bullet_match:
            b_symbol = bullet_match.group(1)
            b_text = bullet_match.group(2).strip()
            
            p = container.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.25
            
            # 清單符號
            if b_symbol in ["-", "*"]:
                sym_run = p.add_run("• ")
                sym_run.bold = True
                sym_run.font.color.rgb = COLOR_CYAN
            else:
                sym_run = p.add_run(b_symbol + " ")
                sym_run.bold = True
                sym_run.font.color.rgb = COLOR_BLUE
            sym_run.font.name = '微軟正黑體'
            sym_run.font.size = Pt(9.5)
            sym_run._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
            
            # 渲染行內格式
            render_inline_formatting(p, b_text, size=9.5)
            i += 1
            continue

        # 普通段落
        if stripped:
            p = container.add_paragraph()
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.3
            render_inline_formatting(p, stripped, size=10)
            
        i += 1

def render_inline_formatting(paragraph, text, size=10):
    """
    處理粗體 **text**、行內程式碼 `code`、超連結 [link](url)
    """
    # 簡化分解 regex
    tokens = re.split(r'(\*\*.*?\*\*|`.*?`|\[.*?\]\(.*?\))', text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) >= 4:
            clean = tok[2:-2]
            r = paragraph.add_run(clean)
            r.bold = True
            r.font.name = '微軟正黑體'
            r.font.size = Pt(size)
            r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
        elif tok.startswith("`") and tok.endswith("`") and len(tok) >= 2:
            clean = tok[1:-1]
            r = paragraph.add_run(clean)
            r.font.name = 'Consolas'
            r.font.size = Pt(size * 0.92)
            r.font.color.rgb = RGBColor(0xA3, 0x15, 0x15)
            r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
        elif tok.startswith("[") and "](" in tok and tok.endswith(")"):
            m = re.match(r'\[(.*?)\]\((.*?)\)', tok)
            if m:
                label, url = m.group(1), m.group(2)
                r = paragraph.add_run(label)
                r.font.name = '微軟正黑體'
                r.font.size = Pt(size)
                r.font.color.rgb = COLOR_BLUE
                r.underline = True
                r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
            else:
                r = paragraph.add_run(tok)
                r.font.name = '微軟正黑體'
                r.font.size = Pt(size)
                r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
        else:
            r = paragraph.add_run(tok)
            r.font.name = '微軟正黑體'
            r.font.size = Pt(size)
            r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')

# ─── 逐輪輸出到 Word 文件 ───
for turn_idx, t in enumerate(turns):
    user_data = t["user"]
    asst_text = t["assistant"]
    step_num = user_data["step"]
    time_str = user_data["time"]
    raw_user = user_data["content"]
    
    # 清理使用者文字（剝除 <USER_REQUEST> 標籤與內部系統中繼資訊）
    m_req = re.search(r'<USER_REQUEST>(.*?)</USER_REQUEST>', raw_user, re.DOTALL)
    if m_req:
        clean_user_req = m_req.group(1).strip()
    else:
        # 去除其他 tag
        clean_user_req = re.sub(r'<[^>]+>', '', raw_user).strip()

    # 檢查是否有使用者附圖
    has_image_note = ""
    if "media_1789264530882" in raw_user or "media_1789264821076" in raw_user:
        has_image_note = " 📎 [包含使用者上傳架構附圖]"

    # 1. 輪次標題
    turn_heading_text = f"第 {turn_idx+1} 輪對話 (Turn {turn_idx+1})  ·  Step {step_num}  [{time_str[:19].replace('T', ' ')}]"
    tp = doc.add_paragraph()
    tp.paragraph_format.space_before = Pt(14)
    tp.paragraph_format.space_after = Pt(4)
    tr = tp.add_run(turn_heading_text)
    tr.bold = True
    tr.font.name = '微軟正黑體'
    tr.font.size = Pt(12)
    tr.font.color.rgb = COLOR_NAVY
    tr._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')

    # 2. 使用者發言外框 (綠色主題卡片)
    u_table = doc.add_table(rows=1, cols=1)
    u_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    u_cell = u_table.rows[0].cells[0]
    u_cell.width = Cm(16.5)
    set_cell_shading(u_cell, "E8F5E9") # 淡綠底
    set_cell_margins(u_cell, 80, 80, 120, 120)
    
    up = u_cell.paragraphs[0]
    up.paragraph_format.space_after = Pt(3)
    ur_title = up.add_run(f"👤 使用者提問 / 需求指令{has_image_note}：\n")
    ur_title.bold = True
    ur_title.font.name = '微軟正黑體'
    ur_title.font.size = Pt(10)
    ur_title.font.color.rgb = COLOR_USER
    ur_title._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
    
    ur_body = up.add_run(clean_user_req)
    ur_body.font.name = '微軟正黑體'
    ur_body.font.size = Pt(10)
    ur_body.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    ur_body._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
    
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    # 3. 助理回覆
    if asst_text:
        ap = doc.add_paragraph()
        ap.paragraph_format.space_before = Pt(2)
        ap.paragraph_format.space_after = Pt(3)
        ar = ap.add_run("🤖 AI 助理回覆 (Assistant)：")
        ar.bold = True
        ar.font.name = '微軟正黑體'
        ar.font.size = Pt(10.5)
        ar.font.color.rgb = COLOR_BLUE
        ar._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
        
        render_markdown_block(doc, asst_text)
    else:
        ap = doc.add_paragraph()
        ap.paragraph_format.space_before = Pt(2)
        ap.paragraph_format.space_after = Pt(4)
        ar = ap.add_run("🤖 AI 助理回覆 (Assistant)：（本輪指令發出後，接續收到補充指示合併執行）")
        ar.italic = True
        ar.font.name = '微軟正黑體'
        ar.font.size = Pt(9.5)
        ar.font.color.rgb = COLOR_LGRAY
        ar._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')

    # 每輪結束的細分隔線
    if turn_idx < len(turns) - 1:
        sep_p = doc.add_paragraph()
        sep_p.paragraph_format.space_before = Pt(6)
        sep_p.paragraph_format.space_after = Pt(8)
        sep_r = sep_p.add_run("─" * 65)
        sep_r.font.size = Pt(7)
        sep_r.font.color.rgb = RGBColor(0xCC, 0xD1, 0xD9)

# 4. 儲存 Word 檔案
doc.save(output_path)
print(f"✅ 對話紀錄 Word 文件已成功生成！")
print(f"   儲存位置：{output_path}")
print(f"   總計匯出輪次：{len(turns)} 輪")
