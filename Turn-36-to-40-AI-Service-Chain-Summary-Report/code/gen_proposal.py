#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
國防 AI 服務鏈建置 Proposal（草稿版）
委託群暉科技 (Synology) 建置
"""
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import sys, os

if sys.platform == "win32":
    try: sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
    except: pass

doc = Document()

# ─── Page setup ───
for section in doc.sections:
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

# ─── Default font ───
style = doc.styles['Normal']
font = style.font
font.name = '微軟正黑體'
font.size = Pt(11)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)

# Heading styles
for level in range(1, 5):
    hs = doc.styles[f'Heading {level}']
    hs.font.name = '微軟正黑體'
    hs.element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
    hs.font.color.rgb = RGBColor(0x0A, 0x0F, 0x1E)

doc.styles['Heading 1'].font.size = Pt(22)
doc.styles['Heading 2'].font.size = Pt(16)
doc.styles['Heading 3'].font.size = Pt(13)

def add_p(text, bold=False, size=11, color=None, align=None, space_after=6):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = '微軟正黑體'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
    run.font.size = Pt(size)
    run.bold = bold
    if color: run.font.color.rgb = color
    if align: p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = Pt(size * 1.6)
    return p

def add_bullet(text, level=0, size=10):
    p = doc.add_paragraph(style='List Bullet')
    p.clear()
    run = p.add_run(text)
    run.font.name = '微軟正黑體'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
    run.font.size = Pt(size)
    p.paragraph_format.left_indent = Cm(1.0 + level * 0.8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = Pt(size * 1.5)
    return p

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def make_table(headers, rows, col_widths=None):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header
    for i, h in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True; r.font.size = Pt(9); r.font.name = '微軟正黑體'
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
        set_cell_shading(cell, "0A0F1E")
    # Rows
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = t.rows[ri+1].cells[ci]
            cell.text = val
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(9); r.font.name = '微軟正黑體'
                    r._element.rPr.rFonts.set(qn('w:eastAsia'), '微軟正黑體')
            if ri % 2 == 0: set_cell_shading(cell, "F0F4F8")
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in t.rows:
                row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return t

def add_divider():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run('─' * 60)
    run.font.size = Pt(6)
    run.font.color.rgb = RGBColor(0xB0, 0xBC, 0xCC)

# ════════════════════════════════════════════
# 封面
# ════════════════════════════════════════════
for _ in range(6): doc.add_paragraph()
add_p("國防 AI 服務鏈建置計畫", True, 28, RGBColor(0x0A, 0x0F, 0x1E), WD_ALIGN_PARAGRAPH.CENTER, 12)
add_p("建置提案書（Proposal）草稿版", True, 18, RGBColor(0x00, 0xB4, 0xD8), WD_ALIGN_PARAGRAPH.CENTER, 24)
add_divider()
add_p("委託單位：國家中山科學研究院", False, 14, None, WD_ALIGN_PARAGRAPH.CENTER, 8)
add_p("承辦廠商：群暉科技股份有限公司 (Synology Inc.)", False, 14, None, WD_ALIGN_PARAGRAPH.CENTER, 8)
add_p("文件版本：V0.1 草稿版", False, 12, RGBColor(0x5A, 0x6A, 0x7E), WD_ALIGN_PARAGRAPH.CENTER, 8)
add_p("提案日期：2026 年 9 月", False, 12, RGBColor(0x5A, 0x6A, 0x7E), WD_ALIGN_PARAGRAPH.CENTER, 8)
add_p("文件等級：內部機密", False, 12, RGBColor(0xEF, 0x53, 0x50), WD_ALIGN_PARAGRAPH.CENTER, 8)
doc.add_page_break()

# ════════════════════════════════════════════
# 文件修訂紀錄
# ════════════════════════════════════════════
doc.add_heading('文件修訂紀錄', level=1)
make_table(
    ["版本", "日期", "修訂內容", "作者", "審核"],
    [
        ["V0.1", "2026/09", "初版草稿", "群暉科技 AI 事業部", "待審"],
        ["V1.0", "", "正式提案版", "", ""],
    ],
    [2, 2.5, 5, 3.5, 3]
)
doc.add_page_break()

# ════════════════════════════════════════════
# 目錄（佔位）
# ════════════════════════════════════════════
doc.add_heading('目錄', level=1)
toc_items = [
    "1. 提案摘要",
    "2. 專案背景與目標",
    "3. 群暉科技公司簡介與 AI Agent 經驗",
    "4. 系統架構設計",
    "  4.1 五大安全治理原則",
    "  4.2 六節點縱深防禦架構",
    "  4.3 Harness 治理外框",
    "  4.4 Portal / Gateway 雙管控",
    "5. 建置範圍與工作項目",
    "  5.1 基礎設施層",
    "  5.2 Agent 開發框架",
    "  5.3 資安防護體系",
    "  5.4 合規與標準覆蓋",
    "6. 資安防護設計",
    "  6.1 單向閘道 Diode / DLP / PII",
    "  6.2 Guardrail 五類佈設",
    "  6.3 SOC 監控與熔斷",
    "  6.4 紅隊演練計畫",
    "7. 專案期程與里程碑",
    "8. 專案團隊組成",
    "9. 預期效益與 KPI",
    "10. 費用估算（概估）",
    "11. 風險評估與因應",
    "12. 結論與建議",
    "附件一：AI 國際標準合規對照表",
    "附件二：Harness 選型對照表",
    "附件三：名詞解釋",
]
for item in toc_items:
    indent = item.startswith("  ")
    p = add_p(item.strip(), not indent, 11 if not indent else 10, None, None, 4)
    if indent: p.paragraph_format.left_indent = Cm(1.5)
doc.add_page_break()

# ════════════════════════════════════════════
# 1. 提案摘要
# ════════════════════════════════════════════
doc.add_heading('1. 提案摘要', level=1)
add_p(
    "本提案書係依據　貴院所規劃之「國防 AI 服務鏈」架構藍圖，由群暉科技股份有限公司（以下簡稱「本公司」或「群暉」）"
    "提出之系統建置計畫書。本計畫以五大安全治理原則（模型分層、資料分級、單一閘道、層層防護、全程留痕）為設計基石，"
    "建構涵蓋 AI Portal、AI Gateway、Agent 執行環境、Harness 治理外框、Guardrail 護欄體系、SOC 監控"
    "等完整 AI 服務鏈基礎設施。"
)
add_p(
    "群暉科技具備豐富的企業級儲存、資料安全、以及 AI Agent 開發經驗（DSM Agent），"
    "能將國際級資料安全能力與 AI Agent 開發實務相結合，為　貴院提供從基礎設施到應用層的一站式建置服務。"
)
add_p("本案核心建置目標：", True, 11)
goals = [
    "建構全院統一 AI 服務閘道，消除影子 AI，實現 100% 呼叫經由閘道",
    "部署六節點縱深防禦架構，確保 D2/D3 敏感資料零出境",
    "建立雙軌 Agent 開發框架：開箱即用 Harness（行政庶務）+ 客製化 Harness（武器系統）",
    "落實 Harness 治理外框四項強制功能：工具白名單 · HITL 審批 · 用量上限 · 全程留紀錄",
    "覆蓋四大國際標準支柱：ISO 42001 · NIST AI RMF · OWASP AISVS/LLM Top 10 · MITRE ATLAS",
    "建立 SOC 監控 + 熔斷 + 季度紅隊演練之持續安全運營體系",
]
for g in goals: add_bullet(g)
doc.add_page_break()

# ════════════════════════════════════════════
# 2. 專案背景與目標
# ════════════════════════════════════════════
doc.add_heading('2. 專案背景與目標', level=1)

doc.add_heading('2.1 專案背景', level=2)
add_p(
    "隨著大型語言模型（LLM）與 AI Agent 技術快速發展，各軍事與國防研究機構面臨前所未有的機遇與挑戰。"
    "AI 技術能大幅提升行政效率、知識管理、戰術決策支援等能力，但同時帶來資料外洩、模型幻覺、"
    "越權操作、供應鏈攻擊、影子 AI 等嚴峻安全風險。"
)
add_p(
    "貴院已完成「AI 服務鏈」完整架構規劃，以五大安全治理原則為設計錨點，涵蓋從 Agent 開發流程、"
    "使用者操作流程、到端到端資安防護之全生命週期設計。本公司將依此規劃藍圖，執行系統建置工程。"
)

doc.add_heading('2.2 專案目標', level=2)
objectives = [
    ("統一入口", "建構全院 AI Portal 單一入口 + AI Gateway 單一出口，杜絕旁路直連"),
    ("資料安全", "實施 DISA IL-2 ~ IL-6 分級管控，D2/D3 敏感資料絕對不出院"),
    ("Agent 治理", "部署 Harness 治理外框，Agent 的每一個工具呼叫、每一次寫入操作均受管控"),
    ("合規覆蓋", "全面對標 ISO 42001、NIST AI RMF 1.0、OWASP AISVS/LLM Top 10、MITRE ATLAS"),
    ("持續安全", "建立 SOC 7×24 監控、斷路器熔斷、季度紅隊演練之持續安全運營閉環"),
    ("效率提升", "行政庶務效率提升 60%+，公文撰擬由 8 小時縮短至 1 小時"),
]
for title, desc in objectives:
    add_bullet(f"{title}：{desc}")
doc.add_page_break()

# ════════════════════════════════════════════
# 3. 群暉科技公司簡介
# ════════════════════════════════════════════
doc.add_heading('3. 群暉科技公司簡介與 AI Agent 經驗', level=1)

doc.add_heading('3.1 公司概況', level=2)
add_p(
    "群暉科技股份有限公司（Synology Inc.）成立於 2000 年，總部位於臺灣台北，"
    "是全球領先的網路附加儲存（NAS）及資料管理解決方案供應商。產品銷售遍及全球，"
    "服務超過千萬用戶，涵蓋企業、政府、教育、醫療等領域。"
)
make_table(
    ["項目", "說明"],
    [
        ["公司全名", "群暉科技股份有限公司 (Synology Inc.)"],
        ["成立時間", "2000 年"],
        ["總部地點", "臺灣台北市"],
        ["核心業務", "NAS、SAN、路由器、監控系統、雲端服務、AI 應用"],
        ["全球據點", "美國、英國、法國、德國、日本、澳洲等"],
        ["資安認證", "ISO 27001、SOC 2 Type II、GDPR 合規"],
        ["AI 產品", "DSM Agent、Active Insight、Synology AI Console"],
    ],
    [4, 12]
)

doc.add_heading('3.2 AI Agent 開發經驗', level=2)
add_p(
    "群暉科技已成功開發並商業化部署 DSM Agent — 一套整合於 DiskStation Manager (DSM) 作業系統中的 AI Agent 系統。"
    "DSM Agent 具備以下核心能力："
)
capabilities = [
    "自然語言對話式系統管理：使用者透過對話即可完成儲存配置、備份排程、權限管理等操作",
    "工具呼叫治理：所有系統操作均經由白名單工具執行，高衝擊動作（如刪除磁區、修改權限）需人工確認",
    "多語言支援：支援中、英、日、韓等 20+ 語系",
    "企業級安全：整合 Active Directory/LDAP 認證、RBAC 權限控制、完整操作稽核日誌",
    "Agentic AI 架構實踐：已驗證 Agent 工具呼叫、人機協作（HITL）、沙箱執行等核心模式",
]
for c in capabilities: add_bullet(c)

doc.add_heading('3.3 與本案之契合度', level=2)
add_p("群暉科技在以下面向與本案需求高度契合：")
fits = [
    ("資料安全 DNA", "群暉核心業務即為資料安全儲存，天然具備加密、備份、災難復原、防竄改等能力"),
    ("AI Agent 實戰經驗", "DSM Agent 已驗證 LLM 工具呼叫、HITL 審批、沙箱隔離等本案核心模式"),
    ("Kubernetes 平台能力", "群暉 Scale-Out 產品線具備 K8s 叢集管理經驗，可直接應用於本案算力中心"),
    ("合規經驗", "ISO 27001、SOC 2 Type II 認證經驗可加速本案 ISO 42001 建置"),
    ("國內在地服務", "總部位於臺灣，可提供即時技術支援、安全回應與客製化開發"),
]
for title, desc in fits:
    add_bullet(f"{title}：{desc}")
doc.add_page_break()

# ════════════════════════════════════════════
# 4. 系統架構設計
# ════════════════════════════════════════════
doc.add_heading('4. 系統架構設計', level=1)

doc.add_heading('4.1 五大安全治理原則', level=2)
add_p("本案所有設計決策均錨定於五大安全治理原則，貫穿 AI 服務鏈全生命週期：")
make_table(
    ["原則", "英文", "核心內涵", "關鍵控制措施"],
    [
        ["模型分層", "Model Tiering", "L1通用基礎模型→L2領域DSLM→L3 Agent→L4 Skill/工具→L5知識庫", "T1~T3地端 / T4雲端路由；離線評測後上線"],
        ["資料分級", "Data Classification", "公開IL-2 / 營業秘密IL-4 / 核心IL-5 / 機密IL-6", "C-I-A三元組評定；標籤繼承至RAG切片"],
        ["單一閘道", "Single Gateway", "Portal=單一入口、Gateway=單一出口", "金鑰僅存Gateway密鑰庫；OPA/Rego三維裁決；fail-closed"],
        ["層層防護", "Defense in Depth", "六節點縱深防禦 + 五類Guardrail + 四級沙箱", "HITL interrupt()閘門；對齊ISO 42001 AIMS"],
        ["全程留痕", "Full Auditability", "8欄位不可否認紀錄 + append-only防竄改", "全鏈路trace + SOC即時告警 + 紅隊演練佐證"],
    ],
    [2.2, 2.5, 4.5, 4.8]
)

doc.add_heading('4.2 六節點縱深防禦架構', level=2)
add_p("AI 服務鏈由六個獨立管控節點組成，每一節點皆為獨立安全邊界，任一節點命中規則即阻斷、留跡並告警：")
make_table(
    ["節點", "功能", "安全控制", "合規對標"],
    [
        ["01 邊界防火牆", "NGFW+IPS 預設拒絕白名單放行", "南北向微分段；出向封鎖API直連", "NIST SP 800-41"],
        ["02 使用者 Portal", "SSO+MFA雙因素；會話綁定部門", "上傳掃描+分級標示；提示前置DLP", "ISO 27001 A.5.15"],
        ["03 AI Gateway", "OPA/Rego三維裁決；分級路由", "注入偵測+速率配額；全量留跡；fail-closed", "OWASP LLM01/10"],
        ["04 核心算力", "四層模型堆疊；GPU配額隔離", "模型權重簽章+SBOM；離線評測後上線", "NIST AI RMF"],
        ["05 沙箱/容器", "每次呼叫獨立容器；用後即銷毀", "預設無網路+唯讀；AppArmor+cgroup", "OWASP AISVS C10"],
        ["06 輸出Guardrail", "敏感資訊偵測遮蔽；越級阻斷", "HITL interrupt()核可；輸出加註分級標籤", "OWASP LLM02"],
    ],
    [2.5, 3.5, 4.5, 3.5]
)

doc.add_heading('4.3 Harness 治理外框', level=2)
add_p(
    "Harness 是 Agent 的「治理外框」— 模型負責「想」，Harness 負責「准不准做」。"
    "以下四項強制功能無法關閉、無法改寫，以基礎映像強制注入，比對失敗即拒絕啟動："
)
harness_funcs = [
    ("工具白名單", "AI 能動用哪些工具，須先經審查登記。外部來源之 MCP 工具伺服器一律不採用，全數自建自審"),
    ("重大動作先問人", "對外發送、系統寫入等無法復原之動作，執行前一律停下等候人工核准 (HITL interrupt())"),
    ("用量與成本上限", "單次任務與各單位每日用量皆設上限，異常暴衝自動熔斷，避免失控支出"),
    ("全程留紀錄", "做了什麼、查了哪些資料、產出什麼，完整留存 (append-only)，事後可逐步重建與課責"),
]
for title, desc in harness_funcs:
    add_bullet(f"{title}：{desc}")

doc.add_heading('4.4 Portal / Gateway 雙管控', level=2)
add_p("系統採用 Portal + Gateway 雙管控模型，使用者端與服務端各自獨立管控：")
make_table(
    ["管控面", "控制項目", "說明"],
    [
        ["Portal 側", "單一撤銷點", "一鍵停用部門/模型/Agent"],
        ["Portal 側", "上架審查", "Agent+技能須經安全審查後掛載"],
        ["Portal 側", "用途宣告", "申請時宣告最高資料密級"],
        ["Portal 側", "生命週期收斂", "閒置逾期自動下架"],
        ["Gateway 側", "強制通道", "全院AI僅經Gateway，無直連"],
        ["Gateway 側", "落點路由", "依分級決定地端/圍籬/外部"],
        ["Gateway 側", "流量成本", "逾限降級或拒絕(fail-closed)"],
        ["Gateway 側", "稽核歸屬", "全量留存+部門歸屬計費"],
        ["Gateway 側", "金鑰集中", "用戶端與Agent一律不持有金鑰"],
    ],
    [2.5, 3, 8.5]
)

add_p(
    "RBAC + ABAC 混合授權：角色(管理員/開發者/使用者/審核官) × 屬性(單位/密級/時段/裝置) "
    "動態策略引擎即時評估，越權即鎖。", False, 10
)
doc.add_page_break()

# ════════════════════════════════════════════
# 5. 建置範圍與工作項目
# ════════════════════════════════════════════
doc.add_heading('5. 建置範圍與工作項目', level=1)

doc.add_heading('5.1 基礎設施層', level=2)
infra = [
    "Kubernetes (K8s) 叢集部署與管理 — GPU 節點調度（MI355X / B200 等）",
    "PAM 特權帳號管理系統整合",
    "PQ Tunnel 零信任網路管理平台 — 符合 NIST SP 800-207 零信任架構",
    "單向閘道器 (Diode/CDS) 物理隔離部署",
    "Core Switch / 網路微分段架構",
    "儲存系統部署 — append-only 稽核日誌儲存（群暉 NAS/SAN）",
]
for item in infra: add_bullet(item)

doc.add_heading('5.2 Agent 開發框架', level=2)
add_p("本案建立雙軌 Agent 開發框架，依安全等級分軌：")
make_table(
    ["維度", "開箱即用 Harness", "客製化 Harness"],
    [
        ["代表工具", "Claude Code / Codex / AGY 2.0", "LangChain DeepAgents v0.7"],
        ["適用場景", "行政庶務 Agent", "武器系統 Agent"],
        ["資料密級", "DISA IL-2 ~ IL-4", "DISA IL-5 ~ IL-6"],
        ["權限模式", "內建 Deny-First", "多層 ACL + 四級沙箱"],
        ["HITL 審批", "單層審批", "多層鏈式審批（指揮官+法律官）"],
        ["模型選用", "雲端/地端通用", "僅限地端隔離模型"],
        ["執行隔離", "容器化沙箱", "gVisor / Kata / Firecracker"],
        ["MCP 治理", "標準工具白名單", "自建自審 + 能力憑證"],
        ["合規覆蓋", "基礎合規", "全規範 + 紅隊演練"],
        ["開發週期", "1~2 週", "2~3 個月"],
    ],
    [3, 5.5, 5.5]
)

doc.add_heading('5.3 資安防護體系', level=2)
security_items = [
    "DLP + PII 遮罩引擎 — 身分證號/座標/武器參數/金鑰即時脫敏",
    "Guardrail 五類佈設 — 輸入/檢索/工具動作/輸出/行為迴圈護欄",
    "資料治理五步管線 — 盤點→標籤繼承→政策碼→執行強制→稽核復原",
    "三落點路由判定 — 地端院內/圍籬內VPC/圍籬外雲端",
    "SOC 7×24 監控 — SIEM + 異常偵測 + 斷路器 + Kill Switch",
    "季度紅隊 AI 攻防演練 — 越獄/注入/越權/記憶投毒/沙箱逃逸",
    "SBOM 軟體料件清單管控 — 模型權重簽章 + 依賴套件驗證",
    "8 欄位不可否認稽核紀錄 — append-only 防竄改保存 ≥ 1 年",
]
for item in security_items: add_bullet(item)

doc.add_heading('5.4 合規與標準覆蓋', level=2)
add_p("本案覆蓋四大國際標準支柱，共計 29 項標準與法規：")
make_table(
    ["支柱", "涵蓋標準", "覆蓋範圍"],
    [
        ["ISO 治理框架", "ISO 42001 · 27001 · 27002 · 27017 · 27018 · 27040 · 27701 · 17025", "AI管理系統 + 資安管理 + 雲端安全 + 隱私"],
        ["NIST 風險框架", "AI RMF 1.0 · AI 600-1 · SP 800-53 R5 · 800-218A · 800-171 R3 · CSF 2.0 · AI 100-2 · 800-88", "風險管理 + GenAI剖繪 + 安全控制基線 + CUI保護"],
        ["OWASP 技術風險", "LLM Top 10 · Agentic AI威脅 · AISVS · ML Security · AI Exchange · GenAI紅隊 · 治理檢核", "注入/洩漏/供應鏈 + Agent安全驗證"],
        ["威脅知識庫與法制", "MITRE ATLAS · EU AI Act · CISA/NSA指引 · CNSSI 1253 · DISA CC SRG · 資通安全管理法 · 個資法 · AI基本法", "對抗戰術知識庫 + 法規合規"],
    ],
    [2.5, 5, 6.5]
)
doc.add_page_break()

# ════════════════════════════════════════════
# 6. 資安防護設計
# ════════════════════════════════════════════
doc.add_heading('6. 資安防護設計', level=1)

doc.add_heading('6.1 單向閘道 Diode / DLP / PII', level=2)
add_p("入向管制：", True)
add_bullet("物理單向傳輸 · 深度封包檢測")
add_bullet("外網語料落地隔離區 → 格式正規化：剔除巨集/可執行碼 → 人工抽驗後匯入內網")
add_p("出向管制：", True)
add_bullet("機敏資料絕對禁止離開內網，禁止送往公有雲模型")
add_bullet("所有出向 → DLP + PII 遮罩檢核 → 嚴禁任何形式繞道直連")
add_p("三落點路由：", True)
make_table(
    ["落點", "可存放資料", "限制條件"],
    [
        ["A 地端院內機房", "D0~D3 皆可", "D3僅限實體隔離網域；本院自建模型"],
        ["B 圍籬內雲端(VPC)", "D0/D1可；D2須逐案核可", "CMEK/EKM自管金鑰；服務邊界限制"],
        ["C 圍籬外雲端", "不存放本院任何資料", "僅供D0+去識別化D1；契約零資料保留"],
    ],
    [3.5, 4, 6.5]
)

doc.add_heading('6.2 Guardrail 五類佈設', level=2)
make_table(
    ["護欄類型", "佈設位置", "檢核內容"],
    [
        ["輸入護欄", "Gateway + Harness", "身分檢核 · Prompt Injection偵測 · 輸入長度限制"],
        ["檢索護欄", "RAG Pipeline", "依密級過濾索引 · 剝除文件夾帶指令 · 標記為不可信"],
        ["工具/動作護欄", "Harness Middleware", "工具白名單 · Schema驗證 · 副作用範圍檢查"],
        ["輸出護欄", "Gateway + Harness", "有害內容過濾 · DLP掃描 · 引用比對 · 去指令化"],
        ["行為/迴圈護欄", "Harness Runtime", "步數/代幣/成本上限 · 重複動作偵測 · 逾限熔斷"],
    ],
    [2.5, 3, 8.5]
)
add_p(
    "處置矩陣五種判定：放行(allow) · 去識別(redact) · 改寫重試(rewrite) · 阻斷(block) · 轉人工(escalate)。"
    "設計原則：檢查器不可用或逾時，一律視為不通過 (fail-closed)。", False, 10
)

doc.add_heading('6.3 SOC 監控與熔斷', level=2)
make_table(
    ["層次", "功能", "具體措施"],
    [
        ["資料蒐集", "日誌集中化", "Agent執行日誌 · Gateway紀錄 · DLP告警 · HITL審批日誌"],
        ["SIEM 分析", "關聯分析+ML偵測", "UEBA行為分析 · 威脅情資整合 · 時序異常識別"],
        ["偵測告警", "即時告警", "異常頻率 · 跨密級存取 · 越權調用 · Prompt Injection"],
        ["熔斷回應", "自動切斷", "Circuit Breaker · Kill Switch · 即拋環境銷毀 · 憑證凍結"],
        ["事後調查", "根因分析", "完整對話還原 · 決策鏈追溯 · 紅隊語料庫擴充"],
    ],
    [2.5, 3, 8.5]
)

doc.add_heading('6.4 紅隊演練計畫', level=2)
add_p("每季度執行 AI 紅隊攻防演練，測試項目包括：")
red_team = [
    "越獄提示攻擊 (Jailbreak Prompt)",
    "間接提示注入 (Indirect Prompt Injection)",
    "工具越權測試 (Tool Privilege Escalation)",
    "跨密級存取試探 (Cross-Classification Access)",
    "記憶投毒 (Memory Poisoning)",
    "沙箱逃逸 (Sandbox Escape)",
]
for item in red_team: add_bullet(item)
add_p(
    "量測指標：機密洩漏率 · 越獄成功率 · 誤攔率(FPR) · 引用覆蓋率 · 延遲預算。"
    "每次更版以固定測試集重跑比對，每月抽樣人工複核。", False, 10
)
doc.add_page_break()

# ════════════════════════════════════════════
# 7. 專案期程
# ════════════════════════════════════════════
doc.add_heading('7. 專案期程與里程碑', level=1)
add_p("本案分四階段推動，總期程約 12 個月：")
make_table(
    ["階段", "期程", "關鍵里程碑", "交付物"],
    [
        ["Q1\n基礎防禦網", "第1-3月", "• Control Gateway MVP上線\n• 資料分級D0~D3定案\n• 稽核紀錄格式發布\n• 單向Diode閘道部署\n• SSO+MFA基礎認證\n• Harness基礎映像準備", "系統架構文件\nGateway MVP\n分級標準書\n稽核格式規範"],
        ["Q2\n單位先導", "第4-6月", "• AI Portal首版上線\n• 先導單位隔離驗證\n• 首批庶務Agent PoC\n• 開箱即用Harness部署\n• 可觀測性平台建置\n• 資安契約範本", "Portal系統\nAgent PoC報告\nHarness部署手冊\n可觀測性儀表板"],
        ["Q3\nAI助理串聯", "第7-9月", "• 跨所AI助理協作上線\n• 跨單位調用核准流程\n• 雲端圍籬整合\n• 客製化Harness框架\n• DeepAgents武器系統試點\n• SOC SIEM全功能上線", "串聯測試報告\n客製化Harness\nSOC運營手冊\n紅隊演練計畫"],
        ["Q4\n全院合規", "第10-12月", "• 全院單位完成接取\n• 關閉舊有直連端點\n• ISO 42001內部稽核\n• 季度紅隊演練啟動\n• 全規範合規矩陣\n• 影子AI完全收斂", "合規稽核報告\n紅隊演練報告\n系統驗收報告\n運維移交文件"],
    ],
    [2, 2, 5, 5]
)
doc.add_page_break()

# ════════════════════════════════════════════
# 8. 專案團隊
# ════════════════════════════════════════════
doc.add_heading('8. 專案團隊組成', level=1)
add_p("群暉科技將組建以下專案團隊：")
make_table(
    ["角色", "人數", "職責", "資格要求"],
    [
        ["專案經理", "1", "專案統籌、進度管控、客戶溝通", "PMP認證；10年+IT專案經驗"],
        ["系統架構師", "2", "整體架構設計、技術決策", "K8s/雲端架構師認證；AI系統經驗"],
        ["AI 工程師", "4", "Agent開發、Harness客製、模型整合", "LLM/Agent開發經驗；Python/JS"],
        ["資安工程師", "2", "安全架構、Guardrail、紅隊演練", "CISSP/CEH；ISO 27001稽核員"],
        ["DevOps 工程師", "2", "K8s部署、CI/CD、監控", "CKA認證；容器安全經驗"],
        ["儲存工程師", "1", "NAS/SAN部署、稽核日誌儲存", "群暉認證工程師"],
        ["品保工程師", "1", "測試驗證、合規稽核", "ISTQB認證；安全測試經驗"],
        ["技術文管", "1", "文件撰寫、交付物管理", "技術寫作經驗"],
    ],
    [2.5, 1.5, 4.5, 5.5]
)
add_p("總計 14 人投入，依階段動態調整。", False, 10)
doc.add_page_break()

# ════════════════════════════════════════════
# 9. 預期效益與 KPI
# ════════════════════════════════════════════
doc.add_heading('9. 預期效益與 KPI', level=1)
make_table(
    ["KPI 指標", "目標值", "衡量方式"],
    [
        ["閘道覆蓋率", "100%", "全院AI呼叫經Gateway，無直連端點殘留"],
        ["資料出境事件", "0 件", "D2/D3資料零出境；DLP+PII全攔截"],
        ["合規覆蓋率", "100%", "ISO 42001全項覆蓋；NIST AI RMF完整對標"],
        ["作業效率提升", "↑ 60%", "公文8hr→1hr；報表4hr→30min"],
        ["越獄成功率", "< 1%", "紅隊演練越獄攻擊成功率"],
        ["誤攔率(FPR)", "< 5%", "Guardrail誤判阻斷合法請求比率"],
        ["影子AI收斂", "100%", "全院無未經授權之AI使用"],
    ],
    [3, 2.5, 8.5]
)

add_p("風險降低評估：", True)
make_table(
    ["風險類別", "防護前", "防護後", "降低幅度", "主要控制措施"],
    [
        ["資料外洩", "極高", "低", "↓ 90%", "Diode+DLP+PII+三落點路由"],
        ["Prompt Injection", "高", "極低", "↓ 95%", "Guardrail+格式正規+fail-closed"],
        ["越權操作", "高", "無", "↓ 100%", "Deny-First+HITL+四級沙箱+白名單"],
        ["模型幻覺", "中", "低", "↓ 70%", "事實驗證+引用比對+輸出護欄"],
        ["供應鏈攻擊", "中", "低", "↓ 80%", "MCP自建自審+SBOM+簽章驗證"],
        ["影子 AI", "高", "無", "↓ 100%", "Gateway強制通道+直連封鎖"],
    ],
    [2.5, 2, 2, 2, 5.5]
)
doc.add_page_break()

# ════════════════════════════════════════════
# 10. 費用估算
# ════════════════════════════════════════════
doc.add_heading('10. 費用估算（概估）', level=1)
add_p("以下為初步概估，實際費用將依詳細需求訪談後調整：", False, 10, RGBColor(0xEF, 0x53, 0x50))
make_table(
    ["項目", "內容說明", "概估費用（萬元）", "備註"],
    [
        ["基礎設施", "K8s叢集 · PAM · PQ Tunnel · Diode · NAS/SAN", "依實際採購", "含硬體+軟體授權"],
        ["平台開發", "AI Portal · AI Gateway · 管理後台", "待議", "含UI/UX設計"],
        ["Harness 框架", "開箱即用整合 + DeepAgents客製化", "待議", "含三種OOB Harness整合"],
        ["資安防護", "DLP · Guardrail · SOC · 紅隊演練", "待議", "含SIEM平台建置"],
        ["合規建置", "ISO 42001導入 · 稽核體系 · 文件", "待議", "含外部稽核費用"],
        ["教育訓練", "管理員 · 開發者 · 使用者培訓", "待議", "含教材編撰"],
        ["維運服務", "年度維運 · SLA · 技術支援", "待議", "含7×24 on-call"],
        ["", "", "", ""],
        ["合計", "", "待詳細需求訪談後提供", ""],
    ],
    [2.5, 5, 3, 3.5]
)
add_p("註：以上費用不含硬體採購費用，硬體規格將於需求訪談後另行報價。", False, 9, RGBColor(0x5A, 0x6A, 0x7E))
doc.add_page_break()

# ════════════════════════════════════════════
# 11. 風險評估
# ════════════════════════════════════════════
doc.add_heading('11. 風險評估與因應', level=1)
make_table(
    ["風險項目", "影響程度", "發生機率", "因應策略"],
    [
        ["LLM模型更新導致相容性問題", "中", "高", "抽象化模型介面層；版本凍結+漸進升級策略"],
        ["國際標準版本更新", "低", "中", "模組化合規框架；預留擴充介面"],
        ["專案人員異動", "中", "低", "完整知識移轉文件；交叉訓練機制"],
        ["硬體交期延遲", "高", "中", "分階段部署；替代方案預備"],
        ["安全漏洞揭露", "高", "中", "即時回應流程；緊急補丁SLA < 24hr"],
        ["使用者抗拒變革", "中", "中", "漸進式推廣；種子使用者培訓；成效展示"],
    ],
    [3.5, 2, 2, 6.5]
)
doc.add_page_break()

# ════════════════════════════════════════════
# 12. 結論
# ════════════════════════════════════════════
doc.add_heading('12. 結論與建議', level=1)
add_p(
    "本提案書完整呈現了群暉科技針對　貴院「國防 AI 服務鏈」之建置計畫。"
    "我們將以五大安全治理原則為設計錨點，結合群暉在資料安全儲存與 AI Agent 開發的雙重優勢，"
    "為　貴院打造符合國際標準、具備縱深防禦能力的 AI 服務基礎設施。"
)
add_p("核心價值主張：", True)
values = [
    "資料安全 DNA：群暉核心業務即為資料安全，天然具備加密、備份、防竄改等能力，與本案安全治理高度契合",
    "AI Agent 實戰驗證：DSM Agent 已驗證 LLM 工具呼叫、HITL、沙箱等核心模式，非紙上談兵",
    "一站式服務：從基礎設施（K8s、NAS/SAN、網路）到應用層（Portal、Gateway、Harness）全棧覆蓋",
    "在地化優勢：臺灣總部，可提供即時技術支援、安全回應與客製化開發，無需依賴海外團隊",
    "合規加速：ISO 27001 + SOC 2 認證經驗，可加速本案 ISO 42001 AIMS 導入",
]
for v in values: add_bullet(v)

add_p("")
add_p("建議下一步行動：", True)
next_actions = [
    "即刻啟動：安排需求訪談會議，確認詳細規格與優先順序",
    "30 天內：完成正式提案書 V1.0 + 詳細費用估算",
    "60 天內：簽訂合約，啟動 Q1 基礎防禦網建置",
]
for a in next_actions: add_bullet(a)

add_p("")
add_p(
    "群暉科技期待與　貴院攜手，共同建構安全、合規、高效的國防 AI 服務鏈。",
    True, 12, RGBColor(0x00, 0xB4, 0xD8)
)
doc.add_page_break()

# ════════════════════════════════════════════
# 附件
# ════════════════════════════════════════════
doc.add_heading('附件一：AI 國際標準合規對照表', level=1)
add_p("（詳見總結報告第 12 頁「AI 國際標準與法規合規全覽」）", False, 10, RGBColor(0x5A, 0x6A, 0x7E))
make_table(
    ["支柱", "標準名稱", "適用範圍", "本案對應"],
    [
        ["ISO", "ISO/IEC 42001", "AI管理系統(AIMS)", "全案治理框架"],
        ["ISO", "ISO/IEC 27001", "資安管理", "SOC+稽核體系"],
        ["NIST", "AI RMF 1.0", "GOVERN/MAP/MEASURE/MANAGE", "風險管理流程"],
        ["NIST", "AI 600-1", "GenAI剖繪12類風險", "Agent風險評估"],
        ["NIST", "SP 800-53 R5", "安全控制基線", "技術控制措施"],
        ["NIST", "SP 800-207", "零信任架構", "PQ Tunnel/ZTA"],
        ["OWASP", "LLM Top 10", "注入/洩漏/供應鏈", "Guardrail設計"],
        ["OWASP", "AISVS", "AI安全驗證標準", "安全測試基準"],
        ["MITRE", "ATLAS", "AI對抗戰術知識庫", "紅隊演練依據"],
        ["法規", "資通安全管理法", "A級機關防護基準", "合規基線"],
    ],
    [2, 3, 4, 5]
)

doc.add_heading('附件二：名詞解釋', level=1)
make_table(
    ["縮寫", "全稱", "說明"],
    [
        ["LLM", "Large Language Model", "大型語言模型"],
        ["HITL", "Human-in-the-Loop", "人機協作審批機制"],
        ["DLP", "Data Loss Prevention", "資料外洩防護"],
        ["PII", "Personally Identifiable Information", "個人可識別資訊"],
        ["MCP", "Model Context Protocol", "模型上下文協議"],
        ["OPA", "Open Policy Agent", "開放策略代理"],
        ["RBAC", "Role-Based Access Control", "角色型存取控制"],
        ["ABAC", "Attribute-Based Access Control", "屬性型存取控制"],
        ["SOC", "Security Operations Center", "安全營運中心"],
        ["SIEM", "Security Information & Event Mgmt", "安全資訊與事件管理"],
        ["SBOM", "Software Bill of Materials", "軟體料件清單"],
        ["ZTA", "Zero Trust Architecture", "零信任架構"],
        ["PAM", "Privileged Access Management", "特權帳號管理"],
        ["VFS", "Virtual File System", "虛擬檔案系統"],
        ["K8s", "Kubernetes", "容器編排平台"],
        ["DSM", "DiskStation Manager", "群暉磁碟管理系統"],
    ],
    [2, 5.5, 6.5]
)

# ─── Save ───
out = r"D:\JavaDO\國防AI服務鏈建置Proposal_草稿版.docx"
doc.save(out)
print(f"✅ Proposal 草稿已生成：{out}")
