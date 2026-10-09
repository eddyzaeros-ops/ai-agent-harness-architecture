#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 Obsidian 知識庫筆記 Part 1:
00-Index 知識地圖
01 ~ 06 對話筆記
"""
import os

target_dir = r"D:\Obsidian\MyVault\Harness\AI Service Chain Summary Report"
os.makedirs(target_dir, exist_ok=True)

def write_md(filename, content):
    path = os.path.join(target_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Written: {filename} ({len(content)} chars)")

# ==============================================================================
# 00-Index-AI-Service-Chain-Summary-Report-知識地圖.md
# ==============================================================================
index_md = """---
date: 2026-09-18
title: "AI Service Chain Summary Report 知識地圖與雙向關聯總覽"
phase: "Master Index"
tags:
  - AI_Service_Chain
  - AI_Agent_Harness
  - 知識地圖
  - 雙向連結
  - 縱深防禦
  - 國防AI
  - Synology_Proposal
  - DeepAgents
---

# AI Service Chain Summary Report 知識地圖與雙向關聯總覽

- **知識庫主題**：`AI Service Chain Summary Report`
- **對話 ID**：`4be13bbb-2ae7-4c18-938f-a204665099e4`
- **所屬領域**：國防 AI 服務鏈、Harness 治理外框、零信任架構、AI Agent 安全工程、企業建置提案
- **儲存目錄**：`D:\\Obsidian\\MyVault\\Harness\\AI Service Chain Summary Report\\`
- **附件圖檔**：`D:\\Obsidian\\MyVault\\Harness\\AI Service Chain Summary Report\\assets\\`

---

## 🗺️ 體系架構圖譜 (Architecture & Knowledge Graph)

本知識庫將整個對話歷程的 21 輪交互梳理為 **四大核心演進階段**，每篇筆記皆以原子化主題形式收錄完整圖表、對話脈絡與深度技術思考，並以雙向鏈結環環相扣：

```mermaid
graph TD
    subgraph P1 ["階段一：架構規劃、原則確立與資安補強 (01 ~ 06)"]
        N01["[[01-五大原則與AI服務鏈初版總結報告|01. 五大原則與服務鏈初版報告]]"]
        N02["[[02-Harness雙軌選型與國際標準補強|02. Harness 雙軌選型與國際標準]]"]
        N03["[[03-Gemini審查機制與四大補強面向規劃|03. Gemini 審查與四大補強規劃]]"]
        N04["[[04-K8s算力中心PAM與PQ-Tunnel零信任架構|04. K8s 算力中心、PAM 與 PQ-Tunnel]]"]
        N05["[[05-護欄運作循序流程與五階防護機制|05. 護欄循序流程與五階防護]]"]
        N06["[[06-總結報告V4補充版架構擴充|06. 總結報告 V4 補充版擴充]]"]
        
        N01 --> N02 --> N03 --> N04 --> N05 --> N06
    end

    subgraph P2 ["階段二：簡報微調、結論建置與演講備忘稿 (07 ~ 08)"]
        N07["[[07-Opus深度微調與最終版結論建構|07. Opus 微調與最終版結論頁]]"]
        N08["[[08-23頁簡報逐頁演講備忘稿完整建置|08. 23 頁簡報演講備忘稿完整建置]]"]
        
        N06 --> N07 --> N08
    end

    subgraph P3 ["階段三：DeepAgents 全景研讀與科技感視覺重構 (09 ~ 12)"]
        N09["[[09-DeepAgents-16章全景架構深度研析|09. Deep Agents 16 章全景研析]]"]
        N10["[[10-科技感視覺設計重構與閱讀層次優化|10. 科技感視覺重構與閱讀層次]]"]
        N11["[[11-簡報風格迭代與版本權衡復原|11. 簡報風格迭代與版本權衡]]"]
        N12["[[12-總結報告科技感全面重製|12. 總結報告 23 頁科技感重製]]"]
        
        N08 --> N09 --> N10 --> N11 --> N12
    end

    subgraph P4 ["階段四：企業提案、專題解讀與成果歸檔 (13 ~ 18)"]
        N13["[[13-群暉科技Synology國防AI建置Proposal草稿|13. 群暉科技建置 Proposal 草稿]]"]
        N14["[[14-核心技術解讀-D2與D3敏感資料分級|14. 核心解讀：D2/D3 資料分級]]"]
        N15["[[15-核心技術解讀-AppArmor與cgroup容器隔離|15. 核心解讀：AppArmor + cgroup]]"]
        N16["[[16-核心技術解讀-OPA與Rego政策三維裁決|16. 核心解讀：OPA / Rego 政策裁決]]"]
        N17["[[17-總結報告科技感版手工修訂基準確立|17. 手工修訂基準確立]]"]
        N18["[[18-對話全量紀錄Docx匯出與歸檔|18. 對話全量 Docx 匯出歸檔]]"]
        
        N12 --> N13
        N13 --> N14
        N13 --> N15
        N13 --> N16
        N12 --> N17
        N17 --> N18
    end
```

---

## 📑 筆記章節目錄與主題導覽

### 階段一：架構規劃、原則確立與資安補強
- [[01-五大原則與AI服務鏈初版總結報告|01. 五大原則與AI服務鏈初版總結報告]]：確立「模型分層、資料分級、單一閘道、層層防護、全程留痕」五大鋼鐵原則，建立 17 頁總結報告初版骨幹。
- [[02-Harness雙軌選型與國際標準補強|02. Harness雙軌選型與國際標準補強]]：確立開箱即用 Harness (Claude Code / Codex / Antigravity 2.0) 與客製化 Harness (LangChain DeepAgents) 雙軌矩陣，對齊四大國際標準支柱（NIST RMF, OWASP AISVS, MITRE ATLAS）。
- [[03-Gemini審查機制與四大補強面向規劃|03. Gemini審查機制與四大補強面向規劃]]：以 Gemini 3.1 Pro 視角執行深入審查，規劃四大維度補強策略（實體架構拓撲、護欄時序流、標準對齊、安全控制矩陣）。
- [[04-K8s算力中心PAM與PQ-Tunnel零信任架構|04. K8s算力中心PAM與PQ-Tunnel零信任架構]]：結合使用者附圖一，深入解析院內 GPU 算力中心 Kubernetes 叢集架構、PAM 特權帳號治理、以及符合 NIST SP 800-207 的後量子密碼學 (PQC) PQ-Tunnel 零信任存取隧道。
- [[05-護欄運作循序流程與五階防護機制|05. 護欄運作循序流程與五階防護機制]]：結合使用者附圖二，完整繪製使用者、Portal、Gateway、Guardrail、模型與 Audit Log 的完整時序互動圖，建構五類護欄與處置矩陣。
- [[06-總結報告V4補充版架構擴充|06. 總結報告V4補充版架構擴充]]：嚴格維持 V2 前 17 頁不變，以「補充篇」形式成功追加 5 頁核心技術投影片（擴充至 22 頁）。

### 階段二：簡報微調、結論建置與演講備忘稿
- [[07-Opus深度微調與最終版結論建構|07. Opus深度微調與最終版結論建構]]：以 Claude Opus 4.6 深度審視補充篇內容，針對 Slide 18/20 進行字體呼吸感微調，並撰寫第 23 頁「跨五大原則全景結論頁」，定稿《總結報告_最終版.pptx》。
- [[08-23頁簡報逐頁演講備忘稿完整建置|08. 23頁簡報逐頁演講備忘稿完整建置]]：為全套 23 頁簡報逐頁建立高階專業提報備忘稿（Speaker Notes），兼顧演講節奏、論述邏輯與防護深度。

