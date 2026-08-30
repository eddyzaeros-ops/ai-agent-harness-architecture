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

## 📚 參考文獻
- 和達, 陶銳, 詹國梁, 等. 智能體駕馭工程：分析 Claude Code 技術實現 [J]. 通信技術, 2026, 59(7): 779-787.
- Hashimoto M. My AI adoption journey, 2026.
- Jimenez C E, et al. SWE-bench: Can language models resolve real-world GitHub issues? 2024.
- Bölük C. I improved 15 LLMs at coding in one afternoon. Only the harness changed, 2026.
- Hu Wei. Architectural Design Decisions in AI Agent Harnesses, 2026.
