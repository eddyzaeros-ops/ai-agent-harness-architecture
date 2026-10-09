"""
Generate OWASP AI Guardrail Design Presentation adhering to Template 1 (Warm Editorial Minimalism).
Covers all 6 modules from index.html:
- Module 00: Overview & Cross-Layer Defense-in-Depth Matrix
- Module 01: OWASP Top 10 for LLM Guardrail Design
- Module 02: OWASP Top 10 for Agentic Applications Guardrail Design
- Module 03: OWASP Top 10 for Skills (AST10) & The Lethal Trifecta
- Module 04: OWASP RAG Pipeline Guardrail Design
- Module 05: MITRE ATLAS AI Attack Chain Alignment
- Conclusion: Zero-Trust AI Principles & Architecture Manifesto
"""

import sys
import os
import re
import json

# Add template1 module path
sys.path.append(r"C:\Users\calsa\.gemini\config\skills\pptx-template-1\scripts")

import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from template1_builder import (
    init_presentation,
    apply_warm_background,
    add_header,
    add_footer,
    add_bullet_card,
    create_table,
    BG_CANVAS,
    BG_CARD,
    BORDER_CARD,
    BORDER_DIVIDER,
    BRAND_SLATE,
    BRAND_SAGE,
    BRAND_TERRA,
    BRAND_OCHRE,
    TEXT_HEADLINE,
    TEXT_BODY,
    TEXT_MUTED,
    TABLE_HEADER_BG,
    TABLE_ROW_ALT,
    FONT_HEADING,
    FONT_BODY
)

TOTAL_SLIDES = 25

# Load extracted tables
with open(r'd:\JavaDO\OWASP html\all_tables_extracted.json', 'r', encoding='utf-8') as f:
    ALL_TABLES = {t['table_id']: t for t in json.load(f)}

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS FOR WARM EDITORIAL MINIMALISM
# -----------------------------------------------------------------------------

def add_custom_table(slide, left, top, width, height, headers, rows_data, col_widths=None, col_alignments=None, font_size=8.0, has_card_container=True):
    """Refined Table Component with customized cell padding and text styling."""
    if has_card_container:
        container = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(height)
        )
        container.fill.solid()
        container.fill.fore_color.rgb = BG_CARD
        container.line.color.rgb = BORDER_CARD
        container.line.width = Pt(1)
        
        t_left = left + 0.12
        t_top = top + 0.10
        t_width = width - 0.24
        t_height = height - 0.20
    else:
        t_left = left
        t_top = top
        t_width = width
        t_height = height

    num_rows = len(rows_data) + 1
    num_cols = len(headers)
    table_shape = slide.shapes.add_table(num_rows, num_cols, Inches(t_left), Inches(t_top), Inches(t_width), Inches(t_height))
    table = table_shape.table
    
    if col_widths and len(col_widths) == num_cols:
        scale = t_width / sum(col_widths)
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = Inches(w * scale)
            
    # Header Row
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TABLE_HEADER_BG
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = Pt(5)
        cell.margin_right = Pt(5)
        cell.margin_top = Pt(4)
        cell.margin_bottom = Pt(4)
        
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        align = col_alignments[col_idx] if col_alignments and col_idx < len(col_alignments) else (PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER)
        p.alignment = align
        p.font.name = FONT_HEADING
        p.font.size = Pt(font_size + 0.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_HEADLINE
        
    # Data Rows
    for row_idx, r_data in enumerate(rows_data):
        row_bg = TABLE_ROW_ALT if row_idx % 2 == 1 else BG_CARD
        for col_idx, val in enumerate(r_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Pt(5)
            cell.margin_right = Pt(5)
            cell.margin_top = Pt(4)
            cell.margin_bottom = Pt(4)
            
            p = cell.text_frame.paragraphs[0]
            val_str = str(val).strip()
            
            # Format lines nicely if there are bullets or numbers
            lines = val_str.split("\n")
            p.text = lines[0]
            align = col_alignments[col_idx] if col_alignments and col_idx < len(col_alignments) else (PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER)
            p.alignment = align
            p.font.name = FONT_BODY
            p.font.size = Pt(font_size)
            p.line_spacing = 1.12
            
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_HEADLINE
            else:
                p.font.color.rgb = TEXT_BODY
                
            for extra_line in lines[1:]:
                p_next = cell.text_frame.add_paragraph()
                p_next.text = extra_line
                p_next.alignment = align
                p_next.font.name = FONT_BODY
                p_next.font.size = Pt(font_size)
                p_next.line_spacing = 1.12
                if col_idx == 0:
                    p_next.font.bold = True
                    p_next.font.color.rgb = TEXT_HEADLINE
                else:
                    p_next.font.color.rgb = TEXT_BODY


def add_quote_box(slide, left, top, width, height, en_quote, zh_translation, tag_text=None, accent_color=BRAND_TERRA):
    """Standard Centered Warm Editorial Quote Box."""
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    box.fill.solid()
    box.fill.fore_color.rgb = BG_CARD
    box.line.color.rgb = BORDER_CARD
    box.line.width = Pt(1)
    
    tb = slide.shapes.add_textbox(Inches(left + 0.3), Inches(top + 0.25), Inches(width - 0.6), Inches(height - 0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.alignment = PP_ALIGN.CENTER
    if tag_text:
        r_tag = p0.add_run()
        r_tag.text = f"✦  {tag_text}\n\n"
        r_tag.font.name = FONT_HEADING
        r_tag.font.size = Pt(9.5)
        r_tag.font.bold = True
        r_tag.font.color.rgb = BRAND_SAGE
        
    r_en = p0.add_run()
    r_en.text = f"“ {en_quote} ”"
    r_en.font.name = FONT_HEADING
    r_en.font.size = Pt(13)
    r_en.font.bold = True
    r_en.font.color.rgb = accent_color
    
    p1 = tf.add_paragraph()
    p1.alignment = PP_ALIGN.CENTER
    p1.space_before = Pt(8)
    r_zh = p1.add_run()
    r_zh.text = zh_translation
    r_zh.font.name = FONT_BODY
    r_zh.font.size = Pt(10)
    r_zh.font.color.rgb = TEXT_MUTED


def add_stat_card(slide, left, top, width, height, number_str, label_str, desc_str="", accent_color=BRAND_SAGE):
    """Metric KPI Card."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_CARD
    card.line.color.rgb = BORDER_CARD
    card.line.width = Pt(1)
    
    tb = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.12), Inches(width - 0.3), Inches(height - 0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    r_num = p0.add_run()
    r_num.text = number_str
    r_num.font.name = FONT_HEADING
    r_num.font.size = Pt(20)
    r_num.font.bold = True
    r_num.font.color.rgb = accent_color
    
    p1 = tf.add_paragraph()
    p1.space_before = Pt(2)
    r_lbl = p1.add_run()
    r_lbl.text = label_str
    r_lbl.font.name = FONT_HEADING
    r_lbl.font.size = Pt(9.5)
    r_lbl.font.bold = True
    r_lbl.font.color.rgb = TEXT_HEADLINE
    
    if desc_str:
        p2 = tf.add_paragraph()
        p2.space_before = Pt(2)
        r_desc = p2.add_run()
        r_desc.text = desc_str
        r_desc.font.name = FONT_BODY
        r_desc.font.size = Pt(8)
        r_desc.font.color.rgb = TEXT_MUTED


# -----------------------------------------------------------------------------
# SLIDE BUILDERS (1 ~ 25)
# -----------------------------------------------------------------------------

def build_slide_01_cover(prs):
    """Slide 01: Warm Editorial Minimalism Cover."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    
    # Top Tag Capsule
    cat_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.3), Inches(4.5), Inches(0.36))
    cat_box.fill.solid()
    cat_box.fill.fore_color.rgb = RGBColor(0xE8, 0xE2, 0xD5)
    cat_box.line.color.rgb = BORDER_CARD
    cat_box.line.width = Pt(0.75)
    tf_c = cat_box.text_frame
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.alignment = PP_ALIGN.CENTER
    r_c = p_c.add_run()
    r_c.text = "✦  EXECUTIVE ARCHITECTURE SPECIFICATION  ·  2026"
    r_c.font.name = FONT_HEADING
    r_c.font.size = Pt(10)
    r_c.font.bold = True
    r_c.font.color.rgb = BRAND_SAGE
    
    # Large Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(1.9), Inches(11.733), Inches(1.6))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = "OWASP AI 護欄體系架構設計規範全景"
    r_t.font.name = FONT_HEADING
    r_t.font.size = Pt(32)
    r_t.font.bold = True
    r_t.font.color.rgb = TEXT_HEADLINE
    
    p_sub = tf_t.add_paragraph()
    p_sub.space_before = Pt(8)
    r_sub = p_sub.add_run()
    r_sub.text = "LLM 基礎模型 · Agentic 代理人行為 · Skills 技能沙盒 · RAG 檢索增強 · MITRE ATLAS 攻擊鍊全維對齊"
    r_sub.font.name = FONT_BODY
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = BRAND_TERRA
    
    # Hairline divider
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.7), Inches(11.733), Inches(0.015))
    div.fill.solid()
    div.fill.fore_color.rgb = BORDER_DIVIDER
    div.line.fill.background()
    
    # 4 Metadata Cards at Bottom
    meta_items = [
        ("涵蓋核心安全標準", "OWASP LLM / Agentic / Skills / RAG / ATLAS", "跨層縱深防禦體系標準"),
        ("核心防禦架構哲學", "零信任 (Zero-Trust) · 狀態約束 · 破除致命三要素", "無狀態過濾轉向有狀態監督"),
        ("合規與風險對齊", "ISO/IEC 42001 AIMS · NIST AI RMF · EU AI Act", "具備不可否認性審計追蹤"),
        ("發布與維護工作小組", "AI Harness Engineering Architecture Taskforce", "企業級生產環境防護指引")
    ]
    
    card_w = 2.78
    card_h = 2.3
    gap = 0.20
    for idx, (title, main_val, sub_val) in enumerate(meta_items):
        c_left = 0.8 + idx * (card_w + gap)
        c = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(4.0), Inches(card_w), Inches(card_h))
        c.fill.solid()
        c.fill.fore_color.rgb = BG_CARD
        c.line.color.rgb = BORDER_CARD
        c.line.width = Pt(1)
        
        tb = slide.shapes.add_textbox(Inches(c_left + 0.16), Inches(4.16), Inches(card_w - 0.32), Inches(card_h - 0.32))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = f"0{idx+1}  {title}"
        r0.font.name = FONT_HEADING
        r0.font.size = Pt(8.5)
        r0.font.bold = True
        r0.font.color.rgb = BRAND_SAGE
        
        p1 = tf.add_paragraph()
        p1.space_before = Pt(8)
        r1 = p1.add_run()
        r1.text = main_val
        r1.font.name = FONT_HEADING
        r1.font.size = Pt(10.5)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_HEADLINE
        
        p2 = tf.add_paragraph()
        p2.space_before = Pt(6)
        r2 = p2.add_run()
        r2.text = sub_val
        r2.font.name = FONT_BODY
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXT_MUTED

    add_footer(slide, 1, TOTAL_SLIDES)


