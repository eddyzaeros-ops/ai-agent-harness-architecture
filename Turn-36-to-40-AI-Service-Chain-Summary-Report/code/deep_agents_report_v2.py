#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep Agents 16 章心得報告.pptx — 科技感重設計版
設計原則：
  - 字型層次：標題 28→副標 14→卡片標 13→內文 11→細節 9
  - 每頁左側強調色邊條 + 標題區 + 內容區三段式
  - 卡片間距統一，呼吸感充足
  - 深藍底 + 漸層卡片 + 金色重點 + 彩色標籤
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import sys

if sys.platform == "win32":
    try: sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
    except: pass

# ─── Palette ───
BG        = RGBColor(0x0A, 0x0F, 0x1E)   # 極深藍黑
CARD      = RGBColor(0x12, 0x1A, 0x2E)   # 深藍卡片
CARD_L    = RGBColor(0x18, 0x22, 0x3A)   # 淺藍卡片
HEADER_BG = RGBColor(0x0E, 0x14, 0x28)   # 標題區底
ACCENT    = RGBColor(0x00, 0xB4, 0xD8)   # 科技青
ACCENT2   = RGBColor(0x48, 0xCA, 0xE4)   # 亮青
GOLD      = RGBColor(0xFF, 0xD6, 0x00)   # 金
ORANGE    = RGBColor(0xFF, 0x8C, 0x42)   # 橙
WHITE     = RGBColor(0xF0, 0xF4, 0xF8)   # 微暖白
LGRAY     = RGBColor(0xB0, 0xBC, 0xCC)   # 淺灰
DGRAY     = RGBColor(0x5A, 0x6A, 0x7E)   # 暗灰
GREEN     = RGBColor(0x2E, 0xCC, 0x71)   # 綠
RED       = RGBColor(0xEF, 0x53, 0x50)   # 紅
TEAL      = RGBColor(0x1A, 0xBC, 0x9C)   # 藍綠
PURPLE    = RGBColor(0xBB, 0x86, 0xFC)   # 紫
BLUE_A    = RGBColor(0x42, 0xA5, 0xF5)   # 藍
PINK      = RGBColor(0xF4, 0x8F, 0xB1)   # 粉

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW = prs.slide_width
FONT = "Microsoft JhengHei"
TS = 18

# ─── Helpers ───
def bg(s):
    s.background.fill.solid(); s.background.fill.fore_color.rgb = BG

def shape(s, tp, l, t, w, h, fc, bc=None, bw=Pt(0)):
    sh = s.shapes.add_shape(tp, l, t, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = fc
    if bc: sh.line.color.rgb = bc; sh.line.width = bw
    else: sh.line.fill.background()
    sh.shadow.inherit = False; return sh

def R(s,l,t,w,h,fc,bc=None,bw=Pt(0)):  return shape(s, MSO_SHAPE.RECTANGLE, l,t,w,h,fc,bc,bw)
def RR(s,l,t,w,h,fc,bc=None,bw=Pt(0)): return shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, l,t,w,h,fc,bc,bw)

def T(s, l, t, w, h, txt, fs=11, c=WHITE, b=False, a=PP_ALIGN.LEFT, va=MSO_ANCHOR.TOP):
    bx = s.shapes.add_textbox(l, t, w, h)
    tf = bx.text_frame; tf.word_wrap = True; tf.auto_size = None
    try: tf.vertical_anchor = va
    except: pass
    p = tf.paragraphs[0]; p.text = txt; p.font.size = Pt(fs)
    p.font.color.rgb = c; p.font.bold = b; p.font.name = FONT; p.alignment = a
    return bx

def ML(s, l, t, w, h, lines, ls=1.35):
    bx = s.shapes.add_textbox(l, t, w, h)
    tf = bx.text_frame; tf.word_wrap = True
    for i,(txt,c,b,fs) in enumerate(lines):
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.text = txt; p.font.size = Pt(fs); p.font.color.rgb = c; p.font.bold = b
        p.font.name = FONT; p.space_after = Pt(2); p.line_spacing = Pt(fs*ls)
    return bx

def ST(sh, txt, fs=11, c=WHITE, b=False, a=PP_ALIGN.CENTER):
    tf = sh.text_frame; tf.word_wrap = True
    try: tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    except: pass
    tf.paragraphs[0].alignment = a
    p = tf.paragraphs[0]; p.text = txt; p.font.size = Pt(fs); p.font.color.rgb = c; p.font.bold = b; p.font.name = FONT

def header(s, num, title, subtitle="", accent=ACCENT):
    """標準頁面框架：頂部金線 + 左側色條 + 標題 + 副標"""
    R(s, Inches(0), Inches(0), SW, Inches(0.04), GOLD)
    R(s, Inches(0), Inches(7.46), SW, Inches(0.04), GOLD)
    R(s, Inches(0), Inches(0.04), Inches(0.06), Inches(7.42), accent)   # 左邊條
    T(s, Inches(0.5), Inches(0.25), Inches(10), Inches(0.55), f"{num}  {title}", 26, WHITE, True)
    if subtitle:
        T(s, Inches(0.5), Inches(0.78), Inches(12), Inches(0.35), subtitle, 12, LGRAY, False)
    T(s, Inches(12.0), Inches(7.1), Inches(1.2), Inches(0.3), f"{num.replace('  ','').replace('—','').strip()[:2] if num else ''}", 9, DGRAY, False, PP_ALIGN.RIGHT)

def sn(s, n):
    T(s, Inches(12.3), Inches(7.1), Inches(1), Inches(0.3), f"{n}/{TS}", 9, DGRAY, False, PP_ALIGN.RIGHT)

def divider(s, y, w=Inches(12.5), x=Inches(0.4)):
    R(s, x, y, w, Inches(0.01), DGRAY)

# ============================================================
# SLIDE 1: 封面
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
R(s, Inches(0), Inches(0), SW, Inches(0.05), GOLD)
R(s, Inches(0), Inches(7.45), SW, Inches(0.05), GOLD)
# 中央大標
T(s, Inches(0.8), Inches(1.6), Inches(11.5), Inches(1.0),
  "Deep Agents 實戰", 48, WHITE, True, PP_ALIGN.CENTER)
T(s, Inches(0.8), Inches(2.6), Inches(11.5), Inches(0.6),
  "16 章深度研讀心得報告", 28, ACCENT2, True, PP_ALIGN.CENTER)
R(s, Inches(4.5), Inches(3.4), Inches(4.3), Inches(0.03), ACCENT)
T(s, Inches(0.8), Inches(3.7), Inches(11.5), Inches(0.5),
  "LangChain DeepAgents v0.7  ·  從架構哲學到企業級安全治理", 16, LGRAY, False, PP_ALIGN.CENTER)

# 16 章標籤 — 四列四行
ch_names = ["Ch01 Harness", "Ch02 快速上手", "Ch03 VFS", "Ch04 規劃",
            "Ch05 子Agent", "Ch06 非同步", "Ch07 Skills", "Ch08 記憶",
            "Ch09 HITL", "Ch10 沙箱", "Ch11 權限", "Ch12 MCP",
            "Ch13 量規", "Ch14 串流", "Ch15 直譯器", "Ch16 動態"]
