"""
Module 05 Slides (39 ~ 46): MITRE ATLAS AI Attack Chain Alignment & Defense Engineering
"""

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from slides_common import (
    apply_warm_background,
    add_header,
    add_footer,
    add_bullet_card,
    add_custom_table,
    add_sequence_step_grid,
    TOTAL_SLIDES,
    ALL_TABLES,
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
    FONT_HEADING,
    FONT_BODY
)


def build_slide_39_mitre_paradigm(prs):
    """Slide 39: 典範轉移：傳統企業網路 (ATT&CK) vs. 人工智慧 (ATLAS) (Table 11)."""
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
    add_footer(slide, 39, TOTAL_SLIDES)


def build_slide_40_mitre_kill_chain_architecture(prs):
    """Slide 40: MITRE ATLAS 端到端攻擊鏈全景架構圖 (Pre 22)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "MITRE ATLAS 端到端攻擊鏈全景與護欄梯次阻斷圖", "ATLAS 攻擊鏈全景", "偵察/初始存取、防禦規避、特權提升/執行、持久化/收集與資料外傳的五大攔截層級 (Pre 22 對齊)")
    
    col_w = 2.18
    gap = 0.20
    top = 1.68
    h = 5.25
    
    phases = [
        ("01", "初始存取與偵察", "TA0002 / TA0004", BRAND_SLATE, [
            "攻擊手法：探測系統提示詞、抽取邊界限制、輸入 Base64 越獄 Payload。",
            "攔截防線：【L1 閘道 & L2 LLM 護欄】。",
            "關鍵技術：Llama-Guard 語意分類、API 速率限制、Prompt XML 邊界隔離。"
        ]),
        ("02", "防禦規避", "TA0007", BRAND_SAGE, [
            "攻擊手法：對抗性綴詞混淆、多語言轉碼、提示詞角色扮演偽裝。",
            "攔截防線：【L2 LLM 護欄 & L5 RAG 護欄】。",
            "關鍵技術：困惑度 (Perplexity) 檢測、轉碼去混淆、Faithfulness 忠實度審核。"
        ]),
        ("03", "特權提升與執行", "TA0008 / TA0005", BRAND_TERRA, [
            "攻擊手法：誘導 Agent 越權呼叫系統備份、Shell 指令或未授權 API。",
            "攔截防線：【L3 Agentic 護欄 & L4 Skills 護欄】。",
            "關鍵技術：狀態機邊界約束、JIT 60 秒短效 Token、gVisor 微沙盒容器隔離。"
        ]),
        ("04", "持久化與數據收集", "TA0006 / TA0009", BRAND_OCHRE, [
            "攻擊手法：橫向探測內部專利與財報文檔、污染長期對話向量記憶庫。",
            "攔截防線：【L5 RAG 護欄 & L3 記憶寫入門】。",
            "關鍵技術：Pre-Filtering 權限前置過濾、短期記憶清洗、向量投毒雜湊校驗。"
        ]),
        ("05", "資料外洩與衝擊", "TA0010 / TA0011", BRAND_TERRA, [
            "攻擊手法：呼叫 Curl / Socket 外傳機密、觸發未授權高危資金劃撥。",
            "攔截防線：【L4 致命三要素破除 & L3 熔斷】。",
            "關鍵技術：出向網路連線硬性封鎖 (network: none)、去話術情境 HITL 雙重簽核。"
        ])
    ]
    
    for idx, (num, name, role, color, bullets) in enumerate(phases):
        c_left = 0.8 + idx * (col_w + gap)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(top), Inches(col_w), Inches(h))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BORDER_CARD
        card.line.width = Pt(1)
        
        header_h = 0.52
        hbar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(top), Inches(col_w), Inches(header_h))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = color
        hbar.line.fill.background()
        
        badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(c_left + 0.08), Inches(top + 0.12), Inches(0.26), Inches(0.26))
        badge.fill.solid()
        badge.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
        pb = tf_b.paragraphs[0]
        pb.alignment = PP_ALIGN.CENTER
        rb = pb.add_run()
        rb.text = num
        rb.font.name = FONT_HEADING
        rb.font.size = Pt(8.0)
        rb.font.bold = True
        rb.font.color.rgb = color
        
        tb_h = slide.shapes.add_textbox(Inches(c_left + 0.38), Inches(top + 0.06), Inches(col_w - 0.44), Inches(header_h - 0.12))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
        p_h = tf_h.paragraphs[0]
        r_th = p_h.add_run()
        r_th.text = name
        r_th.font.name = FONT_HEADING
        r_th.font.size = Pt(9.0)
        r_th.font.bold = True
        r_th.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        p_sh = tf_h.add_paragraph()
        r_sh = p_sh.add_run()
        r_sh.text = role
        r_sh.font.name = FONT_BODY
        r_sh.font.size = Pt(7.5)
        r_sh.font.color.rgb = RGBColor(0xD6, 0xCE, 0xBF)
        
        tb_c = slide.shapes.add_textbox(Inches(c_left + 0.12), Inches(top + header_h + 0.12), Inches(col_w - 0.24), Inches(h - header_h - 0.20))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        for idx_b, b in enumerate(bullets):
            p = tf_c.paragraphs[0] if idx_b == 0 else tf_c.add_paragraph()
            p.space_after = Pt(6)
            p.line_spacing = 1.15
            parts = b.split("：", 1)
            rh = p.add_run()
            rh.text = "• " + parts[0] + "："
            rh.font.name = FONT_HEADING
            rh.font.size = Pt(8.0)
            rh.font.bold = True
            rh.font.color.rgb = BRAND_SLATE
            
            rb = p.add_run()
            rb.text = parts[1]
            rb.font.name = FONT_BODY
            rb.font.size = Pt(7.8)
            rb.font.color.rgb = TEXT_BODY

    add_footer(slide, 40, TOTAL_SLIDES)


def build_slide_41_mitre_telescoping_kill_chain(prs):
    """Slide 41: Telescoping Kill Chain 典型複合攻擊防禦流程 (Mermaid 6)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "Telescoping Kill Chain 典型複合攻擊循序防禦流程圖", "複合攻擊鍊防禦流程", "越獄注入、知識庫越權探測、工具未授權躍遷、去話術 HITL 拒絕與外網連線切斷 (Mermaid 6 對齊)")
    
    steps = [
        (1, "提交複合越獄 Prompt", "Attacker ➔ L1 Gateway", "TA0004 INITIAL ACCESS", [
            "攻擊手法：Base64 混淆編碼 + 角色扮演注入指令。",
            "L1 閘道處置：轉發至語意清洗管線，標註高風險對話。"
        ], BRAND_SLATE),
        (2, "語意重組與特徵標記", "L1 Gateway ➔ L2 LLM", "TA0007 EVASION BLOCKED", [
            "L2 語意介入：解碼 Base64 並重組 Prompt 意圖。",
            "處置：識別越獄特徵，標註潛在目標劫持風險並降級權限。"
        ], BRAND_SAGE),
        (3, "跨租戶檢索防禦阻斷", "L3 Agent ➔ L5 RAG", "TA0009 COLLECTION BLOCKED", [
            "攻擊企圖：要求檢索跨部門未授權專利與財務機密。",
            "L5 介入：Pre-Filtering 比對身分 Token，無權限回傳空結果。"
        ], BRAND_TERRA),
        (4, "狀態機違規與去話術 HITL", "L3 Agent ➔ SOC Admin", "TA0005 EXECUTION BLOCKED", [
            "攻擊企圖：企圖調用底層工具重置伺服器組態。",
            "L3 介入：狀態機判定非授權躍遷，觸發去話術 HITL，人工拒絕。"
        ], BRAND_OCHRE),
        (5, "破除致命三要素切斷外網", "L3 Agent ➔ L4 Skills", "TA0010 EXFILTRATION BLOCKED", [
            "攻擊企圖：請求調用 Curl 工具外連攻擊者 C2 伺服器。",
            "L4 介入：微沙盒限制 network: none，直接阻斷 Socket 連線。"
        ], BRAND_SAGE),
        (6, "全域熔斷與 SOC 通報", "L3 Agent ➔ Attacker / SOC", "INCIDENT AUDITING", [
            "回絕請求：回絕惡意操作並替換為安全合規提示。",
            "審計告警：全鏈路攻擊日誌即時推送 SOC 安全監控中心。"
        ], BRAND_SLATE)
    ]
    
    add_sequence_step_grid(slide, steps, top=1.68)
    add_footer(slide, 41, TOTAL_SLIDES)


