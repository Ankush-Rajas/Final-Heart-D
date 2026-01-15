from utils.db import get_connection

def get_report_by_patient_id(patient_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT patient_id, patient_name, risk_level, report_path, created_at
    FROM patient_reports
    WHERE patient_id = %s
    ORDER BY created_at DESC
    LIMIT 1
    """
    cursor.execute(query, (patient_id,))
    result = cursor.fetchone()

    conn.close()
    return result
