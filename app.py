# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from utils.save_report import save_report_to_db
# from logic.risk_engine import evaluate
# from utils.pdf_report import generate_pdf


# # ================= NORMAL REFERENCE VALUES =================
# GRAPH_PARAMS = {
#     "trestbps": {"normal": 120, "label": "Resting BP"},
#     "chol": {"normal": 200, "label": "Cholesterol"},
#     "thalach": {"normal": 150, "label": "Max Heart Rate"},
#     "oldpeak": {"normal": 1.0, "label": "ST Depression"},
#     "ca": {"normal": 0, "label": "Major Vessels"}
# }


# # ================= SESSION STATE =================
# if "result" not in st.session_state:
#     st.session_state.result = None

# if "last_input" not in st.session_state:
#     st.session_state.last_input = None


# st.set_page_config(page_title="Heart Risk Dashboard", layout="wide")


# # ================= UI STYLE =================
# st.markdown("""
# <style>
# body { background-color:#f5f7fb; }
# </style>
# """, unsafe_allow_html=True)

# st.title("🫀 Heart Disease Risk Assessment Dashboard")


# def load_lottie(path):
#     with open(path, "r") as f:
#         return json.load(f)

# # ================= INPUT PANEL =================
# with st.sidebar:
#     st.header("🧑 Patient Details")
#     patient_name = st.text_input("Patient Name", "John Doe")
#     patient_id = st.text_input("Patient ID", "PID-001")

#     st.divider()
#     st.header("🩺 Clinical Parameters")

#     patient = {
#     "age": st.number_input("Age (years)", 1, 120, 55),

#     "Gender": st.selectbox("Gender", [0, 1], format_func=lambda x: "Male" if x else "Female"),

#     "cp": st.selectbox(
#         "Chest Pain Type",
#         [0, 1, 2, 3],
#         format_func=lambda x: [
#             "Typical Angina",
#             "Atypical Angina",
#             "Non-anginal Pain",
#             "Asymptomatic"
#         ][x]
#     ),

#     "chol": st.number_input("Cholesterol (mg/dl)", 100, 500, 240),

#     "trestbps": st.number_input("Resting BP (mm Hg)", 80, 250, 140),
#     "thalach": st.number_input("Max Heart Rate Achieved", 60, 220, 120),

#     "exang": st.selectbox(
#         "Exercise Induced Angina",
#         [0, 1],
#         format_func=lambda x: "Pain during exercise" if x else "No pain"
#     ),

#     "restecg": st.selectbox("Resting ECG", [0, 1, 2]),

#     "oldpeak": st.slider("ST Depression (oldpeak)", 0.0, 10.0, 2.5),

#     "ca": st.selectbox("Major Vessels (ca)", [0, 1, 2, 3, 4]),

#     "thal": st.selectbox(
#         "Thalassemia",
#         [1, 2, 3],
#         format_func=lambda x: {
#             1: "Normal",
#             2: "Fixed Defect",
#             3: "Reversible Defect"
#         }[x]
#     ),
# }

#     # 🔴 INPUT CHANGE DETECTION
#     current_input = tuple(patient.values())
#     if st.session_state.last_input is not None:
#         if current_input != st.session_state.last_input:
#             st.session_state.result = None

#     st.session_state.last_input = current_input

#     predict_btn = st.button("🔍 Predict Risk")


# # ================= PREDICT =================
# if predict_btn:
#     score, risk, diseases, contrib, explanations = evaluate(patient)
#     st.session_state.result = (score, risk, diseases, contrib)


# # ================= RESULT DISPLAY =================
# if st.session_state.result:
#     score, risk, diseases, contrib = st.session_state.result

#     col1, col2 = st.columns([2, 2])

#     # -------- TEXT RESULT --------
#     with col1:
#         st.subheader("🧠 Risk Result")

#         if "HIGH" in risk:
#             st.error(f"Final Risk Level: {risk}")
#         elif "MEDIUM" in risk:
#             st.warning(f"Final Risk Level: {risk}")
#         else:
#             st.success(f"Final Risk Level: {risk}")

