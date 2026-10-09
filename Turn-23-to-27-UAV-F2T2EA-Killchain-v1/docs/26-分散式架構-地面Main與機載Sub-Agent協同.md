---
date: 2026-09-16
title: "26. 分散式邊緣架構：地面 Main Agent 與機載 Sub-Agents 協同機制"
phase: "Phase 4: 國防自主擊殺鏈 F2T2EA 與分散式邊緣協同作戰"
tags:
  - 分散式協同
  - 地面MainAgent
  - 機載SubAgent
  - 感測融合
  - 頻寬優化
  - 邊緣AI
prev: "[[25-F2T2EA資訊圖表細節調校與放大]]"
next: "[[27-F2T2EA作戰場景合理性評估與4K圖表]]"
related:
  - "[[23-無人機F2T2EA自主擊殺鏈Agent實作]]"
  - "[[24-F2T2EA自主擊殺鏈資訊圖表生成]]"
  - "[[27-F2T2EA作戰場景合理性評估與4K圖表]]"
  - "[[00-Index-AI-Agent-Framework-知識圖譜總覽]]"
---

# 26. 分散式邊緣架構：地面 Main Agent 與機載 Sub-Agents 協同機制

- **對話輪次**：第 26 輪對話 (Turn 26)
- **記錄日期**：`2026-09-16`
- **所屬演進階段**：**Phase 4: 國防自主擊殺鏈 F2T2EA 與分散式邊緣協同作戰**
- **核心關鍵字**：`分散式協同` `地面MainAgent` `機載SubAgent` `感測融合` `頻寬優化` `邊緣AI`
- **主題概述**：深度解答機載邊緣端與地面站之通訊機制：特徵向量回傳、卡爾曼濾波時空對齊及抗電子戰斷鏈韌性。

---

## 🔗 知識脈絡與雙向關聯網絡 (Context & Bilateral Links)

* **上一篇 (Previous)**：[[25-F2T2EA資訊圖表細節調校與放大]]
* **下一篇 (Next)**：[[27-F2T2EA作戰場景合理性評估與4K圖表]]
* **知識圖譜總覽 (Master Index)**：[[00-Index-AI-Agent-Framework-知識圖譜總覽]]
* **橫向技術與架構關聯 (Cross-Cutting References)**：
  - [[23-無人機F2T2EA自主擊殺鏈Agent實作|23. 無人機 F2T2EA 自主擊殺鏈實戰 Agent 實作]]：完整展示利用 LangChain DeepAgents 構建 F2T2EA 擊殺鏈：COP 融合、MCP 叫起 Lattice、MITL 中斷與 BDA 報告。
  - [[24-F2T2EA自主擊殺鏈資訊圖表生成|24. 無人機 F2T2EA 自主擊殺鏈 4K 資訊圖表設計]]：將 F2T2EA 閉環流程整合為海報級 4K 資訊圖表，視覺化六大戰術階段與人機在迴路驗證節點。
  - [[27-F2T2EA作戰場景合理性評估與4K圖表|27. F2T2EA 分散式作戰場景合理性深度論證與 4K 場景圖]]：論證 6 步分散式作戰場景技術可行性（Orin NX + Gemma 4 31B + MCP Lattice + 403 雷達阻斷 + MANET Mesh），交付 4K 場景圖。

---

## 👤 使用者指令 (User Request)

> [!NOTE] 原始提示詞紀錄
> 在 F2T2EA 範例中，Main Agent 是 run 在地面控制站，EO 及 IR Sub-agent 是 run 在無人機上，這樣行得通嗎？
> Main Agent 如何叫起 sub-agent，main agent 如何做 fusion 呢？

---

## 🤖 助理詳細研析與成果交付 (Assistant Response & Deliverables)

在真實國防與戰術自主無人機系統（如美軍 Skyborg 計畫、DARPA CODE、Anduril Lattice 等）中，**「Main Agent 在地面站 (GCS)，EO/IR Sub-agents 在無人機機載電腦 (Airborne Edge)」不僅行得通，而且是現代空地協同分散式 AI 的「最佳標準架構（Golden Standard）」**。

以下為您深入研析其**運作可行性**、**跨鏈路叫起機制**，以及**感測融合（Sensor Fusion）的核心實踐方式**：

