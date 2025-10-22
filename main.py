from fastapi import FastAPI, Depends
from database import engine, Session
from database import Room
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"} 

#驗光好菜          

#管理每次 API 請求的資料庫連線
def get_session(): 
    with Session(engine) as session:
        yield session

@app.post("/rooms/") #新增，提交
def create_Room(room:Room,session:Session=Depends(get_session)):
    session.add(room)
    session.commit() #提交
    session.refresh(room)
    return room #回傳json檔

@app.get("/rooms/") #查詢
def read_rooms(session:Session=Depends(get_session)):
    rooms=session.query(Room).all()
    return rooms