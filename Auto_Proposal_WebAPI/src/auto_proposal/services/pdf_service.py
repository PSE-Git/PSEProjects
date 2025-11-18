import os
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from ..core import models

class PDFService:
    def __init__(self, output_dir: str = "pdf_files"):
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)

    def generate_proposal_pdf(
        self,
        proposal: models.Proposal,
        template: str = "default",
        include_terms: bool = True
    ) -> str:
        """Generate PDF for a proposal and return the file path."""
        
        # Create filename
        filename = f"proposal_{proposal.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph("PROJECT PROPOSAL", title_style))
        story.append(Spacer(1, 20))

        # Client info
        client_info = f"""
        <b>Client:</b> {proposal.client.name}<br/>
        <b>Business Type:</b> {proposal.client.business_type}<br/>
        <b>Email:</b> {proposal.client.email}<br/>
        <b>Phone:</b> {proposal.client.phone}<br/>
        <b>Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/>
        """
        story.append(Paragraph(client_info, styles['Normal']))
        story.append(Spacer(1, 20))

        # Proposal details
        proposal_info = f"""
        <b>Title:</b> {proposal.title}<br/>
        <b>Description:</b> {proposal.description or 'N/A'}<br/>
        """
        story.append(Paragraph(proposal_info, styles['Normal']))
        story.append(Spacer(1, 20))

        # Items table
        if proposal.proposal_items:
            table_data = [['Item', 'Description', 'Quantity', 'Unit Price', 'Total']]
            for item in proposal.proposal_items:
                table_data.append([
                    item.item_name,
                    item.description or '',
                    f"{item.quantity:.2f}",
                    f"${item.unit_price:,.2f}",
                    f"${item.total:,.2f}"
                ])

            # Add total
            table_data.extend([
                ['', '', '', '', ''],
                ['TOTAL', '', '', '', f"${proposal.amount:,.2f}"]
            ])

            # Create and style table
            table = Table(table_data, colWidths=[2*inch, 2*inch, 1*inch, 1.25*inch, 1.25*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)

        # Terms and conditions
        if include_terms:
            story.append(Spacer(1, 30))
            story.append(Paragraph("<b>Terms and Conditions</b>", styles['Heading2']))
            terms = """
            1. All prices are valid for 30 days from the proposal date.
            2. Payment terms: 50% advance, remaining upon completion.
            3. Timeline will be finalized upon project initiation.
            4. Changes to the scope may affect pricing and timeline.
            """
            story.append(Paragraph(terms, styles['Normal']))

        # Build PDF
        doc.build(story)
        
        return filepath