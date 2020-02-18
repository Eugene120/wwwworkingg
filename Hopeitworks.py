import os
import sys
import psycopg2
import argparse

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



    def main(argv):
        parser = argparse.ArgumentParser()
        parser_action = parser.add_mutually_exclusive_group(required=True)
        parser_action.add_argument("--store", action='store_const', const=True, help="Load an image from the named file and save it in the DB")
        parser_action.add_argument("--fetch", type=int, help="Fetch an image from the DB and store it in the named file, overwriting it if it exists. Takes the database file identifier as an argument.", metavar='42')
        parser.add_argument("filename", help="Name of file to write to / fetch from")

        
        args = parser.parse_args(argv[1:])
    
        
        args = {
	
	            'store': 'C:/Users/hc559/Downloads/facial-master/facial-master/dataset/Avan',
	            'fetch': 'C:/Users/hc559/Downloads/facial-master/facial-master/dataset/Avan',
	            'filename': 'C:/Users/hc559/Downloads/facial-master/facial-master/dataset/adrian'
   
    
        }

    

    

        # and run the command
        if args['store']:
            # Reads the whole file into memory. If you want to avoid that,
            # use large object storage instead of bytea; see the psycopg2
            # and postgresql documentation.
            f = open(args['filename'],'rb')

            # The following code works as-is in Python 3.
            #
            # In Python 2, you can't just pass a 'str' directly, as psycopg2
            # will think it's an encoded text string, not raw bytes. You must
            # either use psycopg2.Binary to wrap it, or load the data into a
            # "bytearray" object.
            #
            # so either:
            #
            #   filedata = psycopg2.Binary( f.read() )
            #
            # or
            #
            #   filedata = buffer( f.read() )
            #
            filedata = f.read()
            cursor.execute("INSERT INTO files(id, orig_filename, file_data) VALUES (DEFAULT,%s,%s) RETURNING id", (args['filename'], filedata))
            returned_id = cursor.fetchone()[0]
            f.close()
            connection.commit()
            print("Stored {0} into DB record {1}".format(args['filename'], returned_id))

        elif args['fetch'] is not None:
            # Fetches the file from the DB into memory then writes it out.
            # Same as for store, to avoid that use a large object.
            f = open(args['filename'],'wb')
            cursor.execute("SELECT file_data, orig_filename FROM files WHERE id = %s", (int(args['fetch']),))
            (file_data, orig_filename) = cursor.fetchone()

                # In Python 3 this code works as-is.
                # In Python 2, you must get the str from the returned buffer object.
            f.write(file_data)
            f.close()
            print("Fetched {0} into file {1}; original filename was {2}".format(args['fetch'], args['filename'], orig_filename))

        connection.close()

    if __name__ == '__main__':
        main(sys.argv)

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")    