"""
Module 03 Slides (23 ~ 30): OWASP Agentic Skills Top 10 (AST10) & The Lethal Trifecta
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
    add_quote_box,
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


def build_slide_23_skills_lethal_trifecta(prs):
    """Slide 23: Skills 核心威脅模型：破解「致命三要素 (The Lethal Trifecta)」."""
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
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(top), Inches(col_w), Inches(card_h))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BORDER_CARD
        card.line.width = Pt(1)
        
        header_h = 0.46
        h_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(top), Inches(col_w), Inches(header_h))
        h_shape.fill.solid()
        h_shape.fill.fore_color.rgb = BRAND_SLATE
        h_shape.line.fill.background()
        
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
        
    add_quote_box(
        slide, left=0.8, top=4.28, width=11.733, height=1.55,
        en_quote="NEVER ALLOW ANY SINGLE SKILL TO POSSESS ALL THREE LETHAL ELEMENTS CONCURRENTLY.",
        zh_translation="Skill 護欄的核心設計哲學：透過 Harness 強制隔離，絕對阻斷任何單一 Skill 同時具備這三項要素\n（可接觸機敏資料的 Skill 強制封鎖外網連線；可對外連線的 Skill 絕對禁止掛載內部憑證）。",
        tag_text="THE LETHAL TRIFECTA ISOLATION PHILOSOPHY",
        accent_color=BRAND_TERRA
    )
    
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
    
    add_footer(slide, 23, TOTAL_SLIDES)


def build_slide_24_skills_lifecycle_architecture(prs):
    """Slide 24: Skill 四階段生命週期防線架構 (Pre 11)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "Skill 四階段生命週期防線架構全景圖 (Four-Stage Lifecycle)", "Skills 生命週期防線", "註冊準入、意圖發現、執行微沙盒與審計鑑識的全流程安全閉環 (Pre 11 對齊)")
    
    col_w = 2.78
    gap = 0.20
    top = 1.68
    h = 5.25
    
    stages = [
        ("01", "Phase 1: 註冊與準入", "Registration Guard", BRAND_SLATE, [
            "數位簽章查驗 (AST01)：僅允許企業內部 PKI 認證之 Skill 入庫。",
            "SBOM 相依性鎖定 (AST02)：鎖定 Python/Node.js 套件 Hash，防依賴投毒。",
            "靜態 AST 語法分析 (AST08)：掃描 eval、subprocess、os.system 敏感呼叫。",
            "權限清單最小化審查 (AST03)：逐條核定 Manifest 宣告權限。"
        ]),
        ("02", "Phase 2: 發現與意圖綁定", "Discovery Guard", BRAND_SAGE, [
            "Docstring 消毒 (AST04)：防止工具註解中夾帶攻擊指令污染 Agent 上下文。",
            "DISA 密級標籤綁定 (AST10)：將執行環境嚴格劃分不同機密等級區間。",
            "意圖衝突比對：排查是否存在多工具描述重疊導致之執行混淆。",
            "呼叫白名單核准：依據 Agent 角色指派可見工具子集。"
        ]),
        ("03", "Phase 3: 執行時沙盒隔離", "Runtime Sandbox", BRAND_TERRA, [
            "gVisor 容器沙盒 (AST06)：輕量微容器嚴格隔離作業系統系統調用。",
            "網路硬性白名單 (AST05)：禁止通配符，預設切斷非必要出向連線。",
            "唯讀暫存卷冊：使用 Ephemeral 檔案系統，進程銷毀時資料徹底抹除。",
            "環境變數隔離：禁止直接讀取宿主機環境變數與靜態金鑰。"
        ]),
        ("04", "Phase 4: 審計與行為鑑識", "Audit & Forensic Guard", BRAND_OCHRE, [
            "eBPF 系統調用審計 (AST09)：即時捕獲網路 Socket 與檔案操作軌跡。",
            "行為漂移偵測 (AST07)：監控輸入輸出 Token 與耗時，防範語意漂移。",
            "資源熔斷看門狗：CPU/記憶體消耗超標立即殺死容器執行緒。",
            "防竄改審計寫入：生成 HMAC-SHA256 簽署之安全調用日誌。"
        ])
    ]
    
    for idx, (num, name, role, color, bullets) in enumerate(stages):
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

    add_footer(slide, 24, TOTAL_SLIDES)


