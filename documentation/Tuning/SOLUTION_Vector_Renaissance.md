# The Babel Vector Renaissance: A Complete Engineering Solution

---

## 📜 Preamble: Understanding The Soul of the Problem

The Babel translation engine is a marvel of PDF surgery. It dissects documents into their atomic components—characters, curves, forms, paragraphs—translates the linguistic layer, and reconstructs a new document that speaks a different language while preserving the visual identity.

But we have a blind spot. We see **text** as a first-class citizen, but we treat **vectors** (the lines, curves, and shapes that make diagrams legible) as unwanted guests. We built filters to clean "noise," and those filters became too aggressive. They stripped the schematic soul from engineering documents.

This document presents the **complete solution architecture**—not patches, but a coherent philosophy for how Babel should treat visual elements.

---

## 🔍 Root Cause Analysis: The Three Gates

Every vector graphic must pass through three gates to survive translation. Any one of these gates being closed will kill the graphic.

### Gate 1: The Collection Gate (`ILCreater`)
**Location:** `babeldoc/format/pdf/document_il/frontend/il_creater.py`

The `on_lt_curve` method receives every curve from the PDF parser. It has a gatekeeper:

```python
def on_lt_curve(self, curve: babeldoc.pdfminer.layout.LTCurve):
    if not self.enable_graphic_element_process:
        return  # GATE CLOSED
```

**Problem:** When `--disable-graphic-element-process` is passed (including in "fast" mode in `translate.py`), this gate slams shut. No curves are even collected into the Intermediate Language.

**Current State:** `translate.py` calls `--disable-graphic-element-process` in fast mode (line 177).

---

### Gate 2: The Classification Gate (`debug_info` flag)
**Location:** `il_creater.py` → `PdfCurve` construction

Every curve is assigned a `debug_info` attribute:

```python
curve_obj = il_version_1.PdfCurve(
    ...
    debug_info=False,  # Currently set to False by default (fixed in earlier pass)
    ...
)
```

**Current State:** ✅ Already fixed. Original graphics are marked as content (`debug_info=False`).

---

### Gate 3: The Rendering Gate (`PDFCreater`)
**Location:** `babeldoc/format/pdf/document_il/backend/pdf_creater.py`

The `get_render_units` method decides what actually gets drawn:

```python
if not translation_config.skip_curve_render:
    all_curves = list(page.pdf_curve) + formula_curves
    for i, curve in enumerate(all_curves):
        if (not curve.debug_info) or translation_config.debug:
            render_units.append(CurveRenderUnit(...))
```

**Problem 1:** If `translation_config.skip_curve_render` is `True`, all curves are skipped.
**Problem 2:** If a curve has `debug_info=True` and we're not in debug mode, it's skipped.

**Current State:** `translate.py` no longer passes `--skip-curve-render`. Gate 3 is open for content curves.

---

## 🏗️ The Complete Solution Architecture

### Solution 1: Disable Fast Mode's Graphic Destruction

**File:** `translate.py`
**Current Issue:** Fast mode disables graphic processing entirely.

```python
if kwargs.get("fast"):
    cmd.extend([
        "--skip-scanned-detection",
        "--disable-graphic-element-process"  # <-- This kills all graphics
    ])
```

**Solution:** Remove `--disable-graphic-element-process` from fast mode. If speed is needed, skip *other* operations (like OCR detection), but never skip vector collection.

```python
if kwargs.get("fast"):
    cmd.extend([
        "--skip-scanned-detection",
        # Graphics must ALWAYS be processed. Speed optimization should target
        # CPU-intensive analysis stages (layout AI, OCR), not vector preservation.
    ])
```

---

### Solution 2: Ensure Color and Style Preservation

**File:** `il_creater.py` → `create_graphic_state`
**Current State:** The `passthrough_per_char_instruction` carries the PDF graphic state operators (color, line width, dash patterns).

**Verification:** The method correctly builds the instruction string from the curve's `passthrough_instruction`. No fix needed here, but we must ensure the *renderer* respects it.

**File:** `pdf_creater.py` → `CurveRenderUnit.render`

The render method already applies the passthrough instruction:
```python
draw_op.append(
    curve.graphic_state.passthrough_per_char_instruction.encode(),
)
```

**Status:** ✅ Color/style preservation is already implemented correctly. The problem was earlier: curves weren't reaching the render stage at all.

---

### Solution 3: Protect Diagrams from Line Cleaning

**File:** `babeldoc/format/pdf/document_il/midend/styles_and_formulas.py`
**Current Issue:** The `--remove-non-formula-lines` flag triggers logic that tries to clean up "decorative" lines. This is dangerous for technical documents.

**Solution:** Never enable this flag by default. It should be an explicit opt-in for documents with known excessive underlines.

**File:** `translate.py`

Ensure the following is **NOT** in the command construction:
```python
# DO NOT USE: "--remove-non-formula-lines"
```

**Additional Safety Net:** Modify the cleaning logic to protect lines that are:
1. Inside a layout region classified as "figure" or "table"
2. Connected to text labels (within N pixels)
3. Part of a closed path (likely a box or shape, not a stray underline)

---

### Solution 4: Forms and XObjects (Images Inside Containers)

**File:** `il_creater.py` → `on_xobj_form`
**Current Issue:** Some diagrams are embedded as Form XObjects, not raw curves. If form rendering is skipped, these vanish.

**Verification:**
```python
if not translation_config.skip_form_render:
    # Render forms
```

**Status:** `translate.py` does not pass `--skip-form-render`. Forms should render.

---

## 📝 The Implementation Checklist

| Step | File | Action | Status |
|------|------|--------|--------|
| 1 | `translate.py` | Remove `--disable-graphic-element-process` from fast mode | **TODO** |
| 2 | `il_creater.py` | Confirm `debug_info=False` for `PdfCurve` | ✅ Done |
| 3 | `pdf_creater.py` | Confirm render logic allows content curves | ✅ Done |
| 4 | `translate.py` | Ensure `--skip-curve-render` is never passed | ✅ Done |
| 5 | `translate.py` | Ensure `--remove-non-formula-lines` is never passed | ✅ Done |
| 6 | `styles_and_formulas.py` | Add figure/table protection to line cleaning | **OPTIONAL** |

---

## 🧪 Verification Protocol

After applying the fix, run:

```bash
cd babel
python translate.py --fast "test_pdfs/Design and Manufacture of a mini-turbojet.pdf" nl
```

Then manually inspect:
1. **Page 3 (Schematics):** Figure 4 and 5 must show all connecting lines and arrows.
2. **Page 4 (Graphs):** Figure 3 must show axes and the red data curve.
3. **Page 2 (Bar Chart):** Colored bars must be visible.
4. **Page 1 (Nomenclature):** Columns must be distinct (not merged).

---

## 🌟 The Philosophy Going Forward

> "Babel is not allowed to delete what it does not understand."

Any graphical element from the source PDF—text, vector, raster—is **sacred**. Cleaning algorithms may only *hide* debug artifacts (our own boxes), never *remove* original content.

The flags `--skip-curve-render` and `--disable-graphic-element-process` should be reserved for debugging internals, never exposed to users, and never enabled by default in any mode.

---

*Document authored for the Babel 0.2.0 Renaissance Release*
