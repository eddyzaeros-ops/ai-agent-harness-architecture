# -*- coding: utf-8 -*-
"""
slides_charts.py
Dedicated Matplotlib Chart Slides conforming strictly to PPTX Template 1.
Warm Editorial Minimalism layout: Left High-DPI Chart Card + Right Key Takeaways Bullet Stack.
"""

import os
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from slides_common import (
    apply_warm_background,
    add_header,
    add_footer,
    add_bullet_card,
    TOTAL_SLIDES,
    BG_CARD,
    BORDER_CARD,
    BRAND_SAGE,
    BRAND_TERRA,
    BRAND_SLATE
)

CHARTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")

def _add_chart_slide(slide, title, category, subtitle, chart_filename, right_title, insights):
    """Reusable layout for standard Template 1 chart slide."""
    apply_warm_background(slide)
    add_header(slide, title, category, subtitle)
    
    # Left container card
    container = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.74), Inches(1.75), Inches(7.42), Inches(5.10)
    )
    container.fill.solid()
    container.fill.fore_color.rgb = BG_CARD
    container.line.color.rgb = BORDER_CARD
    container.line.width = Pt(1)
    
    # Left chart image
    chart_path = os.path.join(CHARTS_DIR, chart_filename)
    if os.path.exists(chart_path):
        slide.shapes.add_picture(
            chart_path,
            Inches(0.80), Inches(1.81), Inches(7.30), Inches(4.98)
        )
        
    # Right bullet card stack (Mode B: Modular Stack)
    add_bullet_card(
        slide,
        left=8.30,
        top=1.75,
        width=4.23,
        height=5.10,
        title=right_title,
        items=insights,
        tag="KEY INSIGHTS",
        accent_color=BRAND_SAGE,
        header_bg=BRAND_SLATE
    )
    
    add_footer(slide, 1, TOTAL_SLIDES)


