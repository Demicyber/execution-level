# Renderer Implementation — Technical Pitfalls & Recommendations

> Research findings for Mimi to reference during implementation.
> These are issues that could cause instability if not addressed.

---

## 1. WeasyPrint Pitfalls (PDF Generation)

> **NOTE:** WeasyPrint has been replaced by ReportLab as the primary PDF renderer.
> This section is kept as historical context for why the switch was made.

### 1.1 CJK Font Performance
- **Issue:** Noto Sans CJK (~20MB font) causes 6x slower PDF generation due to fonttools subsetting
- **Fix:** WeasyPrint v63.0+ switched to `hb-subset` (harfbuzz) — **ensure we use WeasyPrint >= 63.0**
- **Ref:** https://github.com/Kozea/WeasyPrint/issues/2120

### 1.2 Font Installation (Linux)
- **Required:** `google-noto-sans-cjk-ttc-fonts` package must be installed on the system
- **Install:** `sudo yum install google-noto-sans-cjk-ttc-fonts` (Amazon Linux) or `sudo apt install fonts-noto-cjk` (Debian/Ubuntu)
- **Verify:** `fc-list | grep -i "noto.*cjk"` should return results
- **Pitfall:** If font not found, WeasyPrint silently falls back to system default → Chinese characters may render as boxes

### 1.3 CSS Features NOT Supported in WeasyPrint
| CSS Feature | Status | Workaround |
|-------------|--------|------------|
| `display: flex` | ✅ Supported (since v57) | — |
| `display: grid` | ❌ NOT supported | Use `float` or `flexbox` |
| `box-shadow` | ⚠️ Partial (no spread) | Use `border` instead |
| `border-radius` on tables | ⚠️ Inconsistent | Apply to wrapper div |
| `position: sticky` | ❌ NOT supported | Not needed for PDF |
| `overflow: hidden` | ⚠️ May clip content | Avoid in print context |
| `max-height` | ⚠️ Can cause content to vanish | Never use in PDF — let content flow |
| CSS variables (`var()`) | ✅ Supported (since v53) | — |
| `white-space: nowrap` | ✅ Supported | — |
| `break-inside: avoid` | ✅ Supported | Works for divs, tables, cards |

### 1.4 Pagination Best Practices
```css
/* SAFE: These work reliably */
h2, h3 { break-after: avoid; }
.card, .stakeholder-card { break-inside: avoid; }
table { break-inside: avoid; }  /* for tables < 60% page height */

/* CAUTION: Large tables */
/* If table > ~60% of page height, break-inside:avoid can push it to next page leaving huge whitespace */
/* Solution: Add class .allow-break for long tables */
table.allow-break { break-inside: auto; }
table.allow-break thead { display: table-header-group; }  /* repeat header on new page */

/* IMPORTANT: orphans/widows */
p { orphans: 2; widows: 2; }  /* prevent single-line orphans */
```

### 1.5 Performance Recommendations
- **Cache font discovery:** First run will be slow as WeasyPrint discovers system fonts. Subsequent runs are faster.
- **Avoid re-parsing CSS:** If rendering multiple documents in one session, reuse the CSS object.
- **Expected timing:** ~2-4 seconds for a 5-page CJK document (with hb-subset fix in v63+)

---

## 2. LLM Output Stability (Structured Markdown)

### 2.1 Why Markdown > JSON for LLM Output
| Factor | JSON | Structured Markdown |
|--------|------|-------------------|
| LLM accuracy | ❌ Brackets/commas easily broken | ✅ Headers/tables natural for LLM |
| Nested data | Complex nesting → errors | Flat sections with lists |
| Validation | Schema validation possible | Section-header based validation |
| Partial output | Broken JSON = total failure | Partial Markdown = partial doc |
| Debugging | Hard to read raw | Human-readable |

### 2.2 Common LLM Failure Modes
| Failure | Frequency | Mitigation |
|---------|-----------|------------|
| Missing section header | Medium | Auto-insert empty section + `[待补充]` |
| Wrong badge value (e.g., "Support" instead of "supporter") | High | Fuzzy-match to nearest valid enum |
| Table column mismatch | Low | Count columns, pad/trim to expected |
| Duplicate section | Low | Keep first occurrence, warn |
| Extra commentary outside sections | Medium | Strip text before first `##` header |
| Frontmatter field missing | Medium | Fill with `[待确认]`, continue |

