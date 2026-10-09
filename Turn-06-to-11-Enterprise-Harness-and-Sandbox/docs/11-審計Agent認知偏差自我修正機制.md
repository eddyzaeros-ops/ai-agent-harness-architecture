---
date: 2026-09-12
title: "11. 審計 Agent 認知反思與自我修正機制"
phase: "Phase 1: Agent Harness 基礎概念與企業審計實作"
tags:
  - 認知反思
  - 自我修正
  - 幻覺抑制
  - 反饋迴路
  - Reflection
prev: "[[10-審計Agent跨模組API介面規範]]"
next: "[[12-企業內部AI-Agent需求與全景架構]]"
related:
  - "[[08-審計報告沙箱安全機制驗證]]"
  - "[[09-審計Agent隔離沙箱技術解析]]"
  - "[[10-審計Agent跨模組API介面規範]]"
  - "[[23-無人機F2T2EA自主擊殺鏈Agent實作]]"
  - "[[00-Index-AI-Agent-Framework-知識圖譜總覽]]"
---

# 11. 審計 Agent 認知反思與自我修正機制

- **對話輪次**：第 11 輪對話 (Turn 11)
- **記錄日期**：`2026-09-12`
- **所屬演進階段**：**Phase 1: Agent Harness 基礎概念與企業審計實作**
- **核心關鍵字**：`認知反思` `自我修正` `幻覺抑制` `反饋迴路` `Reflection`
- **主題概述**：剖析 Agent 於沙箱環境下之 Reflection 反思架構，藉由多步評估回饋修正幻覺與誤判。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：[[10-審計Agent跨模組API介面規範]]
* **下一篇 (Next)**：[[12-企業內部AI-Agent需求與全景架構]]
* **知識圖譜總覽 (Master Index)**：[[00-Index-AI-Agent-Framework-知識圖譜總覽]]
* **橫向技術與架構關聯 (Cross-Cutting References)**：
  - [[08-審計報告沙箱安全機制驗證|08. 審計報告沙箱安全機制與最小權限驗證]]：針對 audit_report.md 進行安全亮點拆解，論證虛擬沙箱隔離對防止惡意程式逃逸的關鍵防護價值。
  - [[09-審計Agent隔離沙箱技術解析|09. 審計 Agent 隔離沙箱技術深度解析 (gVisor/微容器)]]：從作業系統系統呼叫層面解析微容器沙箱，破除憑證、網路與檔案操作同時存在的「致命三要素」。
  - [[10-審計Agent跨模組API介面規範|10. 審計 Agent 跨模組 API 介面契約規範]]：詳細定義 Agent 內部跨模組通訊契約、Pydantic Schema 校驗及防注入型結構化傳輸標準。
  - [[23-無人機F2T2EA自主擊殺鏈Agent實作|23. 無人機 F2T2EA 自主擊殺鏈實戰 Agent 實作]]：完整展示利用 LangChain DeepAgents 構建 F2T2EA 擊殺鏈：COP 融合、MCP 叫起 Lattice、MITL 中斷與 BDA 報告。

---

## 👤 使用者指令 (User Request)

> [!NOTE] 原始提示詞紀錄
> 如何說明 "enterprise_audit_agent.py" 中的防幻覺及自我修正

---

## 🤖 助理詳細研析與成果交付 (Assistant Response & Deliverables)

在企業級 AI Agent 架構中，**「防幻覺（Anti-Hallucination）」與「自我修正（Self-Correction）」絕不能依賴模型自覺或單純在 Prompt 寫『請誠實回答』，而必須依賴 Harness 框架建立的確定性工程約束。**

在向主管、架構審核委員會或評審說明 `enterprise_audit_agent.py` 時，可以從 **「四大防幻覺定錨機制」** 與 **「三大自我修正閉環」** 進行系統性剖析：

---

### 一、防幻覺體系（四大架構定錨機制）

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     防幻覺四大架構防線 (Anti-Hallucination)               │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. 數值運算工具定錨 (Deterministic Tool Grounding)                      │
│    • 嚴禁 LLM 自行心算財務比率；強制調用 calculate_financial_ratios     │
│    • 確保營益率 (15.96%)、負債比 (66.67%) 等關鍵指標具備 100% 數學確定性 │
│                                                                         │
│ 2. 政策規章記憶定錨 (Fact Grounding via Memory)                          │
│    • 決策標準不靠模型腦補；從 /memories/ 讀取機構投資白紙黑字規範       │
│    • 以「負債比 > 200% 一票否決」為事實基準，杜絕標準漂移與幻覺        │
│                                                                         │
│ 3. 獨立穿透查驗定錨 (Quarantined Evidence Verification)                 │
│    • 合規查核不靠模型推測；委派專門子 Agent 調用全球制裁與反洗錢資料庫  │
│    • 必須具備 OFAC / EU 等實質查核證據鏈，方可形成審計結論              │
│                                                                         │
│ 4. 流程狀態錨定 (State Anchor via TodoList)                             │
│    • 5 大步驟寫入圖狀態機；嚴禁「跳步」或在未執行前假裝「已完成」       │
│    • 杜絕長程推理中的偷懶型幻覺 (Lazy Hallucination) 與記憶遺忘          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 1. 數值運算定錨（Deterministic Tool Grounding）
* **痛點**：LLM 在處理浮點數除法、百分比換算與複利時極易產生數值幻覺。
* **技術證據**：
  * Agent 在面對 Acme 的財務數據時，**沒有直接用自然語言猜測數字**，而是發起 Tool Call 呼叫 `@tool calculate_financial_ratios`。
  * 由底層 Python 運行時計算出精確數值（營益率 15.96%、負債比 66.67%、償債風險 LOW），模型僅能引用工具回傳的確定性結構化數據，從根源根絕數值計算幻覺。

