import mysql.connector
cnx = mysql.connector.connect(user='root', password='Lotus@123', host='localhost', database='vivek')
cursor = cnx.cursor()

db_config = {
    'user': 'root',
    'password': 'Lotus@123',
    'host': 'localhost',
    'database': 'vivek'
}

def get_db():
    conn = mysql.connector.connect(**db_config)
    return conn

conn = get_db()
cursor = conn.cursor()
query = "SELECT image_path,animal_name from animals"
cursor.execute(query)
result = cursor.fetchall()
conn.close()
cursor.close()

print(result)