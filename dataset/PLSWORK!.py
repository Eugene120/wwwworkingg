import psycopg2
from config import Config
 
 
def write_blob(part_id, path_to_file, file_extension):
    """ insert a BLOB into a table """
    connection = psycopg2.connect(user = "postgres",
                                  password = "123",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "postgres")
    try:
        # read data from a picture
        drawing = open(path_to_file, 'rb').read()
        # read database configuration
        params = Config()
        # connectionect to the PostgresQL database
        connection = psycopg2.connect(**params)
        # create a new cursor object
        cur = connection.cursor()
        # execute the INSERT statement
        cur.execute("INSERT INTO files(id,orig_filename,file_data) " +
                    "VALUES(%s,%s,%s)",
                    (id, file_data ,psycopg2.Binary(drawing)))
        # commit the changes to the database
        connection.commit()
        # close the communication with the PostgresQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    write_blob(1, 'C:/Users/hc559/Downloads/facial-master/facial-master/dataset/adrian/00002.jpg', 'jpg')   


def read_blob(part_id, path_to_dir):
    """ read BLOB data from a table """
    connection = psycopg2.connect(user = "postgres",
                                  password = "123",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "postgres")
    try:
        # read database configuration
        params = Config()
        # connectionect to the PostgresQL database
        connection = psycopg2.connect(**params)
        # create a new cursor object
        cur = connection.cursor()
        # execute the SELECT statement
        cur.execute(""" SELECT part_name, file_extension, drawing_data
                        FROM part_drawings
                        INNER JOIN parts on parts.part_id = part_drawings.part_id
                        WHERE parts.part_id = %s """,
                    (part_id,))
 
        blob = cur.fetchone()
        open(path_to_dir + blob[0] + '.' + blob[1], 'wb').write(blob[2])
        # close the communication with the PostgresQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()         