#### 2. 政策法規事實定錨（Fact-Grounding via Memory）
* **痛點**：模型容易依據預訓練的通用常識腦補「合格門檻」，偏離企業內部特定的風控規章。
* **技術證據**：
  * 在 Step 2，Agent 顯式調用 `read_file("/memories/tenant_policy.md")`。
  * 該檔案載明機構硬性紅線：「負債比不高於 200%」、「營益率低於 5% 不得給予 A 級以上」。Agent 後續的 AA 級評定完全立足於此事實約束，杜絕判斷準則幻覺。

#### 3. 專職穿透查證（Quarantined Evidence Verification）
* **痛點**：Agent 常為了取悅使用者，信口開河宣稱「該公司信譽良好、完全合規」。
* **技術證據**：
  * 主 Agent 不被允許自行臆測合規性，而是透過 `task` 工具委派專職的 `compliance-auditor`。
  * 子 Agent 必須呼叫 `check_sanctions_and_aml` 實地穿透比對全球監管清單，取得包含 `jurisdictions_checked: ["OFAC", "EU_CFSP", "UN_SANCTIONS"]` 的確切證據鏈，主 Agent 才能採信。

#### 4. 流程狀態錨定（TodoList State Anchor）
* **痛點**：長對話中，模型容易「遺忘最初目標」或「自我感覺良好地假裝已經完成了全部工作」。
* **技術證據**：
  * `TodoListMiddleware` 在圖狀態中維持 5 個嚴格的步驟。
  * 步驟流轉必須從 `pending` ➔ `in_progress` ➔ `completed`。任務清單獨立於會話歷史，即使對話被壓縮，狀態依然釘死在狀態機中，杜絕流程跳躍與偷懶。

---

### 二、自我修正體系（三大反饋閉環）

自我修正體現在**「當系統出錯、權限被拒或人類提出異議時，Agent 能否感知錯誤並調整行為路徑」**：

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    三大自我修正閉環 (Self-Correction Loops)             │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. 權限攔截反饋修正 (Permission Denial Self-Healing)                    │
│    • 企圖越權寫入 /etc/ 被拒絕，Agent 讀取報錯後自主轉向合法工作區      │
│                                                                         │
│ 2. 人機協作介入覆寫 (HITL Decision Override)                            │
│    • 人工審核員使用 "edit" 決策修正不當額度，Agent 依據新參數平滑續行   │
│                                                                         │
│ 3. 運行時量規閉環修訂 (Rubric Evaluation Gate / 擴展架構)                │
│    • 評分模型依據測試證據回傳 "needs_revision" 與具體 Gap，工作模型重寫 │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 1. 權限攔截反饋修正（Permission Denial Self-Healing）
* **實例展示（程式第 3 輪至第 4 輪）**：
  1. Agent 嘗試調用 `write_file("/etc/corporate_secrets.key")`。
  2. 權限中介層攔截並回傳工具報錯：`ToolMessage(content="Error: permission denied for write on /etc/corporate_secrets.key")`。
  3. **自我修正行為**：Agent 接收到此錯誤反饋後，**並未崩潰、也未陷入無窮重試死循環**，而是理解了路徑限制，在後續輪次中修正策略，正確將報告寫入授權工作區 `/workspace/audit_report.md`。

#### 2. 人機協作參數修正（HITL Edit Decision Protocol）
* **實例展示**：
  * 在發起 `publish_audit_decision` 時，系統進入中斷暫停。
  * 審批配置中包含 `allowed_decisions: ["approve", "edit", "reject"]`。
  * **修正路徑**：若人類主管認為投資額度 `$50M` 太高，可回傳 `Command(resume={"decisions": [{"type": "edit", "edited_action": {"args": {"approved_limit_million_usd": 30.0}}}]})`。Agent 將無縫採納主管修正後的額度繼續簽發，體現人機協同的修正機制。

#### 3. 運行時量規閉環修訂（Rubric Evaluation Loop / 進階擴展）
* **進階架構說明**：
  * 結合 Deep Agents 的 `RubricMiddleware`，可在報告產出後啟動獨立的 Grader 模型。
  * 若報告遺漏某項比率，Grader 模型會回傳 `needs_revision` 與具體缺失（`gap: "缺少負債權益比率分析"`），促使 Agent 在預算範圍內針對該 Gap 重新修訂，直到取得 `satisfied` 為止。

---

### 三、標準答辯話術（建議直接使用）

> 「關於 `enterprise_audit_agent.py` 的可信度與防幻覺機制，我們的核心哲學是 **『不把準確性寄託給 Prompt，而是由 Harness 架構提供確定性保證』**：
>
> 1. **在防幻覺方面（雙重定錨）**：
>    * **數值定錨**：財務計算 100% 由 Python 業務工具計算，嚴禁模型心算。
>    * **法規與證據定錨**：審計門檻自長期記憶讀取，合規結論由專職子 Agent 實質查證監管資料庫，全流程有據可查。
> 2. **在防遺忘方面（狀態錨點）**：
>    * 透過 `TodoListMiddleware` 建立結構化待辦清單，防止模型在多輪推理中迷航或跳步。
> 3. **在自我修正方面（反饋閉環）**：
>    * 當 Agent 遭遇權限拒絕（如存取非授權路徑）或執行報錯時，能即時理解工具反饋並自動切換合規路徑；同時具備人機協同中斷機制，允許人工直接修正決策參數。」
