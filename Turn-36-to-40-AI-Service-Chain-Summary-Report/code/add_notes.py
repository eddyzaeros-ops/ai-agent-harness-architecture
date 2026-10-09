#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
為總結報告_最終版.pptx 的每一頁加上備忘稿 (Speaker Notes)
策略：讀取現有 PPTX，僅追加備忘稿，不更動任何投影片內容與樣式
"""

from pptx import Presentation
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

input_path = r"d:\JavaDO\總結報告_最終版.pptx"
prs = Presentation(input_path)
print(f"已載入 {input_path}，共 {len(prs.slides)} 頁")

# ─── 每一頁的備忘稿內容 ───
notes = {
    # === 主體篇 Slide 1~17 ===
    1: """【封面】
報告名稱：國防 AI 服務鏈總結報告
研析引擎：先以 Claude Opus 4.6 (Thinking) 進行深度研析與主體篇撰寫，再以 Gemini 3.1 Pro 進行補強與 Review。

開場說明要點：
• 本報告以「AI 服務鏈資料流」為核心視角，完整涵蓋從 Agent 開發到使用者操作、資安防護到建置藍圖的全生命週期。
• 所有設計決策均錨定於五大安全治理原則：模型分層、資料分級、單一閘道、層層防護、全程留痕。
• 報告整合了「AI Agent Harness 整合提報版 20260906」的完整內容，並額外補強了硬體基礎設施 (K8s/PAM)、護欄時序、SBOM 供應鏈安全與零信任架構。""",

    2: """【目錄】
本報告分為兩大部分：
一、主體篇 (Slide 3~17)：共 14 個章節，涵蓋五大原則、全景架構、Agent 開發者流程、使用者流程、四大資安防護面向、Roadmap 與效益評估。
二、補充篇 (Slide 18~23)：針對 Gemini 3.1 Pro Review 後發現之不足，補強硬體實體架構 (K8s/PAM/PQ Tunnel)、護欄運作循序流程、SBOM 供應鏈管控、ZTA 七大支柱映射與 AI 自動化紅隊演練，以及全案總結論。

提報建議：可依長官關注面向，選擇性深入說明特定章節。""",

    3: """【五大原則總覽】
這五大原則是整份報告的「設計公理」，後續每一頁的架構決策都可回溯至此：

1. 模型分層 (Model Tiering)：
   - L1 基礎模型 → L2 領域 DSLM → L3 Agent → L4 Skill/MCP → L5 RAG 知識庫
   - 各層風險面不同，須分別施加對應的安全控制

2. 資料分級 (Data Classification)：
   - 採用 CNSSI 1253 影響等級評定方法與 DISA CC SRG IL2~IL6 對照
   - 以 C-I-A 三元組 (機密性/完整性/可用性) 取代傳統單一密級

3. 單一閘道 (Single Gateway)：
   - Portal = 唯一入口，Gateway = 唯一出口
   - 金鑰僅存 Gateway 密鑰庫，防火牆封鎖所有 API 直連

4. 層層防護 (Defense in Depth)：
   - 六節點縱深：防火牆→Portal→Gateway→算力→沙箱→Guardrail
   - Harness 治理外框橫跨 L1~L5 五層

5. 全程留痕 (Full Auditability)：
   - 8 欄位 append-only 不可否認稽核紀錄，保存 ≥ 1 年
   - 串接 SOC 即時監控與斷路器熔斷機制""",

    4: """【AI 服務鏈全景架構 — 六節點縱深防禦】
本頁對應整合提報版 Slide 5「AI 服務鏈系統架構與管控節點」。

