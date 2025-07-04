import mysql.connector
from mysql.connector import Error

class DbConnection:
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='ai_agent',
                user='root',
                password='password'  # Replace with your actual MySQL password
            )
            if connection.is_connected():
                print("Connected to MySQL database")
                return connection
        except Error as e:
            print("Error while connecting to MySQL:", e)
            return None

#Test the connection if this file is run directly
if __name__ == "__main__":
    conn = DbConnection.get_connection()
    if conn:
        print("Connection test passed.")
        conn.close()
    else:
        print("Connection test failed.")
