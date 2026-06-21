from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(
    filename,
    report_text
):

    pdf = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = [

        Paragraph(
            "CyberShield Interview Report",
            styles["Title"]
        ),

        Spacer(1,20),

        Paragraph(
            report_text,
            styles["BodyText"]
        )

    ]

    pdf.build(content)