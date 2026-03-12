from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt

from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def _build_chart_image(result):
    chart_stream = BytesIO()

    time_points = result["results"]["time_points"]
    real_values = result["results"]["real_values"]
    predicted_values = result["results"]["predicted_values"]

    plt.figure(figsize=(6.4, 2.6))
    plt.plot(time_points, real_values, label="Real", linewidth=1.5)
    plt.plot(time_points, predicted_values, label="Predicho", linewidth=1.5)
    plt.title(f"Comparacion - {result['algorithm']}")
    plt.xlabel("Tiempo")
    plt.ylabel("FC")
    plt.legend(loc="best")
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(chart_stream, format="png", dpi=140)
    plt.close()

    chart_stream.seek(0)
    return chart_stream


def generate_pdf(results, filename: str, activity: str):
    pdf_stream = BytesIO()
    pdf = SimpleDocTemplate(pdf_stream)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Informe de Modelacion", styles["Title"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Dataset: {filename}", styles["Normal"]))
    elements.append(Paragraph(f"Actividad: {activity}", styles["Normal"]))
    elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    elements.append(Spacer(1, 18))

    for r in results:
        algorithm_label = r["algorithm"]
        if r.get("degree"):
            algorithm_label = f"{algorithm_label} (grado {r['degree']})"

        elements.append(Paragraph(f"Algoritmo: {algorithm_label}", styles["Heading2"]))

        equation = r.get("equation")
        if equation:
            elements.append(Paragraph(f"Ecuacion: {equation}", styles["Normal"]))
        else:
            elements.append(Paragraph("Ecuacion: No disponible para este modelo", styles["Normal"]))

        metrics = r["metrics"]
        metrics_table = Table(
            [
                ["Metrica", "Valor"],
                ["MAE", f"{metrics['mae']:.4f}"],
                ["MSE", f"{metrics['mse']:.4f}"],
                ["RMSE", f"{metrics['rmse']:.4f}"],
                ["R2", f"{metrics['r2_score']:.4f}"],
                ["Tiempo entrenamiento (s)", f"{r['training_time']:.4f}"]
            ],
            colWidths=[180, 220]
        )

        metrics_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (1, 1), (1, -1), "RIGHT")
        ]))

        elements.append(Spacer(1, 6))
        elements.append(metrics_table)
        elements.append(Spacer(1, 10))

        chart_stream = _build_chart_image(r)
        elements.append(Image(chart_stream, width=430, height=180))
        elements.append(Spacer(1, 20))

    pdf.build(elements)
    pdf_stream.seek(0)
    return pdf_stream