# from reportlab.platypus import (
#     SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
# )
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import inch
# from reportlab.lib import colors
# from datetime import datetime
# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt
# import os


# def generate_pdf(patient_name, patient_id, patient, score, risk, diseases, report_path):

#     os.makedirs("reports", exist_ok=True)
#     styles = getSampleStyleSheet()
#     story = []

#     # ================= STYLES =================
#     title_style = ParagraphStyle(
#         "Title",
#         fontName="Helvetica-Bold",
#         fontSize=20,
#         alignment=1,
#         textColor=colors.HexColor("#0b5394"),
#         underline=True,
#         spaceAfter=20
#     )

#     subtitle_style = ParagraphStyle(
#         "SubTitle",
#         fontName="Helvetica",
#         fontSize=14,
#         alignment=1,
#         textColor=colors.HexColor("#333333"),
#         spaceAfter=25
#     )

#     section_style = ParagraphStyle(
#         "Section",
#         fontName="Helvetica-Bold",
#         fontSize=16,
#         textColor=colors.HexColor("#0b5394"),
#         underline=True,
#         spaceBefore=14,
#         spaceAfter=20
#     )

#     normal_style = ParagraphStyle(
#         "NormalText",
#         fontName="Helvetica",
#         fontSize=12,
#         leading=14,
#         textColor=colors.black
#     )

#     small_style = ParagraphStyle(
#         "SmallText",
#         fontName="Helvetica",
#         fontSize=8,
#         textColor=colors.grey
#     )

#     # ================= HEADER =================
#     story.append(Paragraph("CITY CARE MULTISPECIALITY HOSPITAL", title_style))
#     "<br/>"
#     story.append(Paragraph("Heart Disease Risk Assessment Report", subtitle_style))

#     current_dt = datetime.now()

#     story.append(Paragraph(
#         f"<b>Report Date:</b> {current_dt.strftime('%d-%m-%Y')}",
#         normal_style
#     ))
#     story.append(Spacer(1, 6))

#     story.append(Paragraph(
#         f"<b>Report Time:</b> {current_dt.strftime('%I:%M %p')}",
#         normal_style
#     ))
#     story.append(Spacer(1, 10))


#     # ================= PATIENT INFORMATION =================
#     story.append(Paragraph("Patient Information", section_style))

#     patient_table = [
#         ["Patient Name", patient_name],
#         ["Patient ID", patient_id],
#         ["Age", patient["age"]],
#         ["Gender", "Male" if patient["Gender"] == 1 else "Female"],
#         ["Resting BP (mm Hg)", patient["trestbps"]],
#         ["Cholesterol (mg/dl)", patient["chol"]],
#         ["Max Heart Rate", patient["thalach"]],
#         ["Exercise Angina", "Yes" if patient["exang"] else "No"],
#         ["Oldpeak", patient["oldpeak"]],
#         ["Major Vessels (ca)", patient["ca"]],
#         ["Thalassemia", patient["thal"]],
#     ]

#     table = Table(patient_table, colWidths=[3 * inch, 3 * inch])
#     table.setStyle(TableStyle([
#         ("GRID", (0,0), (-1,-1), 0.7, colors.black),
#         ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e9f0fa")),
#         ("FONT", (0,0), (-1,0), "Helvetica-Bold"),
#         ("FONT", (0,1), (-1,-1), "Helvetica"),
#         ("LEFTPADDING", (0,0), (-1,-1), 6),
#         ("RIGHTPADDING", (0,0), (-1,-1), 6),
#         ("TOPPADDING", (0,0), (-1,-1), 5),
#         ("BOTTOMPADDING", (0,0), (-1,-1), 5),
#     ]))
#     story.append(table)
#     story.append(Spacer(1, 14))

#     # ================= RISK SUMMARY =================
#     story.append(Paragraph("Risk Summary", section_style))

#     risk_color = (
#         "red" if "HIGH" in risk or "CRITICAL" in risk
#         else "orange" if "MODERATE" in risk or "MILD" in risk
#         else "green"
#     )