ch_colors = [BLUE_A]*4 + [TEAL]*4 + [ORANGE]*4 + [PURPLE]*4
for i, (cn, cc) in enumerate(zip(ch_names, ch_colors)):
    x = Inches(2.0) + Inches((i%4)*2.4)
    y = Inches(4.6) + Inches((i//4)*0.5)
    b = RR(s, x, y, Inches(2.1), Inches(0.38), CARD, cc, Pt(1))
    ST(b, cn, 9, cc, True)

T(s, Inches(0.8), Inches(6.7), Inches(11.5), Inches(0.4),
  "Claude Opus 4.6 (Thinking)  ·  2026-09-13", 12, DGRAY, False, PP_ALIGN.CENTER)
sn(s, 1)

# ============================================================
# SLIDE 2: 目錄
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "", "研讀心得目錄", "")
T(s, Inches(0.5), Inches(0.25), Inches(6), Inches(0.5), "研讀心得目錄", 28, WHITE, True)

toc = [
    ("01","三層架構與 Context Engineering","Ch01-02",BLUE_A),
    ("02","虛擬檔案系統 (VFS)","Ch03",BLUE_A),
    ("03","任務規劃與中間件體系","Ch04",BLUE_A),
    ("04","子 Agent 委派與隔離","Ch05-06",TEAL),
    ("05","Skills + 長期記憶","Ch07-08",TEAL),
    ("06","HITL 人機協作安全閘門","Ch09",ORANGE),
    ("07","沙箱執行與檔案權限","Ch10-11",ORANGE),
    ("08","MCP 標準協議","Ch12",ORANGE),
    ("09","評分量規品質閉環","Ch13",PURPLE),
    ("10","串流可觀測 + 直譯器 PTC","Ch14-15",PURPLE),
    ("11","動態子 Agent 元編排","Ch16",PURPLE),
    ("12","架構全景 · 國防映射 · 結論","綜合",GOLD),
]
for i, (num, title, ref, clr) in enumerate(toc):
    col = Inches(0.5) if i < 6 else Inches(7.0)
    row = Inches(1.3) + Inches((i if i<6 else i-6)*0.93)
    R(s, col, row, Inches(0.06), Inches(0.7), clr)  # 色條
    RR(s, col+Inches(0.15), row, Inches(5.6), Inches(0.7), CARD)
    T(s, col+Inches(0.3), row+Inches(0.05), Inches(0.4), Inches(0.3), num, 14, clr, True)
    T(s, col+Inches(0.8), row+Inches(0.05), Inches(4.5), Inches(0.3), title, 13, WHITE, True)
    T(s, col+Inches(0.8), row+Inches(0.38), Inches(4.5), Inches(0.25), ref, 10, DGRAY, False)
sn(s, 2)

# ============================================================
# SLIDE 3: 三層架構
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "01", "三層架構哲學 — Runtime · Framework · Harness", "Ch01-02｜從 Prompt Stuffing 到 Context Engineering 的範式轉移", BLUE_A)

layers_data = [
    ("Runtime", "LangGraph", BLUE_A,
     "持久化執行引擎 · 圖排程\n斷點恢復 · 串流 · 人機協作原語"),
    ("Framework", "LangChain 1.0", TEAL,
     "標準化模型抽象 · 工具介面\nAgent 循環 · 中間件支持"),
    ("Harness", "DeepAgents v0.7", ORANGE,
     "虛擬檔案系統 · 任務規劃中間件\n子 Agent 調度 · 長期記憶 Store"),
]
for i, (layer, name, clr, desc) in enumerate(layers_data):
    y = Inches(1.3) + Inches(i*1.45)
    RR(s, Inches(0.5), y, Inches(5.5), Inches(1.3), CARD, clr, Pt(1.5))
    R(s, Inches(0.5), y, Inches(0.08), Inches(1.3), clr)
    badge = RR(s, Inches(0.8), y+Inches(0.2), Inches(1.6), Inches(0.9), clr)
    ST(badge, f"{layer}\n({name})", 11, WHITE, True)
    ML(s, Inches(2.6), y+Inches(0.2), Inches(3.2), Inches(0.9),
       [(ln, LGRAY, False, 11) for ln in desc.split("\n")], 1.5)

# 右側心得
RR(s, Inches(6.3), Inches(1.3), Inches(6.7), Inches(5.5), CARD, GOLD, Pt(1.5))
R(s, Inches(6.3), Inches(1.3), Inches(0.08), Inches(5.5), GOLD)
T(s, Inches(6.6), Inches(1.5), Inches(6), Inches(0.3), "💡 核心心得", 16, GOLD, True)
divider(s, Inches(1.9), Inches(6.1), Inches(6.6))
ML(s, Inches(6.6), Inches(2.1), Inches(6.1), Inches(4.5), [
    ("為何還需要 Harness？", WHITE, True, 13),
    ("三巨頭產品 (Cursor, Claude Code, Manus) 共同驗證了同一套模式：\nVFS + Todo + SubAgent + Memory。\nDeepAgents 將這些共性模式沉澱為開箱即用的底座。", LGRAY, False, 10),
    ("", WHITE, False, 5),
    ("Context Engineering 三大優勢", WHITE, True, 13),
    ("• 終結上下文溢位 — 超過 20K token 自動卸載至 VFS\n• 抵禦注意力稀釋 — 降低 Prompt Injection 風險\n• 模型無關性 — 支持 100+ 模型，消除供應商鎖定", LGRAY, False, 10),
    ("", WHITE, False, 5),
    ("v0.7 三大進化", WHITE, True, 13),
    ("• 基礎 Prompt 留白 → 業務完全自主注入\n• TodoList 按需啟用 → 輕量場景省 Token\n• Backend 顯式實例 → 消除隱式工廠副作用", LGRAY, False, 10),
], 1.3)
sn(s, 3)

# ============================================================
# SLIDE 4: VFS
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "02", "虛擬檔案系統 (VFS) — Context Engineering 核心", "Ch03｜Deep Agents 最具工業價值的創新點", BLUE_A)

# 7 tools row
tools = ["ls", "read_file", "write_file", "edit_file", "delete", "glob", "grep"]
for i, t in enumerate(tools):
    x = Inches(0.5) + Inches(i*1.8)
    b = RR(s, x, Inches(1.3), Inches(1.6), Inches(0.5), ACCENT)
    ST(b, t, 11, WHITE, True)

