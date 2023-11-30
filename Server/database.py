import psycopg2
import uuid
from datetime import datetime, date, timedelta
from statistics import mean
from collections import defaultdict
import face_recognition
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, LargeBinary, case, desc, distinct, func, or_, extract, Date, Time, DateTime, and_, text 
from sqlalchemy.orm import sessionmaker, relationship, aliased
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import UUID
from dateutil.relativedelta import relativedelta


engine = create_engine('postgresql://postgres:12345@localhost:5432/SSS',echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age=Column(Integer)
    encoding = Column(LargeBinary)
    created_at = Column(Date)
    modified_at = Column(Date)
    
class Visit(Base):
    __tablename__ = 'visits'
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    customer_id = Column(UUID, ForeignKey('customer.id'))
    day = Column(Date)
    time_in = Column(Time, nullable=False)
    time_out = Column(Time)
    group_val = Column(Boolean)
    customer = relationship("Customer")

Base.metadata.create_all(engine)

def get_all_encodings():
    try:
        all_customers = session.query(Customer.id, Customer.encoding).all()

        if all_customers:
            return [(customer_id, np.frombuffer(encoding, dtype=np.float64)) for customer_id, encoding in all_customers]
            # Convert the bytes back to the 1D NumPy array
        else:
            return []
    except Exception as error:
        print("Error fetching encodings:", error)
        return []
  
  
def customer_exist(encoding , group_val, gender):
    if encoding is None:
        print("Picture unclear")
        return
    
    all_encodings = get_all_encodings()
    
    if not all_encodings:
        print("No encodings in DB")
        add_customer(gender, encoding, group_val)
        return
    
    for id, db_encoding in all_encodings:
        results = face_recognition.compare_faces([encoding], db_encoding)
        if results[0]:
            #Check if person isnt already in store
            result = check_visit(id)
            if result:
                #Add new visit for customer
                add_visit(id, group_val)
            else:
                print("Visit already added")
                return
            return
    
    add_customer(gender, encoding, group_val)
        

def add_customer(gender, encoding, group_val):
    name= "Unknown Customer"
    created_at = date.today()
    modified_at = date.today()
    encoding_bytes = encoding.tobytes()
    try:
        new_customer = Customer(name=name, gender=gender,age=None,encoding=encoding_bytes, created_at=created_at, modified_at= modified_at )
        session.add(new_customer)
        session.commit()
        print("Customer added")
        add_visit(new_customer.id, group_val)
    except Exception as error:
        print("Couldnt add customer ",error)
    


def add_visit(id,group_val):
    try:
        day = date.today()
        time_in = datetime.now().time()
        new_visit = Visit(customer_id=id, day=day, time_in=time_in, group_val=group_val)
        session.add(new_visit)
        session.commit()
        print("Visit added")
    except Exception as error:
        print("Couldnt add visit ",error)


#To find out if customer isnt still inside the store
def check_visit(id):
    try:
        visit = session.query(Visit).filter_by(customer_id=id, time_out=None).first()
        if visit:
            print("Customer already inside")
            return False
        else:
            return True
    except Exception as error:
        print("Couldnt find visit ",error)


def update_visit_time_out(id):
    day = date.today()
    time_out = datetime.now.time()
    try:
        visit = session.query(Visit).filter_by(customer_id=id,day=day,time_out=None).first()
        if visit:
            visit.time_out=time_out
            session.commit()
            print("Time out updated")
        else:
            print("Couldnt find visit")
    except Exception as error:
        print("Couldnt update Exit time ",error)
    
    

# #FRONT-END CHARTS
def get_daily_gender_distribution():
    current_date = date.today()
    try:
        result = (
            session.query(
                func.count().filter(Customer.gender == 'Male').label('male_count'),
                func.count().filter(Customer.gender == 'Female').label('female_count'),
                func.count().filter(Customer.gender == 'Unknown').label('unknown_count'),
                func.count().label('total_count')
            )
            .filter(Customer.id.in_(
                session.query(Visit.customer_id)
                .filter(Visit.day == current_date)
            ))
            .first()
        )

        if result:
            male_count = result.male_count or 0
            print(male_count)
            female_count = result.female_count or 0
            print(female_count)
            unknown_count = result.unknown_count or 0
            total_count = result.total_count or 1  # Avoid division by zero

            # Calculate percentages
            male_percentage = (male_count / total_count) * 100
            female_percentage = (female_count / total_count) * 100
            print("Unknown: ", unknown_count)
            unknown_percentage = (unknown_count / total_count) * 100
            print(unknown_percentage)

            return {
                'male_percentage': round(male_percentage, 2),
                'female_percentage': round(female_percentage, 2),
                'unknown_percentage': round(unknown_percentage, 2),
            }

    except SQLAlchemyError as error:
        print("Error fetching gender distribution:", error)
        return {
            'male_percentage': 0,
            'female_percentage': 0,
            'unknown_percentage': 0,
        }

#get Daily Line CHart data
def get_daily_line_data():
    try:
        current_date = date.today()

        current_datetime = datetime.now()
        # Calculate the current hour
        current_hour = current_datetime.hour

        start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

        # Generate a list of hours from the current hour to 0
        hours_to_query = range(current_hour, -1, -1)

        # Prepare the result dictionary for the specified hours
        result = {f'{hour:02}:00-{(hour + 1) % 24:02}:00' if hour != 23 else '23:00-00:00': {'Enter': 0, 'Exit': 0, 'Min': 0, 'Max': 0} for hour in hours_to_query}
        # Alias for visits table to join with itself for entry and exit counts

        # Query to get entered counts on an hourly basis for the current date
        entry_counts = (
            session.query(
                extract('hour', Visit.time_in).label('hour_of_entry'),
                func.count().label('number_of_customers')
            )
            .filter(Visit.day == current_date, Visit.time_in.is_not(None))
            .group_by(extract('hour', Visit.time_in))
            .order_by(extract('hour', Visit.time_in))
        ).all()

        for row in entry_counts:
            hour_value = row[0]
            next_hour_value = (hour_value + 1) % 24
            hour_interval = f'{hour_value:02}:00-{next_hour_value:02}:00' if hour_value != 23 else '23:00-00:00'
            
            # If the value is None or 0, set it to 0 in the result dictionary
            result[hour_interval]['Enter'] = row[1] if row[1] is not None and row[1] != 0 else 0


        # Query to get exited counts on an hourly basis for the current date
        exit_counts = (
            session.query(
                extract('hour', Visit.time_out).label('hour_of_exit'),
                func.count().label('number_of_customers')
            )
            .filter(Visit.day == current_date, Visit.time_out.is_not(None))
            .group_by(extract('hour', Visit.time_out))
            .order_by(extract('hour', Visit.time_out))
        ).all()

        for row in exit_counts:
            hour_value = row[0]
            next_hour_value = (hour_value + 1) % 24
            hour_interval = f'{hour_value:02}:00-{next_hour_value:02}:00' if hour_value != 23 else '23:00-00:00'
            
            # If the value is None or 0, set it to 0 in the result dictionary
            result[hour_interval]['Exit'] = row[1] if row[1] is not None and row[1] != 0 else 0


        return result

    except Exception as error:
        print("Error fetching line data:", error)
        return {}


#weekly line chart data
def get_weekly_line_data():
    try:
        # Calculate the date range for the last 7 days
        end_date = date.today()
        start_date = end_date - timedelta(days=6)

        # Initialize the data dictionary
        weekly_data = {'Entered': [], 'Left': [], 'Min': [], 'Max': []}

        # Loop through each day in the week
        for single_date in (start_date + timedelta(n) for n in range(7)):
            date_str = single_date

            # Get the count of people who entered and left the shop on the current day
            entered = (
                session.query(func.count(Visit.customer_id))
                .filter(Visit.day == single_date)
                .scalar()
            )

            left = (
                session.query(func.count(Visit.customer_id))
                .filter(and_(Visit.day == single_date, Visit.time_out.isnot(None)))
                .scalar()
            )

            # Get the min count of people present in the shop at one time on the current day
            subquery_min = (
                session.query(
                    func.count().label('number_of_customers')
                )
                .filter(Visit.day == single_date)
                .group_by(extract('hour', Visit.time_in))
                .order_by('number_of_customers')
                .limit(1)
                .subquery()
            )

            min_count = session.query(func.coalesce(func.min(subquery_min.c.number_of_customers), 0)).scalar()

            # Get the max count of people present in the shop at one time on the current day
            subquery_max = (
                session.query(
                    func.count().label('number_of_customers')
                )
                .filter(Visit.day == single_date)
                .group_by(extract('hour', Visit.time_in))
                .order_by(desc('number_of_customers'))
                .limit(1)
                .subquery()
            )

            max_count = session.query(func.coalesce(func.max(subquery_max.c.number_of_customers), 0)).scalar()


            # Append the data to the weekly_data dictionary
            weekly_data['Entered'].append(entered)
            weekly_data['Left'].append(left)
            weekly_data['Min'].append(min_count)
            weekly_data['Max'].append(max_count)

        return weekly_data

    except Exception as error:
        print("Error fetching weekly line data:", error)
        return {}

#Get monthly line data
def get_monthly_line_data():
    
    current_date = datetime.now().replace(day=1)

    try:
        # Calculate the date range for the previous month
        first_day_of_current_month = current_date.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

        # Initialize the data dictionary
        monthly_data = {'Entered': [], 'Left': [], 'Min': [], 'Max': []}

        # Loop through each month from the current month to the first month of the year
        current_month = first_day_of_current_month
        while current_month >= first_day_of_previous_month.replace(month=1):
            # Get the count of people who entered and left the shop for the current month
            entered = session.query(func.count(Visit.customer_id)).filter(
                extract('month', Visit.day) == current_month.month,
                extract('year', Visit.day) == current_month.year,
            ).scalar()

            left = session.query(func.count(Visit.customer_id)).filter(
                extract('month', Visit.day) == current_month.month,
                extract('year', Visit.day) == current_month.year,
                Visit.time_out.isnot(None),
            ).scalar()

            min_subquery = session.query(
                extract('day', Visit.day).label('day'),
                func.count(Visit.customer_id).label('customer_count')
            ).filter(
                extract('month', Visit.day) == current_month.month,
                extract('year', Visit.day) == current_month.year,
            ).group_by(
                extract('day', Visit.day)
            ).order_by(
                text('customer_count')
            ).limit(1).subquery()

            min_count = int(session.query(func.sum(min_subquery.c.customer_count)).scalar() or 0)

            # Get the max count of people present in the shop at one time for each day of the month
            max_subquery = session.query(
                extract('day', Visit.day).label('day'),
                func.count(Visit.customer_id).label('customer_count')
            ).filter(
                extract('month', Visit.day) == current_month.month,
                extract('year', Visit.day) == current_month.year,
            ).group_by(
                extract('day', Visit.day)
            ).order_by(
                text('customer_count DESC')
            ).limit(1).subquery()

            max_count = int(session.query(func.sum(max_subquery.c.customer_count)).scalar() or 0)

            # Append the data to the monthly_data dictionary
            monthly_data['Entered'].append(entered or 0)
            monthly_data['Left'].append(left or 0)
            monthly_data['Min'].append(min_count or 0)
            monthly_data['Max'].append(max_count or 0)

            # Move to the previous month
            current_month = current_month - relativedelta(months=1)
            
        for key in monthly_data:
            monthly_data[key] = monthly_data[key][::-1]


        return monthly_data

    except Exception as error:
        print("Error fetching monthly line data:", error)
        return {}



def chart_data():
    current_date = date.today()

    try:
        # Get counts using SQLAlchemy ORM
        entered = (
            session.query(func.count())
            .filter(Visit.day == current_date, Visit.time_in.isnot(None))
            .scalar()
        )

        left = (
            session.query(func.count())
            .filter(Visit.day == current_date, Visit.time_out.isnot(None))
            .scalar()
        )

        instore = (
            session.query(func.count())
            .filter(Visit.day == current_date, Visit.time_in.isnot(None), Visit.time_out.is_(None))
            .scalar()
        )

        returning_customers = (
            session.query(func.count(distinct(Visit.customer_id)))
            .join(Customer, Visit.customer_id == Customer.id)
            .filter(Visit.day == current_date, Visit.time_in.isnot(None), Customer.created_at != current_date)
            .scalar()
        )

        new_customers = (
            session.query(func.count(distinct(Visit.customer_id)))
            .join(Customer, Visit.customer_id == Customer.id)
            .filter(Visit.day == current_date, Visit.time_in.isnot(None), Customer.created_at == current_date)
            .scalar()
        )

        groups = (
            session.query(func.count())
            .filter(Visit.day == current_date, Visit.time_in.isnot(None), Visit.group_val.is_(True))
            .scalar()
        )

        result_dict = {
            "entered": entered,
            "left": left,
            "instore": instore,
            "returning": returning_customers,
            "new": new_customers,
            "groups": groups
        }

        return result_dict

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    
    
# get repeat ratio
def get_repeat_ratio_pie_data():
    try:
        # Calculate the date range for the last 7 days
        current_date = date.today()

        # Query to get the count of unique customers and repeat customers in the past week
        total_customers_result= (
            session.query(
                func.count(distinct(Visit.customer_id)).label('total_customers')
            )
            .filter(Visit.day == current_date)
            .first()
        )
        
        repeat_customers_result= (
            session.query(
                func.count(distinct(Visit.customer_id)).label('repeat_customers')
            )
            .join(Customer, Visit.customer_id == Customer.id)
            .filter(and_(Visit.day == current_date, Customer.created_at != current_date))
            .first()
        )
        

        total_customers = total_customers_result[0] if total_customers_result else 0
        repeat_customers = repeat_customers_result[0] if repeat_customers_result else 0


        # Prepare the data for the frontend
        repeat_ratio_data = {
            'total_customers': total_customers,
            'repeat_customers': repeat_customers
        }

        return repeat_ratio_data

    except Exception as error:
        print("Error fetching repeat ratio data:", error)
        return {}
    
    
# #function for getting group Pie chart data
def get_group_pie_data():
    try:
        # Get the current date in the format %d %m %y
        current_date = date.today()

        # Query to get the total number of customers for the current day
        total_customer_result = (
            session.query(
                func.count(Visit.customer_id)
            )
            .filter(Visit.day == current_date)
            .first()
        )

        group_result = (
            session.query(
                func.count(Visit.customer_id)
            )
            .filter(and_(Visit.day == current_date, Visit.group_val == True))
            .first()
        )
        
        total_customers = total_customer_result[0] if total_customer_result else 0
        customers_in_groups = group_result[0] if group_result else 0

        result = {
            'total_customers': total_customers,
            'customers_in_groups': customers_in_groups
        }

        return result

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error fetching group pie data:", error)
        return {} 


def get_daily_gender_bar_data():
    try:
        # Initialize a dictionary to store data for each hour
        hourly_data = defaultdict(lambda: {'Men': 0, 'Women': 0, 'Unknown': 0})

        # Get the current date and time
        current_datetime = datetime.now()

        # Calculate the start of the current day
        start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

        # Generate a list of all hours up to the current hour
        hours_to_query = [start_of_day + timedelta(hours=i) for i in range(current_datetime.hour, current_datetime.hour - 6, -1) if i >= 0]

        # Query to get customer and visit data for the current hour and 5 previous hours
        visits = aliased(Visit)
        stmt = (
            session.query(
                extract('hour', visits.time_in).label('hour_of_entry'),
                Customer.gender,
                func.count().label('gender_count')
            )
            .outerjoin(visits, (Customer.id == visits.customer_id) & (visits.day == start_of_day.date()))
            .filter(visits.day == current_datetime.date())
            .filter(extract('hour', visits.time_in).in_([hour.hour for hour in hours_to_query]))
            .group_by(extract('hour', visits.time_in), Customer.gender)
        )

        # Execute the statement
        rows = stmt.all()

        # Process the data to count Male, Female, and Unknown for each hour
        for row in rows:
            hour = row[0]
            gender = row[1]
            count = row[2]

            # Update the counts based on gender
            if gender == 'Male':
                hourly_data[hour]['Men'] += count
            elif gender == 'Female':
                hourly_data[hour]['Women'] += count
            else:
                hourly_data[hour]['Unknown'] += count
                
        for hour in hours_to_query:
            if hour.hour not in hourly_data:
                hourly_data[hour.hour] = {'Men': 0, 'Women': 0, 'Unknown': 0}

        # Prepare the result as a list of dictionaries
        result = [{'time': f'{hour:02}:00', **data} for hour, data in sorted(hourly_data.items())]

        return result

    except Exception as error:
        print("Error fetching hourly gender data:", error)
        return []



def get_engagement_bar_data():
    try:
        # Get the current date
        current_date = date.today()

        # Query to get customer and visit data for the current day
        visits = aliased(Visit)
        stmt = (
            session.query(Customer.id, visits.time_in, visits.time_out)
            .outerjoin(visits, (Customer.id == visits.customer_id) & (visits.day == current_date))
            .filter(visits.time_out.isnot(None))
        )

        rows = stmt.all()

        # Calculate time spent for each customer in minutes
        time_spent_per_customer = []
        for row in rows:
            customer_id, time_in, time_out = row
            if time_in and time_out:
                time_in_minutes = time_in.hour * 60 + time_in.minute + time_in.second / 60.0
                time_out_minutes = time_out.hour * 60 + time_out.minute + time_out.second / 60.0
                time_spent = time_out_minutes - time_in_minutes
                time_spent_per_customer.append(time_spent)


        # Calculate average, minimum, and maximum time spent
        average_time_spent = mean(time_spent_per_customer) if time_spent_per_customer else 0
        min_time_spent = min(time_spent_per_customer) if time_spent_per_customer else 0
        max_time_spent = max(time_spent_per_customer) if time_spent_per_customer else 0
        
        return [
            {"metric": "Max", "value": abs(max_time_spent)},
            {"metric": "Min", "value": abs(min_time_spent)},
            {"metric": "Avg", "value": abs(average_time_spent)}
        ]

    except Exception as error:
        print("Error fetching engagement bar data:", error)
        return []
    

# #get data for the customers tabel
def get_customers_table_data():
    try:
        # Query to get customer and visit data for the current date
        current_date = date.today()
        
        query = (
            session.query(
                Customer.id.label('customer_id'),
                Customer.name.label('customer_name'),
                func.max(Visit.group_val.cast(Integer)).label('group'),
                func.count(Visit.id).label('total_visits'),
                func.max(Visit.time_in).label('current_visit_time_in'),
                func.max(Visit.time_out).label('current_visit_time_out'),
                Customer.gender,
                Customer.age
            )
            .outerjoin(Visit, Customer.id == Visit.customer_id)
            .filter(Visit.day == current_date)
            .group_by(Customer.id)
        )

        rows = query.all()

        count = 0
        # Prepare the data for the frontend
        result = []
        for row in rows:
            count += 1
            result.append({
                'C_No': count,
                'name': row.customer_name,
                'visits': str(row.total_visits),
                'gender': row.gender,
                'age': str(row.age),
                'group': bool(row.group),
                'timeIn': row.current_visit_time_in.strftime('%H:%M:%S') if row.current_visit_time_in else None,
                'timeOut': row.current_visit_time_out.strftime('%H:%M:%S') if row.current_visit_time_out else None,
                'id': str(row.customer_id),
            })

        return result

    except Exception as error:
        print("Error fetching customer table data:", error)
        return []


# print("eng data: ",get_engagement_bar_data())
# print(get_monthly_line_data())

print(get_daily_line_data())