#         st.subheader("🦠 Possible Associated Diseases")
#         if diseases:
#             for d in diseases:
#                 st.write("•", d)
#         else:
#             st.write("No significant disease detected")
# st.subheader("🧠 Medical Explanation")

# for exp in explanations:
#     st.write("•", exp)

#     # -------- GRAPH --------
#     with col2:
#         st.subheader("📊 Patient vs Normal Clinical Values")

#         labels, patient_vals, normal_vals = [], [], []

#         for p, meta in GRAPH_PARAMS.items():
#             labels.append(meta["label"])
#             patient_vals.append(patient[p])
#             normal_vals.append(meta["normal"])

#         x = range(len(labels))
#         width = 0.35

#         fig, ax = plt.subplots(figsize=(7,4))
#         ax.bar(x, normal_vals, width, label="Normal", color="#b0b0b0")
#         ax.bar([i+width for i in x], patient_vals, width,
#                label="Patient", color="#d9534f")

#         ax.set_xticks([i + width/2 for i in x])
#         ax.set_xticklabels(labels, rotation=30)
#         ax.set_ylabel("Value")
#         ax.set_title("Patient vs Normal Comparison")
#         ax.legend()
#         ax.grid(axis="y", linestyle="--", alpha=0.4)

#         st.pyplot(fig)

#     # -------- COMPARISON TABLE --------
#     st.subheader("📋 Parameter Comparison Table")

#     table_data = []
#     for p, meta in GRAPH_PARAMS.items():
#         val = patient[p]
#         normal = meta["normal"]

#         if val < normal:
#             status = "⬇ Low"
#         elif val > normal:
#             status = "⬆ High"
#         else:
#             status = "✅ Normal"

#         table_data.append([meta["label"], normal, val, status])

#     df_compare = pd.DataFrame(
#         table_data,
#         columns=["Parameter", "Normal Value", "Patient Value", "Status"]
#     )

#     st.dataframe(df_compare, use_container_width=True)


# # ================= PDF DOWNLOAD =================
# if st.session_state.result:
#     report_path = "reports/heart_risk_report.pdf"
#     os.makedirs("reports", exist_ok=True)

#     if st.button("📄 Generate & Download Report"):
#         generate_pdf(
#             patient_name,
#             patient_id,
#             patient,
#             score,
#             risk,
#             diseases,
#             report_path
#         )
#         # 🔥 YAHI PE SAVE KARNA HAI
#         save_report_to_db(
#         patient_id,
#         patient_name,
#         risk,
#         report_path
#         )
#         with open(report_path, "rb") as f:
#             st.download_button(
#                 "⬇ Download Report",
#                 f,
#                 file_name="heart_risk_report.pdf",
#                 mime="application/pdf"
#             )






# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from logic.risk_engine import evaluate
# from utils.pdf_report import generate_pdf
# from utils.save_report import save_report_to_db

# # ================= PAGE CONFIG =================
# st.set_page_config(page_title="Heart Risk Dashboard", layout="wide")

# # ================= NORMAL REFERENCE VALUES =================
# GRAPH_PARAMS = {
#     "trestbps": {"normal": 120, "label": "Resting BP"},
#     "chol": {"normal": 200, "label": "Cholesterol"},
#     "thalach": {"normal": 150, "label": "Max Heart Rate"},
#     "oldpeak": {"normal": 1.0, "label": "ST Depression"},
#     "ca": {"normal": 0, "label": "Major Vessels"}
# }

# # ================= SESSION STATE =================
# if "result" not in st.session_state:
#     st.session_state.result = None

# if "last_input" not in st.session_state:
#     st.session_state.last_input = None

# # ================= UI STYLE =================
# st.markdown("""
# <style>
# body { background-color:#f5f7fb; }
# </style>
# """, unsafe_allow_html=True)

# st.title("🫀 Heart Disease Risk Assessment Dashboard")

