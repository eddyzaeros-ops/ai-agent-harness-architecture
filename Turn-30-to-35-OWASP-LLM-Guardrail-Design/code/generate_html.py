import os
import re
import json
import html
import markdown
import base64
import shutil

SOURCE_DIR = r"D:\Obsidian\MyVault\Harness\OWASP LLM Guardrail Design"
OUTPUT_DIR = r"d:\JavaDO\OWASP html"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "index.html")
NAMED_FILE = os.path.join(OUTPUT_DIR, "OWASP_LLM_Guardrail_Design.html")

FILES_CONFIG = [
    {
        "filename": "00-Guardrail-Architecture-Index.md",
        "tab_id": "tab-00",
        "tab_num": "00",
        "title": "護欄體系總覽與跨層關聯",
        "subtitle": "Architecture Synthesis & Defense-in-Depth Matrix",
        "icon": "📐",
        "badge": "L1~L5 縱深防禦",
        "badge_color": "purple",
        "summary": "建立模型分層、資料分級、單一閘道與三層協同護欄之全域防護體系，拆解複合式多階段攻擊攔截鏈路。"
    },
    {
        "filename": "01-LLM-Guardrail.md",
        "tab_id": "tab-01",
        "tab_num": "01",
        "title": "LLM 基礎模型護欄",
        "subtitle": "OWASP Top 10 for LLM (LLM01~LLM10)",
        "icon": "🛡️",
        "badge": "L1/L2 語意閘門",
        "badge_color": "blue",
        "summary": "聚焦文字輸入與輸出邊界，涵蓋 Prompt 注入防禦、敏感資訊脫敏、DISA IL 密級校驗與 8 大不可否認性審計欄位。"
    },
    {
        "filename": "02-Agentic-Guardrail.md",
        "tab_id": "tab-02",
        "tab_num": "02",
        "title": "Agentic 代理人行為護欄",
        "subtitle": "OWASP Top 10 for Agentic Applications (ASI01~ASI10)",
        "icon": "🤖",
        "badge": "L3 執行監督器",
        "badge_color": "emerald",
        "summary": "突破靜態文字檢核，以「三維六門」防範目標劫持、約束狀態機轉移、核發 JIT 60 秒短效憑證與去話術化情境 HITL。"
    },
    {
        "filename": "03-Skills-Guardrail.md",
        "tab_id": "tab-03",
        "tab_num": "03",
        "title": "Skills 技能工具安全護欄",
        "subtitle": "OWASP Agentic Skills Top 10 (AST10)",
        "icon": "⚡",
        "badge": "L4 沙盒隔離",
        "badge_color": "amber",
        "summary": "防堵實體系統侵害，瓦解「機敏憑證 ⨂ 外部連線 ⨂ 不可信語料」致命三要素，實施 gVisor 微沙盒與漂移斷路器。"
    },
    {
        "filename": "04-RAG-Guardrail.md",
        "tab_id": "tab-04",
        "tab_num": "04",
        "title": "RAG 檢索增強安全護欄",
        "subtitle": "OWASP RAG Security Pipeline (RAG01~RAG10)",
        "icon": "📚",
        "badge": "L5 檢索閘門",
        "badge_color": "cyan",
        "summary": "落實 Pre-Filtering 權限前置過濾、防間接 Prompt 注入、防知識庫投毒與向量逆向推論防禦。"
    },
    {
        "filename": "05-ATLAS-Attack-Chain.md",
        "tab_id": "tab-05",
        "tab_num": "05",
        "title": "MITRE ATLAS 攻擊鍊防禦對齊",
        "subtitle": "Adversarial Threat Landscape (TA0001~TA0016)",
        "icon": "⚔️",
        "badge": "端到端攻擊鍊",
        "badge_color": "rose",
        "summary": "以 MITRE ATLAS 框架解構 AI 攻擊鍊，剖析瞬態坍縮現象、離地攻擊 (LotL-AI) 與縱深防禦映射。"
    }
]

WIKILINK_MAP = {
    "00-Guardrail-Architecture-Index": ("tab-00", "00. 護欄體系總覽與跨層關聯"),
    "01-LLM-Guardrail": ("tab-01", "01. LLM 基礎模型護欄"),
    "02-Agentic-Guardrail": ("tab-02", "02. Agentic 代理人行為護欄"),
    "03-Skills-Guardrail": ("tab-03", "03. Skills 技能工具安全護欄"),
    "04-RAG-Guardrail": ("tab-04", "04. RAG 檢索增強安全護欄"),
    "05-ATLAS-Attack-Chain": ("tab-05", "05. MITRE ATLAS 攻擊鍊防禦對齊"),
    "護欄架構總覽與跨層關聯": ("tab-00", "護欄架構總覽與跨層關聯"),
    "LLM 基礎模型護欄": ("tab-01", "LLM 基礎模型護欄"),
    "Agentic 自主代理人護欄": ("tab-02", "Agentic 自主代理人護欄"),
    "Skills 技能工具安全護欄": ("tab-03", "Skills 技能工具安全護欄"),
    "RAG 檢索增強安全護欄": ("tab-04", "RAG 檢索增強安全護欄"),
    "MITRE ATLAS 攻擊鍊防禦對齊": ("tab-05", "MITRE ATLAS 攻擊鍊防禦對齊"),
    "MITRE ATLAS 攻擊鍊": ("tab-05", "MITRE ATLAS 攻擊鍊"),
    "MITRE ATLAS 攻擊鍊防禦": ("tab-05", "MITRE ATLAS 攻擊鍊防禦"),
    "Agentic 行為防火牆": ("tab-02", "Agentic 行為防火牆"),
    "Skills 護欄": ("tab-03", "Skills 護欄"),
    "RAG 護欄": ("tab-04", "RAG 護欄"),
    "整體縱深架構": ("tab-00", "整體縱深架構")
}

