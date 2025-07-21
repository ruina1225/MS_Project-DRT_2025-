import requests
import oracledb
from geopy.geocoders import Nominatim
from time import sleep

# Oracle 연결
dsn = oracledb.makedsn("195.168.9.70", 1521, service_name="xe")
con = oracledb.connect(user="ynchoi", password="chldPsk", dsn=dsn)
cursor = con.cursor()

# # 🔁 기존 데이터 삭제
# cursor.execute("DELETE FROM HOSPITAL_DEPTS_DRT")
# cursor.execute("DELETE FROM HOSPITALS_DRT")
# con.commit()
# print("🗑 기존 병원 데이터 삭제 완료")

# 지오코딩 도구
geolocator = Nominatim(user_agent="hospital-loader")

# 안전하게 숫자 변환
def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0

def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

# API 요청
url = "https://api.odcloud.kr/api/3045143/v1/uddi:a121e723-7ae7-44df-ba6f-86eb09a633e7"
params = {
    "page": 1,
    "perPage": 1000,
    "returnType": "JSON",
    "serviceKey": "xZq/MBrLVT7SuSCy9Xidjni6dYR2XKaI/FPpv+IA8llCj4GN8NIuwL03CuMTvGNK1nakZ7DwO/LFJS+22qGJew=="
}

response = requests.get(url, params=params)
result = response.json()
hospitals = [item for item in result.get("data", []) if item.get("병원종별", "").strip() == "종합병원"]

# 병원 정보 저장
for item in hospitals:
    name = item.get("의료기관명", "").strip()
    addr = item.get("소재지", "").strip()
    type_ = item.get("병원종별", "").strip()
    tel = item.get("연락처", "").strip()
    room = safe_int(item.get("병실수"))
    bed = safe_int(item.get("병상수"))

    try:
        location = geolocator.geocode(addr)
        lat = safe_float(location.latitude) if location else None
        lon = safe_float(location.longitude) if location else None
        sleep(1)
    except Exception as e:
        print(f"[Geocoding 오류] 주소: {addr}, 오류: {e}")
        lat, lon = None, None

    if lat is not None and lon is not None:
        print(f"[삽입] {name}, {addr}, 위도: {lat}, 경도: {lon}")
        cursor.execute("""
            INSERT INTO HOSPITALS_DRT 
            (name, address, hospital_type, phone, room_count, bed_count, latitude, longitude)
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
        """, (name, addr, type_, tel, room, bed, lat, lon))
        con.commit()
    else:
        print(f"❌ 위경도 없음 → 저장 생략: {name}, 주소: {addr}")

cursor.close()
con.close()
print("✅ 종합병원 정보 저장 완료")
