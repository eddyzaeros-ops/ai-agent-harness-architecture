---
date: 2026-09-09
title: "01. LangChain vs DeepAgents 架構評估與治理觀點"
phase: "Phase 1: Agent Harness 基礎概念與企業審計實作"
tags:
  - AI_Agent_Harness
  - LangChain
  - DeepAgents
  - 架構選型
  - 治理評估
prev: "None"
next: "[[02-Opus-深度研析與概念總結]]"
related:
  - "[[02-Opus-深度研析與概念總結]]"
  - "[[04-DeepAgents-企業級審計Agent實作]]"
  - "[[06-企業內部Harness環境評估]]"
  - "[[00-Index-AI-Agent-Framework-知識圖譜總覽]]"
---

# 01. LangChain vs DeepAgents 架構評估與治理觀點

- **對話輪次**：第 1 輪對話 (Turn 1)
- **記錄日期**：`2026-09-09`
- **所屬演進階段**：**Phase 1: Agent Harness 基礎概念與企業審計實作**
- **核心關鍵字**：`AI_Agent_Harness` `LangChain` `DeepAgents` `架構選型` `治理評估`
- **主題概述**：深入對比 LangChain、LangGraph 與 DeepAgents，剖析從代碼生成轉型至自主 Agent 治理的核心 Harness 需求。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：None
* **下一篇 (Next)**：[[02-Opus-深度研析與概念總結]]
* **知識圖譜總覽 (Master Index)**：[[00-Index-AI-Agent-Framework-知識圖譜總覽]]
* **橫向技術與架構關聯 (Cross-Cutting References)**：
  - [[02-Opus-深度研析與概念總結|02. Opus 深度研析與概念總結]]：以高階邏輯研析 DeepAgents 虛擬檔案系統、子代理人架構與非同步調度機制。
  - [[04-DeepAgents-企業級審計Agent實作|04. DeepAgents 企業級資安審計 Agent 實戰範例]]：提供完整的 enterprise_audit_agent.py 可執行程式碼，實作虛擬沙箱檢查與合規審計報告生成。
  - [[06-企業內部Harness環境評估|06. 企業內部 AI Agent Harness 環境評估與選型]]：提出行政庶務（開箱即用）與武器系統（客製化 LangChain DeepAgents）之雙軌 Harness 評估架構，確立五大原則。

---

## 👤 使用者指令 (User Request)

> [!NOTE] 原始提示詞紀錄
> 1. 讀取並深入理解，同時 visit 文章中所有的連結內容
> "https://wenwender.wordpress.com/2025/12/04/langchain-vs-langgraph-vs-deepagents%EF%BC%9A%E8%A9%B2%E9%81%B8%E5%93%AA%E5%80%8B-ai-agent-%E6%A1%86%E6%9E%B6%EF%BC%9F%E5%AE%8C%E6%95%B4%E5%A0%B4%E6%99%AF%E5%B0%8D%E6%AF%94%E6%8C%87%E5%8D%97/"
> 2. 搜尋與 Langchain Deep Agents 相關的技術資源，包括 Github 的公開 repo
> 3. 讀取 "D:\JavaDO\Harness\Deep Agents" 資料夾下的所有 md 檔
> 深入研究後，從 AI Agent Harness 治理的觀點出發，提出 "Deep Agents.docx" 分析報告，並儲存在 D:\JavaDO\Harness\Deep Agents 資料夾中

---

## 🤖 助理詳細研析與成果交付 (Assistant Response & Deliverables)

已完成對文章內容、關聯技術鏈結、GitHub 開源生態以及 `D:\JavaDO\Harness\Deep Agents` 全部 16 篇章節的深度研究，並從 **AI Agent Harness 治理（AI Agent Harness Governance）** 的企業視角出發，正式產出並儲存了專業分析報告 **`Deep Agents.docx`** 於 `D:\JavaDO\Harness\Deep Agents` 資料夾中。

---

### 一、 關鍵研究資源與外部鏈結解析摘要

