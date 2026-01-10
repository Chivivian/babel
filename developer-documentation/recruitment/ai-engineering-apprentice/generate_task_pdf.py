import fitz  # PyMuPDF
import os
import re

def strip_markdown(text):
    """Remove markdown formatting and return clean text."""
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = text.replace('—', '-')
    return text

def add_text_block(page, text, x, y, width, fontsize, color, line_height=1.5):
    """Add a text block with proper wrapping and return the new y position."""
    text = strip_markdown(text)
    chars_per_line = int(width / (fontsize * 0.52))
    
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if len(test_line) <= chars_per_line:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    for line in lines:
        page.insert_text(fitz.Point(x, y), line, color=color, fontsize=fontsize)
        y += fontsize * line_height
    
    return y

def generate_pdf():
    doc = fitz.open()
    
    # Paths
    base_dir = r"d:\Desktop D\Apps\babel-lunartech\babel\developer-documentation\recruitment\ai-engineering-apprentice"
    img_dir = os.path.join(base_dir, "images")
    assets_dir = r"d:\Desktop D\Apps\babel-lunartech\babel\assets"
    logo_path = os.path.join(assets_dir, "logo.png")
    cover_path = r"C:\Users\lunar\.gemini\antigravity\brain\aaa6d3fa-3289-488d-8290-7967dfc6cc7f\apprentice_program_cover_png_1768046928609.png"
    
    # Images map
    images = {
        "issue_missing_logos": os.path.join(img_dir, "issue_missing_logos.png"),
        "issue_bold_text": os.path.join(img_dir, "issue_bold_text.png"),
        "issue_bullet_points": os.path.join(img_dir, "issue_bullet_points.png"),
        "issue_table_formatting": os.path.join(img_dir, "issue_table_formatting.png"),
        "issue_headers_footer": os.path.join(img_dir, "issue_headers_footer.png"),
        "issue_section_headers": os.path.join(img_dir, "issue_section_headers.png"),
    }
    
    # Page settings
    margin = 50
    page_width = 595.32  # A4
    page_height = 841.89
    text_width = page_width - 2 * margin
    img_width = 450  # Larger images
    img_height = 280
    
    # Colors
    bg_color = (0.08, 0.08, 0.12)
    gold = (1, 0.84, 0)
    white = (1, 1, 1)
    light_gray = (0.85, 0.85, 0.85)
    cyan = (0.4, 0.8, 1)
    
    # ====== PAGE 1: COVER & PROGRAM INTRO ======
    page = doc.new_page(width=page_width, height=page_height)
    page.draw_rect(page.rect, color=bg_color, fill=bg_color)
    
    y = 60
    page.insert_text(fitz.Point(margin, y), "AI ENGINEERING APPRENTICE PROGRAM", color=gold, fontsize=20)
    y += 40
    
    if os.path.exists(cover_path):
        page.insert_image(fitz.Rect(margin, y, page_width - margin, y + 280), filename=cover_path)
        y += 300
    
    y = add_text_block(page, "Your 6-Month Odyssey from Aspiring Talent to AI Trailblazer", margin, y, text_width, 14, gold)
    y += 20
    
    y = add_text_block(page, "Escaping the 'No Experience, No Job' Loop", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "At LunarTech, we keep meeting incredibly motivated people who are stuck in the same loop: 'Every role asks for experience, but no one wants to give me that first real chance.'", margin, y, text_width, 10, light_gray)
    y += 15
    
    y = add_text_block(page, "You might be:", margin, y, text_width, 10, cyan)
    y += 5
    y = add_text_block(page, "- Armed with self-taught knowledge, bootcamps, or early university projects, but constantly rejected for 'lack of real experience'.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Pivoting careers, grinding through tutorials late at night, but craving the rush of applying your skills to actual, high-stakes products.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- An early-career professional who has done courses and projects, yet feels unprepared for the messy reality of production systems.", margin, y, text_width, 10, light_gray)
    y += 15
    
    y = add_text_block(page, "Our highly competitive, remote-first LunarTech Apprenticeship Programs were created to break that loop.", margin, y, text_width, 10, gold)
    y += 10
    y = add_text_block(page, "Over 6 months, you join an international AI startup, contribute to real products, and develop job-ready skills while being closely mentored by professionals. You're not just watching from the sidelines - you're in the arena.", margin, y, text_width, 10, light_gray)
    
    # ====== PAGE 2: WHAT IS BABEL ======
    page = doc.new_page(width=page_width, height=page_height)
    page.draw_rect(page.rect, color=bg_color, fill=bg_color)
    if os.path.exists(logo_path):
        page.insert_image(fitz.Rect(margin, 20, margin + 40, 55), filename=logo_path)
    page.insert_text(fitz.Point(page_width - margin - 50, 40), "Page 2", color=gold, fontsize=10)
    
    y = 80
    y = add_text_block(page, "What is Babel?", margin, y, text_width, 16, gold)
    y += 15
    
    y = add_text_block(page, "Babel is LunarTech's flagship AI-powered document translation platform. Unlike conventional translation services that treat documents as flat text, Babel preserves the original formatting, layout, and structure of your documents - ensuring that complex PDFs with tables, charts, headers, and multi-column layouts are translated seamlessly.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "The Technology Stack:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "- Agentic OCR: Intelligent optical character recognition that understands document structure, not just raw text.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Large Language Models (GPT-4o): Context-aware translation that understands nuance across entire documents.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- PDF Reconstruction Engine: Rebuilds translated documents with identical layouts and styling.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- BabelDOC Core: The engine that powers our high-fidelity translations with layout analysis and term extraction.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Why This Experience Matters:", margin, y, text_width, 12, gold)
    y += 10
    y = add_text_block(page, "Working on Babel gives you real-world experience with some of the most in-demand technologies in AI engineering:", margin, y, text_width, 10, light_gray)
    y += 15
    y = add_text_block(page, "- Document Intelligence: Learn how to parse, analyze, and reconstruct complex document structures - a skill used in legal tech, healthcare, and enterprise software.", margin, y, text_width, 10, light_gray)
    y += 10
    y = add_text_block(page, "- LLM Integration: Gain hands-on experience integrating and optimizing large language models for production workloads.", margin, y, text_width, 10, light_gray)
    y += 10
    y = add_text_block(page, "- Computer Vision: Work with OCR systems, layout analysis, and image processing - core skills for any AI engineer.", margin, y, text_width, 10, light_gray)
    y += 10
    y = add_text_block(page, "- Production Systems: Debug, optimize, and ship code that serves real users - not just tutorial projects.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "By the end of your apprenticeship, you will have portfolio-ready experience solving complex AI engineering problems that companies actively hire for.", margin, y, text_width, 10, gold)

    # ====== PAGE 3: YOUR MISSION ======
    page = doc.new_page(width=page_width, height=page_height)
    page.draw_rect(page.rect, color=bg_color, fill=bg_color)
    if os.path.exists(logo_path):
        page.insert_image(fitz.Rect(margin, 20, margin + 40, 55), filename=logo_path)
    page.insert_text(fitz.Point(page_width - margin - 50, 40), "Page 3", color=gold, fontsize=10)
    
    y = 80
    y = add_text_block(page, "Your First Mission: Babel v0.1.1", margin, y, text_width, 16, gold)
    y += 15
    
    y = add_text_block(page, "You have been assigned to the Babel Core Team. Your immediate objective is to stabilize and enhance Babel v0.1.1, a version currently facing critical challenges in maintaining document integrity during translation.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "The Goal: 'The Perfect Mirror'", margin, y, text_width, 14, white)
    y += 10
    y = add_text_block(page, "A successful translation in Babel should be the exact same document, only in a different language. We are looking for 100% visual and structural fidelity.", margin, y, text_width, 10, light_gray)
    y += 15
    y = add_text_block(page, "- Fidelity: Font sizes, weights, and colors must be 100% accurate.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Identity: Every logo and brand asset preserved in its exact spatial coordinate.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Structure: Tables and lists must retain their precise grid and bullet logic.", margin, y, text_width, 10, light_gray)
    y += 25
    
    y = add_text_block(page, "Your Journey Structure:", margin, y, text_width, 12, gold)
    y += 10
    y = add_text_block(page, "Onboarding & Orientation (Weeks 1-4): Learn the tools, stack, workflows, and expectations. Complete guided onboarding quests.", margin, y, text_width, 10, light_gray)
    y += 10
    y = add_text_block(page, "Deepening & Delivery (Weeks 5-12): Begin contributing to real features with increasing responsibility.", margin, y, text_width, 10, light_gray)
    y += 10
    y = add_text_block(page, "Ownership & Impact (Weeks 13-20): Tackle complex challenges, participate in sprints, work towards a capstone contribution.", margin, y, text_width, 10, light_gray)
    y += 10
    y = add_text_block(page, "Showcase & Transition (Weeks 21-24): Finalize portfolio pieces, present your work, receive certificate of completion.", margin, y, text_width, 10, light_gray)
    y += 25
    
    y = add_text_block(page, "At LunarTech, you're joining:", margin, y, text_width, 11, white)
    y += 10
    y = add_text_block(page, "- An AI-based, remote-first startup working on deep tech products", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- An international, cross-functional team of engineers, designers, data scientists, and product builders", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- A 6-month, part-time (20-25 hours/week) program you can fit around studies or other responsibilities", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- A mentorship-first culture with structured feedback, not just 'sink or swim' tasks", margin, y, text_width, 10, light_gray)

    # ====== PAGE 4: ISSUE 1 - MISSING LOGOS (DETAILED) ======

    page = doc.new_page(width=page_width, height=page_height)
    page.draw_rect(page.rect, color=bg_color, fill=bg_color)
    if os.path.exists(logo_path):
        page.insert_image(fitz.Rect(margin, 20, margin + 40, 55), filename=logo_path)
    page.insert_text(fitz.Point(page_width - margin - 50, 40), "Page 3", color=gold, fontsize=10)
    
    y = 80
    y = add_text_block(page, "Issue 1: Missing Logos and Images", margin, y, text_width, 16, gold)
    y += 10
    y = add_text_block(page, "Priority: HIGH | Component: PDF Parsing / Image Extraction", margin, y, text_width, 10, cyan)
    y += 20
    
    y = add_text_block(page, "Description:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "Publisher logos (ELSEVIER, ScienceDirect, Applied Energy) from the original document are not being preserved in the translated output. The translated side shows placeholder boxes or missing images.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Expected Behavior:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "All embedded images, including publisher logos, should be extracted from the source PDF and placed in the exact same positions in the translated output.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Screenshot:", margin, y, text_width, 11, gold)
    y += 10
    if os.path.exists(images["issue_missing_logos"]):
        page.insert_image(fitz.Rect(margin, y, margin + img_width, y + img_height), filename=images["issue_missing_logos"])
        y += img_height + 20
    
    y = add_text_block(page, "Proposed Fix:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "- Investigate the image extraction logic in BabelDOC", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Ensure all embedded images (not just figures) are captured", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Verify image placement coordinates are preserved during reconstruction", margin, y, text_width, 10, light_gray)
    
    # ====== PAGE 4: ISSUE 2 - BOLD TEXT (DETAILED) ======
    page = doc.new_page(width=page_width, height=page_height)
    page.draw_rect(page.rect, color=bg_color, fill=bg_color)
    if os.path.exists(logo_path):
        page.insert_image(fitz.Rect(margin, 20, margin + 40, 55), filename=logo_path)
    page.insert_text(fitz.Point(page_width - margin - 50, 40), "Page 4", color=gold, fontsize=10)
    
    y = 80
    y = add_text_block(page, "Issue 2: Bold Text Not Preserved", margin, y, text_width, 16, gold)
    y += 10
    y = add_text_block(page, "Priority: HIGH | Component: Font Style Detection / Reconstruction", margin, y, text_width, 10, cyan)
    y += 20
    
    y = add_text_block(page, "Description:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "Bold text formatting is not being captured during PDF parsing. Section headers like 'Abstract' and '1. Introduction and background' should be bold in the translation, but they appear in regular weight.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Expected Behavior:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "Text styling (bold, italic, bold-italic) should be detected from the source PDF and applied to the corresponding translated text.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Screenshot:", margin, y, text_width, 11, gold)
    y += 10
    if os.path.exists(images["issue_bold_text"]):
        page.insert_image(fitz.Rect(margin, y, margin + img_width, y + img_height), filename=images["issue_bold_text"])
        y += img_height + 20
    
    y = add_text_block(page, "Proposed Fix:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "- Enhance font style detection to capture bold/italic variants", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Map source font styles to equivalent styled fonts in the output", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Ensure style metadata is passed through the translation pipeline", margin, y, text_width, 10, light_gray)
    
    # ====== PAGE 5: ISSUE 5 - BULLET POINTS (DETAILED) ======
    page = doc.new_page(width=page_width, height=page_height)
    page.draw_rect(page.rect, color=bg_color, fill=bg_color)
    if os.path.exists(logo_path):
        page.insert_image(fitz.Rect(margin, 20, margin + 40, 55), filename=logo_path)
    page.insert_text(fitz.Point(page_width - margin - 50, 40), "Page 5", color=gold, fontsize=10)
    
    y = 80
    y = add_text_block(page, "Issue 5: Bullet Points and Numbered Lists Converted to Paragraphs", margin, y, text_width, 14, gold)
    y += 10
    y = add_text_block(page, "Priority: HIGH | Component: List Detection / Text Grouping", margin, y, text_width, 10, cyan)
    y += 20
    
    y = add_text_block(page, "Description:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "Numbered lists and bullet points in the original document are being converted to paragraph format in the translation. The list structure is lost, making the translated content harder to read.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Original:", margin, y, text_width, 11, gold)
    y += 10
    y = add_text_block(page, "1. Select a simple open Brayton Joule thermodynamic cycle...", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "2. Adopt a turbine-inlet temperature smaller than 1000 K...", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "3. Choose a single-shaft configuration...", margin, y, text_width, 10, light_gray)
    y += 15
    
    y = add_text_block(page, "Translated (Incorrect):", margin, y, text_width, 11, (1, 0.4, 0.4))
    y += 10
    y = add_text_block(page, "1. Seleccione un ciclo... 2. Adopte una temperatura... 3. Elija una configuracion... (all collapsed into one paragraph)", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Screenshot:", margin, y, text_width, 11, gold)
    y += 10
    if os.path.exists(images["issue_bullet_points"]):
        page.insert_image(fitz.Rect(margin, y, margin + img_width, y + img_height), filename=images["issue_bullet_points"])
        y += img_height + 20
    
    y = add_text_block(page, "Proposed Fix:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "- Improve list detection in the parsing stage", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Preserve list structure in the intermediate representation", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Ensure newlines between list items are maintained during reconstruction", margin, y, text_width, 10, light_gray)
    
    # ====== PAGE 6: ISSUE 6 - TABLES (CRITICAL) ======
    page = doc.new_page(width=page_width, height=page_height)
    page.draw_rect(page.rect, color=bg_color, fill=bg_color)
    if os.path.exists(logo_path):
        page.insert_image(fitz.Rect(margin, 20, margin + 40, 55), filename=logo_path)
    page.insert_text(fitz.Point(page_width - margin - 50, 40), "Page 6", color=gold, fontsize=10)
    
    y = 80
    y = add_text_block(page, "Issue 6: Table Formatting Completely Broken", margin, y, text_width, 16, gold)
    y += 10
    y = add_text_block(page, "Priority: CRITICAL | Component: Table Detection / Table Reconstruction", margin, y, text_width, 10, (1, 0.3, 0.3))
    y += 20
    
    y = add_text_block(page, "Description:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "Tables in the translated output are completely misaligned and broken. The original document has a clean, properly aligned table with parameter names in the left column and values in the right column. In the translated version, the table structure is destroyed - rows are misaligned, columns don't line up, and the table is nearly unreadable.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Expected Behavior:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "Tables should be detected as structured data. During translation, only the text content should be translated while preserving the exact row/column structure. The output table should maintain identical alignment and formatting as the original.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Screenshot:", margin, y, text_width, 11, gold)
    y += 10
    if os.path.exists(images["issue_table_formatting"]):
        page.insert_image(fitz.Rect(margin, y, margin + img_width, y + img_height), filename=images["issue_table_formatting"])
        y += img_height + 20
    
    y = add_text_block(page, "Proposed Fix:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "- Implement proper table detection in the layout analysis stage", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Preserve table structure (rows, columns, cell boundaries) in the intermediate representation", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Translate cell content individually, not as merged text", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Reconstruct tables with proper column alignment and spacing", margin, y, text_width, 10, light_gray)
    
    # ====== PAGE 7: ISSUE 4 - FOOTERS ======
    page = doc.new_page(width=page_width, height=page_height)
    page.draw_rect(page.rect, color=bg_color, fill=bg_color)
    if os.path.exists(logo_path):
        page.insert_image(fitz.Rect(margin, 20, margin + 40, 55), filename=logo_path)
    page.insert_text(fitz.Point(page_width - margin - 50, 40), "Page 7", color=gold, fontsize=10)
    
    y = 80
    y = add_text_block(page, "Issue 4: Missing Page Footer", margin, y, text_width, 16, gold)
    y += 10
    y = add_text_block(page, "Priority: MEDIUM | Component: Layout Detection / Footer Handling", margin, y, text_width, 10, cyan)
    y += 20
    
    y = add_text_block(page, "Description:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "The footer elements from the original document (copyright notice, DOI, author contact information) are not appearing in the translated output.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Expected Behavior:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "Page headers and footers should be extracted and preserved in the translated document. Footer content may or may not be translated depending on configuration.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Screenshot:", margin, y, text_width, 11, gold)
    y += 10
    if os.path.exists(images["issue_headers_footer"]):
        page.insert_image(fitz.Rect(margin, y, margin + img_width, y + img_height), filename=images["issue_headers_footer"])
        y += img_height + 20
    
    y = add_text_block(page, "Proposed Fix:", margin, y, text_width, 12, white)
    y += 10
    y = add_text_block(page, "- Review footer detection in the layout analysis stage", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Ensure footer regions are not being filtered out", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Add configuration option to translate or preserve original footer text", margin, y, text_width, 10, light_gray)
    
    # ====== PAGE 8: QUOTATION & SUBMISSION ======
    page = doc.new_page(width=page_width, height=page_height)
    page.draw_rect(page.rect, color=bg_color, fill=bg_color)
    if os.path.exists(logo_path):
        page.insert_image(fitz.Rect(margin, 20, margin + 40, 55), filename=logo_path)
    page.insert_text(fitz.Point(page_width - margin - 50, 40), "Page 8", color=gold, fontsize=10)
    
    y = 80
    y = add_text_block(page, "Financial Proposal & Quotation Challenge", margin, y, text_width, 16, gold)
    y += 20
    
    y = add_text_block(page, "High-fidelity document translation is not just a technical challenge - it is a resource optimization problem. You must provide a Project Quotation for the resources required to provide 'Perfect Mirror' translation for a 1000-page document.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Quotation Requirements:", margin, y, text_width, 12, gold)
    y += 10
    y = add_text_block(page, "1. Compute Estimate: Predict the number of LLM tokens (Input/Output) required.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "2. Resource Allocation: Estimate the API costs (OpenAI GPT-4o pricing).", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "3. Engineering Overhead: Calculate the time-to-delivery for the fix.", margin, y, text_width, 10, light_gray)
    y += 25
    
    y = add_text_block(page, "Evaluation Metrics", margin, y, text_width, 14, gold)
    y += 10
    y = add_text_block(page, "1. Structural Fidelity (50%): Mirroring fonts, weights, sizes, and tables.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "2. Technical Robustness (20%): Handling 1000-page files and complex characters.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "3. Quotation Accuracy (10%): Realistic financial proposal.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "4. Code Quality (20%): Modular, well-documented Python standards.", margin, y, text_width, 10, light_gray)
    y += 25
    
    y = add_text_block(page, "Submission Requirements:", margin, y, text_width, 12, gold)
    y += 10
    y = add_text_block(page, "- Codebase: A clean GitHub repository with a clear README.md.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Walkthrough: Report demonstrating your fix for at least three issues.", margin, y, text_width, 10, light_gray)
    y += 5
    y = add_text_block(page, "- Project Quotation: Your resource and cost estimate for the 1000-page use case.", margin, y, text_width, 10, light_gray)
    y += 30
    
    y = add_text_block(page, "To the Stars", margin, y, text_width, 14, gold)
    y += 10
    y = add_text_block(page, "The journey to democratize knowledge starts with a single line of perfectly structured code. Show us what you can build.", margin, y, text_width, 10, light_gray)
    y += 20
    
    y = add_text_block(page, "Learn more: lunartech.ai/blog/the-lunartech-apprenticeship-programs", margin, y, text_width, 10, cyan)
    y += 30
    
    if os.path.exists(logo_path):
        page.insert_image(fitz.Rect(page_width/2 - 40, y, page_width/2 + 40, y + 80), filename=logo_path)
        y += 90
    page.insert_text(fitz.Point(page_width/2 - 100, y), "LunarTech Core Architecture Team", color=gold, fontsize=10)
    
    output_path = os.path.join(base_dir, "AI_Engineering_Apprentice_Task_Description.pdf")
    doc.save(output_path)
    print(f"PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    generate_pdf()
