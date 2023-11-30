import shutil
import psycopg2
import os
import uuid
from datetime import datetime
from datetime import datetime, timedelta
import calendar
import statistics
from collections import defaultdict
import face_recognition
import numpy as np

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="SSS",
    user="postgres",
    password="12345" #serG
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
  
    if not all_encodings:
        print("In not all encodings thing")
        add_customer(gender,encoding,group_val)
        return
        
    # Compare the received encoding with all encodings in the database
    for id, db_encoding in all_encodings:
        # Compare the encodings using face_recognition library
        results = face_recognition.compare_faces([encoding], db_encoding,tolerance=0.7)
        # Check if a match is found
        if results[0]:
            result = check_visit(id)
            if result:
                add_visit(id,group_val)
            else:
                check_exit_enter_time_diff(id)
            return
    
    add_customer(gender,encoding,group_val)
            
    
# In the add_customer function
def add_customer(gender, encoding, group_val):
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


#To check if person who entered isnt still in the shop
def check_visit(id):
    try:
        with conn, conn.cursor() as cur:
            cur.execute("""
                SELECT id
                FROM visits
                WHERE customer_id = %s AND time_out IS NULL
            """, (id,))
            
            existing_visit_id = cur.fetchone()
            
            if existing_visit_id:
                print("Customer is already inside. Cant add a new visit entry.")
                return False
            else:
                return True
            
    except(Exception, psycopg2.DatabaseError) as error:
        print("Couldnt finf visit ",error)
    
       
def check_exit_enter_time_diff(id):
    current_time = datetime.now().strftime("%H:%M:%S")
    time_difference_minutes =0
    print("In check time diff")
    try:
        with conn, conn.cursor() as cur:
            cur.execute("""SELECT customer_id, time_in
                        FROM visits
                        WHERE customer_id = %s AND time_out IS NULL;""",(id,))
            
            result = cur.fetchone()

            if result is not None:
                customer_id, time_in_str = result

                time_in = datetime.strptime(time_in_str, "%H:%M:%S")

                # Convert current_time from string to datetime object
                current_time_datetime = datetime.strptime(current_time, "%H:%M:%S")

                # Calculate the time difference in minutes
                time_difference = current_time_datetime - time_in
                time_difference_minutes = time_difference.total_seconds() / 60
                print(f"Time difference: {time_difference}")

        if time_difference_minutes > 4:
            edit_visit(id)
            
    except(Exception, psycopg2.DatabaseError) as error:
        print("Couldnt check time difference ",error)
    
