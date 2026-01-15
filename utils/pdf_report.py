from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


def generate_pdf(
    patient_name,
    patient_id,
    patient,
    score,
    risk,
    diseases,
    report_path
):

    # ================= BASIC SETUP =================
    os.makedirs("reports", exist_ok=True)
    styles = getSampleStyleSheet()
    story = []

    # ================= HEADER SECTION =================
    logo_path = "assets/hospital_logo.png"
    logo = Image(logo_path, 1.2 * inch, 1.2 * inch) if os.path.exists(logo_path) else Spacer(1, 1)

    header_text = Paragraph(
        "<b><font size=16 color='#0b5394'>CITY CARE MULTISPECIALITY HOSPITAL</font></b><br/>"
        "<font size=10>Heart Disease Risk Assessment Report</font>",
        ParagraphStyle("header", alignment=0)
    )

    header_table = Table([[logo, header_text]], colWidths=[1.5 * inch, 4.5 * inch])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12)
    ]))

    story.append(header_table)
    story.append(Spacer(1, 12))

    # ================= DATE SECTION =================
    story.append(Paragraph(
        f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 12))

    # ================= PATIENT INFORMATION =================
    story.append(Paragraph("<b>Patient Information</b>", styles["Heading4"]))

    patient_table = [
        ["Patient Name", patient_name],
        ["Patient ID", patient_id],
        ["Age", patient.get("age", "-")],
        ["Gender", patient.get("Gender", "-")],
        ["Chest Pain (cp)", patient.get("cp", "-")],
        ["Resting BP", patient.get("trestbps", "-")],
        ["Cholesterol", patient.get("chol", "-")],
        ["Fasting Blood Sugar", patient.get("fbs", "-")],
        ["Rest ECG", patient.get("restecg", "-")],
        ["Max Heart Rate", patient.get("thalach", "-")],
        ["Exercise Angina", patient.get("exang", "-")],
        ["Oldpeak", patient.get("oldpeak", "-")],
        ["Slope", patient.get("slope", "-")],
        ["Major Vessels (ca)", patient.get("ca", "-")],
        ["Thal", patient.get("thal", "-")]
    ]

    table = Table(patient_table, colWidths=[3 * inch, 3 * inch])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold")
    ]))

    story.append(table)
    story.append(Spacer(1, 15))

    # ================= RISK SUMMARY =================
    story.append(Paragraph("<b>Risk Summary</b>", styles["Heading4"]))

    risk_color = "red" if "HIGH" in risk else "orange" if "MEDIUM" in risk else "green"

    story.append(Paragraph(
        # f"<b>Total Risk Score:</b> {score}<br/>"
        f"<b>Final Risk Level:</b> "
        f"<font color='{risk_color}'><b>{risk}</b></font>",
        styles["Normal"]
    ))
    story.append(Spacer(1, 15))

    # ================= DISEASE ANALYSIS =================
    story.append(Paragraph("<b>Possible Associated Diseases</b>", styles["Heading3"]))

    if diseases:
        for d in diseases:
            story.append(Paragraph(f"- {d}", styles["Normal"]))
    else:
        story.append(Paragraph("No significant disease pattern detected.", styles["Normal"]))

    story.append(Spacer(1, 18))

    # # ================= CLINICAL PARAMETERS GRAPH =================
    # param_order = [
    #     "sex", "cp", "trestbps", "chol",
    #     "fbs", "restecg", "thalach", "exang",
    #     "oldpeak", "slope", "ca", "thal"
    # ]

    # labels = [p.upper() for p in param_order]
    # values = [patient.get(p, 0) for p in param_order]

    # plt.figure(figsize=(8, 4))
    # plt.bar(labels, values, color="#0b5394")
    # plt.ylabel("Patient Value")
    # plt.xlabel("Clinical Parameters")
    # plt.title("Patient Clinical Parameters Overview")
    # plt.xticks(rotation=45, ha="right")
    # plt.grid(axis="y", linestyle="--", alpha=0.4)
    # plt.tight_layout()

    # graph_path = "reports/patient_all_features_graph.png"
    # plt.savefig(graph_path, dpi=200)
    # plt.close()

    # story.append(Paragraph("<b>Clinical Parameters Analysis</b>", styles["Heading3"]))
    # story.append(Image(graph_path, width=6.5 * inch, height=3.8 * inch))
    # story.append(Spacer(1, 20))



    # ================= GRAPH (PATIENT vs NORMAL) =================
    labels = []
    patient_vals = []
    normal_vals = []

    GRAPH_PARAMS = {
        # "age":        {"normal": 45,  "label": "Age"},
        "trestbps":   {"normal": 120, "label": "Resting BP"},
        "chol":       {"normal": 200, "label": "Cholesterol"},
        "thalach":    {"normal": 150, "label": "Max HR"},
        "oldpeak":    {"normal": 1.0, "label": "ST Depression"},
        "ca":         {"normal": 0,   "label": "Major Vessels"}
    }

    for p, meta in GRAPH_PARAMS.items():
        labels.append(meta["label"])
        patient_vals.append(patient[p])
        normal_vals.append(meta["normal"])

    x = range(len(labels))
    width = 0.35

    plt.figure(figsize=(6, 3.5))
    plt.bar(x, normal_vals, width, label="Normal", color="#b0b0b0")
    plt.bar([i + width for i in x], patient_vals, width,
            label="Patient", color="#d9534f")

    plt.xticks([i + width / 2 for i in x], labels, rotation=30)
    plt.ylabel("Value")
    plt.title("Patient vs Normal Clinical Values")
    plt.legend()
    plt.tight_layout()

    graph_path = "reports/patient_vs_normal.png"
    plt.savefig(graph_path, dpi=200)
    plt.close()

    story.append(Paragraph("<b>Patient vs Normal Parameter Comparison</b>", styles["Heading3"]))
    story.append(Image(graph_path, width=5.5 * inch, height=3.5 * inch))
    story.append(Spacer(1, 12))


    comparison_table = [["Parameter", "Normal", "Patient", "Status"]]

    for p, meta in GRAPH_PARAMS.items():
        val = patient[p]
        normal = meta["normal"]

        if val < normal:
            status = "Low"
        elif val > normal:
            status = "High"
        else:
            status = "Normal"

        comparison_table.append([
            meta["label"],
            normal,
            val,
            status
        ])

    t = Table(comparison_table, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1.1*inch])
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.whitesmoke),
        ("FONT", (0,0), (-1,0), "Helvetica-Bold")
    ]))

    story.append(t)

    # ================= SIGNATURE SECTION =================
    story.append(Spacer(1, 25))
    story.append(Paragraph("Doctor Signature: ____________________________", styles["Normal"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Hospital Stamp: ____________________________", styles["Normal"]))

    # ================= FOOTER NOTE =================
    story.append(Spacer(1, 18))
    story.append(Paragraph(
        "<font size=8><i>"
        "Note: This report is rule-based and intended for Machine Learning."
        "</i></font>",
        styles["Normal"]
    ))

    # ================= PAGE BORDER =================
    def add_border(canvas, doc):
        canvas.setStrokeColor(colors.black)
        canvas.rect(20, 20, A4[0] - 40, A4[1] - 40)

    # ================= BUILD PDF =================
    pdf = SimpleDocTemplate(
        report_path,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=40,
        bottomMargin=30
    )

    pdf.build(story, onFirstPage=add_border, onLaterPages=add_border)

    if os.path.exists(graph_path):
        os.remove(graph_path)