---

### 一、 為什麼這種架構「完全行得通」，而且是唯一實戰可行的解法？

在軍事抗干擾（EW Contested）與惡劣環境下，如果將整個架構反過來（例如把未處理的 EO/IR 原始高畫質影像全串流傳回地面，或是把巨大的戰略決策 LLM 塞進機載晶片），會面臨致命瓶頸：

1. **頻寬與抗干擾瓶頸（RF Link & EW）**：
   - 4K 可見光與高幀率紅外熱像原始視訊串流動輒數十至數百 Mbps。在戰時若遭電子干擾（EW Jamming），鏈路頻寬大幅縮減，原始視訊必然卡頓斷訊，更可能暴露無人機射頻輻射特徵。
   - **解法**：EO/IR Sub-agents 在機載晶片（如 NVIDIA Jetson AGX Orin Industrial、國防抗輻射神經推論晶片）就地運算，**只傳送「結構化特徵與遙測標籤（JSON / Protobuf，每秒僅數 KB）」**，頻寬佔用下降 99.9%，在極弱信號下依然能穩定傳輸。
2. **SWaP-C（尺寸、重量、功耗與成本）限制**：
   - 戰術決策 Main Agent 需要結合龐大戰術地圖、Lattice 聯合作戰系統、戰略雷達庫存取管制、ABAC 護欄檢查及 MITL 指揮官審批，需要高算力伺服器等級硬體支援。地面控制站（GCS）具備充裕的電源與散熱條件，最適合承載 Main Agent。
3. **MITL 人在迴路的自然落點**：
   - 武器釋放授權、ROE 法規檢查必須由作戰指揮官在地面控制台實施，因此 Main Agent 與人機界面的核心樞紐本就應駐留在地面。

---

### 二、 地面 Main Agent 如何「叫起」機載 Sub-agent？

在單機環境中，Agent 調用通常是同一 Python 行程內的記憶體函式調用；但在**跨空地實體鏈路**的分散式系統中，叫起機制採用**「戰術分散式 Agent 通訊協定（Tactical Distributed Agent Protocol）」**：

```
【地面控制站 GCS】                             【無人機機載邊緣 Airborne Edge】
┌────────────────────────┐                    ┌────────────────────────────┐
│   Main Agent (Planner) │                    │  Airborne Agent Runtime    │
│  (DeepAgents / LLM)    │                    │  (Edge Container / Sandbox)│
└──────────┬─────────────┘                    └──────────────┬─────────────┘
           │ 1. 任務派發 (Dispatch Task)                     │
           ▼                                                 │
┌────────────────────────┐                    ┌──────────────▼─────────────┐
│ Ground Tactical Gateway│                    │ Airborne Tactical Gateway  │
│ (ABAC / PQC Encryption)│                    │ (Local Edge Security Proxy)│
└──────────┬─────────────┘                    └──────────────▲─────────────┘
           │ 2. 戰術無線鏈路 (Link-16 / CDL / Mesh)          │
           └──────────────────[ RF Link ]────────────────────┘
                                3. 解包並喚醒機載子代理
                                ┌──────────────┴─────────────┐
                                ▼                            ▼
                     ┌────────────────────┐       ┌────────────────────┐
                     │   EO Sub-Agent     │       │    IR Sub-Agent    │
                     │ (YOLOv10 / Tracker)│       │ (Thermal-CNN / Temp│
                     └────────────────────┘       └────────────────────┘
```

#### 具體調用步驟：

1. **任務規格化（Task Serialization）**：
   - 地面 Main Agent 判定需要進行目標搜尋時，生成標準的任務酬載（Task Envelope）：
     ```json
     {
       "mission_id": "F2T2EA-20260916-01",
       "command": "ACTIVATE_RECON_SUBACTORS",
       "search_box": {"lat_min": 24.120, "lat_max": 24.150, "lon_min": 120.650, "lon_max": 120.680},
       "priors": {"target_type": "TEL", "expected_thermal": "HIGH"},
       "comm_policy": {"report_interval_ms": 500, "confidence_threshold": 0.85}
     }
     ```
