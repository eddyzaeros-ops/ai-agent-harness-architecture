"""
Module 04 Slides (31 ~ 38): OWASP RAG Pipeline Security Guardrail Design
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


def build_slide_31_rag_lifecycle(prs):
    """Slide 31: RAG 生命週期威脅模型與六階段縱深防線 (Pre 16)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "RAG 生命週期威脅模型與六階段縱深防線全景", "RAG 縱深防禦模型", "攝取解析、向量嵌入、向量儲存、語義檢索、上下文組裝與模型生成全流程防護 (Pre 16 對齊)")
    
    col_w = 3.75
    gap = 0.24
    row_h = 2.48
    gap_y = 0.20
    top = 1.68
    
    stages = [
        ("01", "1. 攝取解析 (Ingestion)", "PARSER SANDBOX", BRAND_SLATE, [
            "防禦重點：防範文檔解析器漏洞 (RAG05) 與惡意腳本注入。",
            "落地機制：在無網路沙盒中解析 PDF/Word，清除白底白字、微小字型與潛在 SSRF/RCE 巨集。"
        ]),
        ("02", "2. 向量嵌入 (Embedding)", "EMBEDDING INTEGRITY", BRAND_SAGE, [
            "防禦重點：實施嵌入模型來源簽章，防範特徵逆向推論 (RAG09)。",
            "落地機制：驗證 Embedding 權重 SHA-256，禁止載入未經驗證之外部開源 Embedding 權重。"
        ]),
        ("03", "3. 向量儲存 (Vector Storage)", "STORAGE ISOLATION", BRAND_TERRA, [
            "防禦重點：強制租戶強隔離、Metadata 權限綁定與防投毒雜湊 (RAG02, RAG03)。",
            "落地機制：向量資料庫劃分唯讀分區與敏感分區，定期執行向量空間漂移離群點檢測。"
        ]),
        ("04", "4. 語義檢索 (Retrieval)", "PRE-FILTERING MANDATE", BRAND_OCHRE, [
            "防禦重點：嚴格執行 Pre-Filtering (前置權限過濾)，防跨租戶洩密 (RAG02)。",
            "落地機制：檢索前強制將使用者 TenantID 與 DISA IL 密級下推為向量引擎原生過濾條件。"
        ]),
        ("05", "5. 上下文組裝 (Augmentation)", "CONTEXT ENVELOPE", BRAND_SAGE, [
            "防禦重點：結構化標籤封裝、長度熔斷，防範間接注入與上下文洪水 (RAG01, RAG06)。",
            "落地機制：回傳 Chunks 強制包覆 <untrusted_rag_context> 標籤，並實施 Token 配額限制。"
        ]),
        ("06", "6. 模型生成 (Generation)", "GROUNDING AUDIT", BRAND_SLATE, [
            "防禦重點：忠實度驗證 (Faithfulness Check)，防範幻覺放大 (RAG07)。",
            "落地機制：以輕量 SLM 評估生成答覆之事實支撐度，若 Faithfulness < 0.72 則安全阻斷降級。"
        ])
    ]
    
    for idx, (num, title, tag, color, bullets) in enumerate(stages):
        r_idx = idx // 3
        c_idx = idx % 3
        c_left = 0.8 + c_idx * (col_w + gap)
        c_top = top + r_idx * (row_h + gap_y)
        
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(c_top), Inches(col_w), Inches(row_h))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = BORDER_CARD
        card.line.width = Pt(1)
        
        header_h = 0.44
        hbar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(c_top), Inches(col_w), Inches(header_h))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = BRAND_SLATE
        hbar.line.fill.background()
        
        badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(c_left + 0.12), Inches(c_top + 0.09), Inches(0.26), Inches(0.26))
        badge.fill.solid()
        badge.fill.fore_color.rgb = color
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
        rb.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        tb_h = slide.shapes.add_textbox(Inches(c_left + 0.44), Inches(c_top + 0.04), Inches(col_w - 0.52), Inches(header_h - 0.08))
        tf_h = tb_h.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
        p_h = tf_h.paragraphs[0]
        r_t = p_h.add_run()
        r_t.text = title
        r_t.font.name = FONT_HEADING
        r_t.font.size = Pt(9.5)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        p_sub = tf_h.add_paragraph()
        r_sub = p_sub.add_run()
        r_sub.text = f"防線標籤：[{tag}]"
        r_sub.font.name = FONT_BODY
        r_sub.font.size = Pt(8.0)
        r_sub.font.color.rgb = RGBColor(0xD6, 0xCE, 0xBF)
        
        tb_c = slide.shapes.add_textbox(Inches(c_left + 0.16), Inches(c_top + header_h + 0.08), Inches(col_w - 0.32), Inches(row_h - header_h - 0.14))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        for idx_b, b in enumerate(bullets):
            p = tf_c.paragraphs[0] if idx_b == 0 else tf_c.add_paragraph()
            p.space_after = Pt(4)
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

    add_footer(slide, 31, TOTAL_SLIDES)


