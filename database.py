import mysql.connector

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'tp_final'
}

def create_tables():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    cursor.close()
    cnx.close()

create_tables()
