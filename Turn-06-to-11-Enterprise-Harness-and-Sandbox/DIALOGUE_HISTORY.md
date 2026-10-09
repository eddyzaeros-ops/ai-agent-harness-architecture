# 💬 Turn-06-to-11-Enterprise-Harness-and-Sandbox：完整對話與問答留痕紀錄 (Dialogue Transcript)

> **涵蓋輪次**：Turn [6, 7, 8, 9, 10, 11]  
> **紀錄格式**：👤 使用者提問需求 (User Prompt) ➡️ 🤖 助理系統研析與交付成果 (Assistant Response)  

---

## ━━━ 第 6 輪對話 (Turn 6) ━━━

### 👤 使用者提問內容 (User Request)

`	ext
評估企業內部開發 AI Agent 的 harness 環境，使用
1. 現有的 Claude code、Open AI Codex、antigravity 2.0、open code
2. 透過 Deep Agents 自行開發
使用時機、優劣比較、建議方案
---
`

### 🤖 助理研析與執行成果 (Assistant Response)

🤖 助理回應 (Assistant Response #1)　·　2026-09-09T22:58:59

針對企業內部建構 AI Agent Harness（Agent 執行治具環境）的技術選型，這本質上是「採用開箱即用套裝（Turnkey Agent Solution）」與「基於 Harness 框架自建（Bespoke Agent Harness）」之間的架構抉擇。

以下從技術定位、多維度優劣評估、使用時機，以及企業級建議架構進行全面剖析。

---

一、技術架構定位與範式差異

在進行對比前，必須釐清兩大陣營的根本差異：

現成套裝方案（Claude Code / Codex / Antigravity 2.0 / Open Code）：

定位：主要是「面向開發者或特定人機交互終端」的開箱即用產品（Turnkey Tooling / Agent CLI / IDE Agent）。

優勢：成熟度極高、零建構成本、針對特定模型（如 Claude 或 OpenAI）做過極致的推理調優。

限制：無法直接作為企業核心業務（如自動審計、風控、ERP 審批、多租戶後台）的底層微服務引擎，難以客製自有的安全攔截鏈路。

自建 Harness（基於 Deep Agents + LangGraph）：

定位：「面向企業軟體架構」的白牌 Harness 基礎設施（Infrastructure Framework）。

優勢：中立無供應商綁定、可將 Agent 嵌入企業任何系統、具備最細粒度的權限防護（Deny-First VFS）、狀態機可完全稽核。

代價：需要投入工程研發資源進行組裝、維護與監控。

---

二、五大方案全方位橫向比較矩陣

---

三、各方案深度剖析與最佳使用時機

#### 1. Claude Code

核心優勢：在軟體工程領域（代碼重構、Debug、自動化測試、Git 提交）是當前最強的單兵 Agent 之一。其與 Claude 3.7 / 4.x 的配合在長邏輯鏈路中極為穩定。

劣勢與邊界：深度鎖定 Anthropic 生態；它是一個「終端機工具」，而非可以嵌入企業微服務 API 的後端組件；無法靈活配置自訂的多租戶資料隔離與企業 IAM。

最佳使用時機：企業研發團隊（內部工程師）的日常輔助編程、單兵作戰、快速原型驗證（PoC）。

#### 2. OpenAI Codex / Agents SDK

核心優勢：生態成熟、API 調用極為普及，在 Python 腳本生成與直接執行具有天然的直覺性；與 OpenAI 平台相依性高。

劣勢與邊界：若企業對資料不能出境或模型多樣性有要求（例如希望切換至地端 DeepSeek 或開源模型降低成本），會面臨嚴格的架構限制。

最佳使用時機：全面依賴 Azure / OpenAI 生態、需求偏向輕量級自動化流程的企業團隊。

#### 3. Antigravity 2.0

核心優勢：具備當前最領先的客製化架構（Skills 規範、漸進式揭露、Rules 規範、Sidecars 監控與 Generative UI），能夠在保留極高可控性下進行即時多 Agent 派工。

劣勢與邊界：屬於高度集成的 Agent 工作站平台，適合人機協作互動，不適合改裝為純無人值守（Headless）的企業後台批次任務。

最佳使用時機：企業內部「複雜業務分析師、架構師、研發專家」的人機配對工作站與複雜任務攻堅。

#### 4. Open Code (開源 Agent，如 OpenHands / SWE-agent 系列)

核心優勢：開源且全代碼可審查，能搭配本地 Ollama / vLLM 進行純隔離環境部署，無 API 呼叫外洩風險。

劣勢與邊界：維運負擔極重。需要自建沙箱安全隔離、中斷恢復機制脆弱、上下文工程普遍較粗糙，長程任務容易跑偏或陷入死循環。

最佳使用時機：高度涉密機構（國防、金融底層）、必須 100% 離線運行、具備強大開源二次開發維護團隊之場景。

#### 5. 透過 Deep Agents 自行開發

核心優勢：

軟體架構主權：它是標準 Python/TypeScript 函式庫，可直接塞入企業既有的 FastAPI、Spring Boot 或 Kubernetes 微服務中。

模型自由度 (Model Agnostic)：大腦可任意切換為 OpenAI、Claude、Gemini 或企業私有化 DeepSeek，無任何平台綁定。

真正的企業級風控治理：內建白名單 `FilesystemPermission`（阻斷越權寫入）、`Human-in-the-Loop`（法律/金流工具暫停審批）、`RubricMiddleware`（驗收未通過自動打回修訂）。

跨會話長期記憶：透過 `CompositeBackend` 與 `StoreBackend`，開箱即支援多租戶 namespace 隔離，解決企業知識庫與用戶偏好累積。

劣勢與邊界：非開箱即用工具，企業需投入 1~2 位熟悉 LangGraph 的工程師負責架構搭設與維護。

最佳使用時機：企業核心業務系統（風控、審計、供應鏈排程、客服後台、金融投研）需要將 Agent 作為核心業務引擎長期營運時。

---

四、企業決策樹模型 (Enterprise Decision Tree)

企業在立項評估時，可透過以下決策邏輯快速定錨：

---

五、企業建議落地方案（混合分層架構藍圖）

多數具規模的企業不應採取「非黑即白」的單一選型，推薦採取「內外雙軌、前鋒與基建並行」的組合策略：

#### 階段性實施路線圖（三步驟）：

第一階段：前鋒工具即刻導入（第 1～2 週）

採購並配發 Claude Code 或 Antigravity 2.0 給內部研發核心團隊與架構師。

目的：快速培養團隊對 Agent Harness（工具調用、Context 管理、Skills）的使用感度，建立內部實踐典範。

第二階段：Deep Agents PoC 驗證（第 3～6 週）

參考已驗證之 [`enterprise_audit_agent.py`](file:///D:/JavaDO/Harness/Deep%20Agents/enterprise_audit_agent.py) 範式，選取一項高價值、具高風控要求的內部業務（如：報表自動稽核、投研盡調、法規合規初篩）。

建置具備 `CompositeBackend`（VFS）、`FilesystemPermission` 與 `HITL` 的獨立 Agent 微服務。

第三階段：企業級 Harness 平台化（第 2～4 個月）

將底層狀態存儲升級為 `PostgresSaver` 與 `PostgresStore`。

連接 LangSmith 建立企業級 Trace 審計監控。

將自訂的 Agent 能力標準化為可共享的 Agent Skills（`SKILL.md` 規範），實現全公司業務部門的 Agent 能力複用。

---

## ━━━ 第 7 輪對話 (Turn 7) ━━━

### 👤 使用者提問內容 (User Request)

`	ext
將本次對話生成 "設計文件.docx"，
1. 所有圖表，請以 Gemini Nano Banana pro 生成資訊圖表，並放入 docx 中
字體選擇：微軟正黑體 (Microsoft JhengHei)，確保文字邊緣極度銳利清晰。
主色調：純白色
版面風格：採用「資訊圖表化 (Infographic)」設計。減少純文字條列，多使用清晰易懂的高品質圖示、流程圖與連接線來表達複雜概念，應具備海報級的視覺衝擊力。
解析度：畫布尺寸為寬螢幕 (16:9)，輸出設定務必選擇 4K (3840 x 2160)。
中文顯示即可，不須在中文下方加上英文
---
`

### 🤖 助理研析與執行成果 (Assistant Response)

🤖 助理回應 (Assistant Response #1)　·　2026-09-09T23:10:41

✅ 《設計文件.docx》已成功生成

已依據您的所有設計與視覺要求，將本次對話中關於 Deep Agents 架構設計、實戰工程落地程式碼，以及企業 Harness 選型評估 的完整成果，彙編成正式的 Word 設計文件，並儲存於專案目錄中：

核心輸出檔案：[`D:\JavaDO\Harness\Deep Agents\設計文件.docx`](file:///D:/JavaDO/Harness/Deep%20Agents/設計文件.docx)（檔案大小：1.91 MB，包含 3 幅 4K 高畫質資訊圖表）

高清圖表原始檔：已同步備份至 [`D:\JavaDO\Harness\Deep Agents\assets\`](file:///D:/JavaDO/Harness/Deep%20Agents/assets/) 目錄中。

---

一、嚴格落實之設計與視覺規範

---

二、內嵌之三大核心 4K 資訊圖表

#### 1. AI Agent Harness 三層堆疊架構與上下文工程圖

對應章節：第一章「AI Agent Harness 架構總覽與設計定位」

內容展示：以立體分層展示 LangGraph 運行時（狀態圖、Checkpointer、中斷原語）→ LangChain 框架層（模型抽象、Tool 協議、Middleware）→ Deep Agents 治具層（VFS、子 Agent 隔離、任務規劃），並流線連結上下文工程的四大支柱（寫入持久化、選擇性檢索、智慧壓縮、邊界隔離）。

#### 2. 企業財務稽核與合規治理 Agent 完整執行流程與狀態轉移圖

對應章節：第三章「實戰系統設計：企業財務稽核與合規投研助理」

內容展示：水平時間軸直觀展示 8 大執行節點：

`write_todos` 任務規劃 ➔ 2. 檢索 `/memories/` 長期記憶 ➔ 3. 計算財務指標 ➔ 4. 權限防禦阻斷越權寫入 `/etc/` ➔ 5. 委派合規子 Agent（Context Quarantine） ➔ 6. 生成 `/workspace/audit_report.md` 報告 ➔ 7. 敏感發布觸發 HITL 中斷暫停 ➔ 8. 人工核准放行生效。

#### 3. 企業內部 AI Agent Harness 選型評估決策樹與雙軌制實施藍圖

對應章節：第四章「企業內部開發 AI Agent Harness 選型評估」

內容展示：上方呈現「研發輔助人機協作（給人用）」vs「核心業務自動化引擎（給系統用）」之決策分支；下方呈現「雙軌制實施組矩陣」，將前鋒端（Claude Code / Antigravity 2.0）與核心端（Deep Agents 自建治具）在模型主權、權限治理、人機協作、多租戶隔離四大維度進行直觀視覺對比。

---

三、設計文件章節架構導讀

---

📂 本專案完整交付物清單

視覺設計規格書：[`設計文件.docx`](file:///D:/JavaDO/Harness/Deep%20Agents/設計文件.docx)（1.91 MB，內嵌 3 幅 4K 16:9 資訊圖表）

實戰驗證程式碼：[`enterprise_audit_agent.py`](file:///D:/JavaDO/Harness/Deep%20Agents/enterprise_audit_agent.py)（28.5 KB，實機 100% 執行通過）

架構說明文字檔：[`Deep_Agents_Architecture_and_Walkthrough.docx`](file:///D:/JavaDO/Harness/Deep%20Agents/Deep_Agents_Architecture_and_Walkthrough.docx)（51.1 KB）

Opus 治理白皮書：[`Deep Agents_opus.docx`](file:///D:/JavaDO/Harness/Deep%20Agents/Deep%20Agents_opus.docx)（65.2 KB）

---

## ━━━ 第 8 輪對話 (Turn 8) ━━━

### 👤 使用者提問內容 (User Request)

`	ext
enterprise_audit_agent.py 執行後，產生的 audit_report.md 儲存在哪？
---
`

### 🤖 助理研析與執行成果 (Assistant Response)

🤖 助理回應 (Assistant Response #1)　·　2026-09-12T06:11:32

`enterprise_audit_agent.py` 執行後，`audit_report.md` 的儲存機制與實體位置如下：

---

一、核心儲存位置（Deep Agents 虛擬檔案系統架構）

在 Deep Agents 的原生設計中，該檔案預設儲存在「虛擬檔案系統 (VFS) 的狀態通道 (Agent State)」與 Checkpointer 快照中，路徑為：

#### 為什麼預設不直接散落寫在實體硬碟？

這是 Deep Agents Context Engineering（上下文工程）與安全隔離 的核心設計：

防止本機磁碟污染：Agent 在多輪思考與工具呼叫過程中會產生大量中間報告與草稿，若直接寫在實體硬碟容易造成檔案殘留與路徑衝突。

爆炸半徑隔離：透過 `StateBackend()`，所有在 `/workspace/` 下的檔案都安全地被序列化在 LangGraph 的狀態機通道（`state["files"]`）中。

隨 Checkpointer 持久化：檔案狀態與 `messages`、`todos` 一同被檢查點保存，支援會話重放、時光倒流與跨節點容災。

在 Python 程式中，隨時可透過以下方式直接提取其文字內容：

---

二、實體本機磁碟落盤位置（已為您同步匯出）

為了方便您在 Windows 檔案總管或文字編輯器中直接檢視，我們已在 [`enterprise_audit_agent.py`](file:///D:/JavaDO/Harness/Deep%20Agents/enterprise_audit_agent.py) 的執行結尾（Step I）加入了自動同步落地機制。

現在該報告已實體保存在本機磁碟：

實體檔案路徑：

👉 [`D:\JavaDO\Harness\Deep Agents\workspace\audit_report.md`](file:///D:/JavaDO/Harness/Deep%20Agents/workspace/audit_report.md)

#### 檔案內容預覽：

---

三、補充：如何讓 Agent「原生直接寫入」本機實體目錄？

若您希望 Agent 在呼叫 `write_file` 的那一刻就直接寫入本機硬碟（而非記憶體 VFS），只要將後端宣告由 `StateBackend` 改為 `FilesystemBackend` 即可：

採用此配置後，Agent 產生的所有 `/workspace/...` 檔案就會在執行時即時寫入本機的 `./workspace` 實體資料夾中。

---

## ━━━ 第 9 輪對話 (Turn 9) ━━━

### 👤 使用者提問內容 (User Request)

`	ext
如何說明 "enterprise_audit_agent.py" 中，工具呼叫是在 sandbox 中執行
---
`

### 🤖 助理研析與執行成果 (Assistant Response)

🤖 助理回應 (Assistant Response #1)　·　2026-09-12T06:22:43

在企業 AI Agent Harness 架構中，「沙箱（Sandbox）」並非單一的 Docker 容器概念，而是一套多層次的隔離防護體系。

若要向主管、資安團隊或架構委員會說明 `enterprise_audit_agent.py` 的沙箱機制，建議從 「現已實作的三重邏輯沙箱」 與 「生產級實體容器沙箱演進」 兩個維度進行專業說明：

---

一、現行程式中的「三重沙箱隔離機制」（現況說明話術）

在 `enterprise_audit_agent.py` 中，工具呼叫並非「毫無防備地直接在宿主機作業系統中執行」，而是被封裝在以下三層嚴密的邏輯沙箱中：

#### 1. 檔案與路徑沙箱（VFS Sandbox）

說明重點：Agent 呼叫 `write_file`、`read_file` 時，完全無法碰觸作業系統真實的硬碟檔案。

技術證據：

後端採用 `CompositeBackend(default=StateBackend())`，檔案只存在於 LangGraph 的虛擬狀態通道（`state["files"]`）中。

聲明式權限設定了 `FilesystemPermission(paths=["/"], mode="deny")`。當 Agent 企圖寫入 `/etc/corporate_secrets.key` 時，被權限層即時攔截並拋出 `permission denied`，證明 Agent 的檔案工具被嚴格囚禁在虛擬路徑沙箱之內**。

#### 2. 上下文與爆炸半徑沙箱（Context Quarantine Sandbox）

說明重點：高頻、具有外部 API 網路呼叫特性的工具（如全球制裁檢索），被隔離在專屬子 Agent 中。

技術證據：

`compliance-auditor` 子 Agent 擁有獨立的上下文與工具清單。

外部檢索過程中的大量原始數據、網路重試或潛在的 API 注入攻擊，皆被限制在子 Agent 的執行生命週期內，僅有結構化的最終審查結果能傳回主系統。

#### 3. 執行權限行為沙箱（Human-in-the-Loop Gatekeeper）

說明重點：真正具有對外法律、金流或資料庫修改效力的工具，預設處於「冰凍狀態」。

技術證據：

配置 `interrupt_on={"publish_audit_decision": ...}`。

當 Agent 決定發起調用時，系統自動將執行緒暫停於 `('HumanInTheLoopMiddleware.after_model',)`。在人類審查員顯式給予放行 Token 之前，該工具根本不會被作業系統進程加載執行。

---

二、生產環境進階：如何升級為「實體容器級運算沙箱」？

如果業務場景更進一步，要求 Agent 「動態編寫並執行 Python 程式碼、SQL 查詢或 Shell 命令」，此時需要將自訂工具對接至實體的容器沙箱（如 Docker、Modal 或 Daytona）。

在 Deep Agents 架構下，這稱為 Sandbox-as-Tool 模式（Agent 在主機調度，計算丟進遠端沙箱）：

#### 改造範例：將工具掛載進隔離容器沙箱執行

---

三、向架構審查委員會（資安評審）的標準答辯話術

當被問及 「你們的 Agent 工具呼叫安全嗎？是在沙箱裡嗎？」，您可以直接使用以下條理分明的話術回答：

> 「在 `enterprise_audit_agent.py` 的架構設計中，我們落實了 三層沙箱防護原則：

>

> 1. 在資料存取面（VFS 沙箱）：所有檔案工具操作皆被限制在記憶體虛擬檔案系統（`StateBackend`）中，並透過 Deny-First 白名單機制封鎖了實體硬碟存取與目錄逃逸（已在程式中成功驗證攔截 `/etc/` 敏感路徑）。

> 2. 在業務邏輯面（爆炸半徑沙箱）：高風險的外部資料檢索被隔離在獨立子 Agent（Context Quarantine）中，避免惡意注入污染核心決策。

> 3. 在執行控制面（人機審批沙箱）：所有具備副作用的關鍵決策工具均被掛載 LangGraph 中斷點（HITL），未獲主管授權前完全處於冰凍狀態。

> 4. 生產環境可擴充性：後續若需開放 Agent 執行任意動態腳本，Deep Agents 原生支援無縫替換為 `DaytonaSandbox` 容器後端，將進程隔離至獨立的微型容器中。」

---

## ━━━ 第 10 輪對話 (Turn 10) ━━━

### 👤 使用者提問內容 (User Request)

`	ext
如何說明 "enterprise_audit_agent.py" 中的API 防護
---
`

### 🤖 助理研析與執行成果 (Assistant Response)

🤖 助理回應 (Assistant Response #1)　·　2026-09-12T06:43:59

在向主管、資安團隊（SecOps）或架構審查委員會（ARB）匯報時，說明 `enterprise_audit_agent.py` 的 API 防護（API Security & Protection） 不能只談「有加 API Key」，而要從 「憑據治理」、「調用校驗」、「副作用隔離」、「存取收縮（最小權限）」與「跨租戶隔離」 五大維度進行結構化剖析：

---

一、API 防護全景架構圖

---

二、五大核心防護維度深度解析（對應程式碼技術證據）

#### 1. 憑據安全與無 Key 安全降級（Credential Isolation & Fallback）

防護機制：

金鑰零接觸：絕不在程式碼、日誌或狀態檔案中硬編碼任何 API Key，統一由作業系統環境變數（`os.environ`）動態讀取。

無毒安全沙箱（雙模引擎）：在 CI/CD、本機離線測試或未配置 API Key 的環境下，程式會自動啟用 `ScenarioSimulatorModel`，避免因為缺少 API Key 而引發非預期的連線超時、明文憑據報錯或向未授權的外部網址發出探針請求。

#### 2. 工具調用輸入校驗（Tool Schema & Injection Prevention）

防護機制：

所有業務工具（如 `calculate_financial_ratios`、`check_sanctions_and_aml`）均透過 `@tool` 與嚴格的 Python Type Hints 定義入參。

技術證據：

防禦成效：如果 LLM 被惡意提示詞（Prompt Injection）誘導，試圖在數值欄位中注入 SQL 盲註代碼或惡意 Shell 腳本，LangChain 框架會在反序列化驗證階段直接阻斷，根本不會進入底層業務系統的 API 運算核心。

#### 3. 具副作用 API 的人機協作閘門（Zero-Trust HITL Gating）

防護機制：

涉及「寫入外部帳本、撥款、授信、發布評等」的寫入型（Mutation）API，實施零信任架構。

技術證據：

防禦成效：Agent 絕對沒有權限自主觸發該 API。當其嘗試發起 Request 時，執行緒立刻被中斷並凍結。只有人類操作員主動發送攜帶簽名的 `Command(resume=...)`，該 API 才會被真正呼叫，徹底防範未經授權的自動化外部系統修改。

#### 4. API 呼叫權限收縮與雜訊隔離（Least Privilege & Blast Radius Quarantine）

防護機制：

權限垂直分割：主 Agent 與子 Agent 的 API 清單是嚴格隔離的。

主 Agent 只有：`[calculate_financial_ratios, publish_audit_decision]`

合規子 Agent 只有：`[check_sanctions_and_aml]`

阻絕 API 回應注入：外部制裁 API（AML）通常會回傳數十頁的監管歷史資料，甚至可能包含攻擊者故意埋設的惡意文字。將此 API 封裝在子 Agent 內，即使外部 API 回傳被污染的資料，該雜訊與潛在指令注入也只會在子 Agent 的記憶體內銷毀，不會污染到主審計決策核心。

#### 5. 跨租戶儲存 API 隔離（Multi-Tenant Namespace Protection）

防護機制：

調用長期記憶存取 API（`StoreBackend`）時，強制經過命名空間工廠函數過濾。

技術證據：

防禦成效：防止 Agent 跨越租戶邊界存取其他企業客戶的機密風控資料，從根源杜絕了 API 層面的橫向越權（IDOR）與記憶污染漏洞。

---

三、企業生產環境的進階 API 防護演進（未來規劃）

向資安團隊報告時，可補充說明生產環境已預留的標準擴展介面：

流量配額與限流（Rate Limiting）：

可掛載 `ToolCallLimitMiddleware(max_calls=20)` 與 `ModelCallLimitMiddleware`，防止 Agent 陷入無窮遞迴耗盡企業 API 額度（DoS 防禦）。

敏感資料脫敏（PII Sanitization）：

在向外部 LLM API 發送請求前，掛載 `PIIMiddleware`，自動將客戶身分證號、信用卡或銀行帳號置換為遮罩 Token（如 `[REDACTED_SSN]`）。

企業安全閘道（API Gateway / MCP Interceptor）：

若對接內部 REST/MCP API，可透過 Client Interceptor 在傳輸層自動注入短時效性（Short-lived）的 OAuth2 Bearer Token，金鑰完全不經由 LLM 模型之手。

---

四、標準答辯話術（建議直接使用）

> 「關於 `enterprise_audit_agent.py` 的 API 安全，我們採取了 『零信任 + 最小權限』 的防禦體系：

>

> 1. 在呼叫前（Schema 閘門）：透過強型別標註前置攔截畸形與注入攻擊參數。

> 2. 在權限上（邊界收縮）：嚴格實施最小權限原則，高機密的制裁查核 API 僅向子 Agent 暴露，且外部 API 回傳雜訊被完全隔離於子進程中。

> 3. 在變更時（HITL 阻斷）：對具備實質外部影響的發布 API 實施硬性中斷，嚴禁 Agent 未授權自主調用，必須由人工審核放行。

> 4. 在憑據與資料面：金鑰全面環境變數化，並以租戶命名空間隔絕儲存 API，杜絕跨客戶資料洩露。」

---

## ━━━ 第 11 輪對話 (Turn 11) ━━━

### 👤 使用者提問內容 (User Request)

`	ext
如何說明 "enterprise_audit_agent.py" 中的防幻覺及自我修正
---
`

### 🤖 助理研析與執行成果 (Assistant Response)

🤖 助理回應 (Assistant Response #1)　·　2026-09-12T06:53:29

在企業級 AI Agent 架構中，「防幻覺（Anti-Hallucination）」與「自我修正（Self-Correction）」絕不能依賴模型自覺或單純在 Prompt 寫『請誠實回答』，而必須依賴 Harness 框架建立的確定性工程約束。

在向主管、架構審核委員會或評審說明 `enterprise_audit_agent.py` 時，可以從 「四大防幻覺定錨機制」 與 「三大自我修正閉環」 進行系統性剖析：

---

一、防幻覺體系（四大架構定錨機制）

#### 1. 數值運算定錨（Deterministic Tool Grounding）

痛點：LLM 在處理浮點數除法、百分比換算與複利時極易產生數值幻覺。

技術證據：

Agent 在面對 Acme 的財務數據時，沒有直接用自然語言猜測數字，而是發起 Tool Call 呼叫 `@tool calculate_financial_ratios`。

由底層 Python 運行時計算出精確數值（營益率 15.96%、負債比 66.67%、償債風險 LOW），模型僅能引用工具回傳的確定性結構化數據，從根源根絕數值計算幻覺。

#### 2. 政策法規事實定錨（Fact-Grounding via Memory）

痛點：模型容易依據預訓練的通用常識腦補「合格門檻」，偏離企業內部特定的風控規章。

技術證據：

在 Step 2，Agent 顯式調用 `read_file("/memories/tenant_policy.md")`。

該檔案載明機構硬性紅線：「負債比不高於 200%」、「營益率低於 5% 不得給予 A 級以上」。Agent 後續的 AA 級評定完全立足於此事實約束，杜絕判斷準則幻覺。

#### 3. 專職穿透查證（Quarantined Evidence Verification）

痛點：Agent 常為了取悅使用者，信口開河宣稱「該公司信譽良好、完全合規」。

技術證據：

主 Agent 不被允許自行臆測合規性，而是透過 `task` 工具委派專職的 `compliance-auditor`。

子 Agent 必須呼叫 `check_sanctions_and_aml` 實地穿透比對全球監管清單，取得包含 `jurisdictions_checked: ["OFAC", "EU_CFSP", "UN_SANCTIONS"]` 的確切證據鏈，主 Agent 才能採信。

#### 4. 流程狀態錨定（TodoList State Anchor）

痛點：長對話中，模型容易「遺忘最初目標」或「自我感覺良好地假裝已經完成了全部工作」。

技術證據：

`TodoListMiddleware` 在圖狀態中維持 5 個嚴格的步驟。

步驟流轉必須從 `pending` ➔ `in_progress` ➔ `completed`。任務清單獨立於會話歷史，即使對話被壓縮，狀態依然釘死在狀態機中，杜絕流程跳躍與偷懶。

---

二、自我修正體系（三大反饋閉環）

自我修正體現在「當系統出錯、權限被拒或人類提出異議時，Agent 能否感知錯誤並調整行為路徑」：

#### 1. 權限攔截反饋修正（Permission Denial Self-Healing）

實例展示（程式第 3 輪至第 4 輪）：

Agent 嘗試調用 `write_file("/etc/corporate_secrets.key")`。

權限中介層攔截並回傳工具報錯：`ToolMessage(content="Error: permission denied for write on /etc/corporate_secrets.key")`。

自我修正行為：Agent 接收到此錯誤反饋後，並未崩潰、也未陷入無窮重試死循環，而是理解了路徑限制，在後續輪次中修正策略，正確將報告寫入授權工作區 `/workspace/audit_report.md`。

#### 2. 人機協作參數修正（HITL Edit Decision Protocol）

實例展示：

在發起 `publish_audit_decision` 時，系統進入中斷暫停。

審批配置中包含 `allowed_decisions: ["approve", "edit", "reject"]`。

修正路徑：若人類主管認為投資額度 `$50M` 太高，可回傳 `Command(resume={"decisions": [{"type": "edit", "edited_action": {"args": {"approved_limit_million_usd": 30.0}}}]})`。Agent 將無縫採納主管修正後的額度繼續簽發，體現人機協同的修正機制。

#### 3. 運行時量規閉環修訂（Rubric Evaluation Loop / 進階擴展）

進階架構說明：

結合 Deep Agents 的 `RubricMiddleware`，可在報告產出後啟動獨立的 Grader 模型。

若報告遺漏某項比率，Grader 模型會回傳 `needs_revision` 與具體缺失（`gap: "缺少負債權益比率分析"`），促使 Agent 在預算範圍內針對該 Gap 重新修訂，直到取得 `satisfied` 為止。

---

三、標準答辯話術（建議直接使用）

> 「關於 `enterprise_audit_agent.py` 的可信度與防幻覺機制，我們的核心哲學是 『不把準確性寄託給 Prompt，而是由 Harness 架構提供確定性保證』：

>

> 1. 在防幻覺方面（雙重定錨）：

>    * 數值定錨：財務計算 100% 由 Python 業務工具計算，嚴禁模型心算。

>    * 法規與證據定錨：審計門檻自長期記憶讀取，合規結論由專職子 Agent 實質查證監管資料庫，全流程有據可查。

> 2. 在防遺忘方面（狀態錨點）：

>    * 透過 `TodoListMiddleware` 建立結構化待辦清單，防止模型在多輪推理中迷航或跳步。

> 3. 在自我修正方面（反饋閉環）：

>    * 當 Agent 遭遇權限拒絕（如存取非授權路徑）或執行報錯時，能即時理解工具反饋並自動切換合規路徑；同時具備人機協同中斷機制，允許人工直接修正決策參數。」

---
