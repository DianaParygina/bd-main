import pyodbc

def get_db_connection():
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"  # Замените на имя вашего сервера
        "DATABASE=personal_data;"  # Замените на имя вашей базы данных
        "UID=django_user;"  # Замените на ваше имя пользователя
        "PWD=djangoUser123;"  # Замените на ваш пароль
    )
    conn = pyodbc.connect(connection_string)
    return conn