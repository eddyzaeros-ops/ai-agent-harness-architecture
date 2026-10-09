import os
import re
import markdown

SOURCE_DIR = r"D:\Obsidian\MyVault\Harness\AI Agent Framework Analysis Report"
OUTPUT_HTML = os.path.join(SOURCE_DIR, "index.html")

def sanitize_mermaid_code(code):
    """
    Ensures mermaid code is syntactically valid and clean:
    1. Removes any [[Target|Alias]] -> Alias
    2. Strips out HTML tags <a ...>, </a>, <span> etc.
    3. Keeps arrows -->, -.->, ==> clean without &gt; or &lt;
    4. Escapes quotes inside node labels if necessary
    """
    # 1. Clean Obsidian wikilinks: [[target|alias]] -> alias, [[target]] -> target
    def clean_link(m):
        content = m.group(1)
        if "|" in content:
            return content.split("|", 1)[1].strip()
        return content.strip()
    
    code = re.sub(r'\[\[(.*?)\]\]', clean_link, code)
    
    # 2. Convert <br> or <br/> to <br/> safely
    code = re.sub(r'<br\s*/?>', '<br/>', code, flags=re.IGNORECASE)
    
    # 3. Strip any OTHER HTML tags (like <a>, </a>, <span>, etc.) without stripping <--> or <br/>
    # Notice: <--> is a mermaid bidirectional arrow! Do NOT strip it!
    def strip_html_tags(m):
        tag = m.group(0)
        if tag.lower() in ['<br>', '<br/>', '<br />']:
            return '<br/>'
        if tag.startswith('<--') or tag.startswith('-->'):
            return tag
        return ''
    
    code = re.sub(r'</?[a-zA-Z][^>]*>', strip_html_tags, code)
    
    # Standardize lines
    lines = []
    for line in code.splitlines():
        lines.append(line)
        
    return "\n".join(lines).strip()

