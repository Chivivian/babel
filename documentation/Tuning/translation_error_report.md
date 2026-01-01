# Comprehensive Translation Error Report - Babel 0.1.0

**Date:** January 1, 2026
**Subject:** Forensic Analysis of Graphic and Vector rendering Failures
**Affected Version:** Babel 0.1.0 (Development Build)

## 1. Executive Summary
A detailed visual inspection of the translated output "Babel 0.1.0" confirms a **catastrophic rendering failure** regarding vector graphics and geometric primitives. The translation pipeline successfully processes and re-renders text (including captions, labels, and paragraph body), but it systematically eliminates non-text visual elements such as lines, curves, filled rectangles, and stroke paths.

This selective rendering suggests that the `ILCreater` (Intermediate Language Creater) is correctly identifying text via `LTChar` objects but is either failing to capture or actively suppressing `LTCurve`, `LTLine`, and `LTRect` objects during the `PDFCreater` reconstruction phase.

## 2. Detailed Verification and Error Analysis

### Case Study A: Schematic Diagrams and Flowcharts
**Visual Evidence:** `babel 0.1.0/image_7.png`
![Schematic Failure](babel%200.1.0/image_7.png)

#### Detailed Observation
*   **Target Artifacts:** Figure 4 ("INITIAL CYCLE MODEL") and Figure 5 ("EXTENDED CYCLE MODEL").
*   **What is Present:**
    *   **Text Labels:** All text nodes such as "GGT", "PT", "6/7", "10", and the input/output arrows' labels like "$\pi_{C}$" (rendered as text) are present.
    *   **Captions:** The figure captions "РИСУНОК 4..." and "РИСУНОК 5..." are correctly translated and positioned.
*   **What is Missing:**
    *   **Connectivity:** All connecting lines that define the flow of the cycle are absent.
    *   **Components:** The symbolic representations of the compressor, turbine, and heat exchanger (circles, trapezoids, rectangles) are completely invisible.
    *   **Arrows:** Directional indicators (arrowheads) are missing.
*   **Technical Diagnosis:**
    *   These diagrams typically consist of stroked paths (`m`, `l`, `s` PDF operators). The absence of these paths while text remains in the correct *relative* positions indicates that the coordinate system (`CTM`) is correct, but the **draw operations** for curves are being skipped.
    *   **Root Cause:** The `skip_curve_render` flag was enabled, or `PdfCurve` objects were marked with `debug_info=True`, preventing them from rendering in the final "Production" output.

---

### Case Study B: Quantitative Graphs and Mathematical Layouts
**Visual Evidence:** `babel 0.1.0/image_8.png`
![Graph Failure](babel%200.1.0/image_8.png)

#### Detailed Observation
*   **Target Artifacts:** Figure 3 ("IDEAL TURBO JET CYCLE") and surrounding equations.
*   **What is Present:**
    *   **Axis Labels:** The numbers "0", "s", "6-10s" are floating in white space, marking where the X and Y axes should be.
    *   **Equation Text:** Parts of the equations are visible but appear structurally unsound (e.g., missing fraction bars or radical lines).
    *   **Raster Images:** Interestingly, Figure 2 (the 3D cutaway engine render) appears to be a raster image and **is** rendered correctly.
*   **What is Missing:**
    *   **Coordinate System:** The X and Y axis lines are missing.
    *   **Data Series:** The red plot line representing the cycle path is absent.
    *   **Annotations:** Leader lines connecting labels to specific points on the graph are gone.
    *   **Formula Structure:** Fraction bars (which are often drawn as vector lines rather than text font characters) are likely missing, making equations like $\frac{a}{b}$ look like floating $a$ and $b$.
*   **Technical Diagnosis:**
    *   The successful rendering of Figure 2 (Raster/ImageXObject) vs. the failure of Figure 3 (Vector/Curve) isolates the issue specifically to **Vector Graphics**.
    *   Equation fraction bars are often implemented as `LTCurve` or `LTRect` with a small height. Their absence confirms the global suppression of line drawing operations.

---

### Case Study C: Data Visualization (Bar Charts)
**Visual Evidence:** `babel 0.1.0/image_9.png`
![Bar Chart Failure](babel%200.1.0/image_9.png)

#### Detailed Observation
*   **Target Artifacts:** Comparison Bar Charts for engine power.
*   **What is Present:**
    *   **Grid Context:** The Y-axis values ("150", "100", "50") and X-axis labels ("Jet", "Shaft") are rendered.
    *   **Legend Text:** The names of the engines (AMT, KingTech, etc.) are visible in the legend area.