def build_slide_32_rag_architecture_diagram(prs):
    """Slide 32: RAG 護欄核心系統架構圖 (Pre 17)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "RAG 護欄核心系統架構圖 (Ingestion ⨂ Pre-Filter ⨂ Augmentation)", "RAG 核心系統架構", "身分授權中心、六大安全防護閘門、向量知識庫與審計日誌全景 (Pre 17 對齊)")
    
    col_w = 3.75
    gap = 0.24
    top = 1.68
    h = 5.25
    
    # Col 1: 攝取與預檢
    add_bullet_card(
        slide, left=0.8, top=top, width=col_w, height=h,
        title="入庫清洗與授權排查 (Ingestion & Pre-Check)",
        items=[
            "閘門 1：入庫沙盒清洗閘 (Ingestion Guard)：gVisor 無網路解析容器，過濾 PDF 惡意巨集 (RAG05)。",
            "文檔雜湊簽章校驗 (RAG03)：入庫 Chunk 計算 SHA-256 指紋，防範內部投毒與檔案置換。",
            "閘門 2：前置授權過濾閘 (Pre-Filter Guard)：強制帶入 TenantID 與 DISA IL 標籤 (RAG02)。",
            "禁止事後過濾 (No Post-Filtering)：嚴格禁止召回未授權文檔再由 Prompt 過濾，杜絕資訊洩漏。",
            "閘門 3：對抗性特徵排查 (Adversarial Guard)：困惑度 Perplexity 檢測，排查對抗性綴詞。"
        ],
        tag="INGESTION & PRE-FILTER",
        accent_color=BRAND_SAGE,
        header_bg=BRAND_SLATE
    )
    
    # Col 2: 檢索增強與上下文封裝
    add_bullet_card(
        slide, left=0.8 + col_w + gap, top=top, width=col_w, height=h,
        title="上下文封裝與事實在線審核 (Augmentation & Grounding)",
        items=[
            "閘門 4：上下文安全封裝閘 (Augmentation Guard)：強制包覆 <untrusted_rag_context> 結構化標籤 (RAG01)。",
            "輕量注入分類器：Llama-Guard / SLM 實時掃描檢索文檔塊，剔除潛在越獄語句。",
            "閘門 5：配額與截斷熔斷器 (Budget Guard)：嚴格限制 Top-K (<=5) 與 Token 總量 (RAG06)。",
            "Metadata 敏感欄位過濾 (RAG04)：主動抹除 filepath、內部伺服器名稱與私有 URL。",
            "閘門 6：忠實度事實在線審核 (Grounding Guard)：以 SLM 進行 NLI 推論，相似度 < 0.72 則拒絕輸出。"
        ],
        tag="AUGMENTATION & GROUNDING",
        accent_color=BRAND_TERRA,
        header_bg=BRAND_SLATE
    )
    
    # Col 3: 底層儲存與審計
    add_bullet_card(
        slide, left=0.8 + (col_w + gap) * 2, top=top, width=col_w, height=h,
        title="底層向量知識庫與不可否認性審計 (Vector DB & Audit)",
        items=[
            "向量儲存 (Vector DB)：Milvus / Pinecone 實施物理與命名空間隔離，防止跨租戶借道。",
            "檢索增強組合引擎 (Orchestration)：在安全邊界內將經審查之 Prompt 送入 LLM 推論核心。",
            "不可否認性審計日誌 (SOC / SIEM)：即時記錄查詢輸入 SHA-256、召回文檔塊清單與授權判決。",
            "快取生命週期管理：針對檢索快取設定短期 TTL，並隔離不同權限等級之快取空間。",
            "來源溯源數位水印：每一組裝好的上下文均帶有動態 Canary Token，防止輸出被非法抽取。"
        ],
        tag="VECTOR STORAGE & AUDIT",
        accent_color=BRAND_OCHRE,
        header_bg=BRAND_SLATE
    )
    
    add_footer(slide, 32, TOTAL_SLIDES)


def build_slide_33_rag_sequence_flow(prs):
    """Slide 33: RAG 檢索增強循序防護流程圖 (Mermaid 5)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "RAG 檢索增強循序防護流程圖 (Pre-Retrieval to Grounding)", "RAG 循序流程", "查詢檢驗、Filter-First 向量檢索、標籤隔離封裝、LLM 生成、忠實度審核與審計 (Mermaid 5 對齊)")
    
    steps = [
        (1, "使用者提出知識檢索", "User ➔ Gateway", "QUERY INITIATION", [
            "提問範例：「請幫我統整 Q3 專利報告」。",
            "身分標註：閘道解析 UserToken、TenantID 與 DISA IL 密級。"
        ], BRAND_SLATE),
        (2, "前置檢索授權注入", "Gateway ➔ RAG Guard", "PRE-RETRIEVAL FILTER", [
            "語意防注入檢測 (RAG01)：排查查詢字串中之對抗性語句。",
            "權限強制注入 (RAG02)：將 TenantID 與密級標籤下推至查詢條件。"
        ], BRAND_SAGE),
        (3, "帶權限之向量檢索", "RAG Guard ➔ VectorDB", "FILTER-FIRST SEARCH", [
            "Filter-First 檢索：向量庫僅在符合權限的範圍內比對相似度。",
            "召回過濾：剔除離群塊，安全回傳原始 Chunks 與中繼資料。"
        ], BRAND_TERRA),
        (4, "上下文封裝與配額截斷", "RAG Guard ➔ LLM", "AUGMENTATION ENVELOPE", [
            "相似度門檻截斷 (RAG07)：Cos Sim < 0.72 直接丟棄。",
            "安全封裝 (RAG01)：強制以 <untrusted_rag_chunk> 標籤包覆 Context。"
        ], BRAND_OCHRE),
        (5, "生成初步回覆與忠實度", "LLM ➔ RAG Guard", "GROUNDING VERIFICATION", [
            "推論生成：LLM 依據隔離 Context 產出初步答覆。",
            "忠實度檢驗 (RAG07)：SLM 比對 Context 內容，防範胡謅引文。"
        ], BRAND_SAGE),
        (6, "審計日誌寫入與交付", "RAG Guard ➔ Audit / User", "AUDIT & RESPONSE", [
            "審計寫入 (RAG02)：記錄完整檢索來源、召回塊雜湊與授權軌跡。",
            "合規交付：將具備事實支撐之合規答案安全回傳給使用者。"
        ], BRAND_SLATE)
    ]
    
    add_sequence_step_grid(slide, steps, top=1.68)
    add_footer(slide, 33, TOTAL_SLIDES)