### 階段三：DeepAgents 全景研讀與科技感視覺重構
- [[09-DeepAgents-16章全景架構深度研析|09. DeepAgents-16章全景架構深度研析]]：啟動 4 組並行研究代理人，深度精讀 Ch01~Ch16 共 400KB 的 LangChain DeepAgents v0.7 官方文件，產出 18 頁高水準《心得報告.pptx》。
- [[10-科技感視覺設計重構與閱讀層次優化|10. 科技感視覺設計重構與閱讀層次優化]]：重構視覺語言，採用極深藍黑背景 (`#0A0F1E`)、科技青 (`#00B4D8`)、左側色條錨定、細邊線與卡片呼吸感，生成《心得報告_v2.pptx》。
- [[11-簡報風格迭代與版本權衡復原|11. 簡報風格迭代與版本權衡復原]]：記錄樣式同步測試歷程，評估總結報告舊版色盤與心得報告科技版視覺差異，精準果斷回復高品質科技感版本。
- [[12-總結報告科技感全面重製|12. 總結報告科技感全面重製]]：將 23 頁總結報告完整重寫並套用科技感設計語言，生成《總結報告_科技感版.pptx》，達到雙簡報設計語言的高度統一。

### 階段四：企業提案、專題解讀與成果歸檔
- [[13-群暉科技Synology國防AI建置Proposal草稿|13. 群暉科技Synology國防AI建置Proposal草稿]]：以群暉科技 (Synology) 儲存安全 DNA 與 DSM Agent 商業實戰經驗為基礎，撰寫 12 大章節《國防AI服務鏈建置Proposal_草稿版.docx》。
- [[14-核心技術解讀-D2與D3敏感資料分級|14. 核心技術解讀-D2與D3敏感資料分級]]：專題剖析 D0~D3 四級資料分類法、DISA IL 等級映射、TLP 交通燈標記、以及「D2/D3 資料零出境」的實體隔離邊界。
- [[15-核心技術解讀-AppArmor與cgroup容器隔離|15. 核心技術解讀-AppArmor與cgroup容器隔離]]：專題剖析 Linux 核心級安全隔離機制：AppArmor（管能做什麼，MAC 行為白名單）與 cgroup（管能用多少，防範死迴圈與 Fork Bomb 資源消耗）。
- [[16-核心技術解讀-OPA與Rego政策三維裁決|16. 核心技術解讀-OPA與Rego政策三維裁決]]：專題剖析 Open Policy Agent (OPA) 與 Rego 語言之「政策即程式碼」理念，解析身分 × 分級 × 用途之三維動態裁決與 fail-closed 預設拒絕防線。
- [[17-總結報告科技感版手工修訂基準確立|17. 總結報告科技感版手工修訂基準確立]]：確認使用者手工修改後之《總結報告_科技感版.pptx》為後續專案之主版本 (Single Source of Truth)。
- [[18-對話全量紀錄Docx匯出與歸檔|18. 對話全量紀錄Docx匯出與歸檔]]：解析完整 21 輪交互日誌，於 `D:\\JavaDO\\對話紀錄` 建立《AI Service Chain Summary Report.docx》，達成對話紀錄的結構化封裝。

---

## 🎯 核心技術映射矩陣 (Five Principles vs Artifacts)

| 五大安全治理原則 | 核心技術實作 | 關聯筆記鏈結 | 核心產出成果 |
|:---|:---|:---|:---|
| **模型分層** (Model Tiering) | L1 通用基礎 → L2 領域 DSLM → L3 Agent → L4 Skill → L5 知識庫；T1~T3 地端 / T4 雲端路由 | [[01-五大原則與AI服務鏈初版總結報告]]<br>[[09-DeepAgents-16章全景架構深度研析]] | 總結報告 S3, S6<br>心得報告 S3 |
| **資料分級** (Data Classification) | D0 公開(IL-2) / D1 內部(IL-3) / D2 敏感(IL-4) / D3 機密(IL-5~6)；C-I-A 三元組；標籤切片繼承 | [[01-五大原則與AI服務鏈初版總結報告]]<br>[[14-核心技術解讀-D2與D3敏感資料分級]] | 總結報告 S3, S10<br>Proposal 第 4, 6 章 |
| **單一閘道** (Single Gateway) | Portal 單一入口 + Gateway 單一出口；API 直連封鎖；OPA/Rego 三維授權；fail-closed | [[01-五大原則與AI服務鏈初版總結報告]]<br>[[16-核心技術解讀-OPA與Rego政策三維裁決]] | 總結報告 S4, S8, S9<br>Proposal 第 4 章 |
| **層層防護** (Defense in Depth) | 六節點縱深防禦 + 五類 Guardrail + 四級沙箱 (AppArmor+cgroup) + PQ-Tunnel 零信任 + HITL | [[04-K8s算力中心PAM與PQ-Tunnel零信任架構]]<br>[[05-護欄運作循序流程與五階防護機制]]<br>[[15-核心技術解讀-AppArmor與cgroup容器隔離]] | 總結報告 S4, S11, S19, S20<br>心得報告 S8, S9, S14 |
| **全程留痕** (Full Auditability) | 8 欄位不可否認紀錄；append-only 防竄改保存 ≥ 1年；SOC 7×24 SIEM；熔斷斷路器；季度紅隊攻防 | [[01-五大原則與AI服務鏈初版總結報告]]<br>[[08-23頁簡報逐頁演講備忘稿完整建置]]<br>[[18-對話全量紀錄Docx匯出與歸檔]] | 總結報告 S7, S9, S13<br>對話紀錄 Docx |
"""

write_md("00-Index-AI-Service-Chain-Summary-Report-知識地圖.md", index_md)

# ==============================================================================
# 01-五大原則與AI服務鏈初版總結報告.md
# ==============================================================================
n01_md = """---
date: 2026-09-13
title: "01. 五大原則與 AI 服務鏈初版總結報告"
phase: "Phase 1: 架構規劃、原則確立與資安補強"
tags:
  - 五大原則
  - AI服務鏈
  - 總結報告
  - 架構研析
  - 縱深防禦
prev: "None"
next: "[[02-Harness雙軌選型與國際標準補強]]"
related:
  - "[[00-Index-AI-Service-Chain-Summary-Report-知識地圖]]"
  - "[[02-Harness雙軌選型與國際標準補強]]"
  - "[[06-總結報告V4補充版架構擴充]]"
  - "[[14-核心技術解讀-D2與D3敏感資料分級]]"
---

# 01. 五大原則與 AI 服務鏈初版總結報告

