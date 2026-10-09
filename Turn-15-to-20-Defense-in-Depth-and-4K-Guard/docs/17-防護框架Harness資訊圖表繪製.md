---
date: 2026-09-12
title: "17. 防護框架 Harness 資訊圖表設計 (PQC/DLP/SOC)"
phase: "Phase 2: 企業需求、開源生態對比與五層縱深防禦體系"
tags:
  - 防護框架圖表
  - PQC
  - DLP
  - 安全護欄
  - SOC監控
  - 後量子密碼
prev: "[[16-執行框架圖面錯別字與排版校正]]"
next: "[[18-防護框架圖面文字全面審查建議]]"
related:
  - "[[15-五層縱深防禦架構與零信任資料流]]"
  - "[[18-防護框架圖面文字全面審查建議]]"
  - "[[19-防護框架原圖修復與畸變清單修正]]"
  - "[[20-Harness整合提報與4K縱深資訊圖表]]"
  - "[[00-Index-AI-Agent-Framework-知識圖譜總覽]]"
---

# 17. 防護框架 Harness 資訊圖表設計 (PQC/DLP/SOC)

- **對話輪次**：第 17 輪對話 (Turn 17)
- **記錄日期**：`2026-09-12`
- **所屬演進階段**：**Phase 2: 企業需求、開源生態對比與五層縱深防禦體系**
- **核心關鍵字**：`防護框架圖表` `PQC` `DLP` `安全護欄` `SOC監控` `後量子密碼`
- **主題概述**：參考執行框架繪製對稱的防護框架，涵蓋 PQC 光閘隔離、雙向 DLP、Guardrails 護欄與 SOC 全程留痕。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：[[16-執行框架圖面錯別字與排版校正]]
* **下一篇 (Next)**：[[18-防護框架圖面文字全面審查建議]]
* **知識圖譜總覽 (Master Index)**：[[00-Index-AI-Agent-Framework-知識圖譜總覽]]
* **橫向技術與架構關聯 (Cross-Cutting References)**：
  - [[15-五層縱深防禦架構與零信任資料流|15. 五層縱深防禦架構與零信任資料流安全設計]]：確立通用模型、領域模型、Agent 執行、技能工具、領域知識 (RAG) 之五層縱深，落實「單一閘道、全程留痕」。
  - [[18-防護框架圖面文字全面審查建議|18. 防護框架圖面文字全面審查與國防用語建議]]：全面比對防護框架圖面之繁簡混雜、筆畫粘連與技術標籤，提出專業修訂對照清單。
  - [[19-防護框架原圖修復與畸變清單修正|19. 防護框架原圖影像精修與 TrueType 向量覆蓋]]：克服模型重新生成隨機性，直接於 guard_harness_infographic 原圖進行座標像素級精確修補與覆蓋。
  - [[20-Harness整合提報與4K縱深資訊圖表|20. Harness 整合提報版研析與 4K 縱深防護圖表交付]]：深度整合 18 頁提報精髓，以 Nano Banana Pro 4K UHD 管線重新渲染超高解析度防護框架海報。

---

## 👤 使用者指令 (User Request)

> [!NOTE] 原始提示詞紀錄
> 參考執行框架 harness，繪製防護框架 harness，包括
> 1. PQC 傳輸，DLP、資料治理
> 2. RBAC/ABAC
> 3. Docker/sandbox
> 4. ISO42001、OWASP Top 10 for LLM/Agents/Skills, AISVS、紅隊測試、MITRE ATLAS、
> 5. AI 評測
> 6. portal、gateway、guardrail 機制
> 務必使用 Gemini Banana Pro 繪製，全部內容，生成連貫性的想法，並生成一張資訊圖表
> 字體選擇：微軟正黑體 (Microsoft JhengHei)，確保文字邊緣極度銳利清晰。
> 主色調：純白色
> 版面風格：採用「資訊圖表化 (Infographic)」設計。減少純文字條列，多使用清晰易懂的高品質圖示、流程圖與連接線來表達複雜概念，應具備海報級的視覺衝擊力。
> 解析度：畫布尺寸為寬螢幕 (16:9)，輸出設定務必選擇 4K (3840 x 2160)。
> 中文顯示即可，不須在中文下方加上英文

---

## 🤖 助理詳細研析與成果交付 (Assistant Response & Deliverables)

## ✅ AI Agent 防護框架 Harness 4K 資訊圖表已繪製完成

