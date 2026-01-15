from utils.db import get_db_connection

def save_report_to_db(patient_id, patient_name, risk_level, report_path):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO patient_reports 
    (patient_id, patient_name, risk_level, report_path)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (
        patient_id,
        patient_name,
        risk_level,
        report_path
    ))

    conn.commit()
    cursor.close()
    conn.close()
