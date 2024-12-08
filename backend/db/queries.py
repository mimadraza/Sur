from backend.db.db_connection import get_db_connection

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def call_procedure(proc_name, params):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.callproc(proc_name, params)
        else:
            cursor.callproc(proc_name)

        # Fetch results if the procedure returns data
        results = []
        for result in cursor.stored_results():
            results = result.fetchall()

        return results
    finally:
        cursor.close()
        connection.close()