六節點設計原則：
① 邊界防火牆：NGFW+IPS，預設拒絕，出向封鎖模型 API 直連，與 Diode 單向閘道銜接
② 使用者 Portal：SSO+MFA，上傳掃描+分級標示，禁跨部門歷史檢視
③ AI Gateway：OPA/Rego 三維裁決 (身分×分級×用途)，金鑰集中，fail-closed
④ 核心算力：四層模型堆疊，模型權重簽章驗證+SBOM，部門 GPU 配額隔離
⑤ 沙箱/容器：每次呼叫獨立容器用後即銷毀，MCP 自建自審白名單
⑥ 輸出 Guardrail：敏感資訊遮蔽，越級阻斷，HITL interrupt() 核可

關鍵設計：前一節點失效不得使後續節點失守（縱深獨立性原則）。
Harness 治理外框橫跨五層，以基礎映像強制注入，比對失敗即拒絕啟動。""",

    5: """【Agent 開發者 — 行政庶務 Agent（開箱即用 Harness）】
適用場景：公文撰擬、會議摘要、知識問答、報表產製
安全等級：DISA IL-2 ~ IL-4

三大開箱即用 Harness 選項：
1. Claude Code (Anthropic)：內建 Harness 治理外框、自帶 HITL 審批、檔案系統權限控制
2. OpenAI Codex (OpenAI)：內建程式碼沙箱、工具呼叫標準化、輸入/輸出護欄預置
3. Google Antigravity 2.0 (DeepMind)：子 Agent 委派+隔離、虛擬檔案系統 (VFS)、可觀測性追蹤

這些工具的共同特點是自帶完整的安全治理框架，開發者不需從零建構 Harness，可快速部署。
開發週期約 1~2 週。

共通管控要求：
• Harness 以基礎映像強制注入，比對失敗拒絕啟動
• MCP 伺服器一律自建自審
• 工具採白名單
• 高衝擊動作強制 HITL""",

    6: """【Agent 開發者 — 武器系統 Agent（客製化 Harness）】
適用場景：戰術決策支援、情資分析、武器效能評估
安全等級：DISA IL-5 ~ IL-6

採用 LangChain DeepAgents v0.7 進行客製化開發：
① 三層堆疊：Runtime (LangGraph) → Framework (LangChain) → Harness (DeepAgents)
② Context Engineering：CompositeBackend (VFS) 大檔案卸載，read_file(offset,limit) 精準讀取
③ 強化權限+沙箱：L0語言層→L1程序層→L2容器→L3微虛擬機 (gVisor/Kata/Firecracker)
④ 多層 HITL：武器決策→指揮官→法律官 鏈式審批
⑤ 全規範合規：ISO 42001、NIST AI RMF、OWASP AISVS、MITRE ATLAS

開發週期約 2~3 個月。

Harness 選型對照表 9 維度：
代表工具、適用場景、資料密級、權限模式、HITL 審批、模型選用、執行隔離、MCP 治理、合規覆蓋、開發週期""",

    7: """【Agent 開發者 — Harness 治理外框與管控軌跡】
本頁對應整合提報版 Slide 7-8「Harness 貫穿五層防護」與「Harness 治理外框」。

Harness 四項強制功能（無法關閉、無法改寫）：
1. 工具白名單：外部 MCP 一律不採用，全數自建自審
2. 重大動作先問人：無法復原之動作一律 HITL interrupt()
3. 用量與成本上限：異常暴衝自動熔斷
4. 全程留紀錄：append-only，事後可逐步重建與課責

L1~L5 五層防護：
• L5 知識庫：檢索標記不可信、密級過濾、DLP 比對
• L4 技能/MCP：簽章白名單、Schema 驗證、沙箱執行
• L3 Agent：迴圈步數熔斷、部門隔離、HITL 閘門
• L2 DSLM：語料核可清單、評測門檻 gating
• L1 基礎模型：雜湊驗簽、系統提示凍結唯讀

8 欄位稽核：請求ID、身分/租戶、模型版本、遮罩提示詞、RAG來源、工具呼叫、HITL核可、處置結果""",

    8: """【Agent 使用者 — Portal 到 Agent 的 11 步資料流】