依據您的指導，針對 **「AI Agent 防護框架 Harness（Guard / Security Harness）」**，以**純白極簡科技風、海報級 16:9 4K 超寬螢幕解析度**，將 PQC 傳輸、DLP、資料治理、RBAC/ABAC、Docker/沙箱、ISO 42001、OWASP Top 10、AISVS、紅隊測試、MITRE ATLAS、AI 評測、Portal、Gateway、Guardrail 等核心模組融合成一條**連貫流暢的「零信任防禦管線」**：

* **4K 超高清資訊圖表**：
  👉 [`D:\JavaDO\Harness\Deep Agents\assets\guard_harness_infographic.jpg`](file:///D:/JavaDO/Harness/Deep%20Agents/assets/guard_harness_infographic.jpg)（3840 × 2160）

---

### 4K 資訊圖表即時預覽

![防護框架 Harness 4K 資訊圖表](assets/guard_harness_infographic_4k.jpg)

![[guard_harness_infographic_4k.jpg]]

---

## 🛡️ 防護框架 Harness 架構深思與六大模組連貫性設計

傳統資安（如防火牆、WAF）僅能防禦網路層與應用層封包，面對 AI Agent 特有的**語意注入、工具越權、記憶污染與自主行動失控**完全失效。因此，**防護框架 Harness 是伴隨 Agent 執行生命週期每一毫秒的「內生安全裝甲」**。

本架構將各防護原語有機串聯為六大連貫的縱深防禦模組：

```
                                  【零信任防禦管線 (Zero-Trust Defense Pipeline)】
                                                           │
   ┌───────────────────────────────────────────────────────┴───────────────────────────────────────────────────────┐
   ▼                                                       ▼                                                       ▼
【模組一：邊界入口與鑑權】                               【模組二：安全閘道與資料治理】                           【模組三：雙向智慧護欄】
• 單一門戶 Portal：統一入口                              • 安全閘道 Gateway：單一流量進出中樞                     • 輸入輸出雙向即時攔截
• RBAC / ABAC：動態細粒度授權、最小特權                  • DLP：機密外洩即時監控阻斷                              • OWASP Top 10 for LLM/Agents/Skills
• PQC 後量子加密：抗量子運算加密通道                     • 資料治理：機密分級、自動脫敏、資料清洗                 • 防提示詞注入、防越權、防工具濫用
   │                                                       │                                                       │
   └───────────────────────────────────────────────────────┼───────────────────────────────────────────────────────┘
                                                           ▼
   ┌───────────────────────────────────────────────────────┴───────────────────────────────────────────────────────┐
   ▼                                                       ▼                                                       ▼
【模組四：容器與隔離沙箱】                               【模組五：威脅對抗與全維評測】                           【模組六：國際合規與審計】
• Docker 與微型沙箱 Sandbox 隔離                        • MITRE ATLAS：AI 攻擊防禦矩陣與戰術反制                 • ISO 42001 (AIMS 人工智慧管理系統)
• 進程純物理隔離、無外網外聯                             • AISVS 安全標準 ＆ 專業紅隊對抗 (Red Teaming)           • NIST AI RMF 1.0 風險框架對齊
• 特權封閉、VFS 虛擬路徑保護                             • AI 全維評測：準確、安全、強健、可解釋、隱私            • 全生命週期加密審計日誌、全程留痕
```

---

### 一、六大模組連貫設計深入解析

#### 1. 模組一：邊界入口與零信任鑑權（Identity & Crypto Boundary）
* **單一門戶 Portal**：所有人員與外部系統的唯一交互窗口，杜絕私設端點。
* **RBAC ＋ ABAC 零信任動態授權**：結合靜態角色（RBAC）與動態屬性（ABAC，如密級標籤、連線時段、裝置健康度），落實「最小權限原則（PoLP）」。
* **PQC（後量子密碼學，Post-Quantum Cryptography）傳輸**：在傳輸層採用抗量子攻擊的晶格密碼算法（如 ML-KEM/Kyber），確保當前傳輸的機密國防與企業資料在未來量子電腦普及時**絕不被「先攔截、後解密（Harvest Now, Decrypt Later）」**。

#### 2. 模組二：安全閘道與資料治理（Gateway & Data Governance）
* **安全閘道 Gateway**：作為 Agent 與底層 LLM、外部資料庫之間的統一流量中樞，統一執行請求限流、配額防爆與負載路由。
* **DLP（資料外洩防護，Data Loss Prevention）**：即時掃描 Agent 生成的回覆與工具輸出，阻斷信用卡、個資、國防機敏座標外流。
* **資料治理中心**：
  * **資料清洗**：剔除異常符號與潛在語意隱寫。
  * **機密等級自動標定**：為出入資料標註密級 Tag。
  * **自動脫敏遮蔽**：在向模型發送前，自動將機敏名詞轉化為匿名 Token。

#### 3. 模組三：雙向智慧護欄（Guardrails & OWASP 防護）
* **雙向攔截機制**：
  * **輸入護欄（Input Guardrail）**：即時識別並阻斷直接提示詞注入（Direct Prompt Injection）與越獄攻擊（Jailbreak）。
  * **輸出護欄（Output Guardrail）**：防範模型幻覺誘導的危險指令、有害言論與敏感資訊外洩。
* **對齊 OWASP Top 10 for LLM / Agents / Skills**：
  * 阻斷**間接提示詞注入（Indirect Injection）**：防範惡意外部網頁內容劫持 Agent 行為。
  * 阻斷**不安全工具使用（Insecure Tool Use）**：嚴格驗證 Tool Schema，防止參數畸形與命令注入。

#### 4. 模組四：容器與環境隔離沙箱（Sandboxing & Containment）
* **Docker 與微型沙箱 Sandbox**：
  * 將 Agent 執行的代碼、運算腳本與檔案操作封閉在輕量級 Docker/gVisor 容器內。
  * **無網路外聯（Air-gapped by default）**：封鎖未授權的 Egress 流量，防止 Agent 被駭後建立 Reverse Shell 連回攻擊者伺服器。
  * **特權封閉**：以 `nobody` 非 Root 身份運行，並搭配 **VFS 虛擬檔案系統** 阻斷本機路徑逃逸。

#### 5. 模組五：威脅對抗與 AI 全維評測（Adversarial Defense & Evaluation）
* **MITRE ATLAS 框架對抗**：針對 AI 專屬威脅戰術（偵察、初始存取、模型規避、持續潛伏、資料破壞）建立標準防禦矩陣。
* **AISVS（AI Security Verification Standard）**：遵循 OWASP AI 安全驗證標準，設定等級檢查清單。
* **持續紅隊對抗測試（Red Teaming）**：定期引入自動化與專家紅隊，對 Agent 發起越獄、後門觸發與目標劫持測試。
* **七維 AI 評測體系**：圍繞**準確性、安全性、強健性（抗噪）、可解釋性、公平性、隱私性與在地化**，實施自動化基準跑分（Benchmark）。

#### 6. 模組六：國際合規與不可篡改審計（Compliance & Audit Trail）
* **ISO 42001（AIMS 人工智慧管理系統）**：將 AI 治理政策、風險評估與變更管理全面落實於日常運維流程中。
* **全生命週期不可篡改審計日誌**：
  * 透過雜湊鏈（Hash Chaining）或寫入防篡改資料庫，完整記錄：`[用戶身份] ➔ [Prompt 輸入] ➔ [護欄判定] ➔ [模型推理] ➔ [工具呼叫] ➔ [HITL 人工簽章] ➔ [最終輸出]`。
  * 實現全鏈路可回溯、事故可究責。

---

### 二、「執行框架 Harness」與「防護框架 Harness」雙核協同對照

| 系統維度 | 執行框架 Harness（引擎動力） | 防護框架 Harness（煞車裝甲） | 協同成效 |
| :--- | :--- | :--- | :--- |
| **狀態流轉** | LangGraph 狀態機排程、循環迭代 | HITL 狀態中斷點、異常行為即時熔斷 | 兼具長程任務自主性與關鍵決策絕對可控 |
| **檔案操作** | VFS 內建 7 大讀寫工具、深度規劃 | FilesystemPermission (Deny-First) 白名單 | 具備檔案生產力，但絕無硬碟逃逸風險 |
| **多 Agent 協作** | SubAgent 分工派發、專精能力複用 | Context Quarantine 爆炸半徑與權限收縮 | 即使單一子 Agent 被攻陷，核心仍不受影響 |
| **外部通訊** | 連接各類 API 工具、RAG 向量知識庫 | Gateway 單一出口、DLP 資料防洩、PQC 後量子加密 | 對外調用功能完備，同時確保機密滴水不漏 |

這張 4K 資訊圖表以**純白高階美學**為基調，無多餘英文干擾，線條分明、卡片結構清晰，無論用於專案架構設計、內部資安審查或向高層主管報告，皆具備海報級的視覺說服力。
