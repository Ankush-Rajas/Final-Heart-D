# import mysql.connector
# import os
# from utils.db import get_db_connection

# def save_report_to_db(patient_id, patient_name, risk, pdf_bytes):
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="0103",
#         database="heart_disease_db"
#     )

#     cursor = conn.cursor()

#     sql = """
#     INSERT INTO patient_reports
#     (patient_id, patient_name, risk_level, report_blob)
#     VALUES (%s, %s, %s, %s)
#     """

#     cursor.execute(sql, (
#         patient_id,
#         patient_name,
#         risk,
#         pdf_bytes
#     ))

#     conn.commit()
#     print("✅ Report saved in DB")

#     cursor.close()
#     conn.close()


import mysql.connector
import streamlit as st

def save_report_to_db(patient_id, patient_name, risk_level, pdf_bytes):
    conn = mysql.connector.connect(
        host=st.secrets["MYSQLHOST"],
        user=st.secrets["MYSQLUSER"],
        password=st.secrets["MYSQLPASSWORD"],
        database=st.secrets["MYSQLDATABASE"],
        port=st.secrets["MYSQLPORT"]
    )

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO patient_reports
        (patient_id, patient_name, risk_level, report_blob)
        VALUES (%s, %s, %s, %s)
        """,
        (patient_id, patient_name, risk_level, pdf_bytes)
    )

    conn.commit()
    cursor.close()
    conn.close()