def parse_markdown_file(file_path, filename):
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
        
    # Extract YAML frontmatter
    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            yaml_text = parts[1]
            body = parts[2]
            for line in yaml_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"\'')
                    
    # Determine Title
    title = meta.get("title")
    if not title:
        h1_match = re.search(r"^#\s+(.+)$", body, re.M)
        if h1_match:
            title = h1_match.group(1).strip()
        else:
            title = filename.replace(".md", "")
            
    # Phase / Group
    phase = meta.get("phase", "")
    if not phase:
        if filename.startswith("0") or filename.startswith("10") or filename.startswith("11"):
            if filename.startswith("00"):
                phase = "總覽導航與知識圖譜"
            else:
                phase = "Phase 1: Agent Harness 基礎概念與企業審計實作"
        elif any(filename.startswith(str(n)) for n in range(12, 21)):
            phase = "Phase 2: 企業需求、開源生態與五層縱深防禦體系"
        elif any(filename.startswith(str(n)) for n in [21, 22, 28]):
            phase = "Phase 3: 全服務鏈資料流、高階總結與完整歷程留痕"
        elif any(filename.startswith(str(n)) for n in [23, 24, 25, 26, 27, 29]) or "AAR" in filename:
            phase = "Phase 4: 國防自主擊殺鏈 F2T2EA 與分散式邊緣協同作戰"
        else:
            phase = "其他報告與附錄"
            
    # Short tab label
    tab_label = filename.replace(".md", "")
    prefix_match = re.match(r"^(\d+)-(.*)", tab_label)
    if prefix_match:
        num = prefix_match.group(1)
        rest = prefix_match.group(2)
        parts = rest.split("-")
        clean_name = parts[0] if len(parts) > 0 else rest
        if len(parts) > 1 and len(clean_name) < 4:
            clean_name = parts[0] + " " + parts[1]
        tab_label = f"{num}. {clean_name}"
    elif "AAR" in filename:
        tab_label = "AAR v2 任務事後檢討"

    # 1. Stash Mermaid Blocks FIRST BEFORE ANY Wikilink or HTML transformation
    mermaid_blocks = []
    def stash_mermaid(m):
        code = m.group(1).strip()
        clean_code = sanitize_mermaid_code(code)
        idx = len(mermaid_blocks)
        mermaid_blocks.append(clean_code)
        return f"\n\n<!--MERMAID_PLACEHOLDER_{idx}-->\n\n"
        
    body_no_mermaid = re.sub(r'```mermaid(.*?)```', stash_mermaid, body, flags=re.DOTALL)

    # 2. Process Wikilinks and Markdown in non-mermaid text
    def replace_wikilinks(text):
        # Image links ![[image.jpg]]
        def img_repl(m):
            img_name = m.group(1).strip()
            return f'<div class="figure-container"><img src="assets/{img_name}" alt="{img_name}" class="responsive-img" loading="lazy" onclick="openLightbox(this.src)" /><div class="figure-caption">{img_name}</div></div>'
        text = re.sub(r'!\[\[(.*?)\]\]', img_repl, text)
        
        # Standard markdown images ![alt](assets/...)
        def md_img_repl(m):
            alt = m.group(1)
            src = m.group(2)
            if not src.startswith("http") and not src.startswith("assets/"):
                if "/" in src:
                    src = "assets/" + src.split("/")[-1]
                else:
                    src = "assets/" + src
            return f'<div class="figure-container"><img src="{src}" alt="{alt}" class="responsive-img" loading="lazy" onclick="openLightbox(this.src)" /><div class="figure-caption">{alt}</div></div>'
        text = re.sub(r'!\[(.*?)\]\((.*?)\)', md_img_repl, text)
        
        # Callouts: > [!NOTE], > [!TIP], etc.
        def callout_repl(match):
            ctype = match.group(1).upper()
            title = match.group(2) if match.group(2) else ctype
            return f'> <div class="callout-header"><span class="callout-badge">{ctype}</span> <strong>{title}</strong></div>\n>'
        text = re.sub(r'^>\s*\[!([A-Z]+)\]\s*(.*)$', callout_repl, text, flags=re.M)

        # Standard wikilinks [[File#heading|alias]] or [[File]]
        def link_repl(m):
            link_body = m.group(1)
            if "|" in link_body:
                target, alias = link_body.split("|", 1)
            else:
                target, alias = link_body, link_body
            target_clean = target.split("#")[0].strip()
            return f'<a href="javascript:void(0)" class="obsidian-link" onclick="switchTabByTarget(\'{target_clean}\')">{alias}</a>'
        text = re.sub(r'\[\[(.*?)\]\]', link_repl, text)
        
        return text

    processed_body = replace_wikilinks(body_no_mermaid)
    
    # 3. Convert Markdown to HTML
    html_content = markdown.markdown(
        processed_body,
        extensions=[
            'fenced_code',
            'tables',
            'nl2br',
            'sane_lists',
            'codehilite'
        ]
    )
    
    # 4. Restore Mermaid Blocks with PURE RAW CODE (NO HTML entities like &lt; or &gt;)
    for idx, clean_code in enumerate(mermaid_blocks):
        mermaid_html = f'''
        <div class="mermaid-container">
            <div class="mermaid-toolbar">
                <span class="badge-tech"><i class="ph-tree-structure"></i> Mermaid 互動向量流程圖</span>
                <span class="mermaid-hint">依視窗自動等比自適應縮放，無橫向滾動條</span>
            </div>
            <div class="mermaid-viewport">
                <pre class="mermaid">{clean_code}</pre>
            </div>
        </div>
        '''
        html_content = html_content.replace(f"<!--MERMAID_PLACEHOLDER_{idx}-->", mermaid_html)
        
    return {
        "filename": filename,
        "clean_name": filename.replace(".md", ""),
        "title": title,
        "phase": phase,
        "tab_label": tab_label,
        "date": meta.get("date", ""),
        "tags": meta.get("tags", []),
        "html": html_content
    }

