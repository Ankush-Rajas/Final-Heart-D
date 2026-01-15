# import json
# import os

# # ================= PATH =================
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# RULE_FILE = os.path.join(BASE_DIR, "rules", "risk_rules.json")

# # ================= LOAD RULES =================
# with open(RULE_FILE, "r") as f:
#     RULES = json.load(f)


# # ================= MAIN EVALUATION =================
# def evaluate(patient):
#     total_score = 0
#     diseases = set()
#     contribution = {}

#     # ---------- AGE ----------
#     if patient["age"] >= 70:
#         contribution["age"] = 4
#         total_score += 4
#     elif patient["age"] >= 60:
#         contribution["age"] = 3
#         total_score += 3
#     elif patient["age"] >= 50:
#         contribution["age"] = 2
#         total_score += 2
#     elif patient["age"] >= 40:
#         contribution["age"] = 1
#         total_score += 1

#     # ---------- CHEST PAIN ----------
#     if patient["cp"] == 3:
#         contribution["cp"] = 5
#         total_score += 5
#         diseases.add("Silent Ischemia")
#     elif patient["cp"] == 0:
#         contribution["cp"] = 4
#         total_score += 4
#         diseases.add("Coronary Artery Disease")

#     # ---------- EXERCISE ANGINA ----------
#     if patient["exang"] == 1:
#         contribution["exang"] = 4
#         total_score += 4
#         diseases.add("Exercise Induced Ischemia")

#     # ---------- OLDPEAK ----------
#     if patient["oldpeak"] >= 3.0:
#         contribution["oldpeak"] = 7
#         total_score += 7
#         diseases.add("Severe Myocardial Ischemia")
#     elif patient["oldpeak"] >= 2.0:
#         contribution["oldpeak"] = 5
#         total_score += 5
#         diseases.add("Myocardial Ischemia")

#     # ---------- MAJOR VESSELS ----------
#     if patient["ca"] >= 3:
#         contribution["ca"] = 8
#         total_score += 8
#         diseases.add("Severe Coronary Artery Disease")
#     elif patient["ca"] >= 2:
#         contribution["ca"] = 5
#         total_score += 5
#         diseases.add("Coronary Artery Disease")

#     # ---------- THAL ----------
#     if patient["thal"] == 3:
#         contribution["thal"] = 5
#         total_score += 5
#         diseases.add("Active Ischemia")
#     elif patient["thal"] == 2:
#         contribution["thal"] = 3
#         total_score += 3
#         diseases.add("Previous Myocardial Damage")

#     # ---------- BLOOD PRESSURE ----------
#     if patient["trestbps"] >= 160:
#         contribution["trestbps"] = 6
#         total_score += 6
#         diseases.add("Severe Hypertension")
#     elif patient["trestbps"] >= 140:
#         contribution["trestbps"] = 4
#         total_score += 4
#         diseases.add("Hypertension Related Heart Risk")

#     # ---------- CHOLESTEROL ----------
#     if patient["chol"] >= 280:
#         contribution["chol"] = 6
#         total_score += 6
#         diseases.add("Severe Hypercholesterolemia")
#     elif patient["chol"] >= 240:
#         contribution["chol"] = 4
#         total_score += 4
#         diseases.add("Hypercholesterolemia")

#     # ---------- FINAL RISK ----------
#     if total_score <= 10:
#         risk = "LOW RISK"
#     elif total_score <= 20:
#         risk = "MILD RISK"
#     elif total_score <= 30:
#         risk = "MODERATE RISK"
#     elif total_score <= 40:
#         risk = "HIGH RISK"
#     else:
#         risk = "CRITICAL RISK"

#     return total_score, risk, sorted(diseases), contribution



import json
import os

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULE_FILE = os.path.join(BASE_DIR, "rules", "risk_rules.json")

# ================= LOAD RULES =================
with open(RULE_FILE, "r") as f:
    RULES = json.load(f)


