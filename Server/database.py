import shutil
import psycopg2
import os
import uuid
import datetime
import face_recognition

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
                encoding VARCHAR,
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
    
    
def get_all_encodings():
    try:
        with conn, conn.cursor() as cur:
            cur.execute("SELECT id,encoding FROM parent")
            rows = cur.fetchall()
            return [(row[0],row[1]) for row in rows]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error fetching encodings:", error)
        return []


def customer_exist(encoding):
    all_encodings = get_all_encodings()
    
    if not all_encodings:
        print("No encodings found in the database.")
        return
    
    for id, encoding in all_encodings:
        print(f"Processing id: {id}, encoding: {encoding}")


    unknown_encoding = face_recognition.face_encodings([encoding])[0]

    # Compare the received encoding with all encodings in the database
    for id, db_encoding in all_encodings:
        db_encoding = bytes.fromhex(db_encoding)  # Convert hex string to bytes
        known_encoding = face_recognition.face_encodings([db_encoding])[0]

        # Compare the encodings using face_recognition library
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)

        # Check if a match is found
        if results[0]:
            add_visit(id)
        else:
            add_customer(encoding)
   


def add_customer(gender,encoding):
    name="unknown"
    created_at = datetime.now().strftime("%d %m %y")
    modified_at = datetime.now().strftime("%d %m %y")
    try:
        with conn, conn.cursor() as cur:
            cur.execute("""
                INSERT INTO parent (name, gender, age, encoding, created_at, modified_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, gender, None, encoding, created_at, modified_at))
    except(Exception, psycopg2.DatabaseError) as error:
        print("Couldnt add customer ",error)
 
       
def add_visits(id):
    date = datetime.now().strftime("%d %m %y")
    time_in = current_time = datetime.strptime(str(current_time), '%H:%M:%S')
    try:
        with conn, conn.cursor() as cur:
            cur.execute("""INSERT INTO VISIT (customer_id,date,time_in,time_out,group_val) VALUES (%s,%s,%s,%s,%s)""",
                        (id,date))
    except(Exception, psycopg2.DatabaseError) as error:
        print("Couldnt add visit ",error)
    
    
        
    
# create_tables()