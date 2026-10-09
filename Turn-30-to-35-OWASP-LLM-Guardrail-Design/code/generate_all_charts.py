# -*- coding: utf-8 -*-
"""
generate_all_charts.py
Generate 6 publication-grade Matplotlib charts for PPTX Template 1.
Adheres strictly to Warm Editorial Minimalism color palette and typography.
Completely eliminates all text/element collisions, provides generous headroom,
and ensures all annotations have clean opaque callout boxes.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Configure fonts & styles
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Segoe UI', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.autolayout'] = False

# Color Constants (Warm Editorial Minimalism)
C_CANVAS = '#F5F2EB'
C_CARD = '#FDFCFA'
C_BORDER = '#E3DCCF'
C_DIVIDER = '#D6CEBF'
C_SAGE = '#3B6E58'
C_TERRA = '#9E5A38'
C_SLATE = '#2C3E50'
C_OCHRE = '#B4782A'
C_TEXT = '#232D38'
C_MUTED = '#7C8695'

OUTPUT_DIR = r"d:\JavaDO\OWASP html\charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_ax(ax):
    ax.set_facecolor(C_CARD)
    for spine in ax.spines.values():
        spine.set_color(C_BORDER)
        spine.set_linewidth(1.0)
    ax.tick_params(colors=C_MUTED, labelsize=8.5)
    ax.grid(True, linestyle='--', color=C_BORDER, alpha=0.65, zorder=0)

# ==============================================================================
# Chart 0: Six-Dimensional Radar Chart (Overview)
# ==============================================================================
def generate_chart_0_radar():
    fig_w = 7.30
    fig_h = 4.98
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor=C_CARD, dpi=300)
    
    # Exact 1:1 square polar axes centered in the figure -> 100% mathematically circular!
    ax_size = 3.60  # inches width and height
    ax_left = (fig_w - ax_size) / 2.0 / fig_w
    ax_bottom = 0.50 / fig_h
    ax_w = ax_size / fig_w
    ax_h = ax_size / fig_h
    
    ax = fig.add_axes([ax_left, ax_bottom, ax_w, ax_h], polar=True)
    ax.set_facecolor(C_CARD)
    
    categories = [
        '語意出入安全\n(Prompt Guard)',
        '行為意圖錨定\n(Intent & FSM)',
        '動態身分經紀\n(JIT Broker)',
        '微沙盒隔離\n(gVisor Sandbox)',
        '檢索增強防護\n(RAG Grounding)',
        '全鏈不可否認審計\n(Non-Repudiation)'
    ]
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    # Base orientation: index 0 at top (pi/2), clockwise direction
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Disable default faint gridlines so we can draw prominent custom concentric circles!
    ax.grid(False)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    
    # Draw alternating concentric circular bands & prominent ring lines (25, 50, 75, 100)
    theta_full = np.linspace(0, 2 * np.pi, 360)
    
    # 1. Alternating ring fills for high contrast & prominent concentric rings
    ax.fill_between(theta_full, 75, 100, color='#FAF8F5', alpha=0.95, zorder=0)
    ax.fill_between(theta_full, 50, 75, color='#F2EEE5', alpha=0.95, zorder=0)
    ax.fill_between(theta_full, 25, 50, color='#FAF8F5', alpha=0.95, zorder=0)
    ax.fill_between(theta_full, 0, 25, color='#F2EEE5', alpha=0.95, zorder=0)
    
    # 2. Prominent concentric circle borders (25, 50, 75, 100)
    ring_styles = [
        (25, '#B8AEA0', 1.3, '--'),
        (50, '#8A7E6E', 1.5, '-'),
        (75, '#B8AEA0', 1.3, '--'),
        (100, '#4F473E', 1.8, '-')  # 100 is solid, dark, and highly visible
    ]
    for r_val, color, lw, ls in ring_styles:
        ax.plot(theta_full, [r_val] * len(theta_full), color=color, linewidth=lw, linestyle=ls, zorder=1)
        
    # 3. Radial spokes (from center to 100)
    for ang in angles[:-1]:
        ax.plot([ang, ang], [0, 100], color='#A89D8F', linewidth=1.1, linestyle='-', zorder=1)
        
    # 4. Bold Numeric Badges on concentric circles (25, 50, 75, 100)
    badge_angle = np.pi / 4  # 45 degrees
    for val in [25, 50, 75, 100]:
        ax.text(
            badge_angle, val, f'{val}',
            ha='center', va='center', fontsize=7.8, fontweight='bold', color='#1A242F',
            bbox=dict(boxstyle='round,pad=0.22', facecolor='#FFFFFF', edgecolor='#8C8070', linewidth=0.8, alpha=0.95),
            zorder=6
        )
        
    # 5. Data Polygons
    v_unprotected = [25, 10, 15, 5, 20, 10]
    v_unprotected += v_unprotected[:1]
    
    v_basic = [65, 30, 25, 20, 45, 35]
    v_basic += v_basic[:1]
    
    v_owasp = [96, 94, 98, 99, 95, 99]
    v_owasp += v_owasp[:1]
    
    # OWASP
    ax.plot(angles, v_owasp, color=C_SAGE, linewidth=2.5, marker='o', markersize=4.5,
            label='OWASP 縱深防禦體系 (Defense-in-Depth)', zorder=4)
    ax.fill(angles, v_owasp, color=C_SAGE, alpha=0.28, zorder=3)
    
    # Basic
    ax.plot(angles, v_basic, color=C_OCHRE, linewidth=1.8, linestyle='--', marker='s', markersize=4.0,
            label='基礎防護 (Basic Guardrails)', zorder=3)
    ax.fill(angles, v_basic, color=C_OCHRE, alpha=0.14, zorder=2)
    
    # Unprotected
    ax.plot(angles, v_unprotected, color=C_TERRA, linewidth=1.5, linestyle=':', marker='^', markersize=4.0,
            label='傳統裸奔架構 (Unprotected)', zorder=2)
    ax.fill(angles, v_unprotected, color=C_TERRA, alpha=0.08, zorder=2)
    
    ax.set_ylim(0, 126)  # Generous headroom so data polygon never touches labels!
    
    # 6. Six Custom Collision-Free Category Pill Badges
    label_positions = [
        (angles[0], 122, 'center', 'bottom'),  # Top (90 deg)
        (angles[1], 124, 'left', 'center'),    # Top-Right (30 deg)
        (angles[2], 124, 'left', 'center'),    # Bottom-Right (330 deg)
        (angles[3], 120, 'center', 'top'),     # Bottom (270 deg)
        (angles[4], 124, 'right', 'center'),   # Bottom-Left (210 deg)
        (angles[5], 124, 'right', 'center')    # Top-Left (150 deg)
    ]
    
    for idx, (ang, r_dist, ha, va) in enumerate(label_positions):
        ax.text(
            ang, r_dist, categories[idx],
            ha=ha, va=va, fontsize=8.0, fontweight='bold', color=C_TEXT,
            bbox=dict(boxstyle='round,pad=0.30', facecolor='#FFFFFF', edgecolor='#C4BAA9', linewidth=0.85, alpha=0.98),
            zorder=10
        )
        
    # 7. Legend placed cleanly at the very top of figure
    legend = fig.legend(
        loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=3, frameon=True, fontsize=8.2
    )
    legend.get_frame().set_facecolor(C_CANVAS)
    legend.get_frame().set_edgecolor(C_BORDER)
    legend.get_frame().set_linewidth(0.85)
    for text in legend.get_texts():
        text.set_color(C_TEXT)
        text.set_fontweight('bold')
        
    out_path = os.path.join(OUTPUT_DIR, "chart_0_overview_radar.png")
    plt.savefig(out_path, dpi=300, facecolor=C_CARD)
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# Chart 1: Dual-Axis LLM Top 10 (Occurrence vs. Latency)
# ==============================================================================
def generate_chart_1_llm():
    fig = plt.figure(figsize=(7.5, 4.6), facecolor=C_CARD, dpi=300)
    ax1 = fig.add_axes([0.09, 0.12, 0.81, 0.74])
    setup_ax(ax1)
    
    labels = ['LLM01\n注入', 'LLM02\n洩漏', 'LLM03\n供應鏈', 'LLM04\n投毒', 'LLM05\n輸出處置', 
              'LLM06\n過度依賴', 'LLM07\n組態缺失', 'LLM08\nDoS', 'LLM09\n向量外洩', 'LLM10\n邊界擴張']
    rates = [28.4, 21.6, 14.2, 9.8, 8.5, 6.1, 4.3, 3.5, 2.1, 1.5]
    latencies = [15, 12, 5, 0, 18, 35, 2, 4, 22, 40]
    
    x = np.arange(len(labels))
    width = 0.52
    
    # Left axis: Bar for Occurrence %
    bars = ax1.bar(x, rates, width, color=C_SAGE, alpha=0.85, edgecolor=C_BORDER, linewidth=0.8, zorder=3, label='風險發生比例 (%)')
    ax1.set_ylabel('風險發生比例 (%)', color=C_SAGE, fontsize=9.2, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=C_SAGE)
    ax1.set_ylim(0, 38)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=7.8, color=C_TEXT)
    
    # Bar value labels: Inside bar if tall enough, else on top with clean background
    for bar in bars:
        h = bar.get_height()
        if h >= 10.0:
            ax1.text(bar.get_x() + bar.get_width()/2., h / 2.0, f'{h:.1f}%',
                     ha='center', va='center', fontsize=7.5, color='#FFFFFF', fontweight='bold', zorder=4)
        else:
            ax1.text(bar.get_x() + bar.get_width()/2., h + 0.8, f'{h:.1f}%',
                     ha='center', va='bottom', fontsize=7.2, color=C_SAGE, fontweight='bold', zorder=4)
        
    # Right axis: Line for Latency (ms)
    ax2 = ax1.twinx()
    ax2.set_facecolor('none')
    for spine in ax2.spines.values():
        spine.set_color(C_BORDER)
        
    ax2.plot(x, latencies, color=C_TERRA, marker='o', linewidth=2.0, markersize=5.5, label='護欄延遲開銷 (ms)', zorder=5)
    ax2.set_ylabel('護欄延遲開銷 (ms)', color=C_TERRA, fontsize=9.2, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=C_TERRA)
    ax2.set_ylim(-4, 52)
    
    # Callout badge for line points
    for i, txt in enumerate(latencies):
        offset_y = 3.0 if i != 5 else -4.2  # LLM06 put below to avoid crowding top
        ax2.annotate(
            f'+{txt}ms',
            (x[i], txt + offset_y),
            ha='center', va='center', fontsize=7.0, color=C_TERRA, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.18', facecolor='#FFF8EE', edgecolor='#9E5A38', linewidth=0.6, alpha=0.92),
            zorder=6
        )
        
    # Legend at top outside plotting area
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    legend = fig.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=2, frameon=True, fontsize=8.0)
    legend.get_frame().set_facecolor(C_CANVAS)
    legend.get_frame().set_edgecolor(C_BORDER)
    legend.get_frame().set_linewidth(0.8)
    for text in legend.get_texts():
        text.set_color(C_TEXT)
        text.set_fontweight('bold')
        
    out_path = os.path.join(OUTPUT_DIR, "chart_1_llm_dual_axis.png")
    plt.savefig(out_path, dpi=300, facecolor=C_CARD)
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# Chart 2: Agentic Scatter / Quadrant (Occurrence vs. Interception)
# ==============================================================================
def generate_chart_2_agentic():
    fig = plt.figure(figsize=(7.5, 4.6), facecolor=C_CARD, dpi=300)
    ax = fig.add_axes([0.09, 0.12, 0.88, 0.74])
    setup_ax(ax)
    
    names = ['ASI01 意圖漂移', 'ASI02 身分濫用', 'ASI03 沙盒逃逸', 'ASI04 記憶投毒', 'ASI05 級聯崩潰',
             'ASI06 認知欺瞞', 'ASI07 狀態操作', 'ASI08 迴圈 DoS', 'ASI09 影子代理', 'ASI10 技能篡改']
    shares = [24.5, 19.8, 16.2, 12.4, 8.7, 6.3, 4.8, 3.6, 2.2, 1.5]
    rates = [94.2, 98.6, 99.1, 91.5, 89.3, 85.0, 99.8, 97.4, 92.0, 96.5]
    alerts = [142, 88, 52, 65, 34, 28, 15, 42, 11, 9]
    
    # Quadrant lines
    ax.axvline(x=10.0, color=C_DIVIDER, linestyle=':', linewidth=1.2, zorder=1)
    ax.axhline(y=93.0, color=C_DIVIDER, linestyle=':', linewidth=1.2, zorder=1)
    
    # Subtle Watermark Quadrant Titles (Corners, light alpha to avoid overlap)
    ax.text(26.5, 84.0, '高發威脅 / 防禦攻堅區\n(High Risk - Challenging)', fontsize=8.0, color=C_TERRA, fontweight='bold', ha='right', va='bottom', alpha=0.45)
    ax.text(26.5, 100.4, '核心防線 / 堅實掌控區\n(High Risk - Robust)', fontsize=8.0, color=C_SAGE, fontweight='bold', ha='right', va='top', alpha=0.45)
    ax.text(0.8, 84.0, '長尾隱患 / 需防盲區\n(Long Tail - Watchlist)', fontsize=8.0, color=C_MUTED, fontweight='bold', ha='left', va='bottom', alpha=0.45)
    ax.text(0.8, 100.4, '低頻受控 / 標準沙盒區\n(Low Risk - Controlled)', fontsize=8.0, color=C_SLATE, fontweight='bold', ha='left', va='top', alpha=0.45)
    
    # Modulated bubble sizes
    colors = [C_SAGE if r >= 95 else (C_OCHRE if r >= 90 else C_TERRA) for r in rates]
    bubble_sizes = [a * 3.5 + 100 for a in alerts]
    
    ax.scatter(shares, rates, s=bubble_sizes, c=colors, alpha=0.82, edgecolors=C_BORDER, linewidth=1.0, zorder=3)
    
    # Precision collision-free offsets with clean opaque boxes
    offsets = [
        (-3.2, -1.8),  # ASI01: left-down
        (0.0, 1.4),    # ASI02: above
        (-3.0, -1.6),  # ASI03: left-down
        (0.0, -1.7),   # ASI04: below
        (-2.4, 1.3),   # ASI05: left-up
        (2.6, 0.0),    # ASI06: right
        (2.4, 0.4),    # ASI07: right-up
        (-2.0, -1.5),  # ASI08: left-down
        (2.2, 0.0),    # ASI09: right
        (2.2, -1.2)    # ASI10: right-down
    ]
    
    for i, txt in enumerate(names):
        dx, dy = offsets[i]
        ax.annotate(
            f"{txt}\n({shares[i]}%, {rates[i]}%)",
            (shares[i], rates[i]),
            xytext=(shares[i] + dx, rates[i] + dy),
            fontsize=7.0, color=C_TEXT, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.22', facecolor='#FFFFFF', edgecolor=C_BORDER, linewidth=0.7, alpha=0.92),
            arrowprops=dict(arrowstyle='->', color=C_MUTED, lw=0.6, shrinkA=3, shrinkB=4),
            zorder=5
        )
        
    ax.set_xlabel('受駭事件佔比 (%)', fontsize=9.2, fontweight='bold', color=C_TEXT)
    ax.set_ylabel('護欄阻斷成功率 (%)', fontsize=9.2, fontweight='bold', color=C_TEXT)
    ax.set_xlim(0, 28)
    ax.set_ylim(83, 101.5)
    
    # Legend at top
    dummy_high = ax.scatter([], [], c=C_SAGE, s=70, label='阻斷率 >= 95% (高度掌控)')
    dummy_mid = ax.scatter([], [], c=C_OCHRE, s=70, label='阻斷率 90%~95% (良好防禦)')
    dummy_low = ax.scatter([], [], c=C_TERRA, s=70, label='阻斷率 < 90% (重點攻堅)')
    legend = fig.legend([dummy_high, dummy_mid, dummy_low], ['阻斷率 >= 95% (高度掌控)', '阻斷率 90%~95% (良好防禦)', '阻斷率 < 90% (重點攻堅)'],
                        loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=3, frameon=True, fontsize=8.0)
    legend.get_frame().set_facecolor(C_CANVAS)
    legend.get_frame().set_edgecolor(C_BORDER)
    legend.get_frame().set_linewidth(0.8)
    for text in legend.get_texts():
        text.set_color(C_TEXT)
        text.set_fontweight('bold')
        
    out_path = os.path.join(OUTPUT_DIR, "chart_2_agentic_scatter.png")
    plt.savefig(out_path, dpi=300, facecolor=C_CARD)
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# Chart 3: Skills Horizontal Bar (Risk Share vs. Defense Rate)
# ==============================================================================
def generate_chart_3_skills():
    fig = plt.figure(figsize=(7.5, 4.6), facecolor=C_CARD, dpi=300)
    ax = fig.add_axes([0.22, 0.12, 0.74, 0.74])
    setup_ax(ax)
    
    skills = [
        'AST01 未限制工具調用', 'AST02 運行環境滲透', 'AST03 動態代碼執行', 'AST04 長期憑證濫用',
        'AST05 不受信輸出洗滌', 'AST06 隱蔽數據外傳', 'AST07 技能依賴投毒', 'AST08 跨技能通訊',
        'AST09 資源耗盡死迴圈', 'AST10 權限過度授權'
    ][::-1]
    
    risk_shares = [31.2, 22.4, 15.6, 11.8, 7.5, 4.8, 3.2, 1.8, 1.1, 0.6][::-1]
    block_rates = [96.5, 98.8, 99.4, 99.1, 92.0, 97.5, 95.0, 93.5, 98.0, 99.9][::-1]
    
    y = np.arange(len(skills))
    height = 0.54
    
    bars = ax.barh(y, risk_shares, height, color=C_SAGE, alpha=0.85, edgecolor=C_BORDER, label='風險分佈比例 (%)', zorder=3)
    
    ax.set_yticks(y)
    ax.set_yticklabels(skills, fontsize=7.8, color=C_TEXT, fontweight='bold')
    ax.set_xlabel('風險分佈佔比 (%)', fontsize=9.2, fontweight='bold', color=C_SAGE)
    ax.set_xlim(0, 46)  # Generous headroom so no text is ever clipped
    
    # Internal white labels for large bars, external badge for block rates
    for i, bar in enumerate(bars):
        w = bar.get_width()
        br = block_rates[i]
        
        if w >= 10.0:
            ax.text(w / 2.0, bar.get_y() + bar.get_height()/2., f'{w:.1f}%',
                    ha='center', va='center', fontsize=7.2, color='#FFFFFF', fontweight='bold', zorder=4)
            ax.text(w + 1.0, bar.get_y() + bar.get_height()/2., f'[阻斷率: {br:.1f}%]',
                    ha='left', va='center', fontsize=7.0, color=C_TEXT, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.18', facecolor='#F5F8F6', edgecolor='#3B6E58', linewidth=0.6, alpha=0.9),
                    zorder=4)
        else:
            ax.text(w + 1.0, bar.get_y() + bar.get_height()/2., f'{w:.1f}%  [阻斷率: {br:.1f}%]',
                    ha='left', va='center', fontsize=7.0, color=C_TEXT, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.18', facecolor='#FDFCFA', edgecolor=C_BORDER, linewidth=0.6, alpha=0.9),
                    zorder=4)
        
    legend = fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=1, frameon=True, fontsize=8.0)
    legend.get_frame().set_facecolor(C_CANVAS)
    legend.get_frame().set_edgecolor(C_BORDER)
    legend.get_frame().set_linewidth(0.8)
    for text in legend.get_texts():
        text.set_color(C_TEXT)
        text.set_fontweight('bold')
        
    out_path = os.path.join(OUTPUT_DIR, "chart_3_skills_horizontal.png")
    plt.savefig(out_path, dpi=300, facecolor=C_CARD)
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# Chart 4: RAG Grouped Bar (Risk Share vs. Retrieval Poisoning Impact)
# ==============================================================================
def generate_chart_4_rag():
    fig = plt.figure(figsize=(7.5, 4.6), facecolor=C_CARD, dpi=300)
    ax = fig.add_axes([0.09, 0.12, 0.88, 0.74])
    setup_ax(ax)
    
    rag_labels = ['RAG01\n庫投毒', 'RAG02\n越權檢索', 'RAG03\n上下文注入', 'RAG04\n元數據洩漏', 'RAG05\n幻覺外洩',
                  'RAG06\n對抗擾動', 'RAG07\n巨量DoS', 'RAG08\n快取污染', 'RAG09\n解析逃逸', 'RAG10\n水印缺失']
    shares = [26.8, 23.4, 18.2, 11.5, 8.6, 4.5, 3.2, 1.9, 1.2, 0.7]
    impacts = [42.5, 38.0, 55.0, 22.0, 18.5, 62.0, 10.0, 28.0, 5.0, 0.0]
    
    x = np.arange(len(rag_labels))
    width = 0.36
    
    b1 = ax.bar(x - width/2, shares, width, color=C_SLATE, alpha=0.9, edgecolor=C_BORDER, label='風險發生比例 (%)', zorder=3)
    b2 = ax.bar(x + width/2, impacts, width, color=C_TERRA, alpha=0.85, edgecolor=C_BORDER, label='召回污染衝擊率 (%)', zorder=3)
    
    ax.set_ylabel('百分比 (%)', fontsize=9.2, fontweight='bold', color=C_TEXT)
    ax.set_xticks(x)
    ax.set_xticklabels(rag_labels, fontsize=7.8, color=C_TEXT)
    ax.set_ylim(0, 78)  # Generous headroom to clear top
    
    for bar in b1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 1.2, f'{h:.1f}',
                ha='center', va='bottom', fontsize=6.8, color=C_SLATE, fontweight='bold')
    for bar in b2:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2., h + 1.2, f'{h:.1f}',
                    ha='center', va='bottom', fontsize=6.8, color=C_TERRA, fontweight='bold')
            
    legend = fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=2, frameon=True, fontsize=8.0)
    legend.get_frame().set_facecolor(C_CANVAS)
    legend.get_frame().set_edgecolor(C_BORDER)
    legend.get_frame().set_linewidth(0.8)
    for text in legend.get_texts():
        text.set_color(C_TEXT)
        text.set_fontweight('bold')
        
    out_path = os.path.join(OUTPUT_DIR, "chart_4_rag_grouped.png")
    plt.savefig(out_path, dpi=300, facecolor=C_CARD)
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# Chart 5: MITRE ATLAS Kill Chain Funnel & Interception
# ==============================================================================
def generate_chart_5_atlas():
    fig = plt.figure(figsize=(7.5, 4.6), facecolor=C_CARD, dpi=300)
    ax1 = fig.add_axes([0.09, 0.12, 0.81, 0.74])
    setup_ax(ax1)
    
    tactics = ['初始存取\nTA0002', '執行\nTA0005', '持久化\nTA0006', '防禦規避\nTA0007', '憑證存取\nTA0008',
               '發現偵察\nTA0004', '橫向移動\nTA0009', '資料收集\nTA0035', '外洩滲出\nTA0037', '影響衝擊\nTA0030']
    freqs = [29.5, 22.8, 14.6, 12.3, 8.7, 5.2, 3.1, 2.0, 1.2, 0.6]
    blocks = [96.2, 95.8, 93.4, 88.5, 98.1, 97.0, 94.5, 91.2, 97.8, 99.2]
    intrusions = [34.0, 28.5, 21.0, 45.2, 18.0, 12.5, 15.0, 24.0, 19.5, 31.0]
    
    x = np.arange(len(tactics))
    width = 0.50
    
    # Left axis: frequency bars kept in bottom half
    bars = ax1.bar(x, freqs, width, color=C_OCHRE, alpha=0.82, edgecolor=C_BORDER, label='攻擊發生頻率 (%)', zorder=3)
    ax1.set_ylabel('攻擊發生頻率 (%)', color=C_OCHRE, fontsize=9.2, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=C_OCHRE)
    ax1.set_ylim(0, 48)
    ax1.set_xticks(x)
    ax1.set_xticklabels(tactics, fontsize=7.6, color=C_TEXT)
    
    for bar in bars:
        h = bar.get_height()
        if h >= 10.0:
            ax1.text(bar.get_x() + bar.get_width()/2., h / 2.0, f'{h:.1f}%',
                     ha='center', va='center', fontsize=7.2, color='#FFFFFF', fontweight='bold', zorder=4)
        else:
            ax1.text(bar.get_x() + bar.get_width()/2., h + 0.8, f'{h:.1f}%',
                     ha='center', va='bottom', fontsize=7.0, color=C_OCHRE, fontweight='bold', zorder=4)
        
    # Right axis: lines with generous ceiling so block rate and intrusion rate don't collide with bars
    ax2 = ax1.twinx()
    ax2.set_facecolor('none')
    for spine in ax2.spines.values():
        spine.set_color(C_BORDER)
        
    ax2.plot(x, blocks, color=C_SAGE, marker='s', linewidth=2.0, markersize=5.0, label='護欄防禦攔截率 (%)', zorder=5)
    ax2.plot(x, intrusions, color=C_TERRA, marker='^', linewidth=1.8, linestyle='--', markersize=5.0, label='入侵成功率 (%)', zorder=5)
    
    ax2.set_ylabel('攔截 / 入侵率 (%)', color=C_SLATE, fontsize=9.2, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=C_SLATE)
    ax2.set_ylim(0, 125)  # Ample headroom
    
    # Clean callouts for block rates (above) and intrusion rates (below)
    for i in range(len(tactics)):
        b = blocks[i]
        intr = intrusions[i]
        
        # Block rate above
        ax2.annotate(
            f'{b:.1f}%',
            (x[i], b + 4.5),
            ha='center', va='center', fontsize=6.8, color=C_SAGE, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#F5F8F6', edgecolor='#3B6E58', linewidth=0.6, alpha=0.92),
            zorder=6
        )
        # Intrusion rate below
        ax2.annotate(
            f'{intr:.1f}%',
            (x[i], intr - 5.0),
            ha='center', va='center', fontsize=6.8, color=C_TERRA, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFF8EE', edgecolor='#9E5A38', linewidth=0.6, alpha=0.92),
            zorder=6
        )
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    legend = fig.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=3, frameon=True, fontsize=8.0)
    legend.get_frame().set_facecolor(C_CANVAS)
    legend.get_frame().set_edgecolor(C_BORDER)
    legend.get_frame().set_linewidth(0.8)
    for text in legend.get_texts():
        text.set_color(C_TEXT)
        text.set_fontweight('bold')
        
    out_path = os.path.join(OUTPUT_DIR, "chart_5_atlas_killchain.png")
    plt.savefig(out_path, dpi=300, facecolor=C_CARD)
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    print("Regenerating all 6 publication-grade Matplotlib charts with zero-collision styling...")
    generate_chart_0_radar()
    generate_chart_1_llm()
    generate_chart_2_agentic()
    generate_chart_3_skills()
    generate_chart_4_rag()
    generate_chart_5_atlas()
    print("All charts successfully regenerated with pristine typography!")
