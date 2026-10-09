---
date: 2026-09-09
title: "06. 企業內部 AI Agent Harness 環境評估與選型"
phase: "Phase 1: Agent Harness 基礎概念與企業審計實作"
tags:
  - 企業Harness評估
  - 開箱即用
  - 客製化Harness
  - 五大原則
  - 武器系統vs行政庶務
prev: "[[05-審計Agent文件轉換Docx]]"
next: "[[07-Harness設計文件與資訊圖表]]"
related:
  - "[[01-LangChain-vs-DeepAgents-架構評估]]"
  - "[[07-Harness設計文件與資訊圖表]]"
  - "[[12-企業內部AI-Agent需求與全景架構]]"
  - "[[15-五層縱深防禦架構與零信任資料流]]"
  - "[[21-全服務鏈資料流與總結報告PPTX]]"
  - "[[00-Index-AI-Agent-Framework-知識圖譜總覽]]"
---

# 06. 企業內部 AI Agent Harness 環境評估與選型

- **對話輪次**：第 6 輪對話 (Turn 6)
- **記錄日期**：`2026-09-09`
- **所屬演進階段**：**Phase 1: Agent Harness 基礎概念與企業審計實作**
- **核心關鍵字**：`企業Harness評估` `開箱即用` `客製化Harness` `五大原則` `武器系統vs行政庶務`
- **主題概述**：提出行政庶務（開箱即用）與武器系統（客製化 LangChain DeepAgents）之雙軌 Harness 評估架構，確立五大原則。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：[[05-審計Agent文件轉換Docx]]
* **下一篇 (Next)**：[[07-Harness設計文件與資訊圖表]]
* **知識圖譜總覽 (Master Index)**：[[00-Index-AI-Agent-Framework-知識圖譜總覽]]
* **橫向技術與架構關聯 (Cross-Cutting References)**：
  - [[01-LangChain-vs-DeepAgents-架構評估|01. LangChain vs DeepAgents 架構評估與治理觀點]]：深入對比 LangChain、LangGraph 與 DeepAgents，剖析從代碼生成轉型至自主 Agent 治理的核心 Harness 需求。
  - [[07-Harness設計文件與資訊圖表|07. Harness 設計文件與 Nano Banana Pro 圖表生成]]：整合評估報告為設計文件.docx，並生成架構堆疊與評估矩陣之專業資訊圖表。
  - [[12-企業內部AI-Agent需求與全景架構|12. 企業內部 AI Agent 需求矩陣與全景架構]]：系統化盤點企業開發者、管理者與使用者的三重視角痛點，構建落地架構矩陣。
  - [[15-五層縱深防禦架構與零信任資料流|15. 五層縱深防禦架構與零信任資料流安全設計]]：確立通用模型、領域模型、Agent 執行、技能工具、領域知識 (RAG) 之五層縱深，落實「單一閘道、全程留痕」。
  - [[21-全服務鏈資料流與總結報告PPTX|21. 全服務鏈資料流與五大原則高階簡報 (總結報告.pptx)]]：統整五大原則、Agent 開發者/使用者/資安三條鏈路工作流、AISVS 國際標準及四期建置 Roadmap，產出高階簡報。

---

## 👤 使用者指令 (User Request)

> [!NOTE] 原始提示詞紀錄
> 評估企業內部開發 AI Agent 的 harness 環境，使用
> 1. 現有的 Claude code、Open AI Codex、antigravity 2.0、open code
> 2. 透過 Deep Agents 自行開發
> 使用時機、優劣比較、建議方案

---

## 🤖 助理詳細研析與成果交付 (Assistant Response & Deliverables)

針對企業內部建構 AI Agent Harness（Agent 執行治具環境）的技術選型，這本質上是**「採用開箱即用套裝（Turnkey Agent Solution）」**與**「基於 Harness 框架自建（Bespoke Agent Harness）」**之間的架構抉擇。

以下從技術定位、多維度優劣評估、使用時機，以及企業級建議架構進行全面剖析。

---

### 一、技術架構定位與範式差異

在進行對比前，必須釐清兩大陣營的根本差異：

1. **現成套裝方案（Claude Code / Codex / Antigravity 2.0 / Open Code）**：
   - **定位**：主要是**「面向開發者或特定人機交互終端」**的開箱即用產品（Turnkey Tooling / Agent CLI / IDE Agent）。
   - **優勢**：成熟度極高、零建構成本、針對特定模型（如 Claude 或 OpenAI）做過極致的推理調優。
   - **限制**：無法直接作為企業核心業務（如自動審計、風控、ERP 審批、多租戶後台）的底層微服務引擎，難以客製自有的安全攔截鏈路。
2. **自建 Harness（基於 Deep Agents + LangGraph）**：
   - **定位**：**「面向企業軟體架構」**的白牌 Harness 基礎設施（Infrastructure Framework）。
   - **優勢**：中立無供應商綁定、可將 Agent 嵌入企業任何系統、具備最細粒度的權限防護（Deny-First VFS）、狀態機可完全稽核。
   - **代價**：需要投入工程研發資源進行組裝、維護與監控。

