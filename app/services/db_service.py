from mysql.connector import Error
from app.db.db_connection import DbConnection

class DbService:
    @staticmethod
    def log_chat(user_id,user_input, bank_id, platform, response):
        conn = DbConnection.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                insert_query = """
                    INSERT INTO db_aichats (userId, userInput, bankId, platForm, response)
                    VALUES (%s, %s, %s, %s, %s)
                """
                values = (user_id, user_input, bank_id, platform, response)
                cursor.execute(insert_query, values)
                conn.commit()
                print("Chat logged successfully.")
            except Error as e:
                print("Failed to insert chat:", e)
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def get_chats_by_user_id(user_id):
        conn = DbConnection.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                select_query = "SELECT * FROM db_aichats WHERE userId = %s"
                cursor.execute(select_query, (user_id,))
                results = cursor.fetchall()
                return results
            except Error as e:
                print("Failed to fetch chats:", e)
                return []
            finally:
                cursor.close()
                conn.close()
        return None