#     story.append(Paragraph(
#         f"<b>Final Risk Level:</b> "
#         f"<font color='{risk_color}' size='12'><b>{risk}</b></font>",
#         normal_style
#     ))
#     story.append(Spacer(1, 12))

#     # ================= DISEASE LIST =================
#     story.append(Paragraph("Possible Associated Diseases", section_style))
#     if diseases:
#         for d in diseases:
#             story.append(Paragraph(f"• {d}", normal_style))
#     else:
#         story.append(Paragraph("No significant disease detected.", normal_style))

#     story.append(Spacer(1, 14))

#     # ================= GRAPH =================
#     GRAPH_PARAMS = {
#     "trestbps": {"normal": 120, "label": "Resting BP (mmHg)"},
#     "chol": {"normal": 200, "label": "Cholesterol (mg/dl)"},
#     "thalach": {"normal": 150, "label": "Max Heart Rate"},
#     "oldpeak": {"normal": 1.0, "label": "ST Depression"},
#     "ca": {"normal": 0, "label": "Major Vessels"}
#     }

#     labels, patient_vals, normal_vals = [], [], []

#     for p, meta in GRAPH_PARAMS.items():
#         labels.append(meta["label"])
#         patient_vals.append(patient[p])
#         normal_vals.append(meta["normal"])

#     x = range(len(labels))
#     width = 0.35

#     plt.figure(figsize=(7, 3.8))

#     # Bars
#     normal_bar = plt.bar(
#         x,
#         normal_vals,
#         width,
#         label="Normal Range",
#         color="#cfd8dc"
#     )

#     patient_bar = plt.bar(
#         [i + width for i in x],
#         patient_vals,
#         width,
#         label="Patient Value",
#         color="#ef5350"
#     )

#     # X-axis
#     plt.xticks(
#         [i + width / 2 for i in x],
#         labels,
#         rotation=20,
#         fontsize=9
#     )

#     # Labels & Title
#     plt.ylabel("Clinical Value", fontsize=10)
#     plt.title(
#         "Patient vs Normal Clinical Parameters",
#         fontsize=12,
#         fontweight="bold"
#     )

#     # Grid
#     plt.grid(
#         axis="y",
#         linestyle="--",
#         linewidth=0.6,
#         alpha=0.6
#     )

#     # Legend
#     plt.legend(fontsize=9, frameon=False)

#     # -------- VALUE LABELS (IMPORTANT) --------
#     for bars in [normal_bar, patient_bar]:
#         for bar in bars:
#             height = bar.get_height()
#             plt.text(
#                 bar.get_x() + bar.get_width() / 2,
#                 height,
#                 f"{height}",
#                 ha="center",
#                 va="bottom",
#                 fontsize=8
#             )

#     plt.tight_layout()

#     graph_path = "reports/clinical_comparison.png"
#     plt.savefig(graph_path, dpi=300, bbox_inches="tight")
#     plt.close()

#     # Add to PDF
#     story.append(Paragraph("Clinical Parameter Comparison", section_style))
#     story.append(Image(graph_path, width=6.2 * inch, height=3.6 * inch))
#     story.append(Spacer(1, 14))


#     # ================= MAJOR HEART DISEASE INFORMATION =================
#     story.append(Spacer(4, 14))
#     story.append(Paragraph("Major Heart Disease Information", section_style))

#     story.append(Paragraph(
#         "<b>Coronary Artery Disease (CAD):</b><br/>"
#         "This condition occurs when the coronary arteries supplying blood to the heart become "
#         "narrowed or blocked due to cholesterol and plaque buildup. It reduces oxygen supply to "
#         "the heart muscle and may lead to chest pain (angina) or heart attack. "
#         "Risk factors include high cholesterol, high blood pressure, smoking, diabetes, and obesity.",
#         normal_style
#     ))

#     story.append(Spacer(1, 8))

#     story.append(Paragraph(
#         "<b>Myocardial Ischemia:</b><br/>"
#         "Myocardial ischemia happens when blood flow to the heart muscle is partially reduced. "
#         "This limits oxygen delivery and weakens heart function. It commonly occurs during physical "
#         "activity or stress and increases the risk of heart attack if untreated.",
#         normal_style
#     ))