- **對話輪次**：第 1 輪對話 (Turn 1 / Step 0)
- **記錄日期**：`2026-09-13`
- **所屬階段**：**Phase 1: 架構規劃、原則確立與資安補強**
- **核心關鍵字**：`五大原則` `AI服務鏈` `總結報告` `架構研析` `縱深防禦`
- **主題概述**：依據五大安全治理原則（模型分層、資料分級、單一閘道、層層防護、全程留痕），從全生命週期資料流視角出發，規劃並生成 17 頁《總結報告.pptx》。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：None (本對話起始起點)
* **下一篇 (Next)**：[[02-Harness雙軌選型與國際標準補強]]：因應使用者回饋，精準界定開箱即用與客製化 Harness，並大幅補強國際標準矩陣。
* **中央索引 (Master Index)**：[[00-Index-AI-Service-Chain-Summary-Report-知識地圖]]
* **橫向架構關聯 (Cross References)**：
  - [[14-核心技術解讀-D2與D3敏感資料分級|14. 核心技術解讀：D2/D3 資料分級]]：深入解構資料分級原則在三落點路由中的強制界限。
  - [[16-核心技術解讀-OPA與Rego政策三維裁決|16. 核心技術解讀：OPA / Rego 政策裁決]]：深入解構單一閘道原則的政策裁決核心。

---

## 👤 使用者原始需求指令

> 請總結目前完成的進度摘要，將以 opus 4.6 進行研析及 pptx 製作，以我們規劃的整個 AI 服務鏈資料流角度，記住五大原則："模型分層、資料分級、單一閘道、層層防護、全程留痕"，生成 "總結報告.pptx" 存在 "d:\\JavaDO" 底下。

---

## 🤖 AI 助理深入研析與方案產出

### 1. 五大安全治理原則核心內涵

AI 服務鏈之所有技術規劃與安全防線，皆牢牢錨定於以下五大核心原則：

| 原則名稱 | 英文代稱 | 核心架構內涵 | 落地技術控制措施 |
|:---|:---|:---|:---|
| **模型分層** | Model Tiering | 依照推理能力、部署成本與安全邊界，劃分為 L1 基礎模型、L2 領域 DSLM、L3 Agent 代理、L4 技能工具、L5 領域知識庫。 | 算力中心分級調度；敏感推論落於地端獨立節點；外部公網呼叫嚴格限縮。 |
| **資料分級** | Data Classification | 實施 DISA IL-2 ~ IL-6 四級資料管控（D0 公開、D1 內部、D2 敏感、D3 機密）；落實 C-I-A 三元組評定。 | 標籤繼承至 RAG 向量切塊；D2/D3 實施「資料零出境」；三落點動態路由。 |
| **單一閘道** | Single Gateway | 確立 Portal 為全院單一入口、AI Gateway 為全院單一出口，阻斷所有繞道與影子 AI。 | 防火牆封鎖對外 API 直連；金鑰集中於 Gateway 密鑰庫；OPA/Rego 三維授權裁決；fail-closed。 |
| **層層防護** | Defense in Depth | 建構「六節點縱深防禦」，並在各生命週期佈設 Harness 治理外框、五類 Guardrail 護欄與四級隔離沙箱。 | AppArmor/cgroup 容器隔離；HITL 人工核可中斷點；輸入/輸出雙向 DLP 檢查。 |
| **全程留痕** | Full Auditability | 實施不可否認、防竄改之 8 欄位稽核紀錄，儲存於 append-only 儲存庫，法規保存 ≥ 1 年。 | 全鏈路 Trace ID 追蹤；日誌即時匯流至 SOC SIEM；異常行為觸發自動斷路器熔斷。 |

---

### 2. AI 服務鏈全景資料流：六節點縱深防禦

```mermaid
flowchart LR
    FW["01 邊界防火牆\n(NGFW+IPS)"] --> PT["02 使用者 Portal\n(SSO+MFA+DLP)"]
    PT --> GW["03 AI Gateway\n(OPA三維裁決)"]
    GW --> CMP["04 核心算力中心\n(GPU叢集+SBOM)"]
    CMP --> SBX["05 隔離沙箱\n(即拋容器+AppArmor)"]
    SBX --> GR["06 輸出 Guardrail\n(DLP+浮水印+HITL)"]
    GR -.->|全程稽核匯流| AUD["SOC / SIEM\n8欄位 Append-Only"]
```

1. **節點 01 邊界防火牆**：NGFW + IPS，預設拒絕、白名單放行，出向阻斷任何直連外部 AI API 之流量。
2. **節點 02 使用者 Portal**：雙因素認證 (SSO+MFA)，提示詞前置 DLP 檢驗，防止未授權提示注入與機敏外洩。
3. **節點 03 AI Gateway**：全院核心管控樞紐，執行身分 × 分級 × 用途三維裁決，依資料密級分流至地端或隔離 VPC。
4. **節點 04 核心算力中心**：地端與圍籬算力，模型權重雜湊驗簽與 SBOM 料件管理，切分部門配額。
5. **節點 05 隔離沙箱**：程式碼執行與工具呼叫環境，每次呼叫使用即拋式容器，預設斷網與唯讀保護。
6. **節點 06 輸出 Guardrail**：機敏資訊偵測與遮罩，幻覺與來源真實性比對，高衝擊動作強制觸發 HITL 審批。

---

### 3. 初版 17 頁簡報架構大綱

* **Slide 01: 封面** — 國防 AI 服務鏈總結報告、五大原則徽章。
* **Slide 02: 報告目錄** — 涵蓋 14 大核心主題章節。
* **Slide 03: 五大原則總覽** — 模型分層、資料分級、單一閘道、層層防護、全程留痕。
* **Slide 04: AI 服務鏈全景架構** — 六節點縱深防禦與 Harness 橫向貫穿。
* **Slide 05: Agent 開發者 — 行政庶務流程** — 開發生命週期與安全基線。
* **Slide 06: Agent 開發者 — 武器系統流程** — 高密級戰術代理人與多層沙箱。
* **Slide 07: Agent 開發者 — 管控與軌跡** — Harness 四項強制功能與 8 欄位留痕。
* **Slide 08: Agent 使用者 — Portal 操作流程** — 11 步端到端資料流與 HITL 流程。
* **Slide 09: Agent 使用者 — 管控與軌跡** — Portal/Gateway 雙管控與 fail-closed。
* **Slide 10: 資安防護（一）** — 單向閘道 Diode/CDS、DLP 即時掃描、三落點路由。
* **Slide 11: 資安防護（二）** — 資料治理五步管線、Guardrail 五類佈設點。
* **Slide 12: 資安防護（三）** — 國際標準與法規體系總覽。
* **Slide 13: 資安防護（四）** — SOC 監控、異常斷路器熔斷、季度紅隊演練。
* **Slide 14: 端到端全景工作流程** — 完整資料鏈路與 16 項資安防護檢核清單。
* **Slide 15: AI 服務鏈 Roadmap** — Q1~Q4 四階段建置藍圖。
* **Slide 16: 效益評估與 KPI** — 100% 閘道覆蓋率、0 件資料出境、風險降低矩陣。
* **Slide 17: 結論與下一步行動** — 核心建置成果與近期行動建議。

---

## 💡 深度理解與架構啟示

1. **戰略價值**：五大原則並非孤立的規範，而是緊密互鎖的防禦矩陣。例如，「單一閘道」確保所有流量必經檢核，方能支撐「資料分級」與「全程留痕」的實現。
2. **工程挑戰**：初版報告確立了整體框架，但對於實體網路部署（如 K8s 算力調度、零信任網路技術）以及業界標準之細化對標，仍需進一步深化補強。
"""

write_md("01-五大原則與AI服務鏈初版總結報告.md", n01_md)

# ==============================================================================
# 02-Harness雙軌選型與國際標準補強.md
# ==============================================================================
n02_md = """---
date: 2026-09-13
title: "02. Harness 雙軌選型與國際標準補強"
phase: "Phase 1: 架構規劃、原則確立與資安補強"
tags:
  - Harness選型
  - ClaudeCode
  - OpenAI_Codex
  - Antigravity
  - LangChain_DeepAgents
  - 國際標準
