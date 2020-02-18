import psycopg2

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "123",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "postgres")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from part_drawings"

        
        
    cursor.execute(postgreSQL_select_Query)
    print(" selecting rows from table")
    part_drawings_records= cursor.fetchall()

    print("Print each row and it's columns values")
    for row in part_drawings_records:
            print("part_id =" ,row[0],)
            print("drawing_data =" ,row [1])
            print("file_extension =" ,row[2])

    


    
    
    cursor.execute(postgreSQL_select_Query)
    print(" selecting rows from table")
    person_records= cursor.fetchall()

    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from person"

    print("Print each row and it's columns values1")
    for row in person_records:
        print("id= " ,row[0],)
        print("name =" ,row [1])
        print("file_ext =" ,row[2]) 

    #cursor.execute("insert into category(category_name, category_image) values('hello' ,bytea('C:/Users/L30809.NYPSIT.000/Downloads/new/opencv-face-recognition/dataset'))")
   
       

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
                