#     story.append(Spacer(1, 8))

#     story.append(Paragraph(
#         "<b>Hypertension Related Heart Disease:</b><br/>"
#         "Long-standing high blood pressure forces the heart to work harder than normal. "
#         "Over time, this causes thickening of heart muscles, reduced efficiency, and increases "
#         "the risk of heart failure, stroke, and coronary artery disease.",
#         normal_style
#     ))

#     story.append(Spacer(1, 8))

#     story.append(Paragraph(
#         "<b>Hypercholesterolemia:</b><br/>"
#         "High cholesterol levels result in fat deposition inside blood vessels, leading to "
#         "artery narrowing and blockage. This condition significantly increases the likelihood "
#         "of coronary artery disease and heart attack if not controlled through diet, exercise, "
#         "and medical treatment.",
#         normal_style
#     ))

#     story.append(Spacer(1, 8))

#     story.append(Paragraph(
#         "<b>Exercise-Induced Angina:</b><br/>"
#         "This condition occurs when the heart muscle does not receive adequate oxygen during "
#         "physical activity. It is usually a sign of underlying coronary artery disease and "
#         "should be evaluated by a cardiologist.",
#         normal_style
#     ))

#     story.append(Spacer(1, 10))

#     story.append(Paragraph(
#         "<b>General Preventive Measures:</b><br/>"
#         "• Maintain a heart-healthy diet low in salt and fat.<br/>"
#         "• Engage in regular physical activity.<br/>"
#         "• Control blood pressure, cholesterol, and blood sugar levels.<br/>"
#         "• Avoid smoking and limit alcohol intake.<br/>"
#         "• Undergo routine cardiac evaluations as advised by a physician.",
#         normal_style
#     ))


#     # ================= MEDICAL EXPLANATION & ADVICE =================
#     story.append(Paragraph("Medical Explanation & Advice", section_style))
#     story.append(Paragraph(
#         "Heart disease occurs when blood supply to the heart muscle is reduced due to "
#         "blockage or narrowing of coronary arteries. High blood pressure, high cholesterol, "
#         "and abnormal heart parameters increase strain on the heart and reduce oxygen supply.",
#         normal_style
#     ))

#     story.append(Spacer(1, 8))
#     story.append(Paragraph("<b>What NOT to do:</b>", normal_style))
#     story.append(Paragraph(
#         "• Avoid smoking and alcohol.<br/>"
#         "• Avoid fried, salty, and processed food.<br/>"
#         "• Avoid stress and irregular sleep.<br/>"
#         "• Avoid self-medication.",
#         normal_style
#     ))

#     story.append(Spacer(1, 8))
#     story.append(Paragraph("<b>What to do:</b>", normal_style))
#     story.append(Paragraph(
#         "• Walk at least 30 minutes daily.<br/>"
#         "• Eat fruits, vegetables, and whole grains.<br/>"
#         "• Maintain healthy body weight.<br/>"
#         "• Follow regular medical check-ups.",
#         normal_style
#     ))

#     story.append(Spacer(1, 10))
    
#     story.append(Paragraph("Doctor Signature: ____________________________", styles["Normal"]))
#     story.append(Spacer(1, 10))
#     story.append(Paragraph("Hospital Stamp: ____________________________", styles["Normal"]))
#     story.append(Spacer(1, 10))
#     # ================= PAGE DECORATION =================
#     def decorate_page(canvas, doc):
#         # Border
#         canvas.setStrokeColor(colors.HexColor("#666666"))
#         canvas.rect(20, 20, A4[0] - 40, A4[1] - 40)

#         # Heart Image Watermark
#         watermark = "assets/heart_watermark.png"
#         if os.path.exists(watermark):
#             canvas.saveState()
#             canvas.setFillAlpha(0.08)
#             canvas.drawImage(
#                 watermark,
#                 A4[0]/2 - 200,
#                 A4[1]/2 - 200,
#                 width=400,
#                 height=400,
#                 mask="auto"
#             )
#             canvas.restoreState()

