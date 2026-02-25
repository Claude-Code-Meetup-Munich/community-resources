#!/usr/bin/env python3
"""Direct Markdown → Notion API upload. No intermediate format.

Parses standard markdown and builds Notion block tree from heading hierarchy.
H1 (toggle) > H2 (toggle) > H3 (toggle) > Content.
First H1 is removed (page title). All others become toggle headings.

Usage:
    uv run upload.py <markdown_file> <page_id> [title]
    uv run upload.py --config <dotted.path> <markdown_file> [title]

Config mode reads the page ID from .claude/config/notion.json.
Example: uv run upload.py --config pages.my-page <markdown_file>
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

# ── Config ────────────────────────────────────────────────────────

def load_config():
    """Load Notion config, searching upward from CWD.
    Checks .notion-config.json (legacy) and .claude/config/notion.json.
    If not found, interactively creates .claude/config/notion.json.
    """
    d = os.getcwd()
    search_dir = d
    while True:
        # Canonical path
        cfg = os.path.join(search_dir, ".claude", "config", "notion.json")
        if os.path.exists(cfg):
            with open(cfg) as f:
                return json.load(f)

        # Legacy path (kept for backward compat)
        cfg_legacy = os.path.join(search_dir, ".notion-config.json")
        if os.path.exists(cfg_legacy):
            with open(cfg_legacy) as f:
                return json.load(f)

        parent = os.path.dirname(search_dir)
        if parent == search_dir:
            break
        search_dir = parent
    
    # Fallback to script dir (e.g. for global install)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_script = os.path.join(script_dir, "config", "notion.json")
    if os.path.exists(cfg_script):
        with open(cfg_script) as f:
            return json.load(f)

    # Interactive Setup
    print("\n[!] Notion configuration not found.")
    print("    Let's set up your .claude/config/notion.json now.\n")
    
    token = input("Enter your Notion Integration Token (secret_...): ").strip()
    if not token:
        print("Aborted.")
        sys.exit(1)
        
    print("\nAdd a target page for uploads (you can add more later manually).")
    page_key = input("Page Key (e.g. 'notes'): ").strip() or "default"
    page_id = input("Page ID (from URL): ").strip()
    
    # Format Page ID if needed (remove hyphens to ensure standard format, then re-hyphenate or just store clean)
    # The API accepts formatted (hyphenated) or raw (no-hyphens).
    # Simplest is to store as given or just ensure it looks like a UUID.
    
    config_data = {
        "token": token,
        "pages": {
            page_key: page_id
        }
    }
    
    cfg_dir = os.path.join(d, ".claude", "config")
    os.makedirs(cfg_dir, exist_ok=True)
    target_cfg = os.path.join(cfg_dir, "notion.json")
    with open(target_cfg, "w") as f:
        json.dump(config_data, f, indent=2)

    print(f"\n[+] Configuration saved to {target_cfg}")
    print(f"    Add .claude/config/notion.json to your .gitignore!")
    return config_data


def resolve_config_path(config, path):
    """Resolve a dotted path like 'pages.interview-guide-ws3.id'."""
    obj = config
    for key in path.split("."):
        if isinstance(obj, dict):
            obj = obj[key]
        else:
            raise KeyError(f"Cannot resolve '{key}' in path '{path}'")
    return obj


# Module level — no interactive side effects at import time
CONFIG = TOKEN = HEADERS = BASE = None
API_VERSION = "2025-09-03"


def _ensure_init():
    global CONFIG, TOKEN, HEADERS, BASE
    if CONFIG is not None:
        return
    CONFIG = load_config()
    TOKEN = CONFIG.get("token", "")
    HEADERS = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": API_VERSION,
    }
    BASE = "https://api.notion.com/v1"


# ── Rich Text ──────────────────────────────────────────────────────

def parse_rich_text(text):
    """Parse markdown inline formatting into Notion rich_text array."""
    segments = []
    pattern = re.compile(
        r'(\*\*\*(.+?)\*\*\*)'
        r'|(\*\*(.+?)\*\*)'
        r'|(\*(.+?)\*)'
        r'|(`([^`]+)`)'
        r'|(\[([^\]]+)\]\(notion://([^)]+)\))'
        r'|(\[([^\]]+)\]\(([^)]+)\))'
    )
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            plain = text[pos:m.start()]
            if plain:
                segments.append({"type": "text", "text": {"content": plain}})
        if m.group(2):
            segments.append({"type": "text", "text": {"content": m.group(2)},
                             "annotations": {"bold": True, "italic": True}})
        elif m.group(4):
            segments.append({"type": "text", "text": {"content": m.group(4)},
                             "annotations": {"bold": True}})
        elif m.group(6):
            segments.append({"type": "text", "text": {"content": m.group(6)},
                             "annotations": {"italic": True}})
        elif m.group(8):
            segments.append({"type": "text", "text": {"content": m.group(8)},
                             "annotations": {"code": True}})
        elif m.group(10):
            segments.append({"type": "mention",
                             "mention": {"page": {"id": m.group(11)}}})
        elif m.group(12):
            segments.append({"type": "text",
                             "text": {"content": m.group(13), "link": {"url": m.group(14)}}})
        pos = m.end()
    if pos < len(text):
        remaining = text[pos:]
        if remaining:
            segments.append({"type": "text", "text": {"content": remaining}})
    if not segments:
        segments.append({"type": "text", "text": {"content": text}})
    return segments


# ── Block Factories ────────────────────────────────────────────────

def mk_paragraph(text):
    return {"type": "paragraph", "paragraph": {"rich_text": parse_rich_text(text)}}

def mk_heading(level, text, toggleable=True):
    key = f"heading_{level}"
    return {"type": key, key: {"rich_text": parse_rich_text(text), "is_toggleable": toggleable}}

def mk_bullet(text):
    return {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": parse_rich_text(text)}}

def mk_numbered(text):
    return {"type": "numbered_list_item", "numbered_list_item": {"rich_text": parse_rich_text(text)}}

def mk_todo(text, checked=False):
    return {"type": "to_do", "to_do": {"rich_text": parse_rich_text(text), "checked": checked}}

def mk_quote(text):
    return {"type": "quote", "quote": {"rich_text": parse_rich_text(text)}}

def mk_code(content, language="plain text"):
    lang_map = {"plaintext": "plain text", "": "plain text"}
    language = lang_map.get(language, language)
    # Notion limits rich_text content to 2000 chars measured by JSON-encoded length.
    # Non-ASCII chars (e.g. ═, ä, 🟡) expand to \uXXXX in JSON (6 chars → 1 Python char).
    # We chunk conservatively: accumulate chars until the JSON-encoded chunk would exceed 1990.
    limit = 1990
    chunks = []
    start = 0
    while start < len(content):
        # Binary search for the largest end such that json_len <= limit
        lo, hi = start, min(start + limit, len(content))
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if len(json.dumps(content[start:mid])) - 2 <= limit:  # -2 for surrounding quotes
                lo = mid
            else:
                hi = mid - 1
        end = lo if lo > start else start + 1  # always advance at least 1 char
        chunks.append(content[start:end])
        start = end
    if not chunks:
        chunks = [""]
    rich_text = [{"type": "text", "text": {"content": c}} for c in chunks]
    return {"type": "code", "code": {
        "rich_text": rich_text,
        "language": language}}

def mk_divider():
    return {"type": "divider", "divider": {}}

def mk_table(rows):
    width = max(len(r) for r in rows) if rows else 1
    table_rows = []
    for row in rows:
        cells = [parse_rich_text(cell.strip()) for cell in row]
        while len(cells) < width:
            cells.append([{"type": "text", "text": {"content": ""}}])
        table_rows.append({"type": "table_row", "table_row": {"cells": cells}})
    return {"type": "table", "table": {
        "table_width": width, "has_column_header": True,
        "has_row_header": False, "children": table_rows}}


# ── Tree Node ──────────────────────────────────────────────────────

class Node:
    def __init__(self, block, children=None):
        self.block = block
        self.children = children or []
    def add(self, child):
        self.children.append(child)


# ── Markdown Parser (hierarchy from heading levels) ────────────────

def parse_lines_to_blocks(lines, start, end):
    """Parse a range of content lines (no headings) into a list of Nodes."""
    nodes = []
    i = start
    while i < end:
        line = lines[i].rstrip("\n").rstrip()

        # Empty
        if not line.strip():
            i += 1
            continue

        # Code block
        if line.lstrip().startswith("```"):
            stripped = line.lstrip()
            lang = stripped[3:].strip()
            code_lines = []
            i += 1
            while i < end:
                cl = lines[i].rstrip("\n")
                if cl.lstrip().startswith("```"):
                    i += 1
                    break
                code_lines.append(cl)
                i += 1
            nodes.append(Node(mk_code("\n".join(code_lines), lang or "plain text")))
            continue

        # Table
        if line.lstrip().startswith("|"):
            table_lines = []
            while i < end and lines[i].rstrip("\n").lstrip().startswith("|"):
                table_lines.append(lines[i].rstrip("\n").lstrip())
                i += 1
            rows = []
            for tl in table_lines:
                if re.match(r'^\|[\s\-:|]+\|$', tl):
                    continue
                cells = [c.strip() for c in tl.split("|")[1:-1]]
                rows.append(cells)
            if rows:
                nodes.append(Node(mk_table(rows)))
            continue

        # Divider
        if line.strip() == "---":
            nodes.append(Node(mk_divider()))
            i += 1
            continue

        # Blockquote (collect consecutive lines, including blank `>` continuation)
        if line.lstrip().startswith("> ") or line.lstrip() == ">":
            quote_parts = []
            while i < end:
                ql = lines[i].rstrip("\n").rstrip()
                stripped_ql = ql.lstrip()
                if stripped_ql.startswith("> "):
                    quote_parts.append(stripped_ql[2:])
                    i += 1
                elif stripped_ql == ">":
                    quote_parts.append("")  # blank line within quote
                    i += 1
                else:
                    break
            # Join with newlines, collapse multiple blanks, strip edges
            text = "\n".join(quote_parts).strip()
            nodes.append(Node(mk_quote(text)))
            continue

        # Checkbox
        stripped = line.lstrip()
        if stripped.startswith("- [x] "):
            nodes.append(Node(mk_todo(stripped[6:], checked=True)))
            i += 1
            continue
        if stripped.startswith("- [ ] "):
            nodes.append(Node(mk_todo(stripped[6:], checked=False)))
            i += 1
            continue

        # Bullet (handle sub-bullets)
        if stripped.startswith("- "):
            bullet_node = Node(mk_bullet(stripped[2:]))
            i += 1
            while i < end:
                next_line = lines[i].rstrip("\n")
                if not next_line.strip():
                    break
                indent = len(next_line) - len(next_line.lstrip())
                if indent >= 2 and next_line.lstrip().startswith("- "):
                    bullet_node.add(Node(mk_bullet(next_line.lstrip()[2:])))
                    i += 1
                else:
                    break
            nodes.append(bullet_node)
            continue

        # Numbered list
        m = re.match(r'^(\d+)\. (.+)', stripped)
        if m:
            nodes.append(Node(mk_numbered(m.group(2))))
            i += 1
            continue

        # Paragraph
        nodes.append(Node(mk_paragraph(stripped)))
        i += 1

    return nodes


def parse_markdown(lines, link_map=None):
    """Parse standard markdown into a tree of Nodes using heading hierarchy.

    H1 = toggle heading, contains H2 sections.
    H2 = toggle heading, contains H3 sections and content.
    H3 = toggle heading, contains content.
    First H1 is removed (becomes Notion page title).
    """
    link_map = link_map or {}

    # Replace internal links in all lines
    if link_map:
        for idx in range(len(lines)):
            for fname, target in link_map.items():
                lines[idx] = lines[idx].replace(f"]({fname})", f"](notion://{target})")
                # Also handle anchor links
                if fname.endswith(".md"):
                    lines[idx] = re.sub(
                        rf'\]\({re.escape(fname)}#[^)]*\)',
                        f'](notion://{target})',
                        lines[idx]
                    )

    # Remove first H1
    first_h1_removed = False
    for i, line in enumerate(lines):
        stripped = line.rstrip("\n").strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            lines[i] = "\n"
            first_h1_removed = True
            break

    # Find all heading positions
    headings = []  # (line_idx, level, title)
    for i, line in enumerate(lines):
        stripped = line.rstrip("\n").strip()
        if stripped.startswith("### "):
            headings.append((i, 3, stripped[4:]))
        elif stripped.startswith("## "):
            headings.append((i, 2, stripped[3:]))
        elif stripped.startswith("# ") and not stripped.startswith("## "):
            headings.append((i, 1, stripped[2:]))

    # Build tree
    top_nodes = []
    processed_until = 0

    for h_idx, (line_idx, level, title) in enumerate(headings):
        # Skip headings already processed as children of a parent heading
        if line_idx < processed_until:
            continue

        # Content before this heading (top-level)
        if line_idx > processed_until:
            top_nodes.extend(parse_lines_to_blocks(lines, processed_until, line_idx))

        if level == 1:
            # H1: plain heading, contains H2s
            next_h1 = None
            for future_idx, future_level, _ in headings[h_idx + 1:]:
                if future_level == 1:
                    next_h1 = future_idx
                    break
            section_end = next_h1 if next_h1 is not None else len(lines)

            # Find H2s within this H1 section
            h2s_in_section = [(li, lv, t) for li, lv, t in headings
                              if li > line_idx and li < section_end and lv == 2]

            h1_node = Node(mk_heading(1, title, toggleable=True))

            # Content between H1 and first H2 (or section end)
            content_start = line_idx + 1
            first_h2 = h2s_in_section[0][0] if h2s_in_section else section_end

            if content_start < first_h2:
                h1_node.children.extend(parse_lines_to_blocks(lines, content_start, first_h2))

            # Process H2s within this H1
            for h2_sub_idx, (h2_line, _, h2_title) in enumerate(h2s_in_section):
                if h2_sub_idx + 1 < len(h2s_in_section):
                    h2_end = h2s_in_section[h2_sub_idx + 1][0]
                else:
                    h2_end = section_end

                # Find H3s within this H2
                h3s_in_h2 = [(li, lv, t) for li, lv, t in headings
                             if li > h2_line and li < h2_end and lv == 3]

                h2_node = Node(mk_heading(2, h2_title))
                h2_content_start = h2_line + 1
                first_h3 = h3s_in_h2[0][0] if h3s_in_h2 else h2_end

                if h2_content_start < first_h3:
                    h2_node.children.extend(parse_lines_to_blocks(lines, h2_content_start, first_h3))

                for h3_sub_idx, (h3_line, _, h3_title) in enumerate(h3s_in_h2):
                    if h3_sub_idx + 1 < len(h3s_in_h2):
                        h3_end = h3s_in_h2[h3_sub_idx + 1][0]
                    else:
                        h3_end = h2_end

                    h3_node = Node(mk_heading(3, h3_title))
                    h3_content_start = h3_line + 1
                    if h3_content_start < h3_end:
                        h3_node.children.extend(parse_lines_to_blocks(lines, h3_content_start, h3_end))
                    h2_node.add(h3_node)

                h1_node.add(h2_node)

            top_nodes.append(h1_node)
            processed_until = section_end

        elif level == 2:
            # Standalone H2 (not inside H1): toggle, contains H3s
            next_h_same_or_higher = None
            for future_idx, future_level, _ in headings[h_idx + 1:]:
                if future_level <= 2:
                    next_h_same_or_higher = future_idx
                    break
            section_end = next_h_same_or_higher if next_h_same_or_higher is not None else len(lines)

            h3s_in_section = [(li, lv, t) for li, lv, t in headings
                              if li > line_idx and li < section_end and lv == 3]

            h2_node = Node(mk_heading(2, title))

            content_start = line_idx + 1
            first_h3 = h3s_in_section[0][0] if h3s_in_section else section_end

            if content_start < first_h3:
                h2_node.children.extend(parse_lines_to_blocks(lines, content_start, first_h3))

            for h3_idx, (h3_line, _, h3_title) in enumerate(h3s_in_section):
                if h3_idx + 1 < len(h3s_in_section):
                    h3_end = h3s_in_section[h3_idx + 1][0]
                else:
                    h3_end = section_end

                h3_node = Node(mk_heading(3, h3_title))
                h3_content_start = h3_line + 1
                if h3_content_start < h3_end:
                    h3_node.children.extend(parse_lines_to_blocks(lines, h3_content_start, h3_end))
                h2_node.add(h3_node)

            top_nodes.append(h2_node)
            processed_until = section_end

        elif level == 3:
            # Standalone H3: toggle
            next_heading = None
            for future_idx, _, _ in headings[h_idx + 1:]:
                next_heading = future_idx
                break
            section_end = next_heading if next_heading is not None else len(lines)

            h3_node = Node(mk_heading(3, title))
            content_start = line_idx + 1
            if content_start < section_end:
                h3_node.children.extend(parse_lines_to_blocks(lines, content_start, section_end))

            top_nodes.append(h3_node)
            processed_until = section_end

    # Remaining content after last heading
    if processed_until < len(lines):
        top_nodes.extend(parse_lines_to_blocks(lines, processed_until, len(lines)))

    return top_nodes


# ── API ────────────────────────────────────────────────────────────

def api_call(method, path, data=None):
    _ensure_init()
    url = BASE + path
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error = e.read().decode()
        print(f"  API ERROR {e.code}: {error[:500]}")
        raise


def clear_page(page_id):
    """Delete all blocks from a page, keeping child_page and child_database."""
    deleted = skipped = 0
    start_cursor = None
    while True:
        url = f"/blocks/{page_id}/children?page_size=100"
        if start_cursor:
            url += f"&start_cursor={start_cursor}"
        result = api_call("GET", url)
        for block in result.get("results", []):
            if block.get("type") in ("child_page", "child_database"):
                skipped += 1
                continue
            try:
                api_call("DELETE", f"/blocks/{block['id']}")
                deleted += 1
            except Exception:
                pass
        if not result.get("has_more"):
            break
        start_cursor = result["next_cursor"]
    print(f"  Cleared {deleted} blocks (kept {skipped} child pages)")


def upload_nodes(parent_id, nodes, depth=0):
    """Upload nodes, then recursively upload children into headings."""
    prefix = "  " * depth
    top_blocks = [n.block for n in nodes if n.block]
    toggle_map = []  # (index_in_batch, node)

    for i, node in enumerate(nodes):
        if node.children and node.block and node.block["type"].startswith("heading_"):
            toggle_map.append((i, node))

    if not top_blocks:
        return

    # Upload in batches of 100
    all_results = []
    for batch_start in range(0, len(top_blocks), 100):
        batch = top_blocks[batch_start:batch_start + 100]
        result = api_call("PATCH", f"/blocks/{parent_id}/children", {"children": batch})
        all_results.extend(result.get("results", []))
        if batch_start > 0:
            time.sleep(0.3)

    print(f"{prefix}Uploaded {len(top_blocks)} blocks to {parent_id[:12]}...")

    # Upload heading children
    for orig_idx, node in toggle_map:
        if orig_idx < len(all_results):
            heading_id = all_results[orig_idx]["id"]
            htype = node.block["type"]
            rt = node.block[htype]["rich_text"]
            title = rt[0].get("text", {}).get("content", "?") if rt else "?"
            print(f"{prefix}  → {htype}: {title[:50]}...")
            upload_nodes(heading_id, node.children, depth + 1)
            time.sleep(0.15)


# ── Main ───────────────────────────────────────────────────────────

def upload_file(filepath, page_id, title, link_map=None, append=False):
    print(f"\n{'='*60}")
    print(f"{'Appending' if append else 'Uploading'}: {title}")
    print(f"Source: {filepath}")
    print(f"Page: {page_id}")
    print(f"{'='*60}")

    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    nodes = parse_markdown(lines, link_map)
    print(f"Parsed: {len(nodes)} top-level blocks")

    if not append:
        clear_page(page_id)
    upload_nodes(page_id, nodes)
    print(f"Done: {title}")


if __name__ == "__main__":
    args = sys.argv[1:]

    append = "--append" in args
    if append:
        args.remove("--append")

    if "--config" in args:
        ci = args.index("--config")
        config_path = args[ci + 1]
        remaining = args[:ci] + args[ci + 2:]
        _ensure_init()
        page_id = resolve_config_path(CONFIG, config_path)
        filepath = remaining[0]
        title = remaining[1] if len(remaining) > 1 else "Untitled"
    else:
        filepath = args[0]
        page_id = args[1]
        title = args[2] if len(args) > 2 else "Untitled"

    upload_file(filepath, page_id, title, append=append)