*   **What is Missing:**
    *   **The Data:** The colored bars themselves are completely gone.
    *   **Legend Swatches:** The colored boxes next to the legend names are missing.
    *   **Frame:** The box surrounding the chart is missing.
*   **Technical Diagnosis:**
    *   Bar charts use **Filled Paths** (`f` or `B` operators) rather than just stroked lines. The fact that these are also missing suggests the issue is not limited to line width (stroke) but affects **all vector path rendering**, including fills.
    *   This implies that `PdfCurve` or `PdfRectangle` objects carrying the fill instructions are being discarded or ignored.

---

### Case Study D: Structured Text Areas (Nomenclature)
**Visual Evidence:** `babel 0.1.0/image_10.png`
![Nomenclature Failure](babel%200.1.0/image_10.png)

#### Detailed Observation
*   **Target Artifacts:** Nomenclature Table/List.
*   **What is Present:**
    *   The translated terms are present.
*   **What is Missing/Broken:**
    *   **Alignment/Tabulation:** The user circled this area, indicating a layout break. Without vertical dividing lines or proper tab stop visualizers (often invisible lines in PDF), the distinct columns for "Symbol" and "Description" may have merged or drifted.
    *   **Grouping:** If the original used lines to group related parameters, those lines are gone, making the list harder to read.
*   **Technical Diagnosis:**
    *   While mostly text, the "structure" of such lists is often enforced by visual guides or lines that have been stripped. The layout engine might rely on these boundaries for column separation, and their removal caused the "Paragraph Finder" to merge disjoint columns.

## 3. Conclusion and Remix
The evidence is conclusive: **The translation layer is aggressively stripping vector graphics.**

1.  **Text vs. Graphics:** Text translation (`LTChar`) is functional. Raster image pass-through (`LTImage`) appears functional. Vector graphic pass-through (`LTCurve`, `LTLine`, `LTRect`) is broken.
2.  **Severity:** This is a **Blocker**. Scientific and engineering papers are unintelligible without their diagrams and charts.
3.  **Remediation Action:**
    *   The flag `--skip-curve-render` must be permanently disabled.
    *   The logic in `il_creater.py` must default `debug_info` to `False` for valid content to ensure it renders in production mode.
    *   The `pdf_creater.py` must iterate over all curve objects and render them unless they are explicitly marked as "debug-only" metadata.

## 4. Deep Dive Analysis & Secondary Risks

### A. Color and Style Fidelity (The "Invisible Ink" Risk)
Even if we force the rendering of curves, we must ensure their **Graphic State** is preserved. The `PdfCurve` relies on `passthrough_per_char_instruction` to carry PDF operators for:
*   **Color**: `RG` (stroke RGB), `rg` (fill RGB), `K`/`k` (CMYK).
*   **Stroke Weight**: `w` (line width).
*   **Style**: `d` (dash pattern).
**Risk**: If `ILCreater` doesn't strictly copy these states from the `LTCurve`, we will render "default black" lines instead of the semantic colors (e.g., Red for "Heat", Blue for "Cold") seen in the originals. The Bar Chart in Figure 7 loses all meaning without color differentiation.

### B. Structural Layout Dependency (The "Nomenclature" Effect)
The degradation in the Nomenclature section (Image 10) is likely a secondary effect of the missing vectors.
*   **Mechanism**: Layout analysis engines often use vertical lines (table borders) to distinguish "Columns" from "Close Words".
*   **Failure Chain**: When we strip the vertical lines -> The Layout Parser sees whitespace only -> It may interpret the gap as a "Space" rather than a "Full Tab/Column Break" -> The Text Merger combines "Symbol" and "Definition" into a single text line -> The Translator translates the merged phrase as a sentence (e.g., "c specific work" -> "c specificeren werk").
*   **Conclusion**: Restoring vector lines is a prerequisite for fixing the table layout.

### C. Text-Graphic Conflict (The "Cleaning" Hazard)
The flag `--remove-non-formula-lines` was designed to clean up "garbage" lines (like underlines).
*   **Conflict**: In technical diagrams (like Fig 4), text labels ("GGT", "PT") are often placed *directly on top of* or *very close to* the diagram lines.
*   **Outcome**: An aggressive cleaning algorithm will see a line intersecting a text box and delete it, thinking it's a strikethrough or artifact.
*   **Recommendation**: This feature must be strictly disabled for technical documents where "Text touching Line" is a valid semantic relationship (label + leader line).
