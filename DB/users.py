from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
import oracledb

router = APIRouter()
#script -> generate_fake 와 users.py 연결 
class UserCreate(BaseModel):
    name: str
    birth_date: date
    identifier_code: str

@router.post("/add")
def add_user(user: UserCreate):
    con = oracledb.connect(user="mb", password="mobridge", dsn=oracledb.makedsn("195.168.9.216", 1521, service_name="xe"))
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO USERS_DRT (name, birth_date, identifier_code)
        VALUES (:1, :2, :3)
    """, (user.name, user.birth_date, user.identifier_code))
    con.commit()
    cursor.close()
    con.close()
    return {"message": "User added"}


# api로 사용자 정보 받아올경우 uuid로 identifier_code생성하기 
# from uuid import uuid4

# app = FastAPI()
# class UserIn(BaseModel):
#     name: str
#     birth_date: datetime.date  # 또는 str로 받아도 되고

# @app.post("/users/add")
# def add_user(user: UserIn):
#     identifier_code = str(uuid4())[:12]  # 예: 'a1b2c3d4e5f6'
    
#     # 여기서 DB 저장 로직 수행
#     # 예: INSERT INTO users_drt (name, birth_date, identifier_code) VALUES (...)

#     return {
#         "msg": "사용자가 성공적으로 등록되었습니다.",
#         "identifier_code": identifier_code
#     }