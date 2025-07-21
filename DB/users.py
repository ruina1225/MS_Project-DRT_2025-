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
    con = oracledb.connect(user="ynchoi", password="chldPsk", dsn=oracledb.makedsn("195.168.9.70", 1521, service_name="xe"))
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO USERS_DRT (name, birth_date, identifier_code)
        VALUES (:1, :2, :3)
    """, (user.name, user.birth_date, user.identifier_code))
    con.commit()
    cursor.close()
    con.close()
    return {"message": "User added"}