本頁對應整合提報版 Slide 4「使用者資料流全景」。

11 步資料流：
① 登入並提出需求 → ② 身分驗證與角色套用 → ③ 組裝請求 (範本+語料+分級標記) → ④ Gateway 身分與部門識別 → ⑤ 分級檢核與注入防護 → ⑥ 模型路由與出境判定 → ⑦ 推論/工具執行/向量檢索 → ⑧ 輸出過濾與來源標註 → ⑨ 稽核落檔 (唯讀累加) → ⑩ 回應呈現與引用標示 → ⑪ 使用者取得回應

HITL 人機審批流程 (高衝擊動作)：
Agent 提議 → Harness 攔截 (interrupt_on) → Checkpointer 保存斷點 → Portal 呈現決策軌跡 → 人工 approve/edit/reject → Command(resume=...) 恢復執行

使用者端管控：
• Portal：上架審查、密級宣告、閒置逾期自動下架
• Gateway：OPA 三維裁決、金鑰集中、fail-closed
• 隔離：thread_id 會話隔離、namespace 多租戶""",

    9: """【Agent 使用者 — 操作管控與軌跡紀錄】
本頁對應整合提報版 Slide 6「Portal/Gateway 為單一控制點之管控」。

Portal 側管控：
• 單一撤銷點：一鍵停用部門/模型/Agent
• 上架審查：Agent+技能須經安全審查後掛載
• 使用可視化：用量/成本/拒絕率儀表板
• 生命週期收斂：閒置逾期自動下架

Gateway 側強制 (G1~G4)：
• G1 強制通道+金鑰集中
• G2 落點路由（依分級決定地端/圍籬/外部）
• G3 流量成本 fail-closed
• G4 稽核歸屬計費

fail-closed 設計原則：
• 檢查器不可用或逾時→一律不通過
• 請求未匹配核准政策→一律拒絕
• HITL 逾時→預設拒絕

處置矩陣五種判定：放行(allow)、去識別(redact)、改寫重試(rewrite)、阻斷(block)、轉人工(escalate)""",

    10: """【資安防護（一）：單閘 Diode · DLP · 落點路由】
三大防護面向：

一、單向閘道器 (Diode/CDS)：
• 入向：物理單向傳輸、深度封包檢測、外網語料落地隔離區、格式正規化剔除巨集
• 出向：機敏資料絕對禁止離開內網、禁止送往公有雲模型

二、DLP + PII 遮罩引擎：
• 即時內容掃描：機敏關鍵字/正則/ML 分類器/文件指紋/影像 OCR
• PII 遮罩：身分證號/電話/軍事座標/武器參數/金鑰 → 自動脫敏或即時阻斷

三、三落點路由判定（對應整合提報版 Slide 16）：
• A 地端院內機房：D0~D3 皆可存放，D3 僅限實體隔離
• B 圍籬內雲端 (VPC)：D0/D1 可存放，D2 須逐案核可，CMEK/EKM 金鑰自管
• C 圍籬外雲端：不存放任何本院資料，僅供 D0 + 去識別化 D1

判定原則：以「資料被送到哪一區」認定落點，而非 AI 服務位於何處。就近且從嚴。""",

    11: """【資安防護（二）：資料治理管線 · Guardrail 五類佈設】
本頁對應整合提報版 Slide 11-12, 15。

Agentic 資料安全管控五步路徑（Slide 15）：
01 資料盤點與分級 → 02 標籤綁定與繼承 → 03 政策即程式碼 (OPA/Rego) → 04 執行期強制點 → 05 稽核與復原

Guardrail 五類佈設點（Slide 11）：
• 輸入護欄：身分+部門檢核、Prompt Injection 偵測
• 檢索護欄：依密級過濾索引、剝除文件夾帶指令語意
• 工具/動作護欄：MCP 白名單、參數 Schema 驗證
• 輸出護欄：結構驗證、有害內容過濾、DLP、引用比對、去指令化
• 行為/迴圈護欄：步數/代幣/成本上限、逾限熔斷