prev: "[[01-五大原則與AI服務鏈初版總結報告]]"
next: "[[03-Gemini審查機制與四大補強面向規劃]]"
related:
  - "[[00-Index-AI-Service-Chain-Summary-Report-知識地圖]]"
  - "[[01-五大原則與AI服務鏈初版總結報告]]"
  - "[[09-DeepAgents-16章全景架構深度研析]]"
  - "[[13-群暉科技Synology國防AI建置Proposal草稿]]"
---

# 02. Harness 雙軌選型與國際標準補強

- **對話輪次**：第 2 輪對話 (Turn 2 / Step 32)
- **記錄日期**：`2026-09-13`
- **所屬階段**：**Phase 1: 架構規劃、原則確立與資安補強**
- **核心關鍵字**：`Harness選型` `ClaudeCode` `OpenAI_Codex` `Antigravity` `LangChain_DeepAgents` `國際標準`
- **主題概述**：明確界定「開箱即用 Harness」與「客製化 Harness」的分類標準，並將 AI 國際標準全面補強至四大支柱 29 項規範。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：[[01-五大原則與AI服務鏈初版總結報告]]：初版總結報告建立了 17 頁架構骨幹。
* **下一篇 (Next)**：[[03-Gemini審查機制與四大補強面向規劃]]：在概念界定清楚後，啟動多視角審查與補強規劃。
* **中央索引 (Master Index)**：[[00-Index-AI-Service-Chain-Summary-Report-知識地圖]]
* **橫向架構關聯 (Cross References)**：
  - [[09-DeepAgents-16章全景架構深度研析|09. Deep Agents 16 章全景研析]]：詳盡探討客製化 Harness 的底層機制（VFS、中間件、沙箱、權限）。
  - [[13-群暉科技Synology國防AI建置Proposal草稿|13. 群暉科技建置 Proposal 草稿]]：將雙軌 Harness 選型作為提案書第 5 章的核心工作範疇。

---

## 👤 使用者原始需求指令

> 請依據下面，修調 pptx 內容：
> 1. 我說的開箱即用的 Harness 指的是像：claude code、OpenAI codex、Google antigravity 2.0 這些工具，LangChain DeepAgents 我定義為需客製化開發的 Harness
> 2. AI 國際標準，需包括 NISP RMF 1.0、OWASP AISVS、OWASP Top 10 for LLM/Agents/Skills、MITRE ATLAS 等，不足的話，請你務必補充
> 3. 務必參考 "D:\\JavaDO\\AI_Agent_Harness整合提報版_20260906.pptx" 的內容，內容非常詳細

---

## 🤖 AI 助理深入研析與方案產出

### 1. Harness 雙軌分類體系定義

針對國防與高安全組織需求，將 Agent Harness 明確拆解為雙軌選型架構：

```mermaid
graph TD
    Harness["AI Agent Harness 分類體系"]
    
    Harness --> OOB["軌道一：開箱即用 Harness\n(Out-of-the-Box)"]
    Harness --> CUS["軌道二：客製化開發 Harness\n(Customized Harness)"]
    
    OOB --> C1["Claude Code (Anthropic)"]
    OOB --> C2["OpenAI Codex (OpenAI)"]
    OOB --> C3["Google Antigravity 2.0 (Google DeepMind)"]
    
    CUS --> D1["LangChain DeepAgents v0.7\n(LangChain + LangGraph)"]
    
    OOB -.-> App1["應用場景：行政庶務 Agent (IL-2 ~ IL-4)\n特點：即裝即用、內建治理、快速賦能"]
    CUS -.-> App2["應用場景：武器戰術系統 Agent (IL-5 ~ IL-6)\n特點：深度解耦、四級沙箱、極致安全"]
```

#### 開箱即用 vs 客製化 Harness 對照矩陣

| 評估維度 | 開箱即用 Harness (OOB) | 客製化開發 Harness (Customized) |
|:---|:---|:---|
| **代表工具** | Claude Code, OpenAI Codex, Google Antigravity 2.0 | LangChain DeepAgents v0.7 (基於 LangGraph) |
| **適用業務場景** | 行政庶務、公文撰擬、內部問答、報表整理 | 武器系統、情資研析、戰術決策支援、交戰模擬 |
| **支援資料密級** | DISA IL-2 ~ IL-4 (D0 公開 / D1 內部 / D2 敏感) | DISA IL-5 ~ IL-6 (D2 核心營業秘密 / D3 軍事機密) |
| **權限控制模式** | 工具自帶 Deny-First 白名單與工作區綁定 | 多層檔案系統 ACL (VFS) + 四級沙箱 (L0~L3) 隔離 |
| **HITL 審批能力** | 工具層單點審核 (Prompt 前置確認) | 多節點鏈式中斷 `interrupt()` + 狀態快照保存 |
| **模型適配彈性** | 依賴特定廠商雲端/端點 API | 抽象化介面，相容 100+ 地端隔離模型與私有雲 |
| **治理擴展性** | 封閉或半封閉治理外框 | 開放式三層中間件 (Middleware) 任意自訂插拔 |
| **開發建置週期** | 數天至 1~2 週內快速部署 | 2~3 個月深度客製化研發與紅隊驗證 |

---

### 2. AI 國際標準與法規四大支柱體系

全面梳理並對齊國際頂級 AI 資安治理標準，構築四大支柱矩陣：

```
┌────────────────────────────────────────────────────────────────────────┐
│                   AI 國際標準與法規體系（四大支柱）                    │
├──────────────────┬──────────────────┬──────────────────┬───────────────┤
│  01. ISO 治理框架│  02. NIST 風險   │  03. OWASP 技術  │  04. 威脅法制 │
├──────────────────┼──────────────────┼──────────────────┼───────────────┤
│• ISO/IEC 42001   │• NIST AI RMF 1.0 │• LLM Top 10 2025 │• MITRE ATLAS  │
│  (AI 管理系統)   │  (治理/測繪/評量)│  (注入/外洩/鏈)  │  (對抗戰術庫) │
│• ISO/IEC 27001   │• NIST AI 600-1   │• Agentic AI Top10│• EU AI Act    │
│  (資安管理體系)  │  (GenAI 剖繪)    │  (記憶投毒/越權) │  (風險分級法) │
│• ISO/IEC 27017/18│• NIST SP 800-53  │• OWASP AISVS     │• CISA/NSA     │
│  (雲端安全/個資) │  (安全控制基線)  │  (安全驗證分級)  │  (部署指引)   │
│• ISO/IEC 27040   │• NIST SP 800-218A│• ML Security Top │• CNSSI 1253   │
│  (儲存安全)      │  (安全開發 SSDF) │  (投毒/逆向工程) │  (國安等級)   │
│• ISO/IEC 27701   │• NIST SP 800-207 │• AI Exchange     │• DISA CC SRG  │
│  (隱私資訊管理)  │  (零信任架構)    │  (威脅對映標準)  │  (IL2~IL6軍規)│
│• ISO 17025       │• NIST SP 800-171 │• Red Teaming 指引│• 資通安全管理法│
│  (實驗室稽核能力)│  (CUI 受控保護)  │  (紅隊演練規範)  │  (A級防護基準)│
└──────────────────┴──────────────────┴──────────────────┴───────────────┘
```

