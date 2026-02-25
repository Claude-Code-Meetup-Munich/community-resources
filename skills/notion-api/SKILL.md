---
name: notion-api
description: Notion API integration via curl for reading pages, editing blocks, managing comments, and querying databases. Use when you need to interact with Notion pages, retrieve or modify block content, read/write comments, query databases, or upload markdown to Notion.
allowed_tools: bash, read, write
argument_hint: "[Describe the Notion task]"
---

# Notion API Skill

## Setup

Config file: `.claude/config/notion.json` (standard path in every project).

```json
{
  "token": "ntn_...",
  "pages": {
    "my-page": { "id": "page-id" }
  },
  "databases": {
    "tasks": {
      "database_id": "...",
      "data_source_id": "..."
    }
  }
}
```

> ⚠️ Add `.claude/config/notion.json` to your `.gitignore` — it contains your integration token.

## Authentication

- **API Token:** Read from `.claude/config/notion.json`
- **API Version:** `2025-09-03`
- **Base URL:** `https://api.notion.com/v1`

### Standard Headers for All Requests

Load the token using `jq`:

```bash
TOKEN=$(jq -r .token .claude/config/notion.json)

-H "Authorization: Bearer $TOKEN" \
-H 'Content-Type: application/json' \
-H 'Notion-Version: 2025-09-03'
```

**Important:** Always use single quotes for header values. Double quotes with shell variables cause `blank argument` errors.

## Page IDs

All relevant Notion page IDs are cached in `.claude/config/notion.json` under `pages`.

Structure: `pages.<page-key>.id`

Before each Notion operation, read the config and look up the required ID:

```bash
PAGE_ID=$(jq -r '.pages.my_page.id' .claude/config/notion.json)
```

### Auto-Caching New Page IDs

When working with a page not yet in the config, automatically add its ID to `.claude/config/notion.json` using a descriptive slug (e.g., `meeting-notes`, `project-overview`):

```bash
# Example: Cache new page
jq '.pages["briefing-sales-assistant"] = {"id": "30ad8531-f4ae-80a8-940a-c2585842da40"}' \
  .claude/config/notion.json > /tmp/notion-config-tmp.json && \
  mv /tmp/notion-config-tmp.json .claude/config/notion.json
```

Apply this for all page ID sources: user URLs, API responses, or config lookups.

## Data Sources

Starting with API version `2025-09-03`, Notion uses a **Data Source model**. Databases consist of separate "Data Sources". Pages have `parent.type = "data_source_id"`.

**Concept:** Database → Data Source → Pages

- `GET /v1/data_sources/{id}` — Retrieve schema/properties (property names, types, select options)
- `POST /v1/data_sources/{id}/query` — Query pages (filters, sort, pagination)
- Page creation: `parent: { "data_source_id": "<id>" }` instead of `database_id`

### Config: `databases` Section

Data Source IDs are stored in `.claude/config/notion.json` under `databases`:

```json
{
  "databases": {
    "tasks": {
      "database_id": "...",
      "data_source_id": "..."
    },
    "projects": {
      "database_id": "...",
      "data_source_id": "..."
    }
  }
}
```

Access:

```bash
TASKS_DS=$(jq -r '.databases.tasks.data_source_id' .claude/config/notion.json)
PROJECTS_DS=$(jq -r '.databases.projects.data_source_id' .claude/config/notion.json)
```

### Auto-Detection

When `GET /v1/pages/{id}` returns `parent.type = "data_source_id"`, automatically cache the `data_source_id` in the config (similar to page ID caching).

## API Reference

Detailed endpoint references are in `references/`:

| File | Endpoint | Method |
|---|---|---|
| `retrieve-block-children.md` | `/v1/blocks/{id}/children` | GET |
| `retrieve-a-block.md` | `/v1/blocks/{id}` | GET |
| `update-a-block.md` | `/v1/blocks/{id}` | PATCH |
| `append-block-children.md` | `/v1/blocks/{id}/children` | PATCH |
| `delete-a-block.md` | `/v1/blocks/{id}` | DELETE |
| `list-comments.md` | `/v1/comments?block_id={id}` | GET |
| `create-comment.md` | `/v1/comments` | POST |
| `retrieve-a-comment.md` | `/v1/comments/{id}` | GET |
| **`enhanced-markdown-spec.md`** | **Notion-flavored Markdown Spec** | - |

For content operations (block updates, page creation), always consult `references/enhanced-markdown-spec.md` first. It describes all block types, rich-text formats, escaping rules, and Notion-specific syntax.

## Curl Best Practices

### JSON Payloads via Temp Files

For POST/PATCH requests, write JSON to a temp file and reference it with `-d @filename`. This avoids shell escaping issues:

```bash
# 1. Write JSON
Write /tmp/notion_payload.json → { ... }

# 2. Request with -d @file
curl -s -X PATCH 'https://api.notion.com/v1/blocks/{block_id}' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Notion-Version: 2025-09-03' \
  -d @/tmp/notion_payload.json
```

### Response Validation

```bash
# Short form: OK on success, JSON on error
| python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('type') or d.get('id') else json.dumps(d,indent=2))"
```

### Parallel Requests

Independent API calls (e.g., multiple block updates) can run in parallel — use separate Bash tool invocations in one message.

## Common Issues & Solutions

### Block-Level vs. Page-Level Comments

`GET /v1/comments?block_id={page_id}` returns only **page-level comments**. For **block-level comments** (inline discussions):

