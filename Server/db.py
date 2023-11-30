import psycopg2
import uuid
from datetime import datetime, date
import time
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, LargeBinary, case, func, or_, extract, Date, Time, DateTime
from sqlalchemy.orm import sessionmaker, relationship, aliased
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine('postgresql://postgres:12345@localhost:5432/SSS',echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age=Column(Integer)
    encoding = Column(LargeBinary)
    created_at = Column(Date)
    modified_at = Column(Date)
    
class Visit(Base):
    __tablename__ = 'visits'
    id = Column(String,primary_key=True,default=str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey('customer.id'))
    date = Column(String)
    time_in = Column(Time, nullable=False)
    time_out = Column(Time)
    group_val = Column(Boolean)
    customer = relationship("Customer")

Base.metadata.create_all(engine)

def add_visit(id,group_val):
    try:
        date = Date.now()
        time_in = Time.now()
        new_visit = Visit(customer_id=id, date=date, time_in=time_in, group_val=group_val)
        session.add(new_visit)
        session.commit()
        print("Visit added")
    except Exception as error:
        print("Couldnt add visit ",error)
        
        
def update_visit_time_out(id):
    date= datetime.now().strftime("%d %m %y")
    time_out = datetime.now().strftime("%H:%M:%S")
    try:
        visit = session.query(Visit).filter_by(customer_id=id,date=date,time_out=None).first()
        if visit:
            visit.time_out=time_out
            session.commit()
            print("Time out updated")
        else:
            print("Couldnt find visit")
    except Exception as error:
        print("Couldnt update Exit time ",error)