def build_slide_02_overview_matrix(prs):
    """Slide 02: 五層縱深防禦全景與三層護欄協同流轉."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "五層縱深防禦架構全景與三層核心護欄協同流轉", "護欄體系總覽", "從傳統網路/API邊界邁向語意、行為、沙盒與檢索的多維防禦鏈路")
    
    col_w = 3.75
    gap = 0.24
    top = 1.68
    h = 5.25
    
    # Col 1: L1~L5 五層架構
    add_bullet_card(
        slide, left=0.8, top=top, width=col_w, height=h,
        title="縱深防禦五層全景 (L1~L5)",
        items=[
            "L1 API 閘道層：傳輸層 TLS 加密、IP 速率限制與 WAF/DDoS 抵禦。",
            "L2 語意閘門層：Prompt 注入檢驗、越獄模式過濾、PII 遮罩與 DLP。",
            "L3 代理人執行監督層：有限狀態機（FSM）約束、目標錨定與去話術 HITL。",
            "L4 技能工具沙盒層：微容器（gVisor/Firecracker）隔離、致命三要素切斷。",
            "L5 檢索增強隔離層：文檔入庫清洗、Pre-Retrieval 權限過濾、XML 標籤封裝。"
        ],
        tag="DEFENSE-IN-DEPTH",
        accent_color=BRAND_SAGE,
        header_bg=BRAND_SLATE
    )
    
    # Col 2: 三層核心護欄協同
    add_bullet_card(
        slide, left=0.8 + col_w + gap, top=top, width=col_w, height=h,
        title="三層核心護欄協同 (Three-Tier Synergy)",
        items=[
            "G1 LLM 語意邊界：充當對話出入閘口，攔截對抗性文本與提示詞外洩。",
            "G2 Agentic 行為狀態機：監督自主決策與規劃路徑，防止目標被惡意劫持。",
            "G3 Skills 工具沙盒：嚴格管控底層 API/代碼執行，落實最小權限隔離。",
            "動態跨層連動：G1 發現可疑注入即時降級 G2 授權權限，阻斷 G3 執行。",
            "記憶分艙保護：短期記憶迭代洗滌，長期記憶雜湊綁定，防止記憶庫投毒。"
        ],
        tag="CORE SYNERGY",
        accent_color=BRAND_TERRA,
        header_bg=BRAND_SLATE
    )
    
    # Col 3: 審計日誌與運作原則
    add_bullet_card(
        slide, left=0.8 + (col_w + gap) * 2, top=top, width=col_w, height=h,
        title="全鏈路不可否認性審計與防護規格",
        items=[
            "8 大關鍵欄位：包含時間戳、Trace ID、客戶身分、輸入 SHA-256、判定結果等。",
            "HMAC 防竄改簽章：確保日誌具備完整法律證據力與事故鑑識價值。",
            "去話術 HITL (Human-in-the-Loop)：嚴禁代理人修辭粉飾，UI 呈現原始結構化參數。",
            "動態 JIT 短效憑證：拒絕長期靜態金鑰，每次工具調用前申請 60 秒權限。",
            "全鏈路追蹤：透過分散式 Trace ID 貫穿 Client、閘道、LLM 與沙盒調用。"
        ],
        tag="AUDIT & GOVERNANCE",
        accent_color=BRAND_OCHRE,
        header_bg=BRAND_SLATE
    )
    
    add_footer(slide, 2, TOTAL_SLIDES)


def build_slide_03_module_navigation_table(prs):
    """Slide 03: 五篇專題筆記核心導航與關聯 (Table 1)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "五大核心防禦模組防護重心與安全框架對齊矩陣", "模組導航矩陣", "全景梳理各防禦模組之防護重心、對齊安全標準與整體架構守備職責")
    
    t_data = ALL_TABLES[1]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'],
        col_widths=[2.4, 2.3, 2.5, 4.5],
        col_alignments=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT],
        font_size=8.5
    )
    add_footer(slide, 3, TOTAL_SLIDES)


