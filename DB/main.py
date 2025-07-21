# uvicorn main:app --host=0.0.0.0 --port=3434 --reload

from fastapi import FastAPI, UploadFile
from oracledb import makedsn, connect
import oracledb
from whisper_integration import transcribe_audio
from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import users  # users.py에서 라우터 불러오기
# from query_llm import generate_sql_from_text
# from database import get_hospitals
# from routing import get_best_route

dsn = oracledb.makedsn("195.168.9.70", 1521, service_name="xe")
con = oracledb.connect(user="ynchoi", password="chldPsk", dsn=dsn)


app = FastAPI()
app.include_router(users.router, prefix="/users")



# @app.get("/users")
# async def get_users():
#     cursor = con.cursor()
#     cursor.execute("SELECT user_id, name FROM users_drt")
#     rows = cursor.fetchall()
#     cursor.close()
    
#     users = []
#     for user_id, name in rows:
#         users.append({"user_id": user_id, "name": name})
    
#     return {"users": users}

@app.get("/users")
async def get_users():
    cursor = con.cursor()
    cursor.execute("""
        SELECT user_id, name, birth_date, identifier_code
        FROM users_drt
        ORDER BY user_id
    """)
    rows = cursor.fetchall()
    cursor.close()

    users = []
    for row in rows:
        users.append({
            "user_id": row[0],
            "name": row[1],
            "birth_date": row[2].strftime("%Y-%m-%d"),
            "identifier_code": row[3],
        })

    return {"users": users}


# CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users")
async def create_user(
    name: str = Form(...),
    birth_date: str = Form(...),
    identifier_code: str = Form(...)
):
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO users_drt (name, birth_date, identifier_code)
        VALUES (:name, TO_DATE(:birth_date, 'YYYY-MM-DD'), :identifier_code)
    """, {"name": name, "birth_date": birth_date, "identifier_code": identifier_code})
    con.commit()
    cursor.close()
    return {"message": "사용자 추가 완료"}



@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    cursor = con.cursor()
    cursor.execute("DELETE FROM users_drt WHERE user_id = :user_id", {"user_id": user_id})
    con.commit()
    cursor.close()
    return {"message": "사용자 삭제 완료"}

@app.get("/hospitals")
async def get_hospitals():
    cursor = con.cursor()
    cursor.execute("SELECT name, hospital_id FROM hospitals_drt")
    result = cursor.fetchall()
    cursor.close()
    return {"hospitals": [row[0] for row in result],}

@app.get("/user_visits/{user_id}")
async def get_user_visits(user_id: int):
    cursor = con.cursor()
    sql = """
    SELECT 
        u.user_id, u.name, u.birth_date, u.identifier_code,
        h.hospital_id, h.name AS hospital_name, h.address, h.latitude, h.longitude,
        v.visit_time, v.origin_lat, v.origin_lng, v.dest_lat, v.dest_lng
    FROM VISITS_DRT v
    JOIN USERS_DRT u ON v.user_id = u.user_id
    JOIN HOSPITALS_DRT h ON v.hospital_id = h.hospital_id
    WHERE u.user_id = :user_id
    ORDER BY v.visit_time DESC
    """
    cursor.execute(sql, user_id=user_id)
    rows = cursor.fetchall()
    cursor.close()

    # 결과를 리스트 딕셔너리로 변환
    visits = []
    for row in rows:
        visits.append({
            "user_id": row[0],
            "user_name": row[1],
            "birth_date": row[2].strftime("%Y-%m-%d"),
            "identifier_code": row[3],
            "hospital_id": row[4],
            "hospital_name": row[5],
            "address": row[6],
            "latitude": float(row[7]) if row[7] is not None else None,
            "longitude": float(row[8]) if row[8] is not None else None,
            "visit_time": row[9].strftime("%Y-%m-%d %H:%M:%S"),
            "origin_lat": float(row[10]) if row[10] is not None else None,
            "origin_lng": float(row[11]) if row[11] is not None else None,
            "dest_lat": float(row[12]) if row[12] is not None else None,
            "dest_lng": float(row[13]) if row[13] is not None else None,
        })

    return {"user_visits": visits}


# @app.get("/test/")
# async def test_route(audio_path: str):
#     # 1) 음성 파일 경로를 받아서 음성 인식 (예시: 로컬 경로 or URL)
#     with open(audio_path, "rb") as f:
#         audio_bytes = f.read()
#     text = transcribe_audio(audio_bytes)

#     # 2) 오라클 DB에서 간단 쿼리 (예: 병원 5개만 조회)
#     cursor = con.cursor()
#     cursor.execute("SELECT hospital_name FROM hospitals WHERE ROWNUM <= 5")
#     hospitals = [row[0] for row in cursor.fetchall()]

#     return {
#         "transcribed_text": text,
#         "hospitals_sample": hospitals
#     }


