# Expert Software Engineering Analysis: Structure Preservation in PDF Translation

## Executive Summary

The Babel translation engine has a fundamental architectural limitation: it treats all text content as **prose paragraphs** suitable for reflow. This works for flowing text but destroys structured content like nomenclatures, indices, tables, and lists. This analysis identifies the root cause, proposes a minimal-invasive solution, and outlines implementation paths.

---

## 1. Problem Decomposition

### 1.1 What We Observe
```
Original:                    After Translation:
c    absolute velocity       c absolute snelheid d diameter
d    diameter         →      F stuwkracht h specifieke...
F    thrust                  (all merged into flowing text)
```

### 1.2 The Invariant Being Violated

**Structural Invariant:** In structured content, the **vertical position** of each line is semantically meaningful. Line N must remain at vertical position Y_N after translation.

**Current Behavior:** The typesetter places translated text in a **flowing layout**, where vertical positions are computed dynamically based on text width and available space.

### 1.3 Root Cause: Information Loss

The pipeline discards structural information at multiple stages:

```
Stage 1: PDF → Characters        ✓ Preserves positions
Stage 2: Characters → Lines      ✓ Detects line structure  
Stage 3: Lines → Paragraphs      ⚠️ Lines MERGED into flowing paragraph
Stage 4: Paragraph → Translation ✗ Line boundaries LOST
Stage 5: Translation → Typeset   ✗ Reflows as prose
Stage 6: Typeset → Render        ✗ Wrong positions rendered
```

**Critical Failure Point:** Stage 3 merges lines without preserving the semantic signal that each line is an independent unit.

---

## 2. Architectural Analysis

### 2.1 The Paragraph Abstraction Problem

Babel has ONE text content abstraction: `PdfParagraph`. But documents contain multiple content types:

| Content Type | Reflow Behavior | Line Independence | Example |
|--------------|-----------------|-------------------|---------|
| **Prose** | Full reflow OK | Lines are presentation, not semantic | Article text |
| **Structured List** | Horizontal only | Each line = one item | Nomenclature |
| **Table Cell** | Constrained | Cell boundaries fixed | Data tables |
| **Formula** | No reflow | Characters are positioned | Math equations |

Babel treats types 1-3 identically. This is the architectural gap.

### 2.2 The Data Model Already Supports Lines

Looking at `il_version_1.py`:

```python
@dataclass
class PdfParagraphComposition:
    pdf_character: PdfCharacter | None  # Single character
    pdf_line: PdfLine | None            # Line of characters ← EXISTS!
    pdf_formula: PdfFormula | None      # Formula
```

**The data model ALREADY supports line-level composition!** The issue is that:
1. Lines are detected but merged during paragraph creation
2. Translation flattens lines into a single string
3. Typesetting ignores line boundaries

### 2.3 Where Lines Get Lost

In `paragraph_finder.py`, the `_group_chars_into_lines` method correctly clusters characters into lines. But then `_create_paragraphs_from_lines` merges them:

```python
# Current: All lines become one paragraph
for line in lines:
    current_paragraph.pdf_paragraph_composition.append(
        PdfParagraphComposition(pdf_line=line)
    )
# Result: One paragraph with many lines, but translated as one unit
```

In `il_translator_llm_only.py`, the paragraph text is extracted as a single string:
```python
paragraph_text = paragraph.unicode  # Flattens all lines into one string
translated = self.translator.translate(paragraph_text)  # Translated as prose
```

---

## 3. Solution Architecture

### 3.1 Design Principle: Late Binding of Layout Decisions

**Current (Early Binding):**
```
Detect Structure → Decide Reflow Strategy → Execute
     (lost)              (prose)           (wrong result)
```

**Proposed (Late Binding):**
```
Detect Structure → Preserve All Info → Analyze → Choose Strategy → Execute
   (line info)      (lines in para)    (check    (reflow or not)   (correct)
                                        type)
```

### 3.2 The Minimal Solution: Line-Aware Translation & Typesetting

Instead of a full architectural overhaul, we can add a **line preservation mode**:

1. **Detection Phase:** Identify paragraphs that should preserve line structure
2. **Translation Phase:** Translate line-by-line instead of paragraph-at-once
3. **Typesetting Phase:** Place each line at its original y-position

#### 3.2.1 Detection Heuristics