同一組規則於 Gateway (集中) 與 Harness (單一 Agent) 雙點佈設。
兩段式檢查：確定性規則先行，僅灰區交由模型評審。

不可退讓之架構紅線：
• 隔離邊界不得因 Agent 專案而開孔
• 敏感級以上資料不得送往雲端模型
• 高衝擊動作必經 HITL
• MCP 一律自建自審""",

    12: """【AI 國際標準與法規合規全覽】
本頁對應整合提報版 Slide 2「AI 治理規範總覽」與 Slide 13「資料安全法規」。

四大支柱共 29 項標準：

支柱一：ISO 治理框架
ISO/IEC 42001 (AIMS)、27001/27002、27017/27018 (雲端)、27040 (儲存)、27701 (PIMS)、17025 (稽核)

支柱二：NIST 風險框架
AI RMF 1.0 (四大功能)、AI 600-1 (GenAI 12類風險)、SP 800-53 R5、SP 800-218A (SSDF)、SP 800-171 R3 (CUI)、CSF 2.0、AI 100-2 (對抗式ML)、SP 800-88 (媒體銷毀)

支柱三：OWASP 技術風險
LLM Top 10 (2025)、Agentic AI 威脅、AISVS (分級查核)、ML Security Top 10、AI Exchange、GenAI Red Teaming、LLM 治理檢核

支柱四：威脅知識庫與法制
MITRE ATLAS、EU AI Act、CISA/NSA 指引、CNSSI 1253、DISA CC SRG、資通安全管理法、個資法、AI 基本法

落地主軸：治理制度 (ISO 42001) → 風險流程 (NIST AI RMF) → 技術控制 (OWASP) → 威脅驗證 (MITRE ATLAS) → 稽核佐證 (ISO 17025/27001)""",

    13: """【資安防護（四）：SOC 監控 · 熔斷 · 紅隊演練】
五層 SOC 架構：

1. 資料蒐集：Agent 日誌、Gateway 紀錄、DLP 告警、模型調用、HITL 審批日誌
2. SIEM 分析：關聯分析、ML 異常偵測、UEBA 使用者行為分析、威脅情資整合
3. 偵測告警：異常頻率、跨密級存取、越權調用、Prompt Injection、資料外洩嘗試
4. 熔斷回應：Circuit Breaker 自動熔斷、Kill Switch 緊急停止、即拋式環境銷毀、憑證凍結
5. 事後調查：完整對話還原、決策鏈追溯、工具呼叫重放、根因分析、紅隊語料庫擴充

季度紅隊演練涵蓋：越獄提示攻擊、間接提示注入、工具越權測試、跨密級存取試探、記憶投毒、沙箱逃逸
量測指標：機密洩漏率、越獄成功率、誤攔率(FPR)、引用覆蓋率、延遲預算
每次更版須以固定測試集重跑比對前版，並每月抽樣人工複核。""",

    14: """【AI 資安防護端到端工作流程】
本頁為全案資安防護的鳥瞰圖，將所有防護機制串接為一條完整的防護鏈：

外網資料源 → Diode 單向閘道 → 落地隔離區 → 惡意掃描/格式正規 → DLP/PII 遮罩 → 資料治理五步管線 → Guardrail 五類佈設 → Agent 執行層 → Guardrail 輸出護欄 → DLP 出向檢核 → 使用者交付

全程由 SOC 7×24 持續監控：SIEM、異常偵測、斷路器熔斷、Kill Switch、紅隊演練、稽核留痕

16 項完整檢核清單涵蓋：
☑ 單向閘道 ☑ 惡意掃描 ☑ DLP 掃描 ☑ PII 遮罩 ☑ 資料五步管線 ☑ OPA 三維授權
☑ Guardrail 五類 ☑ 處置矩陣 ☑ 四級沙箱 ☑ HITL ☑ fail-closed ☑ Harness 四項強制
☑ 三落點路由 ☑ 8 欄位稽核 ☑ SOC 斷路器 ☑ 紅隊演練

