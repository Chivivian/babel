
import fitz  # PyMuPDF
import os

def create_rich_task_pdf():
    output_path = r"d:\Desktop D\Apps\babel-lunartech\babel\documentation\Tuning\Mission_Vector_Restoration.pdf"
    image_dir = r"d:\Desktop D\Apps\babel-lunartech\babel\documentation\Tuning\babel 0.1.0"
    
    doc = fitz.open()

    # --- Styles ---
    # Since we lack custom fonts in this env, we rely on size/bold variations of standard fonts
    # Colors (RGB)
    COLOR_PRIMARY = (0, 0, 0.5)  # Navy Blue
    COLOR_ALERT = (0.6, 0.1, 0.1)  # Dark Red
    COLOR_TEXT = (0, 0, 0)
    
    def title(page, text):
        page.insert_text((50, 50), text, fontsize=24, color=COLOR_PRIMARY)
        return 80

    def heading(page, y, text):
        page.insert_text((50, y), text, fontsize=16, color=COLOR_PRIMARY)
        return y + 25

    def body(page, y, text, height=None):
        rect = fitz.Rect(50, y, 550, y + (height if height else 500))
        page.insert_textbox(rect, text, fontsize=11, align=0)
        # simplistic heuristic for new Y: count newlines somewhat or fixed block
        # For this script, we'll manually manage spacing or use large blocks
        return y + (height if height else 100) + 10

    def caption(page, y, text):
        page.insert_text((50, y), text, fontsize=9, color=(0.3, 0.3, 0.3), style=2) # italicish if possible, else normal
        return y + 20

    # =========================================================================
    # PAGE 1: THE MISSION BRIEFING
    # =========================================================================
    page = doc.new_page()
    y = title(page, "OPERATION: VECTOR RESTORATION")
    
    y = heading(page, y, "1. The Narrative Context")
    story_text = (
        "We are building the definitive translation engine for complex scientific documents. "
        "Our system excel at linguistics—translating text, resizing boxes, and matching fonts. "
        "However, we have encountered a critical blind spot in our 'vision'.\n\n"
        "Consider the engineer analyzing a Jet Engine schematic. To them, the text labels 'GGT' "
        "(Gas Generator Turbine) or 'PT' (Power Turbine) are merely nouns. The *verbs* of the system—the "
        "arrows showing airflow, the lines defining the mechanical linkages, the boxes representing "
        "chambers—are the actual schematic soul of the document.\n\n"
        "Currently, our translation pipeline inadvertently acts as a content filter. It sees text as signal "
        "and lines/shapes as noise. It strips the schematic soul, leaving behind a 'ghost document'—labels "
        "floating in a white void. This is not just a bug; it is a breakdown of knowledge transfer."
    )
    y = body(page, y, story_text, height=180)
    
    y = heading(page, y, "2. The Objective")
    obj_text = (
        "Your mission is to restore the visual language of these documents. We must stop stripping "
        "vector graphics (LTCurve, LTLine, LTRect) and start treating them as first-class citizens "
        "alongside the text.\n\n"
        "The output PDF must be visually indistinguishable from the input PDF, except for the language "
        "of the text. All diagrams, graphs, and charts must survive the translation process intact."
    )
    y = body(page, y, obj_text, height=100)
    
    y = heading(page, y, "3. The Critical Protocol")
    warn_text = (
        "WARNING: Restoring these lines requires surgical precision. We previously disabled them "
        "because they caused 'blue debug boxes' or interfered with layout detection. "
        "The fix must be robust: render the content lines, but keep the debug boxes hidden."
    )
    page.insert_textbox(fitz.Rect(50, y, 550, y+100), warn_text, fontsize=11, color=COLOR_ALERT)

    # =========================================================================
    # PAGE 2: VISUAL EVIDENCE (Schematics)
    # =========================================================================
    page = doc.new_page()
    y = title(page, "EXHIBIT A: THE GHOST SCHEMATICS")
    
    img_path = os.path.join(image_dir, "image_7.png")
    if os.path.exists(img_path):
        # Top half
        page.insert_image(fitz.Rect(50, 80, 550, 400), filename=img_path)
        
    y = 410
    caption_text = (
        "Fig 1. Analysis of Failure in Schematic Diagrams (Figure 4 & 5).\n"
        "Observe the labels 'GGT', 'PT', and '10'. They are correctly positioned and translated. "
        "However, they are suspended in nothingness. The logic lines connecting the gas generator to the "
        "power turbine are gone. The arrow indicating heat flow (Q) is gone. The block diagram boxes are gone. "
        "Result: The diagram is scientifically useless."
    )
    y = body(page, y, caption_text, height=80)

    # =========================================================================
    # PAGE 3: VISUAL EVIDENCE (Graphs & Charts)
    # =========================================================================
    page = doc.new_page()
    y = title(page, "EXHIBIT B: DATA LOSS") # A bit overlap on title y, fixed by standardizing
    
    # Graphs
    y = 80
    img_path = os.path.join(image_dir, "image_8.png")
    if os.path.exists(img_path):
        page.insert_image(fitz.Rect(50, y, 300, y+200), filename=img_path)
        
    # Bar Chart
    img_path2 = os.path.join(image_dir, "image_9.png")
    if os.path.exists(img_path2):
        page.insert_image(fitz.Rect(310, y, 560, y+200), filename=img_path2)
        
    y += 220
    caption_text = (
        "Left: The 'Ideal Turbo Jet Cycle' graph has lost its coordinate axes and the cycle plot curve. "
        "It is a map without roads.\n"
        "Right: The Power Comparison bar chart. The legends remain, but the colored bars representing "
        "the actual 15kW/20kW data points are missing. The comparison is impossible to read."
    )
    y = body(page, y, caption_text, height=60)
    
    y = heading(page, y, "Forensic Conclusion")
    concl = (
        "The translation engine successfully identified text blocks but discarded the 'LTCurve' objects "
        "that make up the axes, frames, plot lines, and bars. It treated them as background noise to be cleaned."
    )
    y = body(page, y, concl, height=50)

    # =========================================================================
    # PAGE 4: TECHNICAL EXECUTION PLAN
    # =========================================================================
    page = doc.new_page()
    y = title(page, "TECHNICAL EXECUTION GUIDE")
    
    y = heading(page, y, "Phase 1: Configuration Hygiene")
    text_p1 = (
        "Location: translate.py\n"
        "Action: Remove the hardcoded '--skip-curve-render' flag.\n"
        "Why: This flag is the master switch that turned off our vector engine. It must be destroyed. "
        "Also, ensure '--remove-non-formula-lines' is disabled by default to prevent over-aggressive cleaning."
    )
    y = body(page, y, text_p1, height=80)
    
    y = heading(page, y, "Phase 2: The Parsing Layer (ILCreater)")
    text_p2 = (
        "Location: babeldoc/format/pdf/document_il/frontend/il_creater.py\n"
        "Action: Re-classify Curves.\n"
        "Method:\n"
        "1. In 'on_lt_curve', locate the construction of the 'PdfCurve' object.\n"
        "2. Change 'debug_info=True' (or None) to 'debug_info=False'.\n"
        "3. This semantic shift tells the system: 'This is not a debug artifact. This is content.'"
    )
    y = body(page, y, text_p2, height=100)
    
    y = heading(page, y, "Phase 3: The Rendering Layer (PDFCreater)")
    text_p3 = (
        "Location: babeldoc/format/pdf/document_il/backend/pdf_creater.py\n"
        "Action: Enforce Render Loop.\n"
        "Method:\n"
        "1. In the 'get_render_units' method, locate the curve processing loop.\n"
        "2. The condition 'if (not curve.debug_info) or translation_config.debug:' is the targeted logic.\n"
        "3. Ensure that if a curve is marked as CONTENT (debug_info=False), it renders regardless of debug mode.\n"
        "4. Verify that no 'bounding box' stroke is added unless specifically requested."
    )
    y = body(page, y, text_p3, height=120)

    y = heading(page, y, "Critical Risk Factors (Deep Dive)")
    text_deepchecks = (
        "1. Color Fidelity: The 'Graphic State' must carry the original colors (RG/rg operators). "
        "   Without this, the Bar Charts (Exhibit B) will render as black boxes.\n"
        "2. Layout Dependency: The Nomenclature table (Exhibit D) likely failed because the missing vertical lines "
        "   caused the layout parser to merge columns. Fixing vectors may auto-fix the layout.\n"
        "3. Collision Cleaning: Ensure '--remove-non-formula-lines' is OFF. Otherwise, labels touching diagram lines "
        "   (Exhibit A) will trigger accidental deletion of those lines."
    )
    y = body(page, y, text_deepchecks, height=100)
    
    y = heading(page, y, "Tools & Verification")
    text_p4 = (
        "- Use 'translate.py' to run a test on the 'Design...micro-turbojet.pdf' document.\n"
        "- Inspect Page 3 (Schematics) and Page 4 (Graphs).\n"
        "- Success Condition: The Translated PDF must contain red graph lines and black diagram paths interacting cleanly with the translated text."
    )
    y = body(page, y, text_p4, height=80)

    # =========================================================================
    # PAGE 5: SOLUTION STATUS
    # =========================================================================
    page = doc.new_page()
    y = title(page, "SOLUTION STATUS")
    
    y = heading(page, y, "Fixes Applied")
    fix_applied = (
        "1. translate.py: Removed '--skip-curve-render' flag (done earlier).\n"
        "2. translate.py: Removed '--remove-non-formula-lines' flag (done earlier).\n"
        "3. translate.py: Removed '--disable-graphic-element-process' from fast mode.\n"
        "4. il_creater.py: Set 'debug_info=False' for PdfCurve objects so they render as content.\n"
        "5. pdf_creater.py: Logic already correctly renders curves when debug_info=False."
    )
    y = body(page, y, fix_applied, height=120)
    
    y = heading(page, y, "Verification Required")
    verify_text = (
        "Run a translation with 'python translate.py <pdf> nl' and verify:\n"
        "- Schematic diagrams show all connecting lines and arrows.\n"
        "- Graphs show axes and data curves in original colors.\n"
        "- Bar charts show colored data bars.\n"
        "- Nomenclature columns remain distinct (not merged)."
    )
    y = body(page, y, verify_text, height=100)
    
    y = heading(page, y, "The Philosophy")
    philosophy = (
        "Babel is not allowed to delete what it does not understand.\n\n"
        "Any graphical element from the source PDF—text, vector, raster—is SACRED. "
        "Cleaning algorithms may only HIDE debug artifacts (our own boxes), never REMOVE original content."
    )
    y = body(page, y, philosophy, height=80)

    # Save
    doc.save(output_path)
    print(f"Mission Briefing PDF generated at: {output_path}")

if __name__ == "__main__":
    create_rich_task_pdf()