# # ================= INPUT PANEL =================
# with st.sidebar:
#     st.header("🧑 Patient Details")
#     patient_name = st.text_input("Patient Name", "John Doe")
#     patient_id = st.text_input("Patient ID", "PID-001")

#     st.divider()
#     st.header("🩺 Clinical Parameters")

#     patient = {
#         "age": st.number_input("Age (years)", 1, 120, 55),
#         "Gender": st.selectbox("Gender", [0, 1], format_func=lambda x: "Male" if x else "Female"),
#         "cp": st.selectbox(
#             "Chest Pain Type",
#             [0, 1, 2, 3],
#             format_func=lambda x: [
#                 "Typical Angina",
#                 "Atypical Angina",
#                 "Non-anginal Pain",
#                 "Asymptomatic"
#             ][x]
#         ),
#         "chol": st.number_input("Cholesterol (mg/dl)", 100, 500, 240),
#         "trestbps": st.number_input("Resting BP (mm Hg)", 80, 250, 140),
#         "thalach": st.number_input("Max Heart Rate Achieved", 60, 220, 120),
#         "exang": st.selectbox(
#             "Exercise Induced Angina",
#             [0, 1],
#             format_func=lambda x: "Pain during exercise" if x else "No pain"
#         ),
#         "restecg": st.selectbox("Resting ECG", [0, 1, 2]),
#         "oldpeak": st.slider("ST Depression (oldpeak)", 0.0, 10.0, 2.5),
#         "ca": st.selectbox("Major Vessels (ca)", [0, 1, 2, 3, 4]),
#         "thal": st.selectbox(
#             "Thalassemia",
#             [1, 2, 3],
#             format_func=lambda x: {
#                 1: "Normal",
#                 2: "Fixed Defect",
#                 3: "Reversible Defect"
#             }[x]
#         ),
#     }

#     # 🔴 Input change detection
#     current_input = tuple(patient.values())
#     if st.session_state.last_input is not None and current_input != st.session_state.last_input:
#         st.session_state.result = None

#     st.session_state.last_input = current_input

#     predict_btn = st.button("🔍 Predict Risk")

# # ================= PREDICT =================
# if predict_btn:
#     score, risk, diseases, contrib, explanations = evaluate(patient)
#     st.session_state.result = (score, risk, diseases, contrib, explanations)

# # ================= RESULT DISPLAY =================
# if st.session_state.result:
#     score, risk, diseases, contrib, explanations = st.session_state.result

#     col1, col2 = st.columns([2, 2])

#     # -------- TEXT RESULT --------
#     with col1:
#         st.subheader("🧠 Risk Result")

#         if "CRITICAL" in risk or "HIGH" in risk:
#             st.error(f"Final Risk Level: {risk}")
#         elif "MODERATE" in risk or "MILD" in risk:
#             st.warning(f"Final Risk Level: {risk}")
#         else:
#             st.success(f"Final Risk Level: {risk}")

#         st.subheader("🦠 Possible Associated Diseases")
#         if diseases:
#             for d in diseases:
#                 st.write("•", d)
#         else:
#             st.success("No disease detected. All parameters are normal.")

#         st.subheader("🧠 Medical Explanation (Why this risk?)")
#         for exp in explanations:
#             st.write("•", exp)

#     # -------- GRAPH --------
#     with col2:
#         st.subheader("📊 Patient vs Normal Clinical Values")

#         labels, patient_vals, normal_vals = [], [], []

#         for p, meta in GRAPH_PARAMS.items():
#             labels.append(meta["label"])
#             patient_vals.append(patient[p])
#             normal_vals.append(meta["normal"])

#         x = range(len(labels))
#         width = 0.35

#         fig, ax = plt.subplots(figsize=(7, 4))
#         ax.bar(x, normal_vals, width, label="Normal", color="#b0b0b0")
#         ax.bar([i + width for i in x], patient_vals, width, label="Patient", color="#d9534f")

