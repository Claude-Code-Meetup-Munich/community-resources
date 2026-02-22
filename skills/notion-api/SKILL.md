---
name: notion-api
description: Notion API Integration via curl. Verwende dieses Skill für alle Notion-Aufgaben — Seiten lesen, Blöcke bearbeiten, Kommentare lesen/schreiben, Datenbanken abfragen.
allowed-tools:
  - Bash
  - Read
  - Write
argument-hint: "[Notion-Aufgabe beschreiben]"
---

# Notion API Skill

## Setup

Config-Datei: `.claude/config/notion.json` (Standard-Pfad in jedem Projekt).

```json
{
  "token": "ntn_...",
  "pages": {
    "my-page": { "id": "page-id" }
  }
}
```

## Authentifizierung

- **API Token:** Wird aus `.claude/config/notion.json` gelesen.
- **API Version:** `2025-09-03`
- **Base URL:** `https://api.notion.com/v1`

### Standard-Header für alle Requests

Lade den Token per `jq` oder `python` aus der Config.

```bash
TOKEN=$(jq -r .token .claude/config/notion.json)

-H "Authorization: Bearer $TOKEN" \
-H 'Content-Type: application/json' \
-H 'Notion-Version: 2025-09-03'
```

**Wichtig: Immer single quotes** für Header-Werte verwenden. Double quotes mit Shell-Variablen führen zu `blank argument`-Fehlern.

## Page IDs

Alle relevanten Notion Page IDs werden in **`.claude/config/notion.json`** unter `pages` gecacht.

Struktur: `pages.<page-key>.id`

Vor jeder Notion-Operation: Config lesen und die benötigte ID nachschlagen.
```bash
PAGE_ID=$(jq -r '.pages.my_page.id' .claude/config/notion.json)
```

### Auto-Caching neuer Page IDs

**Wenn du mit einer Page arbeitest, die noch nicht in der Config steht:** Trage die Page ID automatisch in `.claude/config/notion.json` ein. Verwende einen sprechenden Slug als Key (z.B. `meeting-notes`, `project-overview`).

```bash
# Beispiel: Neue Page cachen
jq '.pages["briefing-sales-assistant"] = {"id": "30ad8531-f4ae-80a8-940a-c2585842da40"}' \
  .claude/config/notion.json > /tmp/notion-config-tmp.json && \
  mv /tmp/notion-config-tmp.json .claude/config/notion.json
```

Das gilt für alle Wege, über die eine Page ID reinkommt: URL vom User, Response von der API, oder `--config`-Lookup.

## Data Sources

Ab API-Version `2025-09-03` nutzt Notion ein **Data-Source-Modell**. Datenbanken bestehen aus separaten "Data Sources". Pages haben `parent.type = "data_source_id"`.

**Konzept:** Database → Data Source → Pages

- `GET /v1/data_sources/{id}` — Schema/Properties abrufen (Property-Namen, Typen, Select-Optionen)
- `POST /v1/data_sources/{id}/query` — Pages abfragen (Filter, Sort, Pagination)
- Page-Erstellung: `parent: { "data_source_id": "<id>" }` statt `database_id`

### Config: `databases` Sektion

Data Source IDs werden in `.claude/config/notion.json` unter `databases` gespeichert:

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

Zugriff:
```bash
TASKS_DS=$(jq -r '.databases.tasks.data_source_id' .claude/config/notion.json)
PROJECTS_DS=$(jq -r '.databases.projects.data_source_id' .claude/config/notion.json)
```

### Auto-Detection

Wenn `GET /v1/pages/{id}` einen `parent.type = "data_source_id"` zurückgibt: die `data_source_id` automatisch in der Config cachen (analog zu Page-ID-Caching).

## API-Dokumentation (lokal)

Detaillierte Endpoint-Referenzen liegen in `references/`:

| Datei | Endpoint | Methode |
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

Bei Unsicherheit über Payload-Format: **erst die lokale Referenz lesen** (`references/<endpoint>.md`).

