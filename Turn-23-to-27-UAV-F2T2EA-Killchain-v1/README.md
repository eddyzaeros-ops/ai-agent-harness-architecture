# 📁 Turn-23-to-27-UAV-F2T2EA-Killchain-v1：無人機 F2T2EA 自主擊殺鏈實戰 Agent 與 4K 戰術資訊圖表

> **涵蓋範圍**：Turn 23 ~ Turn 27 (自主擊殺鏈實作、4K 圖表繪製、邊緣協同與圖層防遮擋修復)  
> **目前版本**：v1.0.0  
> **最後更新**：2026-10-09

---

## 📑 文件摘要 (Document Summary)

實現以軍事打擊鏈 F2T2EA（Find, Fix, Track, Target, Engage, Assess）為核心的無人機群自主攻擊協同 Agent。實裝地面指揮 Main Agent 與機載邊緣 Sub-Agent 的分散式通訊協議，並克服影像中文字遮擋問題，產出無遮擋原圖搭配下方獨立大字體中文說明版之 4K 戰術圖表。

---

## 📂 檔案清單與產出物 (Artifacts Inventory)
- [DIALOGUE_HISTORY.md](./DIALOGUE_HISTORY.md) (**本對話輪次完整對話紀錄留痕**)

- docs/23-無人機F2T2EA自主擊殺鏈Agent實作.md (Markdown 核心研析文檔)
- docs/24-F2T2EA自主擊殺鏈資訊圖表生成.md (Markdown 核心研析文檔)
- docs/25-F2T2EA資訊圖表細節調校與放大.md (Markdown 核心研析文檔)
- docs/26-分散式架構-地面Main與機載Sub-Agent協同.md (Markdown 核心研析文檔)
- docs/27-F2T2EA作戰場景合理性評估與4K圖表.md (Markdown 核心研析文檔)
- code/uav_f2t2ea_killchain_agent.py (Python 核心程式碼 / 腳本)
- code/generate_clean_killchain_infographic.py (Python 核心程式碼 / 腳本)
- code/generate_zoomed_clean_infographic.py (Python 核心程式碼 / 腳本)
- pptx/案例場景.pptx (專案簡報與匯報投影片)
- ssets/uav_f2t2ea_killchain_infographic_4k.jpg (4K 高解析度戰術與架構圖資)
- ssets/uav_f2t2ea_killchain_infographic.jpg (4K 高解析度戰術與架構圖資)
- ssets/uav_f2t2ea_scenario_infographic_4k.jpg (4K 高解析度戰術與架構圖資)
- ssets/uav_f2t2ea_scenario_infographic.jpg (4K 高解析度戰術與架構圖資)

---

## 🏷️ 版本管理 (Version Management)

| 版本號 | 發布日期 | 類型 | 狀態 | 負責模組 |
| :--- | :--- | :--- | :--- | :--- |
| **v1.0.0** | 2026-10-09 | 正式發布 (Stable) | ✅ 已收斂審核 | Turn-23-to-27-UAV-F2T2EA-Killchain-v1 |

---

## 🔄 版本差異說明 (Version Changelog / Diffs)

- **本次更新重點**：
  - 首次發表 uav_f2t2ea_killchain_agent.py（5.3 萬字元完整狀態機實作）；解決戰術圖表中文字體蓋台問題，完成下方獨立中文說明版與放大圖層。
  - 將本對話歷程產生的原始碼、圖表、Word (.docx)、簡報 (.pptx) 與 Markdown 研析報告進行正規化歸檔。
  - 對齊 AI Agent Harness 企業級工程規範，落實全流程審計留痕。
