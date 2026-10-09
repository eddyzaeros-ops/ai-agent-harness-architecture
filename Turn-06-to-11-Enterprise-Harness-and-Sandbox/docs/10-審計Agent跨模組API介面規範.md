---
date: 2026-09-12
title: "10. 審計 Agent 跨模組 API 介面契約規範"
phase: "Phase 1: Agent Harness 基礎概念與企業審計實作"
tags:
  - API介面
  - 契約設計
  - 輸入驗證
  - 輸出結構化
  - PydanticSchema
prev: "[[09-審計Agent隔離沙箱技術解析]]"
next: "[[11-審計Agent認知偏差自我修正機制]]"
related:
  - "[[08-審計報告沙箱安全機制驗證]]"
  - "[[09-審計Agent隔離沙箱技術解析]]"
  - "[[11-審計Agent認知偏差自我修正機制]]"
  - "[[23-無人機F2T2EA自主擊殺鏈Agent實作]]"
  - "[[00-Index-AI-Agent-Framework-知識圖譜總覽]]"
---

# 10. 審計 Agent 跨模組 API 介面契約規範

- **對話輪次**：第 10 輪對話 (Turn 10)
- **記錄日期**：`2026-09-12`
- **所屬演進階段**：**Phase 1: Agent Harness 基礎概念與企業審計實作**
- **核心關鍵字**：`API介面` `契約設計` `輸入驗證` `輸出結構化` `PydanticSchema`
- **主題概述**：詳細定義 Agent 內部跨模組通訊契約、Pydantic Schema 校驗及防注入型結構化傳輸標準。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：[[09-審計Agent隔離沙箱技術解析]]
* **下一篇 (Next)**：[[11-審計Agent認知偏差自我修正機制]]
* **知識圖譜總覽 (Master Index)**：[[00-Index-AI-Agent-Framework-知識圖譜總覽]]
* **橫向技術與架構關聯 (Cross-Cutting References)**：
  - [[08-審計報告沙箱安全機制驗證|08. 審計報告沙箱安全機制與最小權限驗證]]：針對 audit_report.md 進行安全亮點拆解，論證虛擬沙箱隔離對防止惡意程式逃逸的關鍵防護價值。
  - [[09-審計Agent隔離沙箱技術解析|09. 審計 Agent 隔離沙箱技術深度解析 (gVisor/微容器)]]：從作業系統系統呼叫層面解析微容器沙箱，破除憑證、網路與檔案操作同時存在的「致命三要素」。
  - [[11-審計Agent認知偏差自我修正機制|11. 審計 Agent 認知反思與自我修正機制]]：剖析 Agent 於沙箱環境下之 Reflection 反思架構，藉由多步評估回饋修正幻覺與誤判。
  - [[23-無人機F2T2EA自主擊殺鏈Agent實作|23. 無人機 F2T2EA 自主擊殺鏈實戰 Agent 實作]]：完整展示利用 LangChain DeepAgents 構建 F2T2EA 擊殺鏈：COP 融合、MCP 叫起 Lattice、MITL 中斷與 BDA 報告。

---

## 👤 使用者指令 (User Request)

> [!NOTE] 原始提示詞紀錄
> 如何說明 "enterprise_audit_agent.py" 中的API 防護

---

## 🤖 助理詳細研析與成果交付 (Assistant Response & Deliverables)

在向主管、資安團隊（SecOps）或架構審查委員會（ARB）匯報時，說明 `enterprise_audit_agent.py` 的 **API 防護（API Security & Protection）** 不能只談「有加 API Key」，而要從 **「憑據治理」、「調用校驗」、「副作用隔離」、「存取收縮（最小權限）」與「跨租戶隔離」** 五大維度進行結構化剖析：

---

### 一、API 防護全景架構圖

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    API 全生命週期防護體系 (API Defense in Depth)          │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. 憑據與連線安全 (Credential & Transport Security)                     │
│    • 環境變數注入，嚴禁金鑰硬編碼；無 Key 自動切換至高仿真無毒沙箱      │
│    • 避免憑據回傳至 Prompt 或被寫入狀態通道                             │
│                                                                         │
│ 2. 工具介面強型別防禦 (Tool Schema & Type Boundary)                      │
│    • Pydantic 強型別標註 (Type Hints)，前置攔截惡意字串與型態畸形攻擊    │
│    • 入參 Schema 自動校驗，不符合規範者直接拒絕，保護底層業務 API        │
│                                                                         │
│ 3. 核心變更 API 閘道防護 (Side-Effect API Gatekeeping / HITL)           │
│    • 具實質影響之 API (publish_audit_decision) 預設「零信任中斷」       │
│    • 透過 interrupt_on 阻斷自主調用，必須取得人類審核 Token 方可放行    │
│                                                                         │
│ 4. 存取權限收縮與爆炸半徑隔離 (API Access Scoping & Quarantine)          │
│    • 最小權限原則 (PoLP)：主 Agent 無查核 API，子 Agent 無簽發 API       │
│    • 外部 API 查詢的大量雜訊與潛在惡意注入，100% 囚禁在子 Agent 內      │
│                                                                         │
│ 5. 多租戶命名空間隔離 (Multi-Tenant Namespace Isolation)                │
│    • 存取長期記憶 Store API 時，強制綁定 enterprise-tenant-888 命名空間  │
│    • 從底層架構防止跨租戶資料洩漏與「記憶中毒 (Memory Poisoning)」      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 二、五大核心防護維度深度解析（對應程式碼技術證據）