---

## 💡 深度理解與架構啟示

1. **務實的落地策略**：若全院均採用客製化開發，將面臨極高的研發與維護成本；若全院皆用開箱即用工具，則無法滿足武器系統 IL-5/IL-6 的極端隔離要求。**雙軌架構精準化解了「開發速度」與「極致安全」的矛盾。**
2. **標準體系的縱向貫通**：治理制度（ISO 42001）由高層向下指導；風險流程（NIST AI RMF）建立操作指引；技術控制（OWASP）防禦具體攻擊；威脅驗證（MITRE ATLAS）提供紅隊攻防語料。四者形成完整閉環。
"""

write_md("02-Harness雙軌選型與國際標準補強.md", n02_md)

# ==============================================================================
# 03-Gemini審查機制與四大補強面向規劃.md
# ==============================================================================
n03_md = """---
date: 2026-09-13
title: "03. Gemini 審查機制與四大補強面向規劃"
phase: "Phase 1: 架構規劃、原則確立與資安補強"
tags:
  - Gemini審查
  - 補強規劃
  - 拓撲架構
  - 護欄時序
  - 標準對齊
prev: "[[02-Harness雙軌選型與國際標準補強]]"
next: "[[04-K8s算力中心PAM與PQ-Tunnel零信任架構]]"
related:
  - "[[00-Index-AI-Service-Chain-Summary-Report-知識地圖]]"
  - "[[04-K8s算力中心PAM與PQ-Tunnel零信任架構]]"
  - "[[05-護欄運作循序流程與五階防護機制]]"
  - "[[06-總結報告V4補充版架構擴充]]"
---

# 03. Gemini 審查機制與四大補強面向規劃

- **對話輪次**：第 3~4 輪對話 (Turn 3~4 / Step 55~57)
- **記錄日期**：`2026-09-13`
- **所屬階段**：**Phase 1: 架構規劃、原則確立與資安補強**
- **核心關鍵字**：`Gemini審查` `補強規劃` `拓撲架構` `護欄時序` `標準對齊`
- **主題概述**：切換至 Google Gemini 3.1 Pro 視角執行深入架構審查，鎖定四大不足之處並提出具體補強規劃方案，等待使用者拍板同意。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：[[02-Harness雙軌選型與國際標準補強]]：確立了雙軌選型與四大標準支柱。
* **下一篇 (Next)**：[[04-K8s算力中心PAM與PQ-Tunnel零信任架構]]：使用者批准規劃並要求依據附圖一深化 K8s 與 PAM 實作。
* **中央索引 (Master Index)**：[[00-Index-AI-Service-Chain-Summary-Report-知識地圖]]
* **橫向架構關聯 (Cross References)**：
  - [[05-護欄運作循序流程與五階防護機制|05. 護欄運作循序流程與五階防護]]：落實四大面向中「護欄運作動態循序流程」之深化。
  - [[06-總結報告V4補充版架構擴充|06. 總結報告 V4 補充版擴充]]：將本規劃轉化為具體補充篇投影片。

---

## 👤 使用者原始需求指令

> 請總結目前完成的進度，將以 Gemini 3.1 pro 來 review pptx 內容，並進行必要及補強性的補充：
> 1. 先研究相關的內容，可以去外面找
> 2. 先提出你的規劃內容，等我同意後再進行

---

## 🤖 AI 助理深入研析與方案產出

### 1. 進度總結與審查現況分析

* **已完成資產**：`總結報告_v2.pptx`（共 17 頁），具備雙軌 Harness 分類與 29 項國際標準支柱。
* **Gemini 3.1 Pro 審查洞察**：
  1. 現有架構偏向「概念層」與「邏輯層」，缺乏地端算力中心與實體網路硬體配置的**具體拓撲層**。
  2. 護欄（Guardrail）機制列出了靜態類別，但缺乏使用者發送請求後，各節點間的**動態時序互動流（Sequence Flow）**。
  3. 軟體供應鏈安全（SBOM）與微服務/工具整合（MCP）的安全驗證流程尚未展開。
  4. 零信任架構（ZTA）與後量子密碼（PQC）在資料通道中的具體實踐有待加強。

---

### 2. 四大補強面向規劃提案

```mermaid
mindmap
  root((Gemini 3.1 Pro\n補強規劃四大面向))
    面向一：資安實體拓撲與算力架構
      Kubernetes 容器編排叢集
      特權帳號管理 PAM
      後量子安全隧道 PQ-Tunnel
      NIST SP 800-207 零信任網路
    面向二：護欄動態循序流程
      Actor 到 Agent 的呼叫鏈
      Guardrail 攔截審查邏輯
      LLM 推論與輸出審核
      不可否認 Audit Log 留痕
    面向三：供應鏈安全與外部整合
      SBOM 軟體料件清單驗證
      模型權重數位簽章
      MCP 伺服器自建自審機制
      API 能力憑證隔離
    面向四：零信任縱深防禦與演練
      微分段與邊界防護
      SOC 關聯分析與斷路器
      季度紅隊 AI 攻防演練
      Fail-Closed 機制驗收
```

1. **補強面向一：資安方案與算力中心實體拓撲**
   - 院內算力中心 Kubernetes (K8s) GPU 節點調度與租戶資源隔離。
   - PAM (Privileged Access Management) 特權帳號存取管控。
   - 導入 PQC (Post-Quantum Cryptography) 之 PQ-Tunnel 建立零信任傳輸通道，符合 NIST SP 800-207。

2. **補強面向二：護欄運作循序流程說明 (Sequence Diagram)**
   - 繪製清晰的時序互動圖：使用者 (Actor) → Portal → Gateway → Guardrail → LLM → Audit Log。
   - 明確標示「請求前置檢查」、「檢索過濾」、「輸出淨化」與「違規阻斷」的即時處置流。

3. **補強面向三：軟體供應鏈安全 (SBOM) 與 MCP 工具治理**
   - 模型權重簽章驗證、開源元件 SBOM 清單比對與漏洞掃描。
   - Model Context Protocol (MCP) 自建自審政策，工具呼叫強制進行 Schema 驗證與沙箱隔離。

4. **補強面向四：零信任微分段與紅隊驗證閉環**
   - 強化南北向/東西向微分段防禦，落實 Policy as Code。
   - 建立紅隊 AI 演練量化指標（越獄成功率、誤攔率 FPR、洩漏率）。

---

## 💡 深度理解與架構啟示

* **多模型交叉審查的價值**：自 Claude Opus 4.6 切換至 Gemini 3.1 Pro，能跳脫單一模型的思維定勢，敏銳發現架構中「邏輯完備但實體缺失」的斷層。
* **規範化提案原則**：遵守「先規劃、獲同意、後執行」的敏捷溝通規範，確保架構擴展完全符合決策者的核心戰略預期。
"""

write_md("03-Gemini審查機制與四大補強面向規劃.md", n03_md)

# ==============================================================================
# 04-K8s算力中心PAM與PQ-Tunnel零信任架構.md
# ==============================================================================
n04_md = """---
date: 2026-09-13
title: "04. K8s 算力中心、PAM 與 PQ-Tunnel 零信任架構"
phase: "Phase 1: 架構規劃、原則確立與資安補強"
tags:
  - 算力中心
  - Kubernetes
  - PAM特權管理
  - PQ_Tunnel
  - 零信任架構
  - NIST_SP_800_207
  - 附圖一