def parse_frontmatter(content):
    frontmatter = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            raw_yaml = parts[1]
            body = parts[2]
            current_list_key = None
            for line in raw_yaml.strip().split("\n"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("- ") and current_list_key:
                    frontmatter[current_list_key].append(line[2:].strip().strip('"').strip("'"))
                elif ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if v == "":
                        frontmatter[k] = []
                        current_list_key = k
                    else:
                        frontmatter[k] = v
                        current_list_key = None
    return frontmatter, body.strip()

def process_wikilinks(text):
    def repl_alias(m):
        target = m.group(1).strip()
        alias = m.group(2).strip()
        tab_info = WIKILINK_MAP.get(target)
        if tab_info:
            return f'<a href="#{tab_info[0]}" class="wikilink" onclick="switchTab(\'{tab_info[0]}\', event)"><span class="wikilink-icon">🔗</span><span class="wikilink-text">{alias}</span></a>'
        return f'<span class="wikilink-unresolved">[[{target}|{alias}]]</span>'

    def repl_direct(m):
        target = m.group(1).strip()
        tab_info = WIKILINK_MAP.get(target)
        if tab_info:
            return f'<a href="#{tab_info[0]}" class="wikilink" onclick="switchTab(\'{tab_info[0]}\', event)"><span class="wikilink-icon">🔗</span><span class="wikilink-text">{tab_info[1]}</span></a>'
        return f'<span class="wikilink-unresolved">[[{target}]]</span>'

    text = re.sub(r'\[\[([^\]\|]+)\|([^\]]+)\]\]', repl_alias, text)
    text = re.sub(r'\[\[([^\]\|]+)\]\]', repl_direct, text)
    return text

def badge_replacer(html_text):
    badge_patterns = [
        (r'\b(Block \(阻斷\)|Block)\b', 'badge-block'),
        (r'\b(Reject \(拒絕載入\)|Reject \(拒絕註冊\)|Reject \(拒絕\)|Reject)\b', 'badge-reject'),
        (r'\b(Mask \(遮罩\)|Mask)\b', 'badge-mask'),
        (r'\b(Sanitize \(消毒\)|Sanitize)\b', 'badge-sanitize'),
        (r'\b(HITL 攔截審核|HITL)\b', 'badge-hitl'),
        (r'\b(Drop \(丟棄並通報\)|Drop)\b', 'badge-drop'),
        (r'\b(Filter \(強制隔離過濾\)|Filter)\b', 'badge-filter'),
        (r'\b(Freeze \(凍結停權\)|Freeze)\b', 'badge-freeze'),
        (r'\b(Circuit Break \(熔斷阻斷\)|Circuit Break)\b', 'badge-circuit'),
        (r'\b(Sandbox Isolation \(強制沙盒化\)|Sandbox Isolation)\b', 'badge-sandbox'),
        (r'\b(Auto-Deprecate \(自動除役\))\b', 'badge-deprecate'),
        (r'\b(Deny \(跨界拒絕\)|Deny \(拒絕\)|Deny)\b', 'badge-deny'),
        (r'\b(Pass / Sanitized|PASS)\b', 'badge-pass'),
        (r'\b(APPROVED)\b', 'badge-pass'),
    ]
    for pattern, css_class in badge_patterns:
        html_text = re.sub(pattern, f'<span class="status-badge {css_class}">\\1</span>', html_text)
    return html_text

def render_image_card(img_name, caption):
    candidates = [
        os.path.join(SOURCE_DIR, img_name),
        os.path.join(r"D:\JavaDO", img_name),
        os.path.join(OUTPUT_DIR, img_name)
    ]
    found_path = None
    for p in candidates:
        if os.path.exists(p):
            found_path = p
            break

    b64_data = ""
    mime_type = "image/png"
    if found_path:
        target_in_out = os.path.join(OUTPUT_DIR, img_name)
        if not os.path.exists(target_in_out) or os.path.getmtime(found_path) > os.path.getmtime(target_in_out):
            try:
                shutil.copy2(found_path, target_in_out)
            except Exception:
                pass

        ext = os.path.splitext(img_name)[1].lower()
        if ext in ['.jpg', '.jpeg']:
            mime_type = 'image/jpeg'
        elif ext == '.svg':
            mime_type = 'image/svg+xml'
        elif ext == '.webp':
            mime_type = 'image/webp'

        try:
            with open(found_path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            pass

    src = f"data:{mime_type};base64,{b64_data}" if b64_data else img_name
    clean_caption = html.escape(caption or img_name)

    return f'''
    <div class="image-card tex2jax_ignore">
        <div class="image-toolbar">
            <div class="image-label">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
                <span>{clean_caption}</span>
            </div>
            <div class="image-btn-group">
                <button class="tool-btn" onclick="openImageModal(this)" title="全螢幕放大檢視">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg>
                    放大
                </button>
                <a class="tool-btn" href="{img_name}" download="{img_name}" title="下載高解析原始圖檔">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                    下載
                </a>
            </div>
        </div>
        <div class="image-canvas">
            <img src="{src}" alt="{clean_caption}" class="responsive-img" onclick="openImageModal(this)" loading="lazy" />
        </div>
        <div class="image-caption">{clean_caption}</div>
    </div>
    '''

def convert_md_file(file_path, tab_cfg):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)

    # 1. Protect Mermaid diagrams
    mermaid_blocks = []
    def save_mermaid(match):
        code = match.group(1).strip()
        code_clean = re.sub(r'\[\[(?:[^\]\|]+\|)?([^\]]+)\]\]', r'\1', code)
        code_clean = re.sub(r'rect\s+rgb\(240,\s*248,\s*255\)', 'rect rgba(59, 130, 246, 0.12)', code_clean)
        code_clean = re.sub(r'rect\s+rgb\(255,\s*245,\s*245\)', 'rect rgba(244, 63, 94, 0.12)', code_clean)
        idx = len(mermaid_blocks)
        mermaid_blocks.append(code_clean)
        return f"\n\n<!--MERMAID_PLACEHOLDER_{idx}-->\n\n"

    body = re.sub(r'```mermaid\s*\n(.*?)\n```', save_mermaid, body, flags=re.DOTALL)

    # 2. Protect Math blocks
    math_blocks = []
    def save_display_math(match):
        math_content = match.group(1)
        idx = len(math_blocks)
        math_blocks.append((True, math_content))
        return f"<!--MATH_PLACEHOLDER_{idx}-->"

    def save_inline_math(match):
        math_content = match.group(1)
        idx = len(math_blocks)
        math_blocks.append((False, math_content))
        return f"<!--MATH_PLACEHOLDER_{idx}-->"

    body = re.sub(r'\$\$(.*?)\$\$', save_display_math, body, flags=re.DOTALL)
    body = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', save_inline_math, body)

    # 3. Process Obsidian callouts
    def repl_callout(match):
        lines = match.group(0).split('\n')
        first_line = lines[0]
        callout_m = re.match(r'>\s*\[!([A-Za-z]+)\]\s*(.*)', first_line)
        if callout_m:
            c_type = callout_m.group(1).lower()
            c_title = callout_m.group(2).strip() or c_type.capitalize()
            rest = [re.sub(r'^>\s?', '', l) for l in lines[1:]]
            rest_text = "\n".join(rest)
            icon = "💡"
            if c_type in ["warning", "caution", "danger"]:
                icon = "⚠️"
            elif c_type in ["important", "tip"]:
                icon = "✨"
            return f'<div class="callout callout-{c_type}"><div class="callout-header"><span class="callout-icon">{icon}</span><span class="callout-title">{c_title}</span></div><div class="callout-body">\n\n{rest_text}\n\n</div></div>'
        return match.group(0)

    body = re.sub(r'(?:^>[^\n]*\n?)+', repl_callout, body, flags=re.MULTILINE)

    # 3.5 Protect Images (Obsidian ![[...]] and Markdown ![...](...))
    image_blocks = []
    def save_obsidian_image(match):
        raw = match.group(1).strip()
        parts = raw.split('|')
        name = parts[0].strip()
        caption = parts[1].strip() if len(parts) > 1 else name
        idx = len(image_blocks)
        image_blocks.append((name, caption))
        return f"\n\n<!--IMAGE_PLACEHOLDER_{idx}-->\n\n"

    def save_md_image(match):
        alt = match.group(1).strip()
        path = match.group(2).strip()
        name = os.path.basename(path)
        caption = alt or name
        idx = len(image_blocks)
        image_blocks.append((name, caption))
        return f"\n\n<!--IMAGE_PLACEHOLDER_{idx}-->\n\n"

    body = re.sub(r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|webp|svg)[^\]]*)\]\]', save_obsidian_image, body, flags=re.IGNORECASE)
    body = re.sub(r'!\[([^\]]*)\]\(([^\)]+\.(?:png|jpg|jpeg|gif|webp|svg)[^\)]*)\)', save_md_image, body, flags=re.IGNORECASE)

    # 4. Process wikilinks
    body = process_wikilinks(body)

    # 5. Convert to HTML
    md_parser = markdown.Markdown(
        extensions=['extra', 'tables', 'fenced_code', 'toc', 'sane_lists'],
        extension_configs={
            'toc': {'permalink': False}
        }
    )
    html_content = md_parser.convert(body)

    # Wrap tables in responsive container
    html_content = re.sub(r'(<table>[\s\S]*?</table>)', r'<div class="table-container">\1</div>', html_content)

    # Restore Image blocks
    for idx, (name, caption) in enumerate(image_blocks):
        wrapper = render_image_card(name, caption)
        html_content = html_content.replace(f"<!--IMAGE_PLACEHOLDER_{idx}-->", wrapper)

    # 6. Restore Mermaid blocks with dedicated source container
    for idx, code in enumerate(mermaid_blocks):
        clean_code_esc = html.escape(code)
        diagram_id = f"diagram-{tab_cfg['tab_id']}-{idx}"
        wrapper = f'''
        <div class="diagram-card tex2jax_ignore" id="{diagram_id}">
            <div class="diagram-toolbar">
                <div class="diagram-label">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/></svg>
                    <span>架構互動圖 (Mermaid Architecture Diagram)</span>
                </div>
                <div class="diagram-btn-group">
                    <button class="tool-btn" onclick="toggleRawCode(this)" title="檢視 Mermaid 原始語法">
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
                        語法
                    </button>
                    <button class="tool-btn" onclick="openDiagramModal('{diagram_id}')" title="全螢幕檢視圖表">
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg>
                        放大
                    </button>
                </div>
            </div>
            <div class="diagram-canvas">
                <div class="mermaid-diagram-box">
                    <pre class="mermaid-src" style="display:none;">{clean_code_esc}</pre>
                    <div class="mermaid-output">
                        <div class="mermaid-loading">
                            <span class="loading-spinner"></span>
                            <span>繪製架構圖表...</span>
                        </div>
                    </div>
                </div>
            </div>
            <pre class="raw-code-panel" style="display:none;"><code>{clean_code_esc}</code></pre>
        </div>
        '''
        html_content = html_content.replace(f"<!--MERMAID_PLACEHOLDER_{idx}-->", wrapper)

    # 7. Restore Math blocks
    for idx, (is_display, math_code) in enumerate(math_blocks):
        if is_display:
            html_content = html_content.replace(f"<!--MATH_PLACEHOLDER_{idx}-->", f"$${math_code}$$")
        else:
            html_content = html_content.replace(f"<!--MATH_PLACEHOLDER_{idx}-->", f"${math_code}$")

    # 8. Add copy buttons to code blocks & check for ASCII art diagrams
    def wrap_code_block(m):
        code_tag_attrs = m.group(1) or ""
        code_body = m.group(2)
        lang = "TEXT"
        lang_match = re.search(r'class="language-([a-zA-Z0-9_\-]+)"', code_tag_attrs)
        # Unescape any wikilink tags that were escaped inside code blocks so they render as interactive links
        code_body = re.sub(
            r'&lt;a\s+href=&quot;([^&]+)&quot;\s+class=&quot;wikilink&quot;\s+onclick=&quot;([^&]+)&quot;&gt;&lt;span\s+class=&quot;wikilink-icon&quot;&gt;([^&]+)&lt;/span&gt;&lt;span\s+class=&quot;wikilink-text&quot;&gt;([^&]+)&lt;/span&gt;&lt;/a&gt;',
            r'<a href="\1" class="wikilink" onclick="\2"><span class="wikilink-icon">\3</span><span class="wikilink-text">\4</span></a>',
            code_body
        )

        if lang_match:
            lang = lang_match.group(1).upper()
        elif "{" in code_body and "}" in code_body and ":" in code_body:
            lang = "JSON"
        elif "skill_id:" in code_body:
            lang = "YAML"
        elif "<untrusted_tool" in code_body:
            lang = "XML"
        elif any(c in code_body for c in ["┌", "└", "│", "├", "─", "▼", "▲"]):
            lang = "ARCHITECTURE MATRIX"
            return f'<div class="code-wrapper ascii-art-wrapper tex2jax_ignore"><div class="code-header"><span class="code-lang"><span class="lang-dot"></span>{lang}</span><button class="copy-code-btn" onclick="copyCode(this)"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>複製</button></div><pre class="ascii-art-pre"><code{code_tag_attrs}>{code_body}</code></pre></div>'

        return f'<div class="code-wrapper tex2jax_ignore"><div class="code-header"><span class="code-lang"><span class="lang-dot"></span>{lang}</span><button class="copy-code-btn" onclick="copyCode(this)"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>複製</button></div><pre><code{code_tag_attrs}>{code_body}</code></pre></div>'

    html_content = re.sub(r'<pre><code(?:\s+class="([^"]*)")?>([\s\S]*?)</code></pre>', wrap_code_block, html_content)

    # 9. Extract Headings for TOC & ensure unique anchor IDs
    headings = []
    def ensure_heading_id(m):
        lvl = int(m.group(1))
        existing_id = m.group(2)
        content_inner = m.group(3)
        clean_text = re.sub(r'<[^>]+>', '', content_inner).strip()
        hid = existing_id or f"{tab_cfg['tab_id']}-" + re.sub(r'[^\w\u4e00-\u9fff\-]+', '-', clean_text).strip('-')
        headings.append({"level": lvl, "id": hid, "text": clean_text})
        return f'<h{lvl} id="{hid}" class="anchor-heading"><a href="#{hid}" class="heading-anchor" title="小節錨點">#</a>{content_inner}</h{lvl}>'

    html_content = re.sub(r'<h([23])(?:\s+id="([^"]+)")?>(.*?)</h\1>', ensure_heading_id, html_content)

    # 10. Status badges styling
    html_content = badge_replacer(html_content)

    return {
        "tab_cfg": tab_cfg,
        "frontmatter": frontmatter,
        "html_content": html_content,
        "headings": headings
    }