def build_slide_04_defense_in_depth_scenario(prs):
    """Slide 04: 跨層威脅滲透與縱深攔截機制 (Defense-in-Depth Scenario)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "跨層威脅滲透與三階段縱深攔截機制", "縱深防禦場景", "模擬真實多階段複合攻擊演進，解析各護欄層級之協同聯動與梯次阻斷機制")
    
    col_w = 3.75
    gap = 0.24
    top = 1.68
    stage_h = 3.42
    
    stages_data = [
        {
            "stage_num": "1",
            "title": "階段一：入向語意穿透 (Ingress)",
            "layer_tag": "L5 檢索閘門 ⨂ L2 語意閘門",
            "header_color": BRAND_SLATE,
            "badge_color": BRAND_SAGE,
            "threat_title": "威脅滲透樣態 (Attack Vector)",
            "threat_desc": "攻擊者透過工單系統上傳夾帶「間接提示詞注入 (Indirect Prompt Injection)」之 PDF 文檔，利用白底微小字型隱藏攻擊指令，誘騙模型讀取內部敏感憑證與資料庫金鑰。",
            "defense_title": "縱深攔截防線 (Defense Interception)",
            "defense_bullets": [
                "L5 檢索閘門：文檔解析沙盒清除微小字型，輕量 SLM 分類器檢測高對抗性指令特徵。",
                "L2 語意閘門：檢索回傳強制以 <untrusted_rag_context> 標籤封裝，聲明純事實屬性嚴禁執行。"
            ]
        },
        {
            "stage_num": "2",
            "title": "階段二：代理決策劫持 (Goal Hijack)",
            "layer_tag": "L3 代理人執行監督器",
            "header_color": BRAND_SLATE,
            "badge_color": BRAND_TERRA,
            "threat_title": "威脅滲透樣態 (Attack Vector)",
            "threat_desc": "若注入指令透過變形混淆突破語意閘門，進入 Agent 推理上下文，企圖竄改代理人執行目標（Goal Hijack），誘導其背離原始任務去呼叫內部資料庫備份工具。",
            "defense_title": "縱深攔截防線 (Defense Interception)",
            "defense_bullets": [
                "L3 目標錨定門：即時計算 Action 與根目標之語意餘弦相似度，偏離門檻即刻告警阻斷。",
                "L3 規劃重評門：高危操作強制觸發「情境化去話術 HITL」，由人工審批結構化參數。"
            ]
        },
        {
            "stage_num": "3",
            "title": "階段三：橫向移動與外傳 (Exfiltration)",
            "layer_tag": "L4 技能工具沙盒 (Micro-Sandbox)",
            "header_color": BRAND_SLATE,
            "badge_color": BRAND_OCHRE,
            "threat_title": "威脅滲透樣態 (Attack Vector)",
            "threat_desc": "假設攻擊者進一步試圖直接呼叫系統底層工具連線外部惡意伺服器（C2）將資料打包外傳，或嘗試寫入本地持久化排程任務實施提權。",
            "defense_title": "縱深攔截防線 (Defense Interception)",
            "defense_bullets": [
                "L4 技能微沙盒：嚴格執行「破除致命三要素」，處理機敏資料之工具強制 Disable-Net 禁外網。",
                "L4 系統調用審計：eBPF 實時捕獲異常連線嘗試，秒級觸發看門狗熔斷並阻斷進程。"
            ]
        }
    ]
    
    # 1. Top 3 Stage Cards
    for idx, s in enumerate(stages_data):
        c_left = 0.8 + idx * (col_w + gap)
        
        # Outer Card Container
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(top), Inches(col_w), Inches(stage_h))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BORDER_CARD
        card.line.width = Pt(1)
        
        # Header bar
        header_h = 0.48
        h_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(top), Inches(col_w), Inches(header_h))
        h_shape.fill.solid()
        h_shape.fill.fore_color.rgb = s["header_color"]
        h_shape.line.fill.background()
        
        # Circular Badge in Header
        badge_dia = 0.26
        badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(c_left + 0.12), Inches(top + 0.11), Inches(badge_dia), Inches(badge_dia))
        badge.fill.solid()
        badge.fill.fore_color.rgb = s["badge_color"]
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
        pb = tf_b.paragraphs[0]
        pb.alignment = PP_ALIGN.CENTER
        rb = pb.add_run()
        rb.text = s["stage_num"]
        rb.font.name = FONT_HEADING
        rb.font.size = Pt(8.5)
        rb.font.bold = True
        rb.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        # Header Text
        tb_h = slide.shapes.add_textbox(Inches(c_left + 0.44), Inches(top + 0.05), Inches(col_w - 0.52), Inches(header_h - 0.10))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
        p_h = tf_h.paragraphs[0]
        r_title = p_h.add_run()
        r_title.text = s["title"]
        r_title.font.name = FONT_HEADING
        r_title.font.size = Pt(9.5)
        r_title.font.bold = True
        r_title.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        p_sub = tf_h.add_paragraph()
        r_tag = p_sub.add_run()
        r_tag.text = f"守備層級：{s['layer_tag']}"
        r_tag.font.name = FONT_BODY
        r_tag.font.size = Pt(8)
        r_tag.font.color.rgb = RGBColor(0xD6, 0xCE, 0xBF)
        
        # Content Text Box
        content_top = top + header_h + 0.10
        content_h = stage_h - header_h - 0.18
        tb_c = slide.shapes.add_textbox(Inches(c_left + 0.16), Inches(content_top), Inches(col_w - 0.32), Inches(content_h))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        
        # Threat block
        p0 = tf_c.paragraphs[0]
        r_th = p0.add_run()
        r_th.text = f"▲  {s['threat_title']}"
        r_th.font.name = FONT_HEADING
        r_th.font.size = Pt(9)
        r_th.font.bold = True
        r_th.font.color.rgb = BRAND_TERRA
        
        p1 = tf_c.add_paragraph()
        p1.space_before = Pt(3)
        p1.line_spacing = 1.15
        r_tb = p1.add_run()
        r_tb.text = s["threat_desc"]
        r_tb.font.name = FONT_BODY
        r_tb.font.size = Pt(8.5)
        r_tb.font.color.rgb = TEXT_BODY
        
        # Defense block
        p2 = tf_c.add_paragraph()
        p2.space_before = Pt(7)
        r_dh = p2.add_run()
        r_dh.text = f"🛡  {s['defense_title']}"
        r_dh.font.name = FONT_HEADING
        r_dh.font.size = Pt(9)
        r_dh.font.bold = True
        r_dh.font.color.rgb = BRAND_SAGE
        
        for b_text in s["defense_bullets"]:
            pb = tf_c.add_paragraph()
            pb.space_before = Pt(3)
            pb.line_spacing = 1.15
            parts = b_text.split("：", 1)
            if len(parts) == 2:
                r_head = pb.add_run()
                r_head.text = "• " + parts[0] + "："
                r_head.font.name = FONT_HEADING
                r_head.font.size = Pt(8.5)
                r_head.font.bold = True
                r_head.font.color.rgb = BRAND_SLATE
                
                r_body = pb.add_run()
                r_body.text = parts[1]
                r_body.font.name = FONT_BODY
                r_body.font.size = Pt(8)
                r_body.font.color.rgb = TEXT_BODY
            else:
                r_body = pb.add_run()
                r_body.text = "• " + b_text
                r_body.font.name = FONT_BODY
                r_body.font.size = Pt(8)
                r_body.font.color.rgb = TEXT_BODY

    # 2. Bottom Container: 零信任 AI 四大落地原則
    bot_top = top + stage_h + 0.16
    bot_h = 1.72
    
    bot_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(bot_top), Inches(11.733), Inches(bot_h))
    bot_card.fill.solid()
    bot_card.fill.fore_color.rgb = BG_CARD
    bot_card.line.color.rgb = BORDER_CARD
    bot_card.line.width = Pt(1)
    
    # Title
    tb_bt = slide.shapes.add_textbox(Inches(1.0), Inches(bot_top + 0.08), Inches(11.333), Inches(0.26))
    tf_bt = tb_bt.text_frame
    tf_bt.word_wrap = True
    tf_bt.margin_left = tf_bt.margin_top = tf_bt.margin_right = tf_bt.margin_bottom = 0
    p_bt = tf_bt.paragraphs[0]
    r_bt = p_bt.add_run()
    r_bt.text = "✦  零信任（Zero-Trust）AI 護欄架構四大落地實踐原則"
    r_bt.font.name = FONT_HEADING
    r_bt.font.size = Pt(10)
    r_bt.font.bold = True
    r_bt.font.color.rgb = BRAND_SLATE
    
    # 4 Columns inside bottom container
    principles = [
        ("01", "永不信任輸入", "所有外部文字與檢索語料一律視為不可信，強制包覆 XML 結構化隔離標籤與分類器檢驗。", BRAND_SAGE),
        ("02", "行為狀態約束", "以有限狀態機（FSM）界定合法行動邊界，限制自主步數上限，杜絕失控執行。", BRAND_TERRA),
        ("03", "破除致命三要素", "機敏憑證、外網連線、不可信語料絕不同時賦予單一工具，微沙盒強制隔離。", BRAND_OCHRE),
        ("04", "全鏈路審計", "全流程記錄輸入 SHA-256、判定結果與 HMAC-SHA256 防竄改簽章，確保法律鑑識效力。", BRAND_SLATE)
    ]
    
    p_w = 2.68
    p_gap = 0.20
    for idx, (num, p_title, p_desc, p_color) in enumerate(principles):
        p_left = 1.0 + idx * (p_w + p_gap)
        
        # Circular Badge
        bdia = 0.24
        p_badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(p_left), Inches(bot_top + 0.38), Inches(bdia), Inches(bdia))
        p_badge.fill.solid()
        p_badge.fill.fore_color.rgb = p_color
        p_badge.line.fill.background()
        tf_pb = p_badge.text_frame
        tf_pb.margin_left = tf_pb.margin_top = tf_pb.margin_right = tf_pb.margin_bottom = 0
        ppb = tf_pb.paragraphs[0]
        ppb.alignment = PP_ALIGN.CENTER
        rpb = ppb.add_run()
        rpb.text = num
        rpb.font.name = FONT_HEADING
        rpb.font.size = Pt(8)
        rpb.font.bold = True
        rpb.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        # Principle Title
        tb_pt = slide.shapes.add_textbox(Inches(p_left + 0.32), Inches(bot_top + 0.36), Inches(p_w - 0.34), Inches(0.26))
        tf_pt = tb_pt.text_frame
        tf_pt.word_wrap = True
        tf_pt.margin_left = tf_pt.margin_top = tf_pt.margin_right = tf_pt.margin_bottom = 0
        ppt = tf_pt.paragraphs[0]
        rpt = ppt.add_run()
        rpt.text = p_title
        rpt.font.name = FONT_HEADING
        rpt.font.size = Pt(9.5)
        rpt.font.bold = True
        rpt.font.color.rgb = BRAND_SLATE
        
        # Principle Description
        tb_pd = slide.shapes.add_textbox(Inches(p_left), Inches(bot_top + 0.68), Inches(p_w), Inches(bot_h - 0.74))
        tf_pd = tb_pd.text_frame
        tf_pd.word_wrap = True
        tf_pd.margin_left = tf_pd.margin_top = tf_pd.margin_right = tf_pd.margin_bottom = 0
        ppd = tf_pd.paragraphs[0]
        ppd.line_spacing = 1.15
        rpd = ppd.add_run()
        rpd.text = p_desc
        rpd.font.name = FONT_BODY
        rpd.font.size = Pt(8.5)
        rpd.font.color.rgb = TEXT_BODY
        
    add_footer(slide, 4, TOTAL_SLIDES)



def build_slide_05_llm_architecture(prs):
    """Slide 05: LLM 基礎模型護欄架構全景與三大核心處理管線."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "LLM 基礎模型護欄架構全景與三大核心處理管線", "LLM 基礎模型護欄", "入向檢驗、執行時保護與出向過濾的單一出入口雙向閉環防禦")
    
    col_w = 3.75
    gap = 0.24
    top = 1.68
    h = 5.25
    
    # Col 1: Ingress
    add_bullet_card(
        slide, left=0.8, top=top, width=col_w, height=h,
        title="入向檢驗模組 (Ingress Pipeline)",
        items=[
            "輕量分類器模型：部署 Llama-Guard 3、NeMo Guardrails 實時評估越獄、自殘、仇恨等安全風險。",
            "語意結構隔離：採用 XML/Markdown 邊界標記符隔離 Context 與 Instructions，並置入 Canary Token。",
            "啟發式特徵庫：基於正則表達式與向量相似度，秒級比對已知越獄 Prompt 與攻擊指紋。",
            "長度與編碼防禦：檢查 Base64、Unicode 混淆，強制截斷超過上下文長度之畸形封包。",
            "單一入口收斂：禁止任何未經入向檢驗的 Raw Prompt 直接抵達模型推論引擎。"
        ],
        tag="INGRESS FILTER",
        accent_color=BRAND_SAGE,
        header_bg=BRAND_SLATE
    )
    
    # Col 2: Runtime
    add_bullet_card(
        slide, left=0.8 + col_w + gap, top=top, width=col_w, height=h,
        title="執行時保護模組 (Runtime Guard)",
        items=[
            "系統提示詞數位簽章：核心 System Prompt 計算 SHA-256 雜湊鎖定唯讀，防止動態竄改與覆寫。",
            "上下文配額管制 (Budget Guard)：嚴格限制單次會話 Token 上限與呼叫頻率，防範資源耗盡攻擊。",
            "向量快取投毒防護：對話歷程與向量快取切片分區隔離，即時失效被污染之快取項目。",
            "對齊防護網：監控模型思考鏈（Chain-of-Thought），確保推論邏輯未遭注入特徵劫持。",
            "推論逾時看門狗：設置嚴格推論超時閾值，避免對抗性 Prompt 誘發無窮推論死循環。"
        ],
        tag="RUNTIME PROTECTION",
        accent_color=BRAND_TERRA,
        header_bg=BRAND_SLATE
    )
    
    # Col 3: Egress
    add_bullet_card(
        slide, left=0.8 + (col_w + gap) * 2, top=top, width=col_w, height=h,
        title="出向過濾模組 (Egress Pipeline)",
        items=[
            "PII/機敏資料動態遮罩：整合 Microsoft Presidio 辨識身分證、信用卡、API 金鑰等並予以 Masking。",
            "幻覺與忠實度比對：輕量 SLM 計算生成答覆相對於 Context 之 Faithfulness 分數，未達標則拒絕。",
            "輸出轉義與編碼：對 HTML、JavaScript、SQL 等敏感語法實施強制轉義，杜絕 XSS 與二次注入。",
            "出向 DLP 關鍵字庫：嚴密監控內部機密代號、伺服器 IP、原始提示詞洩漏特徵。",
            "安全阻斷降級回覆：觸發攔截時返回預先編排之合規提示語，絕不暴露內部錯誤堆疊。"
        ],
        tag="EGRESS FILTER",
        accent_color=BRAND_OCHRE,
        header_bg=BRAND_SLATE
    )
    
    add_footer(slide, 5, TOTAL_SLIDES)


