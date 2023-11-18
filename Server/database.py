import shutil
import psycopg2
import os
import uuid
from datetime import datetime
from datetime import datetime, timedelta
import calendar
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
    if encoding is None:
        print("Picture unclear")
        return
    
    all_encodings = get_all_encodings()
    # for id, encoding in all_encodings:
    #     print(f"Processing id: {id}, encoding: {encoding}")
    
    if not all_encodings:
        add_customer(gender,encoding,group_val)
        return
        
    # Compare the received encoding with all encodings in the database
    for id, db_encoding in all_encodings:
        # Compare the encodings using face_recognition library
        results = face_recognition.compare_faces([encoding], db_encoding,tolerance=0.8)
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
    if encoding is None:
        print("Person image not clear or no face detected.")
        return
    all_encodings = get_all_encodings()
    
    if not all_encodings:
        print("No encodings found in the database.")
        return
    
    # for id, encoding in all_encodings:
    #     print(f"Processing id: {id}, encoding: {encoding}")

    # Compare the received encoding with all encodings in the database
    for id, db_encoding in all_encodings:
        # Compare the encodings using face_recognition library
        results = face_recognition.compare_faces([encoding], db_encoding,tolerance=0.8)
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

#FRONT-END CHARTS
def get_daily_gender_distribution():
    try:
        with conn, conn.cursor() as cur:
            # Query to get daily gender distribution
            print("in pie data 2")
            current_date = datetime.now().strftime('%d %m %y')
            print(current_date)
            cur.execute("""
                SELECT
                    COUNT(CASE WHEN c.gender = 'Male' THEN 1 END) as male_count,
                    COUNT(CASE WHEN c.gender = 'Female' THEN 1 END) as female_count,
                    COUNT(CASE WHEN c.gender NOT IN ('Male', 'Female') THEN 1 END) as unknown_count,
                    COUNT(*) as total_count
                FROM customer c
                WHERE c.created_at = %s
            """, (current_date,))
            print("in pie data 4")

            row = cur.fetchone()

            if row:
                male_count = row[0] or 0
                female_count = row[1] or 0
                unknown_count = row[2] or 0
                total_count = row[3] or 1  # Avoid division by zero

                # Calculate percentages
                male_percentage = (male_count / total_count) * 100
                female_percentage = (female_count / total_count) * 100
                unknown_percentage = (unknown_count / total_count) * 100

                print("in pie data 5")

                return {
                    'male_percentage': round(male_percentage, 2),
                    'female_percentage': round(female_percentage, 2),
                    'unknown_percentage': round(unknown_percentage, 2),
                }

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error fetching gender distribution:", error)
        return {
            'male_percentage': 0,
            'female_percentage': 0,
            'unknown_percentage': 0,
        }
    


#get Daily Line CHart data
def get_daily_line_data():
    try:
        with conn, conn.cursor() as cur:
            # Get the current date in the specified format
            current_date = datetime.now().strftime('%d %m %y')

            # Initialize the result dictionary with hourly intervals
            result = {f'{hour:02}:00-{(hour + 1) % 24:02}:00': {'Enter': 0, 'Exit': 0, 'Min': 0, 'Max': 0} for hour in range(8, 22)}

            # Query to get entered counts on an hourly basis for the current date
            cur.execute("""
                SELECT EXTRACT(HOUR FROM TO_TIMESTAMP(time_in, 'HH24:MI:SS'))::integer AS hour, COUNT(*) as count
                FROM visits
                WHERE date = %s
                GROUP BY hour
            """, (current_date,))

            rows = cur.fetchall()

            # Update the result dictionary with the entered counts
            for row in rows:
                hour_interval = f'{row[0]:02}:00-{(row[0] + 1) % 24:02}:00'
                result[hour_interval]['Enter'] = row[1]

            # Query to get exited counts on an hourly basis for the current date
            cur.execute("""
                SELECT EXTRACT(HOUR FROM TO_TIMESTAMP(time_out, 'HH24:MI:SS'))::integer AS hour, COUNT(*) as count
                FROM visits
                WHERE date = %s
                GROUP BY hour
            """, (current_date,))

            rows = cur.fetchall()

            # Update the result dictionary with the exited counts
            for row in rows:
                hour_interval = f'{row[0]:02}:00-{(row[0] + 1) % 24:02}:00'
                result[hour_interval]['Exit'] = row[1]

            # Calculate Min and Max values for each hour
            for hour_interval in result:
                result[hour_interval]['Min'] = min(result[hour_interval]['Enter'], result[hour_interval]['Exit'])
                result[hour_interval]['Max'] = max(result[hour_interval]['Enter'], result[hour_interval]['Exit'])

            return result

    except(Exception, psycopg2.DatabaseError) as error:
        print("Error fetching line data:", error)
        return {}

