import psycopg2
from config import Config
 
 
def write_blob(part_id, path_to_file, file_extension):
    """ insert a BLOB into a table """
    conn = None
    try:
        # read data from a picture
        drawing = open('C:/Users/hc559/Downloads/facial-master/facial-master/dataset/adrian/00002.jpg', 'rb').read()
        # read database configuration
        
        # connect to the PostgresQL database
        conn = psycopg2.connect(user = "postgres",
                                  password = "123",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "postgres")
        # create a new cursor object
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute("INSERT INTO part_drawings(part_id,file_extension,drawing_data) " +
                    "VALUES(%s,%s,%s)",
                    (part_id, file_extension, psycopg2.Binary(drawing)))
        # commit the changes to the database
        conn.commit()
        # close the communication with the PostgresQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    

    

if __name__ == '__main__':
    write_blob(3, 'C:/Users/hc559/Downloads/facial-master/facial-master/dataset/adrian/00002.jpg', 'jpg')
     



def read_blob(part_id, path_to_dir):
    """ read BLOB data from a table """
    conn = None
    try:
        # read database configuration
        
        # connect to the PostgresQL database
        conn = psycopg2.connect(user = "postgres",
                                  password = "123",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "postgres")
        # create a new cursor object
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(""" SELECT part_name, file_extension, drawing_data
                        FROM part_drawings
                        INNER JOIN parts on parts.part_id = part_drawings.part_id
                        WHERE parts.part_id = %s """,
                    (part_id,))

        
        postgreSQL_select_Query = "select * from part_drawings"

        
        
        cur.execute(postgreSQL_select_Query)
        print(" selecting rows from table")
        part_drawings_records= cur.fetchall()

        print("Print each row and it's columns values")
        for row in part_drawings_records:
            print("part_id =" ,row[0],)
            print("drawing_data =" ,row [1])
            print("file_extension =" ,row[2])

        blob = cur.fetchone()
        open('C:/Users/hc559/Downloads/facial-master/facial-master/dataset/adrian/00002.jpg' + blob[0] + '.' + blob[1], 'wb').write(blob[2])
        # close the communication with the PostgresQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()            