### 2.3 Validation Strategy (validate.py)
```python
def validate(parsed_doc):
    issues = []
    
    # 1. Check all required sections present
    for section in REQUIRED_SECTIONS[doc_type]:
        if section not in parsed_doc.sections:
            parsed_doc.sections[section] = empty_section(section)
            issues.append(f"AUTO-FIX: Added empty section '{section}'")
    
    # 2. Fuzzy-match badge values
    for badge in parsed_doc.all_badges():
        if badge.value not in VALID_VALUES[badge.field]:
            closest = fuzzy_match(badge.value, VALID_VALUES[badge.field])
            if closest and similarity > 0.7:
                badge.value = closest
                issues.append(f"AUTO-FIX: '{badge.original}' → '{closest}'")
    
    # 3. Table column validation
    for table in parsed_doc.all_tables():
        if len(table.headers) != EXPECTED_COLUMNS[table.section]:
            issues.append(f"WARNING: Table in {table.section} has {len(table.headers)} columns, expected {EXPECTED_COLUMNS[table.section]}")
    
    return issues  # Empty = valid
```

### 2.4 Graceful Degradation Strategy
```
Level 1: Perfect parse → render normally
Level 2: Auto-fixable issues → fix + render + append warnings
Level 3: Section unparseable → render raw markdown text in a styled code block
Level 4: Total parse failure → return error message (never happens with section-based parsing)
```

---

## 3. python-docx Pitfalls (Word Generation)

### 3.1 CJK Font Setting
```python
# WRONG: This only sets Western font
run.font.name = "Noto Sans SC"

# CORRECT: Must also set East Asian font via XML
from docx.oxml.ns import qn
rPr = run._r.get_or_add_rPr()
rFonts = rPr.get_or_add_rFonts()
rFonts.set(qn('w:eastAsia'), 'Noto Sans SC')
rFonts.set(qn('w:ascii'), 'Noto Sans SC')
rFonts.set(qn('w:hAnsi'), 'Noto Sans SC')
```

**Best practice:** Set CJK font in `template.docx` Normal style → all text inherits it automatically. Avoid per-run XML manipulation.

### 3.2 Badge Rendering in Word
Word has NO rounded-corner pills. Best approximation:
```python
# Option A: Run-level shading (background color on text)
from docx.oxml.ns import qn
from docx.oxml import parse_xml

shd = parse_xml(f'<w:shd {qn("w:val")}="clear" {qn("w:fill")}="ECFDF5" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
run._r.get_or_add_rPr().append(shd)
run.font.color.rgb = RGBColor(0x05, 0x96, 0x69)  # green text
run.text = " ✓ Achieved "  # space padding simulates pill
```

**Limitation:** No border-radius, no border on individual runs. Accept that Word badges will look like highlighted text spans (still readable, just not as pretty as HTML).

### 3.3 Table Styling
- Set column widths explicitly on EVERY row (not just first row)
- Use `table.style = 'Table Grid'` as base, then customize
- Cell shading requires XML manipulation for custom colors
- Keep tables simple in Word — complex nested layouts break across viewers

### 3.4 Page Break Control
```python
# Before a new section
paragraph = doc.add_paragraph()
paragraph.paragraph_format.page_break_before = True

# Keep with next (prevent orphan headers)
paragraph.paragraph_format.keep_with_next = True
```

---

## 4. System Dependencies Checklist

```bash
# Required on the agent's Linux environment:
pip install weasyprint>=63.0 python-docx markdown pyyaml

# System packages (for WeasyPrint):
# Amazon Linux 2023:
sudo yum install -y pango cairo gdk-pixbuf2 google-noto-sans-cjk-ttc-fonts

# Verify:
python3 -c "import weasyprint; print(weasyprint.__version__)"
fc-list | grep -i "noto.*cjk"
```

---

## 5. Testing Recommendations

1. **Render all 3 sample documents** (minimal/medium/heavy CP) through the full pipeline
2. **Test with missing sections** — remove a `##` from input, verify auto-fix works
3. **Test with invalid badge values** — ensure fuzzy matching doesn't crash
4. **Test CJK rendering** — verify Chinese characters appear in PDF/Word
5. **Test long document pagination** — 5+ page EP, verify no orphaned headers or huge whitespace
6. **Cross-format comparison** — same input should produce visually equivalent HTML/PDF/Word