**Wichtig:** Für alle Content-Operationen (Block-Updates, Page-Erstellung) **immer zuerst** `references/enhanced-markdown-spec.md` konsultieren. Die Spec beschreibt alle Block-Typen, Rich-Text-Formate, Escaping-Regeln und Notion-spezifische Syntax.

## Curl Best Practices

### JSON-Payloads über Temp-Dateien

Für POST/PATCH-Requests: JSON in eine Temp-Datei schreiben und mit `-d @filename` referenzieren. Das vermeidet Shell-Escaping-Probleme.

```bash
# 1. JSON schreiben
Write /tmp/notion_payload.json → { ... }

# 2. Request mit -d @datei
curl -s -X PATCH 'https://api.notion.com/v1/blocks/{block_id}' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Notion-Version: 2025-09-03' \
  -d @/tmp/notion_payload.json
```

### Response-Validierung

```bash
# Kurzform: OK bei Erfolg, JSON bei Fehler
| python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('type') or d.get('id') else json.dumps(d,indent=2))"
```

### Parallele Requests

Unabhängige API-Calls (z.B. mehrere Block-Updates) können parallel ausgeführt werden — separate Bash-Tool-Aufrufe in einer Message.

## Quirks & Gotchas

### 1. Block-Level Comments ≠ Page-Level Comments

`GET /v1/comments?block_id={page_id}` gibt nur **Page-Level-Kommentare** zurück. Für **Block-Level-Kommentare** (Inline-Diskussionen):

```bash
# Schritt 1: Alle Blöcke der Seite holen
curl -s 'https://api.notion.com/v1/blocks/{page_id}/children?page_size=100' ...

# Schritt 2: Jeden Block auf Kommentare prüfen
for block_id in ...; do
  curl -s 'https://api.notion.com/v1/comments?block_id={block_id}' ...
done
```

### 2. discussion_id ≠ block_id

`discussion_id` ist ein Gruppen-Identifier für einen Kommentar-Thread. Es ist **KEIN Block-ID** und kann nicht als `block_id` in API-Calls verwendet werden. Um auf eine Diskussion zu antworten:

```json
{
  "discussion_id": "304d8531-f4ae-...",
  "rich_text": [{ "type": "text", "text": { "content": "Antwort" } }]
}
```

### 3. Block-Updates löschen Kommentar-Threads

Wenn ein Block per `PATCH /v1/blocks/{id}` aktualisiert wird (z.B. `rich_text` ändern), können **bestehende Kommentar-Threads an diesem Block verschwinden**. Bevor ein Block mit Kommentaren geändert wird:

1. Kommentare vorher auslesen und sichern
2. Nach dem Update: neuen Thread erstellen und archivierte Kommentare re-posten

### 4. User Mentions funktionieren nicht mit Integrations

`"mention": { "user": { "id": "..." } }` gibt 404 zurück, wenn die Integration keine User-Visibility hat. **Workaround:** Plain text `"@Name"` statt Rich-Text-Mention verwenden.

### 5. Rich Text Annotations

Block-Updates erfordern die volle `rich_text`-Struktur. Annotations-Objekt:

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

Nur gesetzte Felder übergeben — fehlende defaults zu `false`.

### 6. Shell-Quoting

**Immer single quotes** für curl-Header verwenden:

```bash
# Richtig
-H 'Authorization: Bearer ntn_...'

# Falsch — führt zu "blank argument" Fehlern
-H "Authorization: Bearer $NOTION_TOKEN"  # Variable nicht gesetzt
-H "Content-Type: application/json"       # Kann in manchen Shells brechen
```

### 7. Pagination

Block-Children-Responses können paginiert sein (`has_more: true`). Bei Seiten mit vielen Blöcken:

```bash
curl ... '?page_size=100&start_cursor={next_cursor}'
```

### 8. Data Source vs. Database — API ab 2025-09-03

`POST /v1/databases/{id}/query` schlägt mit `invalid_request_url` (400) fehl für Datenbanken, die als Data Sources existieren (z.B. Notion Projects & Tasks). Stattdessen: `POST /v1/data_sources/{data_source_id}/query` verwenden. Gleiches gilt für Page-Erstellung: `parent.data_source_id` statt `parent.database_id`.