# Left: 雙重防線
RR(s, Inches(0.5), Inches(2.1), Inches(6.0), Inches(4.7), CARD, TEAL, Pt(1.5))
R(s, Inches(0.5), Inches(2.1), Inches(0.07), Inches(4.7), TEAL)
T(s, Inches(0.8), Inches(2.3), Inches(5.5), Inches(0.3), "雙重防線 — 上下文永不爆炸", 15, GOLD, True)
divider(s, Inches(2.7), Inches(5.5), Inches(0.8))
ML(s, Inches(0.8), Inches(2.9), Inches(5.5), Inches(3.5), [
    ("防線一：大結果自動卸載", TEAL, True, 12),
    ("工具輸出 > 20,000 tokens → 自動落盤至 VFS\n對話僅保留「檔案路徑 + 前 10 行預覽」\nAgent 後續用 read_file(offset, limit) 分頁讀取", LGRAY, False, 10),
    ("", WHITE, False, 5),
    ("防線二：對話歷史自動摘要", ORANGE, True, 12),
    ("上下文達模型窗口 85% → 觸發結構化摘要\n舊對話轉儲至 VFS，摘要替換歷史\ntodos 作為結構化狀態始終完整保留", LGRAY, False, 10),
], 1.4)

# Right: 五種 Backend
RR(s, Inches(6.8), Inches(2.1), Inches(6.2), Inches(4.7), CARD, PURPLE, Pt(1.5))
R(s, Inches(6.8), Inches(2.1), Inches(0.07), Inches(4.7), PURPLE)
T(s, Inches(7.1), Inches(2.3), Inches(5.5), Inches(0.3), "五種可插拔 Backend（策略模式）", 15, GOLD, True)
divider(s, Inches(2.7), Inches(5.7), Inches(7.1))
bk = [
    ("StateBackend", "預設，存於 LangGraph State", BLUE_A),
    ("FilesystemBackend", "讀寫宿主磁碟 (virtual_mode 防穿越)", TEAL),
    ("LocalShellBackend", "⚠️ 繼承 FS + execute（高風險）", RED),
    ("StoreBackend", "跨會話持久化，namespace 隔離租戶", PURPLE),
    ("CompositeBackend", "混合路由：前綴 → 不同 Backend", GOLD),
]
for i, (name, desc, clr) in enumerate(bk):
    y = Inches(2.95) + Inches(i*0.7)
    R(s, Inches(7.1), y, Inches(0.05), Inches(0.5), clr)
    T(s, Inches(7.3), y, Inches(2.2), Inches(0.25), name, 12, clr, True)
    T(s, Inches(7.3), y+Inches(0.28), Inches(5.3), Inches(0.25), desc, 10, LGRAY, False)
sn(s, 4)

# ============================================================
# SLIDE 5: 中間件
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "03", "任務規劃與中間件三層體系", "Ch04｜中間件是 Harness 治理的核心骨幹", BLUE_A)

# Left: TodoList
RR(s, Inches(0.5), Inches(1.3), Inches(5.8), Inches(2.8), CARD, TEAL, Pt(1.5))
R(s, Inches(0.5), Inches(1.3), Inches(0.07), Inches(2.8), TEAL)
T(s, Inches(0.8), Inches(1.4), Inches(5.2), Inches(0.3), "TodoListMiddleware — 北極星錨點", 14, GOLD, True)
ML(s, Inches(0.8), Inches(1.9), Inches(5.2), Inches(2.0), [
    ("三狀態機", TEAL, True, 12),
    ("pending → in_progress → completed", ACCENT2, False, 11),
    ("長程任務歷史被壓縮歸檔時，todos 仍完整保留\n→ Agent 經歷「失憶」後仍掌握全局目標", LGRAY, False, 10),
    ("v0.7 改為按需啟用，簡單任務可省略", ORANGE, False, 10),
], 1.4)

# Hook 比較
RR(s, Inches(0.5), Inches(4.4), Inches(5.8), Inches(2.7), CARD, ACCENT, Pt(1.5))
R(s, Inches(0.5), Inches(4.4), Inches(0.07), Inches(2.7), ACCENT)
T(s, Inches(0.8), Inches(4.5), Inches(5.2), Inches(0.3), "Node-style vs Wrap-style Hook", 14, GOLD, True)
ML(s, Inches(0.8), Inches(5.0), Inches(5.2), Inches(1.8), [
    ("✅ Node-style（節點級）", GREEN, True, 11),
    ("before/after_agent · before/after_model\n圖中斷點明確 → interrupt() 的最佳位置", LGRAY, False, 10),
    ("", WHITE, False, 3),
    ("⚠️ Wrap-style（包裹級）", RED, True, 11),
    ("wrap_model_call · wrap_tool_call\n適合重試/快取 → 嚴禁作為人工審批邊界", LGRAY, False, 10),
], 1.35)

# Right: 三層中間件
RR(s, Inches(6.6), Inches(1.3), Inches(6.4), Inches(5.8), CARD, BLUE_A, Pt(1.5))
R(s, Inches(6.6), Inches(1.3), Inches(0.07), Inches(5.8), BLUE_A)
T(s, Inches(6.9), Inches(1.4), Inches(5.8), Inches(0.3), "中間件三層全景", 15, GOLD, True)
divider(s, Inches(1.8), Inches(5.8), Inches(6.9))

mw_layers = [
    ("第一層：框架預設（自動）", BLUE_A, [
        "FilesystemMiddleware — 注入 7 個檔案工具 + 權限",
        "SummarizationMiddleware — 上下文壓縮",
        "PatchToolCallsMiddleware — 工具呼叫修補",
    ]),
    ("第二層：條件啟動（參數驅動）", TEAL, [
        "subagents= → SubAgentMiddleware",
        "skills= → SkillsMiddleware",
        "memory= → MemoryMiddleware",
        "interrupt_on= → HumanInTheLoopMiddleware",
    ]),
    ("第三層：應用選配（手動裝配）", ORANGE, [
        "TodoListMiddleware 規劃 · PIIMiddleware 脫敏",
        "ToolRetryMW / ModelFallbackMW 韌性",
        "ToolCallLimitMW 防死迴圈暴衝",
    ]),
]
y = Inches(2.0)
for name, clr, items in mw_layers:
    R(s, Inches(6.9), y, Inches(5.8), Inches(0.04), clr)
    T(s, Inches(6.9), y+Inches(0.1), Inches(5.8), Inches(0.3), name, 12, clr, True)
    y += Inches(0.45)
    for item in items:
        T(s, Inches(7.1), y, Inches(5.5), Inches(0.25), "▸ " + item, 10, LGRAY, False)
        y += Inches(0.3)
    y += Inches(0.15)
sn(s, 5)

# ============================================================
# SLIDE 6: SubAgent
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "04", "子 Agent 委派 — 上下文隔離與非同步編排", "Ch05-06｜Context Quarantine 是 Token 防火牆", TEAL)

RR(s, Inches(0.5), Inches(1.3), Inches(6.0), Inches(2.8), CARD, TEAL, Pt(1.5))
R(s, Inches(0.5), Inches(1.3), Inches(0.07), Inches(2.8), TEAL)
T(s, Inches(0.8), Inches(1.4), Inches(5.4), Inches(0.3), "同步子 Agent — 上下文隔離", 14, GOLD, True)
ML(s, Inches(0.8), Inches(1.9), Inches(5.4), Inches(2.0), [
    ("父 Agent = 專案經理 · 子 Agent = 專責執行者", TEAL, True, 11),
    ("子 Agent 中間工具輸出完全隔離\n父 Agent 僅收到精煉摘要 → Token 防火牆", LGRAY, False, 10),
    ("", WHITE, False, 3),
    ("繼承語意", WHITE, True, 11),
    ("model/interrupt_on → 預設繼承，可覆寫\ntools/permissions → 若指定則完整替換（非合併）\nsystem_prompt/middleware → 永不繼承", LGRAY, False, 10),
], 1.35)

