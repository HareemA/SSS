import shutil
import psycopg2
import os
import uuid
from datetime import datetime
import face_recognition
import numpy as np

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="SSS",
    user="postgres",
    password="12345"
)

def create_tables():
    try:
        with conn, conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
            
            #Customer table
            cur.execute("""create table if not exists customer(
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                name VARCHAR NOT NULL,
                gender VARCHAR NOT NULL,
                age INT,
                encoding BYTEA,
                created_at VARCHAR,
                modified_at VARCHAR
                )""")
            
            #Visit table
            cur.execute("""create table if not exists visits(
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                customer_id UUID,
                date VARCHAR,
                time_in VARCHAR NOT NULL,
                time_out VARCHAR,
                group_val BOOLEAN,
                FOREIGN KEY(customer_id) references customer(id)
                )""")
    except(Exception, psycopg2.DatabaseError) as error:
        print("Couldnt create tables ",error)
  

def customer_exist(encoding,group_val,gender):
    print("Here 1")
    all_encodings = get_all_encodings()
    print("Here 2")
    # for id, encoding in all_encodings:
    #     print(f"Processing id: {id}, encoding: {encoding}")
    
    if not all_encodings:
        add_customer(gender,encoding,group_val)
        return
        
    # Compare the received encoding with all encodings in the database
    for id, db_encoding in all_encodings:
        # Compare the encodings using face_recognition library
        results = face_recognition.compare_faces([encoding], db_encoding)
        # Check if a match is found
        if results[0]:
            add_visit(id,group_val)
        else:
            add_customer(gender,encoding,group_val)
            
    
# In the add_customer function
def add_customer(gender, encoding, group_val):
    print("In add customer")
    name = "unknown"
    created_at = datetime.now().strftime("%d %m %y")
    modified_at = datetime.now().strftime("%d %m %y")
    try:
        with conn, conn.cursor() as cur:
            # Convert the 1D encoding array to bytes
            encoding_bytes = encoding.tobytes()
            cur.execute("""
                INSERT INTO customer (name, gender, age, encoding, created_at, modified_at)
                VALUES (%s, %s, %s, %s, %s, %s) returning id
            """, (name, gender, None, encoding_bytes, created_at, modified_at))
            customer_id = cur.fetchone()[0]
            print("Customer added ",customer_id)
        add_visit(customer_id, group_val)
    except(Exception, psycopg2.DatabaseError) as error:
        print("Couldnt add customer ", error)

        
       
def add_visit(id,group_val):
    date = datetime.now().strftime("%d %m %y")
    time_in = datetime.now().strftime("%H:%M:%S")
    try:
        with conn, conn.cursor() as cur:
            #To check if persn who entered left as well
            cur.execute("""
                SELECT id
                FROM visits
                WHERE customer_id = %s AND time_out IS NULL
            """, (id,))
            
            existing_visit_id = cur.fetchone()
            
            if existing_visit_id:
                print("Customer is already inside. Cant add a new visit entry.")
                return
            
            cur.execute("""INSERT INTO VISITS (customer_id,date,time_in,group_val) VALUES (%s,%s,%s,%s)""",
                        (id,date,time_in,group_val))
            print("Visit added")
            
    except(Exception, psycopg2.DatabaseError) as error:
        print("Couldnt add visit ",error)
 
 
def customer_leaving(encoding):
    all_encodings = get_all_encodings()
    
    if not all_encodings:
        print("No encodings found in the database.")
        return
    
    # for id, encoding in all_encodings:
    #     print(f"Processing id: {id}, encoding: {encoding}")

    # Compare the received encoding with all encodings in the database
    for id, db_encoding in all_encodings:
        # Compare the encodings using face_recognition library
        results = face_recognition.compare_faces([encoding], db_encoding)
        print("Here 1")
        # Check if a match is found
        if results[0]:
            edit_visit(id)
        else:
            print("Customer not found")
            


def edit_visit(customer_id):
    date = datetime.now().strftime("%d %m %y")
    time_out = datetime.now().strftime("%H:%M:%S")
    try:
        with conn, conn.cursor() as cur:
            cur.execute("""
                UPDATE visits
                SET time_out = %s
                WHERE customer_id = %s AND date = %s AND time_out IS NULL
            """, (time_out, customer_id, date))
    except(Exception, psycopg2.DatabaseError) as error:
        print("Couldn't edit visit ", error)

       
         
def get_all_encodings():
    print("Getting encodings")
    try:
        with conn, conn.cursor() as cur:
            cur.execute("SELECT id, encoding FROM customer")
            rows = cur.fetchall()
            if rows is not None:
                return [(row[0], np.frombuffer(row[1], dtype=np.float64)) for row in rows]
                # Convert the bytes back to the 1D NumPy array
            else:
                return []
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error fetching encodings:", error)
        return []





create_tables()