prev: "[[03-Gemini審查機制與四大補強面向規劃]]"
next: "[[05-護欄運作循序流程與五階防護機制]]"
related:
  - "[[00-Index-AI-Service-Chain-Summary-Report-知識地圖]]"
  - "[[03-Gemini審查機制與四大補強面向規劃]]"
  - "[[05-護欄運作循序流程與五階防護機制]]"
  - "[[06-總結報告V4補充版架構擴充]]"
  - "[[15-核心技術解讀-AppArmor與cgroup容器隔離]]"
---

# 04. K8s 算力中心、PAM 與 PQ-Tunnel 零信任架構

- **對話輪次**：第 5 輪對話 (Turn 5 / Step 61)
- **記錄日期**：`2026-09-13`
- **所屬階段**：**Phase 1: 架構規劃、原則確立與資安補強**
- **核心關鍵字**：`算力中心` `Kubernetes` `PAM特權管理` `PQ_Tunnel` `零信任架構` `NIST_SP_800_207` `附圖一`
- **主題概述**：依據使用者提供之附圖一（圖73 資安方案與本案架構說明），深入設計院內算力中心 Kubernetes 叢集、特權帳號管理 (PAM)、以及後量子密碼學 (PQC) PQ-Tunnel 零信任存取架構。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：[[03-Gemini審查機制與四大補強面向規劃]]：規劃了實體拓撲與算力架構的補強方向。
* **下一篇 (Next)**：[[05-護欄運作循序流程與五階防護機制]]：接續處理使用者提供的附圖二（護欄運作循序流程）。
* **中央索引 (Master Index)**：[[00-Index-AI-Service-Chain-Summary-Report-知識地圖]]
* **橫向架構關聯 (Cross References)**：
  - [[06-總結報告V4補充版架構擴充|06. 總結報告 V4 補充版擴充]]：將本篇內容具體實作為 Slide 19 投影片。
  - [[15-核心技術解讀-AppArmor與cgroup容器隔離|15. 核心技術解讀：AppArmor + cgroup]]：深入解析 K8s 工作節點內部容器沙箱的核心安全機制。

---

## 👤 使用者原始需求指令

> 同意上述 4 點補強規劃，請再加強：
> 1. SBOM，軟體料件清單管控
> 2. 參考附圖一的資安架構圖，院內算力中心使用 Kubernets(K8s) 架構及 PAM 特權帳號管理
> 3. 導入 PQC 的 PQ tunnel 零信任網路管理平台，符合 NISP SP 800-207
> 4. 參考附圖二的護欄運作循序流程圖
> 
> 先提出你的規劃內容，等我同意後再進行

---

## 🖼️ 架構參考依據：圖73 資安方案與本案架構說明

![[assets/fig73_k8s_pam_security_arch.jpg]]
*圖 73：資安方案與本案架構拓撲說明（院內算力中心、K8s 叢集、PAM 與網路拓撲）*

---

## 🤖 AI 助理深入研析與方案產出

### 1. 實體與邏輯拓撲架構

結合附圖一之架構配置，本案於地端與邊界建立高安全隔離分段：

```mermaid
graph TD
    subgraph ClientZone ["客戶端與傳輸邊界 (Zero Trust Perimeter)"]
        User["終端使用者 / 管理員"]
        PQ["PQ-Tunnel 零信任管理平台\n(PQC 後量子加密通道 · NIST SP 800-207)"]
        PAM["PAM 特權帳號管理系統\n(Session 錄影 · MFA · 動態提權)"]
        
        User -->|加密通道| PQ
        User -.->|特權操作需經| PAM
    end

    subgraph CoreSwitch ["核心交換與邊界隔離"]
        CS["核心交換機 (Core Switch) / 微分段防火牆"]
        PQ --> CS
        PAM --> CS
    end

    subgraph ComputeCluster ["院內核心算力中心 (Kubernetes Cluster)"]
        CS --> K8sM["K8s Control Plane / Master"]
        
        subgraph WorkerNodes ["GPU / CPU 運算節點"]
            W1["Worker Node 1\n(AMD MI355X / NVIDIA B200)"]
            W2["Worker Node 2\n(GPU 資源隔離 · cgroup)"]
            W3["Worker Node 3\n(推論容器沙箱 · AppArmor)"]
        end
        
        K8sM --> W1
        K8sM --> W2
        K8sM --> W3
    end

    subgraph StorageZone ["安全儲存與留痕專區"]
        NAS["不可竄改儲存系統 (WORM / Append-Only)\n(審計紀錄 · 模型權重 · 訓練語料)"]
        W1 -.-> NAS
        W2 -.-> NAS
        W3 -.-> NAS
    end
```

---

### 2. 三大核心安全支柱深度解析

#### 支柱一：院內算力中心 Kubernetes (K8s) 架構
1. **多租戶資源切分**：以 Namespace 切分不同單位與機密專案，配置專屬 ResourceQuota 與 LimitRange，嚴格限制 GPU/CPU 算力佔用。
2. **網路安全政策 (NetworkPolicy)**：預設啟用 Default-Deny-All，僅開放 Pod 間經核可之標籤通訊；封鎖未授權之橫向移動 (Lateral Movement)。
3. **工作節點強化**：節點運行客製化 Linux 核心，整合 AppArmor 安全配置與 cgroup 資源限制，確保 Agent 程式碼無法越權存取宿主主機。

#### 支柱二：PAM (Privileged Access Management) 特權帳號治理
1. **特權存取受控**：算力叢集節點、資料庫與模型權重之管理權限全面收歸 PAM 系統，禁止系統管理員直連根帳號。
2. **即時會話監控與側錄**：所有 SSH/RDP/Kubectl 終端操作實施全程錄影與指令紀錄，嚴禁未授權之高危指令執行。
3. **一次性動態認證 (JIT / JEA)**：落實 Just-In-Time 授權與 Just-Enough-Access 原則，憑證即用即拋，消除靜態密鑰外洩風險。

#### 支柱三：PQC 之 PQ-Tunnel 零信任網路平台 (NIST SP 800-207)
1. **後量子密碼演算法 (PQC)**：通道採用 NIST 標準化抗量子加密演算法（如 ML-KEM / Kyber 密鑰封裝、ML-DSA / Dilithium 數位簽章），防範「先攔截、後解密」(Harvest Now, Decrypt Later) 之威脅。
2. **零信任持續驗證**：符合 NIST SP 800-207 標準，每次連線皆評估終端設備健康狀態、使用者身分、地理時序等屬性，不因身處內網而降低認證要求。
3. **微分段動態穿透**：使用者僅能存取經 OPA/Rego 策略明確授權的特定服務端點，完全隱蔽內部算力網路拓撲。

---

## 💡 深度理解與架構啟示

