import os
from datetime import datetime

from fpdf import FPDF

EXPORT_FOLDER = "static/exports"
FONT_PATH = "static/fonts/DejaVuSans.ttf"


def save_pdf(layout: list) -> str:
    """
    Compiles the layout into an exportable multi-page PDF document.
    """
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    use_unicode = False

    if os.path.exists(FONT_PATH):
        pdf.add_font("DejaVu", "", FONT_PATH)
        pdf.set_font("DejaVu", "", 12)
        use_unicode = True
    else:
        pdf.set_font("Helvetica", size=12)

    for panel in layout:
        image_path = panel["image_path"]
        story_text = panel["text"]
        pdf.add_page()

        if use_unicode:
            pdf.set_font("DejaVu", "", 14)
        else:
            pdf.set_font("Helvetica", style="B", size=14)

        pdf.cell(0, 10, f"Panel {panel['panel']}: {panel['title']}", new_x="LMARGIN", new_y="NEXT", align="C")

        if use_unicode:
            pdf.set_font("DejaVu", "", 12)
        else:
            pdf.set_font("Helvetica", size=11)

        y_image = 30
        image_height = 100
        spacing_after_image = 15

        if os.path.exists(image_path):
            pdf.image(image_path, x=25, y=y_image, w=160, h=image_height)
        else:
            pdf.set_y(y_image)
            pdf.multi_cell(0, 10, f"Image missing: {image_path}")

        pdf.set_y(y_image + image_height + spacing_after_image)

        if not use_unicode:
            story_text = story_text.encode("latin-1", "replace").decode("latin-1")

        pdf.multi_cell(0, 8, story_text)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = os.path.join(EXPORT_FOLDER, filename)
    pdf.output(pdf_path)
    return pdf_path