```python
def should_preserve_lines(paragraph: PdfParagraph) -> bool:
    """Determine if paragraph has structured (non-prose) layout."""
    
    if not paragraph.pdf_paragraph_composition:
        return False
    
    lines = [c.pdf_line for c in paragraph.pdf_paragraph_composition if c.pdf_line]
    if len(lines) < 2:
        return False
    
    # Heuristic 1: Short lines suggest list/table structure
    avg_line_length = mean(len(line.unicode) for line in lines)
    if avg_line_length < 40:  # Short lines
        return True
    
    # Heuristic 2: Lines don't end with punctuation (not sentences)
    ends_with_punct = sum(1 for l in lines if l.unicode.rstrip()[-1] in '.!?;')
    if ends_with_punct < len(lines) * 0.3:
        return True
    
    # Heuristic 3: Regular vertical spacing (list-like)
    y_positions = [line.box.y for line in lines]
    y_gaps = [y_positions[i+1] - y_positions[i] for i in range(len(y_positions)-1)]
    if len(y_gaps) > 1 and stdev(y_gaps) < mean(y_gaps) * 0.15:
        return True
    
    return False
```

#### 3.2.2 Line-by-Line Translation

```python
def translate_paragraph(paragraph: PdfParagraph) -> PdfParagraph:
    if should_preserve_lines(paragraph):
        # Translate each line independently
        for composition in paragraph.pdf_paragraph_composition:
            if composition.pdf_line:
                line_text = composition.pdf_line.unicode
                translated_text = self.translator.translate(line_text)
                composition.pdf_line.translated_unicode = translated_text
        paragraph.preserve_line_structure = True
    else:
        # Normal paragraph translation
        paragraph.translated_unicode = self.translator.translate(paragraph.unicode)
        paragraph.preserve_line_structure = False
    
    return paragraph
```

#### 3.2.3 Structure-Preserving Typesetting

```python
def typeset_paragraph(paragraph: PdfParagraph, available_box: Box):
    if getattr(paragraph, 'preserve_line_structure', False):
        # Line-preserving mode
        for composition in paragraph.pdf_paragraph_composition:
            if composition.pdf_line:
                line = composition.pdf_line
                # Keep original y-position, only adjust x if needed
                typeset_line_horizontal(
                    line,
                    y=line.box.y,  # PRESERVE original y
                    max_width=available_box.x2 - line.box.x
                )
    else:
        # Normal flowing typeset
        typeset_flowing(paragraph, available_box)
```

---

## 4. Implementation Plan

### Phase 1: Minimal Viable Solution (3-5 hours)

| Task | File | Complexity |
|------|------|------------|
| Add `preserve_line_structure` flag | `il_version_1.py` | Low |
| Add `should_preserve_lines()` detection | `paragraph_finder.py` | Medium |
| Modify translation to handle line-by-line | `il_translator_llm_only.py` | Medium |
| Modify typesetting to preserve y-positions | `typesetting.py` | Medium |
| Add CLI flag `--preserve-structure` | `translate.py`, `main.py` | Low |

### Phase 2: Refinements (Optional)

- Tune detection heuristics based on real documents
- Add layout-label-based detection (if layout model can identify "list" or "nomenclature")
- Support mixed paragraphs (prose with embedded lists)

### Phase 3: Full Architecture (Future)

- Introduce `ContentType` enum: PROSE, STRUCTURED_LIST, TABLE, FORMULA
- Route content types through different processing pipelines
- Train layout model to recognize structured sections

---

## 5. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| False positives (prose treated as structured) | Medium | Medium | Conservative heuristics; fallback to prose |
| Translation quality degradation | Low | Low | Line context usually sufficient for indices |
| Horizontal overflow | Medium | Low | Allow horizontal reflow within line |
| Performance impact | Low | Low | Minimal additional computation |

---

## 6. Recommendation

**Implement Phase 1 immediately.** The minimal solution:
- Preserves existing behavior for prose (no regression)
- Fixes structure preservation for lists/nomenclatures
- Requires ~200-300 lines of code changes
- Can be feature-flagged for safe rollout

The key insight is that we're not changing the architecture—we're adding a **mode** to the existing architecture that respects line boundaries when appropriate.

---

## 7. Success Criteria

After implementation, the Nomenclature section should render as:

```
NOMENCLATURE
c    absolute snelheid
d    diameter
F    stuwkracht
h    specifieke enthalpie
...
```

Each line maintains its vertical position. Horizontal alignment may shift slightly due to translation length differences, but the **semantic line structure** is preserved.

---

*Analysis by: Software Engineering Expert*
*Date: 2026-01-01*
