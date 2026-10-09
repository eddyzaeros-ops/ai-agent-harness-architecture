---
date: 2026-09-12
title: "09. 審計 Agent 隔離沙箱技術深度解析 (gVisor/微容器)"
phase: "Phase 1: Agent Harness 基礎概念與企業審計實作"
tags:
  - 隔離沙箱技術
  - gVisor
  - 微容器
  - AST10防護
  - 致命三要素
prev: "[[08-審計報告沙箱安全機制驗證]]"
next: "[[10-審計Agent跨模組API介面規範]]"
related:
  - "[[08-審計報告沙箱安全機制驗證]]"
  - "[[10-審計Agent跨模組API介面規範]]"
  - "[[11-審計Agent認知偏差自我修正機制]]"
  - "[[15-五層縱深防禦架構與零信任資料流]]"
  - "[[00-Index-AI-Agent-Framework-知識圖譜總覽]]"
---

# 09. 審計 Agent 隔離沙箱技術深度解析 (gVisor/微容器)

- **對話輪次**：第 9 輪對話 (Turn 9)
- **記錄日期**：`2026-09-12`
- **所屬演進階段**：**Phase 1: Agent Harness 基礎概念與企業審計實作**
- **核心關鍵字**：`隔離沙箱技術` `gVisor` `微容器` `AST10防護` `致命三要素`
- **主題概述**：從作業系統系統呼叫層面解析微容器沙箱，破除憑證、網路與檔案操作同時存在的「致命三要素」。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：[[08-審計報告沙箱安全機制驗證]]
* **下一篇 (Next)**：[[10-審計Agent跨模組API介面規範]]
* **知識圖譜總覽 (Master Index)**：[[00-Index-AI-Agent-Framework-知識圖譜總覽]]
* **橫向技術與架構關聯 (Cross-Cutting References)**：
  - [[08-審計報告沙箱安全機制驗證|08. 審計報告沙箱安全機制與最小權限驗證]]：針對 audit_report.md 進行安全亮點拆解，論證虛擬沙箱隔離對防止惡意程式逃逸的關鍵防護價值。
  - [[10-審計Agent跨模組API介面規範|10. 審計 Agent 跨模組 API 介面契約規範]]：詳細定義 Agent 內部跨模組通訊契約、Pydantic Schema 校驗及防注入型結構化傳輸標準。
  - [[11-審計Agent認知偏差自我修正機制|11. 審計 Agent 認知反思與自我修正機制]]：剖析 Agent 於沙箱環境下之 Reflection 反思架構，藉由多步評估回饋修正幻覺與誤判。
  - [[15-五層縱深防禦架構與零信任資料流|15. 五層縱深防禦架構與零信任資料流安全設計]]：確立通用模型、領域模型、Agent 執行、技能工具、領域知識 (RAG) 之五層縱深，落實「單一閘道、全程留痕」。

---

## 👤 使用者指令 (User Request)

> [!NOTE] 原始提示詞紀錄
> 如何說明 "enterprise_audit_agent.py" 中，工具呼叫是在 sandbox 中執行

---

## 🤖 助理詳細研析與成果交付 (Assistant Response & Deliverables)

在企業 AI Agent Harness 架構中，「**沙箱（Sandbox）**」並非單一的 Docker 容器概念，而是一套**多層次的隔離防護體系**。

若要向主管、資安團隊或架構委員會說明 `enterprise_audit_agent.py` 的沙箱機制，建議從 **「現已實作的三重邏輯沙箱」** 與 **「生產級實體容器沙箱演進」** 兩個維度進行專業說明：

---

### 一、現行程式中的「三重沙箱隔離機制」（現況說明話術）

在 `enterprise_audit_agent.py` 中，工具呼叫並非「毫無防備地直接在宿主機作業系統中執行」，而是被封裝在以下三層嚴密的邏輯沙箱中：

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    三重沙箱隔離體系 (Three-Tier Sandbox)                │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. 儲存與檔案沙箱 (VFS Storage Sandbox)                                │
│    • 採用 StateBackend 虛擬檔案通道，所有檔案均在記憶體狀態中模擬         │
│    • FilesystemPermission 實施 Deny-First 白名單，嚴格禁止逃逸至實體硬碟 │
│                                                                         │
│ 2. 爆炸半徑與上下文沙箱 (Context Quarantine Sandbox)                    │
│    • 外部查詢工具 (check_sanctions_and_aml) 運行於獨立子 Agent 沙箱      │
│    • 大量查詢日誌與異常被 100% 阻絕在子環境，污染不溢出至主業務核心      │
│                                                                         │
│ 3. 狀態機行為防護沙箱 (HITL State Machine Sandbox)                      │
│    • 具副作用的工具 (publish_audit_decision) 呼叫前被 Checkpointer 凍結  │
│    • 在未取得人工審核指令 (Command) 前，工具處於「不可執行之隔離態」     │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 1. 檔案與路徑沙箱（VFS Sandbox）
* **說明重點**：Agent 呼叫 `write_file`、`read_file` 時，**完全無法碰觸作業系統真實的硬碟檔案**。
* **技術證據**：
  * 後端採用 `CompositeBackend(default=StateBackend())`，檔案只存在於 LangGraph 的虛擬狀態通道（`state["files"]`）中。
  * 聲明式權限設定了 `FilesystemPermission(paths=["/**"], mode="deny")`。當 Agent 企圖寫入 `/etc/corporate_secrets.key` 時，被權限層即時攔截並拋出 `permission denied`，證明 Agent 的檔案工具**被嚴格囚禁在虛擬路徑沙箱之內**。

