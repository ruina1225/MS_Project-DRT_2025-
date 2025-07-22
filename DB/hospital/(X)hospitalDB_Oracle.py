import csv
import oracledb

import pandas as pd

# 원본 파일 경로
input_path = "새 폴더\\MS_Project-DRT_2025-\\DB\\hospital\\files\\l_c0903a3bc93d414e8f7b84cd33264ee0.csv"
output_path = "새 폴더\\MS_Project-DRT_2025-\\DB\\hospital\\files\\hospitals_geocoded_final.csv"

# CSV 읽기
df = pd.read_csv(input_path, encoding="utf-8-sig")

# 컬럼명 변경 (x → longitude, y → latitude)
df.rename(columns={"type":"hospital_type", "x": "longitude", "y": "latitude"}, inplace=True)

# 새 파일로 저장
df.to_csv(output_path, index=False, encoding="utf-8-sig")
print("✅ 저장 완료: hospitals_geocoded_final.csv")

# Oracle 연결 정보
dsn = oracledb.makedsn("195.168.9.70", 1521, service_name="xe")
con = oracledb.connect(user="ynchoi", password="chldPsk", dsn=dsn)
cursor = con.cursor()

# 지오코딩된 파일 경로
file_path = "새 폴더\\MS_Project-DRT_2025-\\DB\\hospital\\files\\hospitals_geocoded_final.csv"  # ← 실제 경로로 바꿔주세요

def safe_int(val):
    try:
        return int(val)
    except:
        return None

def safe_float(val):
    try:
        return float(val)
    except:
        return None

with open(file_path, newline="", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row.get("name", "").strip()
        addr = row.get("address", "").strip()
        type_ = row.get("hospital_type", "").strip()
        phone = row.get("phone", "").strip()
        room = safe_int(row.get("room_count", 0))
        bed = safe_int(row.get("bed_count", 0))
        lat = safe_float(row.get("latitude"))
        lon = safe_float(row.get("longitude"))

        if lat is not None and lon is not None:
            print(f"📍 저장: {name}, {addr} → 위도: {lat}, 경도: {lon}")
            cursor.execute("""
                INSERT INTO HOSPITALS_DRT
                (name, address, hospital_type, phone, room_count, bed_count, latitude, longitude)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
            """, (name, addr, type_, phone, room, bed, lat, lon))
        else:
            print(f"⚠️ 위경도 없음 → 생략: {name}")

    con.commit()

cursor.close()
con.close()
print("✅ DB 저장 완료")