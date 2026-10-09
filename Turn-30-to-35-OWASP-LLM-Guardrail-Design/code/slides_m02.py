"""
Module 02 Slides (15 ~ 22): OWASP Top 10 for Agentic Applications Guardrail Design
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


def build_slide_15_agentic_paradigm(prs):
    """Slide 15: 典範轉移：傳統 LLM 護欄 vs. Agentic 代理人行為護欄 (Table 4)."""
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
    add_footer(slide, 15, TOTAL_SLIDES)


def build_slide_16_agentic_three_dimensions_diagram(prs):
    """Slide 16: Agentic 「三維六門」防禦架構全景圖 (Pre 8)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "Agentic 「三維六門」防禦架構全景流程圖", "三維六門架構全景", "意圖防護、動態憑證、工具沙盒、記憶隔離、跨代理網格與級聯熔斷 (Pre 8 對齊)")
    
    col_w = 3.75
    gap = 0.24
    top = 1.68
    h = 5.25
    
    # Col 1: 意圖與規劃維度 (門 1 + 門 2)
    add_bullet_card(
        slide, left=0.8, top=top, width=col_w, height=h,
        title="維度一：意圖與規劃 (Intent & Planning)",
        items=[
            "門 1：目標錨定門 (Goal Anchor)：System Prompt 數位簽章鎖定唯讀，禁止代理人黑箱修改 Root Mission。",
            "語意漂移評估 (Drift Detector)：即時比對子任務與最初登錄任務之餘弦相似度，偏離門檻即阻斷。",
            "門 2：規劃重評門 (Plan Re-evaluator)：由隔離的 Supervisor Model 獨立審查 Action Plan，驗證合法性。",
            "自主步驟配額：單次執行上限 25 步，累計偏離超過 2 次強制終止並退回人工審查。",
            "不可逆狀態檢查：偵測是否有破壞性指令（如格式化、DROP、覆寫政策），即時標記高危。"
        ],
        tag="GATES 1 & 2",
        accent_color=BRAND_SAGE,
        header_bg=BRAND_SLATE
    )
    
    # Col 2: 工具調用與身分授權 (門 3 + 門 4)
    add_bullet_card(
        slide, left=0.8 + col_w + gap, top=top, width=col_w, height=h,
        title="維度二：工具與授權 (Tools & Identity)",
        items=[
            "門 3：動態身分經紀 (JIT Broker)：拒絕長期靜態金鑰；每次工具調用前簽發 60 秒短效最小權限 Token。",
            "DISA IL 密級校驗：比對呼叫者身分標籤與工具環境密級，不符直接拒發憑證。",
            "門 4：工具沙盒防火牆 (Tool Sandbox)：所有工具在 gVisor 微容器中執行，限制資源與出向網路。",
            "參數 Schema 嚴格校驗：Tool Arguments 強制通過 Pydantic / JSON Schema 驗證，防 SQLi 與溢出。",
            "情境化去話術 HITL：高危操作 UI 強制展示原始結構化參數，嚴禁代理人修辭粉飾誤導。"
        ],
        tag="GATES 3 & 4",
        accent_color=BRAND_TERRA,
        header_bg=BRAND_SLATE
    )
    
    # Col 3: 記憶與多代理人協同 (門 5 + 門 6)
    add_bullet_card(
        slide, left=0.8 + (col_w + gap) * 2, top=top, width=col_w, height=h,
        title="維度三：記憶與協同 (Memory & Multi-Agent)",
        items=[
            "門 5：記憶隔離護欄 (Memory Guard)：短期對話歷程每輪迭代洗滌；長期向量記憶切片綁定雜湊防投毒。",
            "記憶寫入閘門：高密級資料嚴禁沉澱為泛用記憶；長期記憶庫分艙隔離與唯讀簽署。",
            "門 6：跨代理網格 (A2A Mesh)：多代理人通訊強制雙向 mTLS 認證，附帶帶簽章之 Context Trace。",
            "級聯熔斷看門狗 (Cascade Breaker)：多代理人協同設置最大迴圈深度 (Max Hop=8) 與 Token 配額。",
            "死迴圈偵測：連續異常重試或重複執行 3 次立即熔斷，阻斷級聯崩潰並通報 SOC。"
        ],
        tag="GATES 5 & 6",
        accent_color=BRAND_OCHRE,
        header_bg=BRAND_SLATE
    )
    
    add_footer(slide, 16, TOTAL_SLIDES)