# ==============================================================================
# Slide Chart 0: Overview Radar Chart
# ==============================================================================
def build_slide_chart_0_overview_radar(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    insights = [
        "跨維度代差級躍升：從傳統架構平均 14.2 分躍升至 OWASP 縱深防禦架構 96.8 分，徹底消除任一節點單點破防之災難性後果。",
        "沙盒隔離填補真空：傳統架構在工具微沙盒 (5分) 與意圖錨定 (10分) 幾近完全不設防，是目前全球 Agentic 應用最核心受駭破口。",
        "不可否認全鏈審計：引入密碼學不可抹除日誌，提供 99.0 分高完備度，完全滿足金融支付與國防機敏環境之嚴格監管合規要求。",
        "雙向閉環全面加固：兼顧入向 Prompt 注入防禦與出向資料洩漏洗滌，建構「預設不信任、執行必審查」之零信任閉環防線。"
    ]
    
    _add_chart_slide(
        slide,
        title="圖 0-1 企業 AI 護欄體系六維防護能力雷達評估對比",
        category="護欄能力基準",
        subtitle="六維核心指標：語意過濾、意圖錨定、動態身分、微沙盒隔離、檢索增強與全鏈路審計",
        chart_filename="chart_0_overview_radar.png",
        right_title="防護能力量化評估矩陣",
        insights=insights
    )


# ==============================================================================
# Slide Chart 1: LLM Dual-Axis Chart
# ==============================================================================
def build_slide_chart_1_llm_dual_axis(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    insights = [
        "注入與洩漏雙高峰：Prompt 注入 (28.4%) 與機敏洩漏 (21.6%) 合占半壁江山 (50.0%)，為 L2 模型護欄最關鍵的防護重心。",
        "延遲投資報酬極佳：Prompt 注入攔截之模型推理開銷僅 +15ms，以極低延遲代價換取最大安全收益，性價比極高。",
        "輸出審查開銷顯著：過度依賴 (+35ms) 與邊界擴張 (+40ms) 因涉及多輪語意推論與事實查核，為系統延遲的主要瓶頸。",
        "輕量過濾推至閘道：組態缺失與 DoS 防禦應推至 L1 API 閘道處理 (+2~4ms)，避免消耗昂貴的大模型推論資源。"
    ]
    
    _add_chart_slide(
        slide,
        title="圖 1-1 全球 10 大 LLM 風險發生率與護欄延遲開銷雙軸指標對比",
        category="LLM 量化分析圖",
        subtitle="雙軸呈現：左軸為全球事件發生比例 (%)，右軸為護欄服務端到端延遲開銷 (ms)",
        chart_filename="chart_1_llm_dual_axis.png",
        right_title="LLM 護欄效能與開銷權衡",
        insights=insights
    )


# ==============================================================================
# Slide Chart 2: Agentic Scatter / Quadrant Chart
# ==============================================================================
def build_slide_chart_2_agentic_scatter(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    insights = [
        "意圖漂移高發威脅：ASI01 佔全體事件 24.5% 且日均告警達 142 次，必須透過數位簽名 System Prompt 與 FSM 強制約束規劃路徑。",
        "沙盒防線成效顯著：工具沙盒逃逸 (99.1%) 與不可逆操作 (99.8%) 阻斷成功率極高，證明 gVisor 微容器防護極為堅實可靠。",
        "認知欺瞞防禦攻堅：認知對抗阻斷率僅 85.0%，顯示單純自然語言提示詞難以抵抗多輪話術偽裝，需引入隔離的 Supervisor 獨立仲裁。",
        "級聯崩潰熔斷看門狗：多代理協同阻斷率 89.3%，必須在跨代理網格強制設置最大跳數 (Max Hop=8) 與重試死迴圈熔斷器。"
    ]
    
    _add_chart_slide(
        slide,
        title="圖 2-1 Agentic 10 大威脅事件佔比 vs. 護欄阻斷成功率矩陣散佈圖",
        category="Agentic 四象限矩陣",
        subtitle="四象限分析：橫軸為事件發生佔比 (%)，縱軸為阻斷成功率 (%)，氣泡大小對應每日告警頻率",
        chart_filename="chart_2_agentic_scatter.png",
        right_title="Agentic 威脅態勢與防禦攻堅",
        insights=insights
    )


# ==============================================================================
# Slide Chart 3: Skills Horizontal Bar Chart
# ==============================================================================
def build_slide_chart_3_skills_horizontal(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    insights = [
        "未限制調用高居榜首：AST01 佔全體風險 31.2%，凸顯嚴格定義 Tool Schema 與參數白名單校驗為代理人防護第一要務。",
        "容器隔離阻斷率卓越：微沙盒環境阻斷代碼執行 (99.4%) 與環境滲透 (98.8%)，且誤報率均壓制在 0.8% 以下，成效斐然。",
        "輸出洗滌挑戰最高：不受信輸出阻斷率 92.0% 且誤報率達 2.5%，需改採 XML 語意隔離與純文本降級策略徹底杜絕二次注入。",
        "動態身分打破死結：60 秒 JIT 短效 Token 使機敏憑證外洩攔截率達 99.1%，徹底破解「機敏憑證+外網+不可信語料」致命三要素。"
    ]
    
    _add_chart_slide(
        slide,
        title="圖 3-1 Skills 工具沙盒 10 大風險分佈與防禦阻斷率對比分析",
        category="Skills 沙盒指標圖",
        subtitle="橫向柱狀分析：風險分佈佔比 (%) 與微沙盒環境實際防禦阻斷成功率 (%) 精準對標",
        chart_filename="chart_3_skills_horizontal.png",
        right_title="Skills 威脅分佈與沙盒效能",
        insights=insights
    )


# ==============================================================================
# Slide Chart 4: RAG Grouped Bar Chart
# ==============================================================================
def build_slide_chart_4_rag_grouped(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    insights = [
        "提示詞注入污染最深：RAG03 雖然發生率為 18.2%，但一旦破防將造成高達 55.0% 召回文檔污染，必須前置隔離過濾。",
        "投毒與越權合占半壁：向量庫投毒 (26.8%) 與越權檢索 (23.4%) 合占 50.2%，向量資料庫多租戶物理與命名空間隔離為關鍵防線。",
        "對抗擾動衝擊最高：維度對抗擾動 (RAG06) 召回污染率達 62.0%，顯示單純向量相似度無法辨識微小特徵擾動，需輔以困惑度檢測。",
        "前置強制過濾排查：嚴格實施 Pre-Filtering 帶入 TenantID 與安全標籤，杜絕 Post-Filtering 導致之未授權文檔記憶體側漏。"
    ]
    
    _add_chart_slide(
        slide,
        title="圖 4-1 RAG 檢索增強管線 10 大風險佔比 vs. 召回污染衝擊率對比",
        category="RAG 檢索衝擊矩陣",
        subtitle="雙色柱狀對比：深藍柱為風險發生佔比 (%)，赤陶柱為突破後召回結果污染衝擊率 (%)",
        chart_filename="chart_4_rag_grouped.png",
        right_title="RAG 風險佔比與污染衝擊評析",
        insights=insights
    )


# ==============================================================================
# Slide Chart 5: MITRE ATLAS Kill Chain Funnel & Radar Chart
# ==============================================================================
def build_slide_chart_5_atlas_killchain(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    insights = [
        "防禦規避突破率最高：TA0007 入侵成功率達 45.2%，傳統靜態特徵匹配難以應對對抗性編碼與語意偽裝，需仰賴多層語意檢測模型。",
        "終端衝擊攔截率最高：影響衝擊階段 (TA0030) 攔截率達 99.2%，嚴格工具微沙盒與人工在環 (HITL) 確保了最後底線安全。",
        "梯次防禦漏斗效應：攻擊頻率沿漏斗遞減（初始存取 29.5% 降至終端衝擊 0.6%），充分驗證多層次縱深防禦之梯次阻斷效益。",
        "憑證存取固若金湯：JIT 短效 Token 與身分經紀使 TA0008 攔截率達 98.1%，將憑證竊取之入侵成功率成功壓制在 18% 以下。"
    ]
    
    _add_chart_slide(
        slide,
        title="圖 5-1 MITRE ATLAS AI 攻擊鏈 10 大戰術階段防禦攔截率全景圖",
        category="ATLAS 攻擊鏈全景",
        subtitle="組合分析：柱狀為攻擊發生頻率 (%)，綠線為護欄防禦攔截率 (%)，紅虛線為實際入侵成功率 (%)",
        chart_filename="chart_5_atlas_killchain.png",
        right_title="ATLAS 戰術階段防禦全景洞察",
        insights=insights
    )