def main():
    print("Scanning Markdown files in:", SOURCE_DIR)
    all_files = sorted([f for f in os.listdir(SOURCE_DIR) if f.endswith(".md") and not f.startswith(".")])
    print(f"Found {len(all_files)} markdown files.")
    
    articles = []
    for f in all_files:
        path = os.path.join(SOURCE_DIR, f)
        data = parse_markdown_file(path, f)
        articles.append(data)
        
    phases = {}
    for a in articles:
        p = a["phase"]
        if p not in phases:
            phases[p] = []
        phases[p].append(a)
        
    nav_html = []
    content_html = []
    
    tab_index = 0
    for phase_name, items in phases.items():
        nav_html.append(f'<div class="nav-group">')
        nav_html.append(f'<div class="nav-group-title"><i class="ph-folder-simple-bold"></i> {phase_name}</div>')
        nav_html.append(f'<div class="nav-group-items">')
        for item in items:
            active_cls = "active" if tab_index == 0 else ""
            nav_html.append(f'''
            <button class="nav-tab-btn {active_cls}" 
                    data-tab-id="tab-{tab_index}" 
                    data-target="{item['clean_name']}" 
                    onclick="switchTab({tab_index})">
                <span class="tab-num">{item['tab_label'].split('.')[0] if '.' in item['tab_label'] else '★'}</span>
                <span class="tab-text" title="{item['title']}">{item['tab_label']}</span>
            </button>
            ''')
            
            display_style = "display: block;" if tab_index == 0 else "display: none;"
            content_html.append(f'''
            <div id="tab-{tab_index}" class="tab-pane {active_cls}" style="{display_style}">
                <div class="article-header">
                    <div class="article-breadcrumb">
                        <span class="phase-tag">{item['phase']}</span>
                        <span class="date-tag"><i class="ph-calendar-blank"></i> {item['date']}</span>
                    </div>
                    <h1 class="article-title">{item['title']}</h1>
                    <div class="article-meta-bar">
                        <span class="file-name"><i class="ph-file-text"></i> {item['filename']}</span>
                        <div class="header-actions">
                            <button class="btn-action" onclick="window.print()"><i class="ph-printer"></i> 列印</button>
                            <button class="btn-action" onclick="copyCurrentLink({tab_index})"><i class="ph-link"></i> 複製分頁連結</button>
                        </div>
                    </div>
                </div>
                <div class="article-body">
                    {item['html']}
                </div>
            </div>
            ''')
            tab_index += 1
            
        nav_html.append('</div>')
        nav_html.append('</div>')
        
    full_nav_html = "\n".join(nav_html)
    full_content_html = "\n".join(content_html)
    
    full_page = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Framework Analysis Report | 知識庫專案儀表板</title>
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
    <!-- Phosphor Icons -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <!-- Local / Fallback Mermaid.js -->
    <script src="assets/mermaid.min.js"></script>
    <script>
        if (typeof mermaid === 'undefined') {{
            document.write('<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"><\\/script>');
        }}
    </script>
    
    <style>
        :root {{
            --bg-base: #f8fafc;
            --bg-surface: #ffffff;
            --bg-sidebar: #0f172a;
            --sidebar-hover: #1e293b;
            --sidebar-active: #2563eb;
            --sidebar-text: #94a3b8;
            --sidebar-text-active: #ffffff;
            
            --border-color: #e2e8f0;
            --border-dark: #334155;
            
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            
            --accent-primary: #0284c7;
            --accent-teal: #0d9488;
            --accent-indigo: #4f46e5;
            --accent-amber: #d97706;
            --accent-rose: #e11d48;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Noto Sans TC', 'Microsoft JhengHei', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-base);
            color: var(--text-primary);
            height: 100vh;
            display: flex;
            overflow: hidden;
            -webkit-font-smoothing: antialiased;
        }}

        .app-layout {{
            display: flex;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
        }}

        /* Left Sidebar Tabs */
        .sidebar {{
            width: 380px;
            min-width: 320px;
            max-width: 440px;
            background-color: var(--bg-sidebar);
            display: flex;
            flex-direction: column;
            border-right: 1px solid var(--border-dark);
            z-index: 50;
            box-shadow: 4px 0 20px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
        }}

        .sidebar-header {{
            padding: 22px 20px;
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            border-bottom: 1px solid var(--border-dark);
        }}

        .brand-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(37, 99, 235, 0.2);
            color: #60a5fa;
            border: 1px solid rgba(96, 165, 250, 0.3);
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .sidebar-title {{
            color: #f8fafc;
            font-size: 18px;
            font-weight: 800;
            line-height: 1.4;
        }}

        .sidebar-subtitle {{
            color: #64748b;
            font-size: 12px;
            margin-top: 4px;
        }}

        .sidebar-search {{
            padding: 12px 18px;
            border-bottom: 1px solid var(--border-dark);
            background: #0f172a;
        }}

        .search-wrapper {{
            position: relative;
            display: flex;
            align-items: center;
        }}

        .search-icon {{
            position: absolute;
            left: 12px;
            color: #64748b;
            font-size: 16px;
        }}

        .search-input {{
            width: 100%;
            padding: 9px 12px 9px 36px;
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
            color: #f1f5f9;
            font-size: 13px;
            outline: none;
            transition: all 0.2s;
        }}

        .search-input:focus {{
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
        }}

        .sidebar-nav {{
            flex: 1;
            overflow-y: auto;
            padding: 14px 12px 40px 12px;
            scrollbar-width: thin;
            scrollbar-color: #334155 transparent;
        }}

        .sidebar-nav::-webkit-scrollbar {{
            width: 6px;
        }}
        .sidebar-nav::-webkit-scrollbar-thumb {{
            background: #334155;
            border-radius: 4px;
        }}

        .nav-group {{
            margin-bottom: 18px;
        }}

        .nav-group-title {{
            padding: 8px 12px;
            font-size: 11px;
            font-weight: 800;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .nav-group-items {{
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}

        .nav-tab-btn {{
            width: 100%;
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 14px;
            background: transparent;
            border: 1px solid transparent;
            border-radius: 8px;
            color: var(--sidebar-text);
            font-size: 13.5px;
            font-weight: 500;
            text-align: left;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }}

        .nav-tab-btn:hover {{
            background: var(--sidebar-hover);
            color: #f8fafc;
            transform: translateX(3px);
        }}

        .nav-tab-btn.active {{
            background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%);
            color: #ffffff;
            font-weight: 700;
            border-color: rgba(255,255,255,0.15);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
        }}

        .tab-num {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 26px;
            height: 24px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.1);
            font-size: 12px;
            font-weight: 700;
            font-family: 'Fira Code', monospace;
        }}

        .nav-tab-btn.active .tab-num {{
            background: rgba(255, 255, 255, 0.25);
            color: #ffffff;
        }}

        .tab-text {{
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        /* Main Content Viewport */
        .main-viewport {{
            flex: 1;
            height: 100vh;
            overflow-y: auto;
            background: var(--bg-base);
            display: flex;
            flex-direction: column;
            position: relative;
        }}

        .tab-pane {{
            max-width: 1380px;
            width: 100%;
            margin: 0 auto;
            padding: 40px 60px 100px 60px;
            animation: fadeIn 0.25s ease-in-out;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .article-header {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 32px 36px;
            margin-bottom: 32px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.03);
            position: relative;
            overflow: hidden;
        }}

        .article-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #0284c7, #4f46e5, #0d9488);
        }}

        .article-breadcrumb {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}

        .phase-tag {{
            display: inline-block;
            background: #e0f2fe;
            color: #0369a1;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
        }}

        .date-tag {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            color: var(--text-muted);
            font-size: 12.5px;
            font-weight: 500;
        }}

        .article-title {{
            font-size: 28px;
            font-weight: 900;
            color: var(--text-primary);
            line-height: 1.35;
            margin-bottom: 16px;
            letter-spacing: -0.5px;
        }}

        .article-meta-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 16px;
            border-top: 1px solid #f1f5f9;
            color: var(--text-muted);
            font-size: 13px;
        }}

        .file-name {{
            font-family: 'Fira Code', monospace;
            background: #f1f5f9;
            padding: 3px 8px;
            border-radius: 5px;
        }}

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .btn-action {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #f8fafc;
            border: 1px solid var(--border-color);
            padding: 6px 14px;
            border-radius: 6px;
            color: var(--text-secondary);
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .btn-action:hover {{
            background: #f1f5f9;
            color: var(--text-primary);
            border-color: #cbd5e1;
        }}

        .article-body {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 44px 52px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.03);
            line-height: 1.85;
            font-size: 16px;
            color: #334155;
        }}

        .article-body h1, .article-body h2, .article-body h3, .article-body h4 {{
            color: var(--text-primary);
            font-weight: 800;
            line-height: 1.4;
            margin-top: 36px;
            margin-bottom: 16px;
            letter-spacing: -0.3px;
        }}

        .article-body h1 {{ font-size: 24px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
        .article-body h2 {{ font-size: 20px; border-left: 4px solid var(--accent-primary); padding-left: 14px; }}
        .article-body h3 {{ font-size: 18px; }}
        .article-body h4 {{ font-size: 16px; }}

        .article-body p {{
            margin-bottom: 20px;
        }}

        .article-body ul, .article-body ol {{
            margin-bottom: 24px;
            padding-left: 28px;
        }}

        .article-body li {{
            margin-bottom: 8px;
        }}

        .article-body hr {{
            border: none;
            border-top: 1px solid var(--border-color);
            margin: 36px 0;
        }}

        .article-body table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 28px 0;
            font-size: 14.5px;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        }}

        .article-body th {{
            background: #f1f5f9;
            color: var(--text-primary);
            font-weight: 700;
            text-align: left;
            padding: 12px 16px;
            border-bottom: 2px solid var(--border-color);
        }}

        .article-body td {{
            padding: 12px 16px;
            border-bottom: 1px solid #f1f5f9;
            color: #334155;
            vertical-align: top;
        }}

        .article-body tr:last-child td {{
            border-bottom: none;
        }}

        .article-body tr:hover td {{
            background: #f8fafc;
        }}

        .article-body pre {{
            background: #0f172a;
            color: #f8fafc;
            padding: 20px 24px;
            border-radius: 12px;
            overflow-x: auto;
            font-family: 'Fira Code', monospace;
            font-size: 13.5px;
            line-height: 1.6;
            margin: 24px 0;
            border: 1px solid #1e293b;
            box-shadow: 0 4px 14px rgba(0,0,0,0.1);
        }}

        .article-body code {{
            font-family: 'Fira Code', monospace;
            background: #f1f5f9;
            color: #0284c7;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 500;
        }}

        .article-body pre code {{
            background: transparent;
            color: inherit;
            padding: 0;
        }}

        .article-body blockquote {{
            margin: 24px 0;
            padding: 16px 20px;
            background: #f0fdf4;
            border-left: 4px solid #16a34a;
            border-radius: 0 10px 10px 0;
            color: #166534;
        }}

        .callout-badge {{
            display: inline-block;
            background: #16a34a;
            color: white;
            font-size: 11px;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 4px;
            margin-right: 8px;
        }}

        .obsidian-link {{
            color: #0284c7;
            text-decoration: none;
            font-weight: 600;
            border-bottom: 1.5px dashed #38bdf8;
            transition: all 0.2s;
            cursor: pointer;
        }}

        .obsidian-link:hover {{
            color: #0369a1;
            background: rgba(2, 132, 199, 0.08);
            border-bottom-style: solid;
        }}

        .figure-container {{
            margin: 36px 0;
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            transition: all 0.3s ease;
        }}

        .figure-container:hover {{
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
            border-color: #cbd5e1;
        }}

        .responsive-img {{
            max-width: 100%;
            height: auto;
            object-fit: contain;
            border-radius: 8px;
            cursor: zoom-in;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: block;
        }}

        .figure-caption {{
            margin-top: 12px;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-muted);
            text-align: center;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .figure-caption::before {{
            content: '🔍 點擊圖片可全螢幕高清檢視 (4K)';
            font-size: 11.5px;
            background: #e2e8f0;
            padding: 2px 8px;
            border-radius: 4px;
            color: #475569;
        }}

        /* Mermaid Flowchart Containers (精準滿版與等比例縮放，無橫向滾動條) */
        .mermaid-container {{
            margin: 32px 0;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,0,0,0.04);
        }}

        .mermaid-toolbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 18px;
            background: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
        }}

        .badge-tech {{
            font-size: 12.5px;
            font-weight: 700;
            color: #0369a1;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .mermaid-hint {{
            font-size: 12px;
            color: #64748b;
        }}

        .mermaid-viewport {{
            padding: 24px 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            background: #ffffff;
            min-height: 200px;
        }}

        pre.mermaid {{
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            display: flex !important;
            justify-content: center !important;
            font-family: inherit !important;
        }}

        pre.mermaid svg {{
            width: 100% !important;
            max-width: 100% !important;
            height: auto !important;
        }}

        /* Lightbox Modal */
        .lightbox-modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(15, 23, 42, 0.95);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            padding: 24px;
            backdrop-filter: blur(8px);
        }}

        .lightbox-img {{
            max-width: 95vw;
            max-height: 90vh;
            object-fit: contain;
            border-radius: 8px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }}

        .lightbox-close {{
            position: absolute;
            top: 24px;
            right: 28px;
            color: #ffffff;
            font-size: 32px;
            cursor: pointer;
            background: rgba(255,255,255,0.1);
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }}

        .lightbox-close:hover {{
            background: rgba(255,255,255,0.25);
            transform: scale(1.05);
        }}
    </style>