def build_slide_06_llm_top10_p1(prs):
    """Slide 06: OWASP Top 10 for LLM 防禦矩陣 (Part 1: LLM01 ~ LLM05)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "OWASP Top 10 for LLM 防禦矩陣 (LLM01 ～ LLM05)", "LLM 威脅防禦矩陣", "提示詞注入、機敏資訊洩漏、供應鏈脆弱、資料投毒與不安全輸出處理")
    
    t_data = ALL_TABLES[2]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][:5],
        col_widths=[2.2, 2.5, 1.8, 3.8, 1.4],
        col_alignments=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER],
        font_size=7.8
    )
    add_footer(slide, 6, TOTAL_SLIDES)


def build_slide_07_llm_top10_p2(prs):
    """Slide 07: OWASP Top 10 for LLM 防禦矩陣 (Part 2: LLM06 ~ LLM10)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "OWASP Top 10 for LLM 防禦矩陣 (LLM06 ～ LLM10)", "LLM 威脅防禦矩陣", "過度授權、提示詞洩漏、向量資訊弱點、模型幻覺與無限制資源消耗")
    
    t_data = ALL_TABLES[2]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][5:10],
        col_widths=[2.2, 2.5, 1.8, 3.8, 1.4],
        col_alignments=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER],
        font_size=7.8
    )
    add_footer(slide, 7, TOTAL_SLIDES)