CLIENT_JAVASCRIPT = r"""
let mermaidCounter = 0;

// Render Mermaid on demand for a container
async function renderMermaidInElement(container) {
    if (!container) return;
    const boxes = container.querySelectorAll('.mermaid-diagram-box');
    for (const box of boxes) {
        const out = box.querySelector('.mermaid-output');
        const src = box.querySelector('.mermaid-src');
        if (!out || !src || out.getAttribute('data-rendered') === 'true') continue;

        const code = src.textContent.trim();
        if (!code) continue;

        if (!window.mermaid) {
            out.innerHTML = '<pre class="mermaid-fallback">' + escapeHtml(code) + '</pre>';
            out.setAttribute('data-rendered', 'true');
            continue;
        }

        mermaidCounter++;
        const uniqueId = 'mermaid_svg_' + mermaidCounter;
        try {
            const { svg } = await mermaid.render(uniqueId, code);
            out.innerHTML = svg;
            out.setAttribute('data-rendered', 'true');
        } catch (err) {
            console.error('Mermaid render error:', err);
            out.innerHTML = '<div class="diagram-error"><div class="error-msg">⚠️ 圖表繪製異常：' + escapeHtml(err.message || String(err)) + '</div><pre>' + escapeHtml(code) + '</pre></div>';
            out.setAttribute('data-rendered', 'true');
        }
    }
}

// 1. Tab Switching System
function switchTab(tabId, event) {
    if (event) event.preventDefault();
    
    // Update Tab Buttons
    const buttons = document.querySelectorAll('.nav-tab-btn');
    buttons.forEach(btn => {
        if (btn.dataset.tab === tabId) {
            btn.classList.add('active');
            btn.setAttribute('aria-selected', 'true');
        } else {
            btn.classList.remove('active');
            btn.setAttribute('aria-selected', 'false');
        }
    });

    // Update Tab Panes
    const panes = document.querySelectorAll('.tab-pane');
    let targetPane = null;
    panes.forEach(pane => {
        if (pane.id === tabId) {
            pane.classList.add('active');
            targetPane = pane;
        } else {
            pane.classList.remove('active');
        }
    });

    // Update Quicklinks in sidebar
    document.querySelectorAll('.ql-item').forEach(item => {
        if (item.getAttribute('href') === '#' + tabId) {
            item.classList.add('ql-current');
        } else {
            item.classList.remove('ql-current');
        }
    });

    // Update URL hash
    history.replaceState(null, null, '#' + tabId);

    // Render Mermaid in newly active pane
    if (targetPane) {
        renderMermaidInElement(targetPane);
        if (window.MathJax && MathJax.typesetPromise) {
            MathJax.typesetPromise([targetPane]).catch(err => console.log('MathJax error:', err));
        }
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Listen to hash changes (browser back/forward)
window.addEventListener('hashchange', () => {
    const hash = window.location.hash.replace('#', '');
    if (hash.startsWith('tab-')) {
        switchTab(hash);
    } else {
        const target = document.getElementById(hash);
        if (target) {
            const parentPane = target.closest('.tab-pane');
            if (parentPane && !parentPane.classList.contains('active')) {
                switchTab(parentPane.id);
            }
            setTimeout(() => {
                target.scrollIntoView({ behavior: 'smooth' });
            }, 100);
        }
    }
});

// Initialize Tab based on initial hash or default to tab-00
window.addEventListener('DOMContentLoaded', () => {
    const initialHash = window.location.hash.replace('#', '');
    if (initialHash && document.getElementById(initialHash)) {
        const target = document.getElementById(initialHash);
        if (target.classList.contains('tab-pane')) {
            switchTab(initialHash);
        } else {
            const parentPane = target.closest('.tab-pane');
            if (parentPane) {
                switchTab(parentPane.id);
                setTimeout(() => {
                    target.scrollIntoView({ behavior: 'smooth' });
                }, 200);
            }
        }
    } else {
        const activePane = document.querySelector('.tab-pane.active');
        if (activePane) {
            renderMermaidInElement(activePane);
        }
    }
    initScrollSpy();
    initKeyboardNav();
});

// Keyboard Tab Navigation (Left / Right Arrow)
function initKeyboardNav() {
    const tabList = document.querySelector('.tab-nav-container');
    if (!tabList) return;
    const tabButtons = Array.from(tabList.querySelectorAll('.nav-tab-btn'));
    tabButtons.forEach((btn, idx) => {
        btn.addEventListener('keydown', (e) => {
            let targetIdx = null;
            if (e.key === 'ArrowRight') {
                targetIdx = (idx + 1) % tabButtons.length;
            } else if (e.key === 'ArrowLeft') {
                targetIdx = (idx - 1 + tabButtons.length) % tabButtons.length;
            }
            if (targetIdx !== null) {
                e.preventDefault();
                tabButtons[targetIdx].focus();
                switchTab(tabButtons[targetIdx].dataset.tab);
            }
        });
    });
}

// 2. Scroll to heading with offset
function scrollToHeading(e, headingId) {
    if (e) e.preventDefault();
    const el = document.getElementById(headingId);
    if (el) {
        const navBar = document.querySelector('.tab-nav-bar');
        const offset = (navBar ? navBar.offsetHeight : 0) + 90;
        const bodyRect = document.body.getBoundingClientRect().top;
        const elementRect = el.getBoundingClientRect().top;
        const elementPosition = elementRect - bodyRect;
        const offsetPosition = elementPosition - offset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
        history.replaceState(null, null, '#' + headingId);
    }
}

// 3. Scroll Spy for active TOC item
function initScrollSpy() {
    window.addEventListener('scroll', () => {
        const fab = document.getElementById('fab-top');
        if (fab) {
            if (window.scrollY > 400) {
                fab.classList.add('show');
            } else {
                fab.classList.remove('show');
            }
        }

        const activePane = document.querySelector('.tab-pane.active');
        if (!activePane) return;

        const headings = activePane.querySelectorAll('h2[id], h3[id]');
        const scrollPos = window.scrollY + 160;

        let currentId = '';
        headings.forEach(h => {
            if (h.offsetTop <= scrollPos) {
                currentId = h.id;
            }
        });

        const tocLinks = activePane.querySelectorAll('.toc-link');
        tocLinks.forEach(link => {
            if (link.getAttribute('href') === '#' + currentId) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }, { passive: true });
}

// 4. Code Block Copying
function copyCode(btn) {
    const wrapper = btn.closest('.code-wrapper');
    const codeEl = wrapper ? wrapper.querySelector('pre code') : null;
    if (!codeEl) return;

    navigator.clipboard.writeText(codeEl.innerText).then(() => {
        const orig = btn.innerHTML;
        btn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg> 已複製';
        btn.style.color = '#10b981';
        setTimeout(() => {
            btn.innerHTML = orig;
            btn.style.color = '';
        }, 2000);
    });
}

// 5. Toggle Raw Mermaid Code
function toggleRawCode(btn) {
    const card = btn.closest('.diagram-card');
    const canvas = card.querySelector('.diagram-canvas');
    const rawPanel = card.querySelector('.raw-code-panel');
    if (rawPanel.style.display === 'none') {
        rawPanel.style.display = 'block';
        canvas.style.display = 'none';
        btn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg> 圖表';
    } else {
        rawPanel.style.display = 'none';
        canvas.style.display = 'flex';
        btn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg> 語法';
    }
}

// 6. Diagram Zoom Modal
function openDiagramModal(diagramId) {
    const card = document.getElementById(diagramId);
    if (!card) return;
    const svg = card.querySelector('.mermaid-output svg');
    if (!svg) return;

    const modal = document.getElementById('diagram-modal');
    const target = document.getElementById('diagram-modal-target');
    target.innerHTML = svg.outerHTML;
    modal.classList.add('active');
}

function closeDiagramModal() {
    const modal = document.getElementById('diagram-modal');
    if (modal) modal.classList.remove('active');
}

function closeDiagramModalOnOverlay(e) {
    if (e.target.id === 'diagram-modal') {
        closeDiagramModal();
    }
}

// 6.5 Image Zoom Modal
function openImageModal(el) {
    let img = null;
    if (el.tagName === 'IMG') {
        img = el;
    } else {
        const card = el.closest('.image-card');
        if (card) img = card.querySelector('img');
    }
    if (!img) return;
    const modal = document.getElementById('diagram-modal');
    const target = document.getElementById('diagram-modal-target');
    target.innerHTML = '<div style="text-align:center; padding:10px;"><img src="' + img.src + '" style="max-width:100%; max-height:80vh; object-fit:contain; border-radius:8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);" /><div style="margin-top:12px; font-weight:600; color:var(--text-secondary);">' + escapeHtml(img.alt || '') + '</div></div>';
    modal.classList.add('active');
}

// 7. Full Text Search
function openSearchModal() {
    const modal = document.getElementById('search-modal');
    modal.classList.add('active');
    setTimeout(() => {
        const input = document.getElementById('search-query-input');
        if (input) input.focus();
    }, 100);
}

function closeSearchModal() {
    const modal = document.getElementById('search-modal');
    if (modal) modal.classList.remove('active');
}

function closeSearchModalOnOverlay(e) {
    if (e.target.id === 'search-modal') {
        closeSearchModal();
    }
}

// Ctrl + K shortcut
window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openSearchModal();
    }
    if (e.key === 'Escape') {
        closeSearchModal();
        closeDiagramModal();
    }
});

function executeSearch() {
    const input = document.getElementById('search-query-input');
    const query = input ? input.value.trim() : '';
    const resultsBox = document.getElementById('search-results-box');
    if (!resultsBox) return;

    if (!query) {
        resultsBox.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-muted); font-size: 13px;">請輸入關鍵字進行搜尋</div>';
        return;
    }

    const qLower = query.toLowerCase();
    const results = [];

    if (window.TAB_DOCS && Array.isArray(window.TAB_DOCS)) {
        window.TAB_DOCS.forEach(doc => {
            const text = doc.plain_text;
            const lower = text.toLowerCase();
            let pos = lower.indexOf(qLower);
            let count = 0;
            while (pos !== -1 && count < 3) {
                const start = Math.max(0, pos - 50);
                const end = Math.min(text.length, pos + query.length + 60);
                let snippet = text.substring(start, end).trim();
                
                const regex = new RegExp('(' + query.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&') + ')', 'gi');
                snippet = snippet.replace(regex, '<mark>$1</mark>');

                results.push({
                    tab_id: doc.tab_id,
                    tab_title: doc.tab_title,
                    snippet: (start > 0 ? '...' : '') + snippet + (end < text.length ? '...' : '')
                });

                count++;
                pos = lower.indexOf(qLower, pos + query.length + 10);
            }
        });
    }

    if (results.length === 0) {
        resultsBox.innerHTML = '<div style="padding: 24px; text-align: center; color: var(--text-muted); font-size: 13px;">查無與「<b>' + escapeHtml(query) + '</b>」相符的內容</div>';
        return;
    }

    let outHtml = '';
    results.forEach(res => {
        outHtml += `
        <div class="search-result-item" onclick="jumpToSearchResult('${res.tab_id}')">
            <div class="res-tab-title">章節：${res.tab_title}</div>
            <div class="res-snippet">${res.snippet}</div>
        </div>
        `;
    });
    resultsBox.innerHTML = outHtml;
}

function jumpToSearchResult(tabId) {
    closeSearchModal();
    switchTab(tabId);
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// 8. Theme Toggle
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    try {
        localStorage.setItem('owasp_theme', next);
    } catch(e) {}
    updateThemeIcon(next);
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('theme-icon');
    if (!icon) return;
    if (theme === 'light') {
        icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';
    } else {
        icon.innerHTML = '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>';
    }
}

// Init Saved Theme
try {
    const savedTheme = localStorage.getItem('owasp_theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    }
} catch(e) {}
"""