def build_slide_25_skills_sequence_flow(prs):
    """Slide 25: Skill 執行時循序防護流程 (Mermaid 4)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "Skill 執行時微沙盒循序防護流程圖", "Skills 循序流程", "請求呼叫、Schema 驗證、JIT 短效 Token 簽發、微容器沙盒執行、回傳標籤封裝與審計 (Mermaid 4 對齊)")
    
    steps = [
        (1, "請求呼叫技能工具", "Agent ➔ Skill Guard", "TOOL INVOCATION", [
            "呼叫參數：傳入 Skill Name、Args 與 Context Trace。",
            "意圖綁定：確認當前任務允許呼叫該指定工具。"
        ], BRAND_SLATE),
        (2, "三要素衝突與密級校驗", "Skill Guard ➔ Guard", "SAFETY VERIFICATION", [
            "三要素校驗：驗證無「憑證 ⨂ 外網 ⨂ 不可信語料」衝突。",
            "密級比對：確認呼叫者具備相應之 DISA IL 權限標籤。"
        ], BRAND_SAGE),
        (3, "簽發單次 JIT 短效 Token", "Skill Guard ➔ Guard", "JIT TOKEN ISSUANCE", [
            "動態金鑰：產生僅限該工具與本次調用之 60 秒 Token。",
            "微沙盒啟動：在 gVisor 中以唯讀暫存卷冊啟動容器實例。"
        ], BRAND_TERRA),
        (4, "微沙盒隔離執行代碼", "Skill Guard ➔ Sandbox", "ISOLATED RUNTIME", [
            "限制連線：若需外網，僅限預先核准之特定 FQDN 白名單。",
            "無網路運算：本地代碼運算強制 network: none，防資料外傳。"
        ], BRAND_OCHRE),
        (5, "回傳清洗與安全封裝", "Sandbox ➔ Skill Guard", "ENVELOPE ISOLATION", [
            "不可信回傳封裝：強制包覆 <untrusted_tool_output> 標籤。",
            "行為漂移比對：檢查輸出長度與格式是否符合基準線。"
        ], BRAND_SAGE),
        (6, "寫入調用審計與回傳", "Skill Guard ➔ Audit / Agent", "AUDIT & RESPONSE", [
            "審計寫入：將 Syscall 軌跡與 SHA-256 簽署日誌寫入 SOC。",
            "結果交付：回傳清洗後之結構化結果供 Agent 繼續推論。"
        ], BRAND_SLATE)
    ]
    
    add_sequence_step_grid(slide, steps, top=1.68)
    add_footer(slide, 25, TOTAL_SLIDES)


def build_slide_26_skills_top10_p1(prs):
    """Slide 26: OWASP Agentic Skills Top 10 (Part 1: AST01 ~ AST05)."""
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
    add_footer(slide, 26, TOTAL_SLIDES)


def build_slide_27_skills_top10_p2(prs):
    """Slide 27: OWASP Agentic Skills Top 10 (Part 2: AST06 ~ AST10)."""
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
    add_footer(slide, 27, TOTAL_SLIDES)


def build_slide_28_skills_quant_p1(prs):
    """Slide 28: 全球 10 大 Skills 風險發生量化比例 (Part 1: Top 1~5)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "全球 10 大 Skills 風險發生量化比例與實證分佈 (Part 1)", "Skills 量化實證", "分析 AST01 ～ AST05 弱點審計與沙盒阻斷告警，揭示過度特權與依賴脆弱為最大宗 (Top 1~5)")
    
    t_data = ALL_TABLES[8]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][:5],
        col_widths=[1.0, 2.5, 1.8, 1.8, 4.6],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=7.8
    )
    add_footer(slide, 28, TOTAL_SLIDES)


