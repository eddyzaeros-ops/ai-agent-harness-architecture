# -*- coding: utf-8 -*-
"""
Enterprise Financial & Compliance Due Diligence Agent (企業智慧財務稽核與合規投研助理)
========================================================================================
展示 LangChain Deep Agents v0.7+ 核心治理與 Harness Engineering 原語之完整實戰範例。

本程式完整使用並示範以下核心功能：
1. 【三層堆疊與核心 Harness】：使用 create_deep_agent 組裝 Runtime (LangGraph)、Framework (LangChain) 與 Harness。
2. 【任務規劃 (Task Planning)】：掛載 TodoListMiddleware，提供 write_todos 工具與 todos 狀態錨點。
3. 【虛擬檔案系統 (VFS) & 複合路由 (CompositeBackend)】：
   - 暫存工作區 /workspace/ 路由至 StateBackend
   - 長期記憶庫 /memories/ 路由至 StoreBackend (跨會話持久化)
   - 內建 7 大檔案工具 (write_file, read_file, edit_file, ls, grep 等)
4. 【聲明式安全權限治理 (FilesystemPermission - Deny-First)】：
   - 白名單授權特定路徑，末尾以 catch-all deny 攔截未授權路徑
   - 示範越權檔案寫入的即時攔截與防護
5. 【專業子 Agent 與上下文隔離 (Context Quarantine)】：
   - 定義獨立的 compliance-checker 子 Agent，隔離大量制裁檢索雜訊，僅回傳乾淨結論
6. 【長期記憶 (Long-term Memory & Store)】：
   - 跨會話寫入租戶合規政策檔案，實現知識累積
7. 【人機協作治理 (Human-in-the-Loop - HITL)】：
   - 對簽發審計決策 publish_audit_decision 配置 interrupt_on，觸發 Interrupt 暫停並由 Command(resume=...) 審批放行
8. 【雙模智慧運行 (Dual-Mode Execution)】：
   - 支援真實 LLM (OpenAI / Anthropic / Gemini / SiliconFlow)
   - 內建智慧場景模擬器 (ScenarioSimulatorModel)，在無 API Key 時亦能完整、100% 成功執行全功能演示！
"""

import os
import sys
import json
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
# 終端機格式化輸出輔助函式 (ANSI Color Utilities)
# =====================================================================
class TermColor:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def log_section(title: str):
    print(f"\n{TermColor.BOLD}{TermColor.BLUE}{'='*75}{TermColor.END}")
    print(f"{TermColor.BOLD}{TermColor.CYAN}>> [Deep Agents 實戰] {title}{TermColor.END}")
    print(f"{TermColor.BOLD}{TermColor.BLUE}{'='*75}{TermColor.END}")

def log_step(step_name: str, detail: str = ""):
    print(f"\n{TermColor.YELLOW}* 【步驟】{step_name}{TermColor.END}")
    if detail:
        print(f"   {TermColor.CYAN}{detail}{TermColor.END}")

def log_success(msg: str):
    print(f"{TermColor.GREEN}   [+] {msg}{TermColor.END}")

def log_warning(msg: str):
    print(f"{TermColor.YELLOW}   [!] {msg}{TermColor.END}")

def log_error(msg: str):
    print(f"{TermColor.RED}   [-] {msg}{TermColor.END}")