def add_visit(id,group_val):
    date = datetime.now().strftime("%d %m %y")
    time_in = datetime.now().strftime("%H:%M:%S")
    try:
        with conn, conn.cursor() as cur:
            cur.execute("""INSERT INTO VISITS (customer_id,date,time_in,group_val) VALUES (%s,%s,%s,%s)""",
                        (id,date,time_in,group_val))
            
            print("Visit added")
            
    except(Exception, psycopg2.DatabaseError) as error:
        print("Couldnt add visit ",error)
     

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
            print("Time out updated")
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
            current_date = datetime.now().strftime('%d %m %y')
            print(current_date)
            cur.execute("""
                SELECT
                    COUNT(CASE WHEN c.gender = 'Male' THEN 1 END) as male_count,
                    COUNT(CASE WHEN c.gender = 'Female' THEN 1 END) as female_count,
                    COUNT(CASE WHEN c.gender = 'Unknown' THEN 1 END) as unknown_count,
                    COUNT(*) as total_count
                    FROM customer c
                    WHERE c.id IN (
                        SELECT v.customer_id
                        FROM visits v
                        WHERE v.date = %s
                    );
            """, (current_date,))

            row = cur.fetchone()

            if row:
                male_count = row[0] or 0
                print(male_count)
                female_count = row[1] or 0
                print(female_count)
                unknown_count = row[2] or 0
                total_count = row[3] or 1  # Avoid division by zero

                # Calculate percentages
                male_percentage = (male_count / total_count) * 100
                female_percentage = (female_count / total_count) * 100
                print("Unknown: ",unknown_count)
                unknown_percentage = (unknown_count / total_count) * 100
                print(unknown_percentage)


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
            print(current_date)

            # Initialize the result dictionary with hourly intervals
            result = {f'{hour:02}:00-{(hour + 1) % 24:02}:00': {'Enter': 0, 'Exit': 0, 'Min': 0, 'Max': 0} for hour in range(8, 22)}

            # Query to get entered counts on an hourly basis for the current date
            cur.execute("""
                SELECT
                hours.hour_of_entry,
                COALESCE(COUNT(v.id), 0) AS number_of_customers
                    FROM
                        (SELECT generate_series(0, 23) AS hour_of_entry) hours
                    LEFT JOIN
                        visits v
                    ON
                        hours.hour_of_entry = EXTRACT(HOUR FROM TO_TIMESTAMP(v.time_in, 'HH24:MI:SS')) AND v.date = %s
                    GROUP BY
                        hours.hour_of_entry
                    ORDER BY
                        hours.hour_of_entry ;
            """, (current_date,))

            rows = cur.fetchall()

                  


            for row in rows:
                try:
                    hour_interval = f'{row[0]:02}:00-{(row[0] + 1) % 24:02}:00'
                    
                    # If the value is None or 0, set it to 0 in the result dictionary
                    result[hour_interval]['Enter'] = row[1] if row[1] is not None and row[1] != 0 else 0
                except KeyError as e:
                    print(f"Error updating 'Enter' value for {hour_interval}: {e}")
                except Exception as ex:
                    print(f"Error processing data for {hour_interval}: {ex}")

            

            # Query to get exited counts on an hourly basis for the current date
            cur.execute("""
                SELECT
                hours.hour_of_entry,
                COALESCE(COUNT(v.id), 0) AS number_of_customers
                    FROM
                        (SELECT generate_series(0, 23) AS hour_of_entry) hours
                    LEFT JOIN
                        visits v
                    ON
                        hours.hour_of_entry = EXTRACT(HOUR FROM TO_TIMESTAMP(v.time_out, 'HH24:MI:SS')) AND v.date = %s
                    GROUP BY
                        hours.hour_of_entry
                    ORDER BY
                        hours.hour_of_entry ;

            """, (current_date,))

            rows = cur.fetchall()
            

            # Update the result dictionary with the exited counts
            
            for row in rows:
                try:
                    hour_interval = f'{row[0]:02}:00-{(row[0] + 1) % 24:02}:00'
                    
                    # If the value is None or 0, set it to 0 in the result dictionary
                    result[hour_interval]['Enter'] = row[1] if row[1] is not None and row[1] != 0 else 0
                except KeyError as e:
                    print(f"Error updating 'Enter' value for {hour_interval}: {e}" )

            return result

    except(Exception, psycopg2.DatabaseError) as error:
        print("Error fetching line data:", error)
        return {}

# hourly_data = get_daily_line_data()
# print(hourly_data)


# weekly line chart data
def get_weekly_line_data():
    try:
        with conn, conn.cursor() as cur:
            # Calculate the date range for the last 7 days
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=6)

            # Array of days
            days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

            # Find the current day of the week
            day_index = datetime.now().weekday()

            # Initialize the data dictionary
            weekly_data = {'Entered': [], 'Left': [], 'Min': [], 'Max': [], 'index': day_index}

            # Loop through each day in the week
            for single_date in (start_date + timedelta(n) for n in range(7)):
                date_str = single_date.strftime('%d %m %y')

                # Get the count of people who entered and left the shop on the current day
                cur.execute("""
                    SELECT COUNT(v.customer_id), COUNT(CASE WHEN v.time_out IS NOT NULL THEN v.customer_id END)
                    FROM visits v
                    WHERE v.date = %s
                """, (date_str,))

                entered, left = cur.fetchone()

                # Get the min count of people present in the shop at one time on the current day
                cur.execute("""
                    SELECT
                    COUNT(*) AS number_of_customers
                    FROM
                        visits v
                    WHERE
                        date = %s
                    GROUP BY
                        EXTRACT(HOUR FROM TO_TIMESTAMP(v.time_in, 'HH24:MI:SS'))
                    ORDER BY
                        number_of_customers
                    LIMIT 1;

                """, (date_str,))

                min_count = cur.fetchone()

                # Get the min count of people present in the shop at one time on the current day
                cur.execute("""
                    SELECT
                    COUNT(*) AS number_of_customers
                    FROM
                        visits v
                    WHERE
                        date = %s
                    GROUP BY
                        EXTRACT(HOUR FROM TO_TIMESTAMP(v.time_in, 'HH24:MI:SS'))
                    ORDER BY 
                        number_of_customers DESC
                    LIMIT 1;
                """, (date_str,))

                max_count = cur.fetchone()

                # Append the data to the weekly_data dictionary
                weekly_data['Entered'].append(entered)
                weekly_data['Left'].append(left)
                weekly_data['Min'].append(min_count)
                weekly_data['Max'].append(max_count)
            
            return weekly_data

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error fetching weekly line data:", error)
        return{}
    


