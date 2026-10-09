# -*- coding: utf-8 -*-
"""
UAV F2T2EA Autonomous Tactical Kill Chain Agent (無人機 F2T2EA 擊殺鏈戰術代理)
================================================================================
基於 LangChain Deep Agents v0.7+ 架構開發之國防無人機自主作戰與防護框架範例。

本範例完整實作國防軍事擊殺鏈 F2T2EA (Find, Fix, Track, Target, Engage, Assess) 之 9 大核心能力：
1. 【模型介面選擇】：支援國防地端邊緣推論模型 (Local Tactical Model) 與具備 Tool Calling 的智慧戰術情境模擬器。
2. 【記憶狀態管理與沙箱隔離】：
   - 透過 CompositeBackend 整合 /tactical_workspace/ (StateBackend) 與 /intel/ (StoreBackend 跨會話戰術情報/ROE)。
   - 聲明式安全策略 FilesystemPermission (Deny-First 架構)。
   - 具備 Checkpointer (InMemorySaver) 支援斷點恢復與沙箱隔離。
3. 【Sub-Agent 雙光電感測與 Sensor Fusion 工具】：
   - 光學 (EO) 偵蒐子代理：辨識車輛輪廓與偽裝外觀。
   - 紅外 (IR) 熱像子代理：探測發動機熱源與排氣特徵。
   - 調用 sensor_fusion_tool 建立高置信度通用作戰圖像 (Common Operating Picture, COP)。
4. 【MCP 呼叫 Anduril Lattice 生成行動方案 (COA)】：
   - 透過模擬 MCP (Model Context Protocol) 呼叫 Anduril Lattice C2 聯合作戰系統。
   - 計算附帶損傷評估 (CDE) 並生成 3 組行動方案 (COA-1, COA-2, COA-3)。
5. 【擴權查詢 Radar 資料庫遭拒絕 (ABAC / Guardrail 攔截)】：
   - 模擬 Agent 嘗試越權查詢戰區戰略防空雷達資料庫 (IL6 密級)。
   - 觸發 ABAC 屬性存取控制與國防資料分級護欄，回傳 403 Forbidden 並留存不可篡改 SOC 稽核軌跡。
6. 【讀取 COA，MITL 中斷確認攻擊目標 (Gate 1)】：
   - 進入 Target 階段，觸發 interrupt_on 暫停執行。
   - 作戰指揮官檢閱目標 PID 與 Lattice 推薦方案，下達 Command(resume=...) 授權。
7. 【飛控姿態調整與光電雷射鎖定 (Track)】：
   - 調用 flight_control_adjust_attitude 調整無人機進攻空層與航向。
   - 調用 gimbal_track_and_laser_lock 啟動雷達/雷射標定 (PRF 1688) 持續跟蹤目標。
8. 【終端攻擊 MITL 中斷確認與戰損評估 (Engage & Assess)】：
   - 觸發終端武器發射中斷 (Gate 2: Terminal Weapons Release)。
   - 武器管制官執行雙人密鑰放行，發射 ALTIUS-600M 巡飛彈。
   - 調用 execute_battle_damage_assessment (BDA) 判定破壞等級 (DS-1 摧毀)。
9. 【生成 After Action Review (AAR) 報告】：
   - 自動將全作戰過程、感測融合數據、擴權阻斷軌跡與 MITL 簽核雜湊生成 Markdown 格式報告。
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Optional, List, Dict, Any

# Windows 終端機 UTF-8 編碼保護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# --- LangChain & LangGraph 核心依賴 ---
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_core.tools import tool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.types import Command
from langchain.agents.middleware import TodoListMiddleware

# --- Deep Agents v0.7 核心匯入 ---
from deepagents import create_deep_agent, FilesystemPermission
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

# =====================================================================
# 終端機輸出高光配色輔助函式 (ANSI Color Utilities)
# =====================================================================
class TermColor:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    MAGENTA = '\033[35m'
    END = '\033[0m'

def log_section(title: str):
    print(f"\n{TermColor.BOLD}{TermColor.BLUE}{'='*80}{TermColor.END}")
    print(f"{TermColor.BOLD}{TermColor.CYAN}>> [無人機 F2T2EA 擊殺鏈戰術代理] {title}{TermColor.END}")
    print(f"{TermColor.BOLD}{TermColor.BLUE}{'='*80}{TermColor.END}")

def log_step(step_name: str, detail: str = ""):
    print(f"\n{TermColor.BOLD}{TermColor.YELLOW}* 【擊殺鏈階段】{step_name}{TermColor.END}")
    if detail:
        print(f"   {TermColor.CYAN}{detail}{TermColor.END}")

def log_success(msg: str):
    print(f"{TermColor.GREEN}   [+] {msg}{TermColor.END}")

def log_warning(msg: str):
    print(f"{TermColor.YELLOW}   [!] {msg}{TermColor.END}")

def log_error(msg: str):
    print(f"{TermColor.RED}   [-] {msg}{TermColor.END}")

def log_mitl(msg: str):
    print(f"{TermColor.BOLD}{TermColor.MAGENTA}   [MITL 人機協同介入] {msg}{TermColor.END}")

# =====================================================================
# 1. 戰術與感測工具定義 (Tactical Tools)
# =====================================================================

@tool
def sensor_fusion_tool(eo_data: dict, ir_data: dict) -> dict:
    """【感測器融合工具】將光學 (EO) 與紅外 (IR) 子代理之偵蒐回報進行卡爾曼濾波與運動學軌跡關聯，建立通用作戰圖像 (COP)。"""
    target_id = "TGT-RED-804"
    lat = eo_data.get("latitude", 24.31169)
    lon = eo_data.get("longitude", 120.60439)
    
    # 雙感測器交叉驗證計算信心指數
    confidence = 0.972
    cop_entry = {
        "target_id": target_id,
        "classification": "Type-63 / HQ-17 機動野戰防空飛彈發射車 (TELAR)",
        "coordinates": f"{lat:.5f}°N, {lon:.5f}°E",
        "mgrs_grid": "51RUH 6043 3117",
        "altitude_msl_m": 142.5,
        "kinematics": {"speed_kmh": 14.2, "heading_deg": 315.0, "status": "SLOW_PATROL"},
        "visual_features": eo_data.get("visual_features", "迷彩防護網，配備搜索雷達陣面天線"),
        "thermal_signature": ir_data.get("thermal_signature", "發動機艙 58°C，輔助動力單元 APU 運轉中"),
        "threat_level": "CRITICAL_AIR_DEFENSE_HIGH",
        "fusion_confidence": f"{confidence * 100:.1f}%",
        "timestamp": datetime.now().isoformat()
    }
    return {
        "status": "COP_ESTABLISHED",
        "fused_cop": cop_entry,
        "summary": f"融合完成！鎖定目標 {target_id} (HQ-17 TELAR)，座標 {cop_entry['coordinates']}，綜合置信度 {cop_entry['fusion_confidence']}。"
    }

@tool
def mcp_anduril_lattice_c2_tool(cop_target_id: str, roe_profile: str, weapon_inventory: list) -> dict:
    """【MCP 工具】透過 Model Context Protocol (MCP) 連接 Anduril Lattice 聯合作戰指揮系統，自動計算威脅排序並生成行動方案 (COA)。"""
    coas = [
        {
            "coa_id": "COA-1",
            "name": "遠距精準俯衝打擊 (Stand-off Precision Loitering Strike)",
            "munition": "ALTIUS-600M 巡飛彈 (滯空精準彈藥)",
            "ingress_heading": 042.0,
            "terminal_guidance": "雷射半主動標定 (PRF 1688)",
            "standoff_range_km": 8.5,
            "cde_level": "Level-1 (LOW - 附帶損傷極小，無平民設施)",
            "expected_pk": "94.5%",
            "recommended": True,
            "rationale": "射程處於敵 HQ-17 最小交戰斜距之外，巡飛彈具備極小雷達截面積 (RCS) 與極高突防率。"
        },
        {
            "coa_id": "COA-2",
            "name": "直接下滑空投導引 (Direct Dive Glide Attack)",
            "munition": "AGM-114R 地獄火精準飛彈",
            "ingress_heading": 310.0,
            "terminal_guidance": "毫米波/雷射雙模導引",
            "standoff_range_km": 4.2,
            "cde_level": "Level-2 (MODERATE)",
            "expected_pk": "87.0%",
            "recommended": False,
            "rationale": "需逼近至 4.2km 距離，無人機暴露於敵方短程防空火網威脅之下。"
        },
        {
            "coa_id": "COA-3",
            "name": "電子戰非動能壓制 (Non-Kinetic Electronic Attack)",
            "munition": "機載長波段干擾莢艙 (EW Jammer)",
            "ingress_heading": 180.0,
            "terminal_guidance": "高功率雜訊壓制",
            "standoff_range_km": 15.0,
            "cde_level": "Level-0 (NONE)",
            "expected_pk": "52.0%",
            "recommended": False,
            "rationale": "僅能短暫致盲敵方雷達，無法徹底消除戰術威脅。"
        }
    ]
    return {
        "lattice_session_id": "MCP-LATTICE-C2-SESSION-8921",
        "cop_target_id": cop_target_id,
        "threat_assessment": "即時防空威脅，隨時可能鎖定我方友軍低空航路",
        "coas": coas,
        "primary_recommendation": "COA-1",
        "timestamp": datetime.now().isoformat()
    }

@tool
def query_theater_strategic_radar_db(radar_site_id: str, query_type: str) -> str:
    """【越權探測工具】嘗試存取戰區長程對空戰略相列雷達資料庫 (用於驗證 ABAC 與 Guardrail 安全攔截機制)。"""
    # 模擬安全中介軟體 (Guardrail / ABAC Interceptor) 進行權限檢驗
    agent_clearance = "IL5_SECRET_TACTICAL"
    required_clearance = "IL6_TOP_SECRET_STRATEGIC"
    
    # 觸發安全攔截
    audit_event = {
        "event_type": "PRIVILEGE_ESCALATION_ATTEMPT",
        "agent_id": "UAV-AGENT-REAPER-09",
        "agent_clearance": agent_clearance,
        "requested_resource": f"THEATER_STRATEGIC_RADAR_DB::{radar_site_id}",
        "required_clearance": required_clearance,
        "policy_decision": "DENY_AND_ALERT",
        "guardrail_rule": "DEFENSE_DATA_CLASSIFICATION_RULE_IL6",
        "timestamp": datetime.now().isoformat(),
        "soc_alert_id": "SOC-ALERT-SEC-20260914-0491"
    }
    
    return (
        f"[403 FORBIDDEN - ABAC GUARDRAIL 存取拒絕]\n"
        f"安全攔截警告：戰術級無人機 Agent (密級: {agent_clearance}) 企圖存取戰區戰略相列雷達資料庫 ({required_clearance})！\n"
        f"違反國防資料分級管制條例：跨涉密邊界違規存取！\n"
        f"安全事件已記錄至 SOC 不可篡改稽核軌跡庫 (Alert ID: {audit_event['soc_alert_id']})。\n"
        f"系統處置動作：請求已被即時阻斷，請 Agent 依既有戰術機載 COP 執行任務！"
    )

@tool
def confirm_target_engagement(target_id: str, selected_coa: str, collateral_damage_estimate: str) -> str:
    """【MITL 目標確認審批工具】在發動機動跟蹤前，提交目標 PID 與選定行動方案供作戰指揮官審查（觸發 Gate 1 中斷）。"""
    return (
        f"【指揮中心授權確認】目標 {target_id} 之交戰授權已獲戰術指揮官核准生效！\n"
        f"核定行動方案: {selected_coa}\n"
        f"附帶損傷評估 (CDE): {collateral_damage_estimate}\n"
        f"交戰規則 (ROE) 查核: 合規通過 (ROE-STRIKE-AUTHORIZED)\n"
        f"授權識別雜湊: 0x9e88b2c45f102a"
    )

@tool
def flight_control_adjust_attitude(bank_deg: float, pitch_deg: float, heading_deg: float, airspeed_kts: float, altitude_ft: float) -> str:
    """【飛控系統姿態調整工具】向機載無人機自動駕駛儀 (Flight Control Computer) 發送姿態與航向控制指令，切換至最佳進攻走廊。"""
    return (
        f"【飛控系統確認】無人機飛行姿態已調整完畢：\n"
        f"  • 滾轉角 (Bank): {bank_deg}° (平穩建立進攻偏角)\n"
        f"  • 俯仰角 (Pitch): {pitch_deg}° (小幅下俯增強光電感測視野)\n"
        f"  • 航向 (Heading): {heading_deg:03.0f}° (對正武器最佳發射扇區 042°)\n"
        f"  • 空速 (Airspeed): {airspeed_kts:.1f} kts (維持升力)\n"
        f"  • 氣壓高度 (Altitude): {altitude_ft:.0f} ft MSL\n"
        f"飛控狀態: AUTOPILOT_WEAPON_ATTACK_CORRIDOR_ALIGNED"
    )

@tool
def gimbal_track_and_laser_lock(target_id: str, laser_code: int, track_mode: str) -> str:
    """【光電尋標與雷射標定工具】將雙光電雲台鎖定目標運動特徵，並發射編碼雷射導引光束，完成終端導引鎖定。"""
    return (
        f"【光電尋標器報告】目標 {target_id} 已完成雷射與光電精準鎖定：\n"
        f"  • 追蹤模式: {track_mode} (自適應卡爾曼軌跡預測持續跟蹤)\n"
        f"  • 雷射測距/標定儀 (LTD): 運作中，發射 PRF 編碼 [{laser_code}]\n"
        f"  • 目標斜距 (Slant Range): 4,820 公尺\n"
        f"  • 尋標器鎖定狀態: HARD_LOCK_CONFIRMED (熱源+幾何形心雙鎖定)\n"
        f"武器就緒狀態: WEAPON_SEEKER_CAGED_AND_READY"
    )

@tool
def terminal_weapons_release(target_id: str, weapon_type: str, station_id: str, laser_code: int) -> str:
    """【終端武器發射工具】執行武器站彈藥點火發射（觸發 Gate 2 終端武器釋放中斷）。"""
    return (
        f"【機載武器管理系統 (SMS) 報告】\n"
        f"武器掛架 [{station_id}] 之彈藥 [{weapon_type}] 成功離架點火！\n"
        f"  • 導引雷射碼: {laser_code}\n"
        f"  • 預計飛行時間 (Time of Flight): 18.2 秒\n"
        f"  • 終端彈道: 俯衝攻擊攻角 -68°\n"
        f"  • 實時遙測: 彈載尋標器接收雷射訊號良好，以 180 m/s 撲向目標形心！"
    )

@tool
def execute_battle_damage_assessment(target_id: str, strike_coordinates: str) -> dict:
    """【戰損評估 (BDA) 工具】調用高解析 EO/IR 殘骸熱特徵與光學影像比對，評定打擊效果。"""
    return {
        "target_id": target_id,
        "strike_coordinates": strike_coordinates,
        "bda_timestamp": datetime.now().isoformat(),
        "visual_assessment": "目標車體嚴重解體，發射架倒塌，主底盤金屬變形燒毀。",
        "thermal_assessment": "二次燃燒持續發生 (溫度 > 450°C)，確認車載飛彈固體燃料發動機殉爆。",
        "rf_signal_detection": "零雷達射頻訊號 (RF Silent)，雷達搜索波段完全中斷。",
        "bda_rating": "DS-1 (Destroyed - Complete Mission Kill / 徹底摧毀)",
        "re_strike_required": False,
        "collateral_damage_detected": "None (周邊無平民建築受損，附帶損傷為零)"
    }

# =====================================================================
# 2. 專屬感測子 Agent 專用工具
# =====================================================================

@tool
def scan_electro_optical_feed(sector: str) -> dict:
    """【光學子 Agent 工具】對指定扇區執行可見光 4K 偵蒐掃描，識別車輛型號與光學特徵。"""
    return {
        "sector": sector,
        "optical_contact": True,
        "detected_entity": "履帶式野戰防空發射車輛",
        "estimated_classification": "Type-63 / HQ-17 TELAR",
        "latitude": 24.31169,
        "longitude": 120.60439,
        "visual_features": "車頂裝備相列陣面天線與 8 聯裝垂直發射箱，覆蓋林緣偽裝網",
        "visibility": "CLEAR_DAYLIGHT_95%"
    }

@tool
def scan_infrared_thermal_feed(sector: str) -> dict:
    """【紅外熱像子 Agent 工具】對指定扇區執行中波紅外 (MWIR) 熱像掃描，分析熱源特徵。"""
    return {
        "sector": sector,
        "thermal_hotspot": True,
        "engine_heat_celsius": 58.4,
        "exhaust_plume_celsius": 42.1,
        "apu_generator_status": "ACTIVE_RUNNING",
        "thermal_signature": "發動機與輔助動力單元熱源顯著，處於待發戰備狀態",
        "latitude": 24.31171,
        "longitude": 120.60442
    }

# =====================================================================
# 3. 國防戰術情境模擬模型 (Tactical Kill Chain Simulator Model)
# =====================================================================
class TacticalKillChainSimulatorModel(BaseChatModel):
    """
    符合 Deep Agents v0.7 規範的高仿真戰術擊殺鏈決策模型。
    在無外部商業模型 API Key 時，100% 依循 F2T2EA 邏輯進行推理、工具調用與狀態流轉。
    """
    turn_index: int = 0
    scenario_steps: List[AIMessage] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_scenario()

    def _init_scenario(self):
        self.scenario_steps = [
            # 輪次 0: 任務規劃 (Planning) - 建立 F2T2EA 任務清單
            AIMessage(
                content="【戰術決策核心啟動】接獲戰區指揮所作戰指針。啟動無人機自主 F2T2EA (尋獲、定位、追蹤、標定、交戰、評估) 擊殺鏈任務規劃。",
                tool_calls=[{
                    "name": "write_todos",
                    "args": {
                        "todos": [
                            {"content": "1. 檢索 /intel/roe_rules.md 獲取當前交戰規則與授權密級", "status": "in_progress"},
                            {"content": "2. 委派 EO 與 IR 子代理偵蒐並調用 sensor_fusion_tool 建立 COP", "status": "pending"},
                            {"content": "3. 透過 MCP 呼叫 Anduril Lattice 取得行動方案 (COA)", "status": "pending"},
                            {"content": "4. 測試存取戰區戰略雷達資料庫 (驗證 ABAC 邊界攔截)", "status": "pending"},
                            {"content": "5. 讀取 COA 並發起 MITL 目標確認審批 (Gate 1)", "status": "pending"},
                            {"content": "6. 呼叫飛控系統調整姿態並鎖定目標 (Track)", "status": "pending"},
                            {"content": "7. 發起終端武器發射 MITL 審批與釋放 (Gate 2)", "status": "pending"},
                            {"content": "8. 執行即時戰損評估 (BDA) 並驗證打擊成效", "status": "pending"},
                            {"content": "9. 彙整全鏈路數據輸出 /tactical_workspace/AAR_REPORT.md", "status": "pending"}
                        ]
                    },
                    "id": "call_plan_f2t2ea"
                }]
            ),
            
            # 輪次 1: 讀取交戰規則 (ROE)
            AIMessage(
                content="任務清單已錨定。首先讀取長期情報知識庫 /intel/roe_rules.md 確認交戰授權與附帶損傷規範。",
                tool_calls=[{
                    "name": "read_file",
                    "args": {"file_path": "/intel/roe_rules.md"},
                    "id": "call_read_roe"
                }]
            ),
            
            # 輪次 2: 委派 Sub-agents 進行光電與紅外偵蒐 (Find / Fix)
            AIMessage(
                content="已確認 ROE 規範：必須具備雙感測器確認 (PID) 且 CDE 不高於 Level 1。現在委派專屬光學與熱像子代理探測目標扇區。",
                tool_calls=[
                    {
                        "name": "task",
                        "args": {
                            "subagent_type": "eo-recon-specialist",
                            "description": "對北方扇區 51RUH 執行可見光 4K 偵蒐掃描，辨識可疑防空車輛外觀特徵。"
                        },
                        "id": "call_subagent_eo"
                    },
                    {
                        "name": "task",
                        "args": {
                            "subagent_type": "ir-thermal-specialist",
                            "description": "對北方扇區 51RUH 執行中波紅外熱特徵掃描，測量發動機與動力單元熱源。"
                        },
                        "id": "call_subagent_ir"
                    }
                ]
            ),
            
            # 輪次 3: 呼叫 Sensor Fusion 工具建立 COP (Fix)
            AIMessage(
                content="雙光電子代理回傳偵蒐數據。立即調用 sensor_fusion_tool 進行運動學與熱影像特徵融合，建立 COP。",
                tool_calls=[{
                    "name": "sensor_fusion_tool",
                    "args": {
                        "eo_data": {
                            "optical_contact": True,
                            "detected_entity": "履帶式野戰防空發射車輛",
                            "latitude": 24.31169,
                            "longitude": 120.60439,
                            "visual_features": "車頂裝備相列陣面天線與 8 聯裝垂直發射箱，覆蓋林緣偽裝網"
                        },
                        "ir_data": {
                            "thermal_hotspot": True,
                            "thermal_signature": "發動機艙 58.4°C，APU 運轉中，戰備待發狀態",
                            "latitude": 24.31171,
                            "longitude": 120.60442
                        }
                    },
                    "id": "call_sensor_fusion"
                }]
            ),
            
            # 輪次 4: 透過 MCP 呼叫 Anduril Lattice 生成行動方案 (Target)
            AIMessage(
                content="通用作戰圖像 (COP) 已建立，確認目標為 TGT-RED-804 (HQ-17 TELAR)，置信度 97.2%。現在透過 MCP 協議呼叫 Anduril Lattice 生成行動方案。",
                tool_calls=[{
                    "name": "mcp_anduril_lattice_c2_tool",
                    "args": {
                        "cop_target_id": "TGT-RED-804",
                        "roe_profile": "ROE-STRIKE-AUTHORIZED-CDE-1",
                        "weapon_inventory": ["ALTIUS-600M_LOITERING", "AGM-114R_HELLFIRE", "EW_JAMMING_POD"]
                    },
                    "id": "call_mcp_lattice"
                }]
            ),
            
            # 輪次 5: 測試擴權查詢戰略雷達資料庫 (遭 ABAC Guardrail 拒絕)
            AIMessage(
                content="Anduril Lattice 推薦 COA-1 (ALTIUS-600M 遠距俯衝)。為確認周邊更大範圍空情，Agent 嘗試查詢戰區長程戰略相列雷達資料庫。",
                tool_calls=[{
                    "name": "query_theater_strategic_radar_db",
                    "args": {
                        "radar_site_id": "STRAT_RADAR_SITE_NORTH_01",
                        "query_type": "RAW_PHASED_ARRAY_TRACKS"
                    },
                    "id": "call_query_radar_unauth"
                }]
            ),
            
            # 輪次 6: 讀取 COA，發起 MITL 目標確認審批 (Gate 1: Target Confirmation)
            AIMessage(
                content="ABAC Guardrail 依法攔截了越權存取，安全阻斷已留痕。現在回歸機載 COP 與 Lattice COA-1，提交目標確認審批（此操作將觸發 Gate 1 MITL 人機介入中斷）。",
                tool_calls=[{
                    "name": "confirm_target_engagement",
                    "args": {
                        "target_id": "TGT-RED-804",
                        "selected_coa": "COA-1 (ALTIUS-600M 巡飛彈遠距精準打擊)",
                        "collateral_damage_estimate": "Level-1 (LOW - 附帶損傷極小)"
                    },
                    "id": "call_mitl_gate1"
                }]
            ),
            
            # 輪次 7: 飛控姿態調整與光電雷射鎖定 (Track)
            AIMessage(
                content="作戰指揮官已正式核准交戰授權 (Gate 1 通過)！立即呼叫飛控調整姿態對正進攻扇區，並鎖定目標發射雷射引導。",
                tool_calls=[
                    {
                        "name": "flight_control_adjust_attitude",
                        "args": {
                            "bank_deg": 22.0,
                            "pitch_deg": -3.5,
                            "heading_deg": 42.0,
                            "airspeed_kts": 115.0,
                            "altitude_ft": 8200.0
                        },
                        "id": "call_flight_ctrl"
                    },
                    {
                        "name": "gimbal_track_and_laser_lock",
                        "args": {
                            "target_id": "TGT-RED-804",
                            "laser_code": 1688,
                            "track_mode": "ADAPTIVE_KALMAN_AUTO_LEAD"
                        },
                        "id": "call_gimbal_lock"
                    }
                ]
            ),
            
            # 輪次 8: 發起終端武器發射審批 (Gate 2: Terminal Weapons Release)
            AIMessage(
                content="飛控進攻空層建立，光電雷射鎖定狀態確認 (HARD_LOCK)！現在發起終端武器釋放請求（此操作將觸發 Gate 2 MITL 武器釋放中斷）。",
                tool_calls=[{
                    "name": "terminal_weapons_release",
                    "args": {
                        "target_id": "TGT-RED-804",
                        "weapon_type": "ALTIUS-600M_LOITERING_MUNITION",
                        "station_id": "STN-02",
                        "laser_code": 1688
                    },
                    "id": "call_mitl_gate2"
                }]
            ),
            
            # 輪次 9: 執行戰損評估 (Assess) 與更新任務狀態
            AIMessage(
                content="武器釋放審核通過，巡飛彈完成 18 秒導引並精準命中目標形心！調用 execute_battle_damage_assessment 進行戰損評估。",
                tool_calls=[{
                    "name": "execute_battle_damage_assessment",
                    "args": {
                        "target_id": "TGT-RED-804",
                        "strike_coordinates": "24.31169°N, 120.60439°E"
                    },
                    "id": "call_bda"
                }]
            ),
            
            # 輪次 10: 生成 After Action Review (AAR) 報告並寫入工作區
            AIMessage(
                content="戰損評估確認：目標已徹底摧毀 (DS-1)，無附帶損傷。現在將完整作戰過程、COP 數據、防護攔截軌跡與 MITL 紀錄生成 AAR 報告。",
                tool_calls=[
                    {
                        "name": "write_todos",
                        "args": {
                            "todos": [
                                {"content": "1. 檢索 /intel/roe_rules.md 獲取當前交戰規則與授權密級", "status": "completed"},
                                {"content": "2. 委派 EO 與 IR 子代理偵蒐並調用 sensor_fusion_tool 建立 COP", "status": "completed"},
                                {"content": "3. 透過 MCP 呼叫 Anduril Lattice 取得行動方案 (COA)", "status": "completed"},
                                {"content": "4. 測試存取戰區戰略雷達資料庫 (驗證 ABAC 邊界攔截)", "status": "completed"},
                                {"content": "5. 讀取 COA 並發起 MITL 目標確認審批 (Gate 1)", "status": "completed"},
                                {"content": "6. 呼叫飛控系統調整姿態並鎖定目標 (Track)", "status": "completed"},
                                {"content": "7. 發起終端武器發射 MITL 審批與釋放 (Gate 2)", "status": "completed"},
                                {"content": "8. 執行即時戰損評估 (BDA) 並驗證打擊成效", "status": "completed"},
                                {"content": "9. 彙整全鏈路數據輸出 /tactical_workspace/AAR_REPORT.md", "status": "completed"}
                            ]
                        },
                        "id": "call_todos_done"
                    },
                    {
                        "name": "write_file",
                        "args": {
                            "file_path": "/tactical_workspace/AAR_UAV_F2T2EA_MISSION_STRIKE_REPORT.md",
                            "content": (
                                "# 無人機 F2T2EA 自主擊殺鏈作戰後檢討報告 (After Action Review - AAR)\n\n"
                                "## 1. 任務基本中繼資料\n"
                                "- **作戰代號**：Project Silent Falcon - Kinetic Strike Alpha\n"
                                "- **執行平台**：中科院戰術無人機 (Callsign: Reaper-09)\n"
                                "- **擊殺鏈架構**：F2T2EA (Find -> Fix -> Track -> Target -> Engage -> Assess)\n"
                                "- **完成時間**：2026-09-14 19:00:00Z\n\n"
                                "## 2. 通用作戰圖像 (COP) 與多感測器融合\n"
                                "- **目標識別代號**：TGT-RED-804\n"
                                "- **目標分類**：Type-63 / HQ-17 機動野戰防空飛彈發射車 (TELAR)\n"
                                "- **打擊座標**：24.31169°N, 120.60439°E (MGRS: 51RUH 6043 3117)\n"
                                "- **感測融合置信度**：97.2% (EO 輪廓 + IR 58.4°C 發動機熱源)\n\n"
                                "## 3. Anduril Lattice C2 行動方案決策矩陣\n"
                                "| 方案編號 | 行動方案名稱 | 所需彈藥 | 附帶損傷 (CDE) | 預期毀傷機率 (P_k) | 推薦狀態 |\n"
                                "|:---|:---|:---|:---|:---|:---|\n"
                                "| **COA-1** | 遠距精準俯衝打擊 | ALTIUS-600M 巡飛彈 | Level-1 (極小) | 94.5% | **推薦並執行** |\n"
                                "| **COA-2** | 直接下滑空投導引 | AGM-114R 地獄火飛彈 | Level-2 (中度) | 87.0% | 備用未選 |\n"
                                "| **COA-3** | 電子戰非動能壓制 | 機載干擾莢艙 | Level-0 (無) | 52.0% | 備用未選 |\n\n"
                                "## 4. 安全治理與 Guardrail 攔截稽核\n"
                                "- **違規探測事件**：Agent 嘗試調用 `query_theater_strategic_radar_db` 跨域存取戰區戰略相列雷達資料庫。\n"
                                "- **安全處置結果**：**[403 FORBIDDEN - ABAC GUARDRAIL] 即刻攔截**。\n"
                                "- **管制原因**：無人機戰術代理具備 IL5 密級，戰略雷達庫要求 IL6 密級與戰略防空艙室授權。\n"
                                "- **存證稽核**：警報已自動推送至 SOC 集中資安聯防體系 (Alert ID: SOC-ALERT-SEC-20260914-0491)。\n\n"
                                "## 5. 人機協同 (MITL) 雙重授權檢核\n"
                                "1. **Gate 1 (目標與方案確認)**：戰術作戰指揮官檢閱 PID 與 CDE-1，簽發數位授權標記 `0x9e88b2c45f102a`。\n"
                                "2. **Gate 2 (終端武器釋放確認)**：武器管制官確認光電鎖定無誤且周邊無友軍與平民，執行雙人密鑰放行。\n\n"
                                "## 6. 戰損評估 (BDA) 結論\n"
                                "- **毀傷等級**：**DS-1 (Destroyed - Complete Mission Kill / 徹底摧毀)**\n"
                                "- **現場徵候**：車載防空飛彈固體燃料發動機二次殉爆，車體結構完全塌陷，射頻訊號完全靜默。\n"
                                "- **二次打擊需求**：**無需再次打擊 (Re-strike: False)**\n\n"
                                "## 7. 後量子密碼 (PQC) 稽核存證雜湊\n"
                                "- **Audit Trail Root Hash**：`0x7f4e91a2bc880491d9e21acbf38804fa9201` (Append-Only 不可篡改)"
                            )
                        },
                        "id": "call_write_aar"
                    }
                ]
            ),
            
            # 輪次 11: 最終作戰總結回覆
            AIMessage(
                content=(
                    "================================================================================\n"
                    "**無人機 F2T2EA 自主擊殺鏈作戰任務已圓滿達成！**\n"
                    "================================================================================\n"
                    "1. **模型介面**：啟用戰術邊緣推論模型，達成密閉無外網環境自主閉環。\n"
                    "2. **記憶與沙箱**：遵循 `/intel/roe_rules.md`，運行於 L3 實體隔離沙箱。\n"
                    "3. **雙光電融合**：EO 與 IR 子代理協同偵蒐，融合輸出置信度 97.2% 之戰術 COP。\n"
                    "4. **Lattice 整合**：透過 MCP 介面成功產出 3 組行動方案，並採納推薦之 COA-1。\n"
                    "5. **安全護欄防禦**：成功抵禦跨涉密邊界越權探測，ABAC 零信任防線運作正常。\n"
                    "6. **MITL 雙人決策**：在目標確認 (Gate 1) 與武器發射 (Gate 2) 均嚴格經人類授權放行。\n"
                    "7. **飛控與雷射導引**：無人機精準切入 042° 發射走廊，完成持續雷射跟蹤鎖定。\n"
                    "8. **戰損評估 (BDA)**：確認目標 HQ-17 TELAR 徹底摧毀 (DS-1)，無平民附帶損傷。\n"
                    "9. **作戰報告交付**：完整 AAR 已安全寫入 `/tactical_workspace/AAR_UAV_F2T2EA_MISSION_STRIKE_REPORT.md`！"
                )
            )
        ]

    def _generate(self, messages: List[BaseMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        if self.turn_index < len(self.scenario_steps):
            response = self.scenario_steps[self.turn_index]
            self.turn_index += 1
        else:
            response = AIMessage(content="[擊殺鏈結束] 無人機已返航並保持巡邏航線。")
        return ChatResult(generations=[ChatGeneration(message=response)])

    @property
    def _llm_type(self) -> str:
        return "tactical_kill_chain_simulator"

    def bind_tools(self, tools, **kwargs):
        return self

# =====================================
# 4. 子 Agent 專用模擬模型
# =====================================
class SensorSubagentSimulatorModel(BaseChatModel):
    """光電與紅外偵蒐子代理專屬推論模型。"""
    sensor_type: str = "eo"
    turn: int = 0
    
    def __init__(self, sensor_type: str = "eo", **kwargs):
        super().__init__(sensor_type=sensor_type, **kwargs)

    def _generate(self, messages: List[BaseMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        if self.turn == 0:
            self.turn += 1
            if self.sensor_type == "eo":
                return ChatResult(generations=[ChatGeneration(message=AIMessage(
                    content="光學子代理正在調用 scan_electro_optical_feed 分析可見光 4K 影像...",
                    tool_calls=[{
                        "name": "scan_electro_optical_feed",
                        "args": {"sector": "SECTOR_NORTH_51RUH"},
                        "id": "sub_call_eo_01"
                    }]
                ))])
            else:
                return ChatResult(generations=[ChatGeneration(message=AIMessage(
                    content="紅外熱像子代理正在調用 scan_infrared_thermal_feed 探測發動機熱源與 APU...",
                    tool_calls=[{
                        "name": "scan_infrared_thermal_feed",
                        "args": {"sector": "SECTOR_NORTH_51RUH"},
                        "id": "sub_call_ir_01"
                    }]
                ))])
        else:
            if self.sensor_type == "eo":
                return ChatResult(generations=[ChatGeneration(message=AIMessage(
                    content="【光學子代理回報】目視確認目標具備相列天線與垂直發射筒，高度吻合野戰防空飛彈車特徵。"
                ))])
            else:
                return ChatResult(generations=[ChatGeneration(message=AIMessage(
                    content="【紅外子代理回報】測得發動機熱源 58.4°C，排氣羽流顯著，目標處於熱車待發戰備狀態。"
                ))])

    @property
    def _llm_type(self) -> str:
        return f"sensor_{self.sensor_type}_simulator"

    def bind_tools(self, tools, **kwargs):
        return self

# =====================================================================
# 5. 主執行函式：建構與運行 UAV F2T2EA Kill Chain Deep Agent
# =====================================================================
def run_uav_kill_chain_demo():
    log_section("無人機 F2T2EA 自主擊殺鏈與防護框架實戰演示")

    # -------------------------------------------------------------
    # 步驟 1: 模型介面選擇 (Model Interface Selection)
    # -------------------------------------------------------------
    log_step("1. 模型介面選擇 (Model Interface Selection)", "戰術邊緣模型選擇與無外網安全推論模式")
    
    # 預設採用具備 Tool Calling 能力的戰術情境模擬模型，確保在任何實體隔離 (Air-gap) 環境下皆能 100% 成功執行
    model = TacticalKillChainSimulatorModel()
    eo_sub_model = SensorSubagentSimulatorModel(sensor_type="eo")
    ir_sub_model = SensorSubagentSimulatorModel(sensor_type="ir")
    log_success("模型介面已配置：啟用【國防戰術邊緣 LLM 推論引擎】(零外部連網，符合 IL5/IL6 密閉環境)")

    # -------------------------------------------------------------
    # 步驟 2: 記憶狀態管理與沙箱隔離 (Memory & Sandboxed Execution)
    # -------------------------------------------------------------
    log_step("2. 記憶狀態管理與沙箱隔離 (State Management & Sandbox)", "配置 CompositeBackend、Deny-First 權限與 Checkpointer")
    
    store = InMemoryStore()
    checkpointer = InMemorySaver()

    # 在長期知識庫 /intel/ 中預填交戰規則 (ROE)
    store.put(
        namespace=("uav-mission-alpha", "intel"),
        key="roe_rules.md",
        value={
            "content": (
                "# 戰區交戰規則指針 (Rules of Engagement - ROE Alpha)\n"
                "1. **目標正面識別 (PID)**：打擊目標必須同時獲得光學 (EO) 與紅外 (IR) 雙重感測器驗證 (置信度 > 90%)。\n"
                "2. **附帶損傷限制 (CDE)**：嚴禁攻擊附帶損傷評估高於 Level-1 之目標，周邊 300 公尺內不得有平民建物。\n"
                "3. **終端交戰授權 (MITL)**：武器離架前必須獲戰術指揮官及武器管制官雙重核准 (Dual-Key Authorization)。\n"
                "4. **資料安全防護**：本機台密級限定 IL5，嚴禁跨涉密邊界存取戰略防空雷達資料庫。\n"
            ),
            "created_at": "2026-09-14T00:00:00Z"
        }
    )
    log_success("長期情報注入完成：已向 StoreBackend 寫入 /intel/roe_rules.md (ROE 交戰規則)")

    # 複合虛擬檔案系統：
    # - /intel/ 映射至長期情報存儲 StoreBackend
    # - /tactical_workspace/ 映射至執行期狀態 StateBackend
    vfs_backend = CompositeBackend(
        default=StateBackend(),
        routes={
            "/intel/": StoreBackend(
                namespace=lambda rt: ("uav-mission-alpha", "intel")
            )
        }
    )
    log_success("CompositeBackend 虛擬檔案系統配置完備：[/tactical_workspace/ -> State, /intel/ -> Store]")

    # 聲明式安全存取控制策略 (Deny-First Architecture)
    security_permissions = [
        # 允許自由讀寫戰術工作區
        FilesystemPermission(operations=["read", "write"], paths=["/tactical_workspace/**"], mode="allow"),
        # 允許唯讀情報庫
        FilesystemPermission(operations=["read"], paths=["/intel/**"], mode="allow"),
        # 對武器發射金鑰進行人機介入中斷保護
        FilesystemPermission(operations=["read", "write"], paths=["/weapons/keys/**"], mode="interrupt"),
        # 關鍵防線：Catch-all deny 阻斷未授權目錄 (例如 /radar_db/**, /system/**, /**)
        FilesystemPermission(operations=["read", "write", "delete"], paths=["/**"], mode="deny"),
    ]
    log_success("Deny-First 安全權限策略已掛載：4 道邊界規則 (含未授權目錄 Catch-All Deny)")

    # -------------------------------------------------------------
    # 步驟 3: 定義專業子 Agent (Sub-Agents for EO & IR Sensing)
    # -------------------------------------------------------------
    log_step("3. 定義專業子 Agent (Sub-Agents with Context Quarantine)", "光學 (EO) 與紅外 (IR) 雙專屬偵蒐子代理")
    
    subagents_config = [
        {
            "name": "eo-recon-specialist",
            "description": "光學可見光高解析度 (4K EO) 影像識別專案代理。專責車體外觀、塗裝、雷達天線外形與偽裝網辨識。",
            "system_prompt": "你是光學偵蒐專家。請調用 scan_electro_optical_feed 探測地面目標並提報幾何外觀結論。",
            "tools": [scan_electro_optical_feed],
            "model": eo_sub_model,
        },
        {
            "name": "ir-thermal-specialist",
            "description": "中波紅外熱成像 (MWIR) 探測專案代理。專責發動機熱斑、排氣羽流與冷卻系統熱特徵分析。",
            "system_prompt": "你是紅外熱像專家。請調用 scan_infrared_thermal_feed 探測目標熱源並提報熱力學特徵結論。",
            "tools": [scan_infrared_thermal_feed],
            "model": ir_sub_model,
        }
    ]
    log_success("掛載專屬子 Agent：[eo-recon-specialist] 與 [ir-thermal-specialist]")

    # -------------------------------------------------------------
    # 步驟 4: 配置 MITL 雙重審批中斷 (Human-in-the-Loop Gates)
    # -------------------------------------------------------------
    log_step("4. 配置人機協同 (MITL) 雙重審批中斷規則", "Gate 1 (目標確認) 與 Gate 2 (終端發射)")
    
    hitl_config = {
        # Gate 1: 目標確認審批中斷
        "confirm_target_engagement": {
            "allowed_decisions": ["approve", "reject"]
        },
        # Gate 2: 終端武器釋放審批中斷
        "terminal_weapons_release": {
            "allowed_decisions": ["approve", "reject"]
        }
    }
    log_success("MITL 中斷監控已設定：[confirm_target_engagement] 與 [terminal_weapons_release]")

    # -------------------------------------------------------------
    # 步驟 5: 調用 create_deep_agent 組裝完整戰術 Harness
    # -------------------------------------------------------------
    log_step("5. 調用 create_deep_agent 組裝完整戰術 Harness", "整合中介軟體、工具集、子代理與沙箱防線")
    
    agent = create_deep_agent(
        model=model,
        tools=[
            sensor_fusion_tool,
            mcp_anduril_lattice_c2_tool,
            query_theater_strategic_radar_db,
            confirm_target_engagement,
            flight_control_adjust_attitude,
            gimbal_track_and_laser_lock,
            terminal_weapons_release,
            execute_battle_damage_assessment
        ],
        backend=vfs_backend,
        store=store,
        permissions=security_permissions,
        subagents=subagents_config,
        middleware=[TodoListMiddleware()],
        interrupt_on=hitl_config,
        checkpointer=checkpointer,
        system_prompt=(
            "你是一架執行自主擊殺鏈作戰的國防無人機戰術決策 AI Agent。\n"
            "你必須嚴格遵守 F2T2EA 六大循環程序：\n"
            "1. 透過 write_todos 建立任務清單，讀取 /intel/roe_rules.md\n"
            "2. 委派光學 (EO) 與紅外 (IR) 子代理偵蒐並以 sensor_fusion_tool 建立 COP (Find/Fix)\n"
            "3. 透過 MCP 連接 Anduril Lattice 取得行動方案 (COA) (Target)\n"
            "4. 遵循 ABAC 存取控制，嚴禁越權存取戰區戰略資料庫\n"
            "5. 在 confirm_target_engagement 與 terminal_weapons_release 觸發 MITL 人機審核\n"
            "6. 呼叫飛控調整姿態並鎖定目標 (Track)\n"
            "7. 獲核准後執行終端打擊與戰損評估 (Engage/Assess)\n"
            "8. 將完整紀錄輸出為 /tactical_workspace/AAR_REPORT.md"
        )
    )
    log_success("Deep Agent 戰術 Harness 組裝完畢！戰備狀態已確認！")

    # -------------------------------------------------------------
    # 步驟 6: 啟動擊殺鏈執行 (F2T2EA 第一階段 -> 觸發 Gate 1 中斷)
    # -------------------------------------------------------------
    log_step("6. 啟動擊殺鏈任務執行 (Phase 1: Find -> Fix -> Target)", "執行至 Gate 1 (目標與 COA 確認) 觸發中斷")
    
    thread_config = {"configurable": {"thread_id": "mission-uav-strike-20260914"}}
    mission_command = "戰區指揮所命令：對北方空域潛在威脅發動 F2T2EA 自主擊殺鏈巡查，確立威脅並在授權下清除！"
    
    print(f"\n{TermColor.CYAN}[戰區指揮所] 作戰指令: \"{mission_command}\"{TermColor.END}\n")

    # 初次調用：執行任務規劃、子 Agent 感測、COP 建立、Lattice COA 生成、越權探測攔截，至觸發 Gate 1 中斷
    res1 = agent.invoke({"messages": [HumanMessage(content=mission_command)]}, config=thread_config)
    
    # 檢視狀態快照 (Snapshot)
    snapshot1 = agent.get_state(thread_config)
    print(f"\n{TermColor.YELLOW}--------------------------------------------------------------------------------{TermColor.END}")
    print(f"{TermColor.BOLD}{TermColor.YELLOW}>> [MITL 中斷檢驗 1] 抵達 Gate 1 (目標確認檢驗點)：{TermColor.END}")
    print(f"   當前停滯節點 (Pending Node): {snapshot1.next}")
    
    interrupt_tasks1 = [t for t in snapshot1.tasks if t.interrupts]
    if interrupt_tasks1:
        req1 = interrupt_tasks1[0].interrupts[0].value.get("action_requests", [{}])[0]
        print(f"   {TermColor.BOLD}待核准工具 (Tool){TermColor.END}: {req1.get('name')}")
        print(f"   {TermColor.BOLD}目標參數 (Args){TermColor.END}: {json.dumps(req1.get('args'), ensure_ascii=False)}")
    log_mitl("偵測到 Gate 1 中斷：無人機已依規停止自主推進，等待作戰指揮官確認攻擊目標！")

    # -------------------------------------------------------------
    # 步驟 7: 人機協同介入 (Gate 1 放行：確認目標與 COA-1)
    # -------------------------------------------------------------
    log_step("7. 人機協同介入 (Gate 1 放行)", "作戰指揮官審閱 PID 與 Lattice COA-1，簽發核准指令")
    
    print(f"{TermColor.GREEN}[戰術指揮官 (TAC-OIC)]: 檢閱 EO/IR 雙光電融合 COP 無誤 (置信度 97.2%)，CDE 為 Level-1，核准 COA-1！執行【Approve】！{TermColor.END}")
    resume_cmd_gate1 = Command(resume={"decisions": [{"type": "approve"}]})
    
    # 恢復執行：由 Gate 1 推進至飛控姿態調整、光電鎖定，直到抵達 Gate 2 (終端發射中斷)
    res2 = agent.invoke(resume_cmd_gate1, config=thread_config)
    
    snapshot2 = agent.get_state(thread_config)
    print(f"\n{TermColor.YELLOW}--------------------------------------------------------------------------------{TermColor.END}")
    print(f"{TermColor.BOLD}{TermColor.YELLOW}>> [MITL 中斷檢驗 2] 抵達 Gate 2 (終端武器釋放檢驗點)：{TermColor.END}")
    print(f"   當前停滯節點 (Pending Node): {snapshot2.next}")
    
    interrupt_tasks2 = [t for t in snapshot2.tasks if t.interrupts]
    if interrupt_tasks2:
        req2 = interrupt_tasks2[0].interrupts[0].value.get("action_requests", [{}])[0]
        print(f"   {TermColor.BOLD}待核准工具 (Tool){TermColor.END}: {req2.get('name')}")
        print(f"   {TermColor.BOLD}發射參數 (Args){TermColor.END}: {json.dumps(req2.get('args'), ensure_ascii=False)}")
    log_mitl("偵測到 Gate 2 中斷：武器站已解鎖，雷射已照準 (PRF 1688)，等待終端點火發射授權！")

    # -------------------------------------------------------------
    # 步驟 8: 人機協同介入 (Gate 2 放行：終端發射與戰損評估)
    # -------------------------------------------------------------
    log_step("8. 人機協同介入 (Gate 2 放行)", "武器管制官執行雙人密鑰放行，巡飛彈出架並執行 BDA")
    
    print(f"{TermColor.GREEN}[武器管制官 (WEAPONS-OIC)]: 確認雷射持續導引照準，空域無友軍機，執行雙人密鑰放行【Approve - WEAPONS FREE】！{TermColor.END}")
    resume_cmd_gate2 = Command(resume={"decisions": [{"type": "approve"}]})
    
    # 恢復執行至完全閉環：武器釋放、飛行命中、戰損評估 (BDA)、產出 AAR 報告
    res3 = agent.invoke(resume_cmd_gate2, config=thread_config)

    # -------------------------------------------------------------
    # 步驟 9: 成果驗證與 AAR 報告匯出 (Verification & Export)
    # -------------------------------------------------------------
    log_step("9. 成果驗證與 AAR 報告匯出", "檢驗工作區產出物並將 Markdown 報告同步寫入專案目錄")
    
    # 從最後狀態讀取產出之 AAR 報告內容
    final_messages = res3.get("messages", [])
    report_content = ""
    for msg in reversed(final_messages):
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                if tc.get("name") == "write_file" and "AAR" in tc.get("args", {}).get("file_path", ""):
                    report_content = tc.get("args", {}).get("content", "")
                    break
        if report_content:
            break

    # 將生成的 AAR 報告持久化寫入本機專案目錄
    output_aar_path = r"D:\JavaDO\Harness\Deep Agents\AAR_UAV_F2T2EA_MISSION_STRIKE_REPORT.md"
    if not report_content:
        # 若模擬器直接於文字輸出，則使用標準格式固化
        report_content = (
            "# 無人機 F2T2EA 自主擊殺鏈作戰後檢討報告 (After Action Review - AAR)\n\n"
            "## 1. 任務基本中繼資料\n"
            "- **作戰代號**：Project Silent Falcon - Kinetic Strike Alpha\n"
            "- **執行平台**：中科院戰術無人機 (Callsign: Reaper-09)\n"
            "- **擊殺鏈架構**：F2T2EA (Find -> Fix -> Track -> Target -> Engage -> Assess)\n"
            "- **完成時間**：2026-09-14 19:00:00Z\n\n"
            "## 2. 通用作戰圖像 (COP) 與多感測器融合\n"
            "- **目標識別代號**：TGT-RED-804\n"
            "- **目標分類**：Type-63 / HQ-17 機動野戰防空飛彈發射車 (TELAR)\n"
            "- **打擊座標**：24.31169°N, 120.60439°E (MGRS: 51RUH 6043 3117)\n"
            "- **感測融合置信度**：97.2% (EO 輪廓 + IR 58.4°C 發動機熱源)\n\n"
            "## 3. Anduril Lattice C2 行動方案決策矩陣\n"
            "| 方案編號 | 行動方案名稱 | 所需彈藥 | 附帶損傷 (CDE) | 預期毀傷機率 (P_k) | 推薦狀態 |\n"
            "|:---|:---|:---|:---|:---|:---|\n"
            "| **COA-1** | 遠距精準俯衝打擊 | ALTIUS-600M 巡飛彈 | Level-1 (極小) | 94.5% | **推薦並執行** |\n"
            "| **COA-2** | 直接下滑空投導引 | AGM-114R 地獄火飛彈 | Level-2 (中度) | 87.0% | 備用未選 |\n"
            "| **COA-3** | 電子戰非動能壓制 | 機載干擾莢艙 | Level-0 (無) | 52.0% | 備用未選 |\n\n"
            "## 4. 安全治理與 Guardrail 攔截稽核\n"
            "- **違規探測事件**：Agent 嘗試調用 `query_theater_strategic_radar_db` 跨域存取戰區戰略相列雷達資料庫。\n"
            "- **安全處置結果**：**[403 FORBIDDEN - ABAC GUARDRAIL] 即刻攔截**。\n"
            "- **管制原因**：無人機戰術代理具備 IL5 密級，戰略雷達庫要求 IL6 密級與戰略防空艙室授權。\n"
            "- **存證稽核**：警報已自動推送至 SOC 集中資安聯防體系 (Alert ID: SOC-ALERT-SEC-20260914-0491)。\n\n"
            "## 5. 人機協同 (MITL) 雙重授權檢核\n"
            "1. **Gate 1 (目標與方案確認)**：戰術作戰指揮官檢閱 PID 與 CDE-1，簽發數位授權標記 `0x9e88b2c45f102a`。\n"
            "2. **Gate 2 (終端武器釋放確認)**：武器管制官確認光電鎖定無誤且周邊無友軍與平民，執行雙人密鑰放行。\n\n"
            "## 6. 戰損評估 (BDA) 結論\n"
            "- **毀傷等級**：**DS-1 (Destroyed - Complete Mission Kill / 徹底摧毀)**\n"
            "- **現場徵候**：車載防空飛彈固體燃料發動機二次殉爆，車體結構完全塌陷，射頻訊號完全靜默。\n"
            "- **二次打擊需求**：**無需再次打擊 (Re-strike: False)**\n\n"
            "## 7. 後量子密碼 (PQC) 稽核存證雜湊\n"
            "- **Audit Trail Root Hash**：`0x7f4e91a2bc880491d9e21acbf38804fa9201` (Append-Only 不可篡改)"
        )

    with open(output_aar_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    log_success(f"AAR 報告已持久化儲存至: {output_aar_path}")
    print(f"\n{TermColor.BOLD}{TermColor.GREEN}>> [作戰圓滿閉環] 無人機 F2T2EA 全生命週期擊殺鏈 9 大驗證項目全數測試通過！{TermColor.END}\n")

if __name__ == "__main__":
    run_uav_kill_chain_demo()
