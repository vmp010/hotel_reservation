from sqlmodel import Field, SQLModel, create_engine, Session

class Room(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    available: bool 

DATABASE_URL = "sqlite:///./rooms.db"
engine=create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)