def build_slide_34_rag_top10_p1(prs):
    """Slide 34: OWASP RAG Pipeline 10 大關鍵風險 (Part 1: RAG01 ~ RAG05)."""
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
    add_footer(slide, 34, TOTAL_SLIDES)


def build_slide_35_rag_top10_p2(prs):
    """Slide 35: OWASP RAG Pipeline 10 大關鍵風險 (Part 2: RAG06 ~ RAG10)."""
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
    add_footer(slide, 35, TOTAL_SLIDES)


def build_slide_36_rag_quant_p1(prs):
    """Slide 36: 全球 10 大 RAG 風險發生量化比例 (Part 1: Top 1~5)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "全球 10 大 RAG 風險發生量化比例與實證分佈 (Part 1)", "RAG 量化實證分析", "分析 RAG01 ～ RAG05 實證受駭事件與網關攔截告警，揭示間接注入與檢索越權居前列 (Top 1~5)")
    
    t_data = ALL_TABLES[10]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][:5],
        col_widths=[1.0, 2.5, 1.8, 1.8, 4.6],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=7.8
    )
    add_footer(slide, 36, TOTAL_SLIDES)


def build_slide_37_rag_quant_p2(prs):
    """Slide 37: 全球 10 大 RAG 風險發生量化比例 (Part 2: Top 6~10)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "全球 10 大 RAG 風險發生量化比例與實證分佈 (Part 2)", "RAG 量化實證分析", "幻覺事實缺乏、對抗性探測、向量庫洩漏、敏感快取與元資料投毒之實證數據分析 (Top 6~10)")
    
    t_data = ALL_TABLES[10]
    add_custom_table(
        slide, left=0.8, top=1.68, width=11.733, height=5.25,
        headers=t_data['headers'],
        rows_data=t_data['rows'][5:10],
        col_widths=[1.0, 2.5, 1.8, 1.8, 4.6],
        col_alignments=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT],
        font_size=7.8
    )
    add_footer(slide, 37, TOTAL_SLIDES)