合規覆蓋：ISO 42001、NIST AI RMF 1.0、AI 600-1、SP 800-53、OWASP AISVS、LLM Top 10、MITRE ATLAS、DISA IL、EU AI Act""",

    15: """【AI 服務鏈 Roadmap — 四階段建置期程】
本頁對應整合提報版 Slide 18「導入藍圖與成效衡量」。

Q1 基礎防禦網：
• Control Gateway 最小可行版上線
• 資料分級 D0~D3 定案+機器判讀
• 稽核紀錄格式與留存政策發布
• 單向 Diode 閘道部署、SSO+MFA、Harness 基礎映像

Q2 單一部門先導：
• AI Portal 首版（模型+工具目錄）
• 先導單位隔離驗證
• 首批行政庶務 Agent PoC (開箱即用 Harness)
• 可觀測性平台建置

Q3 AI 助理串聯：
• 跨所 AI 助理協作上線
• 雲端圍籬+閘道事件回送整合
• 客製化 Harness 框架建立 (DeepAgents)
• SOC SIEM 全功能上線

Q4 全院合規上線：
• 全院單位完成接取
• 關閉舊有直連端點
• ISO 42001 內部稽核+管理審查
• 季度紅隊演練啟動

年度 KPI：100% 閘道覆蓋 · 0 件 D2/D3 出境 · 影子 AI 收斂""",

    16: """【效益評估與 KPI 指標】
四大 KPI 指標：

1. 閘道覆蓋率 100%：全院 AI 呼叫經 Gateway，無直連殘留，影子 AI 完全收斂
2. 資料出境事件 0 件：D2/D3 資料零出境，DLP+PII 全攔截，越權 100% 阻斷
3. 合規覆蓋率 100%：ISO 42001 全項、NIST AI RMF 完整對標、OWASP AISVS 分級通過
4. 作業效率提升 60%：公文 8hr→1hr、報表 4hr→30min、知識檢索 ×10

風險降低矩陣：
• 資料外洩：極高→低 (↓90%)，主要控制：Diode+DLP+PII+三落點路由
• Prompt Injection：高→極低 (↓95%)，主要控制：Guardrail+格式正規+fail-closed
• 越權操作：高→無 (↓100%)，主要控制：Deny-First+HITL+四級沙箱+白名單
• 模型幻覺：中→低 (↓70%)，主要控制：事實驗證+引用比對+輸出護欄
• 供應鏈攻擊：中→低 (↓80%)，主要控制：MCP自建自審+SBOM+簽章驗證
• 影子 AI：高→無 (↓100%)，主要控制：Gateway強制通道+直連封鎖""",

    17: """【結論與下一步行動】
本頁為主體篇的收尾。

10 項關鍵研究成果：
✅ 五大原則驅動架構設計 ✅ Harness 治理外框 ✅ 開箱即用 vs 客製化雙軌
✅ 11 步資料流 ✅ 16 項檢核清單 ✅ 國際標準 29 項
✅ Guardrail 五類+fail-closed ✅ SOC+紅隊+8欄位 ✅ 三落點+OPA
✅ Roadmap+KPI

行動建議：
• 即刻：Gateway 最小可行版 + 資料分級定案
• 30 天：首批庶務 Agent PoC + 稽核政策發布
• 90 天：Portal 首版上線 + Guardrail + SOC
• 180 天：DeepAgents 客製化 + ISO 42001 稽核

接下來翻至補充篇，深入說明硬體基礎設施、護欄時序、供應鏈安全與零信任架構。""",

    # === 補充篇 Slide 18~23 ===
    18: """【補充篇過場頁】
本節為 Gemini 3.1 Pro Review 後補強的四大進階主題。