def build_full_html():
    parsed_tabs = []
    for cfg in FILES_CONFIG:
        path = os.path.join(SOURCE_DIR, cfg["filename"])
        parsed = convert_md_file(path, cfg)
        parsed_tabs.append(parsed)

    # Generate Tab Navigation Buttons
    nav_tabs_html = []
    for idx, t in enumerate(parsed_tabs):
        cfg = t["tab_cfg"]
        active_cls = "active" if idx == 0 else ""
        nav_tabs_html.append(f'''
        <button class="nav-tab-btn {active_cls}" data-tab="{cfg['tab_id']}" onclick="switchTab('{cfg['tab_id']}')" role="tab" aria-selected="{str(idx==0).lower()}" tabindex="0">
            <span class="tab-icon">{cfg['icon']}</span>
            <div class="tab-label-group">
                <div class="tab-title-line">
                    <span class="tab-num">{cfg['tab_num']}</span>
                    <span class="tab-main-title">{cfg['title']}</span>
                </div>
                <div class="tab-subtitle-line">{cfg['subtitle']}</div>
            </div>
            <span class="tab-badge badge-{cfg['badge_color']}">{cfg['badge']}</span>
        </button>
        ''')

    # Generate Tab Content Panes
    tab_panes_html = []
    total_tabs = len(parsed_tabs)
    for idx, t in enumerate(parsed_tabs):
        cfg = t["tab_cfg"]
        fm = t["frontmatter"]
        active_cls = "active" if idx == 0 else ""

        tags_list = fm.get("tags", [])
        if isinstance(tags_list, str):
            tags_list = [tags_list]
        tags_html = "".join([f'<span class="tag-pill">#{tag}</span>' for tag in tags_list])

        toc_items = []
        for h in t["headings"]:
            lvl_cls = f"toc-level-{h['level']}"
            toc_items.append(f'<a href="#{h["id"]}" class="toc-link {lvl_cls}" onclick="scrollToHeading(event, \'{h["id"]}\')">{h["text"]}</a>')
        toc_html = "\n".join(toc_items) if toc_items else '<div class="toc-empty">無小節標題</div>'

        ql_items = []
        for other_cfg in FILES_CONFIG:
            cur_cls = "ql-current" if other_cfg['tab_id'] == cfg['tab_id'] else ""
            ql_items.append(f'''
            <a href="#{other_cfg['tab_id']}" class="ql-item {cur_cls}" onclick="switchTab('{other_cfg['tab_id']}', event)">
                <span class="ql-icon">{other_cfg['icon']}</span>
                <span class="ql-name">{other_cfg['tab_num']}. {other_cfg['title']}</span>
            </a>
            ''')
        ql_html = "".join(ql_items)

        prev_btn = ""
        if idx > 0:
            prev_cfg = parsed_tabs[idx - 1]["tab_cfg"]
            prev_btn = f'''
            <button class="pager-btn pager-prev" onclick="switchTab('{prev_cfg['tab_id']}')">
                <span class="pager-arrow">←</span>
                <div class="pager-text">
                    <span class="pager-hint">上一章節</span>
                    <span class="pager-target">{prev_cfg['tab_num']}. {prev_cfg['title']}</span>
                </div>
            </button>
            '''
        next_btn = ""
        if idx < total_tabs - 1:
            next_cfg = parsed_tabs[idx + 1]["tab_cfg"]
            next_btn = f'''
            <button class="pager-btn pager-next" onclick="switchTab('{next_cfg['tab_id']}')">
                <div class="pager-text">
                    <span class="pager-hint">下一章節</span>
                    <span class="pager-target">{next_cfg['tab_num']}. {next_cfg['title']}</span>
                </div>
                <span class="pager-arrow">→</span>
            </button>
            '''

        pane_html = f'''
        <div class="tab-pane {active_cls}" id="{cfg['tab_id']}" role="tabpanel">
            <div class="pane-layout">
                <main class="pane-main-content">
                    <div class="note-hero">
                        <div class="hero-header-line">
                            <span class="hero-badge badge-{cfg['badge_color']}">{cfg['badge']}</span>
                            <span class="hero-date"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg> 建立日期：{fm.get('date', '2026-09-18')}</span>
                            <span class="hero-vault-label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg> 筆記：<code>{cfg['filename']}</code></span>
                        </div>
                        <h1 class="hero-title"><span class="hero-icon">{cfg['icon']}</span> {fm.get('title', cfg['title'])}</h1>
                        <p class="hero-desc">{cfg['summary']}</p>
                        <div class="hero-tags">
                            {tags_html}
                        </div>
                    </div>

                    <article class="markdown-article">
                        {t['html_content']}
                    </article>

                    <div class="pane-pager">
                        {prev_btn}
                        {next_btn}
                    </div>
                </main>

                <aside class="pane-sidebar">
                    <div class="sidebar-sticky-wrapper">
                        <div class="sidebar-box toc-box">
                            <div class="sidebar-box-header">
                                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
                                <span>章節目錄 (TOC)</span>
                            </div>
                            <nav class="toc-nav">
                                {toc_html}
                            </nav>
                        </div>

                        <div class="sidebar-box quicklink-box">
                            <div class="sidebar-box-header">
                                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                                <span>體系專題導航</span>
                            </div>
                            <div class="quicklink-list">
                                {ql_html}
                            </div>
                        </div>

                        <div class="sidebar-box vault-box">
                            <div class="vault-info">
                                <div class="vault-badge">OBSIDIAN SOURCE FILE</div>
                                <div class="vault-path">Harness / OWASP LLM Guardrail Design</div>
                                <div class="vault-file"><code>{cfg['filename']}</code></div>
                            </div>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
        '''
        tab_panes_html.append(pane_html)

    def extract_clean_text(html_str):
        # Remove script and style
        cleaned = re.sub(r'<(script|style)[^>]*>[\s\S]*?</\1>', ' ', html_str)
        # Remove tags
        cleaned = re.sub(r'<[^>]+>', ' ', cleaned)
        # Unescape HTML entities
        cleaned = html.unescape(cleaned)
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip()

    tab_docs_json = json.dumps([
        {
            "tab_id": t["tab_cfg"]["tab_id"],
            "tab_title": t["tab_cfg"]["tab_num"] + ". " + t["tab_cfg"]["title"],
            "plain_text": extract_clean_text(t["html_content"])
        } for t in parsed_tabs
    ], ensure_ascii=False)

    html_page = """<!DOCTYPE html>
<html lang="zh-Hant" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OWASP AI 護欄體系設計知識庫 (LLM · Agentic · Skills)</title>
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700;800&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    
    <!-- Mermaid.js -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        if (window.mermaid) {
            mermaid.initialize({
                startOnLoad: false,
                theme: 'dark',
                securityLevel: 'loose',
                themeVariables: {
                    darkMode: true,
                    background: '#151c2c',
                    primaryColor: '#6366f1',
                    primaryTextColor: '#f0f4fc',
                    primaryBorderColor: '#4f46e5',
                    lineColor: '#818cf8',
                    secondaryColor: '#1e293b',
                    tertiaryColor: '#0a0d14'
                }
            });
        }
    </script>

    <!-- MathJax -->
    <script>
        window.MathJax = {
            options: {
                ignoreHtmlClass: 'tex2jax_ignore|diagram-card|diagram-canvas|mermaid-diagram-box|mermaid-output|code-wrapper|raw-code-panel',
                processHtmlClass: 'tex2jax_process'
            },
            tex: {
                inlineMath: [['$', '$']],
                displayMath: [['$$', '$$']]
            },
            svg: { fontCache: 'global' }
        };
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>

    <style>
        :root {
            --bg-base: #0a0d14;
            --bg-elevated: #101522;
            --bg-card: #151c2c;
            --bg-card-hover: #1c2538;
            --bg-input: #121826;
            --border-subtle: #222d42;
            --border-strong: #334466;
            
            --text-primary: #f0f4fc;
            --text-secondary: #9cb1d1;
            --text-muted: #64748b;
            
            --primary: #6366f1;
            --primary-light: #818cf8;
            --primary-glow: rgba(99, 102, 241, 0.25);
            
            --cyan: #06b6d4;
            --cyan-glow: rgba(6, 182, 212, 0.2);
            --emerald: #10b981;
            --amber: #f59e0b;
            --rose: #f43f5e;
            --purple: #a855f7;

            --code-bg: #070a10;
            --font-sans: 'Inter', 'Noto Sans TC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            --font-mono: 'Fira Code', Consolas, Monaco, monospace;
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
            --radius-xl: 20px;
            --transition-smooth: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
        }

        [data-theme="light"] {
            --bg-base: #f5f7fb;
            --bg-elevated: #ffffff;
            --bg-card: #ffffff;
            --bg-card-hover: #f8fafc;
            --bg-input: #f1f5f9;
            --border-subtle: #e2e8f0;
            --border-strong: #cbd5e1;
            
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #94a3b8;
            
            --primary: #4f46e5;
            --primary-light: #6366f1;
            --primary-glow: rgba(79, 70, 229, 0.15);
            
            --cyan: #0891b2;
            --cyan-glow: rgba(8, 145, 178, 0.15);
            --emerald: #059669;
            --amber: #d97706;
            --rose: #e11d48;
            --purple: #9333ea;

            --code-bg: #f8fafc;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: var(--font-sans);
            background-color: var(--bg-base);
            color: var(--text-primary);
            line-height: 1.75;
            font-size: 15px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-base);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--border-strong);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary-light);
        }

        /* App Header */
        header.app-header {
            position: sticky;
            top: 0;
            z-index: 1000;
            background: rgba(16, 21, 34, 0.9);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-subtle);
        }
        [data-theme="light"] header.app-header {
            background: rgba(255, 255, 255, 0.9);
        }

        .header-container {
            max-width: 1560px;
            margin: 0 auto;
            padding: 12px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }

        .brand-section {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .brand-logo-badge {
            width: 44px;
            height: 44px;
            border-radius: var(--radius-md);
            background: linear-gradient(135deg, #4f46e5, #06b6d4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            box-shadow: 0 4px 14px var(--primary-glow);
            color: #fff;
        }

        .brand-text-group {
            display: flex;
            flex-direction: column;
        }

        .brand-title {
            font-size: 17.5px;
            font-weight: 800;
            letter-spacing: -0.3px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .brand-version-tag {
            font-size: 11px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 999px;
            background: var(--primary-glow);
            color: var(--primary-light);
            border: 1px solid var(--primary);
        }

        .brand-subtitle {
            font-size: 12px;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .btn-search-trigger {
            display: flex;
            align-items: center;
            gap: 8px;
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 8px 14px;
            border-radius: var(--radius-md);
            font-size: 13px;
            cursor: pointer;
            transition: var(--transition-smooth);
        }
        .btn-search-trigger:hover {
            border-color: var(--primary-light);
            color: var(--text-primary);
            box-shadow: 0 0 10px var(--primary-glow);
        }
        .kbd-shortcut {
            background: var(--bg-base);
            border: 1px solid var(--border-strong);
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 10.5px;
            font-family: var(--font-mono);
            color: var(--text-muted);
        }

        .btn-action-icon {
            width: 36px;
            height: 36px;
            border-radius: var(--radius-md);
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: var(--transition-smooth);
        }
        .btn-action-icon:hover {
            color: var(--text-primary);
            border-color: var(--primary-light);
            background: var(--bg-card-hover);
        }

        /* Tab Navigation Bar */
        nav.tab-nav-bar {
            position: sticky;
            top: 69px;
            z-index: 990;
            background: var(--bg-elevated);
            border-bottom: 1px solid var(--border-subtle);
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
        }

        .tab-nav-container {
            max-width: 1560px;
            margin: 0 auto;
            padding: 8px 24px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            overflow-x: auto;
        }

        .nav-tab-btn {
            background: transparent;
            border: 1px solid transparent;
            border-radius: var(--radius-md);
            padding: 10px 14px;
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            transition: var(--transition-smooth);
            text-align: left;
            position: relative;
            user-select: none;
            color: var(--text-secondary);
        }

        .nav-tab-btn:hover {
            background: var(--bg-card);
            color: var(--text-primary);
            border-color: var(--border-subtle);
        }

        .nav-tab-btn.active {
            background: var(--bg-card);
            border-color: var(--primary);
            box-shadow: 0 4px 16px var(--primary-glow);
            color: var(--text-primary);
        }

        .nav-tab-btn.active::after {
            content: '';
            position: absolute;
            bottom: -9px;
            left: 12px;
            right: 12px;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--cyan));
            border-radius: 3px 3px 0 0;
        }

        .tab-icon {
            font-size: 22px;
            line-height: 1;
            flex-shrink: 0;
        }

        .tab-label-group {
            display: flex;
            flex-direction: column;
            overflow: hidden;
            flex-grow: 1;
        }

        .tab-title-line {
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .tab-num {
            font-size: 12px;
            font-family: var(--font-mono);
            font-weight: 700;
            color: var(--primary-light);
        }

        .tab-main-title {
            font-size: 13.5px;
            font-weight: 700;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .tab-subtitle-line {
            font-size: 11px;
            color: var(--text-muted);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .nav-tab-btn.active .tab-subtitle-line {
            color: var(--text-secondary);
        }

        .tab-badge {
            font-size: 10px;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 999px;
            white-space: nowrap;
            flex-shrink: 0;
        }

        .badge-purple {
            background: rgba(168, 85, 247, 0.15);
            color: #c084fc;
            border: 1px solid rgba(168, 85, 247, 0.4);
        }
        .badge-blue {
            background: rgba(99, 102, 241, 0.15);
            color: #818cf8;
            border: 1px solid rgba(99, 102, 241, 0.4);
        }
        .badge-emerald {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }
        .badge-amber {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.4);
        }
        .badge-cyan {
            background: rgba(6, 182, 212, 0.15);
            color: #22d3ee;
            border: 1px solid rgba(6, 182, 212, 0.4);
        }
        .badge-rose {
            background: rgba(244, 63, 94, 0.15);
            color: #fb7185;
            border: 1px solid rgba(244, 63, 94, 0.4);
        }

        /* Workspace Wrapper */
        .workspace-wrapper {
            flex-grow: 1;
            max-width: 1560px;
            margin: 0 auto;
            width: 100%;
            padding: 24px;
        }

        .tab-pane {
            display: none;
            animation: fadeIn 0.25s ease;
        }

        .tab-pane.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .pane-layout {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 300px;
            gap: 28px;
            align-items: start;
        }

        /* Hero Banner */
        .note-hero {
            background: linear-gradient(135deg, var(--bg-card), var(--bg-elevated));
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 28px 32px;
            margin-bottom: 28px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        }
        .note-hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, var(--primary), var(--cyan));
        }

        .hero-header-line {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }

        .hero-badge {
            font-size: 11px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 999px;
            text-transform: uppercase;
        }

        .hero-date, .hero-vault-label {
            font-size: 12.5px;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 6px;
            font-family: var(--font-mono);
        }

        .hero-title {
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -0.4px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--text-primary);
        }

        .hero-icon {
            font-size: 26px;
        }

        .hero-desc {
            font-size: 14.5px;
            color: var(--text-secondary);
            margin-bottom: 16px;
            line-height: 1.6;
        }

        .hero-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .tag-pill {
            background: var(--bg-base);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            font-size: 11.5px;
            font-family: var(--font-mono);
            padding: 3px 9px;
            border-radius: var(--radius-sm);
            transition: var(--transition-smooth);
        }
        .tag-pill:hover {
            color: var(--primary-light);
            border-color: var(--primary);
        }

        /* Markdown Article */
        .markdown-article {
            font-size: 15px;
            line-height: 1.8;
            color: var(--text-primary);
        }

        .markdown-article h1,
        .markdown-article h2,
        .markdown-article h3,
        .markdown-article h4 {
            color: var(--text-primary);
            font-weight: 700;
            margin-top: 2em;
            margin-bottom: 0.8em;
            position: relative;
        }

        .markdown-article h1 {
            font-size: 24px;
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 8px;
        }

        .markdown-article h2 {
            font-size: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 6px;
        }

        .markdown-article h3 {
            font-size: 17px;
            color: var(--text-primary);
        }

        .heading-anchor {
            opacity: 0;
            color: var(--primary-light);
            text-decoration: none;
            margin-right: 6px;
            font-weight: 400;
            transition: var(--transition-smooth);
        }
        .anchor-heading:hover .heading-anchor {
            opacity: 1;
        }

        .markdown-article p {
            margin-bottom: 1.2em;
        }

        .markdown-article ul,
        .markdown-article ol {
            margin-bottom: 1.2em;
            padding-left: 24px;
        }

        .markdown-article li {
            margin-bottom: 0.4em;
        }

        .markdown-article hr {
            border: 0;
            height: 1px;
            background: var(--border-subtle);
            margin: 28px 0;
        }

        .markdown-article strong {
            color: var(--text-primary);
            font-weight: 700;
        }

        .markdown-article code:not(pre code) {
            font-family: var(--font-mono);
            background: var(--code-bg);
            border: 1px solid var(--border-subtle);
            color: #38bdf8;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 13.5px;
        }
        [data-theme="light"] .markdown-article code:not(pre code) {
            color: #0284c7;
        }

        /* Markdown Tables */
        .table-container {
            width: 100%;
            overflow-x: auto;
            margin: 24px 0;
            background: var(--bg-card);
            border-radius: var(--radius-md);
            border: 1px solid var(--border-subtle);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
        }

        .markdown-article table {
            width: 100%;
            border-collapse: collapse;
            margin: 0;
            font-size: 13.5px;
            text-align: left;
        }

        .markdown-article thead {
            background: var(--bg-elevated);
        }

        .markdown-article th {
            background: var(--bg-elevated);
            color: var(--text-primary);
            font-weight: 700;
            text-align: left;
            padding: 13px 16px;
            border-bottom: 2px solid var(--border-strong);
            white-space: nowrap;
            position: static !important;
            top: auto !important;
            z-index: 1;
        }

        .markdown-article td {
            padding: 13px 16px;
            border-bottom: 1px solid var(--border-subtle);
            vertical-align: top;
            color: var(--text-secondary);
            line-height: 1.65;
        }

        .markdown-article tbody tr:nth-child(even) td {
            background: rgba(255, 255, 255, 0.015);
        }

        [data-theme="light"] .markdown-article tbody tr:nth-child(even) td {
            background: rgba(0, 0, 0, 0.02);
        }

        .markdown-article tbody tr:last-child td {
            border-bottom: none;
        }

        .markdown-article tbody tr:hover td {
            background: var(--bg-card-hover);
            color: var(--text-primary);
        }

        /* 1st column styling in OWASP tables */
        .markdown-article td:first-child strong {
            color: var(--primary-light);
            font-size: 13.5px;
        }

        /* Status Badges */
        .status-badge {
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
            white-space: nowrap;
            margin: 2px 0;
        }
        .badge-block, .badge-reject, .badge-deny {
            background: rgba(244, 63, 94, 0.16);
            color: #fda4af;
            border: 1px solid rgba(244, 63, 94, 0.4);
        }
        .badge-mask, .badge-filter {
            background: rgba(6, 182, 212, 0.16);
            color: #67e8f9;
            border: 1px solid rgba(6, 182, 212, 0.4);
        }
        .badge-sanitize, .badge-circuit {
            background: rgba(168, 85, 247, 0.16);
            color: #d8b4fe;
            border: 1px solid rgba(168, 85, 247, 0.4);
        }
        .badge-hitl, .badge-freeze, .badge-drop, .badge-deprecate {
            background: rgba(245, 158, 11, 0.16);
            color: #fde68a;
            border: 1px solid rgba(245, 158, 11, 0.4);
        }
        .badge-sandbox, .badge-pass {
            background: rgba(16, 185, 129, 0.16);
            color: #6ee7b7;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }

        /* Obsidian Wikilink */
        .wikilink {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background: rgba(99, 102, 241, 0.12);
            color: var(--primary-light);
            border: 1px solid rgba(99, 102, 241, 0.35);
            padding: 2px 7px;
            border-radius: var(--radius-sm);
            text-decoration: none;
            font-weight: 600;
            font-size: 13.5px;
            transition: var(--transition-smooth);
        }
        .wikilink:hover {
            background: var(--primary);
            color: #ffffff;
            box-shadow: 0 2px 10px var(--primary-glow);
            transform: translateY(-1px);
        }
        .wikilink-icon {
            font-size: 11px;
        }

        .ascii-art-pre .wikilink {
            font-family: var(--font-sans);
            font-size: 12px;
            padding: 1px 7px;
            vertical-align: middle;
            margin: 0 4px;
        }

        /* Callouts */
        .callout {
            border-radius: var(--radius-md);
            padding: 16px 20px;
            margin: 20px 0;
            background: var(--bg-card);
            border-left: 4px solid var(--primary);
            border: 1px solid var(--border-subtle);
            border-left-width: 4px;
        }
        .callout-header {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            font-size: 14.5px;
            margin-bottom: 8px;
            color: var(--text-primary);
        }
        .callout-body {
            font-size: 14px;
            color: var(--text-secondary);
        }
        .callout-note {
            border-left-color: var(--cyan);
            background: rgba(6, 182, 212, 0.05);
        }
        .callout-tip {
            border-left-color: var(--emerald);
            background: rgba(16, 185, 129, 0.05);
        }
        .callout-warning {
            border-left-color: var(--amber);
            background: rgba(245, 158, 11, 0.05);
        }

        /* Code Blocks */
        .code-wrapper {
            margin: 20px 0;
            border-radius: var(--radius-md);
            background: var(--code-bg);
            border: 1px solid var(--border-subtle);
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
        }

        .code-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 14px;
            background: var(--bg-elevated);
            border-bottom: 1px solid var(--border-subtle);
            font-size: 11.5px;
            font-family: var(--font-mono);
            color: var(--text-muted);
        }

        .code-lang {
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 600;
            color: var(--text-secondary);
        }

        .lang-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--cyan);
        }

        .copy-code-btn {
            background: transparent;
            border: 1px solid var(--border-subtle);
            border-radius: 4px;
            color: var(--text-secondary);
            font-size: 11px;
            padding: 3px 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
            transition: var(--transition-smooth);
        }
        .copy-code-btn:hover {
            background: var(--primary-glow);
            color: var(--primary-light);
            border-color: var(--primary);
        }

        .markdown-article pre {
            margin: 0;
            padding: 16px;
            overflow-x: auto;
            font-family: var(--font-mono);
            font-size: 13px;
            line-height: 1.6;
        }

        /* ASCII Art Box */
        .ascii-art-wrapper {
            border-color: var(--border-strong);
            background: #06090f;
        }
        .ascii-art-pre {
            font-family: var(--font-mono) !important;
            font-size: 12.5px !important;
            line-height: 1.35 !important;
            color: #7dd3fc;
            padding: 18px !important;
        }
        [data-theme="light"] .ascii-art-pre {
            color: #0369a1;
        }

        /* Diagrams */
        .diagram-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            margin: 28px 0;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }

        .diagram-toolbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 16px;
            background: var(--bg-elevated);
            border-bottom: 1px solid var(--border-subtle);
        }

        .diagram-label {
            font-size: 12.5px;
            font-weight: 700;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .diagram-btn-group {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .tool-btn {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            border-radius: 4px;
            font-size: 11.5px;
            padding: 4px 8px;
            display: flex;
            align-items: center;
            gap: 4px;
            cursor: pointer;
            transition: var(--transition-smooth);
        }
        .tool-btn:hover {
            color: var(--primary-light);
            border-color: var(--primary);
        }

        .diagram-canvas {
            padding: 24px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow-x: auto;
            background: var(--code-bg);
            min-height: 220px;
        }

        .mermaid-diagram-box {
            width: 100%;
            display: flex;
            justify-content: center;
        }
        .mermaid-output {
            width: 100%;
            display: flex;
            justify-content: center;
        }
        .mermaid-output svg {
            max-width: 100% !important;
            height: auto !important;
        }

        .mermaid-loading {
            color: var(--text-muted);
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 20px;
        }

        .loading-spinner {
            width: 14px;
            height: 14px;
            border: 2px solid var(--border-strong);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .diagram-error {
            color: var(--rose);
            padding: 16px;
            font-size: 12.5px;
            background: rgba(244, 63, 94, 0.08);
            border-radius: var(--radius-sm);
        }

        .raw-code-panel {
            padding: 16px;
            background: var(--code-bg);
            border-top: 1px solid var(--border-subtle);
            font-family: var(--font-mono);
            font-size: 12px;
            overflow-x: auto;
        }

        /* Image Cards */
        .image-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            margin: 28px 0;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        .image-card:hover {
            border-color: var(--primary);
            box-shadow: 0 8px 30px rgba(99, 102, 241, 0.15);
        }

        .image-toolbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 16px;
            background: var(--bg-elevated);
            border-bottom: 1px solid var(--border-subtle);
        }

        .image-label {
            font-size: 12.5px;
            font-weight: 700;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .image-btn-group {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .image-canvas {
            padding: 24px;
            display: flex;
            justify-content: center;
            align-items: center;
            background: var(--code-bg);
            overflow-x: auto;
        }

        .image-canvas img {
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            cursor: zoom-in;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
        }

        .image-canvas img:hover {
            transform: scale(1.015);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
        }

        .image-caption {
            padding: 10px 16px;
            font-size: 12px;
            color: var(--text-muted);
            text-align: center;
            background: var(--bg-elevated);
            border-top: 1px solid var(--border-subtle);
        }

        /* Pager */
        .pane-pager {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 48px;
            padding-top: 24px;
            border-top: 1px solid var(--border-subtle);
            gap: 16px;
        }

        .pager-btn {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 14px 20px;
            display: flex;
            align-items: center;
            gap: 14px;
            cursor: pointer;
            transition: var(--transition-smooth);
            text-align: left;
            flex: 1;
            max-width: 380px;
        }
        .pager-btn:hover {
            background: var(--bg-card-hover);
            border-color: var(--primary);
            box-shadow: 0 4px 14px var(--primary-glow);
            transform: translateY(-2px);
        }
        .pager-prev {
            margin-right: auto;
        }
        .pager-next {
            margin-left: auto;
            text-align: right;
            justify-content: flex-end;
        }
        .pager-arrow {
            font-size: 18px;
            font-weight: 700;
            color: var(--primary-light);
        }
        .pager-text {
            display: flex;
            flex-direction: column;
        }
        .pager-hint {
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
        }
        .pager-target {
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-primary);
        }

        /* Sticky Sidebar */
        .pane-sidebar {
            position: relative;
        }

        .sidebar-sticky-wrapper {
            position: sticky;
            top: 154px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            max-height: calc(100vh - 170px);
            overflow-y: auto;
            padding-right: 4px;
        }

        .sidebar-box {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 16px;
        }

        .sidebar-box-header {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-subtle);
        }

        /* TOC Nav */
        .toc-nav {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .toc-link {
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 12.5px;
            line-height: 1.5;
            padding: 5px 8px;
            border-radius: var(--radius-sm);
            transition: var(--transition-smooth);
            border-left: 2px solid transparent;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .toc-link:hover {
            color: var(--primary-light);
            background: var(--bg-card-hover);
        }

        .toc-link.active {
            color: var(--primary-light);
            font-weight: 600;
            border-left-color: var(--primary);
            background: var(--primary-glow);
        }

        .toc-level-2 {
            padding-left: 8px;
            font-weight: 600;
        }

        .toc-level-3 {
            padding-left: 18px;
            font-size: 12px;
            color: var(--text-muted);
        }

        /* Quick Links */
        .quicklink-list {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .ql-item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 10px;
            border-radius: var(--radius-sm);
            text-decoration: none;
            color: var(--text-secondary);
            font-size: 12px;
            transition: var(--transition-smooth);
        }
        .ql-item:hover {
            background: var(--bg-card-hover);
            color: var(--primary-light);
        }
        .ql-item.ql-current {
            background: var(--primary-glow);
            color: var(--primary-light);
            font-weight: 700;
        }

        /* Vault Box */
        .vault-info {
            font-size: 11.5px;
            color: var(--text-muted);
            line-height: 1.6;
        }
        .vault-badge {
            font-size: 9.5px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: var(--cyan);
            margin-bottom: 4px;
        }
        .vault-path {
            font-family: var(--font-mono);
            word-break: break-all;
            margin-bottom: 4px;
        }
        .vault-file code {
            color: var(--text-primary);
        }

        /* Footer */
        footer.app-footer {
            border-top: 1px solid var(--border-subtle);
            background: var(--bg-elevated);
            padding: 24px;
            margin-top: 48px;
        }

        .footer-inner {
            max-width: 1560px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 12.5px;
            color: var(--text-muted);
            flex-wrap: wrap;
            gap: 12px;
        }

        /* Modal Dialog */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(8px);
            z-index: 2000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .modal-overlay.active {
            display: flex;
        }

        .search-modal {
            background: var(--bg-elevated);
            border: 1px solid var(--border-strong);
            border-radius: var(--radius-lg);
            width: 100%;
            max-width: 640px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            animation: modalPop 0.2s ease;
        }

        @keyframes modalPop {
            from { opacity: 0; transform: scale(0.96); }
            to { opacity: 1; transform: scale(1); }
        }

        .search-input-header {
            display: flex;
            align-items: center;
            padding: 14px 18px;
            border-bottom: 1px solid var(--border-subtle);
            gap: 12px;
        }

        .search-input-header input {
            flex-grow: 1;
            background: transparent;
            border: none;
            outline: none;
            color: var(--text-primary);
            font-size: 15px;
            font-family: var(--font-sans);
        }

        .search-results-list {
            max-height: 420px;
            overflow-y: auto;
            padding: 12px;
        }

        .search-result-item {
            padding: 12px;
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: var(--transition-smooth);
            margin-bottom: 6px;
            border: 1px solid transparent;
        }
        .search-result-item:hover {
            background: var(--bg-card);
            border-color: var(--border-subtle);
        }
        .res-tab-title {
            font-size: 11px;
            color: var(--primary-light);
            font-weight: 700;
            margin-bottom: 4px;
        }
        .res-snippet {
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.5;
        }
        .res-snippet mark {
            background: rgba(245, 158, 11, 0.3);
            color: var(--amber);
            font-weight: 700;
            padding: 0 2px;
            border-radius: 2px;
        }

        .diagram-modal-card {
            background: var(--bg-elevated);
            border: 1px solid var(--border-strong);
            border-radius: var(--radius-lg);
            width: 95vw;
            height: 90vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.6);
        }

        .diagram-modal-header {
            padding: 14px 20px;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .diagram-modal-body {
            flex-grow: 1;
            overflow: auto;
            padding: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--code-bg);
        }
        .diagram-modal-body svg {
            width: 100% !important;
            height: auto !important;
            max-height: 80vh !important;
        }

        /* Floating Back to Top */
        .fab-top {
            position: fixed;
            bottom: 24px;
            right: 24px;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: var(--bg-card);
            border: 1px solid var(--border-strong);
            color: var(--text-primary);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            opacity: 0;
            visibility: hidden;
            transition: var(--transition-smooth);
            z-index: 999;
        }
        .fab-top.show {
            opacity: 1;
            visibility: visible;
        }
        .fab-top:hover {
            background: var(--primary);
            border-color: var(--primary);
            color: #fff;
            transform: translateY(-2px);
        }

        /* Responsive Breakpoints */
        @media (max-width: 1200px) {
            .tab-nav-container {
                grid-template-columns: repeat(2, 1fr);
            }
            .pane-layout {
                grid-template-columns: 1fr;
            }
            .pane-sidebar {
                display: none;
            }
        }

        @media (max-width: 768px) {
            .tab-nav-container {
                grid-template-columns: 1fr;
            }
            .brand-subtitle {
                display: none;
            }
            .hero-title {
                font-size: 20px;
            }
            .pane-pager {
                flex-direction: column;
            }
            .pager-btn {
                max-width: 100%;
            }
        }

        @media print {
            header.app-header,
            nav.tab-nav-bar,
            .pane-sidebar,
            .pane-pager,
            .diagram-toolbar,
            .fab-top {
                display: none !important;
            }
            .tab-pane {
                display: block !important;
                page-break-after: always;
            }
            .workspace-wrapper {
                padding: 0;
                max-width: 100%;
            }
            body {
                background: #fff;
                color: #000;
            }
        }
    </style>
</head>
<body>

    <!-- App Header -->
    <header class="app-header">
        <div class="header-container">
            <div class="brand-section">
                <div class="brand-logo-badge">🛡️</div>
                <div class="brand-text-group">
                    <div class="brand-title">
                        <span>OWASP AI Guardrail Design</span>
                        <span class="brand-version-tag">L1~L5 縱深防禦</span>
                    </div>
                    <div class="brand-subtitle">模型分層 · 資料分級 · 單一閘道 · 致命三要素破除 · 全生命週期留痕</div>
                </div>
            </div>

            <div class="header-actions">
                <button class="btn-search-trigger" onclick="openSearchModal()" title="全庫全文檢索 (Ctrl+K)">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    <span>全庫檢索...</span>
                    <span class="kbd-shortcut">Ctrl+K</span>
                </button>

                <button class="btn-action-icon" id="theme-toggle-btn" onclick="toggleTheme()" title="切換深色/淺色主題">
                    <svg id="theme-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
                </button>

                <button class="btn-action-icon" onclick="window.print()" title="列印或另存 PDF">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
                </button>
            </div>
        </div>
    </header>

    <!-- Tab Navigation Bar -->
    <nav class="tab-nav-bar" role="tablist">
        <div class="tab-nav-container">
            <!-- NAV_TABS_PLACEHOLDER -->
        </div>
    </nav>

    <!-- Main Workspace Area -->
    <div class="workspace-wrapper">
        <!-- TAB_PANES_PLACEHOLDER -->
    </div>

    <!-- App Footer -->
    <footer class="app-footer">
        <div class="footer-inner">
            <div class="footer-left">
                <strong>OWASP LLM Guardrail Design</strong> · Obsidian 知識庫全書數位化轉換交付
            </div>
            <div class="footer-right">
                對齊規範：OWASP Top 10 for LLM (LLM01~10) · OWASP Top 10 for Agentic (ASI01~10) · OWASP AST10 · DISA IL 1~6
            </div>
        </div>
    </footer>

    <!-- Floating Back to Top Button -->
    <button class="fab-top" id="fab-top" onclick="window.scrollTo({top: 0, behavior: 'smooth'})" title="回到頁首">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="18 15 12 9 6 15"></polyline></svg>
    </button>

    <!-- Search Modal -->
    <div class="modal-overlay" id="search-modal" onclick="closeSearchModalOnOverlay(event)">
        <div class="search-modal">
            <div class="search-input-header">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <input type="text" id="search-query-input" placeholder="搜尋關鍵字（例如：致命三要素、JIT、Prompt Injection、gVisor...）" oninput="executeSearch()">
                <button class="btn-action-icon" onclick="closeSearchModal()" title="關閉">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>
            <div class="search-results-list" id="search-results-box">
                <div style="padding: 20px; text-align: center; color: var(--text-muted); font-size: 13px;">
                    請輸入關鍵字進行全文搜尋
                </div>
            </div>
        </div>
    </div>

    <!-- Diagram Zoom Modal -->
    <div class="modal-overlay" id="diagram-modal" onclick="closeDiagramModalOnOverlay(event)">
        <div class="diagram-modal-card">
            <div class="diagram-modal-header">
                <span style="font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 8px;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/></svg>
                    架構圖表放大檢視
                </span>
                <button class="btn-action-icon" onclick="closeDiagramModal()">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>
            <div class="diagram-modal-body" id="diagram-modal-target"></div>
        </div>
    </div>

    <!-- Inject Search Docs -->
    <script>
        window.TAB_DOCS = <!-- TAB_DOCS_JSON_PLACEHOLDER -->;
    </script>

    <!-- Global Client-side Logic -->
    <script>
        <!-- CLIENT_JS_PLACEHOLDER -->
    </script>
</body>
</html>
"""

    html_page = html_page.replace("<!-- NAV_TABS_PLACEHOLDER -->", "".join(nav_tabs_html))
    html_page = html_page.replace("<!-- TAB_PANES_PLACEHOLDER -->", "".join(tab_panes_html))
    html_page = html_page.replace("<!-- TAB_DOCS_JSON_PLACEHOLDER -->", tab_docs_json)
    html_page = html_page.replace("<!-- CLIENT_JS_PLACEHOLDER -->", CLIENT_JAVASCRIPT)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_page)
    with open(NAMED_FILE, "w", encoding="utf-8") as f:
        f.write(html_page)
    print(f"Generated successfully: {OUTPUT_FILE} and {NAMED_FILE}")

if __name__ == "__main__":
    build_full_html()
