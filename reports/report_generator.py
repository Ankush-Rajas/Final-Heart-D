from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime


def generate_pdf(patient_name, patient_id, patient, score, risk, diseases, report_path):

    c = canvas.Canvas(report_path, pagesize=A4)
    width, height = A4
    y = height - 50

    # ---------- TITLE ----------
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y, "Heart Disease Risk Assessment Report")
    y -= 30

    c.setStrokeColor(colors.black)
    c.line(40, y, width - 40, y)
    y -= 20

    # ---------- DATE ----------
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    y -= 25

    # ---------- PATIENT INFO ----------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Patient Information")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(60, y, f"Patient Name : {patient_name}")
    y -= 15
    c.drawString(60, y, f"Patient ID   : {patient_id}")
    y -= 25

    # ---------- PARAMETERS ----------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Clinical Parameters")
    y -= 20

    c.setFont("Helvetica", 10)
    for k, v in patient.items():
        if y < 60:        # page overflow protection
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

        c.drawString(60, y, f"{k.upper()} : {v}")
        y -= 15

    # ---------- RISK RESULT ----------
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Risk Result")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(60, y, f"Total Risk Score : {score}")
    y -= 15
    c.drawString(60, y, f"Final Risk Level : {risk}")
    y -= 25

    # ---------- DISEASES ----------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Possible Associated Diseases")
    y -= 20

    c.setFont("Helvetica", 10)
    if diseases:
        for d in diseases:
            if y < 60:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)

            c.drawString(60, y, f"- {d}")
            y -= 15
    else:
        c.drawString(60, y, "No major disease pattern detected.")
        y -= 15

    # ---------- FOOTER ----------
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(
        50,
        40,
        "Note: This report is rule-based and intended for clinical decision support only."
    )

    c.save()
