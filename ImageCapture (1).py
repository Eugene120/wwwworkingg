import sqlite3
from io import StringIO, BytesIO
import numpy as np
from sqlite3 import dbapi2 as sqlite

import cv2
import os
from PIL import Image


def create_table(cursor):
    create_table_query = """
        CREATE TABLE IF NOT EXISTS image (
        name varchar(20) NOT NULL PRIMARY KEY,
        image_file blob NOT NULL
    );
    """
    cursor.execute(create_table_query)


def store_in_database(cur, image_name, data):
    cur.execute("INSERT INTO image (name, image_file) values (?, ?)", (image_name, sqlite.Binary(data)))
    conn.commit()


def retrieve_from_database(cur, image):
    cur.execute("SELECT image_file FROM image WHERE name = ?", (image,))
    img = cur.fetchone()[0]
    return StringIO(img)


def retrieve_all(cur, show=False):
    cur.execute("SELECT * FROM image")
    all_imgs = cur.fetchall()
    image_dict = dict()
    for img in all_imgs:
        image = Image.open(BytesIO(img[1]))
        image_dict[img[0]] = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        if show:
            image.show()
    return image_dict


cam = cv2.VideoCapture(0)

# Connect to the database and create table if it doesn't exist
conn = sqlite3.connect(os.path.join(os.getcwd(), 'images.db'))
cur = conn.cursor()
create_table(cur)

cv2.namedWindow("test")

img_counter = 0

name_of_person = input("Please enter the name:")

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed
        img_name = "{0}_{1}.png".format(name_of_person, img_counter)
        # Convert the cv2 img matrix to string
        img_data = cv2.imencode(".png", frame)[1].tostring()

        # Save to database
        store_in_database(cur, img_name, img_data)

        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