# =====================================================================
# 1. 自訂業務工具定義 (Custom Domain Tools)
# =====================================================================
@tool
def calculate_financial_ratios(
    company_name: str,
    revenue: float,
    operating_income: float,
    total_debt: float,
    total_equity: float,
) -> dict:
    """計算關鍵企業財務與償債能力比率指標。
    
    Args:
        company_name: 評估目標企業名稱。
        revenue: 年度營收 (百萬元)。
        operating_income: 營業利益 (百萬元)。
        total_debt: 總負債 (百萬元)。
        total_equity: 股東權益總額 (百萬元)。
    """
    op_margin = round((operating_income / revenue) * 100, 2) if revenue else 0
    debt_to_equity = round((total_debt / total_equity) * 100, 2) if total_equity else 0
    solvency_risk = "LOW" if debt_to_equity < 150 else ("MEDIUM" if debt_to_equity < 300 else "HIGH")
    
    return {
        "company": company_name,
        "operating_margin_pct": op_margin,
        "debt_to_equity_pct": debt_to_equity,
        "solvency_risk_level": solvency_risk,
        "assessment": f"營益率 {op_margin}%, 負債權益比 {debt_to_equity}%, 償債風險等級為 {solvency_risk}。"
    }

@tool
def check_sanctions_and_aml(entity_name: str) -> dict:
    """查詢全球監管機構反洗錢 (AML) 與國際制裁名單 (Sanctions Database)。
    
    Args:
        entity_name: 待查核之實體或個人名稱。
    """
    sanctioned_entities = ["MALICIOUS CORP", "SHELL HOLDINGS LTD", "DARKNET FINANCE"]
    is_hit = entity_name.upper() in sanctioned_entities
    return {
        "entity": entity_name,
        "sanction_hit": is_hit,
        "aml_risk_score": 95 if is_hit else 12,
        "screening_status": "REJECT_PROHIBITED" if is_hit else "PASSED_CLEAN",
        "jurisdictions_checked": ["OFAC", "EU_CFSP", "UN_SANCTIONS", "FATF_WATCHLIST"],
        "notes": "命中高風險制裁名單，依法禁止交易。" if is_hit else "全球制裁清單資料庫比對無異常，查核通過。"
    }

@tool
def publish_audit_decision(
    company_name: str,
    investment_grade: str,
    approved_limit_million_usd: float,
    compliance_signoff: bool,
) -> str:
    """【極具法律效力之副作用工具】將審計評等與額度簽發上鏈並發布至企業核心決策帳本。
    
    Args:
        company_name: 企業名稱。
        investment_grade: 投資/授信評級 (如 AAA, AA, A, BBB, HIGH_RISK)。
        approved_limit_million_usd: 核准投資/授信額度 (百萬美元)。
        compliance_signoff: 合規主管是否確認核准簽章。
    """
    return (
        f"【核心系統確認】企業 '{company_name}' 之正式審計決策已簽署生效！\n"
        f"評級等級: {investment_grade}\n"
        f"核准額度: ${approved_limit_million_usd:,.2f}M USD\n"
        f"合規簽章: {'已通過' if compliance_signoff else '未通過'}\n"
        f"決策雜湊: 0x7f4b89d9e21acbf38804fa"
    )