補強背景：
主體篇已完整建構邏輯架構與管控流程，但經 Review 後發現以下面向可進一步深化：
1. 硬體與網路層面的實體防護（K8s 容器排程、PAM 特權管控、PQ Tunnel 後量子零信任）
2. 護欄服務的具體運作時序（如何做到 Input/Output 雙向攔截）
3. 軟體供應鏈安全（SBOM 料件清單管控、MCP 工具的零信任授權機制）
4. 國防部零信任架構的七大支柱對齊，以及 AI 驅動的自動化紅隊演練

這四個補強項目均已交叉覆蓋五大原則，形成完整的防護矩陣（詳見最後一頁結論）。""",

    19: """【補充 01：硬體實體架構與零信任網路】
本頁依據「圖 73 資安方案與本案架構說明」設計，對映至真實的網路與硬體拓樸。

核心交換層：
• Core Switch 以 100Gbps / 400Gbps Ethernet 建構高速骨幹
• 導入 PQ Tunnel（後量子密碼學）零信任網路管理平台，完全符合 NIST SP 800-207 ZTA 標準
• 確保即使未來量子電腦成熟，通道加密仍不會被破解

四區隔離設計：
1. 資料清洗區：單向閘道器 (Diode) 搭配清洗節點，負責外網資料過濾與格式正規化
2. 算力資源區：以 Kubernetes (K8s) 進行容器化排程與資源隔離；搭載 Liquid-Cooled AMD MI355X 與 NVIDIA HGX B200；啟用 TEE 機密運算保護運行中的模型權重（即使維運人員也無法從記憶體 Dump 模型）
3. 存取控制區：PAM 特權帳號管理節點嚴格控管 K8s 叢集與 Mgt 節點的維運存取權限
4. 資安監控區：日誌管理節點 (1-4) 與威脅情資管理節點 (1-2)，介接 SOC 中心""",

    20: """【補充 02：護欄運作雙向循序流程】
本頁依據「圖 79 護欄運作循序流程說明」設計。

護欄服務為獨立於代理層和 LLM 之外的攔截點，強制執行雙向檢核：

階段 0（前置設定）：
Admin 管理員設定 System Prompt 與護欄政策規則（政策即程式碼 OPA/Rego）

階段 1（輸入檢核）：
1.  User 發送 Request → 代理層接收
1.1 代理層將輸入送交護欄服務檢查（Prompt Injection 偵測、密級比對、DLP）
1.2 護欄服務回應輸入確認結果（allow / block）
1.3 若通過，代理層才將安全的 Prompt 送交 LLM

階段 2（輸出檢核）：
2.1 LLM 回傳回應給代理層
2.2 代理層將輸出送交護欄服務檢查（敏感資訊、越級內容、有害內容）
2.3 護欄服務回應輸出確認結果

處置邏輯：
• 若判定為「阻斷」→ 代理層將回應替換為系統警告字串後回傳使用者
• 若判定為「通過」→ 完整回應回傳給使用者，完成推論請求

全程寫入 Audit Log（單向、不可竄改）。""",

    21: """【補充 03：SBOM 供應鏈管控與 MCP 零信任授權】
對齊 NIST SP 800-218A SSDF（安全軟體開發框架），從模型到工具建立完整信任鏈。

一、SBOM (軟體料件清單) 管控：

基礎模型層 (L1)：
• 模型權重下載後強制要求提供 SBOM
• 進行雜湊值 (Hash) 比對與數位簽章驗證
• 確認無遭竄改或植入後門方可掛載至算力區 (K8s)

MCP 工具層 (L4)：
• MCP 伺服器與外掛套件上架前，必須提交原始碼與相依套件 SBOM
• 經過自動化弱點掃描 (SCA) 排除已知 CVE 漏洞
• 於 Portal 上架時由資安官進行雙重確認

二、MCP 工具零信任授權 (mTLS)：