def build_slide_17_agentic_sequence_flow(prs):
    """Slide 17: Agentic 核心執行循序流程 (Mermaid 3)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "Agentic 核心執行循序流程圖 (Tool Call & Memory)", "Agentic 循序流程", "規劃提交、意圖驗證、去話術 HITL 審核、JIT 憑證經紀、沙盒執行與記憶防投毒 (Mermaid 3 對齊)")
    
    steps = [
        (1, "使用者下達複合任務", "User ➔ Agent Runtime", "TASK DISPATCH", [
            "複合任務請求：如「排查並修復伺服器異常連線」。",
            "初始化會話：生成 Context Trace ID 並鎖定根目標。"
        ], BRAND_SLATE),
        (2, "提交規劃步驟清單", "Agent ➔ Guardrail", "PLAN SUBMISSION", [
            "目標不可變驗證 (ASI01)：比對當前意圖與 System Prompt 簽名。",
            "狀態機檢查 (ASI10)：驗證步驟是否符合 FSM 合法轉移路徑。"
        ], BRAND_SAGE),
        (3, "工具調用與去話術 HITL", "Guardrail ➔ Approver", "SAFETY & HITL", [
            "死迴圈排查 (ASI08)：檢查目前迴圈計數器與調用頻率。",
            "情境化 HITL (ASI09)：判定為高危操作，展示原始參數交審批。"
        ], BRAND_TERRA),
        (4, "JIT 憑證動態簽發", "Guardrail ➔ Broker", "DYNAMIC TOKEN", [
            "短效授權 (ASI03)：授權通過後向 Broker 申請臨時 Token。",
            "時效與範圍：核發 60 秒有效期與嚴格最小權限之 Token。"
        ], BRAND_OCHRE),
        (5, "沙盒受限執行代碼", "Guardrail ➔ Sandbox", "SANDBOX EXECUTION", [
            "隔離環境 (ASI05)：在 gVisor 微容器中執行指令，禁非必要外網。",
            "過濾回傳：將純淨標準輸出回傳給 Agent Runtime。"
        ], BRAND_SAGE),
        (6, "記憶防投毒寫入與回報", "Guardrail ➔ Memory / User", "MEMORY & DELIVER", [
            "記憶防投毒 (ASI06)：去除潛在腳本，計算雜湊後安全寫入記憶。",
            "回報完成：向使用者呈現經護欄審查通過之最終執行成果。"
        ], BRAND_SLATE)
    ]
    
    add_sequence_step_grid(slide, steps, top=1.68)
    add_footer(slide, 17, TOTAL_SLIDES)


def build_slide_18_agentic_top10_p1(prs):
    """Slide 18: OWASP Top 10 for Agentic Applications (Part 1: ASI01 ~ ASI05)."""
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
    add_footer(slide, 18, TOTAL_SLIDES)


def build_slide_19_agentic_top10_p2(prs):
    """Slide 19: OWASP Top 10 for Agentic Applications (Part 2: ASI06 ~ ASI10)."""
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
    add_footer(slide, 19, TOTAL_SLIDES)


def build_slide_20_agentic_quant_p1(prs):
    """Slide 20: 全球 10 大 Agentic 應用受駭事件量化分佈 (Part 1: ASI01 ~ ASI05)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "全球 Agentic 應用受駭事件與執行時告警量化分佈 (Part 1)", "Agentic 量化實證", "分析 ASI01 ～ ASI05 實證受駭事件與監控告警，揭示目標劫持與工具濫用為最大宗風險")
    
    t_data = ALL_TABLES[6]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][:5],
        col_widths=[1.0, 2.5, 1.8, 1.8, 4.6],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=7.8
    )
    add_footer(slide, 20, TOTAL_SLIDES)


def build_slide_21_agentic_quant_p2(prs):
    """Slide 21: 全球 10 大 Agentic 應用受駭事件量化分佈 (Part 2: ASI06 ~ ASI10)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "全球 Agentic 應用受駭事件與執行時告警量化分佈 (Part 2)", "Agentic 量化實證", "記憶投毒、不安全通訊、級聯失敗、阻斷服務與缺乏監督之實證數據分析 (ASI06~10)")
    
    t_data = ALL_TABLES[6]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][5:10],
        col_widths=[1.0, 2.5, 1.8, 1.8, 4.6],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=7.8
    )
    add_footer(slide, 21, TOTAL_SLIDES)


def build_slide_22_agentic_security_controls(prs):
    """Slide 22: Agentic 核心安全控制規格."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "Agentic 核心安全控制規格與落地實施標準", "安全控制規格標準", "落實動態 JIT 短效授權、去話術化情境 HITL 雙重簽核、有限狀態機與記憶分艙隔離")
    
    col_w = 2.78
    gap = 0.20
    top = 1.68
    h = 5.25
    
    controls = [
        ("01", "JIT 動態憑證規格", "Just-In-Time Credential", BRAND_SLATE, [
            "拒絕靜態金鑰：代理人永不直接持有主機密鑰或資料庫帳密。",
            "60 秒短效 Token：每次工具調用前由 Broker 動態簽發。",
            "範圍精準綁定：Token 僅限特定 Tool Action 與指定資料庫資源。",
            "單次使用即失效：防止 Token 殘留於上下文中遭攻擊者重放。"
        ]),
        ("02", "去話術 HITL 規格", "Epistemic Contextual HITL", BRAND_SAGE, [
            "杜絕修辭粉飾：禁止 Agent 代替人做主或以自然語言美化高危動作。",
            "結構化參數呈現：UI 強制展示被執行的原始 SQL、Shell 或 API Payload。",
            "影響範圍評估：明確標記涉及之資產重要度與不可逆後果。",
            "安全官員獨立簽章：高危寫入動作必須經由人類雙重授權確認。"
        ]),
        ("03", "有限狀態機約束", "Finite State Machine (FSM)", BRAND_TERRA, [
            "顯式狀態定義：定義 Agent 僅能在「規劃-驗證-執行-回報」狀態間流轉。",
            "禁止非法躍遷：若 Agent 企圖從「閱讀」直接跳躍至「執行高危寫入」，即刻凍結。",
            "執行步數計數器：單一任務最大步數限制為 25 步，超標即斷路。",
            "狀態快照回滾：每一步驟前儲存 Checkpoint，違規時一秒復原。"
        ]),
        ("04", "記憶分艙與簽名", "Memory Isolation & Hashing", BRAND_OCHRE, [
            "短期記憶洗滌：每一輪迭代前過濾注入特徵與異常指令。",
            "長期記憶切片綁定：向量記憶庫切片綁定來源 SHA-256 雜湊與時間戳。",
            "密級繼承：高密級資料（DISA IL-4+）絕對禁止沉澱為泛用對話記憶。",
            "記憶寫入閘門：寫入長期記憶庫前必須通過獨立安全審查器比對。"
        ])
    ]
    
    for idx, (num, name, role, color, bullets) in enumerate(controls):
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

    add_footer(slide, 22, TOTAL_SLIDES)
