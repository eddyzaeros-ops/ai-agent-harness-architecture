# 🤖 AI Agent Harness 架構深度解析 (AI Agent Harness Architecture)

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-0E7C86?style=for-the-badge&logo=github)](https://eddyzaeros-ops.github.io/ai-agent-harness-architecture/)
[![Research Paper](https://img.shields.io/badge/Paper-通信技術%202026-1B2A4A?style=for-the-badge)](./智能體駕馭工程：分析Claude_Code技術實現_和達.pdf)

> **Agent = LLM (Model) + Harness**  
> 深入研究 Claude Code 六層架構、五大核心機制與 2026 年最新智能體駕馭工程（Harness Engineering）實踐。

---

## 🌐 線上互動展示 (Live Interactive Demo)

👉 **點擊體驗線上互動解析網頁**：[https://eddyzaeros-ops.github.io/ai-agent-harness-architecture/](https://eddyzaeros-ops.github.io/ai-agent-harness-architecture/)

---

## 📂 專案內容

| 檔案 | 格式 | 說明 |
| :--- | :--- | :--- |
| [AI_Agent_Harness_架構解析.html](./AI_Agent_Harness_架構解析.html) | HTML | 互動式視覺化解析架構網頁（可直接於瀏覽器開啟） |
| [index.html](./index.html) | HTML | GitHub Pages 首頁進入點 |
| [智能體駕馭工程_Claude_Code深度研究報告.docx](./智能體駕馭工程_Claude_Code深度研究報告.docx) | Word | 完整的深度學術與工程研析報告（約 4 萬字元） |
| [智能體駕馭工程_Claude_Code簡報.pptx](./智能體駕馭工程_Claude_Code簡報.pptx) | PowerPoint | 15 頁專業簡報（符合企業級資安架構樣式規範） |
| [智能體駕馭工程：分析Claude_Code技術實現_和達.pdf](./智能體駕馭工程：分析Claude_Code技術實現_和達.pdf) | PDF | 原始參考學術論文（和達 等，通信技術 2026） |

---

## 🧠 核心概念摘要

### 1. 核心公式
\\text{Agent} = \\text{LLM (Model)} + \\text{Harness}

- **LLM（大腦）**：純粹的推理與生成，僅佔約 **1.6%** 核心決策邏輯。
- **Harness（駕馭層/作業系統）**：提供確定性約束、安全護欄、記憶與狀態管理，佔工程代碼 **98.4%**。

### 2. Claude Code 六層架構
1. **使用者介面層 (UI Layer)**：終端交互 (React/Ink)、IDE 橋接、Headless 無頭模式。
2. **編排層 (Orchestration Layer)**：主迴圈 (Think-Act-Observe-Repeat)、模型路由、錯誤恢復。
3. **智能層 (Intelligence Layer)**：動態提示詞載入、三級記憶架構、五級上下文壓縮。
4. **能力層 (Capability Layer)**：40+ 工具模組、子智能體隔離委派、MCP 協議整合。
5. **安全治理層 (Security Layer)**：三級權限門控、YOLO 分類器兜底、命令黑名單、沙箱隔離。
6. **基礎設施層 (Infrastructure Layer)**：會話持久化、KAIROS 守護進程、Token 計費與追蹤。

### 3. 五大核心駕馭機制
- 🎯 **提示詞動態載入**：6 來源即時組裝，落實漸進式揭露 (Progressive Disclosure)。
- 🧠 **資訊熵治理**：三級記憶（常駐/按需/冷備）+ 五級漸進壓縮（83.5% 觸發閾值，33K 系統緩衝）。
- 🔗 **流程確定性管控 (Hooks)**：30+ 生命週期事件，將確定性規則自概率推理中剝離。
- 🔄 **任務回環極簡設計**：~50 行核心邏輯，「將智能交給模型，將確定性留給框架」。
- 🔧 **工具系統與權限管控**：低/中/高三級風險策略，搭配沙箱與二次確認。

---

---

## 🗂️ 全系列對話歷程歸檔與模組目錄 (Conversation Modules & Artifacts)

本倉庫完整歸檔本專案執行過程中產生的 **37 篇 Markdown 研析文檔、Python 核心代碼、HTML 互動式儀表板、Word (.docx) 審計留痕報告、PowerPoint (.pptx) 簡報與高解析度量化資訊圖表**。依照對話執行歷程與技術範疇獨立劃分為以下模組資料夾：

| 對話資料夾 | 涵蓋對話輪次 | 模組主題說明 | 核心產出物類型 | 版本狀態 |
| :--- | :--- | :--- | :--- | :--- |
| [📁 Turn-00-Index-and-Dashboard](./Turn-00-Index-and-Dashboard) | Turn 00 | AI Agent Framework 知識圖譜導航與視覺化儀表板 | md, html, py, assets | v1.2.0 ✅ |
| [📁 Turn-01-LangChain-vs-DeepAgents](./Turn-01-LangChain-vs-DeepAgents) | Turn 01 | LangChain vs DeepAgents 架構評估與治理觀點 | md, assets | v1.0.0 ✅ |
| [📁 Turn-02-to-03-Opus-Deep-Analysis](./Turn-02-to-03-Opus-Deep-Analysis) | Turn 02 ~ 03 | Opus 深度研析與任務規劃架構深化 | md, docx | v1.0.0 ✅ |
| [📁 Turn-04-to-05-DeepAgents-Audit-Implementation](./Turn-04-to-05-DeepAgents-Audit-Implementation) | Turn 04 ~ 05 | DeepAgents 企業級資安審計 Agent 實作與留痕 | md, py, docx | v1.1.0 ✅ |
| [📁 Turn-06-to-11-Enterprise-Harness-and-Sandbox](./Turn-06-to-11-Enterprise-Harness-and-Sandbox) | Turn 06 ~ 11 | 企業內部雙軌 Harness 與 gVisor 三重沙箱隔離架構 | md, docx, pptx, assets | v1.3.0 ✅ |
| [📁 Turn-12-to-14-Harness-Architecture-and-Comparison](./Turn-12-to-14-Harness-Architecture-and-Comparison) | Turn 12 ~ 14 | 企業需求矩陣與 OpenCode / Claude Code 開源架構對比 | md, pptx, assets | v1.1.0 ✅ |
| [📁 Turn-15-to-20-Defense-in-Depth-and-4K-Guard](./Turn-15-to-20-Defense-in-Depth-and-4K-Guard) | Turn 15 ~ 20 | 五層縱深防禦架構與 4K 防護框架 Harness 全景圖 | md, html, assets | v2.0.0 ✅ |
| [📁 Turn-21-to-22-Summary-Reports-and-Audit-Export](./Turn-21-to-22-Summary-Reports-and-Audit-Export) | Turn 21~22, 28 | 全服務鏈資料流總結報告與全歷程 Docx 格式化留痕 | md, docx, pptx | v2.1.0 ✅ |
| [📁 Turn-23-to-27-UAV-F2T2EA-Killchain-v1](./Turn-23-to-27-UAV-F2T2EA-Killchain-v1) | Turn 23 ~ 27 | 無人機 F2T2EA 自主擊殺鏈實戰 Agent 與 4K 戰術資訊圖表 | md, py, pptx, assets | v1.0.0 ✅ |
| [📁 Turn-29-UAV-F2T2EA-v2-Skills-Hooks-Lattice](./Turn-29-UAV-F2T2EA-v2-Skills-Hooks-Lattice) | Turn 29 | 無人機 F2T2EA v2 架構演進：Skills、Hooks 與 Lattice 深度模擬 | md, py, json, assets | v2.0.0 ✅ |
| [📁 Turn-30-to-35-OWASP-LLM-Guardrail-Design](./Turn-30-to-35-OWASP-LLM-Guardrail-Design) | Turn 30 ~ 35 | OWASP Top 10 全維度 AI 護欄體系設計與 MITRE ATLAS 攻擊鍊防禦對齊 | md, docx, pptx, html, py, assets | v2.2.0 ✅ |
| [📁 Turn-36-to-40-AI-Service-Chain-Summary-Report](./Turn-36-to-40-AI-Service-Chain-Summary-Report) | Turn 36 ~ 40 | 國防 AI 服務鏈總結報告、DeepAgents 16章研析與群暉科技建置 Proposal | md, docx, pptx, py, assets | v2.3.0 ✅ |

> 💡 **版本管理與留痕規範**：各模組目錄內均附有專屬 README.md，提供嚴謹的**文件摘要**、**產出物清單**、**版本號碼標註**與**版本差異說明 (Changelog)**。

## 📚 參考文獻
- 和達, 陶銳, 詹國梁, 等. 智能體駕馭工程：分析 Claude Code 技術實現 [J]. 通信技術, 2026, 59(7): 779-787.
- Hashimoto M. My AI adoption journey, 2026.
- Jimenez C E, et al. SWE-bench: Can language models resolve real-world GitHub issues? 2024.
- Bölük C. I improved 15 LLMs at coding in one afternoon. Only the harness changed, 2026.
- Hu Wei. Architectural Design Decisions in AI Agent Harnesses, 2026.