#         ax.set_xticks([i + width / 2 for i in x])
#         ax.set_xticklabels(labels, rotation=30)
#         ax.set_ylabel("Value")
#         ax.set_title("Patient vs Normal Comparison")
#         ax.legend()
#         ax.grid(axis="y", linestyle="--", alpha=0.4)

#         st.pyplot(fig)

#     # -------- COMPARISON TABLE --------
#     st.subheader("📋 Parameter Comparison Table")

#     table_data = []
#     for p, meta in GRAPH_PARAMS.items():
#         val = patient[p]
#         normal = meta["normal"]

#         if val < normal:
#             status = "⬇ Low"
#         elif val > normal:
#             status = "⬆ High"
#         else:
#             status = "✅ Normal"

#         table_data.append([meta["label"], normal, val, status])

#     df_compare = pd.DataFrame(
#         table_data,
#         columns=["Parameter", "Normal Value", "Patient Value", "Status"]
#     )

#     st.dataframe(df_compare, width="stretch")

# # ================= PDF DOWNLOAD =================
# if st.session_state.result:
#     report_path = "reports/heart_risk_report.pdf"
#     os.makedirs("reports", exist_ok=True)

#     if st.button("📄 Generate & Download Report"):
#         generate_pdf(
#             patient_name,
#             patient_id,
#             patient,
#             score,
#             risk,
#             diseases,
#             report_path
#         )
#         save_report_to_db(patient_id, patient_name, risk, report_path)

#         with open(report_path, "rb") as f:
#             st.download_button(
#                 "⬇ Download Report",
#                 f,
#                 file_name="heart_risk_report.pdf",
#                 mime="application/pdf"
#             )




import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from logic.risk_engine import evaluate
from utils.pdf_report import generate_pdf
from utils.save_report import save_report_to_db


# ================= PAGE CONFIG =================
st.set_page_config(page_title="Heart Risk Dashboard", layout="wide")


# ================= NORMAL REFERENCE VALUES =================
GRAPH_PARAMS = {
    "trestbps": {"normal": 120, "label": "Resting BP"},
    "chol": {"normal": 200, "label": "Cholesterol"},
    "thalach": {"normal": 150, "label": "Max Heart Rate"},
    "oldpeak": {"normal": 1.0, "label": "ST Depression"},
    "ca": {"normal": 0, "label": "Major Vessels"}
}


# ================= SESSION STATE =================
if "result" not in st.session_state:
    st.session_state.result = None

if "last_input" not in st.session_state:
    st.session_state.last_input = None


# ================= UI STYLE =================
st.markdown("""
<style>
body { background-color:#f5f7fb; }
</style>
""", unsafe_allow_html=True)

st.title("🫀 Heart Disease Risk Assessment Dashboard")
st.caption("🧑‍⚕️ Doctor-assisted Clinical Decision Support System")


# ================= INPUT PANEL =================
with st.sidebar:
    st.header("🧑‍⚕️ Doctor Input Panel")

    patient_name = st.text_input("Patient Name", "John Doe")
    patient_id = st.text_input("Patient ID", "PID-001")

    st.divider()
    st.header("🩺 Clinical Parameters")

    patient = {
        "age": st.number_input("Age (years)", 1, 120, 55),

        "Gender": st.selectbox(
            "Gender", [0, 1],
            format_func=lambda x: "Male" if x else "Female"
        ),

        "cp": st.selectbox(
            "Chest Pain Type",
            [0, 1, 2, 3],
            format_func=lambda x: [
                "Typical Angina",
                "Atypical Angina",
                "Non-anginal Pain",
                "Asymptomatic"
            ][x]
        ),

        "chol": st.number_input("Cholesterol (mg/dl)", 100, 500, 240),

        "trestbps": st.number_input("Resting BP (mm Hg)", 80, 250, 140),

        "thalach": st.number_input("Max Heart Rate Achieved", 60, 220, 120),

        "exang": st.selectbox(
            "Exercise Induced Angina",
            [0, 1],
            format_func=lambda x: "Pain during exercise" if x else "No pain"
        ),

        "restecg": st.selectbox("Resting ECG", [0, 1, 2]),

        "oldpeak": st.slider("ST Depression (oldpeak)", 0.0, 10.0, 2.5),

        "ca": st.selectbox("Major Vessels (ca)", [0, 1, 2, 3, 4]),

        "thal": st.selectbox(
            "Thalassemia",
            [1, 2, 3],
            format_func=lambda x: {
                1: "Normal",
                2: "Fixed Defect",
                3: "Reversible Defect"
            }[x]
        ),
    }

    # 🔴 INPUT CHANGE DETECTION
    current_input = tuple(patient.values())
    if st.session_state.last_input and current_input != st.session_state.last_input:
        st.session_state.result = None

    st.session_state.last_input = current_input

    predict_btn = st.button("🔍 Predict Risk")