**Erkennung:** Wenn ein Page-Response `parent.type = "data_source_id"` zeigt, ist die DB eine Data Source.

## Toggle Headings & Verschachtelung

**WICHTIG: Notion API akzeptiert KEINE `children` beim Erstellen von Toggle Headings!**

Toggle Headings müssen in zwei Schritten erstellt werden:
1. Heading-Block mit `is_toggleable: true` erstellen (OHNE `children` Feld)
2. Kinder-Blöcke separat mit `PATCH /v1/blocks/{heading_id}/children` hinzufügen

**Fehlgeschlagener Ansatz:**
```json
{
  "type": "heading_2",
  "heading_2": {
    "rich_text": [...],
    "is_toggleable": true
  },
  "children": [...]  // Wird abgelehnt!
}
```

**Korrekter Ansatz:**
```python
# Schritt 1: Heading erstellen
response = requests.patch(f"/v1/blocks/{parent_id}/children", json={
  "children": [{
    "type": "heading_2",
    "heading_2": {
      "rich_text": [...],
      "is_toggleable": true
    }
  }]
})

heading_id = response.json()["results"][0]["id"]

# Schritt 2: Kinder hinzufügen
requests.patch(f"/v1/blocks/{heading_id}/children", json={
  "children": [...]  // Jetzt erlaubt
})
```

## Markdown → Notion Upload

**Upload-Script:** `.claude/skills/notion-api/upload.py`

Parst Standard-Markdown direkt in Notion API Blöcke — kein Intermediate-Format nötig.

```bash
# Mit Page ID
uv run .claude/skills/notion-api/upload.py <datei.md> <page-id> [titel]

# Mit Config-Pfad (liest ID aus .notion-config.json)
uv run .claude/skills/notion-api/upload.py --config pages.<page-key> <datei.md> [titel]
```

**Heading-Hierarchie:**
- Erste H1 wird entfernt (= Notion-Seitentitel)
- Alle weiteren H1/H2/H3 → Toggle Headings
- H1 enthält H2, H2 enthält H3, H3 enthält Content

**Unterstützte Blöcke:** Paragraphs, Bullets (mit Sub-Bullets), Numbered Lists, Tables, Code-Blöcke, Blockquotes (mehrzeilig), Divider, Checkboxen

**Rich Text:** `**bold**`, `*italic*`, `` `code` ``, `[text](url)`, `[text](notion://page-id)` → Page Mention

**Cross-Page-Links:** `link_map` Parameter ersetzt `](datei.md)` durch `](notion://page-id)` für Page Mentions.

**Wichtig:** `clear_page()` schützt `child_page` und `child_database` Blöcke.

## Häufige Operationen

### Block-Inhalt aktualisieren

```json
{
  "<block_type>": {
    "rich_text": [
      { "type": "text", "text": { "content": "Neuer Text" } }
    ]
  }
}
```

`<block_type>` = `paragraph`, `heading_3`, `quote`, `bulleted_list_item`, etc.

### Kommentar in bestehendem Thread posten

```json
{
  "discussion_id": "<discussion_id>",
  "rich_text": [
    { "type": "text", "text": { "content": "Kommentar-Text hier" } }
  ]
}
```

### Neuen Kommentar an Block posten

```json
{
  "parent": { "block_id": "<block_id>" },
  "rich_text": [
    { "type": "text", "text": { "content": "Kommentar-Text hier" } }
  ]
}
```

### Page ID aus URL extrahieren

Notion Page URLs haben das Format:
```
https://www.notion.so/Page-Title-{page_id_raw}
```

Die letzten 32 Hex-Zeichen sind die Page ID (ohne Bindestriche). Für die API formatieren:

```bash
# Raw: 302d8531f4ae80a7b070cfb7e5468ee1
# Formatted: 302d8531-f4ae-80a7-b070-cfb7e5468ee1
```

Python one-liner:
```python
# UUID aus letzten 32 Zeichen mit Bindestrichen
raw = "302d8531f4ae80a7b070cfb7e5468ee1"
formatted = f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"
```