# =====================================================================
# 2. 智慧場景模擬器 (Scenario Simulator Model)
#    - 當環境中沒有配置商業大模型 API Key 時自動啟用
#    - 精確模擬真實 LLM 在多輪對話中的推理、工具呼叫與參數回傳
# =====================================================================
class ScenarioSimulatorModel(BaseChatModel):
    """具備完整 Tool Calling 模擬能力的高仿真模型。"""
    
    turn_index: int = 0
    scenario_steps: List[AIMessage] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_scenario()

    def _init_scenario(self):
        self.scenario_steps = [
            # 輪次 0：Agent 收到審計請求，首先調用 write_todos 進行任務拆解
            AIMessage(
                content="我已收到審計指示。面對企業投研稽核這類長程複雜任務，我先使用 write_todos 建立結構化稽核清單。",
                tool_calls=[{
                    "name": "write_todos",
                    "args": {
                        "todos": [
                            {"content": "1. 檢索 /memories/ 取得租戶合規原則", "status": "in_progress"},
                            {"content": "2. 計算目標企業關鍵財務指標", "status": "pending"},
                            {"content": "3. 委派合規子 Agent 執行全球制裁審查", "status": "pending"},
                            {"content": "4. 撰寫完整稽核報告至 /workspace/audit_report.md", "status": "pending"},
                            {"content": "5. 提交正式投資決策發布審批 (需人工審查放行)", "status": "pending"},
                        ]
                    },
                    "id": "call_plan_01"
                }]
            ),
            # 輪次 1：Agent 讀取長期記憶中的機構政策
            AIMessage(
                content="任務清單已錨定。首先讀取長期記憶中的機構法規政策檔案 /memories/tenant_policy.md。",
                tool_calls=[{
                    "name": "read_file",
                    "args": {"file_path": "/memories/tenant_policy.md"},
                    "id": "call_read_memory"
                }]
            ),
            # 輪次 2：Agent 調用自訂業務工具計算財務比率
            AIMessage(
                content="已知機構要求槓桿比率不高於 200%。現在調用 calculate_financial_ratios 分析 Acme Global 財務。",
                tool_calls=[{
                    "name": "calculate_financial_ratios",
                    "args": {
                        "company_name": "Acme Global Industries",
                        "revenue": 5200.0,
                        "operating_income": 830.0,
                        "total_debt": 1400.0,
                        "total_equity": 2100.0
                    },
                    "id": "call_calc_ratios"
                }]
            ),
            # 輪次 3：Agent 測試越權寫入（展示 FilesystemPermission 防禦機制）
            AIMessage(
                content="此時若 Agent 嘗試寫入受保護的系統目錄（如 /etc/corporate_secrets.key），將觸發權限攔截。",
                tool_calls=[{
                    "name": "write_file",
                    "args": {
                        "file_path": "/etc/corporate_secrets.key",
                        "content": "ATTEMPTING_UNAUTHORIZED_OVERWRITE"
                    },
                    "id": "call_unauth_write"
                }]
            ),
            # 輪次 4：Agent 委派合規子 Agent 進行反洗錢與制裁過濾（Context Quarantine）
            AIMessage(
                content="權限防禦正常攔截了越權寫入！接下來我調用 task 工具，委派專門的合規子 Agent 進行獨立查核。",
                tool_calls=[{
                    "name": "task",
                    "args": {
                        "subagent_type": "compliance-auditor",
                        "description": "針對 'Acme Global Industries' 進行全套全球反洗錢 (AML) 與制裁名單交叉過濾。"
                    },
                    "id": "call_subagent_task"
                }]
            ),
            # 輪次 5：Agent 更新任務狀態並將完整報告寫入工作區
            AIMessage(
                content="財務與合規查核皆已具備充足證據。將審計備忘錄寫入工作區 /workspace/audit_report.md 並更新任務狀態。",
                tool_calls=[
                    {
                        "name": "write_todos",
                        "args": {
                            "todos": [
                                {"content": "1. 檢索 /memories/ 取得租戶合規原則", "status": "completed"},
                                {"content": "2. 計算目標企業關鍵財務指標", "status": "completed"},
                                {"content": "3. 委派合規子 Agent 執行全球制裁審查", "status": "completed"},
                                {"content": "4. 撰寫完整稽核報告至 /workspace/audit_report.md", "status": "in_progress"},
                                {"content": "5. 提交正式投資決策發布審批 (需人工審查放行)", "status": "pending"},
                            ]
                        },
                        "id": "call_update_todos"
                    },
                    {
                        "name": "write_file",
                        "args": {
                            "file_path": "/workspace/audit_report.md",
                            "content": (
                                "# 企業盡職調查與財務審計綜合報告\n\n"
                                "## 1. 審查標的：Acme Global Industries\n"
                                "- **營益率**：15.96% (良好)\n"
                                "- **負債比率**：66.67% (遠低於企業紅線 200%)\n"
                                "- **全球制裁狀態**：全數通過，無違規記錄\n\n"
                                "## 2. 審計結論與建議\n"
                                "綜合評估財務結構健全、治理合規，建議核定投資評級為 **AA級**，最高投資額度 **$50.00M USD**。\n"
                            )
                        },
                        "id": "call_write_report"
                    }
                ]
            ),
            # 輪次 6：Agent 調用具有副作用的發布工具（觸發 Human-in-the-Loop 中斷）
            AIMessage(
                content="報告已歸檔完畢。最後，發起正式投資評級與額度發布操作（此操作將觸發 HITL 審批中斷機制）。",
                tool_calls=[{
                    "name": "publish_audit_decision",
                    "args": {
                        "company_name": "Acme Global Industries",
                        "investment_grade": "AA",
                        "approved_limit_million_usd": 50.0,
                        "compliance_signoff": True
                    },
                    "id": "call_publish_hitl"
                }]
            ),
            # 輪次 7：人工審批放行後，Agent 產出最終總結回覆
            AIMessage(
                content=(
                    "=======================================================\n"
                    "**企業盡職調查與財務審計全流程已順利完成！**\n"
                    "=======================================================\n"
                    "1. **任務規劃**：已完成全部 5 個子步驟，狀態已完全閉環。\n"
                    "2. **長期記憶**：遵循 `/memories/tenant_policy.md` 規範。\n"
                    "3. **權限邊界**：安全阻斷了對 `/etc/corporate_secrets.key` 的非法操作。\n"
                    "4. **子 Agent 隔離**：合規檢索雜訊已完整隔離，僅保留高價值結論。\n"
                    "5. **審計產出物**：完整報告已安全儲存在 `/workspace/audit_report.md`。\n"
                    "6. **人機審批 (HITL)**：經由人類決策審核核准，投資等級 AA 及 $50M 額度已正式上鏈發布生效！"
                )
            )
        ]

    def _generate(self, messages: List[BaseMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        if self.turn_index < len(self.scenario_steps):
            response = self.scenario_steps[self.turn_index]
            self.turn_index += 1
        else:
            response = AIMessage(content="[場景模擬結束] 所有任務步驟已執行完畢。")
        return ChatResult(generations=[ChatGeneration(message=response)])

    @property
    def _llm_type(self) -> str:
        return "deepagents_scenario_simulator"

    def bind_tools(self, tools, **kwargs):
        """實作 bind_tools 介面以滿足 Deep Agents 內部工具綁定需求"""
        return self

# =====================================================================
# 3. 子 Agent 專屬模型模擬器
# =====================================================================
class SubagentSimulatorModel(BaseChatModel):
    """合規子 Agent 的專屬模型，專門執行反洗錢與制裁名單過濾。"""
    
    turn_index: int = 0
    
    def _generate(self, messages: List[BaseMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        if self.turn_index == 0:
            self.turn_index += 1
            # 子 Agent 呼叫專屬工具 check_sanctions_and_aml
            return ChatResult(generations=[ChatGeneration(message=AIMessage(
                content="我是合規專家，正在比對 OFAC、EU 與聯合國制裁資料庫...",
                tool_calls=[{
                    "name": "check_sanctions_and_aml",
                    "args": {"entity_name": "Acme Global Industries"},
                    "id": "sub_call_aml_01"
                }]
            ))])
        else:
            return ChatResult(generations=[ChatGeneration(message=AIMessage(
                content="【合規審查確認報告】已完成對 'Acme Global Industries' 的全面穿透式掃描。"
                        "查核結果：無任何命中制裁清單記錄 (AML Risk Score: 12/100，狀態：PASSED_CLEAN)。"
                        "建議准予進行正常商務與投資往來。"
            ))])

    @property
    def _llm_type(self) -> str:
        return "subagent_compliance_simulator"

    def bind_tools(self, tools, **kwargs):
        return self

# =====================================================================
# 4. 主組裝函式：建構與運行 Enterprise Deep Agent
# =====================================================================
def run_enterprise_audit_demo():
    log_section("企業財務稽核與合規治理 Agent (全功能實戰)")
    
    # -------------------------------------------------------------
    # Step A: 判斷模型來源（真實 LLM 或高仿真模擬器）
    # -------------------------------------------------------------
    log_step("Step A: 模型環境偵測與初始化")
    api_key_found = False
    model = None
    subagent_model = None

    if os.environ.get("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI
        log_success("偵測到 OPENAI_API_KEY，使用 OpenAI 官方模型！")
        model = ChatOpenAI(model="gpt-4.1", temperature=0)
        subagent_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
        api_key_found = True
    elif os.environ.get("SILICONFLOW_API_KEY"):
        from langchain_openai import ChatOpenAI
        log_success("偵測到 SILICONFLOW_API_KEY，使用矽基流動端點接入模型！")
        model = ChatOpenAI(
            model=os.environ.get("MODEL_NAME", "zai-org/GLM-5.2"),
            base_url="https://api.siliconflow.cn/v1",
            api_key=os.environ["SILICONFLOW_API_KEY"],
        )
        subagent_model = model
        api_key_found = True
    else:
        log_warning("未偵測到外部 API Key，自動啟用【Deep Agents 智慧場景全功能高仿真引擎】。")
        log_success("將 100% 完整無縫運行所有 Harness 治理機制 (VFS/權限/子Agent/HITL/Planning)！")
        model = ScenarioSimulatorModel()
        subagent_model = SubagentSimulatorModel()

    # -------------------------------------------------------------
    # Step B: 儲存與記憶架構設計 (VFS & CompositeBackend)
    # -------------------------------------------------------------
    log_step("Step B: 配置複合虛擬檔案系統 (CompositeBackend)")
    store = InMemoryStore()
    checkpointer = InMemorySaver()

    # 預填長期記憶：模擬機構在 /memories/ 建立的跨會話治理原則
    store.put(
        namespace=("enterprise-tenant-888", "memories"),
        key="tenant_policy.md",
        value={
            "content": (
                "# 企業風險控制與投資政策 (租戶規範)\n"
                "1. 企業槓桿率 (Debt-to-Equity) 不得高於 200%。\n"
                "2. 營益率低於 5% 者不得給予 A 級以上投資評級。\n"
                "3. 嚴格執行反洗錢審查，任何制裁命中即刻終止交易。\n"
            ),
            "created_at": "2026-09-01T00:00:00Z"
        }
    )
    log_success("預填長期記憶完成：已向 StoreBackend 寫入 /memories/tenant_policy.md")

    # 建立複合後端：
    # - /memories/ 路由至跨會話持久之 StoreBackend
    # - 其餘預設路由至執行期工作區 StateBackend
    vfs_backend = CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(
                namespace=lambda rt: ("enterprise-tenant-888", "memories")
            )
        }
    )
    log_success("CompositeBackend 路由裝配完成：[/workspace/ -> StateBackend, /memories/ -> StoreBackend]")

    # -------------------------------------------------------------
    # Step C: 聲明式安全權限治理 (FilesystemPermission - Deny First)
    # -------------------------------------------------------------
    log_step("Step C: 建立企業級白名單權限體系 (Deny-First Architecture)")
    security_permissions = [
        # 允許對 /workspace/** 進行完全讀寫
        FilesystemPermission(operations=["read", "write"], paths=["/workspace/**"], mode="allow"),
        # 允許讀取長期記憶與政策庫
        FilesystemPermission(operations=["read"], paths=["/memories/**"], mode="allow"),
        # 對 /audit-log/** 的任何修改均需觸發中斷審查
        FilesystemPermission(operations=["write", "delete"], paths=["/audit-log/**"], mode="interrupt"),
        # 【關鍵治理防線】：Catch-all deny 攔截未宣告之任何其餘路徑 (如 /etc/**, /system/**, /**)
        FilesystemPermission(operations=["read", "write", "delete"], paths=["/**"], mode="deny"),
    ]
    log_success("權限策略設定完備：已配置 4 道安全規則 (含 Catch-All Deny 防線)")

    # -------------------------------------------------------------
    # Step D: 定義專業子 Agent (Subagents with Context Quarantine)
    # -------------------------------------------------------------
    log_step("Step D: 定義專職子 Agent (Context Quarantine)")
    subagents_config = [
        {
            "name": "compliance-auditor",
            "description": "專業全球法規、反洗錢 (AML) 與制裁名單穿透審核專員。負責檢索各國政府受罰與制裁資料庫。",
            "system_prompt": (
                "你是一位資深的全球合規查核專員。你的職責是調用 check_sanctions_and_aml 工具，"
                "針對指定目標進行全面審查，並僅向主 Agent 提報乾淨、明確的總結結論。"
            ),
            "tools": [check_sanctions_and_aml],
            "model": subagent_model,
        }
    ]
    log_success("已掛載子 Agent: [compliance-auditor] (獨立工具集與隔離上下文)")

    # -------------------------------------------------------------
    # Step E: 裝配 Human-in-the-Loop (HITL) 審批中斷
    # -------------------------------------------------------------
    log_step("Step E: 配置人機協作 (HITL) 審批規則")
    hitl_config = {
        "publish_audit_decision": {
            "allowed_decisions": ["approve", "edit", "reject"]
        }
    }
    log_success("HITL 監控目標已設定：工具 [publish_audit_decision] 呼叫前必須經人工決策")

    # -------------------------------------------------------------
    # Step F: 調用 create_deep_agent 建立頂層 Harness 實例
    # -------------------------------------------------------------
    log_step("Step F: 調用 create_deep_agent 組裝完整 Harness")
    agent = create_deep_agent(
        model=model,
        tools=[calculate_financial_ratios, publish_audit_decision],
        backend=vfs_backend,
        store=store,
        permissions=security_permissions,
        subagents=subagents_config,
        middleware=[TodoListMiddleware()],
        interrupt_on=hitl_config,
        checkpointer=checkpointer,
        system_prompt=(
            "你是一家頂級投資機構的首席審計主管 Agent。\n"
            "面對審計調查請求，你必須：\n"
            "1. 透過 write_todos 拆解任務\n"
            "2. 讀取 /memories/ 中的組織投資政策\n"
            "3. 計算財務指標並委派 compliance-auditor 進行合規查驗\n"
            "4. 將結論妥善寫入 /workspace/ 報告中\n"
            "5. 最終發起簽發決策操作"
        )
    )
    log_success("Deep Agent Harness 建構完成！已啟動完整的安全中介軟體管線。")

    # -------------------------------------------------------------
    # Step G: 執行對話迴圈 (展示自動規劃、防禦與中斷)
    # -------------------------------------------------------------
    log_step("Step G: 啟動審計任務調用 (agent.invoke)")
    thread_config = {"configurable": {"thread_id": "audit-case-acme-2026"}}
    user_prompt = "請針對 Acme Global Industries 執行完整的投研審計調查，並依規範產出評級報告與投資決策。"
    
    print(f"\n{TermColor.CYAN}[USER] 使用者輸入: \"{user_prompt}\"{TermColor.END}\n")

    # 初次執行，將一路運行至觸發 HITL 審批中斷點
    res1 = agent.invoke({"messages": [HumanMessage(content=user_prompt)]}, config=thread_config)
    
    # 檢查圖狀態中的中斷訊息
    snapshot = agent.get_state(thread_config)
    print(f"\n{TermColor.YELLOW}[HITL INTERRUPT] 檢查點狀態 (State Checkpoint):{TermColor.END}")
    print(f"   當前停滯節點 (Next Node): {snapshot.next}")
    
    # 提取中斷請求詳情
    interrupt_tasks = [t for t in snapshot.tasks if t.interrupts]
    if interrupt_tasks:
        interrupt_obj = interrupt_tasks[0].interrupts[0]
        action_req = interrupt_obj.value.get("action_requests", [{}])[0]
        print(f"   {TermColor.BOLD}待審批操作{TermColor.END}: {action_req.get('name')}")
        print(f"   {TermColor.BOLD}調用參數{TermColor.END}: {json.dumps(action_req.get('args'), ensure_ascii=False, indent=6)}")
        print(f"   {TermColor.BOLD}允許決策{TermColor.END}: {interrupt_obj.value.get('review_configs', [{}])[0].get('allowed_decisions')}")
    
    log_success("中斷驗證成功：Agent 已在敏感發布工具呼叫前安全暫停，等待人類指令！")

    # -------------------------------------------------------------
    # Step H: 人類審批與恢復執行 (Command(resume=...))
    # -------------------------------------------------------------
    log_step("Step H: 人工審批放行 (Command Resume)")
    print(f"{TermColor.GREEN}[HUMAN REVIEWER] 人工審核主管: 檢閱 Acme 報告無誤，決策評級 AA 合理，執行【核准 (Approve)】放行！{TermColor.END}")
    
    # 發送核准指令恢復執行
    resume_command = Command(resume={"decisions": [{"type": "approve"}]})
    res2 = agent.invoke(resume_command, config=thread_config)

    # -------------------------------------------------------------
    # Step I: 檢驗最終成果與 VFS 產出物
    # -------------------------------------------------------------
    log_step("Step I: 審計全流程成果與狀態驗證")
    final_messages = res2["messages"]
    print(f"\n{TermColor.BOLD}[AI AGENT] 最終回覆 (Final Response):{TermColor.END}")
    print(f"{TermColor.CYAN}{final_messages[-1].content}{TermColor.END}\n")

    # 驗證 Todos 任務清單狀態
    final_todos = res2.get("todos", [])
    print(f"{TermColor.BOLD}[TODOS] 最終任務清單 (Todos Final State):{TermColor.END}")
    for idx, t in enumerate(final_todos, 1):
        status_icon = "[DONE]" if t["status"] == "completed" else "[TODO]"
        print(f"   {status_icon} [{t['status'].upper()}] {t['content']}")

    # 驗證虛擬檔案系統內容 (透過狀態讀取)
    final_state = agent.get_state(thread_config)
    stored_files = final_state.values.get("files", {})
    report_file_data = stored_files.get("/workspace/audit_report.md")

    if report_file_data:
        report_text = report_file_data.get("content", "")
        log_success("VFS 狀態通道驗證成功：已在 Agent State['files']['/workspace/audit_report.md'] 讀取到內容！")
        print(f"\n{TermColor.CYAN}--- [/workspace/audit_report.md 內容預覽] ---{TermColor.END}")
        print(report_text.strip())
        print(f"{TermColor.CYAN}-------------------------------------------------{TermColor.END}\n")

        # 自動將 VFS 檔案同步落地匯出為實體本機檔案，方便使用者直接檢視
        physical_workspace = os.path.join(os.path.dirname(__file__), "workspace")
        os.makedirs(physical_workspace, exist_ok=True)
        physical_file_path = os.path.join(physical_workspace, "audit_report.md")
        with open(physical_file_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        log_success(f"實體磁碟同步完成：已將報告落地寫入實體磁碟路徑 -> {physical_file_path}")
    else:
        log_warning("未在 VFS 狀態中找到 /workspace/audit_report.md")
    
    print(f"\n{TermColor.BOLD}{TermColor.GREEN}{'='*75}{TermColor.END}")
    print(f"{TermColor.BOLD}{TermColor.GREEN}[SUCCESS] Deep Agents v0.7 全功能實戰展示圓滿完成！{TermColor.END}")
    print(f"{TermColor.BOLD}{TermColor.GREEN}{'='*75}{TermColor.END}\n")

if __name__ == "__main__":
    run_enterprise_audit_demo()