def build_slide_38_rag_code_and_bundle(prs):
    """Slide 38: Pre-Filtering 前置強制過濾 Python 代碼 (Pre 20) 與上下文安全封裝 XML (Pre 21)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_warm_background(slide)
    add_header(slide, "RAG 前置強制過濾代碼規格與上下文安全封裝範本", "代碼規格與封裝標籤", "嚴格禁止事後過濾，落實 Pre-Filtering 原生下推與 Context Grounding Bundle XML (Pre 20/21 對齊)")
    
    col_w = 5.75
    gap = 0.23
    top = 1.68
    h = 5.25
    
    py_text = """# 嚴格禁止：先檢索向量再手動 filter (Post-filtering 會洩漏距離)
# 正確做法：Pre-filtering (強制將授權標籤納入 ANN 核心條件)
search_params = {
    "collection_name": "enterprise_knowledge_base",
    "vector": query_embedding,
    "limit": 5,  # 嚴格限制 Top-K，防止 Context Flooding (RAG06)
    "expr": (
        f'tenant_id == "{current_user.tenant_id}" and '
        f'clearance_level <= {current_user.disa_il}'
    ),
    "output_fields": [
        "doc_id", "title", "safe_summary", "public_url"
    ]  # 嚴禁暴露內部 filepath (RAG04)
}"""

    xml_text = """<!-- 護欄強制封裝：提示推論引擎不得將其視為管理員指令 -->
<context_grounding_bundle 
    query_id="req-9842" 
    max_tokens="2048">
  <untrusted_rag_chunk 
      id="chunk-01" 
      doc_id="patent-2026-q3" 
      score="0.88">
    <![CDATA[
    [已過濾潛在隱藏標籤與腳本]
    2026 年第三季量子通訊專利摘要：...
    ]]>
  </untrusted_rag_chunk>
</context_grounding_bundle>"""
    
    # Left Box: Python Code
    add_code_box(slide, left=0.8, top=top, width=col_w, height=h, code_text=py_text, title="Pre-Filtering 向量檢索安全規格 (Python)", lang="PYTHON")
    
    # Right Top Box: XML Bundle
    right_left = 0.8 + col_w + gap
    add_code_box(slide, left=right_left, top=top, width=col_w, height=2.45, code_text=xml_text, title="檢索上下文安全隔離標籤 (Grounding XML)", lang="XML")
    
    # Right Bottom Box: Architectural Rules
    add_bullet_card(
        slide, left=right_left, top=top + 2.60, width=col_w, height=2.65,
        title="RAG 檢索與封裝兩大工程鐵律",
        items=[
            "權限原生下推規格 (RAG02)：在執行向量 Similarity Search 前，強制注入原生過濾條件，禁止送入未授權文檔再由 Prompt 忽略。",
            "欄位白名單審查 (RAG04)：嚴格禁止輸出原始 filepath 或系統內部絕對路徑，輸出必須脫敏為公開或安全代號。",
            "上下文 CDATA 封裝 (RAG01)：所有召回片段強制包覆於 <untrusted_rag_chunk> 中，明確宣告純事實屬性，徹底免疫間接提示詞注入。"
        ],
        tag="SECURITY ENFORCEMENT",
        accent_color=BRAND_TERRA,
        header_bg=BRAND_SLATE
    )
    
    add_footer(slide, 38, TOTAL_SLIDES)