#### 1. 溫煜鈞部落格文章與外部鏈結深度研讀
- **文章核心觀點**：深入梳理了 LangChain 生態從 **LangChain（組件抽象/線性鏈）** $\rightarrow$ **LangGraph（圖運行時/狀態機）** $\rightarrow$ **DeepAgents（自主推理/上下文工程套件）** 的架構演進光譜，並指出這並非取代關係，而是自底向上的分層依賴。
- **訪問實務鏈結（`jason8745/llm-kaggle-agent`）**：
  - 作者於 2026/04 新增的參考應用，是以 DeepAgents 的 Harness Engineering 為理念設計的輕量級 Kaggle 競賽分析 Agent。
  - **關鍵治理實踐**：
    1. **人機協同介入（HITL）**：終端模糊搜尋競賽後，強制由人類確認選定後才觸發 Agent。
    2. **智能過濾（Smart Kernel Filtering）**：自動略過純教學與 EDA 筆記本，精準鎖定最高票真實模型解法。
    3. **結構化知識蒸餾**：標準化提取任務類型、資料特徵、評價指標對齊與模型細節。
    4. **持久化知識沉澱**：產出報告沉澱至 `memory/knowledge/<competition-slug>.md`，形成可跨會話檢索的專家記憶庫。
    5. **Token 與財務審計**：每次執行即時輸出 Input/Output Token 消耗統計。
- **官方文檔鏈結**：同步核對了 LangChain OSS Docs、LangGraph Docs 與 DeepAgents Docs 的核心規範。

#### 2. 全球開源技術生態調查（GitHub 公開資源）
- **`langchain-ai/deepagents` (Python)**：官方核心庫（`pip install deepagents`），現已演進至 v0.7+，核心轉向顯式宣告與按需啟用中間件（Opt-in Middleware）。
- **`langchain-ai/deepagentsjs` (TypeScript/JS)**：提供 NPM 原生包，具備相同的上下文工程與工具規範。
- **`langchain-ai/deep-agents-ui`**：官方推出的視覺化互動與執行期監控介面。
- **`langchain-ai/deep-agents-from-scratch`**：從零解構 Deep Agents 底層在 LangGraph 上的實作原理。
- **`datawhalechina/deepagents-in-action`**：中文社群推動的生產級實戰教程。

---

### 二、 本地 16 章核心架構全面梳理

本研究系統化梳理了 `D:\JavaDO\Harness\Deep Agents` 的 16 個篇章：
1. **ch01-agent-harness**：Runtime（LangGraph）/ Framework（LangChain）/ Harness（Deep Agents）三層劃分與 Context Engineering 概念。
2. **ch02-quickstart**：快速上手、模型初始化（含 SiliconFlow 接入）、自定義工具定義三要素（型別標註、Docstring、預設值）。
3. **ch03-virtual-filesystem**：虛擬檔案系統（7 大核心工具）與可插拔後端（StateBackend, FilesystemBackend, StoreBackend, CompositeBackend）。
4. **ch04-task-planning**：`TodoListMiddleware` 與 `write_todos`，以外部狀態錨點抵禦長流程目標飄移。
5. **ch05-subagents**：同步子 Agent 委派（`task` 工具）、`CompiledSubAgent`、結構化 JSON 輸出與上下文隔離。
6. **ch06-async-subagents**：異步子 Agent（5 大控制器：`wait`, `poll`, `cancel`, `list`, `get`；ASGI vs HTTP 雙傳輸通道）。
7. **ch07-skills**：`SKILL.md` 規範、漸進式揭示（Progressive Disclosure：Metadata $\rightarrow$ Instructions $\rightarrow$ Scripts/References）。
8. **ch08-long-term-memory**：雙層記憶體系（Checkpointer 執行緒短時記憶 vs. LangGraph Store 跨會話長時記憶）。
9. **ch09-human-in-the-loop**：`interrupt_on` 風險中斷、直接放行、參數覆寫修改（Edit Args）與拒絕反饋。
10. **ch10-sandboxes**：Sandbox-as-Tool 模式、LangSmithSandbox / Docker 隔離、網路出站限制（Egress Filtering）。
11. **ch11-filesystem-permissions**：宣告式權限規則（`operations`, `paths`, `mode`）、First-Match-Wins 評估模型、工作區白名單。
12. **ch12-mcp**：Model Context Protocol 企業工具集成、資源、提示詞與安全攔截器。
13. **ch13-grading-rubrics**：`RubricMiddleware`、雙模型閉環（Working Model vs Grader Model）、確定性 Evidence Tools 取證、Fail-Closed 原則。
14. **ch14-streaming**：生產級即時流（`type/ns/data` 事件三元組）、多 Agent 事件解多工。
15. **ch15-interpreters**：代碼解釋器、程式化工具呼叫（PTC），在沙箱中以 JS/Python 批次調用工具，將數萬 Token 降至數百。
16. **ch16-dynamic-subagents**：AI 動態生成程式碼即時組裝子 Agent 的前沿模式。

