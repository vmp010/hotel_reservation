from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

URL_DATABASE = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://admin:admin123@db:3306/hotel_reservation"
)
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()