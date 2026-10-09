import os
from PIL import Image, ImageDraw, ImageFont

def generate_perfect_killchain_infographic():
    src_path = "C:/Users/calsa/.gemini/antigravity/brain/48a4c0f2-8114-4ba4-b208-8d216674689f/uav_f2t2ea_infographic_1789390679129.jpg"
    out_dirs = [
        "D:/JavaDO/Harness/Deep Agents/assets",
        "D:/Obsidian/MyVault/Harness/AI Agent Framework Analysis Report/assets"
    ]
    for d in out_dirs:
        os.makedirs(d, exist_ok=True)
        
    img_orig = Image.open(src_path).convert("RGB")
    orig_w, orig_h = img_orig.size # (1376, 768)
    
    # 4K 畫布配置 (3840 x 2160)
    canvas_w, canvas_h = 3840, 2160
    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    
    # 版面空間分配：
    # 頂部 Header: y: 35 ~ 170 (高度 135px)
    # 中間原始英文圖（無遮擋、無覆蓋）:
    # 設原圖高度 = 1380px -> 寬度 = 1380 * (1376/768) = 2472px
    # 置中 img_x = (3840 - 2472) // 2 = 684
    # 原圖 y: 175 ~ 1555
    # 下方獨立中文說明區：
    # 左右外邊距: 60px (總寬度 3720px，填滿左、下、右空白處)
    # y: 1580 ~ 2125 (高度 545px)
    # 6 欄卡片：寬度每欄 (3720 - 5 * 20) / 6 = 603px
    
    img_disp_h = 1380
    img_disp_w = int(img_disp_h * (orig_w / orig_h)) # 2472
    img_scaled = img_orig.resize((img_disp_w, img_disp_h), Image.Resampling.LANCZOS)
    
    img_x = (canvas_w - img_disp_w) // 2 # 684
    img_y = 175
    canvas.paste(img_scaled, (img_x, img_y))
    
    draw = ImageDraw.Draw(canvas)
    
    font_bold = "C:/Windows/Fonts/msjhbd.ttc"
    font_reg = "C:/Windows/Fonts/msjh.ttc"
    
    f_title = ImageFont.truetype(font_bold, 62)
    f_sub = ImageFont.truetype(font_reg, 32)
    f_card_badge = ImageFont.truetype(font_bold, 26)
    f_card_title = ImageFont.truetype(font_bold, 34)
    f_card_sub = ImageFont.truetype(font_bold, 26)
    f_card_desc = ImageFont.truetype(font_bold, 28) # 採用粗體 28px，清晰度極致銳利！
    
    # 1. 頂部 Header
    title_text = "無人機 F2T2EA 自主擊殺鏈戰術代理 ： 全流程架構圖"
    sub_text = "Deep Agents 邊緣架構  |  雙光電感測融合  |  Anduril Lattice 聯合指管  |  雙重 MITL 授權  |  安全沙箱與 BDA 評估"
    
    tb = draw.textbbox((0, 0), title_text, font=f_title)
    draw.text(((canvas_w - (tb[2] - tb[0])) // 2, 40), title_text, fill=(15, 23, 42), font=f_title)
    
    sb = draw.textbbox((0, 0), sub_text, font=f_sub)
    draw.text(((canvas_w - (sb[2] - sb[0])) // 2, 118), sub_text, fill=(2, 132, 199), font=f_sub)
    
    # 分隔線 (貫穿全寬)
    draw.line([(60, 165), (3780, 165)], fill=(226, 232, 240), width=2)
    
    # 2. 底部獨立說明專區
    footer_x_start = 60
    footer_total_w = 3840 - (60 * 2) # 3720px
    card_gap = 20
    card_w = (footer_total_w - card_gap * 5) // 6 # (3720 - 100) // 6 = 603px
    footer_y = 1575
    card_h = 550
    
    stages_info = [
        {
            "tag": "F - FIND 尋獲",
            "name": "模型隔離與感測融合",
            "steps": "步驟 1 & 步驟 2",
            "bullets": [
                "• L3 容器沙箱環境安全隔離",
                "• 記憶狀態管理防目標漂移",
                "• EO/IR 雙光電子代理感測",
                "• 邊緣特徵融合建立即時 COP"
            ],
            "accent": (2, 132, 199)
        },
        {
            "tag": "F - FIX 定位",
            "name": "Lattice 聯合方案生成",
            "steps": "步驟 3",
            "bullets": [
                "• 透過標準 MCP 呼叫指管核心",
                "• Lattice Menace-T 戰術引擎",
                "• 結合威脅時序動態推演",
                "• 即時生成 3 組作戰方案 COA"
            ],
            "accent": (14, 165, 233)
        },
        {
            "tag": "T - TRACK 跟蹤",
            "name": "零信任阻斷與人機確認",
            "steps": "步驟 4 & 步驟 5 (Gate 1)",
            "bullets": [
                "• ABAC 護欄阻斷跨級雷達查詢",
                "• 攔截越權 (403 Forbidden)",
                "• 全鏈路 SOC 留痕安全稽核",
                "• MITL Gate 1: 作戰官核准方案"
            ],
            "accent": (13, 148, 136)
        },
        {
            "tag": "T - TARGET 標定",
            "name": "飛控引導與雷射鎖定",
            "steps": "步驟 5-2 & 步驟 6",
            "bullets": [
                "• 長期記憶 ROE 規則生效確認",
                "• 飛控系統調整安全飛行姿態",
                "• 切入 042° 走廊持續動態跟蹤",
                "• PRF 1688 編碼雷射照準鎖定"
            ],
            "accent": (99, 102, 241)
        },
        {
            "tag": "E - ENGAGE 交戰",
            "name": "終端打擊與武器釋放",
            "steps": "步驟 7 (Gate 2)",
            "bullets": [
                "• MITL Gate 2: 終端武器釋放審批",
                "• 雙人密鑰認證防範自主失控",
                "• 點火出架釋放精準巡飛彈",
                "• 終端俯衝精確突防打擊目標"
            ],
            "accent": (239, 68, 68)
        },
        {
            "tag": "A - ASSESS 評估",
            "name": "戰損評估與 AAR 存證",
            "steps": "步驟 8 & 步驟 9",
            "bullets": [
                "• 紅外熱斑檢測與發動機殉爆",
                "• 評定 DS-1 徹底摧毀 (Catastrophic)",
                "• CDE 附帶損傷評估為 0 公尺",
                "• 生成 AAR 報告與後量子密鑰留痕"
            ],
            "accent": (217, 119, 6)
        }
    ]
    
    for idx, info in enumerate(stages_info):
        cx = footer_x_start + idx * (card_w + card_gap)
        cy = footer_y
        
        # 卡片底色 (微淺灰底 + 雙像素精緻邊框)
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=16, fill=(248, 250, 252), outline=(203, 213, 225), width=2)
        
        # 頂部色彩條
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + 10], radius=4, fill=info["accent"])
        
        # 標籤 Badge (動態測量，大字體 26px)
        tb_badge = draw.textbbox((0, 0), info["tag"], font=f_card_badge)
        badge_text_w = tb_badge[2] - tb_badge[0]
        badge_w = badge_text_w + 28
        badge_h = 42
        draw.rounded_rectangle([cx + 20, cy + 24, cx + 20 + badge_w, cy + 24 + badge_h], radius=8, fill=info["accent"])
        draw.text((cx + 34, cy + 29), info["tag"], fill=(255, 255, 255), font=f_card_badge)
        
        # 標題與步數 (大字體 34px / 26px)
        draw.text((cx + 20, cy + 82), info["name"], fill=(15, 23, 42), font=f_card_title)
        draw.text((cx + 20, cy + 130), info["steps"], fill=info["accent"], font=f_card_sub)
        
        # 分隔線
        draw.line([(cx + 20, cy + 172), (cx + card_w - 20, cy + 172)], fill=(226, 232, 240), width=2)
        
        # 條列內文 (大字體 28px，行距 70px)
        line_y = cy + 195
        for b in info["bullets"]:
            draw.text((cx + 20, line_y), b, fill=(30, 41, 59), font=f_card_desc)
            line_y += 72
            
    # 儲存 4K 版
    out_4k_path = "D:/JavaDO/Harness/Deep Agents/assets/uav_f2t2ea_killchain_infographic_4k.jpg"
    canvas.save(out_4k_path, "JPEG", quality=96)
    print(f"Saved 4K balanced infographic: {out_4k_path}")
    
    # 儲存 HD 版 (1920x1080)
    canvas_hd = canvas.resize((1920, 1080), Image.Resampling.LANCZOS)
    out_hd_path = "D:/JavaDO/Harness/Deep Agents/assets/uav_f2t2ea_killchain_infographic.jpg"
    canvas_hd.save(out_hd_path, "JPEG", quality=92)
    print(f"Saved HD balanced infographic: {out_hd_path}")
    
    # 同步至 Obsidian
    obs_4k = "D:/Obsidian/MyVault/Harness/AI Agent Framework Analysis Report/assets/uav_f2t2ea_killchain_infographic_4k.jpg"
    canvas.save(obs_4k, "JPEG", quality=96)
    print(f"Synced to Obsidian: {obs_4k}")

if __name__ == "__main__":
    generate_perfect_killchain_infographic()