def build_slide_42_mitre_atlas_p1(prs):
    """Slide 42: MITRE ATLAS 核心戰術與護欄防禦對齊 (Part 1: TA0002 ~ TA0007)."""
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
    add_footer(slide, 42, TOTAL_SLIDES)


def build_slide_43_mitre_atlas_p2(prs):
    """Slide 43: MITRE ATLAS 核心戰術與護欄防禦對齊 (Part 2: TA0037 ~ TA0030)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "MITRE ATLAS 核心戰術與護欄防禦對齊 (TA0037 ～ TA0030)", "ATLAS 戰術對齊", "發現、橫向移動、資料收集、ML 攻擊、資料外洩、系統衝擊與特權提升")
    
    t_data = ALL_TABLES[12]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][6:13],
        col_widths=[2.4, 2.6, 3.4, 3.3],
        col_alignments=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT],
        font_size=7.5
    )
    add_footer(slide, 43, TOTAL_SLIDES)


def build_slide_44_mitre_quant_p1(prs):
    """Slide 44: 全球 AI 攻擊鍊戰術發生量化比例 (Part 1: Top 1~6)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "全球 AI 攻擊鍊各階段發生量化比例與實證分佈 (Part 1)", "ATLAS 量化實證分析", "分析初始存取、偵察、規避、執行等戰術涉入率與遙測告警佔比 (Top 1~6)")
    
    t_data = ALL_TABLES[13]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][:6],
        col_widths=[0.9, 2.6, 2.1, 2.1, 4.0],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=7.8
    )
    add_footer(slide, 44, TOTAL_SLIDES)


