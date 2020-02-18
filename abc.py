import sqlite3

# Connect to the database and create table if it doesn't exist
conn = sqlite3.connect('images.db')
cur = conn.cursor()

def create_table(cursor):
    create_table_query = """
        CREATE TABLE IF NOT EXISTS image (
        name varchar(20) NOT NULL PRIMARY KEY,
        image_file blob NOT NULL
    );
    """
    cursor.execute(create_table_query)

create_table(cur)

cur.execute("SELECT * from image")
abc = cur.fetchall()
print(abc)
