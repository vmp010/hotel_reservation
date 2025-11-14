from sqlalchemy import  create_engine,event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine
import os

URL_DATABASE = os.getenv(
    "DATABASE_URL",
    "sqlite:///./hotel_reservation.db"
)
engine = create_engine(URL_DATABASE)


# 啟用 SQLite 外鍵約束
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    if "sqlite" in URL_DATABASE:
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()