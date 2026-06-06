# Design Specification — Execution-Level Document Renderer

> Implementation brief for the shared rendering engine across EP, CP, EB, PMR.

---

## 1. Architecture Overview

```
LLM generates Structured Markdown (per-skill spec)
         │
         ▼
   ┌──────────────┐
   │   parse.py   │  → Markdown → Python dict (sections, tables, badges, metadata)
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │  validate.py │  → Checks required sections, badge values, frontmatter
   └──────┬───────┘
          │ PASS (auto-fix minor issues, flag missing sections)
          │
          ├──────────────────┬──────────────────┐
          ▼                  ▼                  ▼
   ┌────────────┐    ┌────────────┐    ┌────────────┐
   │  html.py   │    │   pdf.py   │    │  docx.py   │
   │ Self-contained│  │ ReportLab  │    │ python-docx│
   │ inline CSS │    │ direct     │    │ w/ styles  │
   └────────────┘    └────────────┘    └────────────┘
```

### Key Principles
- **MD3 Purple + McKinsey hybrid** — rounded cards & pill badges (MD3) + tight typography, numbered exhibits & exhibit-style tables (McKinsey). Section headers show `N. 📊 Title`.
- **Zero external dependencies at runtime** — no CDN, no Google Fonts download
- **Self-contained HTML** — single .html file with all CSS inlined
- **ReportLab for PDF** — direct dict→PDF rendering, no HTML intermediate step
- **python-docx for Word** — with .docx style template for brand consistency
- **Deterministic** — same Markdown input = identical output every time

---

## 2. Design System — Visual Language

### 2.1 Color Palette

```css
:root {
  /* Primary */
  --color-primary: #6D28D9;        /* Purple 700 — main accent */
  --color-primary-light: #EDE9FE;  /* Purple 50 — light backgrounds */
  --color-primary-dark: #4C1D95;   /* Purple 900 — dark text on light */
  
  /* Semantic — Stance */
  --color-champion: #059669;       /* Emerald 600 */
  --color-supporter: #059669;      /* Same as champion */
  --color-neutral: #D97706;        /* Amber 600 */
  --color-non-supporter: #DC2626;  /* Red 600 */
  --color-unknown: #6B7280;        /* Gray 500 */
  
  /* Semantic — Status */
  --color-done: #059669;           /* Green */
  --color-next: #6D28D9;           /* Purple */
  --color-planned: #9CA3AF;        /* Gray 400 */
  --color-achieved: #059669;       /* Green */
  --color-partial: #D97706;        /* Amber */
  --color-not-achieved: #DC2626;   /* Red */
  
  /* Semantic — Priority */
  --color-high: #DC2626;           /* Red */
  --color-medium: #D97706;         /* Amber */
  --color-low: #059669;            /* Green */
  
  /* Semantic — Objection Category */
  --color-risk-trust: #DC2626;     /* Red */
  --color-capability: #EA580C;     /* Orange 600 */
  --color-authority: #D97706;      /* Amber */
  --color-price-value: #6D28D9;    /* Purple */
  --color-status-quo: #6B7280;     /* Gray */
  
  /* Neutral */
  --color-bg: #FFFFFF;
  --color-bg-page: #F9FAFB;       /* Gray 50 — page background */
  --color-border: #E5E7EB;        /* Gray 200 */
  --color-text: #111827;          /* Gray 900 */
  --color-text-secondary: #6B7280; /* Gray 500 */
  --color-text-muted: #9CA3AF;    /* Gray 400 */
  
  /* Document Type Accents (header label color) */
  --color-ep: #6D28D9;            /* Purple */
  --color-cp: #6D28D9;            /* Purple */
  --color-eb: #6D28D9;            /* Purple */
  --color-pmr: #6D28D9;           /* Purple */
  
  /* Special */
  --color-confidential: #DC2626;   /* Red — for EB internal banner */
}
```

### 2.2 Typography

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", 
               "PingFang SC", "Hiragino Sans GB", sans-serif;
  font-size: 14px;
  line-height: 1.75;  /* Optimized for CJK mixed content */
  color: var(--color-text);
}

h1 { font-size: 28px; font-weight: 700; }  /* Document title */
h2 { font-size: 18px; font-weight: 600; }  /* Section header */
h3 { font-size: 15px; font-weight: 600; }  /* Sub-section */

.doc-type-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-primary);
}
```

### 2.3 Layout

```css
.page {
  max-width: 820px;
  margin: 0 auto;
  padding: 40px 48px;
  background: var(--color-bg);
}

.section-card {
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  background: var(--color-bg);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--color-primary-light);
  font-size: 18px;
  font-weight: 600;
}