• 全面禁止靜態 API Key，防止一旦外洩即造成橫向移動威脅
• 改採短時效憑證 (Ephemeral Credentials)：例如 5 分鐘有效期，逾期自動失效
• 結合 SPIFFE/SPIRE 簽發工作負載身分，MCP 與 Agent 之間強制 mTLS 雙向加密

SBOM 紀錄一併綁定至 8 欄位稽核日誌，落實全鏈路 Traceability。""",

    22: """【補充 04：ZTA 七大支柱映射與 AI 自動化紅隊演練】

一、國防部零信任 ZTA 七大支柱對齊 (NIST SP 800-207)：
柱 1 User：SSO/MFA + ABAC 動態屬性授權
柱 2 Device：端點 MDM / 內網設備健康度檢查
柱 3 Network：PQ Tunnel 後量子通道 + 單閘 Diode
柱 4 App：Harness 治理外框 + K8s 沙箱隔離
柱 5 Data：DISA IL 分級 + RAG 隔離 + DLP 遮罩
柱 6 Visibility：8 欄位留痕 + SBOM + SOC 監控
柱 7 Automation：異常自動熔斷斷路器 (Circuit Breaker)

二、AI 驅動之自動化紅隊演練 (Automated AI Red Teaming)：
改變傳統靜態演練，引入「對抗性 LLM」自動對 Agent 進行攻擊測試。

AIEC 量化防禦指標 (AI Evaluation Criteria)：
• 提示抗注入率 (Prompt Robustness)：目標 > 99.9%
• 防降密洩漏率 (Data Exfiltration Prevention)：100% 阻斷
• 沙箱與 MCP 逃逸防禦 (Sandbox Escape Resilience)：零容忍
• 護欄攔截準確率 (Guardrail Precision)：每月抽樣重跑比對基準""",

    23: """【全案總結論 — 五大原則 × 四大補強 完整覆蓋】
本頁為整份 23 頁簡報的最終收尾。

覆蓋矩陣說明：
五大原則（模型分層/資料分級/單一閘道/層層防護/全程留痕）與四大補強（K8s·PAM·PQ Tunnel / 護欄雙向時序 / SBOM·MCP mTLS / ZTA 七柱·AI 紅隊）形成 5×4 = 20 格交叉矩陣，每一格均有對應的技術措施與驗證機制，確保「沒有死角」。

對長官的三項決策建議：
1. 建議立即啟動 Gateway + PQ Tunnel 建置 — Q1 完成最小可行版
2. 建議先導單位 PoC 雙軌並行 — 庶務 (開箱即用) + 武器 (DeepAgents)
3. 建議建立 SBOM + AI 紅隊常態機制 — 納入 CI/CD + 季度演練

全案 23 頁核心交付成果：
• 主體篇 17 頁：五大原則、六節點縱深、Harness 雙軌、11步資料流、Guardrail 五類、國際標準 29 項、SOC 熔斷、端到端 16 項檢核、Q1~Q4 Roadmap、風險矩陣、KPI
• 補充篇 6 頁：K8s/PAM/PQ Tunnel 實體架構、護欄 I/O 時序、SBOM+mTLS、ZTA 七柱+AI 紅隊、覆蓋矩陣+決策建議

五大原則貫穿全案，首尾呼應。報告完畢，敬請裁示。"""
}

# ─── 寫入備忘稿 ───
for slide_num, note_text in notes.items():
    slide = prs.slides[slide_num - 1]
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = note_text.strip()
    print(f"  ✓ Slide {slide_num:2d} 備忘稿已寫入 ({len(note_text.strip())} 字)")

# ─── Save ───
output_path = r"d:\JavaDO\總結報告_最終版.pptx"
try:
    prs.save(output_path)
    print(f"\n✅ 備忘稿已成功寫入：{output_path}")
    print(f"   共為 {len(notes)} 頁投影片加上備忘稿")
except Exception as e:
    print(f"❌ 寫入失敗: {e}")