#### 2. 上下文與爆炸半徑沙箱（Context Quarantine Sandbox）
* **說明重點**：高頻、具有外部 API 網路呼叫特性的工具（如全球制裁檢索），被隔離在專屬子 Agent 中。
* **技術證據**：
  * `compliance-auditor` 子 Agent 擁有獨立的上下文與工具清單。
  * 外部檢索過程中的大量原始數據、網路重試或潛在的 API 注入攻擊，皆被限制在子 Agent 的執行生命週期內，僅有結構化的最終審查結果能傳回主系統。

#### 3. 執行權限行為沙箱（Human-in-the-Loop Gatekeeper）
* **說明重點**：真正具有對外法律、金流或資料庫修改效力的工具，預設處於「冰凍狀態」。
* **技術證據**：
  * 配置 `interrupt_on={"publish_audit_decision": ...}`。
  * 當 Agent 決定發起調用時，系統自動將執行緒暫停於 `('HumanInTheLoopMiddleware.after_model',)`。在人類審查員顯式給予放行 Token 之前，該工具**根本不會被作業系統進程加載執行**。

---

### 二、生產環境進階：如何升級為「實體容器級運算沙箱」？

如果業務場景更進一步，要求 Agent **「動態編寫並執行 Python 程式碼、SQL 查詢或 Shell 命令」**，此時需要將自訂工具對接至實體的容器沙箱（如 Docker、Modal 或 Daytona）。

在 Deep Agents 架構下，這稱為 **Sandbox-as-Tool** 模式（Agent 在主機調度，計算丟進遠端沙箱）：

#### 改造範例：將工具掛載進隔離容器沙箱執行
```python
from deepagents.backends import DaytonaSandbox # 或使用 ModalSandbox / DockerSandbox
from langchain_core.tools import tool

# 1. 建立獨立的遠端實體容器沙箱實例 (具備 CPU/記憶體/網路限制)
secure_sandbox = DaytonaSandbox(
    image="python:3.12-slim",
    cpu=1,
    memory_limit="512MB",
    network_egress="restricted",  # 禁止任意聯網，僅允許特定白名單
    timeout=30.0                  # 執行超時自動銷毀
)

# 2. 定義受沙箱保護的運算工具
@tool
def calculate_financial_ratios_in_sandbox(code_script: str) -> dict:
    """在獨立的安全容器沙箱中執行進階財務建模代碼。"""
    # 程式碼不是在 Agent 所在的本地伺服器跑，而是透過 RPC 丟進 Docker/Daytona 沙箱內執行
    result = secure_sandbox.execute(f"python -c '{code_script}'")
    if result.exit_code != 0:
        return {"error": result.stderr}
    return {"output": result.stdout}
```

---

### 三、向架構審查委員會（資安評審）的標準答辯話術

當被問及 **「你們的 Agent 工具呼叫安全嗎？是在沙箱裡嗎？」**，您可以直接使用以下條理分明的話術回答：

> 「在 `enterprise_audit_agent.py` 的架構設計中，我們落實了 **三層沙箱防護原則**：
>
> 1. **在資料存取面（VFS 沙箱）**：所有檔案工具操作皆被限制在記憶體虛擬檔案系統（`StateBackend`）中，並透過 Deny-First 白名單機制封鎖了實體硬碟存取與目錄逃逸（已在程式中成功驗證攔截 `/etc/` 敏感路徑）。
> 2. **在業務邏輯面（爆炸半徑沙箱）**：高風險的外部資料檢索被隔離在獨立子 Agent（Context Quarantine）中，避免惡意注入污染核心決策。
> 3. **在執行控制面（人機審批沙箱）**：所有具備副作用的關鍵決策工具均被掛載 LangGraph 中斷點（HITL），未獲主管授權前完全處於冰凍狀態。
> 4. **生產環境可擴充性**：後續若需開放 Agent 執行任意動態腳本，Deep Agents 原生支援無縫替換為 `DaytonaSandbox` 容器後端，將進程隔離至獨立的微型容器中。」