# ================= MAIN EVALUATION =================
def evaluate(patient):
    total_score = 0
    diseases = []
    contribution = {}
    explanations = []   # 👈 NEW (reason + explanation)

    # ---------- AGE ----------
    if patient["age"] >= 70:
        score = 4
        reason = "Advanced age weakens arteries and heart muscles"
        effect = "Higher chance of artery blockage and heart failure"
    elif patient["age"] >= 60:
        score = 3
        reason = "Age-related loss of vessel elasticity"
        effect = "Reduced blood flow efficiency"
    elif patient["age"] >= 50:
        score = 2
        reason = "Middle age increases cardiovascular stress"
        effect = "Moderate risk of heart disease"
    elif patient["age"] >= 40:
        score = 1
        reason = "Early age-related heart risk"
        effect = "Low but noticeable heart strain"
    else:
        score = 0
        reason = "Young age"
        effect = "Minimal heart risk"

    total_score += score
    contribution["age"] = score
    explanations.append(
        f"AGE: {reason}. Effect: {effect}."
    )

    # ---------- CHEST PAIN ----------
    if patient["cp"] == 3:
        score = 5
        disease = "Silent Ischemia"
        reason = "Heart muscle receives less oxygen without visible pain"
        effect = "Hidden heart damage risk"
    elif patient["cp"] == 0:
        score = 4
        disease = "Coronary Artery Disease"
        reason = "Blocked coronary arteries reduce blood supply"
        effect = "Chest pain and heart attack risk"
    else:
        score = 0
        disease = None
        reason = "No severe chest pain type"
        effect = "Low blockage risk"

    total_score += score
    contribution["cp"] = score
    explanations.append(f"CHEST PAIN: {reason}. Effect: {effect}.")
    if disease:
        diseases.append(disease)

    # ---------- EXERCISE ANGINA ----------
    if patient["exang"] == 1:
        score = 4
        disease = "Exercise Induced Ischemia"
        reason = "Heart cannot supply enough oxygen during physical activity"
        effect = "High risk during exercise"
    else:
        score = 0
        disease = None
        reason = "No pain during exercise"
        effect = "Good oxygen supply"

    total_score += score
    contribution["exang"] = score
    explanations.append(f"EXERCISE ANGINA: {reason}. Effect: {effect}.")
    if disease:
        diseases.append(disease)

    # ---------- OLDPEAK ----------
    if patient["oldpeak"] >= 3.0:
        score = 7
        disease = "Severe Myocardial Ischemia"
        reason = "Major ST depression during stress"
        effect = "Severe oxygen deficiency to heart muscle"
    elif patient["oldpeak"] >= 2.0:
        score = 5
        disease = "Myocardial Ischemia"
        reason = "Moderate ST depression"
        effect = "Reduced blood flow during stress"
    else:
        score = 0
        disease = None
        reason = "Normal ST segment"
        effect = "Healthy heart response"

    total_score += score
    contribution["oldpeak"] = score
    explanations.append(f"OLDPEAK: {reason}. Effect: {effect}.")
    if disease:
        diseases.append(disease)

    # ---------- MAJOR VESSELS ----------
    if patient["ca"] >= 3:
        score = 8
        disease = "Severe Coronary Artery Disease"
        reason = "Multiple blood vessels are blocked"
        effect = "Very high heart attack risk"
    elif patient["ca"] >= 2:
        score = 5
        disease = "Coronary Artery Disease"
        reason = "Partial blockage in coronary vessels"
        effect = "Reduced blood flow to heart"
    else:
        score = 0
        disease = None
        reason = "No major vessel blockage"
        effect = "Normal circulation"

    total_score += score
    contribution["ca"] = score
    explanations.append(f"VESSELS (CA): {reason}. Effect: {effect}.")
    if disease:
        diseases.append(disease)

    # ---------- THAL ----------
    if patient["thal"] == 3:
        score = 5
        disease = "Active Ischemia"
        reason = "Reversible defect indicates active blood flow problem"
        effect = "Ongoing heart muscle stress"
    elif patient["thal"] == 2:
        score = 3
        disease = "Previous Myocardial Damage"
        reason = "Fixed defect shows permanent damage"
        effect = "Reduced heart efficiency"
    else:
        score = 0
        disease = None
        reason = "Normal thalassemia test"
        effect = "Healthy heart tissue"

    total_score += score
    contribution["thal"] = score
    explanations.append(f"THAL: {reason}. Effect: {effect}.")
    if disease:
        diseases.append(disease)

    # ---------- BLOOD PRESSURE ----------
    if patient["trestbps"] >= 160:
        score = 6
        disease = "Severe Hypertension"
        reason = "Very high blood pressure increases heart workload"
        effect = "Heart failure and stroke risk"
    elif patient["trestbps"] >= 140:
        score = 4
        disease = "Hypertension"
        reason = "High blood pressure stresses arteries"
        effect = "Long-term heart damage"
    else:
        score = 0
        disease = None
        reason = "Normal blood pressure"
        effect = "Healthy circulation"

    total_score += score
    contribution["trestbps"] = score
    explanations.append(f"BLOOD PRESSURE: {reason}. Effect: {effect}.")
    if disease:
        diseases.append(disease)

    # ---------- CHOLESTEROL ----------
    if patient["chol"] >= 280:
        score = 6
        disease = "Severe Hypercholesterolemia"
        reason = "Excess cholesterol blocks arteries"
        effect = "High heart attack risk"
    elif patient["chol"] >= 240:
        score = 4
        disease = "Hypercholesterolemia"
        reason = "Fat buildup inside arteries"
        effect = "Reduced blood flow"
    else:
        score = 0
        disease = None
        reason = "Normal cholesterol level"
        effect = "Clear arteries"

    total_score += score
    contribution["chol"] = score
    explanations.append(f"CHOLESTEROL: {reason}. Effect: {effect}.")
    if disease:
        diseases.append(disease)

    # ---------- FINAL RISK ----------
    if total_score <= 10:
        risk = "LOW RISK"
    elif total_score <= 20:
        risk = "MILD RISK"
    elif total_score <= 30:
        risk = "MODERATE RISK"
    elif total_score <= 40:
        risk = "HIGH RISK"
    else:
        risk = "CRITICAL RISK"

    # 👇 FINAL RETURN (IMPORTANT)
    return total_score, risk, sorted(set(diseases)), contribution, explanations


# ab risk_engin file me kya likhu jise konse value pe konsa disease ha dikhe input parameter ke hisab se 