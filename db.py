import mysql.connector
from mysql.connector import Error

# Database connection details
DB_HOST = 'localhost'  # Change this to your remote host or Docker container IP
DB_NAME = 'attendance_db'
DB_USER = 'root'
DB_PASS = '3699'

def connect_db():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        if conn.is_connected():
            print("Connected to the database successfully")
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None