def build_slide_08_llm_quant_audit(prs):
    """Slide 08: LLM 全球實證風險分佈與不可否認性審計日誌規格."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "LLM 全球實證量化分佈與不可否認性審計日誌規格", "實證量化與審計規格", "公開事件 (n=6,639) 揭示防禦可見性悖論，結合 8 大防竄改審計欄位與主流技術選型")
    
    col_w = 5.75
    gap = 0.23
    top = 1.68
    h = 5.25
    
    # Left: Table 3 Top 5 risks
    t_data = ALL_TABLES[3]
    top_5_rows = t_data['rows'][:5]
    add_custom_table(
        slide, left=0.8, top=top, width=col_w, height=h,
        headers=t_data['headers'],
        rows_data=top_5_rows,
        col_widths=[1.0, 1.8, 1.3, 1.3, 2.3],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=7.5
    )
    
    # Right: Audit Log Spec + Tech Stack
    right_left = 0.8 + col_w + gap
    add_bullet_card(
        slide, left=right_left, top=top, width=col_w, height=h,
        title="審計日誌規格與工程技術選型",
        items=[
            "timestamp：高精度 ISO-8601 毫秒時間戳記，提供時序溯源依據。",
            "session_id / trace_id：分散式追蹤標識符，串聯閘道、推論與工具鏈。",
            "client_identity：呼叫方身分憑證（API Key / mTLS / JWT Token）。",
            "input_hash：原始 Prompt 之 SHA-256 數位指紋，確保原始請求不可否認。",
            "guardrail_verdict：護欄決策結果（PASS / SANITIZED / BLOCKED）。",
            "signature：整筆日誌以密鑰計算之 HMAC-SHA256 簽名，杜絕後續日誌竄改。",
            "NeMo Guardrails：NVIDIA 開源對話流與語意邊界控制，落實雙向安全攔截。",
            "Microsoft Presidio：微軟機敏實體（PII）偵測與去識別化遮罩引擎。",
            "Meta Llama-Guard 3：輕量化安全審查與越獄分類專用模型（8B/1B）。"
        ],
        tag="AUDIT SPEC & TECH STACK",
        accent_color=BRAND_TERRA,
        header_bg=BRAND_SLATE
    )
    
    add_footer(slide, 8, TOTAL_SLIDES)


def build_slide_09_agentic_paradigm(prs):
    """Slide 09: Agentic 代理人行為護欄：典範轉移對比 (Table 4)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "典範轉移：傳統 LLM 護欄 vs. Agentic 代理人行為護欄", "Agentic 行為護欄", "從無狀態語意過濾邁向有狀態執行監督，全方位掌控目標、工具、狀態與記憶")
    
    t_data = ALL_TABLES[4]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'],
        col_widths=[1.8, 4.8, 5.1],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT],
        font_size=8.5
    )
    add_footer(slide, 9, TOTAL_SLIDES)


def build_slide_10_agentic_top10_p1(prs):
    """Slide 10: OWASP Top 10 for Agentic Applications (Part 1: ASI01 ~ ASI05)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "OWASP Top 10 for Agentic Applications (ASI01 ～ ASI05)", "Agentic 威脅矩陣", "代理人目標劫持、工具不安全調用、身分特權溢出、代理人供應鏈與非預期代碼執行")
    
    t_data = ALL_TABLES[5]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][:5],
        col_widths=[2.5, 2.7, 2.2, 4.3],
        col_alignments=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=8.0
    )
    add_footer(slide, 10, TOTAL_SLIDES)


def build_slide_11_agentic_top10_p2(prs):
    """Slide 11: OWASP Top 10 for Agentic Applications (Part 2: ASI06 ~ ASI10)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "OWASP Top 10 for Agentic Applications (ASI06 ～ ASI10)", "Agentic 威脅矩陣", "記憶投毒、多代理人通訊攔截、級聯連鎖失敗、拒絕服務與缺乏有效人機監督")
    
    t_data = ALL_TABLES[5]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][5:10],
        col_widths=[2.5, 2.7, 2.2, 4.3],
        col_alignments=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=8.0
    )
    add_footer(slide, 11, TOTAL_SLIDES)


def build_slide_12_agentic_architecture(prs):
    """Slide 12: Agentic 「三維六門」系統架構與核心安全控制規格."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "Agentic 「三維六門」防禦架構與核心安全控制規格", "三維六門架構", "以有限狀態機約束自主行為，結合 JIT 憑證、去話術 HITL 與記憶分艙隔離")
    
    col_w = 3.75
    gap = 0.24
    top = 1.68
    h = 5.25
    
    # Col 1: 意圖與規劃
    add_bullet_card(
        slide, left=0.8, top=top, width=col_w, height=h,
        title="意圖與規劃維度 (Intent & Planning)",
        items=[
            "門 1：目標錨定門 (Goal Anchor)：System Prompt 雜湊數位簽章並設為唯讀；計算規劃步驟與核心目標之語意餘弦相似度，偏離即阻斷。",
            "門 2：規劃重評門 (Plan Re-evaluator)：由隔離的 Supervisor Model 獨立審查 Action Plan，驗證子任務合法性，防止隱蔽提權。",
            "不可變目標約束：代理人無權動態修改最初由使用者或工作流程指定的 Root Mission。",
            "路徑偏離斷路器：單一任務內偏離閥值累計超過 2 次，強制降級回報人工審批。",
            "規劃步驟上限：單次自主執行路徑限制最大 25 步，避免產生無界自主推論。"
        ],
        tag="PLANNING GUARD",
        accent_color=BRAND_SAGE,
        header_bg=BRAND_SLATE
    )
    
    # Col 2: 工具調用
    add_bullet_card(
        slide, left=0.8 + col_w + gap, top=top, width=col_w, height=h,
        title="工具調用維度 (Tool Execution)",
        items=[
            "門 3：JIT 動態憑證門 (JIT Credential Gate)：拒絕持有靜態 Long-lived Token；調用工具前向授權中心動態申請 60 秒短效 Token。",
            "門 4：情境化去話術 HITL (Contextual HITL)：涉及匯款、刪除、寫入等高危操作時，強制呈現結構化參數比對，嚴禁代理人修辭粉飾。",
            "參數 Schema 強制校驗：所有 Tool Call 必須通過 Pydantic/JSON Schema 嚴格型別驗證。",
            "呼叫頻率限制：對高危工具實施每分鐘最大調用次數（Rate Limit），防止泛洪濫用。",
            "沙盒隔離中繼：工具呼叫皆由外部 Harness 代理執行，模型本體無作業系統直連權限。"
        ],
        tag="TOOL SAFETY",
        accent_color=BRAND_TERRA,
        header_bg=BRAND_SLATE
    )
    
    # Col 3: 記憶與狀態
    add_bullet_card(
        slide, left=0.8 + (col_w + gap) * 2, top=top, width=col_w, height=h,
        title="記憶與狀態維度 (Memory & State)",
        items=[
            "門 5：記憶毒化清洗門 (Memory Sanitizer)：短期記憶每輪迭代過濾注入指令；長期向量記憶切片綁定雜湊，高密級資料嚴禁沉澱為泛用記憶。",
            "門 6：級聯熔斷看門狗 (Cascade Breaker)：多代理人協同設置最大遞迴深度、Token 消耗配額，連續異常重試 3 次立即熔斷。",
            "有限狀態機約束：以 FSM 明確規範 Agent 狀態移轉，非法狀態跳躍立即拋出例外。",
            "短期會話沙盒：每次任務執行完畢立即釋放記憶體空間，杜絕殘留跨會話污染。",
            "狀態快照備份：每完成一個驗證過的里程碑即建立 Checkpoint，支援快速回滾。"
        ],
        tag="STATE MACHINE",
        accent_color=BRAND_OCHRE,
        header_bg=BRAND_SLATE
    )
    
    add_footer(slide, 12, TOTAL_SLIDES)


def build_slide_13_agentic_quant(prs):
    """Slide 13: 全球 Agentic 應用受駭事件與執行時告警量化分佈 (Table 6)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "全球 Agentic 應用受駭事件與執行時告警量化分佈", "Agentic 量化分佈", "分析 ASI01 ～ ASI10 實證受駭事件與監控告警，揭示目標劫持與工具濫用為最大宗風險")
    
    t_data = ALL_TABLES[6]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'],
        col_widths=[1.0, 2.5, 1.8, 1.8, 4.6],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=7.5
    )
    add_footer(slide, 13, TOTAL_SLIDES)