.section-header .emoji {
  font-size: 20px;
}
```

### 2.4 Badge / Tag Styles

**Stance badges — outline style (print-friendly):**

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 10px;
  border-radius: 9999px;  /* full pill */
  font-size: 12px;
  font-weight: 500;
  border: 1.5px solid;
  white-space: nowrap;
}

.badge-champion    { color: var(--color-champion); border-color: var(--color-champion); background: #ECFDF5; }
.badge-supporter   { color: var(--color-supporter); border-color: var(--color-supporter); background: #ECFDF5; }
.badge-neutral     { color: var(--color-neutral); border-color: var(--color-neutral); background: #FFFBEB; }
.badge-non-supporter { color: var(--color-non-supporter); border-color: var(--color-non-supporter); background: #FEF2F2; }
.badge-unknown     { color: var(--color-unknown); border-color: var(--color-unknown); background: #F9FAFB; }

/* Role badges — subtle filled */
.badge-decision-maker { color: #1F2937; background: #F3F4F6; border-color: #D1D5DB; }
.badge-technical-evaluator { color: var(--color-primary-dark); background: var(--color-primary-light); border-color: #C4B5FD; }
.badge-influencer { color: #92400E; background: #FEF3C7; border-color: #FCD34D; }
.badge-end-user   { color: #6B7280; background: #F9FAFB; border-color: #E5E7EB; }

/* Priority badges */
.badge-high   { color: #FFF; background: var(--color-high); border-color: var(--color-high); }
.badge-medium { color: #FFF; background: var(--color-medium); border-color: var(--color-medium); }
.badge-low    { color: #FFF; background: var(--color-low); border-color: var(--color-low); }

/* Status badges */
.badge-achieved     { color: var(--color-achieved); border-color: var(--color-achieved); background: #ECFDF5; }
.badge-partial      { color: var(--color-partial); border-color: var(--color-partial); background: #FFFBEB; }
.badge-not-achieved { color: var(--color-not-achieved); border-color: var(--color-not-achieved); background: #FEF2F2; }
```

**Provenance labels:**
```css
.provenance {
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 4px;
  font-weight: 500;
}
.provenance-sales    { color: #059669; background: #ECFDF5; }  /* [销售确认] */
.provenance-web { color: #2563EB; background: #EFF6FF; }  /* [网络搜索] */
.provenance-ai { color: #6B7280; background: #F3F4F6; }   /* [AI推断] */
```

### 2.5 Tables

```css
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

th {
  text-align: left;
  font-weight: 600;
  color: var(--color-text-secondary);
  font-size: 12px;
  padding: 8px 12px;
  border-bottom: 2px solid var(--color-border);
}

td {
  padding: 10px 12px;
  border-bottom: 1px solid #F3F4F6;
  vertical-align: top;
}

tr:last-child td {
  border-bottom: none;
}
```

### 2.6 Stakeholder Card

```css
.stakeholder-card {
  border: 1px solid var(--color-border);
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 16px;
  position: relative;
}

.stakeholder-card .name {
  font-size: 16px;
  font-weight: 700;
}

.stakeholder-card .title {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.stakeholder-card .stance-badge {
  position: absolute;
  top: 16px;
  right: 16px;
}

.stakeholder-card .how-to-win {
  background: var(--color-primary-light);
  border-radius: 8px;
  border-left: 3px solid var(--color-primary);
  padding: 12px 16px;
  margin-top: 12px;
  font-size: 13px;
}
```

### 2.7 Roadmap Timeline (EP specific)

```css
.roadmap {
  position: relative;
  padding-left: 44px;
}

.roadmap::before {
  content: '';
  position: absolute;
  left: 15px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, var(--color-done), var(--color-primary), var(--color-border));
  border-radius: 1px;
}

.milestone {
  position: relative;
  margin-bottom: 20px;
  padding: 16px 20px;
  border: 1px solid var(--color-border);
  border-radius: 10px;
}

.milestone-marker {
  position: absolute;
  left: -37px;
  top: 18px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}

.milestone-marker.done { background: var(--color-done); color: white; }
.milestone-marker.next { background: var(--color-next); color: white; }
.milestone-marker.planned { background: #F3F4F6; color: var(--color-text-secondary); border: 2px solid var(--color-border); }
```

### 2.8 Objection Cards (CP specific)

```css
.objection-card {
  border: 1px solid var(--color-border);
  border-left: 4px solid;
  border-radius: 10px;
  padding: 16px 20px;
  margin-bottom: 12px;
}

.objection-card.risk-trust    { border-left-color: var(--color-risk-trust); }
.objection-card.capability    { border-left-color: var(--color-capability); }
.objection-card.authority     { border-left-color: var(--color-authority); }
.objection-card.price-value   { border-left-color: var(--color-price-value); }
.objection-card.status-quo    { border-left-color: var(--color-status-quo); }
```

---

## 3. Document Header Template