2. **安全閘道加密下傳（Tactical Data Link）**：
   - 透過戰術閘道以 **PQC（後量子加密）/ 零信任 ABAC 驗證**，經由戰術通訊協定（如 **DDS - Data Distribution Service**、**Tactical MQTT** 或 **gRPC**）下傳至無人機機載閘道。
3. **機載 Runtime 喚醒 Sub-agents**：
   - 無人機上的機載 Agent Runtime 接收指令後，在機載獨立容器沙箱中喚醒/初始化 `EO_SubAgent` 與 `IR_SubAgent`，將雲台相機（Gimbal）轉動至目標空域，開始讀取機載感測器串流。
4. **自主斷網包（DIL Fallback机制）**：
   - 若地面通訊因強烈干擾中斷（DIL: Disconnected, Intermittent, Limited），機載 Sub-agents 依任務包中的「自主作戰授權（Mission Envelope）」持續跟蹤並保存快取，待鏈路恢復後自動重傳。

---

### 三、 感測融合（Sensor Fusion）在哪裡做？如何做？

針對融合機制，工程上有兩種主流實踐路線，軍事上**以「路線 A（機載邊緣航跡融合）」為最佳實踐**，路線 B 則作為決策輔助：

```
【路線 A：機載邊緣航跡融合（最推薦，極致省頻寬）】
  EO Sensor ──> [ EO Sub-Agent ] ──┐
                                     ├──> [ 機載 Sensor Fusion ] ──> Fused Track ──(鏈路傳輸)──> [ 地面 Main Agent ]
  IR Sensor ──> [ IR Sub-Agent ] ──┘     (卡爾曼濾波 / 航跡融合)        (每秒 2KB JSON)

【路線 B：地面決策級融合（頻寬充足時採用）】
  EO Sensor ──> [ EO Sub-Agent ] ──(特徵向量下傳)──┐
                                                    ├──> [ 地面 Main Agent / Fusion Tool ] ──> COP 作戰圖像
  IR Sensor ──> [ IR Sub-Agent ] ──(熱特徵下傳)────┘     (時空對齊 / LLM 語意動態權重)
```

#### 融合演算法的 4 大核心步驟：

#### 步驟 1：時間對齊（Temporal Synchronization）
- 機載 EO 與 IR 相機幀率可能不同（例如 EO 60fps、IR 30fps）。
- 利用硬體 PTP/GPS 時戳對每一偵檢測結果打上微秒級時戳，採用**線性內插或外推預測**，使兩者觀測時間對齊至同一基準。

#### 步驟 2：空間座標轉換與配準（Spatial Registration）
- 將 EO 像素座標 $(u_1, v_1)$ 與 IR 像素座標 $(u_2, v_2)$，透過雙光鏡頭的外參標定矩陣（Homography Matrix）以及無人機 INS/GPS 姿態角（Roll/Pitch/Yaw），統一轉換至 **NED 地理座標系（北-東-地）或 WGS-84 經緯度**。

#### 步驟 3：狀態估計與卡爾曼濾波（EKF / JPDAF 融合）
- **數值融合**：
  $$\mathbf{x}_{k} = \mathbf{F} \mathbf{x}_{k-1} + \mathbf{w}_k$$
  利用**擴展卡爾曼濾波（EKF）**或**聯合概率數據互聯（JPDAF）**，將 EO 提供的高精度幾何輪廓與邊緣資訊，與 IR 提供的熱質心（Thermal Centroid）進行共變異矩陣融合，算出運動速度向量與高精度目標位置。
- **置信度融合（Dempster-Shafer 證據理論）**：
  若 EO 置信度為 $m_{EO}(\text{TEL}) = 0.88$，IR 測得發動機異常高溫 $m_{IR}(\text{TEL}) = 0.93$，結合兩者獨立證據計算聯合質量函數：
  $$m_{fused}(\text{TEL}) = \frac{m_{EO} \cdot m_{IR}}{1 - \text{衝突係數}} \approx 0.972\ (97.2\%)$$