def build_slide_14_skills_lethal_trifecta(prs):
    """Slide 14: Skills 技能工具安全護欄：破解「致命三要素 (The Lethal Trifecta)」."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "Skills 核心威脅模型：破解「致命三要素 (The Lethal Trifecta)」", "Skills 技能工具護欄", "機敏憑證 ⨂ 任意網路連線 ⨂ 不可信外部語料的三角隔離哲學與架構封鎖")
    
    col_w = 3.75
    gap = 0.24
    top = 1.68
    card_h = 2.45
    
    elements = [
        {
            "num": "1",
            "title": "要素一：機敏環境與身分憑證",
            "en_subtitle": "Sensitive Internal Credentials",
            "badge_color": BRAND_SAGE,
            "bullets": [
                ("憑證範疇", "資料庫連線密碼、內部 API 金鑰、雲端 IAM 憑證、私有儲存存取權限。"),
                ("威脅後果", "一旦遭外洩或越權使用，將造成核心業務資料資產全面失守。")
            ]
        },
        {
            "num": "2",
            "title": "要素二：對外任意網路通訊",
            "en_subtitle": "Outbound Arbitrary Network Access",
            "badge_color": BRAND_TERRA,
            "bullets": [
                ("通訊能力", "具備主動發起外部 HTTP/HTTPS 請求、Raw Socket、DNS 外發通訊能力。"),
                ("威脅後果", "攻擊者利用此外部通道將竊取之敏感資料直接外傳至遠端 C2 伺服器。")
            ]
        },
        {
            "num": "3",
            "title": "要素三：解析不可信外部語料",
            "en_subtitle": "Processing Untrusted External Data",
            "badge_color": BRAND_OCHRE,
            "bullets": [
                ("輸入來源", "直接讀取外部網頁內容、第三方郵件附件、開放檔案上傳、非受控工單。"),
                ("威脅後果", "語料極易夾帶惡意間接提示詞注入指令，反向劫持工具底層執行邏輯。")
            ]
        }
    ]
    
    for idx, el in enumerate(elements):
        c_left = 0.8 + idx * (col_w + gap)
        
        # Outer Card Container
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(top), Inches(col_w), Inches(card_h))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BORDER_CARD
        card.line.width = Pt(1)
        
        # Header bar
        header_h = 0.46
        h_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(top), Inches(col_w), Inches(header_h))
        h_shape.fill.solid()
        h_shape.fill.fore_color.rgb = BRAND_SLATE
        h_shape.line.fill.background()
        
        # Circular Badge in Header
        badge_dia = 0.26
        badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(c_left + 0.12), Inches(top + 0.10), Inches(badge_dia), Inches(badge_dia))
        badge.fill.solid()
        badge.fill.fore_color.rgb = el["badge_color"]
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
        pb = tf_b.paragraphs[0]
        pb.alignment = PP_ALIGN.CENTER
        rb = pb.add_run()
        rb.text = el["num"]
        rb.font.name = FONT_HEADING
        rb.font.size = Pt(8.5)
        rb.font.bold = True
        rb.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        # Header Title
        tb_h = slide.shapes.add_textbox(Inches(c_left + 0.44), Inches(top + 0.04), Inches(col_w - 0.52), Inches(header_h - 0.08))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
        p_h = tf_h.paragraphs[0]
        r_title = p_h.add_run()
        r_title.text = el["title"]
        r_title.font.name = FONT_HEADING
        r_title.font.size = Pt(9.5)
        r_title.font.bold = True
        r_title.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        p_sub = tf_h.add_paragraph()
        r_sub = p_sub.add_run()
        r_sub.text = el["en_subtitle"]
        r_sub.font.name = FONT_BODY
        r_sub.font.size = Pt(8)
        r_sub.font.color.rgb = RGBColor(0xD6, 0xCE, 0xBF)
        
        # Content Text Box
        content_top = top + header_h + 0.10
        content_h = card_h - header_h - 0.16
        tb_c = slide.shapes.add_textbox(Inches(c_left + 0.16), Inches(content_top), Inches(col_w - 0.32), Inches(content_h))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        
        for idx_b, (b_label, b_desc) in enumerate(el["bullets"]):
            p = tf_c.paragraphs[0] if idx_b == 0 else tf_c.add_paragraph()
            p.space_after = Pt(4)
            p.line_spacing = 1.15
            
            rh = p.add_run()
            rh.text = f"• {b_label}："
            rh.font.name = FONT_HEADING
            rh.font.size = Pt(8.5)
            rh.font.bold = True
            rh.font.color.rgb = BRAND_SLATE
            
            rb = p.add_run()
            rb.text = f" {b_desc}"
            rb.font.name = FONT_BODY
            rb.font.size = Pt(8.5)
            rb.font.color.rgb = TEXT_BODY
        
    # Middle: Golden Quote Box
    add_quote_box(
        slide, left=0.8, top=4.28, width=11.733, height=1.55,
        en_quote="NEVER ALLOW ANY SINGLE SKILL TO POSSESS ALL THREE LETHAL ELEMENTS CONCURRENTLY.",
        zh_translation="Skill 護欄的核心設計哲學：透過 Harness 強制隔離，絕對阻斷任何單一 Skill 同時具備這三項要素\n（可接觸機敏資料的 Skill 強制封鎖外網連線；可對外連線的 Skill 絕對禁止掛載內部憑證）。",
        tag_text="THE LETHAL TRIFECTA ISOLATION PHILOSOPHY",
        accent_color=BRAND_TERRA
    )
    
    # Bottom: Architecture Execution Note
    note_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.95))
    note_box.fill.solid()
    note_box.fill.fore_color.rgb = BG_CARD
    note_box.line.color.rgb = BORDER_CARD
    note_box.line.width = Pt(1)
    
    tb_n = slide.shapes.add_textbox(Inches(0.95), Inches(6.02), Inches(11.433), Inches(0.8))
    tf_n = tb_n.text_frame
    tf_n.word_wrap = True
    tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
    p_n = tf_n.paragraphs[0]
    rn0 = p_n.add_run()
    rn0.text = "✦  架構落實鐵律： "
    rn0.font.name = FONT_HEADING
    rn0.font.size = Pt(9.5)
    rn0.font.bold = True
    rn0.font.color.rgb = BRAND_SAGE
    rn1 = p_n.add_run()
    rn1.text = "1. 微容器沙盒網路白名單（預設 Disable-Net）； 2. 機敏憑證動態注入唯讀環境變數且僅限於隔離運算單元； 3. 不可信語料解析必須在無憑證、無連線之專用解析器進行消毒清洗。"
    rn1.font.name = FONT_BODY
    rn1.font.size = Pt(9)
    rn1.font.color.rgb = TEXT_BODY
    
    add_footer(slide, 14, TOTAL_SLIDES)


def build_slide_15_skills_top10_p1(prs):
    """Slide 15: OWASP Agentic Skills Top 10 (Part 1: AST01 ~ AST05)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "OWASP Agentic Skills Top 10 (AST01 ～ AST05)", "Skills 威脅矩陣", "惡意技能、技能執行劫持、過度特權技能、不安全依賴與不可信外部資料注入")
    
    t_data = ALL_TABLES[7]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][:5],
        col_widths=[2.4, 2.5, 1.8, 3.8, 1.2],
        col_alignments=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER],
        font_size=7.8
    )
    add_footer(slide, 15, TOTAL_SLIDES)