```bash
# Step 1: Get all blocks on the page
curl -s 'https://api.notion.com/v1/blocks/{page_id}/children?page_size=100' ...

# Step 2: Check each block for comments
for block_id in ...; do
  curl -s 'https://api.notion.com/v1/comments?block_id={block_id}' ...
done
```

### discussion_id ≠ block_id

`discussion_id` groups comments in a thread — it is **not a block ID** and cannot be used as `block_id` in API calls. To reply to a discussion:

```json
{
  "discussion_id": "304d8531-f4ae-...",
  "rich_text": [{ "type": "text", "text": { "content": "Reply text" } }]
}
```

### Block Updates Delete Comment Threads

Updating a block via `PATCH /v1/blocks/{id}` (e.g., changing `rich_text`) may delete existing comment threads. Before modifying a block with comments:

1. Read and save comments first
2. After update: create new thread and re-post archived comments

### User Mentions Don't Work with Integrations

`"mention": { "user": { "id": "..." } }` returns 404 if the integration lacks user visibility. **Workaround:** Use plain text `"@Name"` instead of rich-text mentions.

### Rich Text Annotations

Block updates require full `rich_text` structure with annotations:

```json
{
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  }
}
```

Only include fields you're setting — missing fields default to `false`.

### Shell Quoting

Always use single quotes for curl headers:

```bash
# Correct
-H 'Authorization: Bearer ntn_...'

# Wrong — causes "blank argument" errors
-H "Authorization: Bearer $NOTION_TOKEN"
```

### Pagination

Block-children responses may be paginated (`has_more: true`). For pages with many blocks:

```bash
curl ... '?page_size=100&start_cursor={next_cursor}'
```

### Data Source vs. Database (API v2025-09-03)

`POST /v1/databases/{id}/query` fails with `invalid_request_url` (400) for databases that exist as Data Sources (e.g., Notion Projects & Tasks). Use `POST /v1/data_sources/{data_source_id}/query` instead. Same for page creation: use `parent.data_source_id` instead of `parent.database_id`.

**Detection:** If a page response shows `parent.type = "data_source_id"`, the database is a Data Source.

## Toggle Headings & Nesting

**Important:** Notion API does not accept `children` when creating toggle headings!

Create toggle headings in two steps:

1. Create heading block with `is_toggleable: true` (WITHOUT `children` field)
2. Add child blocks separately using `PATCH /v1/blocks/{heading_id}/children`

**Incorrect approach:**

```json
{
  "type": "heading_2",
  "heading_2": {
    "rich_text": [...],
    "is_toggleable": true
  },
  "children": [...]  // Rejected!
}
```

**Correct approach:**

```bash
# Step 1: Create heading
curl -s -X PATCH 'https://api.notion.com/v1/blocks/{parent_id}/children' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Notion-Version: 2025-09-03' \
  -d '{
    "children": [{
      "type": "heading_2",
      "heading_2": {
        "rich_text": [...],
        "is_toggleable": true
      }
    }]
  }' | jq -r '.results[0].id' > /tmp/heading_id.txt

HEADING_ID=$(cat /tmp/heading_id.txt)

# Step 2: Add children to heading
curl -s -X PATCH "https://api.notion.com/v1/blocks/$HEADING_ID/children" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Notion-Version: 2025-09-03' \
  -d '{ "children": [...] }'
```

## Markdown Upload

**Upload script:** `.claude/skills/notion-api/upload.py`

Parses standard Markdown directly into Notion API blocks — no intermediate format needed.

```bash
# With page ID
uv run .claude/skills/notion-api/upload.py <file.md> <page-id> [title]

# With config path (reads ID from config)
uv run .claude/skills/notion-api/upload.py --config pages.<page-key> <file.md> [title]
```

**Heading hierarchy:**
- First H1 is removed (becomes Notion page title)
- All subsequent H1/H2/H3 become toggle headings
- H1 contains H2, H2 contains H3, H3 contains content

**Supported blocks:** Paragraphs, bullets (with sub-bullets), numbered lists, tables, code blocks, blockquotes (multi-line), dividers, checkboxes

**Rich text:** `**bold**`, `*italic*`, `` `code` ``, `[text](url)`, `[text](notion://page-id)` → page mention

**Cross-page links:** `link_map` parameter replaces `](file.md)` with `](notion://page-id)` for page mentions.

**Important:** `clear_page()` protects `child_page` and `child_database` blocks.

## Common Operations

### Update Block Content

```json
{
  "<block_type>": {
    "rich_text": [
      { "type": "text", "text": { "content": "New text" } }
    ]
  }
}
```

`<block_type>` = `paragraph`, `heading_3`, `quote`, `bulleted_list_item`, etc.

### Post Comment in Existing Thread

```json
{
  "discussion_id": "<discussion_id>",
  "rich_text": [
    { "type": "text", "text": { "content": "Comment text" } }
  ]
}
```

### Post New Comment on Block

```json
{
  "parent": { "block_id": "<block_id>" },
  "rich_text": [
    { "type": "text", "text": { "content": "Comment text" } }
  ]
}
```

### Extract Page ID from URL

Notion page URLs have the format:

```
https://www.notion.so/Page-Title-{page_id_raw}
```

The last 32 hex characters are the page ID (without hyphens). Format for API use:

```bash
# Raw: 302d8531f4ae80a7b070cfb7e5468ee1
# Formatted: 302d8531-f4ae-80a7-b070-cfb7e5468ee1
```

Python one-liner:

```python
raw = "302d8531f4ae80a7b070cfb7e5468ee1"
formatted = f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"
```
