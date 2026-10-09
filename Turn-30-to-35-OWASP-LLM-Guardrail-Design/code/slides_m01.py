"""
Module 01 Slides (07 ~ 14): OWASP Top 10 for LLM Guardrail Design
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
    add_code_box,
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


def build_slide_07_llm_architecture(prs):
    """Slide 07: LLM 雙向過濾管線架構與三大核心處理管線."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "LLM 基礎模型護欄架構全景與三大核心處理管線", "LLM 基礎模型護欄", "入向檢驗、執行時保護與出向過濾的單一出入口雙向閉環防禦")
    
    col_w = 3.75
    gap = 0.24
    top = 1.68
    h = 5.25
    
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
    
    add_footer(slide, 7, TOTAL_SLIDES)


def build_slide_08_llm_sequence_flow(prs):
    """Slide 08: 護欄服務架構全景與循序資料流 (Mermaid 2)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "護欄服務架構全景與端到端循序資料流圖", "LLM 循序流程", "請求入向消毒、快取命中、LLM 推論、工具審查、出向 DLP 與審計日誌全鏈路 (Mermaid 2 對齊)")
    
    steps = [
        (1, "使用者下達提示詞", "User ➔ Agent", "PROMPT REQUEST", [
            "請求參數：傳入 Raw Prompt 與會話 Token。",
            "安全起點：請求經由單一入口接入，尚未進入推論環境。"
        ], BRAND_SLATE),
        (2, "入向檢驗與脫敏", "Agent ➔ Guardrail", "INBOUND FILTER", [
            "入向檢驗：Llama-Guard / 特徵匹配評估 Jailbreak 評分。",
            "處置：PII 遮罩、XML 邊界隔離、驗證 DISA IL 密級標籤。"
        ], BRAND_SAGE),
        (3, "語意快取查驗", "Guardrail ➔ Cache", "CACHE LOOKUP", [
            "向量相似度比對：檢查是否有安全的高信度快取答覆。",
            "快取防投毒：僅允許白名單簽章之答案命中，命中即刻返回。"
        ], BRAND_TERRA),
        (4, "安全推論與工具審查", "Agent ➔ LLM / Tool", "RUNTIME INFERENCE", [
            "推論執行：提交消過毒之組合 Prompt 至 LLM 核心。",
            "工具審查：若觸發 Tool Call，經由護欄驗證參數與 HITL 門檻。"
        ], BRAND_OCHRE),
        (5, "出向檢驗與 DLP 防護", "LLM ➔ Guardrail", "OUTBOUND DLP", [
            "出向檢驗：掃描系統提示詞外洩、出向 DLP、XSS 編碼。",
            "忠實度查核：SLM 進行事實性 NLI 比對，杜絕模型胡謅。"
        ], BRAND_SAGE),
        (6, "安全回覆與審計寫入", "Guardrail ➔ User / Audit", "AUDIT & DELIVER", [
            "交付用戶：合規放行完整輸出，異常時替換為安全提示。",
            "審計寫入：8 大欄位經 HMAC-SHA256 簽署後寫入 SOC。"
        ], BRAND_SLATE)
    ]
    
    add_sequence_step_grid(slide, steps, top=1.68)
    add_footer(slide, 8, TOTAL_SLIDES)


def build_slide_09_llm_top10_p1(prs):
    """Slide 09: OWASP Top 10 for LLM 防禦矩陣 (Part 1: LLM01 ~ LLM05)."""
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
    add_footer(slide, 9, TOTAL_SLIDES)


def build_slide_10_llm_top10_p2(prs):
    """Slide 10: OWASP Top 10 for LLM 防禦矩陣 (Part 2: LLM06 ~ LLM10)."""
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
    add_footer(slide, 10, TOTAL_SLIDES)


def build_slide_11_llm_quant_p1(prs):
    """Slide 11: 全球 10 大 LLM 風險發生量化比例與實證分佈 (Part 1: Top 1~5)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "全球 10 大 LLM 風險發生量化比例與實證分佈 (Part 1)", "LLM 量化實證分析", "分析真實公開受駭事件 (n=6,639) 與企業網關遙測數據，揭示防禦可見性悖論 (LLM01~05)")
    
    t_data = ALL_TABLES[3]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][:5],
        col_widths=[1.0, 2.4, 2.0, 2.0, 4.3],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=8.0
    )
    add_footer(slide, 11, TOTAL_SLIDES)