#### 步驟 4：Main Agent 的語義決策動態調權（LLM Semantic Weighting）
地面 Main Agent 最強大的地方在於**結合環境脈絡與情報知識庫**：
- **晴天白晝**：Main Agent 動態調整融合權重：$\alpha_{\text{EO}} = 0.7, \beta_{\text{IR}} = 0.3$。
- **起霧、夜間或遭煙幕彈干擾**：EO 置信度驟降，Main Agent 接收環境警報，即時將權重動態切換為：$\alpha_{\text{EO}} = 0.1, \beta_{\text{IR}} = 0.9$。
- **最終輸出**：生成符合 NATO 標準的 **COP 作戰圖像物件**，呈現在指揮官控制螢幕上供 MITL 審批。

---

### 四、 程式碼實現架構範例（Python / DeepAgents）

在程式碼層面，Main Agent 透過分散式傳輸調用工具，機載 Sub-agent 執行邊緣融合後回傳：

```python
# ==============================================================================
# 地面 Main Agent: 透過戰術數據鏈工具 (Tactical Comm Tool) 派發任務
# ==============================================================================
class GroundMainAgent:
    def __init__(self, datalink_client, guardrail_engine):
        self.datalink = datalink_client
        self.guardrail = guardrail_engine

    def execute_recon_phase(self, target_aoi):
        # 1. 護欄與權限檢核
        self.guardrail.verify_permission(action="AIRBORNE_TASK_DISPATCH", clearance="SECRET")
        
        # 2. 跨空地網絡發送派發命令 (DDS / Protobuf)
        payload = {
            "task": "ACTIVATE_DUAL_SENSOR_FUSION",
            "aoi": target_aoi,
            "fusion_mode": "EDGE_TRACK_TO_TRACK"
        }
        print("[地面 Main Agent] 透過 Link-16/DDS 叫起機載 EO & IR Sub-agents...")
        
        # 3. 非同步等待機載回傳之結構化融合航跡 (非原始影像)
        fused_track = self.datalink.send_and_wait_telemetry(payload, timeout_sec=5.0)
        
        # 4. Main Agent 接收融合結果並建立 COP 通用作戰圖像
        print(f"[地面 Main Agent] 收到機載融合 COP: 目標={fused_track['type']}, 置信度={fused_track['confidence']:.1%}")
        return fused_track

# ==============================================================================
# 機載邊緣端 (UAV Edge): EO & IR Sub-agents + 機載本地融合器
# ==============================================================================
class AirborneEdgeRuntime:
    def __init__(self):
        self.eo_agent = AirborneEOSubAgent()
        self.ir_agent = AirborneIRSubAgent()

    def on_task_received(self, command):
        # 本地呼叫機載 EO 與 IR 感測子代理
        eo_det = self.eo_agent.detect_frame()  # 本地 YOLO 推論
        ir_det = self.ir_agent.detect_frame()  # 本地 熱成像 推論
        
        # 本地執行卡爾曼濾波與時空對齊融合 (無需回傳大頻寬影像)
        fused_cop = self.local_fuse(eo_det, ir_det)
        return fused_cop  # 僅將 2KB 結構化遙測下傳地面

    def local_fuse(self, eo, ir):
        # 時空投影與 Dempster-Shafer 置信度疊加
        combined_conf = 1.0 - (1.0 - eo["conf"]) * (1.0 - ir["conf"])
        return {
            "track_id": "T-092",
            "type": "TEL_MISSILE_LAUNCHER",
            "coords": {"lat": 24.133, "lon": 120.672, "alt": 180},
            "confidence": min(0.99, combined_conf)
        }
```

---

### 五、 總結

| 核心問題 | 結論與解決機制 |
| :--- | :--- |
| **行得通嗎？** | **完全行得通，且為現代分散式戰術 C4ISR 的核心設計**。地面負責戰略推理、安全護欄與指揮審批；機載負責邊緣高速推論與特徵萃取。 |
| **如何叫起？** | 透過**戰術資料鏈（Link-16 / CDL / Tactical Mesh）**結合 **DDS / Protobuf / gRPC** 封裝任務包，機載 Agent Runtime 接獲指令後在隔離容器內啟動實體感測 Sub-agents。 |
| **如何 Fusion？** | 採**機載邊緣航跡融合（Airborne Track Fusion）**：機載雙光子代理先做時序同步、空間配準與 EKF 數值融合，僅將數 KB 的結構化 COP 航跡傳回地面；地面 Main Agent 則基於天候與戰場情資進行動態語意加權。 |