---

### 二、五大方案全方位橫向比較矩陣

| 評估維度 | ① Claude Code | ② OpenAI Codex / SDK | ③ Antigravity 2.0 | ④ Open Code (開源) | ⑤ 基於 Deep Agents 自建 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **底層模型相容** | 僅支援 Anthropic Claude 系列 | 僅支援 OpenAI 系列 | 支援 Google Gemini 系列為主，具多模態優勢 | 支援多數開源與商業模型 API | **完全中立**（OpenAI, Claude, Gemini, DeepSeek, 地端開源） |
| **部署型態** | CLI 終端工具 / 桌面環境 | API SDK / 開發平台 | IDE 插件 / 原生 Agent 協作環境 | 本地容器 / CLI / WebUI | **微服務 / 容器 / 嵌入現有系統** |
| **上下文工程 (Context Eng.)** | 內建壓縮與 Git 追蹤 | 依賴模型長視窗與基本記憶 | **極強**（Skills 漸進揭露、Artifacts、Sidecars） | 基礎剪裁，易上下文膨脹 | **極強**（VFS 虛擬檔案系統、20K 自動卸載、85% 摘要） |
| **檔案權限治理** | 基礎 CLI 確認 (Prompt 詢問) | 沙箱隔離（限制在容器） | 宣告式 Permissions、工作區邊界 | 仰賴 Docker 容器環境隔離 | **聲明式 Deny-First**（可對特定目錄 deny / allow / interrupt） |
| **人機協作 (HITL)** | 人工在終端機輸入 Y/N | 支援基本 Tool Approval | 互動式多選、審批對話框 | 終端機手動確認 | **原生狀態機中斷**（`interrupt_on` + `Command(resume)` 跨時間續行） |
| **多 Agent 協作** | 有限子任務呼叫 | 多 Agent 路由 | 多 Agent 派工 (`invoke_subagent`) | 單 Agent 為主 / 簡單 Multi-agent | **世代領先**（同步/異步/動態編排 + Context Quarantine 隔離） |
| **運行時品質驗收** | 依靠測試腳本回傳錯誤 | 依靠 Prompt 自檢 | 支援驗證與回溯檢查 | 無內建驗收機制 | **RubricMiddleware**（Fail-Closed 門禁 + 取證工具循環修訂） |
| **企業資料主權 (隱私)** | 資料送往 Anthropic 雲端 | 資料送往 OpenAI 雲端 | 符合企業級合規授權 | 支援純地端部署 | **完全自主掌控**（可搭配地端 vLLM / Ollama） |
| **開發建造成本** | 零（即裝即用） | 低（快速上手） | 低～中（依附於專屬工具鏈） | 中（需自建沙箱與相依性） | **中～高**（需編寫膠水代碼與架構組裝） |

---

### 三、各方案深度剖析與最佳使用時機

#### 1. Claude Code
- **核心優勢**：在軟體工程領域（代碼重構、Debug、自動化測試、Git 提交）是當前最強的單兵 Agent 之一。其與 Claude 3.7 / 4.x 的配合在長邏輯鏈路中極為穩定。
- **劣勢與邊界**：深度鎖定 Anthropic 生態；它是一個「終端機工具」，而非可以嵌入企業微服務 API 的後端組件；無法靈活配置自訂的多租戶資料隔離與企業 IAM。
- **最佳使用時機**：**企業研發團隊（內部工程師）的日常輔助編程、單兵作戰、快速原型驗證（PoC）**。

#### 2. OpenAI Codex / Agents SDK
- **核心優勢**：生態成熟、API 調用極為普及，在 Python 腳本生成與直接執行具有天然的直覺性；與 OpenAI 平台相依性高。
- **劣勢與邊界**：若企業對資料不能出境或模型多樣性有要求（例如希望切換至地端 DeepSeek 或開源模型降低成本），會面臨嚴格的架構限制。
- **最佳使用時機**：**全面依賴 Azure / OpenAI 生態、需求偏向輕量級自動化流程的企業團隊**。

#### 3. Antigravity 2.0
- **核心優勢**：具備當前最領先的客製化架構（Skills 規範、漸進式揭露、Rules 規範、Sidecars 監控與 Generative UI），能夠在保留極高可控性下進行即時多 Agent 派工。
- **劣勢與邊界**：屬於高度集成的 Agent 工作站平台，適合人機協作互動，不適合改裝為純無人值守（Headless）的企業後台批次任務。
- **最佳使用時機**：**企業內部「複雜業務分析師、架構師、研發專家」的人機配對工作站與複雜任務攻堅**。

#### 4. Open Code (開源 Agent，如 OpenHands / SWE-agent 系列)
- **核心優勢**：開源且全代碼可審查，能搭配本地 Ollama / vLLM 進行純隔離環境部署，無 API 呼叫外洩風險。
- **劣勢與邊界**：維運負擔極重。需要自建沙箱安全隔離、中斷恢復機制脆弱、上下文工程普遍較粗糙，長程任務容易跑偏或陷入死循環。
- **最佳使用時機**：**高度涉密機構（國防、金融底層）、必須 100% 離線運行、具備強大開源二次開發維護團隊之場景**。