# ================= PREDICT =================
if predict_btn:
    score, risk, diseases, contrib, explanations = evaluate(patient)
    st.session_state.result = (score, risk, diseases, contrib, explanations)


# ================= RESULT DISPLAY =================
if st.session_state.result:
    score, risk, diseases, contrib, explanations = st.session_state.result

    col1, col2 = st.columns([2, 2])

    # -------- TEXT RESULT --------
    with col1:
        st.subheader("🧠 Risk Result")

        if "CRITICAL" in risk or "HIGH" in risk:
            st.error(f"Final Risk Level: {risk}")
        elif "MODERATE" in risk or "MILD" in risk:
            st.warning(f"Final Risk Level: {risk}")
        else:
            st.success(f"Final Risk Level: {risk}")

        st.subheader("🦠 Possible Associated Diseases")
        if diseases:
            for d in diseases:
                st.write("•", d)
        else:
            st.success("No significant disease detected")

        st.subheader("🧠 Medical Explanation")
        for exp in explanations:
            st.write("•", exp)

    # -------- GRAPH --------
    with col2:
        st.subheader("📊 Patient vs Normal Clinical Values")

        labels, patient_vals, normal_vals = [], [], []

        for p, meta in GRAPH_PARAMS.items():
            labels.append(meta["label"])
            patient_vals.append(patient[p])
            normal_vals.append(meta["normal"])

        x = range(len(labels))
        width = 0.35

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(x, normal_vals, width, label="Normal")
        ax.bar([i + width for i in x], patient_vals, width, label="Patient")

        ax.set_xticks([i + width / 2 for i in x])
        ax.set_xticklabels(labels, rotation=30)
        ax.set_ylabel("Value")
        ax.set_title("Patient vs Normal Comparison")
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.4)

        st.pyplot(fig)

    # -------- COMPARISON TABLE --------
    st.subheader("📋 Parameter Comparison Table")

    table_data = []
    for p, meta in GRAPH_PARAMS.items():
        val = patient[p]
        normal = meta["normal"]

        if val < normal:
            status = "⬇ Low"
        elif val > normal:
            status = "⬆ High"
        else:
            status = "✅ Normal"

        table_data.append([meta["label"], normal, val, status])

    df_compare = pd.DataFrame(
        table_data,
        columns=["Parameter", "Normal Value", "Patient Value", "Status"]
    )

    st.dataframe(df_compare, use_container_width=True)


# ================= PDF DOWNLOAD =================
if st.session_state.result:
    report_path = "reports/heart_risk_report.pdf"
    os.makedirs("reports", exist_ok=True)

    if st.button("📄 Generate & Download Report"):
        generate_pdf(
            patient_name,
            patient_id,
            patient,
            score,
            risk,
            diseases,
            report_path
        )

        with open(report_path, "rb") as f:
            pdf_bytes = f.read()

        save_report_to_db(
            patient_id,
            patient_name,
            risk,
            pdf_bytes
        )

        st.download_button(
            "⬇ Download Report",
            pdf_bytes,
            file_name="heart_risk_report.pdf",
            mime="application/pdf"
        )