def build_slide_29_skills_quant_p2(prs):
    """Slide 29: 全球 10 大 Skills 風險發生量化比例 (Part 2: Top 6~10)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "全球 10 大 Skills 風險發生量化比例與實證分佈 (Part 2)", "Skills 量化實證", "狀態覆寫、硬編碼憑證、無界並行、語意漂移與跨技能通訊脆弱實證數據分析 (Top 6~10)")
    
    t_data = ALL_TABLES[8]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][5:10],
        col_widths=[1.0, 2.5, 1.8, 1.8, 4.6],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=7.8
    )
    add_footer(slide, 29, TOTAL_SLIDES)


def build_slide_30_skills_manifest_and_envelope(prs):
    """Slide 30: Skill Manifest YAML 標準 (Pre 14) 與外部隔離封裝 XML (Pre 15)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "Skill Manifest YAML 清單標準與隔離封裝規範", "技術清單與封裝規範", "宣告權限最小化清單 (AST03) 與外部不可信回傳隔離封裝標籤 (AST05) (Pre 14/15 對齊)")
    
    col_w = 5.75
    gap = 0.23
    top = 1.68
    h = 5.25
    
    yaml_text = """skill_id: "sec-network-analyzer-v1"
version: "1.2.0"
signature: "SHA256-RSA:a98f12c..." # 企業 PKI 簽名
disa_clearance_allowed: ["DISA_IL_2", "DISA_IL_4"]

capabilities:
  network:
    allowed_egress_domains: ["api.threat-intel.internal"]
    max_payload_bytes: 1048576 # 限制 1MB
  filesystem:
    mode: "read-only"
    allowed_paths: ["/tmp/sandbox_data"]
  credentials:
    allow_ambient_credentials: false # 禁讀環境變數
    token_ttl_seconds: 60            # JIT 60 秒短效"""

    xml_text = """<!-- 護欄強制封裝：明確告知模型此為不可信資料，非系統指令 -->
<untrusted_tool_execution_result 
    skill_id="sec-network-analyzer-v1" 
    status="SUCCESS">
  <![CDATA[
  [已過濾可能包含的惡意腳本與隱藏 Prompt]
  原始查詢結果：...
  ]]>
</untrusted_tool_execution_result>"""
    
    # Left Box: Skill Manifest YAML
    add_code_box(slide, left=0.8, top=top, width=col_w, height=h, code_text=yaml_text, title="Skill 權限清單標準 (Skill Manifest)", lang="YAML")
    
    # Right Top Box: XML Isolation Envelope
    right_left = 0.8 + col_w + gap
    add_code_box(slide, left=right_left, top=top, width=col_w, height=2.45, code_text=xml_text, title="外部回傳隔離標籤 (Untrusted Envelope)", lang="XML")
    
    # Right Bottom Box: Architectural Rules
    add_bullet_card(
        slide, left=right_left, top=top + 2.60, width=col_w, height=2.65,
        title="清單標準與隔離標籤設計鐵律",
        items=[
            "權限顯式聲明 (AST03)：嚴禁在 Manifest 中使用萬用字元（*）；網路與檔案系統存取必須顯式列舉白名單。",
            "環境變數封鎖：allow_ambient_credentials 強制設為 false，徹底杜絕 Skill 偷讀主機 AWS/OpenAI 金鑰。",
            "結構化 CDATA 封裝 (AST05)：所有 Skill 產出強制包覆 <untrusted_tool_execution_result> 標籤，宣告純資料屬性，徹底免疫 Prompt 二次注入。"
        ],
        tag="SECURITY ENFORCEMENT",
        accent_color=BRAND_TERRA,
        header_bg=BRAND_SLATE
    )
    
    add_footer(slide, 30, TOTAL_SLIDES)