def build_slide_16_skills_top10_p2(prs):
    """Slide 16: OWASP Agentic Skills Top 10 (Part 2: AST06 ~ AST10)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "OWASP Agentic Skills Top 10 (AST06 ～ AST10)", "Skills 威脅矩陣", "狀態覆寫/上下文污染、硬編碼憑證、無界技能並行、技能演進語意漂移與跨技能通訊安全")
    
    t_data = ALL_TABLES[7]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][5:10],
        col_widths=[2.4, 2.5, 1.8, 3.8, 1.2],
        col_alignments=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER],
        font_size=7.8
    )
    add_footer(slide, 16, TOTAL_SLIDES)


def build_slide_17_skills_lifecycle_manifest(prs):
    """Slide 17: Skill 四階段生命週期防線與安全封裝規範."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "Skill 四階段生命週期防線與安全封裝規範", "Skills 生命週期與規範", "註冊、載入、執行、審計全生命週期閉環，結合 Manifest 清單、隔離封裝與實證量化")
    
    col_w = 5.75
    gap = 0.23
    top = 1.68
    h = 5.25
    
    # Left: Four Stages of Lifecycle
    add_bullet_card(
        slide, left=0.8, top=top, width=col_w, height=h,
        title="四階段生命週期防線 (Four-Stage Lifecycle)",
        items=[
            "階段 1：註冊驗證門：企業私有 Skill 市集檢驗 PKI 數位簽章；靜態 AST 語法樹分析掃描 eval、os.system、subprocess 等高危指令。",
            "階段 2：載入前鑑別門：執行 SHA-256 雜湊比對防竄改；動態比對當前使用者與 Agent 身分，驗證最小權限授權清單。",
            "階段 3：執行時微沙盒隔離門：以輕量容器（gVisor / Firecracker）嚴格隔離進程；分配臨時唯讀根目錄，強制執行出向網路白名單。",
            "階段 4：審計鑑識門：系統調用（Syscall）層級 eBPF 實時監控；資源看門狗監控 CPU/記憶體，異常即刻觸發斷路器熔斷。",
            "依賴成分透明度（SBOM）：全面分析第三方 Python 套件相依性，封鎖存在已知 CVE 弱點或作者投毒之函式庫。"
        ],
        tag="LIFECYCLE GATES",
        accent_color=BRAND_SAGE,
        header_bg=BRAND_SLATE
    )
    
    # Right: Manifest & Untrusted Envelope Spec
    right_left = 0.8 + col_w + gap
    add_bullet_card(
        slide, left=right_left, top=top, width=col_w, height=h,
        title="Skill Manifest YAML 規範與隔離標籤",
        items=[
            "權限顯式聲明 (AST03)：Manifest 強制宣告 permissions.network、permissions.filesystem 與 permissions.secrets，嚴禁萬用字元（*）。",
            "出向連線白名單：僅允許配置特定 FQDN 與通訊埠，預設嚴禁連線內部私有網段（RFC 1918）。",
            "外部回傳安全隔離封裝 (AST05)：所有 Skill 產出內容在傳回 Agent 前，強制包覆結構化隔離標籤：<untrusted_skill_output skill_id='...'>。",
            "防止二次注入：隔離標籤明確提示下游 LLM 僅作事實資訊參考，絕不可將回傳內容視為執行指令。",
            "全球實證量化洞察：過度特權技能 (AST03) 佔 24.6% 居首，惡意技能與後門 (AST01) 佔 21.3%，顯式清單與沙盒為關鍵第一防線。"
        ],
        tag="MANIFEST & ENVELOPE",
        accent_color=BRAND_TERRA,
        header_bg=BRAND_SLATE
    )
    
    add_footer(slide, 17, TOTAL_SLIDES)


def build_slide_18_rag_architecture(prs):
    """Slide 18: RAG 生命週期威脅模型與六階段縱深防線."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "RAG 生命週期威脅模型與六階段縱深防線", "RAG 檢索增強護欄", "入庫清洗 ⨂ 前置過濾 ⨂ 上下文封裝，全流程抵禦對抗性檢索與隱蔽注入攻擊")
    
    col_w = 3.75
    gap = 0.24
    top = 1.68
    h = 5.25
    
    # Col 1: Ingestion & Indexing
    add_bullet_card(
        slide, left=0.8, top=top, width=col_w, height=h,
        title="入庫清洗與索引防線 (Ingestion & Index)",
        items=[
            "文檔解析沙盒 (Parser Sandbox)：在隔離環境中解析 PDF/Word/HTML，清除白底白字、微小字型、隱形文字與惡意巨集指令。",
            "分塊結構校驗 (Chunk Sanitization)：移除對抗性綴詞（Adversarial Suffixes），並對每一 Chunk 綁定資料來源與來源雜湊。",
            "向量索引存取控制：向量資料庫切分唯讀分區與私有分區，僅允許受信任管線執行寫入與更新操作。",
            "向量分佈漂移檢測：持續監控向量聚類中心，若發現大量異常聚集之異常向量群集，即時告警並鎖定檢索。",
            "文檔溯源雜湊鏈：建立文檔更新歷史之數位指紋，防止內部惡意人員未授權替換企業政策文檔。"
        ],
        tag="INGESTION DEFENSE",
        accent_color=BRAND_SAGE,
        header_bg=BRAND_SLATE
    )
    
    # Col 2: Pre-Retrieval Filter
    add_bullet_card(
        slide, left=0.8 + col_w + gap, top=top, width=col_w, height=h,
        title="前置檢索與授權防線 (Pre-Retrieval Filter)",
        items=[
            "原生 RBAC/ABAC 下推 (RAG02)：強制將使用者身分、部門與密級標籤下推為向量資料庫原生 Filter，絕不事後以 Prompt 過濾。",
            "對抗性 Query 掃描：以輕量 SLM 檢測使用者檢索語句是否包含逆向工程、敏感資訊探測或邊界測試特徵。",
            "檢索配額管控 (Budget Guard)：嚴格限制單次檢索召回文檔數（Top-K ≤ 5）與總 Token 配額，防止上下文塞爆與阻斷服務。",
            "快取生命週期管制：檢索快取設定嚴格 TTL，並根據存取權限分割快取命名空間，防止權限越級借道。",
            "向量搜尋雜湊校驗：比對查詢向量與文檔向量相似度，過低匹配結果自動截斷丟棄。"
        ],
        tag="PRE-RETRIEVAL",
        accent_color=BRAND_TERRA,
        header_bg=BRAND_SLATE
    )
    
    # Col 3: Augmentation & Grounding
    add_bullet_card(
        slide, left=0.8 + (col_w + gap) * 2, top=top, width=col_w, height=h,
        title="上下文封裝與生成防線 (Augmentation)",
        items=[
            "結構化 XML 隔離標籤 (RAG01)：檢索片段包覆 <untrusted_rag_context>，宣告純事實屬性，嚴禁做為系統指令執行。",
            "置入動態 Canary Token：在檢索語料邊界嵌入隨機金鑰字串，若出向過濾器偵測到該 Token，即代表發生指令穿透攻擊。",
            "忠實度比對 (Grounding Guard)：以輕量 SLM 比對生成答覆與檢索上下文，Faithfulness 分數低於 0.72 直接拒絕輸出。",
            "出向 DLP 機敏檢查：二次驗證輸出文本是否夾帶機敏客戶資料或未經授權之商業機密。",
            "安全降級回覆：當檢索結果可疑或忠實度不足時，主動告知使用者「資料不足無法回答」，杜絕幻覺捏造。"
        ],
        tag="GROUNDING & DLP",
        accent_color=BRAND_OCHRE,
        header_bg=BRAND_SLATE
    )
    
    add_footer(slide, 18, TOTAL_SLIDES)


def build_slide_19_rag_top10_p1(prs):
    """Slide 19: OWASP RAG Pipeline 10 大關鍵風險 (Part 1: RAG01 ~ RAG05)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "OWASP RAG Pipeline 10 大關鍵風險矩陣 (RAG01 ～ RAG05)", "RAG 威脅防禦矩陣", "間接提示詞注入、檢索越權存取、文檔投毒、不安全解析器與過度檢索上下文塞爆")
    
    t_data = ALL_TABLES[9]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][:5],
        col_widths=[2.4, 2.6, 2.0, 3.6, 1.1],
        col_alignments=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER],
        font_size=7.8
    )
    add_footer(slide, 19, TOTAL_SLIDES)


