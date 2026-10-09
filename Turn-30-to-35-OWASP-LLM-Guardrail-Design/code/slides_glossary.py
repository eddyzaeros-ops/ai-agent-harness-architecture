# -*- coding: utf-8 -*-
"""
slides_glossary.py
Dedicated Terminology and Acronym Glossary Slides conforming strictly to PPTX Template 1.
Explains keywords, English acronyms, full names, core architectural meanings, and module references.
"""

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from slides_common import (
    apply_warm_background,
    add_header,
    add_footer,
    add_custom_table,
    TOTAL_SLIDES,
    BRAND_SAGE,
    BRAND_TERRA,
    BRAND_SLATE,
    TEXT_HEADLINE,
    TEXT_BODY,
    BG_CARD,
    TABLE_HEADER_BG,
    TABLE_ROW_ALT
)

GLOSSARY_COL_WIDTHS = [2.0, 2.7, 5.5, 1.5]
GLOSSARY_COL_ALIGNMENTS = [PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER]
GLOSSARY_HEADERS = ["縮寫 / 關鍵字", "英文全稱 / 概念原型", "核心意涵與工程防護定位", "報告對應模組"]

# ==============================================================================
# Slide Glossary 1: Core Architecture & Governance
# ==============================================================================
def build_slide_glossary_1(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    apply_warm_background(slide)
    
    add_header(
        slide,
        "名詞對照表 (一)：核心架構、護欄防禦與治理框架全解",
        "術語與縮寫精解",
        "全景梳理報告引用之核心英文縮寫與專有名詞，協助跨領域架構師與資安團隊精準對齊技術語義"
    )
    
    rows = [
        ["OWASP", "Open Worldwide Application Security Project", "全球權威應用軟體安全非營利組織，發布 LLM Top 10 與 Agentic Top 10 核心資安標準指引。", "核心標準 (P2, P4, P10)"],
        ["LLM", "Large Language Model", "大語言模型。基於 Transformer 架構之次字元機率預測神經網絡，為代理人決策與推論大腦。", "模型層 (P2, P8, P10)"],
        ["Agentic", "Autonomous Agent Architecture", "自主代理人架構。具備自主規劃、狀態記憶、工具執行與環境反饋循環（ReAct）之複合 AI 軟體實體。", "代理層 (P2, P17, P20)"],
        ["Guardrails", "Safety & Security Guardrails", "安全護欄。獨立於模型外部的確定性軟體層，在請求入向與輸出出向執行即時安全校驗與攔截。", "核心概念 (P2, P5, P8)"],
        ["Harness Eng.", "Execution Harness Engineering", "束具工程。將不可預測的機率模型包裹於確定性架構（狀態機、沙盒、審計）中之工程方法論。", "核心理念 (P1, P54, P58)"],
        ["Defense-in-Depth", "Multi-Tier Layered Defense", "縱深防禦。源自軍事資安架構原則，不依賴單一防線，在 L1~L5 佈建多層獨立互補的攔截關卡。", "架構總綱 (P2, P5, P6)"],
        ["Zero-Trust", "Zero-Trust Architecture (NIST)", "零信任架構。核心哲學「永不信任、始終驗證」，預設所有輸入、外部文檔與工具回傳均為不可信。", "安全綱領 (P5, P46, P57)"],
        ["FSM", "Finite State Machine", "有限狀態機。約束代理人規劃路徑的確定性狀態模型，嚴格限定狀態轉移規則，防止行為失控。", "行為約束 (P18, P25)"],
        ["JIT", "Just-In-Time Dynamic Authorization", "即時動態授權。每次工具調用前動態簽發 60 秒短效最小權限 Token，調用結束即作廢，杜絕憑證濫用。", "動態身分 (P18, P25, P34)"],
        ["HITL / HOTL", "Human-in-the-Loop / on-the-Loop", "人工在環（高危操作強制人審）與人工在旁（自動運行但具備緊急熔斷機制）之分級治理機制。", "治理機制 (P22, P25)"],
        ["SLM", "Small Language Model (< 8B)", "輕量端側小模型。參數量小於 8B 之專用模型（如 Llama-Guard），以極低延遲執行特定護欄檢驗。", "護欄引擎 (P8, P16, P36)"]
    ]
    
    add_custom_table(
        slide,
        left=0.80, top=1.72, width=11.733, height=5.15,
        headers=GLOSSARY_HEADERS,
        rows_data=rows,
        col_widths=GLOSSARY_COL_WIDTHS,
        col_alignments=GLOSSARY_COL_ALIGNMENTS,
        font_size=7.8,
        has_card_container=True
    )
    
    add_footer(slide, 1, TOTAL_SLIDES)


# ==============================================================================
# Slide Glossary 2: Semantic Boundary & Prompt Attacks
# ==============================================================================
def build_slide_glossary_2(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    apply_warm_background(slide)
    
    add_header(
        slide,
        "名詞對照表 (二)：語意邊界、提示詞攻擊與審計日誌全解",
        "術語與縮寫精解",
        "深入解析 Prompt 注入、越獄逃逸、資料脫敏防護機制與密碼學不可否認審計日誌之專有名詞"
    )
    
    rows = [
        ["Prompt Injection", "Direct & Indirect Prompt Injection", "提示詞注入。攻擊者透過惡意文字覆寫系統指令，強迫模型執行偏離預期意圖之越權操作或有害輸出。", "語意安全 (P8, P10, P14)"],
        ["Jailbreak", "Safety Alignment Bypass Attack", "越獄攻擊。利用認知混淆、多語言轉碼或角色扮演假想情境，繞過模型內建倫理對齊與安全防禦邊界。", "語意安全 (P8, P10, P45)"],
        ["System Prompt", "System Instruction Baseline", "系統提示詞。定義模型核心角色定位、行為邊界與不可違背規則之頂層宣告，需實施數位簽章鎖定。", "意圖防護 (P8, P18)"],
        ["Canary Token", "Dynamic Cryptographic Honeyword", "金絲雀標記。隨機注入系統提示或檢索上下文之密鑰字串，若在輸出中被偵測即判定提示詞發生外洩。", "洩漏偵測 (P8, P15, P36)"],
        ["PII", "Personally Identifiable Information", "個人身分識別資訊。個人姓名、身分證號、信用卡等敏感隱私資訊，護欄必須實施強制脫敏（Masking）。", "資料保護 (P8, P10, P15)"],
        ["DLP", "Data Loss Prevention", "資料外洩防護。即時監控並阻止內部專利代碼、財報數據透過模型輸出管道未授權流向外部未受控網絡。", "出向護欄 (P8, P10, P16)"],
        ["PPL", "Perplexity (Language Uncertainty)", "困惑度檢測。統計語言模型對文本的預測不確定性指標；文字經對抗性擾動時困惑度異常飆高，可精準排查。", "對抗防禦 (P36, P43)"],
        ["Hallucination", "Model Hallucination & Fabrication", "模型幻覺。模型生成自信但完全捏造、錯誤或背離檢索上下文事實的回答，需透過 NLI 模組校驗。", "出向校驗 (P8, P36, P38)"],
        ["NLI", "Natural Language Inference", "自然語言推論。以輕量模型推論產出語句是否嚴格蘊含（Entailment）於檢索文檔，量化計算忠實度分數。", "事實審核 (P36, P38)"],
        ["Non-Repudiation", "Non-Repudiation Cryptographic Trail", "不可否認性審計。日誌附帶 SHA-256 雜湊鏈與密碼學簽章，證明防禦判決與操作紀錄未遭事後篡改。", "審計基石 (P5, P15, P57)"]
    ]
    
    add_custom_table(
        slide,
        left=0.80, top=1.72, width=11.733, height=5.15,
        headers=GLOSSARY_HEADERS,
        rows_data=rows,
        col_widths=GLOSSARY_COL_WIDTHS,
        col_alignments=GLOSSARY_COL_ALIGNMENTS,
        font_size=7.8,
        has_card_container=True
    )
    
    add_footer(slide, 1, TOTAL_SLIDES)


# ==============================================================================
# Slide Glossary 3: Skills Security & Micro-Sandbox
# ==============================================================================
def build_slide_glossary_3(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    apply_warm_background(slide)
    
    add_header(
        slide,
        "名詞對照表 (三)：Skills 技能工具、微沙盒與致命三要素全解",
        "術語與縮寫精解",
        "解析工具調用威脅模型、gVisor 微容器架構、系統調用白名單過濾與多代理級聯熔斷看門狗"
    )
    
    rows = [
        ["Lethal Trifecta", "The Lethal Trifecta (Attack Pattern)", "致命三要素。同時具備「機敏憑證存取」、「外網連線能力」與「不可信語料讀取」之架構死穴，引爆外洩。", "威脅模型 (P26, P33)"],
        ["gVisor", "Google Application Kernel Sandbox", "Google 輕量級安全微容器環境。在使用者空間重寫 Linux 核心架構，攔截並隔離危險 syscall，防容器逃逸。", "沙盒隔離 (P27, P33, P34)"],
        ["Syscall Filter", "System Call Whitelisting (Seccomp)", "系統調用過濾。嚴格封鎖 execve、socket、ptrace 等高危系統調用，僅允許沙盒執行純計算與安全受控 I/O。", "執行防禦 (P27, P34)"],
        ["Seccomp", "Secure Computing Mode (Linux Kernel)", "安全計算模式。Linux 內核級安全機制，可根據系統調用號碼和參數進行封包過濾，建立最小進程沙盒。", "容器加固 (P27, P34)"],
        ["Capability Leaking", "Overprivileged Tool Exposure (AST10)", "能力洩漏。技能工具未依最小特權原則收斂，將全權 Admin API 暴露給代理人，遭攻擊者利用提權。", "權限收斂 (P29, P32)"],
        ["Tool Poisoning", "Skill Manifest Tampering (AST07)", "工具投毒。攻擊者篡改 Skill Manifest 中的描述或參數規範，欺騙 LLM 調用惡意偽裝之第三方函數。", "供應鏈防禦 (P27, P30)"],
        ["Shadow Agent", "Unauthorized Autonomous Sub-Agent", "影子代理人。代理人未經安全註冊，自主在後台衍生之非受控背景子進程，脫離日誌監控與憑證管理。", "行為審計 (P21, P23)"],
        ["Cascade Failure", "Multi-Agent Cascading Breakdown", "級聯崩潰。多代理網路中一個代理人的錯誤或毒化輸出被非線性循環放大，導致全體死迴圈或癱瘓。", "協同防禦 (P18, P21)"],
        ["Circuit Breaker", "Loop & Quota Watchdog Breaker", "熔斷看門狗。監控代理人執行步驟數（配額 <= 25 步）與重試頻率，偵測到重複動作連續 3 次立即熔斷。", "穩定性機制 (P18, P25)"],
        ["XML Envelope", "Untrusted Context Semantic Isolation", "XML 語意隔離封裝。將工具執行回傳以 <untrusted_tool_result> 標籤包裹，提示模型該文字僅供分析禁止執行。", "輸出隔離 (P30, P34)"]
    ]
    
    add_custom_table(
        slide,
        left=0.80, top=1.72, width=11.733, height=5.15,
        headers=GLOSSARY_HEADERS,
        rows_data=rows,
        col_widths=GLOSSARY_COL_WIDTHS,
        col_alignments=GLOSSARY_COL_ALIGNMENTS,
        font_size=7.8,
        has_card_container=True
    )
    
    add_footer(slide, 1, TOTAL_SLIDES)


# ==============================================================================
# Slide Glossary 4: RAG Pipeline, Vector DB & MITRE ATLAS
# ==============================================================================
def build_slide_glossary_4(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    apply_warm_background(slide)
    
    add_header(
        slide,
        "名詞對照表 (四)：RAG 檢索增強、向量安全與 MITRE ATLAS 全解",
        "術語與縮寫精解",
        "解析向量資料庫前置過濾、事實錨定檢驗、MITRE ATLAS AI 殺傷鏈戰術與量化效能指標"
    )
    
    rows = [
        ["RAG", "Retrieval-Augmented Generation", "檢索增強生成。透過向量資料庫檢索即時專屬知識，與使用者的 Prompt 拼接後再送交 LLM 推論的架構。", "知識外掛 (P35, P38)"],
        ["Vector DB", "Vector Database (Milvus / Pinecone)", "向量資料庫。將文本語意特徵轉化為高維稠密向量並實施高維相似度檢索（如 HNSW、Cosine）之儲存系統。", "向量儲存 (P35, P36)"],
        ["Pre-Filtering", "Mandatory Tenant & Security Filter", "前置強制過濾。向量檢索階段即帶入租戶 ID 與 DISA IL 密級過濾，嚴格禁止事後過濾以杜絕記憶體側漏。", "授權邊界 (P36, P43)"],
        ["Post-Filtering", "Post-Retrieval Filter (Anti-Pattern)", "事後過濾（反面模式）。檢索出未授權文檔後再依賴 Prompt 或代碼剔除，極易遭提示詞注入突破導致洩漏。", "反面模式 (P36, P43)"],
        ["DISA IL", "Defense Info Systems Agency Impact Level", "美國國防資訊系統局資安衝擊評級（IL2 非機敏至 IL6 機密密級），定義不同數據艙之隔離標準。", "國防密級 (P36, P43)"],
        ["Grounding", "Fact Grounding & Faithfulness Audit", "錨定驗證。透過語意蘊含模型確保產生的回答嚴格錨定在檢索文檔塊內，未經文檔證實者判定為幻覺拒答。", "幻覺防禦 (P36, P43)"],
        ["MITRE ATLAS", "Adversarial Threat Landscape for AI", "針對人工智慧與機器學習系統專屬對抗攻擊技術、戰術與常見知識庫（AI 版 ATT&CK）。", "威脅矩陣 (P44, P47)"],
        ["MITRE ATT&CK", "Adversarial Tactics, Techniques, & CK", "全球權威傳統企業網路對抗攻擊戰術與技術知識庫，奠定資安攻擊鏈防禦之標準基礎。", "傳統資安 (P44)"],
        ["Kill Chain", "Cyber / AI Attack Kill Chain", "攻擊殺傷鏈。攻擊者從偵察、初始存取、持久化、特權提升到終端影響的端到端連鎖作戰生命週期模型。", "作戰模型 (P45, P51)"],
        ["MTTD / MTTR", "Mean Time To Detect / Remediate", "平均威脅偵測時間（毫秒級）與平均應變處置時間，為衡量護欄與 SOC 監控效能核心 KPI。", "量化指標 (P12, P22, P49)"],
        ["FPR / FNR", "False Positive / False Negative Rate", "護欄誤報率（正常請求被誤攔）與漏報率（惡意請求未被檢測），衡量防禦精準度之核心數據。", "效能平衡 (P12, P31, P40)"]
    ]
    
    add_custom_table(
        slide,
        left=0.80, top=1.72, width=11.733, height=5.15,
        headers=GLOSSARY_HEADERS,
        rows_data=rows,
        col_widths=GLOSSARY_COL_WIDTHS,
        col_alignments=GLOSSARY_COL_ALIGNMENTS,
        font_size=7.8,
        has_card_container=True
    )
    
    add_footer(slide, 1, TOTAL_SLIDES)
