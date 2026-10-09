# 📁 Turn-30-to-35-OWASP-LLM-Guardrail-Design：OWASP Top 10 全維度 AI 護欄體系設計與 MITRE ATLAS 攻擊鍊防禦對齊

> **涵蓋範圍**：Turn 30 ~ Turn 35 (OWASP LLM / Agentic / Skills / RAG 護欄體系、MITRE ATLAS 威脅框架、實證量化統計、自包含互動式 HTML 儀表板、36 頁旗艦級 PPTX 簡報與 Docx 審計留痕)  
> **目前版本**：v2.2.0  
> **最後更新**：2026-10-09  

---

## 📑 文件摘要 (Document Summary)

本模組為 AI 系統安全與自主代理人治理之核心旗艦成果，完整收斂由模型底座至自主任務執行的縱深防禦體系：
1. **五層縱深防禦 (Defense-in-Depth L1~L5)**：
   - **L1/L2 語意閘門**：聚焦 OWASP Top 10 for LLM (LLM01~LLM10)，涵蓋 Prompt 注入防禦、敏感資訊脫敏、DISA IL 密級校驗與 8 大不可否認性審計欄位。
   - **L3 執行監督器**：依據 OWASP Top 10 for Agentic Applications (ASI01~ASI10)，以「三維六門」防範目標劫持、約束狀態機轉移、核發 JIT 60 秒短效憑證與去話術化情境人機在迴路 (HITL)。
   - **L4 沙盒隔離**：依據 OWASP Top 10 for Skills (AST10)，瓦解「機敏憑證 ⨂ 外部連線 ⨂ 不可信語料」致命三要素，實施 gVisor 微沙盒隔離與漂移斷路器。
   - **L5 檢索閘門**：針對 RAG 安全管道 (RAG01~RAG10)，實施 Pre-Filtering 權限前置過濾、防間接 Prompt 注入、防知識庫投毒與向量逆向推論防禦。
2. **端到端攻擊鍊對齊 (MITRE ATLAS TA0001~TA0016)**：
   - 全面解析 16 大戰術階段與 72+ 戰術技術矩陣，深入探討「瞬態坍縮現象 (Transient Collapse)」與「離地工具攻擊 (LotL-AI)」。
3. **實證統計量化與視覺化**：
   - 採用 Matplotlib 生成 5 張高解析圖表（LLM、Agentic、Skills、RAG、MITRE ATLAS），具備雙維度實證涉入率 vs. 遙測告警事件剖析。
4. **全自包含 HTML 儀表板 (6 Tabs)**：
   - 單一便攜 HTML，Base64 內嵌高解析圖卡（支援燈箱全螢幕與下載）、即時 Mermaid 互動架構圖、雙向快速導航與 Ctrl+K 全文檢索。
5. **36 頁高階商業與技術架構簡報 (PPTX)**：
   - 採用溫潤極簡商業風，具備全防碰撞排版、色彩徽章標籤、實證數據卡與雷達分佈。

---

## 📂 檔案清單與產出物 (Artifacts Inventory)

- [DIALOGUE_HISTORY.md](./DIALOGUE_HISTORY.md) (**本模組全系列對話歷程與問答雙向留痕**)

### 1. 核心研析文檔與審計報告 (`docs/`)
- `docs/00-Guardrail-Architecture-Index.md`：六大專題總覽與跨層交叉對照矩陣
- `docs/01-LLM-Guardrail.md`：LLM 基礎模型護欄與 L1/L2 語意閘門
- `docs/02-Agentic-Guardrail.md`：Agentic 代理人行為護欄與 L3 執行監督器
- `docs/03-Skills-Guardrail.md`：Skills 技能工具安全護欄與 L4 沙盒隔離
- `docs/04-RAG-Guardrail.md`：RAG 檢索增強安全護欄與 L5 檢索閘門
- `docs/05-ATLAS-Attack-Chain.md`：MITRE ATLAS 攻擊鍊防禦對齊與瞬態坍縮剖析
- `docs/OWASP LLM Guardrail Design.docx`：企業級架構審計留痕 Word 報告

### 2. 簡報投影片 (`pptx/`)
- `pptx/OWASP_LLM_Guardrail_Design.pptx`：36 頁完整旗艦架構投影片（依循樣式一色系與卡片排版規範）

### 3. 互動式儀表板 (`html/`)
- `html/index.html`：6 分頁全自包含互動式展示系統
- `html/OWASP_LLM_Guardrail_Design.html`：離線便攜單檔網頁（支援 Base64 圖卡與 Mermaid）

### 4. 核心建置程式碼 (`code/`)
- `code/generate_html.py`：HTML 靜態儀表板編譯引擎（支援 Obsidian 語法、Callout、TOC、全文索引）
- `code/generate_all_charts.py`：5 大安全領域量化統計繪圖腳本
- `code/build_master_pptx.py`：36 頁 PPTX 簡報自動化組裝引擎
- `code/slides_common.py` ~ `code/slides_m05.py`：模組化投影片版面生成腳本

### 5. 高解析度量化圖資 (`assets/`)
- `assets/owasp_llm_top10_risk_distribution.png`：OWASP LLM Top 10 全球實證量化分佈圖
- `assets/owasp_agentic_top10_risk_distribution.png`：OWASP Agentic Top 10 弱點量化分佈圖
- `assets/owasp_skills_top10_risk_distribution.png`：OWASP Skills Top 10 風險量化分佈圖
- `assets/owasp_rag_top10_risk_distribution.png`：OWASP RAG Pipeline 10 大安全風險分佈圖
- `assets/mitre_atlas_attack_chain_distribution.png`：MITRE ATLAS 16 大戰術階段雙維度分佈圖

---

## 🏷️ 版本管理 (Version Management)

| 版本號 | 發布日期 | 類型 | 狀態 | 負責模組 |
| :--- | :--- | :--- | :--- | :--- |
| **v1.0.0** | 2026-09-18 | Initial Release | ✅ 歸檔 | LLM/Agentic/Skills 三層護欄初始架構建立 |
| **v2.0.0** | 2026-09-28 | Major Expansion | ✅ 歸檔 | 納入 RAG 與 MITRE ATLAS，生成自包含 HTML (6 Tabs) |
| **v2.2.0** | 2026-10-09 | Production Release | ✅ 正式發布 | 完成 36 頁旗艦 PPTX、Docx 審計留痕與全對話歷史對齊 |

---

## 🔄 版本差異說明 (Version Changelog / Diffs)

- **相較前一輪對話 (Turn 29) 之核心演進**：
  - **範疇躍遷**：由單一無人機 F2T2EA 戰術任務擴展至企業級全局 AI 安全治理框架（跨越模型層、代理人層、技能工具層、檢索管線層與對抗攻擊鍊）。
  - **體系完整化**：正式由三層防禦（LLM/Agentic/Skills）拓展為五層縱深防禦（新增 RAG01~RAG10）與端到端 MITRE ATLAS 攻擊鍊對齊。
  - **可交付物多元化**：同步提供 Obsidian 知識庫（雙向鏈結）、5 張 Matplotlib 科研級圖表、單檔離線 6-Tab HTML 儀表板、36 頁高階商業簡報 (PPTX) 與專業 Word 報告。