#to get data for monthly line chart
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
                    SELECT COUNT(v.customer_id), COUNT(CASE WHEN v.time_out IS NOT NULL THEN v.customer_id END)
                    FROM visits v
                    WHERE v.date = %s
                """, (date_str,))

                entered, left = cur.fetchone()

                 # Get the min count of people present in the shop at one time on the current day
                cur.execute("""
                    SELECT
                    COUNT(*) AS number_of_customers
                    FROM
                        visits v
                    WHERE
                        date = %s
                    GROUP BY
                        EXTRACT(HOUR FROM TO_TIMESTAMP(v.time_in, 'HH24:MI:SS'))
                    ORDER BY
                        number_of_customers
                    LIMIT 1;

                """, (date_str,))

                min_count = cur.fetchone()

                # Get the min count of people present in the shop at one time on the current day
                cur.execute("""
                    SELECT
                    COUNT(*) AS number_of_customers
                    FROM
                        visits v
                    WHERE
                        date = %s
                    GROUP BY
                        EXTRACT(HOUR FROM TO_TIMESTAMP(v.time_in, 'HH24:MI:SS'))
                    ORDER BY 
                        number_of_customers DESC
                    LIMIT 1;
                """, (date_str,))

                max_count = cur.fetchone()


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


def chart_data():
    current_date = datetime.now().strftime("%d %m %y")
    try:
        with conn, conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    (SELECT COUNT(*) FROM visits WHERE date = '{current_date}' AND time_in IS NOT NULL) AS entered,
                    (SELECT COUNT(*) FROM visits WHERE date = '{current_date}' AND time_out IS NOT NULL) AS left,
                    (SELECT COUNT(*) FROM visits WHERE date = '{current_date}' AND time_in IS NOT NULL AND time_out IS NULL) AS instore,
                    (SELECT COUNT(DISTINCT v.customer_id) FROM visits v
                     LEFT JOIN customer c ON v.customer_id = c.id
                     WHERE v.date = '{current_date}' AND v.time_in IS NOT NULL AND c.created_at != '{current_date}') AS returning_customers,
                    (SELECT COUNT(DISTINCT v.customer_id) FROM visits v
                     LEFT JOIN customer c ON v.customer_id = c.id
                     WHERE v.date = '{current_date}' AND v.time_in IS NOT NULL AND c.created_at = '{current_date}') AS new_customers,
                    (SELECT COUNT(v.customer_id) FROM visits v
                     WHERE v.date = '{current_date}' AND v.time_in IS NOT NULL AND v.group_val = TRUE) AS groups;
            """)

            result = cur.fetchone()

            if result:
                column_names = ["entered", "left", "instore", "returning", "new", "groups"]
                result_dict = dict(zip(column_names, result))
                return result_dict
            else:
                return {"error": "No data found"}

    except (Exception, psycopg2.DatabaseError) as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    
#to get data for monthly line chart
def get_repeat_ratio_pie_data():
    try:
        with conn, conn.cursor() as cur:
            # Calculate the date range for the last 7 days
            current_date = datetime.now().strftime("%d %m %y")

            # Query to get the count of unique customers and repeat customers in the past week
            cur.execute("""
                SELECT 
                    COUNT(DISTINCT v.customer_id) AS total_customers,
                    COUNT(DISTINCT CASE WHEN c.created_at != %s THEN v.customer_id END) AS new_customers
                FROM visits v
                LEFT JOIN customer c ON v.customer_id = c.id
                WHERE v.date = %s;
            """, (current_date, current_date))

            total_customers, repeat_customers = cur.fetchone()

            # Prepare the data for the frontend
            repeat_ratio_data = {
                'total_customers': total_customers,
                'repeat_customers': repeat_customers
            }

            return repeat_ratio_data

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error fetching repeat ratio data:", error)
        return {}
    
#function for getting group Pie chart data
def get_group_pie_data():
    try:
        # Get the current date in the format %d %m %y
        current_date = datetime.now().strftime('%d %m %y')

        with conn, conn.cursor() as cur:
            # Query to get the total number of customers for the current day
            cur.execute("""
                SELECT count(customer_id) from visits WHERE date=%s
            """, (current_date,))

            total_customers = cur.fetchone()[0] or 0

            # Query to get the number of customers in groups for the current day
            cur.execute("""
                SELECT
                COUNT(CASE WHEN group_val THEN 1 END) as group_count
                FROM visits
                WHERE date = %s
            """, (current_date,))

            customers_in_groups = cur.fetchone()[0] or 0

            result = {
                'total_customers': total_customers,
                'customers_in_groups': customers_in_groups
            }

            return result

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error fetching group pie data:", error)
        return {} 

