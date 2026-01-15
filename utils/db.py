import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # apna user
        password="0103",  # apna password
        database="heart_disease_db"
    )