#### 5. 透過 Deep Agents 自行開發
- **核心優勢**：
  1. **軟體架構主權**：它是標準 Python/TypeScript 函式庫，可直接塞入企業既有的 FastAPI、Spring Boot 或 Kubernetes 微服務中。
  2. **模型自由度 (Model Agnostic)**：大腦可任意切換為 OpenAI、Claude、Gemini 或企業私有化 DeepSeek，無任何平台綁定。
  3. **真正的企業級風控治理**：內建白名單 `FilesystemPermission`（阻斷越權寫入）、`Human-in-the-Loop`（法律/金流工具暫停審批）、`RubricMiddleware`（驗收未通過自動打回修訂）。
  4. **跨會話長期記憶**：透過 `CompositeBackend` 與 `StoreBackend`，開箱即支援多租戶 namespace 隔離，解決企業知識庫與用戶偏好累積。
- **劣勢與邊界**：非開箱即用工具，企業需投入 1~2 位熟悉 LangGraph 的工程師負責架構搭設與維護。
- **最佳使用時機**：**企業核心業務系統（風控、審計、供應鏈排程、客服後台、金融投研）需要將 Agent 作為核心業務引擎長期營運時**。

---

### 四、企業決策樹模型 (Enterprise Decision Tree)

企業在立項評估時，可透過以下決策邏輯快速定錨：

```
                              [企業內部 AI Agent 需求]
                                         │
                   ┌─────────────────────┴─────────────────────┐
             【給人用？】                                  【給系統用？】
         (輔助研發/人機協作)                             (嵌入業務/自動化流程)
                   │                                           │
         ┌─────────┴─────────┐                                 │
   【偏向純寫代碼】     【多模態/複雜架構分析】                           │
         │                   │                                 │
   ┌─────┴─────┐             │                                 │
【Claude生態】【OpenAI生態】   │                                 │
   ▼           ▼             ▼                                 │
Claude Code  Codex    Antigravity 2.0                          │
                                                               │
                         ┌─────────────────────────────────────┴──────────────────┐
                   【極端密閉隔離/無外網】                                  【現代企業混合雲/多模型】
                   (預算有限/願承擔維運)                                    (需嚴格風控、租戶隔離、HITL)
                         │                                                        │
                         ▼                                                        ▼
                    Open Code                                          Deep Agents 自建
                 (如 OpenHands)                                       (Harness 企業標準化)
```

---

### 五、企業建議落地方案（混合分層架構藍圖）

多數具規模的企業**不應採取「非黑即白」的單一選型**，推薦採取**「內外雙軌、前鋒與基建並行」**的組合策略：

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    雙軌制企業 AI Agent Harness 藍圖                         │
├─────────────────────────────────────┬──────────────────────────────────────┤
│  【前鋒端：研發與專業人員賦能】    │  【核心端：業務流程與自動化引擎】   │
│                                     │                                      │
│  • 採用方案：Claude Code /          │  • 採用方案：Deep Agents 自建治具    │
│    Antigravity 2.0                  │  • 承載場景：審計、投研、CRM/ERP 自動│
│  • 承載場景：工程師日常 Coding、   │    化、供應鏈風控                    │
│    架構原型發想、快速文檔分析       │  • 關鍵特性：                        │
│  • 核心價值：零部署時間，立即提升   │    - 支援多模型路由（省成本與合規）  │
│    內部 30~50% 的個人生產力        │    - 嚴格 Deny-First 權限阻斷        │
│                                     │    - 嵌入既有微服務，支援長程 HITL   │
└─────────────────────────────────────┴──────────────────────────────────────┘
```

#### 階段性實施路線圖（三步驟）：

1. **第一階段：前鋒工具即刻導入（第 1～2 週）**
   - 採購並配發 **Claude Code** 或 **Antigravity 2.0** 給內部研發核心團隊與架構師。
   - 目的：快速培養團隊對 Agent Harness（工具調用、Context 管理、Skills）的使用感度，建立內部實踐典範。
2. **第二階段：Deep Agents PoC 驗證（第 3～6 週）**
   - 參考已驗證之 [`enterprise_audit_agent.py`](file:///D:/JavaDO/Harness/Deep%20Agents/enterprise_audit_agent.py) 範式，選取一項**高價值、具高風控要求**的內部業務（如：報表自動稽核、投研盡調、法規合規初篩）。
   - 建置具備 `CompositeBackend`（VFS）、`FilesystemPermission` 與 `HITL` 的獨立 Agent 微服務。
3. **第三階段：企業級 Harness 平台化（第 2～4 個月）**
   - 將底層狀態存儲升級為 `PostgresSaver` 與 `PostgresStore`。
   - 連接 **LangSmith** 建立企業級 Trace 審計監控。
   - 將自訂的 Agent 能力標準化為可共享的 **Agent Skills（`SKILL.md` 規範）**，實現全公司業務部門的 Agent 能力複用。