#
def get_daily_gender_bar_data():
    try:
        # Initialize a dictionary to store data for each hour
        hourly_data = defaultdict(lambda: {'Men': 0, 'Women': 0, 'Unidentified': 0})

        with conn, conn.cursor() as cur:
            # Get the current date
            current_date = datetime.now().strftime('%d %m %y')

            # Query to get customer and visit data for the current day
            cur.execute("""
                SELECT c.gender, v.time_in
                FROM customer c
                LEFT JOIN visits v ON c.id = v.customer_id AND v.date = %s
            """, (current_date,))

            rows = cur.fetchall()

            # Process the data to count Male, Female, and Unknown for each hour
            for row in rows:
                gender = row[0]
                time_in = row[1]

                # Check if time_in is not None
                if time_in:
                    if time_in == '24:00:00':
                        time_in = '00:00:00'
                    # Extract the hour from the timestamp
                    hour = datetime.strptime(time_in, '%H:%M:%S').hour

                    # Update the counts based on gender
                    if gender == 'Male':
                        hourly_data[hour]['Men'] += 1
                    elif gender == 'Female':
                        hourly_data[hour]['Women'] += 1
                    else:
                        hourly_data[hour]['Unidentified'] += 1

        # Prepare the result as a list of dictionaries
        result = [{'time': f'{hour:02}:00', **data} for hour, data in hourly_data.items()]

        return result

    except(Exception, psycopg2.DatabaseError) as error:
        print("Error fetching daily gender bar data:", error)
        return []
    

def get_engagement_bar_data():
    try:
        # Get the current date in the required format
        current_date = datetime.now().strftime('%d %m %y')

        with conn, conn.cursor() as cur:
            # Query to get customer and visit data for the current day
            cur.execute("""
                SELECT c.id, v.time_in, v.time_out
                FROM customer c
                LEFT JOIN visits v ON c.id = v.customer_id AND v.date = %s
            """, (current_date,))

            rows = cur.fetchall()

            # Calculate time spent for each customer
            time_spent_per_customer = []
            for row in rows:
                _, time_in, time_out = row
                if time_in == '24:00:00':
                        time_in = '00:00:00'
                if time_out == '24:00:00':
                        time_out = '00:00:00'
                if time_in and time_out:
                    time_in_dt = datetime.strptime(time_in, '%H:%M:%S')
                    time_out_dt = datetime.strptime(time_out, '%H:%M:%S')
                    time_spent = (time_out_dt - time_in_dt).total_seconds() / 60.0
                    time_spent_per_customer.append(time_spent)

            # Calculate average, minimum, and maximum time spent
            average_time_spent = statistics.mean(time_spent_per_customer) if time_spent_per_customer else 0
            min_time_spent = min(time_spent_per_customer) if time_spent_per_customer else 0
            max_time_spent = max(time_spent_per_customer) if time_spent_per_customer else 0

            return [
                {"metric": "Max", "value": abs(round(max_time_spent, 2))},
                {"metric": "Min", "value": abs(round(min_time_spent, 2))},
                {"metric": "Avg", "value": abs(round(average_time_spent, 2))}
            ]

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error fetching engagement bar data:", error)
        return []
    

#get data for the customers tabel
def get_customers_table_data():
    try:
        with conn, conn.cursor() as cur:
            # Query to get customer and visit data for the current date
            current_date = datetime.now().strftime('%d %m %y')
            cur.execute("""
                SELECT
                    c.id AS customer_id,
                    c.name AS customer_name,
                    MAX(CAST(v.group_val AS INTEGER))::BOOLEAN AS group,
                    COUNT(v.id) AS total_visits,
                    MAX(v.time_in) AS current_visit_time_in,
                    MAX(v.time_out) AS current_visit_time_out,
                    c.gender,
                    c.age
                FROM
                    customer c
                LEFT JOIN
                    visits v ON c.id = v.customer_id
                WHERE
                    v.date = %s
                GROUP BY
                    c.id, c.name, c.gender, c.age;
            """, (current_date,))

            rows = cur.fetchall()

            count = 0
            # Prepare the data for the frontend
            result = []
            for row in rows:
                count=count+1
                result.append({
                    'C_No': (count),
                    'name': row[1],
                    'visits': str(row[3]),
                    'gender': row[6],
                    'age': str(row[7]),
                    'group': row[2],
                    'timeIn': row[4],
                    'timeOut': row[5],
                    'id': str(row[0]),
                })

            return result

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error fetching customer table data:", error)
        return []

# create_tables()
# print(get_daily_gender_distribution())
print(get_weekly_line_data())