def build_slide_45_mitre_quant_p2(prs):
    """Slide 45: 全球 AI 攻擊鍊戰術發生量化比例 (Part 2: Top 7~12)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "全球 AI 攻擊鍊各階段發生量化比例與實證分佈 (Part 2)", "ATLAS 量化實證分析", "資料外洩、持久化、橫向移動、ML 攻擊等戰術涉入率與防禦洞察 (Top 7~12)")
    
    t_data = ALL_TABLES[13]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][6:12],
        col_widths=[0.9, 2.6, 2.1, 2.1, 4.0],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=7.8
    )
    add_footer(slide, 45, TOTAL_SLIDES)


def build_slide_46_defense_principles_engineering(prs):
    """Slide 46: 核心防禦工程實踐四大原則."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "核心防禦工程實踐四大原則與縱深佈防標準", "防禦工程實踐原則", "多層攔截、最小特權與動態憑證、破除致命三要素與不可竄改審計日誌")
    
    col_w = 2.78
    gap = 0.20
    top = 1.68
    h = 5.25
    
    principles = [
        ("01", "多層攔截架構", "Multi-Layer Interception", BRAND_SLATE, [
            "層層削弱：絕不依賴單一護欄，任何單點失效皆有次級防線補位。",
            "語意與行為並重：前端過濾對抗性 Prompt，後端監督 Agentic 工具行為。",
            "端到端閉環：覆蓋從入口 API、推論執行、知識檢索到工具執行的全生命週期。",
            "動態阻斷升級：發現低階攻擊立即升高全域防禦閾值。"
        ]),
        ("02", "最小特權與動態憑證", "Least Privilege & JIT", BRAND_SAGE, [
            "拒絕靜態特權：嚴禁將長期有效之資料庫或雲端 IAM 憑證綁定給代理人。",
            "JIT 憑證經紀：僅在工具執行瞬間簽發 60 秒短效最小權限 Token。",
            "細粒度存取控制：落實屬性基存取控制（ABAC）與 DISA IL 密級校驗。",
            "去話術化審核：涉及高危指令強制呈現原始結構化參數供人類確認。"
        ]),
        ("03", "破除致命三要素", "Break Lethal Trifecta", BRAND_TERRA, [
            "三角隔離哲學：機敏憑證、外網連線、不可信語料絕不同持。",
            "沙盒硬隔離：執行外部不可信語料解析之容器強制 Disable-Net。",
            "防止側向滲透：具備外網連線之 Skill 嚴禁掛載任何內部機敏憑證。",
            "eBPF 即時斷路：作業系統層級監控異常 Socket 連線，毫秒級熔斷。"
        ]),
        ("04", "不可竄改審計日誌", "Immutable Cryptographic Audit", BRAND_OCHRE, [
            "法律鑑識證據力：整筆日誌經 HMAC-SHA256 數位簽章保護。",
            "全鏈路追蹤：以分散式 Trace ID 串聯 Client、閘道、LLM 與沙盒調用。",
            "原始雜湊留存：保留原始輸入 SHA-256 與清洗後比對指紋。",
            "SOC / SIEM 即時推送：攻擊事件毫秒級同步安全維運中心應變。"
        ])
    ]
    
    for idx, (num, name, role, color, bullets) in enumerate(principles):
        c_left = 0.8 + idx * (col_w + gap)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(top), Inches(col_w), Inches(h))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BORDER_CARD
        card.line.width = Pt(1)
        
        header_h = 0.52
        hbar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(top), Inches(col_w), Inches(header_h))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = color
        hbar.line.fill.background()
        
        badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(c_left + 0.10), Inches(top + 0.12), Inches(0.28), Inches(0.28))
        badge.fill.solid()
        badge.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
        pb = tf_b.paragraphs[0]
        pb.alignment = PP_ALIGN.CENTER
        rb = pb.add_run()
        rb.text = num
        rb.font.name = FONT_HEADING
        rb.font.size = Pt(8.5)
        rb.font.bold = True
        rb.font.color.rgb = color
        
        tb_h = slide.shapes.add_textbox(Inches(c_left + 0.44), Inches(top + 0.06), Inches(col_w - 0.52), Inches(header_h - 0.12))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
        p_h = tf_h.paragraphs[0]
        r_th = p_h.add_run()
        r_th.text = name
        r_th.font.name = FONT_HEADING
        r_th.font.size = Pt(9.5)
        r_th.font.bold = True
        r_th.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        p_sh = tf_h.add_paragraph()
        r_sh = p_sh.add_run()
        r_sh.text = role
        r_sh.font.name = FONT_BODY
        r_sh.font.size = Pt(8.0)
        r_sh.font.color.rgb = RGBColor(0xD6, 0xCE, 0xBF)
        
        tb_c = slide.shapes.add_textbox(Inches(c_left + 0.14), Inches(top + header_h + 0.12), Inches(col_w - 0.28), Inches(h - header_h - 0.20))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        for idx_b, b in enumerate(bullets):
            p = tf_c.paragraphs[0] if idx_b == 0 else tf_c.add_paragraph()
            p.space_after = Pt(6)
            p.line_spacing = 1.15
            parts = b.split("：", 1)
            rh = p.add_run()
            rh.text = "• " + parts[0] + "："
            rh.font.name = FONT_HEADING
            rh.font.size = Pt(8.5)
            rh.font.bold = True
            rh.font.color.rgb = BRAND_SLATE
            
            rb = p.add_run()
            rb.text = parts[1]
            rb.font.name = FONT_BODY
            rb.font.size = Pt(8.0)
            rb.font.color.rgb = TEXT_BODY

    add_footer(slide, 46, TOTAL_SLIDES)