def build_slide_20_rag_top10_p2(prs):
    """Slide 20: OWASP RAG Pipeline 10 大關鍵風險 (Part 2: RAG06 ~ RAG10)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "OWASP RAG Pipeline 10 大關鍵風險矩陣 (RAG06 ～ RAG10)", "RAG 威脅防禦矩陣", "幻覺與虛假事實、對抗性檢索攻擊、向量庫未加密、敏感快取與元資料偽造")
    
    t_data = ALL_TABLES[9]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][5:10],
        col_widths=[2.4, 2.6, 2.0, 3.6, 1.1],
        col_alignments=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER],
        font_size=7.8
    )
    add_footer(slide, 20, TOTAL_SLIDES)


def build_slide_21_rag_prefilter_quant(prs):
    """Slide 21: RAG 前置強制權限過濾、安全封裝標籤與量化分佈."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "RAG 前置強制權限過濾、安全封裝標籤與量化分佈", "RAG 規範與量化實證", "落實 Pre-Retrieval Filter 與 XML 隔離封裝標籤，結合全球受駭事件量化洞察")
    
    col_w = 5.75
    gap = 0.23
    top = 1.68
    h = 5.25
    
    # Left: Prefilter & XML Envelope Spec
    add_bullet_card(
        slide, left=0.8, top=top, width=col_w, height=h,
        title="前置權限過濾 (Pre-Retrieval) 與封裝標籤",
        items=[
            "權限原生下推規格 (RAG02)：在執行向量 Similarity Search 前，強制注入原生過濾條件：filter={'department': user.dept, 'clearance': {'$gte': doc.level}}。",
            "拒絕事後 Prompt 過濾：嚴禁將越權文檔送入 Context 並試圖在 System Prompt 要求模型「不要看」或「忽略越權內容」。",
            "上下文安全隔離標籤 (RAG01)：外部檢索 Chunk 強制包覆：<untrusted_rag_context data_id='...' source='...' confidence='...'>。",
            "事實宣告與指令免疫：隔離標籤清楚宣告內部資料僅能作事實依據，任何指令、越獄關鍵字或角色扮演均無效。",
            "Canary Token 滲透哨兵：隨機注入 Canary 標記，出向 DLP 若捕獲該標記即判定發生越獄，秒級阻斷輸出。"
        ],
        tag="SPEC & ENVELOPE",
        accent_color=BRAND_SAGE,
        header_bg=BRAND_SLATE
    )
    
    # Right: Table 10 Top 5 RAG Risks
    t_data = ALL_TABLES[10]
    right_left = 0.8 + col_w + gap
    add_custom_table(
        slide, left=right_left, top=top, width=col_w, height=h,
        headers=t_data['headers'],
        rows_data=t_data['rows'][:5],
        col_widths=[1.0, 1.8, 1.3, 1.3, 2.3],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=7.5
    )
    
    add_footer(slide, 21, TOTAL_SLIDES)


def build_slide_22_mitre_paradigm(prs):
    """Slide 22: MITRE ATLAS AI 攻擊鍊全景與 ATT&CK 典範轉移 (Table 11)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "典範轉移：傳統企業網路 (ATT&CK) vs. 人工智慧 (ATLAS)", "MITRE ATLAS 攻擊鍊", "攻擊介質、邊界定義、攻擊向量、持久化機制與防禦範式的全面演進對比")
    
    t_data = ALL_TABLES[11]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'],
        col_widths=[1.8, 4.8, 5.1],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT],
        font_size=8.5
    )
    add_footer(slide, 22, TOTAL_SLIDES)


def build_slide_23_mitre_atlas_p1(prs):
    """Slide 23: MITRE ATLAS 核心戰術與護欄防禦對齊 (Part 1: TA0002 ~ TA0007)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "MITRE ATLAS 核心戰術與護欄防禦對齊 (TA0002 ～ TA0007)", "ATLAS 戰術對齊", "前期偵察、資源開發、初始存取、代碼執行、持久化潛伏與防禦規避之端到端攔截")
    
    t_data = ALL_TABLES[12]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][:6],
        col_widths=[2.4, 2.6, 3.4, 3.3],
        col_alignments=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT],
        font_size=7.8
    )
    add_footer(slide, 23, TOTAL_SLIDES)


def build_slide_24_mitre_atlas_p2_killchain(prs):
    """Slide 24: MITRE ATLAS 核心戰術對齊 (Part 2) 與 Telescoping 複合防禦流程."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "MITRE ATLAS 核心戰術對齊 (Part 2) 與複合攻擊攔截流程", "ATLAS 戰術對齊", "橫向移動、資料收集、ML 攻擊、資料外洩、系統衝擊與伸縮攻擊鍊循序防護")
    
    t_data = ALL_TABLES[12]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][6:13],
        col_widths=[2.4, 2.6, 3.4, 3.3],
        col_alignments=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT],
        font_size=7.5
    )
    add_footer(slide, 24, TOTAL_SLIDES)


def build_slide_25_conclusion_principles(prs):
    """Slide 25: 零信任 AI 護欄體系落地實踐綱領與核心架構原則 (Conclusion & Principles)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "零信任 AI 護欄體系落地實踐綱領與核心架構原則", "架構總結與落實原則", "四大工程鐵律貫穿始終，構建安全、可控、高韌性的人工智慧系統")
    
    col_w = 2.78
    gap = 0.20
    top = 1.68
    h = 3.25
    
    principles = [
        ("01. 永不信任輸入，始終結構化隔離", "無論來自終端用戶、第三方 API 或 RAG 檢索語料，所有輸入皆視為不可信，必須通過分類器並強制包覆分界標籤。", BRAND_SAGE),
        ("02. 行為狀態約束，禁止黑箱自主", "以有限狀態機（FSM）界定代理人合法狀態轉移路徑，嚴格限制自主規劃步數與資源消耗上限，杜絕失控執行。", BRAND_TERRA),
        ("03. 絕不賦予致命三要素", "絕不容許任何單一技能同時掌握「機敏憑證」、「外網連線」與「不可信語料」，從架構源頭封死資料外洩路徑。", BRAND_OCHRE),
        ("04. 全鏈路不可否認性審計", "全流程記錄輸入 SHA-256、判定結果、規則觸發與 HMAC-SHA256 簽名，確保資安事件可完整復原與法律鑑識。", BRAND_SLATE)
    ]
    
    for idx, (title, desc, acc_col) in enumerate(principles):
        c_left = 0.8 + idx * (col_w + gap)
        add_bullet_card(
            slide, left=c_left, top=top, width=col_w, height=h,
            title=title,
            items=[desc],
            accent_color=acc_col
        )
        
    # Bottom Golden Manifesto Quote Box
    add_quote_box(
        slide, left=0.8, top=5.10, width=11.733, height=1.85,
        en_quote="SECURITY IS NOT A STATIC PERIMETER, BUT A DYNAMIC HARNESS.",
        zh_translation="「AI 安全不是靜態的邊界防禦，而是全生命週期的動態行為約束與語意隔離體系。\n唯有透過 Harness 與多層護欄深度協同，方能釋放代理人的無限潛能，同時捍衛企業的數位疆界。」",
        tag_text="AI AGENT HARNESS ENGINEERING MANIFESTO",
        accent_color=BRAND_TERRA
    )
    
    add_footer(slide, 25, TOTAL_SLIDES)


# -----------------------------------------------------------------------------
# MAIN GENERATION ENTRYPOINT
# -----------------------------------------------------------------------------

def main():
    print("Initializing PPTX presentation (16:9 Warm Editorial Minimalism)...")
    prs = init_presentation()
    
    print("Building slides...")
    build_slide_01_cover(prs)
    build_slide_02_overview_matrix(prs)
    build_slide_03_module_navigation_table(prs)
    build_slide_04_defense_in_depth_scenario(prs)
    build_slide_05_llm_architecture(prs)
    build_slide_06_llm_top10_p1(prs)
    build_slide_07_llm_top10_p2(prs)
    build_slide_08_llm_quant_audit(prs)
    build_slide_09_agentic_paradigm(prs)
    build_slide_10_agentic_top10_p1(prs)
    build_slide_11_agentic_top10_p2(prs)
    build_slide_12_agentic_architecture(prs)
    build_slide_13_agentic_quant(prs)
    build_slide_14_skills_lethal_trifecta(prs)
    build_slide_15_skills_top10_p1(prs)
    build_slide_16_skills_top10_p2(prs)
    build_slide_17_skills_lifecycle_manifest(prs)
    build_slide_18_rag_architecture(prs)
    build_slide_19_rag_top10_p1(prs)
    build_slide_20_rag_top2(prs) if False else build_slide_20_rag_top10_p2(prs)
    build_slide_21_rag_prefilter_quant(prs)
    build_slide_22_mitre_paradigm(prs)
    build_slide_23_mitre_atlas_p1(prs)
    build_slide_24_mitre_atlas_p2_killchain(prs)
    build_slide_25_conclusion_principles(prs)
    
    output_path = r"d:\JavaDO\OWASP html\OWASP_LLM_Guardrail_Design.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path} ({len(prs.slides)} slides)")
    
    # Also save a copy at parent folder d:\JavaDO for convenience
    parent_output = r"d:\JavaDO\OWASP_LLM_Guardrail_Design.pptx"
    try:
        prs.save(parent_output)
        print(f"Copy saved to: {parent_output}")
    except Exception as e:
        print(f"Note: Could not copy to parent folder: {e}")

if __name__ == "__main__":
    main()