RR(s, Inches(6.8), Inches(1.3), Inches(6.2), Inches(2.8), CARD, ORANGE, Pt(1.5))
R(s, Inches(6.8), Inches(1.3), Inches(0.07), Inches(2.8), ORANGE)
T(s, Inches(7.1), Inches(1.4), Inches(5.6), Inches(0.3), "非同步子 Agent — 背景平行", 14, GOLD, True)
ML(s, Inches(7.1), Inches(1.9), Inches(5.6), Inches(2.0), [
    ("五大編排工具", ORANGE, True, 11),
    ("start_async_task → 啟動背景任務\ncheck_async_task → 查詢狀態\nupdate_async_task → 注入新指令\ncancel_async_task → 中止執行\nlist_async_tasks → 聚合所有狀態", LGRAY, False, 10),
], 1.35)

RR(s, Inches(0.5), Inches(4.4), Inches(12.5), Inches(2.7), CARD, PURPLE, Pt(1.5))
R(s, Inches(0.5), Inches(4.4), Inches(0.07), Inches(2.7), PURPLE)
T(s, Inches(0.8), Inches(4.5), Inches(8), Inches(0.3), "💡 心得：異質模型分層 × 成本最佳化", 14, GOLD, True)
ML(s, Inches(0.8), Inches(5.0), Inches(12), Inches(1.8), [
    ("• 簡單查詢 → 7B 免費模型（成本 ≈ 0）  ·  複雜推理 → 旗艦模型 (GLM-5.2 / Claude / Gemini)", LGRAY, False, 11),
    ("• response_format (Pydantic Schema) → 確保下游 API 可靠消費", LGRAY, False, 11),
    ("• CompiledSubAgent 可包裝任意 LangGraph DAG → 既有工作流無縫接入 Deep Agents", LGRAY, False, 11),
], 1.4)
sn(s, 6)

# ============================================================
# SLIDE 7: Skills + Memory
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "05", "Skills 能力包與長期記憶", "Ch07-08｜漸進式披露是效率之鑰；記憶是 Agent 進化的基石", TEAL)