All 4 document types share the same header structure:

```
┌─────────────────────────────────────────────────────────┐
│ ENGAGEMENT PLAN (small, uppercase, purple)    📅 Date   │
│                                                         │
│ Customer Name (28px bold)                               │
│ Opportunity / Meeting Title (14px gray)                 │
│                                                         │
│ [Stage Badge]  [TCV/Value Badge if applicable]          │
└─────────────────────────────────────────────────────────┘
```

EB additionally has:
```
┌─────────────────────────────────────────────────────────┐
│ 🔒 INTERNAL USE ONLY — AWS Confidential                 │
│ (red background, white text, full-width banner)         │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Print & PDF Rules

### 4.1 Page Setup
```css
@page {
  size: A4;
  margin: 20mm 18mm 20mm 18mm;
}
```

### 4.2 Smart Pagination
```css
/* Protect small units */
h2, h3 {
  break-after: avoid;
  orphans: 3;
  widows: 3;
}

.stakeholder-card,
.objection-card,
.milestone {
  break-inside: avoid;
}

table {
  break-inside: avoid;
}

/* If table is too tall (>60% page), allow break but repeat header */
table.allow-break {
  break-inside: auto;
}
table.allow-break thead {
  display: table-header-group;  /* Repeat on each page */
}

/* Section headers never orphaned at page bottom */
.section-header {
  break-after: avoid;
}
```

### 4.3 Print Badge Optimization
```css
@media print {
  .badge {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  
  /* Ensure badges remain visible in B&W printing */
  .badge-high, .badge-medium, .badge-low {
    background: transparent !important;
    color: inherit !important;
    border: 1.5px solid currentColor !important;
  }
}
```

### 4.4 Page Header & Footer (PDF only)
```
Header: [Doc Type] | [Customer] | [Date]              Page X/Y
Footer: Generated by Dali · Confidential
        (EB adds: INTERNAL USE ONLY — AWS Confidential)
```

### 4.5 Path Headers (Next Steps multi-path)
```css
.path-header {
  font-size: 15px;  /* slightly larger than body for visual weight */
  font-weight: 600;
}
.path-header .path-icon {
  font-size: 18px;
}
```

---

## 5. Emoji Usage Guidelines 🏷️

Emojis are used as **section icons** and **inline markers**:

| Context | Emojis |
|---------|--------|
| **Section Headers** | 📋 Meeting Details, 🎯 Target Outcomes, ✅ Success Criteria, 🔄 Information Exchange, 🛡️ Objections, 📅 Agenda, ➡️ Next Steps, 👥 Key Stakeholders, 📊 Opportunity Snapshot, 📍 Engagement Roadmap, 📝 What Changed, 🔍 Meeting Insights |
| **Status** | ✅ Achieved, ⚠️ Partial, ❌ Not achieved, ✓ Done, ▶ Next, ○ Planned |
| **Paths** | ✅ Primary path, ⏳ Fallback path, 🚪 Graceful exit |
| **Priority** | 🔴 High, 🟡 Medium, 🟢 Low |
| **Inline** | 👤 Person, 📅 Date, 📈 Stage progression, 💰 TCV/Value, 🔒 Confidential |

**Rule:** Emojis appear BEFORE text in headers. Maximum 1 emoji per header. No emoji in body text (except provenance markers and inline person/date references).

**Provenance display:** Only `[销售确认]` and `[网络搜索]` are shown explicitly. No label = AI推断 (default). This follows the principle of minimal annotation — only flag non-AI sources.

---

## 6. Error Handling & Fallbacks

| Scenario | Behavior |
|----------|----------|
| Missing required section | Auto-insert empty section with `[待补充]` marker, render continues |
| Invalid badge value | Render as gray badge with original text, log warning |
| Table parse failure | Render raw markdown text in a code block, flag in output |
| Render script crash | Return partial HTML up to the crash point + error message |
| Font not available | System font stack gracefully degrades |

---

## 7. File Dependencies

```
shared/
├── DESIGN_SPEC.md          ← This file
├── render.py               ← Main entry: render(input_md, format, output_path)
├── parse.py                ← Markdown → structured dict
├── validate.py             ← Schema validation + auto-fix
├── html_renderer.py        ← Dict → self-contained HTML
├── pdf_renderer.py         ← DEPRECATED (WeasyPrint, kept for reference only)
├── reportlab_renderer.py   ← Dict → PDF via ReportLab (primary PDF engine)
├── docx_renderer.py        ← Dict → styled Word doc
├── theme.css               ← Full CSS (inlined into HTML)
├── fonts/
│   ├── download.sh         ← Download Noto Sans SC Regular + Bold
│   └── .gitignore          ← Ignores downloaded .ttf files
└── requirements.txt        ← Python dependencies
```
