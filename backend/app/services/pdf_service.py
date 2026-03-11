from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(results):

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Informe de Modelación", styles['Title']))
    elements.append(Spacer(1,20))

    for r in results:

        elements.append(Paragraph(f"Algoritmo: {r['name']}", styles['Heading2']))
        elements.append(Paragraph(f"Formula: {r['formula']}", styles['Normal']))

        elements.append(Paragraph(f"MAE: {r['mae']}", styles['Normal']))
        elements.append(Paragraph(f"MSE: {r['mse']}", styles['Normal']))
        elements.append(Paragraph(f"RMSE: {r['rmse']}", styles['Normal']))
        elements.append(Paragraph(f"R2: {r['r2']}", styles['Normal']))

        elements.append(Image(r["plot"], width=400, height=300))
        elements.append(Spacer(1,40))

    pdf = SimpleDocTemplate("report.pdf")
    pdf.build(elements)