#### 1. 憑據安全與無 Key 安全降級（Credential Isolation & Fallback）
* **防護機制**：
  * **金鑰零接觸**：絕不在程式碼、日誌或狀態檔案中硬編碼任何 API Key，統一由作業系統環境變數（`os.environ`）動態讀取。
  * **無毒安全沙箱（雙模引擎）**：在 CI/CD、本機離線測試或未配置 API Key 的環境下，程式會自動啟用 `ScenarioSimulatorModel`，**避免因為缺少 API Key 而引發非預期的連線超時、明文憑據報錯或向未授權的外部網址發出探針請求**。

#### 2. 工具調用輸入校驗（Tool Schema & Injection Prevention）
* **防護機制**：
  * 所有業務工具（如 `calculate_financial_ratios`、`check_sanctions_and_aml`）均透過 `@tool` 與嚴格的 Python Type Hints 定義入參。
  * **技術證據**：
    ```python
    @tool
    def calculate_financial_ratios(
        company_name: str,
        revenue: float,            # 強制 float 型別
        operating_income: float,
        total_debt: float,
        total_equity: float,
    ) -> dict:
    ```
  * **防禦成效**：如果 LLM 被惡意提示詞（Prompt Injection）誘導，試圖在數值欄位中注入 SQL 盲註代碼或惡意 Shell 腳本，LangChain 框架會在**反序列化驗證階段直接阻斷**，根本不會進入底層業務系統的 API 運算核心。

#### 3. 具副作用 API 的人機協作閘門（Zero-Trust HITL Gating）
* **防護機制**：
  * 涉及「寫入外部帳本、撥款、授信、發布評等」的寫入型（Mutation）API，實施**零信任架構**。
  * **技術證據**：
    ```python
    interrupt_on={"publish_audit_decision": {"allowed_decisions": ["approve", "edit", "reject"]}}
    ```
  * **防禦成效**：Agent **絕對沒有權限自主觸發該 API**。當其嘗試發起 Request 時，執行緒立刻被中斷並凍結。只有人類操作員主動發送攜帶簽名的 `Command(resume=...)`，該 API 才會被真正呼叫，徹底防範未經授權的自動化外部系統修改。

#### 4. API 呼叫權限收縮與雜訊隔離（Least Privilege & Blast Radius Quarantine）
* **防護機制**：
  * **權限垂直分割**：主 Agent 與子 Agent 的 API 清單是嚴格隔離的。
    * 主 Agent 只有：`[calculate_financial_ratios, publish_audit_decision]`
    * 合規子 Agent 只有：`[check_sanctions_and_aml]`
  * **阻絕 API 回應注入**：外部制裁 API（AML）通常會回傳數十頁的監管歷史資料，甚至可能包含攻擊者故意埋設的惡意文字。將此 API 封裝在子 Agent 內，即使外部 API 回傳被污染的資料，該雜訊與潛在指令注入也只會在子 Agent 的記憶體內銷毀，**不會污染到主審計決策核心**。

#### 5. 跨租戶儲存 API 隔離（Multi-Tenant Namespace Protection）
* **防護機制**：
  * 調用長期記憶存取 API（`StoreBackend`）時，強制經過命名空間工廠函數過濾。
  * **技術證據**：
    ```python
    routes={
        "/memories/": StoreBackend(
            namespace=lambda rt: ("enterprise-tenant-888", "memories")
        )
    }
    ```
  * **防禦成效**：防止 Agent 跨越租戶邊界存取其他企業客戶的機密風控資料，從根源杜絕了 API 層面的橫向越權（IDOR）與記憶污染漏洞。

---

### 三、企業生產環境的進階 API 防護演進（未來規劃）

向資安團隊報告時，可補充說明生產環境已預留的標準擴展介面：

1. **流量配額與限流（Rate Limiting）**：
   * 可掛載 `ToolCallLimitMiddleware(max_calls=20)` 與 `ModelCallLimitMiddleware`，防止 Agent 陷入無窮遞迴耗盡企業 API 額度（DoS 防禦）。
2. **敏感資料脫敏（PII Sanitization）**：
   * 在向外部 LLM API 發送請求前，掛載 `PIIMiddleware`，自動將客戶身分證號、信用卡或銀行帳號置換為遮罩 Token（如 `[REDACTED_SSN]`）。
3. **企業安全閘道（API Gateway / MCP Interceptor）**：
   * 若對接內部 REST/MCP API，可透過 Client Interceptor 在傳輸層自動注入短時效性（Short-lived）的 OAuth2 Bearer Token，**金鑰完全不經由 LLM 模型之手**。

---

### 四、標準答辯話術（建議直接使用）

> 「關於 `enterprise_audit_agent.py` 的 API 安全，我們採取了 **『零信任 + 最小權限』** 的防禦體系：
>
> 1. **在呼叫前（Schema 閘門）**：透過強型別標註前置攔截畸形與注入攻擊參數。
> 2. **在權限上（邊界收縮）**：嚴格實施最小權限原則，高機密的制裁查核 API 僅向子 Agent 暴露，且外部 API 回傳雜訊被完全隔離於子進程中。
> 3. **在變更時（HITL 阻斷）**：對具備實質外部影響的發布 API 實施硬性中斷，嚴禁 Agent 未授權自主調用，必須由人工審核放行。
> 4. **在憑據與資料面**：金鑰全面環境變數化，並以租戶命名空間隔絕儲存 API，杜絕跨客戶資料洩露。」