# hourly_data = get_daily_line_data()
# print(hourly_data)


#weekly line chart data
def get_weekly_line_data():
    try:
        with conn, conn.cursor() as cur:
            # Calculate the date range for the last 7 days
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=6)

            # Initialize the data dictionary
            weekly_data = {'Entered': [], 'Left': [], 'Min': [], 'Max': []}

            # Loop through each day in the week
            for single_date in (start_date + timedelta(n) for n in range(7)):
                date_str = single_date.strftime('%d %m %y')

                # Get the count of people who entered and left the shop on the current day
                cur.execute("""
                    SELECT COUNT(DISTINCT v.customer_id), COUNT(DISTINCT CASE WHEN v.time_out IS NOT NULL THEN v.customer_id END)
                    FROM visits v
                    WHERE v.date = %s
                """, (date_str,))

                entered, left = cur.fetchone()

                # Get the min and max count of people present in the shop at one time on the current day
                cur.execute("""
                    SELECT MIN(people_count), MAX(people_count)
                    FROM (
                        SELECT COUNT(DISTINCT customer_id) AS people_count
                        FROM visits
                        WHERE date = %s
                        GROUP BY time_in
                    ) AS counts
                """, (date_str,))

                min_count, max_count = cur.fetchone()

                # Append the data to the weekly_data dictionary
                weekly_data['Entered'].append(entered)
                weekly_data['Left'].append(left)
                weekly_data['Min'].append(min_count)
                weekly_data['Max'].append(max_count)
            
            return weekly_data

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error fetching weekly line data:", error)
        return {}
    

from datetime import datetime, timedelta
import calendar

def get_monthly_line_data():
    try:
        with conn, conn.cursor() as cur:
            # Calculate the date range for the previous month
            today = datetime.now()
            first_day_of_current_month = today.replace(day=1)
            last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
            first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

            # Initialize the data dictionary
            monthly_data = {'Entered': [], 'Left': [], 'Min': [], 'Max': []}

            # Loop through each day of the previous month
            current_date = first_day_of_previous_month
            while current_date <= last_day_of_previous_month:
                date_str = current_date.strftime('%d %m %y')

                # Get the count of people who entered and left the shop on the current day
                cur.execute("""
                    SELECT COUNT(DISTINCT v.customer_id), COUNT(DISTINCT CASE WHEN v.time_out IS NOT NULL THEN v.customer_id END)
                    FROM visits v
                    WHERE v.date = %s
                """, (date_str,))

                entered, left = cur.fetchone()

                # Get the min and max count of people present in the shop at one time on the current day
                cur.execute("""
                    SELECT MIN(people_count), MAX(people_count)
                    FROM (
                        SELECT COUNT(DISTINCT customer_id) AS people_count
                        FROM visits
                        WHERE date = %s
                        GROUP BY time_in
                    ) AS counts
                """, (date_str,))

                min_count, max_count = cur.fetchone()

                # Append the data to the monthly_data dictionary
                monthly_data['Entered'].append(entered)
                monthly_data['Left'].append(left)
                monthly_data['Min'].append(min_count)
                monthly_data['Max'].append(max_count)

                # Move to the next day
                current_date += timedelta(days=1)

            return monthly_data

    except(Exception, psycopg2.DatabaseError) as error:
        print("Error fetching monthly line data:", error)
        return {}


   

# monthly_data = get_monthly_line_data()
# print(monthly_data) 
 
pie_data = get_daily_gender_distribution()
print("pie data gender: ",pie_data)       
    
# create_tables()