def build_slide_12_llm_quant_p2(prs):
    """Slide 12: 全球 10 大 LLM 風險發生量化比例與實證分佈 (Part 2: Top 6~10)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "全球 10 大 LLM 風險發生量化比例與實證分佈 (Part 2)", "LLM 量化實證分析", "過度代理、提示詞洩漏、向量弱點與無限制消耗之實證數據分析 (LLM06~10)")
    
    t_data = ALL_TABLES[3]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][5:10],
        col_widths=[1.0, 2.4, 2.0, 2.0, 4.3],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=8.0
    )
    add_footer(slide, 12, TOTAL_SLIDES)


def build_slide_13_audit_log_spec(prs):
    """Slide 13: 不可否認性審計日誌結構規格 (Pre 7: JSON 規格 + 8 大核心欄位)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "不可否認性審計日誌結構規格 (Non-Repudiation Audit Log)", "審計日誌技術規格", "8 大核心欄位規格、SHA-256 輸入雜湊指紋與 HMAC-SHA256 防竄改數位簽章 (Pre 7 對齊)")
    
    col_w = 5.75
    gap = 0.23
    top = 1.68
    h = 5.25
    
    json_text = """{
  "timestamp": "2026-09-15T20:17:20.124Z",
  "request_id": "req-9dfdbde8-b8b3-40aa-b189-85a716c14879",
  "actor": {
    "user_id": "sec_operator_01",
    "tenant_id": "dept_alpha",
    "clearance_level": "DISA_IL_4"
  },
  "guardrail_inspection": {
    "inbound": {
      "raw_prompt_hash": "e3b0c44298fc1c149afbf4c8996fb...",
      "sanitized_prompt": "請協助分析 [REDACTED_IP] 異常...",
      "jailbreak_score": 0.02,
      "disa_tag_verified": true,
      "status": "PASS"
    },
    "outbound": {
      "token_usage": { "prompt": 128, "completion": 45 },
      "pii_detected": false,
      "dlp_rule_matched": null,
      "faithfulness_score": 0.94,
      "status": "PASS"
    }
  },
  "signature": "HMAC-SHA256:7f83b1657ff1fc53b92dc181..."
}"""
    
    # Left: Code Box
    add_code_box(slide, left=0.8, top=top, width=col_w, height=h, code_text=json_text, title="審計日誌 JSON 結構範例 (Audit Schema)", lang="JSON")
    
    # Right: 8 Key Fields Explanation
    right_left = 0.8 + col_w + gap
    add_bullet_card(
        slide, left=right_left, top=top, width=col_w, height=h,
        title="審計日誌 8 大關鍵欄位工程定義",
        items=[
            "timestamp：高精度 ISO-8601 毫秒時間戳記，提供時序溯源依據。",
            "request_id / trace_id：分散式追蹤識別碼，串聯閘道、推論與工具鏈。",
            "actor (client_identity)：呼叫方使用者識別、租戶 ID 與 DISA IL 密級標籤。",
            "raw_prompt_hash：原始 Prompt 之 SHA-256 數位指紋，確保原始請求不可否認。",
            "sanitized_prompt：經 PII 遮罩與邊界隔離後之清洗文字，保留比對軌跡。",
            "guardrail_verdict：護欄決策結果（PASS / SANITIZED / BLOCKED）。",
            "rule_metrics：越獄評分 (Jailbreak Score) 與事實忠實度評分 (Faithfulness)。",
            "signature：整筆日誌以私鑰計算之 HMAC-SHA256 簽名，杜絕事後篡改日誌。"
        ],
        tag="FIELD SPECIFICATIONS",
        accent_color=BRAND_SAGE,
        header_bg=BRAND_SLATE
    )
    
    add_footer(slide, 13, TOTAL_SLIDES)


def build_slide_14_llm_tech_stack(prs):
    """Slide 14: LLM 護欄工程落地建議與主流技術選型."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "LLM 護欄工程落地建議與主流技術選型矩陣", "工程落地與技術選型", "語意邊界、機敏脫敏、越獄分類與結構化防護的開源與企業級最佳實踐組合")
    
    col_w = 2.78
    gap = 0.20
    top = 1.68
    h = 5.25
    
    techs = [
        ("01", "NeMo Guardrails", "NVIDIA 開源對話護欄", BRAND_SLATE, [
            "核心定位：基於 Colang 的語意路由與可控對話流引擎。",
            "防護重心：入向話題導引、執行時流程約束與自定義對話防禦。",
            "優勢：高度靈活之語意 Programmable Guardrails，支援多模型串接。",
            "建議場景：企業級客服機器人與特定主題限制任務。"
        ]),
        ("02", "Microsoft Presidio", "微軟機敏實體脫敏引擎", BRAND_SAGE, [
            "核心定位：高效能機敏資料 (PII) 識別、分析與動態遮罩工具包。",
            "防護重心：身分證號、信用卡、電子郵件、電話、自定義機密實體。",
            "優勢：結合 NER 命名實體識別與正則表達式，多語言支援佳。",
            "建議場景：出入向 PII 動態匿名化與資料合規落地。"
        ]),
        ("03", "Meta Llama-Guard 3", "輕量安全審查模型", BRAND_TERRA, [
            "核心定位：專為 AI 安全對齊訓練之輕量化審查分類器 (8B / 1B)。",
            "防護重心：越獄模式偵測、仇恨言論、違法行為、自殘與暴力指引。",
            "優勢：基於 MLPerf 推論架構，延遲極低 (<50ms)，準確率高。",
            "建議場景：第一道入向 Prompt 快速安全二分類。"
        ]),
        ("04", "Guardrails AI", "結構化驗證與型別安全", BRAND_OCHRE, [
            "核心定位：輸出結構約束與 Pydantic 型別防禦中介軟體。",
            "防護重心：不安全代碼輸出、SQL 注入、XSS 載荷、格式畸形。",
            "優勢：支援自定義 Validator 鏈，提供即時自動修復 (Reask) 能力。",
            "建議場景：代理人結構化 JSON / Tool Arguments 輸出校驗。"
        ])
    ]
    
    for idx, (num, name, role, color, bullets) in enumerate(techs):
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

    add_footer(slide, 14, TOTAL_SLIDES)