---

### 三、 「AI Agent Harness 治理」核心白皮書架構

在產出的 **`Deep Agents.docx`** 中，全面跳脫了傳統「提示詞安全」的狹隘視角，針對具備真實世界執行副作用（Side Effects）的自主 Agent，建立了**企業級六大治理支柱**：

```
                    ┌─────────────────────────────────────────────────────────┐
                    │      AI Agent Harness 企業級安全與合規治理架構           │
                    └────────────────────────────┬────────────────────────────┘
                                                 │
      ┌────────────────────────┬─────────────────┴───────────────┬────────────────────────┐
      ▼                        ▼                                 ▼                        ▼
【支柱 1：記憶與上下文安全】  【支柱 2：存取控制與沙箱隔離】  【支柱 3：多智能體委派治理】  【支柱 4：人機協同雙人控制】
• 記憶投毒防禦 (Poisoning)   • 宣告式 FilesystemPermission     • 子任務降權與邊界繼承       • 風險分級中斷 (interrupt_on)
• PII 敏感資料過濾攔截       • 警惕首條匹配與預設放行陷阱      • 異步任務心跳與孤兒回收     • 人工審批三動態 (放行/改參/拒絕)
• 租戶隔離與動態 TTL 淘汰    • 工作區嚴格白名單 + 出站阻斷     • 循環中斷器 (Circuit Breaker)• 檢查點狀態重放與安全回滾
      │                        │                                 │                        │
      └────────────────────────┼─────────────────────────────────┴────────────────────────┘
                               ▼                                 ▼
                 【支柱 5：評分量規驗收閉環】       【支柱 6：全鏈路可觀測性與 FinOps】
                 • 區分「模型停止」與「業務驗收」    • LangSmith 分散式調用追蹤 (Call Tree)
                 • Working Model vs Grader Model     • 不可篡改稽核軌跡 (Audit Trail)
                 • 確定性取證工具 (Evidence Tools)   • 即時 Token 預算與動態模型降級熔斷
                 • Fail-Closed 規則與迭代修訂預算
```

#### 報告核心亮點摘要：
1. **揭露評估模型的「預設放行（Default Allow）陷阱」**：
   - 詳解 `FilesystemPermission` 採用 First-Match-Wins 原則；若無任何規則命中，系統預設是放行而非阻斷！
   - 白皮書提供標準企業配置範本：必須在規則末尾宣告 `paths=['/**'], mode='deny'`，並在白名單前優先阻斷 `.env`、`*.key`、`secrets/**` 等敏感路徑。
2. **重塑驗收機制（Rubric Governance）**：
   - 指出傳統重試的無效性，將 `RubricMiddleware` 確立為企業級業務驗收門檻。
   - 堅持「工作模型不自我裁決」與「Fail-Closed」原則，唯有客觀證據工具（測試、Schema 檢查）全數通過且取得 `satisfied` 結論時，方能交付下游。
3. **混合架構落地藍圖與就緒清單**：
   - 制定了從 MVP（LangChain）、狀態化流程（LangGraph）到自主長程任務（Deep Agents）的選型光譜矩陣。
   - 附帶 8 大項「企業生產上線前治理就緒檢查清單（Production Readiness Checklist）」。

---

### 四、 產出報告檔案位置

- **文件路徑**：[Deep Agents.docx](file:///D:/JavaDO/Harness/Deep%20Agents/Deep%20Agents.docx)
- **檔案規格**：約 58 KB，包含 121 個結構化段落、9 張專業格式化表格（含層級架構、Harness 競品對比、角色邊界、決策矩陣等）、深藍商務配色（Deep Navy `#1A365D` / Slate Blue `#2B6CB0`）、關鍵資安警告 Callout Box 以及程式碼範式區塊。