* **前瞻防禦的必要性**：軍事與國防資料具有極長之機密保密年限（20~30 年）。傳統 RSA/ECC 加密恐於未來量子電腦成熟時遭破解，因此**在資料傳輸層直接導入 PQC PQ-Tunnel 是保護國防核心資產的關鍵技術決策**。
* **軟硬體無縫銜接**：將軟體層的 Agent Harness 與基礎設施層的 K8s/PAM/PQC 深度整合，使安全防線下沉至網路封包與容器命名空間層級，杜絕單點失效。
"""

write_md("04-K8s算力中心PAM與PQ-Tunnel零信任架構.md", n04_md)

# ==============================================================================
# 05-護欄運作循序流程與五階防護機制.md
# ==============================================================================
n05_md = """---
date: 2026-09-13
title: "05. 護欄運作循序流程與五階防護機制"
phase: "Phase 1: 架構規劃、原則確立與資安補強"
tags:
  - 護欄循序流程
  - SequenceDiagram
  - 處置矩陣
  - 提示注入防護
  - 附圖二
  - 五階防護
prev: "[[04-K8s算力中心PAM與PQ-Tunnel零信任架構]]"
next: "[[06-總結報告V4補充版架構擴充]]"
related:
  - "[[00-Index-AI-Service-Chain-Summary-Report-知識地圖]]"
  - "[[04-K8s算力中心PAM與PQ-Tunnel零信任架構]]"
  - "[[06-總結報告V4補充版架構擴充]]"
  - "[[16-核心技術解讀-OPA與Rego政策三維裁決]]"
---

# 05. 護欄運作循序流程與五階防護機制

- **對話輪次**：第 5~6 輪對話 (Turn 5~6 / Step 61~63)
- **記錄日期**：`2026-09-13`
- **所屬階段**：**Phase 1: 架構規劃、原則確立與資安補強**
- **核心關鍵字**：`護欄循序流程` `SequenceDiagram` `處置矩陣` `提示注入防護` `附圖二` `五階防護`
- **主題概述**：依據使用者提供之附圖二（圖79 護欄運作循序流程說明），完整構建從使用者輸入、Portal 前置檢查、Gateway 政策裁決、Guardrail 雙向過濾、LLM 推論到不可否認 Audit Log 留痕的完整動態時序流程圖。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：[[04-K8s算力中心PAM與PQ-Tunnel零信任架構]]：完成了實體拓撲與算力架構規劃。
* **下一篇 (Next)**：[[06-總結報告V4補充版架構擴充]]：使用者全面同意規劃，啟動 V4 補充版簡報製作。
* **中央索引 (Master Index)**：[[00-Index-AI-Service-Chain-Summary-Report-知識地圖]]
* **橫向架構關聯 (Cross References)**：
  - [[06-總結報告V4補充版架構擴充|06. 總結報告 V4 補充版擴充]]：將本流程實作為 Slide 20 投影片。
  - [[16-核心技術解讀-OPA與Rego政策三維裁決|16. 核心技術解讀：OPA / Rego 政策裁決]]：深入解析流程中 Step 3 Gateway 的裁決演算法。

---

## 🖼️ 架構參考依據：圖79 護欄運作循序流程說明

![[assets/fig79_guardrail_sequence_flow.jpg]]
*圖 79：護欄運作循序流程說明（使用者操作、Guardrail 雙向檢核、模型推論與稽核紀錄）*

---

## 🤖 AI 助理深入研析與方案產出

### 1. 護欄運作循序流程 (Detailed Sequence Diagram)

```mermaid
sequenceDiagram
    autonumber
    actor User as 使用者 (Actor)
    participant Portal as AI Portal (使用者入口)
    participant Gateway as AI Gateway (OPA裁決)
    participant InGR as 輸入/檢索 Guardrail
    participant Agent as Agent 核心 / LLM
    participant OutGR as 輸出 Guardrail / DLP
    participant Audit as 稽核系統 (Audit Log / SOC)

    User->>Portal: 1. 提交 Prompt 請求與操作指令
    activate Portal
    Portal->>Portal: 2. 前置檢查 (身分驗證/格式檢查)
    Portal->>Gateway: 3. 轉發請求 (包含使用者身分與密級標籤)
    activate Gateway
    
    Gateway->>Gateway: 4. OPA/Rego 策略三維裁決 (身分×分級×用途)
    alt 裁決拒絕 (Deny)
        Gateway-->>Audit: 記錄違規阻斷事件
        Gateway-->>Portal: 回傳阻斷訊息
        Portal-->>User: 顯示無權存取 / 策略阻斷
    else 裁決放行 (Allow)
        Gateway->>InGR: 5. 進入輸入護欄檢核
        activate InGR
        InGR->>InGR: 6. Prompt Injection 偵測 / PII 遮罩 / 敏感詞過濾
        alt 輸入檢核違規 (Block)
            InGR-->>Audit: 記錄攻擊/外洩日誌
            InGR-->>Gateway: 阻斷通知
            Gateway-->>User: 請求包含機敏或惡意指令，已終止
        else 輸入檢核通過 (Pass)
            InGR->>Agent: 7. 派發安全提示詞至 Agent
            activate Agent
            Agent->>Agent: 8. 推論計算 / 工具呼叫 (Tool Calls)
            Agent->>OutGR: 9. 產出原始回覆內容
            deactivate Agent
            activate OutGR
            
            OutGR->>OutGR: 10. 輸出檢核 (DLP掃描/機密外洩偵測/幻覺比對)
            alt 觸發高衝擊動作 (HITL Required)
                OutGR->>Portal: 11. 掛起執行，呈現審批面板給審核官
                Portal->>User: 等候主管/法律官核准
            else 輸出安全通過 (Clean)
                OutGR->>Gateway: 12. 回傳安全脫敏回覆
                deactivate OutGR
                Gateway->>Audit: 13. 全量寫入 8 欄位不可否認稽核紀錄 (append-only)
                Gateway->>Portal: 14. 交付加註浮水印與分級標記之內容
                deactivate Gateway
                Portal-->>User: 15. 使用者查閱/下載成果
                deactivate Portal
            end
        end
    end
```

---

### 2. 五類護欄佈設與防護職責

| 護欄類型 | 佈設位置 | 核心檢核職責 | 典型攔截威脅 |
|:---|:---|:---|:---|
| **輸入護欄** (Input Guardrail) | Portal / Gateway 入口 | 身分檢驗、輸入長度規範、Prompt Injection 偵測、越獄防護。 | 惡意提示注入、越獄字串、格式破壞攻擊。 |
| **檢索護欄** (Retrieval Guardrail) | RAG Pipeline 檢索層 | 依使用者密級過濾向量索引、去除外部文件夾帶之隱含指令、標記外部語料為不可信。 | 間接提示注入 (Indirect Injection)、跨密級資料窺探。 |
| **工具/動作護欄** (Tool Guardrail) | Harness Middleware | 工具白名單限制、參數 Schema 強制校驗、副作用與資源範圍限制。 | 惡意指令執行、非預期系統寫入、超額調用。 |
| **輸出護欄** (Output Guardrail) | Gateway 出口前置層 | DLP 內容掃描、個資/座標自動遮蔽、引用依據比對、數位浮水印加註。 | 機敏資料外洩、模型幻覺、無來源虛構。 |
| **行為/迴圈護欄** (Behavior Guardrail) | Harness Runtime 執行層 | 步數上限熔斷、Token 配額限制、死迴圈與重複動作偵測、成本防暴衝。 | Agent 迴圈暴衝 (Fork Bomb)、資源耗盡攻擊 (DoS)。 |

---

### 3. 處置矩陣 (Decision & Action Matrix)