#         # Header
#         canvas.setFont("Helvetica-Bold", 9)
#         canvas.drawString(30, A4[1] - 30, "City Care Multispeciality Hospital")

#         # Footer
#         canvas.setFont("Helvetica", 9)
#         canvas.drawString(
#             30, 25,
#             "Address: MG Road, Indore | Phone: +91-9876543210 | Email: care@citycare.com"
#         )
#         canvas.drawRightString(A4[0] - 30, 25, f"Page {doc.page}")

#     pdf = SimpleDocTemplate(
#         report_path,
#         pagesize=A4,
#         rightMargin=30,
#         leftMargin=30,
#         topMargin=60,
#         bottomMargin=40
#     )

#     pdf.build(story, onFirstPage=decorate_page, onLaterPages=decorate_page)

#     if os.path.exists(graph_path):
#         os.remove(graph_path)





from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


def generate_pdf(patient_name, patient_id, patient, score, risk, diseases, report_path):

    os.makedirs("reports", exist_ok=True)
    styles = getSampleStyleSheet()
    story = []

    # ================= STYLES =================
    title_style = ParagraphStyle(
        "Title",
        fontName="Helvetica-Bold",
        fontSize=20,
        alignment=1,
        textColor=colors.HexColor("#0b5394"),
        underline=True,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        "SubTitle",
        fontName="Helvetica",
        fontSize=14,
        alignment=1,
        textColor=colors.HexColor("#333333"),
        spaceAfter=20
    )

    section_style = ParagraphStyle(
        "Section",
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=colors.HexColor("#0b5394"),
        underline=True,
        spaceBefore=14,
        spaceAfter=14
    )

    normal_style = ParagraphStyle(
        "NormalText",
        fontName="Helvetica",
        fontSize=12,
        leading=15
    )

    small_style = ParagraphStyle(
        "SmallText",
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.grey
    )

    # ================= HEADER =================
    story.append(Paragraph("CITY CARE MULTISPECIALITY HOSPITAL", title_style))
    story.append(Paragraph("Heart Disease Risk Assessment Report", subtitle_style))

    current_dt = datetime.now()
    story.append(Paragraph(f"<b>Report Date:</b> {current_dt.strftime('%d-%m-%Y')}", normal_style))
    story.append(Paragraph(f"<b>Report Time:</b> {current_dt.strftime('%I:%M %p')}", normal_style))
    story.append(Spacer(1, 12))

    # ================= PATIENT INFORMATION =================
    story.append(Paragraph("Patient Information", section_style))

    patient_table = [
        ["Patient Name", patient_name],
        ["Patient ID", patient_id],
        ["Age", patient["age"]],
        ["Gender", "Male" if patient["Gender"] == 1 else "Female"],
        ["Resting BP (mm Hg)", patient["trestbps"]],
        ["Cholesterol (mg/dl)", patient["chol"]],
        ["Max Heart Rate", patient["thalach"]],
        ["Exercise Angina", "Yes" if patient["exang"] else "No"],
        ["Oldpeak", patient["oldpeak"]],
        ["Major Vessels (ca)", patient["ca"]],
        ["Thalassemia", patient["thal"]],
    ]

    table = Table(patient_table, colWidths=[3 * inch, 3 * inch])
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.7, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e9f0fa")),
        ("FONT", (0,0), (-1,0), "Helvetica-Bold"),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 16))

    # ================= RISK SUMMARY =================
    story.append(Paragraph("Risk Summary", section_style))

    risk_color = (
        "red" if "HIGH" in risk or "CRITICAL" in risk
        else "orange" if "MODERATE" in risk or "MILD" in risk
        else "green"
    )

    story.append(Paragraph(
        f"<b>Final Risk Level:</b> <font color='{risk_color}'><b>{risk}</b></font>",
        normal_style
    ))
    story.append(Spacer(1, 12))

    # ================= DISEASE LIST =================
    story.append(Paragraph("Possible Associated Diseases", section_style))
    if diseases:
        for d in diseases:
            story.append(Paragraph(f"• {d}", normal_style))
            story.append(Spacer(1, 4))
    else:
        story.append(Paragraph("No significant disease detected.", normal_style))

    story.append(Spacer(1, 16))

    # ================= GRAPH =================
    GRAPH_PARAMS = {
        "trestbps": {"normal": 120, "label": "Resting BP (mmHg)"},
        "chol": {"normal": 200, "label": "Cholesterol (mg/dl)"},
        "thalach": {"normal": 150, "label": "Max Heart Rate"},
        "oldpeak": {"normal": 1.0, "label": "ST Depression"},
        "ca": {"normal": 0, "label": "Major Vessels"}
    }

    labels, patient_vals, normal_vals = [], [], []
    for p, meta in GRAPH_PARAMS.items():
        labels.append(meta["label"])
        patient_vals.append(patient[p])
        normal_vals.append(meta["normal"])

    x = range(len(labels))
    width = 0.35

    plt.figure(figsize=(7, 4))
    normal_bar = plt.bar(x, normal_vals, width, label="Normal", color="#cfd8dc")
    patient_bar = plt.bar([i + width for i in x], patient_vals, width, label="Patient", color="#ef5350")

    plt.xticks([i + width/2 for i in x], labels, rotation=30, fontsize=9)
    plt.ylabel("Clinical Value")
    plt.title("Patient vs Normal Clinical Parameters", fontsize=12, fontweight="bold")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.legend(frameon=False)

    for bars in [normal_bar, patient_bar]:
        for bar in bars:
            h = bar.get_height()
            plt.text(bar.get_x()+bar.get_width()/2, h, f"{h}", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    graph_path = "reports/clinical_comparison.png"
    plt.savefig(graph_path, dpi=300)
    plt.close()

    story.append(Paragraph("Clinical Parameter Comparison", section_style))
    story.append(Image(graph_path, width=6.3 * inch, height=3.8 * inch))
    story.append(Spacer(1, 18))

    # ================= MEDICAL ADVICE =================
    story.append(Paragraph("Medical Explanation & Advice", section_style))
    story.append(Paragraph(
        "Heart disease develops when blood flow to the heart muscle is reduced due to blockage "
        "or narrowing of coronary arteries. Timely lifestyle changes and medical supervision "
        "can significantly reduce future complications.",
        normal_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>What NOT to do:</b>", normal_style))
    story.append(Paragraph(
        "• Avoid smoking and alcohol<br/>"
        "• Avoid fried and salty food<br/>"
        "• Avoid stress and irregular sleep<br/>"
        "• Avoid self-medication",
        normal_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>What to do:</b>", normal_style))
    story.append(Paragraph(
        "• Walk at least 30 minutes daily<br/>"
        "• Eat fruits, vegetables, whole grains<br/>"
        "• Maintain healthy body weight<br/>"
        "• Follow regular medical check-ups",
        normal_style
    ))

    story.append(Spacer(1, 16))
    story.append(Paragraph("Doctor Signature: ____________________________", normal_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Hospital Stamp: ____________________________", normal_style))

    # ================= PAGE DECORATION =================
    def decorate_page(canvas, doc):
        canvas.setStrokeColor(colors.HexColor("#666666"))
        canvas.rect(20, 20, A4[0]-40, A4[1]-40)

        watermark = "assets/heart_watermark.png"
        if os.path.exists(watermark):
            canvas.saveState()
            canvas.setFillAlpha(0.08)
            canvas.drawImage(watermark, A4[0]/2-200, A4[1]/2-200, 400, 400, mask="auto")
            canvas.restoreState()

        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(30, A4[1]-30, "City Care Multispeciality Hospital")
        canvas.setFont("Helvetica", 9)
        canvas.drawString(30, 25, "Address: MG Road, Indore | Phone: +91-9876543210 | Email: care@citycare.com")
        canvas.drawRightString(A4[0]-30, 25, f"Page {doc.page}")

    pdf = SimpleDocTemplate(
        report_path,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=60,
        bottomMargin=40
    )

    pdf.build(story, onFirstPage=decorate_page, onLaterPages=decorate_page)

    if os.path.exists(graph_path):
        os.remove(graph_path)
