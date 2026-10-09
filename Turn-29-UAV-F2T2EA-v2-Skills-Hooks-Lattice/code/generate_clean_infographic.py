import os
from PIL import Image, ImageDraw, ImageFont

def generate_clean_annotated_infographic():
    src_path = "C:/Users/calsa/.gemini/antigravity/brain/48a4c0f2-8114-4ba4-b208-8d216674689f/uav_f2t2ea_v2_harness_architecture_1790380871313.jpg"
    out_dir = "D:/JavaDO/Harness/Deep Agents/v2/assets"
    os.makedirs(out_dir, exist_ok=True)
    
    img_orig = Image.open(src_path).convert("RGB")
    orig_w, orig_h = img_orig.size # (1376, 768)
    
    # 畫布尺寸：3840 x 2160 (4K UHD)
    canvas_w, canvas_h = 3840, 2160
    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    
    # 版面空間分配：
    # 頂部 Header: y = 30 ~ 170 (高度 140px)
    # 中間主圖區: y = 175 ~ 1705 (高度 1530px，原圖 100% 完整保留，無任何重疊)
    # 底部說明卡片: y = 1735 ~ 2115 (高度 380px，充分展現微軟正黑體繁體中文清晰度)
    
    img_disp_h = 1530
    img_disp_w = int(img_disp_h * (orig_w / orig_h)) # 1530 * 1.7916 = 2741
    img_scaled = img_orig.resize((img_disp_w, img_disp_h), Image.Resampling.LANCZOS)
    
    img_x = (canvas_w - img_disp_w) // 2 # (3840 - 2741) // 2 = 549
    img_y = 175
    canvas.paste(img_scaled, (img_x, img_y))
    
    draw = ImageDraw.Draw(canvas)
    
    # 字體設定 (微軟正黑體 粗體與常規體)
    font_bold = "C:/Windows/Fonts/msjhbd.ttc"
    font_reg = "C:/Windows/Fonts/msjh.ttc"
    
    f_title = ImageFont.truetype(font_bold, 56)
    f_sub = ImageFont.truetype(font_reg, 28)
    f_card_badge = ImageFont.truetype(font_bold, 22)
    f_card_title = ImageFont.truetype(font_bold, 30)
    f_card_sub = ImageFont.truetype(font_bold, 22)
    f_card_desc = ImageFont.truetype(font_reg, 21)
    
    # 1. 頂部 Header
    title_text = "無人機 F2T2EA 自主擊殺鏈戰術代理 v2 ： 全架構演進圖"
    sub_text = "Agent Skills 專業能力庫  |  Lifecycle Hooks 零信任生命週期安全鉤子  |  Anduril Lattice Menace-T 戰術引擎深度模擬"
    
    tb = draw.textbbox((0, 0), title_text, font=f_title)
    draw.text(((canvas_w - (tb[2] - tb[0])) // 2, 40), title_text, fill=(15, 23, 42), font=f_title)
    
    sb = draw.textbbox((0, 0), sub_text, font=f_sub)
    draw.text(((canvas_w - (sb[2] - sb[0])) // 2, 115), sub_text, fill=(2, 132, 199), font=f_sub)
    
    # 頂部分隔淡線
    draw.line([(img_x, 162), (img_x + img_disp_w, 162)], fill=(226, 232, 240), width=2)
    
    # 2. 底部獨立說明專區
    footer_y = img_y + img_disp_h + 25 # 175 + 1530 + 25 = 1730
    card_gap = 24
    total_cards_w = img_disp_w
    card_w = (total_cards_w - card_gap * 3) // 4 # (2741 - 72) // 4 = 667
    card_h = 385
    
    blocks_info = [
        {
            "tag": "BLOCK 1",
            "name": "邊緣戰術偵察機 (Find & Fix)",
            "subtitle": "NVIDIA Jetson 雙感測子代理",
            "bullets": [
                "• EO/IR 雙子代理於 Jetson Orin NX (100 TOPS) 邊緣推論",
                "• 僅回傳時空特徵向量，頻寬消耗從 50Mbps 壓降至 <50kbps",
                "• 地面 Main Agent 進行多源異質時空融合生成即時 COP"
            ],
            "accent": (2, 132, 199)
        },
        {
            "tag": "BLOCK 2",
            "name": "安全鉤子與能力庫 (Track)",
            "subtitle": "Lifecycle Hooks & Agent Skills",
            "bullets": [
                "• PreTool 飛行包線安全檢查 (姿態攔截 roll>45° 失速)",
                "• PreTool 零信任 ABAC 攔截 (403 阻斷非授權雷達查詢)",
                "• PostTool 全鏈路 SOC 留痕 + CDE 附帶損傷評估 Skill"
            ],
            "accent": (13, 148, 136)
        },
        {
            "tag": "BLOCK 3",
            "name": "指管核心伺服器 (Target & Engage)",
            "subtitle": "Anduril Lattice Menace-T 模擬",
            "bullets": [
                "• 電磁頻譜熱圖 (EW/EMCON) 與威脅動態時序評分 (0.94)",
                "• 自動生成 3 組高勝率行動方案 (COA-1/2/3 戰術評估)",
                "• 結合長期記憶 ROE 接戰準則，自適應優選精確路徑"
            ],
            "accent": (79, 70, 229)
        },
        {
            "tag": "BLOCK 4",
            "name": "打擊型無人機 (Engage & Assess)",
            "subtitle": "MUM-T 協同與雙重 MITL 審批",
            "bullets": [
                "• MUM-T 跨平台協同：釋放 ALTIUS-600M 巡飛彈終端打擊",
                "• 雙重人機在迴路 (MITL)：目標確認核准與接戰開火授權",
                "• Tactical MANET Mesh 無中心動態加密跳頻抗干擾網路"
            ],
            "accent": (217, 119, 6)
        }
    ]
    
    for idx, info in enumerate(blocks_info):
        cx = img_x + idx * (card_w + card_gap)
        cy = footer_y
        
        # 卡片圓角白色/灰藍背景與細緻投影輪廓
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=16, fill=(248, 250, 252), outline=(203, 213, 225), width=2)
        
        # 頂部強調色條
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + 9], radius=4, fill=info["accent"])
        
        # 標籤 Badge
        badge_w, badge_h = 108, 30
        draw.rounded_rectangle([cx + 20, cy + 22, cx + 20 + badge_w, cy + 22 + badge_h], radius=6, fill=info["accent"])
        draw.text((cx + 28, cy + 26), info["tag"], fill=(255, 255, 255), font=f_card_badge)
        
        # 標題與副標題
        draw.text((cx + 20, cy + 64), info["name"], fill=(15, 23, 42), font=f_card_title)
        draw.text((cx + 20, cy + 104), info["subtitle"], fill=info["accent"], font=f_card_sub)
        
        # 細分隔線
        draw.line([(cx + 20, cy + 140), (cx + card_w - 20, cy + 140)], fill=(226, 232, 240), width=1)
        
        # 條列內文
        line_y = cy + 155
        for b in info["bullets"]:
            draw.text((cx + 20, line_y), b, fill=(30, 41, 59), font=f_card_desc)
            line_y += 46
            
    # 儲存獨立檔案：uav_f2t2ea_v2_clean_infographic_4k.jpg (3840x2160)
    out_4k_path = os.path.join(out_dir, "uav_f2t2ea_v2_clean_infographic_4k.jpg")
    canvas.save(out_4k_path, "JPEG", quality=96)
    print(f"Saved 4K clean infographic to: {out_4k_path}")
    
    # 儲存獨立檔案：uav_f2t2ea_v2_clean_infographic.jpg (1920x1080)
    canvas_hd = canvas.resize((1920, 1080), Image.Resampling.LANCZOS)
    out_hd_path = os.path.join(out_dir, "uav_f2t2ea_v2_clean_infographic.jpg")
    canvas_hd.save(out_hd_path, "JPEG", quality=92)
    print(f"Saved HD clean infographic to: {out_hd_path}")

    # 同時同步至 Obsidian 資產庫獨立檔案
    obsidian_dir = "D:/Obsidian/MyVault/Harness/AI Agent Framework Analysis Report/assets"
    if os.path.exists(obsidian_dir):
        obs_4k = os.path.join(obsidian_dir, "uav_f2t2ea_v2_clean_infographic_4k.jpg")
        canvas.save(obs_4k, "JPEG", quality=96)
        print(f"Synced to Obsidian: {obs_4k}")

if __name__ == "__main__":
    generate_clean_annotated_infographic()
