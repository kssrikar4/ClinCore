import polars as pl
from pathlib import Path
from ClinCore.config import StudyConfig
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_reports(config: StudyConfig, study_dir: Path):
    out_dir = study_dir / "output"
    adam_dir = out_dir / "adam"
    pdf_path = out_dir / "tlfs.pdf"
    
    if not config.reports:
        return

    doc = SimpleDocTemplate(
        str(pdf_path), 
        pagesize=landscape(letter),
        rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
    )
    styles = getSampleStyleSheet()
    elements = []

    # Calculate available width (11 inches - margins)
    available_width = 11 * inch - 60 

    # Create distinct styles to avoid mutation issues
    body_p_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=7,
        leading=8,
        textColor=colors.black  # Explicitly Black for visibility
    )

    header_p_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica-Bold',
        textColor=colors.whitesmoke, # White for contrast against Grey header
        alignment=1 # Center aligned
    )

    for report in config.reports:
        ds_path = adam_dir / f"{report.dataset.lower()}.csv"
        if not ds_path.exists():
            continue
            
        df = pl.read_csv(ds_path)
        available_cols = [c for c in report.columns if c in df.columns]
        if not available_cols:
            continue
            
        display_df = df.select(available_cols)
        
        # Add Title
        title = Paragraph(f"<b>Report: {report.id} ({report.type}) - Dataset: {report.dataset}</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        data = []
        # Headers
        data.append([Paragraph(f"<b>{c}</b>", header_p_style) for c in display_df.columns])
        
        # Rows
        for row in display_df.head(100).iter_rows():
            data.append([Paragraph(str(x) if x is not None else "", body_p_style) for x in row])
            
        # Calculate dynamic column widths
        num_cols = len(display_df.columns)
        col_width = available_width / num_cols
        
        # Create Table
        table = Table(data, colWidths=[col_width] * num_cols, repeatRows=1)
        
        # Table Styling
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ])
        
        # Add alternating row colors for readability
        for i, _ in enumerate(data[1:], 1):
            if i % 2 == 0:
                style.add('BACKGROUND', (0, i), (-1, i), colors.whitesmoke)
            else:
                style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey)
        
        table.setStyle(style)
        elements.append(table)
        elements.append(Spacer(1, 24))
        print(f"Adding report {report.id} to PDF (Columns: {', '.join(available_cols)})...")

    if elements:
        doc.build(elements)
        print(f"Generated TLF report at: {pdf_path}")
    else:
        print("No reports generated.")
