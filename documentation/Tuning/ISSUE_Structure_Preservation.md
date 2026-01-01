# Babel Structure Preservation Issue: Index/Nomenclature Sections

## The Problem

When translating documents with structured index/nomenclature sections, Babel destroys the tabular structure. Example:

**Original (two-column layout):**
```
c    absolute velocity
d    diameter
F    thrust
h    specific enthalpy
```

**After Translation (jumbled text):**
```
c absolute snelheid d diameter F strekracht h specifieke enthalpie...
```

## Root Cause Analysis

The Babel translation pipeline has these stages:

1. **PDF Parsing** (`il_creater.py`) - Extracts characters with positions
2. **Paragraph Finding** (`paragraph_finder.py`) - Groups characters into paragraphs
3. **Formula Detection** (`styles_and_formulas.py`) - Identifies formulas within paragraphs
4. **Translation** (`il_translator_llm_only.py`) - Translates paragraph text
5. **Typesetting** (`typesetting.py`) - Reflows translated text to fit layout

**The Breaking Points:**

### Stage 2: Paragraph Finding
- Characters are grouped by proximity and layout region
- A two-column list gets merged into a single paragraph
- No awareness that each LINE is a separate semantic unit

### Stage 3: No Special Handling
- Nomenclature sections aren't detected as a special layout type
- They're treated as regular "content" or "text" paragraphs

### Stage 5: Typesetting Reflow
- The translated paragraph is reflowed to fit the bounding box
- Line breaks from original are lost because there's no line-level structure

## Potential Solutions

### Solution A: Line-Level Translation (Complex)
1. Detect nomenclature/index sections (heuristics: short lines, symbol+definition pattern)
2. Preserve line structure in paragraphs
3. Translate each line separately
4. Typeset each line to its original position

**Complexity:** High - requires changes to paragraph finder, translator, and typesetter

### Solution B: Skip Translation for Index Sections (Simple)
1. Detect nomenclature/index sections
2. Mark them as "do not translate"
3. Render original text in original positions

**Complexity:** Medium - requires detection heuristics and a bypass mechanism

### Solution C: Table Detection (Medium)
1. Improve layout detection to recognize two-column lists as tables
2. Use existing table handling (which should preserve cell structure)

**Complexity:** Medium - relies on layout model improvements

### Solution D: User Annotation (Pragmatic)
1. Allow users to specify page regions or section headers to skip
2. Implement a CLI flag: `--skip-sections "Nomenclature,References"`

**Complexity:** Low - straightforward to implement

## Recommended Approach

For immediate relief, implement **Solution D** (user annotation to skip sections).

For long-term quality, pursue **Solution C** (better layout detection).

## Implementation Notes for Solution D

In `translate.py`:
```python
@click.option(
    "--skip-sections",
    type=str,
    default="",
    help="Comma-separated list of section titles to skip (e.g., 'Nomenclature,References')",
)
```

In `il_translator_llm_only.py`:
- Check if paragraph is in a skipped section
- If yes, copy original characters without translation

This preserves both content and layout for sections that shouldn't be translated.
