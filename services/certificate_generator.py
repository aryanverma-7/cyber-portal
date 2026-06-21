from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDoc, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from datetime import datetime
import os
import uuid

class CertificateGenerator:
    """PDF Certificate generator"""
    
    def __init__(self):
        self.certificates_dir = Config.CERTIFICATES_DIR
    
    def generate_course_certificate(self, user, course):
        """Generate certificate for course completion"""
        
        cert_number = f"CS-{datetime.utcnow().year}-{uuid.uuid4().hex[:8].upper()}"
        filename = f"certificate_{user.id}_{course.id}_{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(self.certificates_dir, filename)
        
        doc = SimpleDoc(filepath, pagesize=landscape(letter))
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=36,
            textColor=HexColor('#00d4ff'),
            alignment=1,
            fontName='Helvetica-Bold'
        )
        
        text_style = ParagraphStyle(
            'CustomText',
            parent=styles['Normal'],
            fontSize=16,
            textColor=black,
            alignment=1
        )
        
        # Build certificate
        content = []
        
        # Header
        content.append(Paragraph("🛡️ CYBERSHIELD", title_style))
        content.append(Paragraph("CERTIFICATE OF COMPLETION", text_style))
        content.append(Paragraph("", styles['Normal']))
        
        # Recipient
        content.append(Paragraph("This certificate is proudly awarded to", text_style))
        content.append(Paragraph("", styles['Normal']))
        content.append(Paragraph(f"{user.get_full_name()}".upper(), 
                                ParagraphStyle('Name', parent=text_style, fontSize=28)))
        content.append(Paragraph("", styles['Normal']))
        
        # Course
        content.append(Paragraph("For successfully completing the course", text_style))
        content.append(Paragraph("", styles['Normal']))
        content.append(Paragraph(f'"{course.title}"'.upper(), 
                                ParagraphStyle('Course', parent=text_style, fontSize=22)))
        content.append(Paragraph("", styles['Normal']))
        
        # Details
        details = [
            ["Certificate Number:", cert_number],
            ["Date:", datetime.utcnow().strftime('%B %d, %Y')],
            ["Duration:", f"{course.duration_minutes} minutes"],
            ["Level:", course.level]
        ]
        
        table = Table(details)
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        content.append(table)
        content.append(Paragraph("", styles['Normal']))
        
        # Footer
        content.append(Paragraph("🔐 Cybersecurity Awareness & Threat Education", text_style))
        content.append(Paragraph("www.cybershield.platform", text_style))
        
        doc.build(content)
        
        return filename