```
[檢核結果] ──┬── 通過 (Pass) ───────────→ 【放行 Allow】 (保留完整稽核紀錄)
              ├── 低度敏感/個資 ────────→ 【去識別 Redact】 (遮罩脫敏後放行)
              ├── 格式錯誤/輕微幻覺 ────→ 【改寫重試 Rewrite】 (限次自動退回修正)
              ├── 機密外洩/惡意注入 ────→ 【阻斷 Block】 (立即終止 + 觸發告警)
              └── 高衝擊/系統變更 ──────→ 【轉人工 Escalate】 (HITL 審批核可後放行)
```

---

## 💡 深度理解與架構啟示

* **動態防護與靜態防線的結合**：單有防火牆與權限白名單不足以抵禦 GenAI 特有的提示語意攻擊。本流程將護欄細分為輸入、檢索、工具、輸出、行為五個切入點，實現了**語意層級的縱深防禦**。
* **Fail-Closed 鋼鐵法則**：流程中任何一個檢查模組發生超時、宕機或內部異常，系統一律判定為「不通過」，絕不採取鬆懈放行策略。
"""

write_md("05-護欄運作循序流程與五階防護機制.md", n05_md)

# ==============================================================================
# 06-總結報告V4補充版架構擴充.md
# ==============================================================================
n06_md = """---
date: 2026-09-13
title: "06. 總結報告 V4 補充版架構擴充"
phase: "Phase 1: 架構規劃、原則確立與資安補強"
tags:
  - 總結報告V4
  - 補充篇
  - 不動原檔
  - PPTX生成
  - 投影片擴充
prev: "[[05-護欄運作循序流程與五階防護機制]]"
next: "[[07-Opus深度微調與最終版結論建構]]"
related:
  - "[[00-Index-AI-Service-Chain-Summary-Report-知識地圖]]"
  - "[[04-K8s算力中心PAM與PQ-Tunnel零信任架構]]"
  - "[[05-護欄運作循序流程與五階防護機制]]"
  - "[[07-Opus深度微調與最終版結論建構]]"
  - "[[08-23頁簡報逐頁演講備忘稿完整建置]]"
---

# 06. 總結報告 V4 補充版架構擴充

- **對話輪次**：第 7 輪對話 (Turn 7 / Step 73)
- **記錄日期**：`2026-09-13`
- **所屬階段**：**Phase 1: 架構規劃、原則確立與資安補強**
- **核心關鍵字**：`總結報告V4` `補充篇` `不動原檔` `PPTX生成` `投影片擴充`
- **主題概述**：嚴格遵循使用者「不更動總結報告_v2.pptx 原有內容及樣式，採補充方式新增」的要求，以獨立 Python 腳本追加 5 頁核心補充內容，成功產出 22 頁《總結報告_v4_補充版.pptx》。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：[[05-護欄運作循序流程與五階防護機制]]：確認了護欄循序時序流程。
* **下一篇 (Next)**：[[07-Opus深度微調與最終版結論建構]]：切換至 Opus 4.6 進行深度品質審核，並追加最後第 23 頁結論頁。
* **中央索引 (Master Index)**：[[00-Index-AI-Service-Chain-Summary-Report-知識地圖]]
* **橫向架構關聯 (Cross References)**：
  - [[04-K8s算力中心PAM與PQ-Tunnel零信任架構|04. K8s 算力中心 PAM 架構]]：轉化為補充篇第 19 頁。
  - [[05-護欄運作循序流程與五階防護機制|05. 護欄運作循序流程]]：轉化為補充篇第 20 頁。

---

## 👤 使用者原始需求指令

> 1. 請不要更動 "總結報告_v2.pptx" 所有的內容及樣式，
> 2. 請用補充的方式，增加及更新 pptx 內容，不要更動原來投影片

---

## 🤖 AI 助理深入研析與方案產出

### 1. 工程實踐策略：保持原版基線，追加補充篇

為確保前 17 頁已有成果之排版、字級、佈局百分之百不受影響，設計自動化腳本：
1. 直接載入 `總結報告_v2.pptx` 之 Presentation 物件。
2. 保留原 17 頁所有形狀、文字框與母片設定。
3. 依序在尾部新增 5 頁補充簡報，標記為「補充 - 1」至「補充 - 5」。
4. 另存為獨立新檔：`D:\\JavaDO\\總結報告_v4_補充版.pptx`。

---

### 2. 補充篇 5 頁內容架構設計

```
[總結報告_v2.pptx (1~17 頁 原有內容完整鎖定)]
                    │
                    ▼ 追加「補充篇」
┌────────────────────────────────────────────────────────────────────────┐
│ Slide 18: 補充篇過渡頁 ── 深度架構細節與技術補充                       │
│ • 標明四大補充主軸：實體拓撲、護欄時序、供應鏈SBOM、零信任微服務       │
├────────────────────────────────────────────────────────────────────────┤
│ Slide 19: 補充 01 ── 實體架構與零信任網管 (基於附圖一)                 │
│ • 院內算力中心 K8s GPU 叢集排程 (AMD MI355X / NVIDIA B200)             │
│ • PAM 特權帳號管理 (Session 側錄 / 一次性動態權限)                    │
│ • PQC PQ-Tunnel 零信任存取隧道 (符合 NIST SP 800-207)                  │
├────────────────────────────────────────────────────────────────────────┤
│ Slide 20: 補充 02 ── 護欄運作循序流程 (基於附圖二)                     │
│ • Actor → Portal → Gateway → InGuardrail → Agent → OutGuardrail        │
│ • 處置矩陣五種判定 (Allow / Redact / Rewrite / Block / Escalate)       │
│ • 確定性規則先行，Fail-Closed 鋼鐵防線                                 │
├────────────────────────────────────────────────────────────────────────┤
│ Slide 21: 補充 03 ── 軟體料件清單 (SBOM) 與 MCP 工具治理               │
│ • 開源套件 SBOM 管控，模型權重雜湊簽名 (CycloneDX / SPDX)             │
│ • Model Context Protocol (MCP) 伺服器自建自審白名單                    │
│ • 工具參數 Schema 驗證，消除未審直連風險                               │
├────────────────────────────────────────────────────────────────────────┤
│ Slide 22: 補充 04 ── 零信任微服務邊界與 AI 自動化演練                   │
│ • 南北向 NGFW + 東西向 K8s 微分段隔離                                  │
│ • SOC 異常熔斷斷路器 (Circuit Breaker) 與緊急 Kill Switch              │
│ • 季度紅隊攻防測試指標：越獄成功率 <1%、誤攔率 <5%                    │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 3. 生成與驗證紀錄

* **執行腳本**：`append_v4_pptx.py`
* **產出檔案**：`D:\JavaDO\總結報告_v4_補充版.pptx`
* **驗證結果**：成功生成 22 頁，前 17 頁字元雜湊與樣式無縫銜接，後 5 頁版面高度協調。

---

## 💡 深度理解與架構啟示

* **軟體工程原則之「開閉原則」(OCP)**：對擴展開放，對修改封閉。本輪操作堪稱文件工程中開閉原則的典範實踐——在完全不碰觸既有穩定基線的前提下，以高內聚的外掛結構順暢達成重大架構升級。
"""

write_md("06-總結報告V4補充版架構擴充.md", n06_md)

print("Part 1 Complete!")