RR(s, Inches(0.5), Inches(1.3), Inches(6.0), Inches(5.7), CARD, TEAL, Pt(1.5))
R(s, Inches(0.5), Inches(1.3), Inches(0.07), Inches(5.7), TEAL)
T(s, Inches(0.8), Inches(1.4), Inches(5.4), Inches(0.3), "Skills — 跨平台能力包", 14, GOLD, True)
divider(s, Inches(1.8), Inches(5.4), Inches(0.8))
ML(s, Inches(0.8), Inches(1.95), Inches(5.4), Inches(5.0), [
    ("漸進式披露（Progressive Disclosure）", TEAL, True, 12),
    ("L1 元資料：僅載入 name + description（~百 tokens）\nL2 指令：匹配後才載入 SKILL.md 全文\nL3 資源：scripts/references 按需讀取", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("開放標準 Agent Skills Specification", BLUE_A, True, 12),
    ("相容 30+ 平台（Claude Code, Cursor, Codex...）\n目錄：SKILL.md + scripts/ + references/ + assets/", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("層疊優先（Last Wins）", ORANGE, True, 12),
    ("skills=[org/, team/, project/]\n企業基線 → 團隊 → 專案客製（後者覆寫前者）", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("安全防護", RED, True, 12),
    ("mode='deny' → 企業 SOP 不可被改寫\nmode='interrupt' → 修改需人工審批", LGRAY, False, 10),
], 1.35)

RR(s, Inches(6.8), Inches(1.3), Inches(6.2), Inches(5.7), CARD, PURPLE, Pt(1.5))
R(s, Inches(6.8), Inches(1.3), Inches(0.07), Inches(5.7), PURPLE)
T(s, Inches(7.1), Inches(1.4), Inches(5.6), Inches(0.3), "長期記憶 — 跨會話持久化", 14, GOLD, True)
divider(s, Inches(1.8), Inches(5.6), Inches(7.1))
ML(s, Inches(7.1), Inches(1.95), Inches(5.6), Inches(5.0), [
    ("三個作用域", PURPLE, True, 12),
    ("Agent-Scoped：共享知識庫 / AGENTS.md\nUser-Scoped：個人偏好 / 專案上下文\nOrg-Scoped：企業政策（唯讀）", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("進階能力", TEAL, True, 12),
    ("情節記憶：搜索歷史 Checkpoint 回想過去解法\n背景整合：Cron 觸發冷路徑去重沉澱穩定記憶", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("💡 核心洞見", GOLD, True, 12),
    ("記憶即檔案\n用 read / edit / write_file 操作記憶\n比複雜向量 DB 查詢 Prompt 大幅降低認知負擔", ACCENT2, False, 11),
], 1.35)
sn(s, 7)

# ============================================================
# SLIDE 8: HITL
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "06", "HITL 人機協作 — 安全閘門設計", "Ch09｜四種決策 + 五條避坑規則 = 企業級審批安全基石", ORANGE)

dec_data = [
    ("approve ✅", GREEN, "批准原始工具呼叫"),
    ("edit ✏️", TEAL, "修改參數後執行"),
    ("reject ❌", RED, "拒絕 + 告知原因"),
    ("respond 💬", BLUE_A, "直接回覆（僅互動工具）"),
]
for i, (name, clr, desc) in enumerate(dec_data):
    x = Inches(0.5) + Inches(i*3.2)
    RR(s, x, Inches(1.3), Inches(2.9), Inches(1.3), CARD, clr, Pt(1.5))
    T(s, x+Inches(0.15), Inches(1.45), Inches(2.6), Inches(0.35), name, 15, clr, True, PP_ALIGN.CENTER)
    T(s, x+Inches(0.15), Inches(1.9), Inches(2.6), Inches(0.5), desc, 11, LGRAY, False, PP_ALIGN.CENTER)

RR(s, Inches(0.5), Inches(2.9), Inches(12.5), Inches(4.2), CARD, ORANGE, Pt(1.5))
R(s, Inches(0.5), Inches(2.9), Inches(0.07), Inches(4.2), ORANGE)
T(s, Inches(0.8), Inches(3.0), Inches(8), Inches(0.3), "⚠️ 底層 interrupt() 五條避坑規則", 15, GOLD, True)
divider(s, Inches(3.4), Inches(12), Inches(0.8))
rules = [
    ("01", "嚴禁裸 try...except Exception 包裹 interrupt()，會吞噬中斷異常"),
    ("02", "interrupt() 之前的副作用必須設計為冪等操作（重放語意）"),
    ("03", "禁止動態改變 interrupt() 呼叫順序（索引匹配機制）"),
    ("04", "多分支並行中斷需基於 Interrupt.id 建立映射恢復"),
    ("05", "輸入驗證應採「單次中斷 + 條件邊回環」，避免 while True 重跑堆疊"),
]
for i, (num, desc) in enumerate(rules):
    y = Inches(3.6) + Inches(i*0.65)
    b = RR(s, Inches(0.8), y, Inches(0.5), Inches(0.45), ORANGE)
    ST(b, num, 13, WHITE, True)
    T(s, Inches(1.5), y+Inches(0.08), Inches(11), Inches(0.35), desc, 12, LGRAY, False)
sn(s, 8)

# ============================================================
# SLIDE 9: Sandbox + Permissions
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "07", "沙箱執行與檔案權限 — 縱深防禦雙軌", "Ch10-11｜Sandbox-as-Tool 是推薦模式；權限預設 ALLOW 必須兜底 DENY", ORANGE)

RR(s, Inches(0.5), Inches(1.3), Inches(6.0), Inches(5.7), CARD, TEAL, Pt(1.5))
R(s, Inches(0.5), Inches(1.3), Inches(0.07), Inches(5.7), TEAL)
T(s, Inches(0.8), Inches(1.4), Inches(5.4), Inches(0.3), "沙箱執行 Ch10", 14, GOLD, True)
divider(s, Inches(1.8), Inches(5.4), Inches(0.8))
ML(s, Inches(0.8), Inches(1.95), Inches(5.4), Inches(4.5), [
    ("兩種模式", TEAL, True, 12),
    ("❌ Agent-in-Sandbox → API Key 在容器內 (高風險)", RED, False, 10),
    ("✅ Sandbox-as-Tool → 推理留宿主，僅執行遠端呼叫", GREEN, False, 10),
    ("", WHITE, False, 4),
    ("雙平面設計", BLUE_A, True, 12),
    ("Agent 工具平面 → 沙箱內 (read/write/execute)\n宿主應用平面 → upload/download (SDK 通道)", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("安全邊界", RED, True, 12),
    ("✅ 保護：宿主檔案 / 環境變數 / 進程\n❌ 不防：Prompt Injection 誘導沙箱內有害動作\n❌ 不防：出站網路資料外傳（須配合斷網）", LGRAY, False, 10),
], 1.35)

RR(s, Inches(6.8), Inches(1.3), Inches(6.2), Inches(5.7), CARD, ORANGE, Pt(1.5))
R(s, Inches(6.8), Inches(1.3), Inches(0.07), Inches(5.7), ORANGE)
T(s, Inches(7.1), Inches(1.4), Inches(5.6), Inches(0.3), "檔案權限 Ch11", 14, GOLD, True)
divider(s, Inches(1.8), Inches(5.6), Inches(7.1))
ML(s, Inches(7.1), Inches(1.95), Inches(5.6), Inches(4.5), [
    ("⚠️ 預設行為 = ALLOW！", RED, True, 13),
    ("只寫 allow /workspace/** 不是白名單\n必須以 deny /** 兜底！", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("正確配置順序", TEAL, True, 12),
    ("1. deny .env → 敏感文件保護\n2. allow /workspace/** → 工作區放行\n3. deny /** → 全域兜底拒絕", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("🔴 防護邊界（極重要）", RED, True, 12),
    ("FilesystemPermission 僅保護內建檔案工具！\n完全不保護：自訂工具、MCP、沙箱 execute\n→ 系統設計必須多軌並行防禦", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("mode='interrupt' → 聯動 HITL 審批", PURPLE, True, 11),
], 1.35)
sn(s, 9)

# ============================================================
# SLIDE 10: MCP
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "08", "MCP 標準協議 — 擴展 Agent 工具生態", "Ch12｜MCP 是 Agent 連接企業微服務的「USB 協議」", ORANGE)

RR(s, Inches(0.5), Inches(1.3), Inches(12.5), Inches(1.0), CARD, ACCENT, Pt(1))
T(s, Inches(0.8), Inches(1.5), Inches(12), Inches(0.5),
  "Deep Agents (編排) → LangChain Tool (介面) → mcp-adapters (轉換) → MultiServerMCPClient (網路) → MCP Server (業務)", 12, ACCENT2, True, PP_ALIGN.CENTER)

cols_data = [
    ("三項能力邊界", TEAL,
     "Tools → 轉為 StructuredTool，直接可用\nResources → 需應用手動拉取\nPrompts → 需手動拉取，不自動注入"),
    ("傳輸協議選型", ORANGE,
     "stdio → 本地開發（⚠️ 嚴禁 print）\nhttp (Streamable HTTP) → 生產首選\n支持 Bearer Header / OAuth"),
    ("關鍵安全考量", RED,
     "• Token/憑證由 Client 注入，嚴禁暴露給模型\n• FilesystemPermission 無法攔截 MCP 工具\n• Session 不存入 Checkpoint\n• 帶副作用工具須支持冪等"),
]
for i, (title, clr, desc) in enumerate(cols_data):
    x = Inches(0.5) + Inches(i*4.2)
    RR(s, x, Inches(2.6), Inches(3.9), Inches(4.3), CARD, clr, Pt(1.5))
    R(s, x, Inches(2.6), Inches(0.07), Inches(4.3), clr)
    T(s, x+Inches(0.2), Inches(2.7), Inches(3.5), Inches(0.3), title, 14, GOLD, True)
    divider(s, Inches(3.1), Inches(3.5), x+Inches(0.2))
    ML(s, x+Inches(0.2), Inches(3.3), Inches(3.5), Inches(3.3),
       [(ln, LGRAY, False, 10) for ln in desc.split("\n")], 1.5)
sn(s, 10)

# ============================================================
# SLIDE 11: Grading Rubrics
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "09", "評分量規 — AI 品質自動驗收閉環", "Ch13｜解耦「生成結束」與「通過驗收」是品質保證的關鍵", PURPLE)

roles_data = [("Working Agent", BLUE_A), ("Rubric", TEAL), ("Grader Agent", ORANGE), ("Evidence Tool", GREEN)]
for i, (name, clr) in enumerate(roles_data):
    x = Inches(0.5) + Inches(i*3.2)
    b = RR(s, x, Inches(1.3), Inches(2.9), Inches(0.6), clr)
    ST(b, name, 13, WHITE, True)

RR(s, Inches(0.5), Inches(2.2), Inches(6.0), Inches(4.7), CARD, RED, Pt(1.5))
R(s, Inches(0.5), Inches(2.2), Inches(0.07), Inches(4.7), RED)
T(s, Inches(0.8), Inches(2.3), Inches(5.4), Inches(0.3), "Fail-Closed 驗收門", 14, GOLD, True)
divider(s, Inches(2.7), Inches(5.4), Inches(0.8))
ML(s, Inches(0.8), Inches(2.85), Inches(5.4), Inches(3.8), [
    ("僅在 result == 'satisfied' 時放行", RED, True, 13),
    ("", WHITE, False, 3),
    ("satisfied — 全部標準通過 ✅", GREEN, False, 11),
    ("needs_revision — 未達標，注入 gap 重試 🔄", ORANGE, False, 11),
    ("max_iterations_reached — 超出預算停止 ⛔", RED, False, 11),
    ("failed / grader_error — 異常停止 🚫", RED, False, 11),
    ("", WHITE, False, 3),
    ("⚠️ 單純有最終文本消息一律視為未達標", GOLD, True, 11),
], 1.4)

RR(s, Inches(6.8), Inches(2.2), Inches(6.2), Inches(4.7), CARD, PURPLE, Pt(1.5))
R(s, Inches(6.8), Inches(2.2), Inches(0.07), Inches(4.7), PURPLE)
T(s, Inches(7.1), Inches(2.3), Inches(5.6), Inches(0.3), "💡 Actor-Critic 閉環迴圈", 14, GOLD, True)
divider(s, Inches(2.7), Inches(5.6), Inches(7.1))
ML(s, Inches(7.1), Inches(2.85), Inches(5.6), Inches(3.8), [
    ("生成 → 確定性取證 → 差距診斷 → 再生成", ACCENT2, True, 12),
    ("", WHITE, False, 4),
    ("• Working Model 與 Grader Model 可異質配比\n  （工作用程式碼大模型，裁判用推理模型）", LGRAY, False, 10),
    ("• 取證工具僅供 Grader 使用，嚴格隔離", LGRAY, False, 10),
    ("• 生產須將 RubricEvaluation 接入離線評測\n  統計首輪通過率與修訂成本", LGRAY, False, 10),
], 1.5)
sn(s, 11)

# ============================================================
# SLIDE 12: Streaming + PTC
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "10", "串流可觀測性與直譯器 PTC", "Ch14-15｜消除黑盒轉圈 + 削減 80% Token 消耗", PURPLE)

RR(s, Inches(0.5), Inches(1.3), Inches(6.0), Inches(5.7), CARD, BLUE_A, Pt(1.5))
R(s, Inches(0.5), Inches(1.3), Inches(0.07), Inches(5.7), BLUE_A)
T(s, Inches(0.8), Inches(1.4), Inches(5.4), Inches(0.3), "Streaming v3 Typed Projection", 14, GOLD, True)
divider(s, Inches(1.8), Inches(5.4), Inches(0.8))
ML(s, Inches(0.8), Inches(1.95), Inches(5.4), Inches(4.5), [
    ("五大根級投影", BLUE_A, True, 12),
    ("stream.messages — 主 Agent 消息\nstream.tool_calls — 工具呼叫增量\nstream.subagents — 子 Agent 句柄\nstream.values — 狀態快照\nstream.output — 最終輸出", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("工具呼叫三態判定", ORANGE, True, 12),
    ("not completed → running\nerror is not None → failed\ncompleted && no error → completed", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("並發消費", TEAL, True, 12),
    ("asyncio.gather() 或 interleave()\n避免串行導致時序顛倒", LGRAY, False, 10),
], 1.35)

RR(s, Inches(6.8), Inches(1.3), Inches(6.2), Inches(5.7), CARD, ORANGE, Pt(1.5))
R(s, Inches(6.8), Inches(1.3), Inches(0.07), Inches(5.7), ORANGE)
T(s, Inches(7.1), Inches(1.4), Inches(5.6), Inches(0.3), "Interpreters — PTC 效率革命", 14, GOLD, True)
divider(s, Inches(1.8), Inches(5.6), Inches(7.1))
ML(s, Inches(7.1), Inches(1.95), Inches(5.6), Inches(4.5), [
    ("普通 vs PTC", ORANGE, True, 12),
    ("普通：80 筆 = 80 輪 LLM 往返 → 上下文爆炸\nPTC：一次 eval(JS) → Promise.all 並發\n→ 記憶體過濾 → 僅返回聚合摘要", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("三種狀態模式", TEAL, True, 12),
    ("call — 每次 eval 銷毀（最隔離）\nturn — 同回合共享變數\nthread — Snapshot 跨輪持久化", LGRAY, False, 10),
    ("", WHITE, False, 4),
    ("🔴 安全警示", RED, True, 12),
    ("• QuickJS 非記憶體隔離沙箱\n• PTC 不觸發 HITL 審批！\n  高危操作嚴禁加入白名單\n• 四道防線：timeout / memory_limit\n  / max_ptc_calls / max_result_chars", LGRAY, False, 10),
], 1.35)
sn(s, 12)

# ============================================================
# SLIDE 13: Dynamic Subagents
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "11", "動態子 Agent — 用程式碼編排多角色協作", "Ch16｜LLM 充當工作流架構師，動態生成編排腳本", PURPLE)

patterns_data = [
    ("分類後分流", BLUE_A, "Classifier 打標\n→ 按映射表路由\n→ 專責 Agent 處理"),
    ("並行扇出 + 對抗複核", TEAL, "Promise.all 並發審查\n→ 去重合併候選\n→ Verifier 獨立證偽"),
    ("迭代收斂搜索", ORANGE, "循環搜索直到無新增\n→ 增量去重\n→ 硬性安全輪次上限"),
]
for i, (name, clr, desc) in enumerate(patterns_data):
    x = Inches(0.5) + Inches(i*4.2)
    RR(s, x, Inches(1.3), Inches(3.9), Inches(2.2), CARD, clr, Pt(1.5))
    R(s, x, Inches(1.3), Inches(0.07), Inches(2.2), clr)
    b = RR(s, x+Inches(0.2), Inches(1.45), Inches(3.5), Inches(0.4), clr)
    ST(b, name, 12, WHITE, True)
    T(s, x+Inches(0.2), Inches(2.0), Inches(3.5), Inches(1.2), desc, 10, LGRAY, False, PP_ALIGN.CENTER)

# Bottom two cards
RR(s, Inches(0.5), Inches(3.8), Inches(6.0), Inches(3.2), CARD, RED, Pt(1.5))
R(s, Inches(0.5), Inches(3.8), Inches(0.07), Inches(3.2), RED)
T(s, Inches(0.8), Inches(3.9), Inches(5.4), Inches(0.3), "🔴 安全關鍵考量", 14, GOLD, True)
ML(s, Inches(0.8), Inches(4.4), Inches(5.4), Inches(2.2), [
    ("Agent Fork Bomb 風險", RED, True, 12),
    ("max_ptc_calls 僅限 tools.* 呼叫\n不限制 task() 啟動數量！\n防禦：Prompt 邊界 + timeout + Token 配額", LGRAY, False, 10),
    ("", WHITE, False, 3),
    ("無級聯審批", ORANGE, True, 12),
    ("動態代碼中批量子 Agent 預設無 HITL\n外部寫入必須維持強管控", LGRAY, False, 10),
], 1.35)

RR(s, Inches(6.8), Inches(3.8), Inches(6.2), Inches(3.2), CARD, GREEN, Pt(1.5))
R(s, Inches(6.8), Inches(3.8), Inches(0.07), Inches(3.2), GREEN)
T(s, Inches(7.1), Inches(3.9), Inches(5.6), Inches(0.3), "💡 架構演化最前沿", 14, GOLD, True)
ML(s, Inches(7.1), Inches(4.4), Inches(5.6), Inches(2.2), [
    ("融合「程式碼確定性」與「LLM 推理靈活性」", GREEN, True, 12),
    ("• 從 Prompt 猜測 → 程式碼確定性編排\n• 100% 輸入覆蓋，杜絕遺漏\n• 對模型要求極高（需精通非同步 JS）\n• 必須集成 LangSmith 捕獲父子 Span 樹", LGRAY, False, 10),
], 1.35)
sn(s, 13)

# ============================================================
# SLIDE 14: 四軌聯防
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "12", "企業級縱深防禦 — 四軌聯防體系", "綜合心得｜單一機制無法覆蓋所有攻擊面，必須多軌並行", GOLD)

tracks = [
    ("FilesystemPermission", "Ch11", BLUE_A, "✅ 虛擬檔案路徑控制\n✅ read/write 操作攔截", "❌ 不保護 MCP 工具\n❌ 不保護沙箱 execute\n❌ 不保護自訂工具"),
    ("Sandbox", "Ch10", TEAL, "✅ 不可信程式碼隔離\n✅ 宿主進程防護\n✅ 雙平面設計", "❌ 不防 Prompt Injection\n❌ 不防網路外傳\n❌ 不防沙箱內有害操作"),
    ("MCP + Interceptor", "Ch12", ORANGE, "✅ 企業微服務安全接入\n✅ 憑證注入 + ACL\n✅ 工具命名前綴防衝突", "❌ Session 不存 Checkpoint\n❌ 須自身實現冪等\n❌ stdio 有進程權限風險"),
    ("HITL", "Ch09", RED, "✅ 終極人工決策閘門\n✅ 跨工具/路徑/流程\n✅ 審批可跨天恢復", "❌ 需 Checkpointer 持久化\n❌ PTC 呼叫不觸發\n❌ 動態子 Agent 無級聯"),
]
for i, (name, ch, clr, covers, limits) in enumerate(tracks):
    x = Inches(0.5) + Inches(i*3.2)
    RR(s, x, Inches(1.3), Inches(3.0), Inches(5.7), CARD, clr, Pt(1.5))
    R(s, x, Inches(1.3), Inches(3.0), Inches(0.6), clr)
    T(s, x, Inches(1.4), Inches(3.0), Inches(0.4), f"{name}\n{ch}", 11, WHITE, True, PP_ALIGN.CENTER)
    T(s, x+Inches(0.15), Inches(2.1), Inches(2.7), Inches(0.2), "覆蓋", 11, GREEN, True)
    ML(s, x+Inches(0.15), Inches(2.4), Inches(2.7), Inches(2.0),
       [(ln, LGRAY, False, 9) for ln in covers.split("\n")], 1.5)
    T(s, x+Inches(0.15), Inches(4.6), Inches(2.7), Inches(0.2), "不保護", 11, RED, True)
    ML(s, x+Inches(0.15), Inches(4.9), Inches(2.7), Inches(2.0),
       [(ln, LGRAY, False, 9) for ln in limits.split("\n")], 1.5)
sn(s, 14)

# ============================================================
# SLIDE 15: 成熟度
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "13", "16 章成熟度與完備性總評", "", GOLD)

ch_eval = [
    ("Ch01 Harness", "高", BLUE_A), ("Ch02 快速上手", "高", BLUE_A),
    ("Ch03 VFS", "極高 ★", BLUE_A), ("Ch04 規劃", "極高 ★", BLUE_A),
    ("Ch05 子 Agent", "生產就緒", TEAL), ("Ch06 非同步", "Preview", TEAL),
    ("Ch07 Skills", "高", TEAL), ("Ch08 記憶", "高", TEAL),
    ("Ch09 HITL", "高", ORANGE), ("Ch10 沙箱", "工業級", ORANGE),
    ("Ch11 權限", "成熟", ORANGE), ("Ch12 MCP", "高", ORANGE),
    ("Ch13 量規", "Beta", PURPLE), ("Ch14 串流", "生產就緒", PURPLE),
    ("Ch15 直譯器", "Beta", PURPLE), ("Ch16 動態", "Beta", PURPLE),
]
for i, (ch, mat, clr) in enumerate(ch_eval):
    col = Inches(0.5) + Inches((i%4)*3.2)
    row = Inches(1.3) + Inches((i//4)*1.4)
    RR(s, col, row, Inches(3.0), Inches(1.2), CARD, clr, Pt(1))
    R(s, col, row, Inches(0.07), Inches(1.2), clr)
    T(s, col+Inches(0.2), row+Inches(0.15), Inches(1.8), Inches(0.3), ch, 12, WHITE, True)
    b = RR(s, col+Inches(0.2), row+Inches(0.55), Inches(1.5), Inches(0.4), clr)
    ST(b, mat, 11, WHITE, True)
sn(s, 15)

# ============================================================
# SLIDE 16: 國防映射
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "14", "Deep Agents × 國防 AI 服務鏈映射", "將 16 章技術能力映射至五大原則與六節點縱深防禦", GOLD)

map_data = [
    ("模型分層", BLUE_A, "Ch01 三層堆疊 → L1~L5\nCh05 異質模型分層\n→ 成本最佳化路由"),
    ("資料分級", TEAL, "Ch03 VFS 路徑隔離\nCh11 Permission 分級\n→ Backend 路由控管"),
    ("單一閘道", ORANGE, "Ch12 MCP 統一聚合\nCh04 中間件管道\n→ Gateway 入口"),
    ("層層防護", PURPLE, "Ch09 HITL + Ch10 沙箱\nCh11 權限 + Ch13 量規\n→ fail-closed 閘門"),
    ("全程留痕", GREEN, "Ch08 記憶持久化\nCh14 串流可觀測\n→ LangSmith 追蹤"),
]
for i, (p, clr, desc) in enumerate(map_data):
    x = Inches(0.5) + Inches(i*2.55)
    RR(s, x, Inches(1.3), Inches(2.35), Inches(5.5), CARD, clr, Pt(1.5))
    R(s, x, Inches(1.3), Inches(2.35), Inches(0.55), clr)
    T(s, x, Inches(1.4), Inches(2.35), Inches(0.35), p, 15, WHITE, True, PP_ALIGN.CENTER)
    ML(s, x+Inches(0.15), Inches(2.05), Inches(2.05), Inches(4.0),
       [(ln, LGRAY, False, 10) for ln in desc.split("\n")], 1.6)
sn(s, 16)

# ============================================================
# SLIDE 17: 十大洞見
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
header(s, "15", "十大關鍵洞見", "400KB · 16 章技術文件的精華濃縮", GOLD)

insights_data = [
    ("01","Context Engineering 是 Agent 成敗的分水嶺", BLUE_A),
    ("02","Harness 是「裝配齊全的工坊」，非 Framework", BLUE_A),
    ("03","中間件三層體系實現全面非業務功能解耦", TEAL),
    ("04","Context Quarantine 是 Token 防火牆", TEAL),
    ("05","Skills 三層懶載入避免上下文飽和", TEAL),
    ("06","記憶即檔案 — 簡潔而強大的介面", ORANGE),
    ("07","HITL 五條規則是血淚教訓", ORANGE),
    ("08","FilesystemPermission 預設 ALLOW 是陷阱", RED),
    ("09","PTC 削減 80% Token 但繞過 HITL", RED),
    ("10","動態子 Agent — 最前沿但最危險", PURPLE),
]
for i, (num, txt, clr) in enumerate(insights_data):
    col = Inches(0.5) if i < 5 else Inches(6.8)
    row = Inches(1.3) + Inches((i if i<5 else i-5)*1.15)
    RR(s, col, row, Inches(6.0), Inches(0.95), CARD, clr, Pt(1))
    R(s, col, row, Inches(0.07), Inches(0.95), clr)
    b = RR(s, col+Inches(0.2), row+Inches(0.2), Inches(0.55), Inches(0.55), clr)
    ST(b, num, 14, WHITE, True)
    T(s, col+Inches(0.9), row+Inches(0.25), Inches(5), Inches(0.5), txt, 12, WHITE, True)
sn(s, 17)

# ============================================================
# SLIDE 18: 結論
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
R(s, Inches(0), Inches(0), SW, Inches(0.05), GOLD)
R(s, Inches(0), Inches(7.45), SW, Inches(0.05), GOLD)
R(s, Inches(0), Inches(0.05), Inches(0.08), Inches(7.4), GOLD)

T(s, Inches(0.5), Inches(0.3), Inches(12), Inches(0.5),
  "結論 — Deep Agents 是國防 AI Agent 客製化 Harness 的最佳底座", 24, WHITE, True)

RR(s, Inches(0.5), Inches(1.1), Inches(12.5), Inches(5.8), CARD, GOLD, Pt(1.5))
R(s, Inches(0.5), Inches(1.1), Inches(0.07), Inches(5.8), GOLD)

ML(s, Inches(0.9), Inches(1.3), Inches(11.8), Inches(5.2), [
    ("一、架構哲學的價值", GOLD, True, 15),
    ("Deep Agents v0.7 將 Agent 工業落地的共性模式沉澱為開箱即用的底座。\n"
     "三層架構 (Runtime → Framework → Harness) 精準對應我們\n"
     "國防 AI 服務鏈的 L1 基礎模型 → L3 Agent → L4 Skill 的模型分層原則。", LGRAY, False, 11),
    ("", WHITE, False, 5),
    ("二、安全治理的啟示", GOLD, True, 15),
    ("16 章反覆強調：沒有單一銀彈。\n"
     "FilesystemPermission 不保護 MCP、沙箱不防 Prompt Injection、\n"
     "PTC 繞過 HITL、動態子 Agent 無 max_task_calls。\n"
     "唯有四軌聯防才能構建縱深防禦 — 與我們「層層防護」原則完全一致。", LGRAY, False, 11),
    ("", WHITE, False, 5),
    ("三、落地策略建議", GOLD, True, 15),
    ("• 行政庶務 Agent → 開箱即用 Harness (Claude Code / Codex / AGY 2.0)\n"
     "• 武器系統 Agent → Deep Agents 客製化底座 + 四級沙箱 + 多層 HITL + SBOM\n"
     "• 統一經 AI Gateway (中間件管道) 接入 → 單一閘道 + 全程留痕\n"
     "• Skills 開放規範確保跨平台共享；長期記憶 Store 實現知識持續進化", LGRAY, False, 11),
    ("", WHITE, False, 5),
    ("Deep Agents 不只是一個框架，而是 Agent 工業化生產的成熟方法論。", ACCENT2, True, 14),
], 1.3)

for i, (p, c) in enumerate(zip(["模型分層","資料分級","單一閘道","層層防護","全程留痕"],
                               [BLUE_A, TEAL, ORANGE, PURPLE, GREEN])):
    b = RR(s, Inches(1.6)+Inches(i*2.1), Inches(7.15), Inches(1.8), Inches(0.25), c)
    ST(b, p, 10, WHITE, True)
sn(s, 18)

# ─── Speaker Notes ───
notes_map = {
1: "封面。Deep Agents v0.7 共 16 章約 400KB 技術文件的深度研讀心得。以 Claude Opus 4.6 Thinking 模式進行研析，並行 4 個研究子代理同時閱讀。",
2: "目錄。12 個主題從架構哲學到國防映射。建議依關注面向選擇性深入。",
3: "三層架構。為何需要 Harness？Context Engineering 三大優勢。v0.7 三大進化。",
4: "VFS 是最具工業價值的創新。雙重防線確保上下文永不爆炸。五種可插拔 Backend。",
5: "中間件三層體系。TodoList 北極星錨點。Node-style vs Wrap-style Hook 區分。",
6: "子 Agent Context Quarantine = Token 防火牆。異質模型分層策略。非同步五大編排工具。",
7: "Skills 漸進式披露三層懶載入。長期記憶三個作用域。核心洞見：記憶即檔案。",
8: "HITL 四種決策。五條避坑規則（每條都是實戰踩坑的血淚教訓）。",
9: "沙箱 Sandbox-as-Tool 推薦模式。檔案權限預設 ALLOW 陷阱。防護邊界極重要。",
10: "MCP = Agent 的 USB 協議。三項能力邊界。傳輸選型。安全考量。",
11: "評分量規四方職責解耦。Fail-Closed 驗收門。Actor-Critic 閉環迴圈。",
12: "串流 v3 消除黑盒。PTC 削減 80% Token。安全警示：QuickJS 非隔離沙箱、不觸發 HITL。",
13: "動態子 Agent 三大範式。Fork Bomb 風險。架構演化最前沿方向。",
14: "四軌聯防：權限+沙箱+MCP+HITL。每軌都有明確的覆蓋範圍與不保護範圍。",
15: "16 章成熟度總評。Ch03 VFS 與 Ch04 中間件達「極高」。Ch13/15/16 為 Beta。",
16: "五大原則與 16 章技術的精準映射。設計哲學高度契合國防安全治理。",
17: "十大關鍵洞見。400KB 文件的精華濃縮。每一條可展開為獨立技術討論。",
18: "結論。架構哲學價值。安全治理啟示（四軌聯防）。落地策略建議（雙軌 + Gateway）。Deep Agents 是 Agent 工業化生產的成熟方法論。",
}
for num, text in notes_map.items():
    prs.slides[num-1].notes_slide.notes_text_frame.text = text

# ─── Save ───
out = r"D:\JavaDO\Harness\Deep Agents\MD\心得報告_v2.pptx"
# Overwrite with the tech-aesthetic version
prs.save(out)
print(f"✅ 科技感重設計版已生成：{out}")
print(f"   共 {TS} 頁 · 含備忘稿")