</head>
<body>
    <div class="app-layout">
        <!-- Left Sidebar (Tabs) -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <span class="brand-badge"><i class="ph-shield-check"></i> JADC2 國防級 Harness</span>
                <h1 class="sidebar-title">AI Agent Framework</h1>
                <p class="sidebar-subtitle">全系列 31 篇研究研析與作戰報告</p>
            </div>
            
            <div class="sidebar-search">
                <div class="search-wrapper">
                    <i class="ph-magnifying-glass search-icon"></i>
                    <input type="text" id="tabSearch" class="search-input" placeholder="搜尋主題、關鍵字或輪次..." oninput="filterTabs()">
                </div>
            </div>
            
            <nav class="sidebar-nav" id="sidebarNav">
                {full_nav_html}
            </nav>
        </aside>

        <!-- Right Viewport (Content) -->
        <main class="main-viewport" id="mainViewport">
            {full_content_html}
        </main>
    </div>

    <!-- Lightbox for 4K Infographics -->
    <div id="lightbox" class="lightbox-modal" onclick="closeLightbox()">
        <span class="lightbox-close">&times;</span>
        <img id="lightboxImg" class="lightbox-img" src="" alt="Enlarged view">
    </div>

    <script>
        // Initialize Mermaid safely
        mermaid.initialize({{
            startOnLoad: false,
            theme: 'default',
            securityLevel: 'loose',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }}
        }});

        // Render visible mermaid diagrams
        function renderMermaidInContainer(container) {{
            const elements = container.querySelectorAll('pre.mermaid:not([data-processed="true"])');
            if (elements.length > 0) {{
                try {{
                    mermaid.run({{
                        nodes: elements
                    }});
                }} catch (err) {{
                    console.warn('Mermaid render error:', err);
                }}
            }}
        }}

        // Tab Switching Logic
        function switchTab(index) {{
            const buttons = document.querySelectorAll('.nav-tab-btn');
            const panes = document.querySelectorAll('.tab-pane');

            buttons.forEach(btn => btn.classList.remove('active'));
            panes.forEach(pane => {{
                pane.classList.remove('active');
                pane.style.display = 'none';
            }});

            const targetBtn = document.querySelector(`.nav-tab-btn[data-tab-id="tab-${{index}}"]`);
            const targetPane = document.getElementById(`tab-${{index}}`);

            if (targetBtn && targetPane) {{
                targetBtn.classList.add('active');
                targetPane.classList.add('active');
                targetPane.style.display = 'block';

                document.getElementById('mainViewport').scrollTop = 0;
                
                // Trigger mermaid render for this specific pane
                setTimeout(() => {{
                    renderMermaidInContainer(targetPane);
                }}, 60);
            }}
        }}

        // Switch Tab by Target Filename or Wikilink
        function switchTabByTarget(targetName) {{
            const cleanTarget = targetName.replace('.md', '').trim();
            const btn = document.querySelector(`.nav-tab-btn[data-target="${{cleanTarget}}"]`);
            if (btn) {{
                btn.click();
                btn.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
            }} else {{
                const allBtns = document.querySelectorAll('.nav-tab-btn');
                for (const b of allBtns) {{
                    const t = b.getAttribute('data-target');
                    if (t && (t.includes(cleanTarget) || cleanTarget.includes(t))) {{
                        b.click();
                        b.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
                        break;
                    }}
                }}
            }}
        }}

        // Search Filter for Tabs
        function filterTabs() {{
            const query = document.getElementById('tabSearch').value.toLowerCase().trim();
            const buttons = document.querySelectorAll('.nav-tab-btn');
            const groups = document.querySelectorAll('.nav-group');

            buttons.forEach(btn => {{
                const text = btn.innerText.toLowerCase();
                const target = (btn.getAttribute('data-target') || '').toLowerCase();
                if (text.includes(query) || target.includes(query)) {{
                    btn.style.display = 'flex';
                }} else {{
                    btn.style.display = 'none';
                }}
            }});

            groups.forEach(group => {{
                const visibleButtons = group.querySelectorAll('.nav-tab-btn[style="display: flex;"]');
                if (query === '' || visibleButtons.length > 0) {{
                    group.style.display = 'block';
                }} else {{
                    group.style.display = 'none';
                }}
            }});
        }}

        function copyCurrentLink(index) {{
            const url = window.location.href.split('#')[0] + '#tab-' + index;
            navigator.clipboard.writeText(url).then(() => {{
                alert('已成功複製此分頁的直連網址！');
            }});
        }}

        function openLightbox(src) {{
            const lb = document.getElementById('lightbox');
            const img = document.getElementById('lightboxImg');
            img.src = src;
            lb.style.display = 'flex';
        }}

        function closeLightbox() {{
            document.getElementById('lightbox').style.display = 'none';
        }}

        window.addEventListener('DOMContentLoaded', () => {{
            const hash = window.location.hash;
            let initialTab = 0;
            if (hash && hash.startsWith('#tab-')) {{
                const idx = parseInt(hash.replace('#tab-', ''), 10);
                if (!isNaN(idx)) {{
                    initialTab = idx;
                }}
            }}
            switchTab(initialTab);
        }});
    </script>
</body>
</html>
'''
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(full_page)
        
    print(f"Successfully generated clean tabbed HTML at: {OUTPUT_HTML}")
    print(f"File size: {os.path.getsize(OUTPUT_HTML):,} bytes")

if __name__ == "__main__":
    main()
