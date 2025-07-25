import uuid
import os
# import oracledb

original_filename = "새 폴더/MS_Project-DRT_2025-/DB/user/user_img/스크린샷 2025-07-25 113043.png"
extension = os.path.splitext(original_filename)[1]  # .jpg
uuid_filename = f"{uuid.uuid4()}{extension}"

print(uuid_filename)  # 예: 3fa85f64-5717-4562-b3fc-2c963f66afa6.jpg



# # Oracle 연결 정보
# dsn = oracledb.makedsn("195.168.9.216", 1521, service_name="xe")
# con = oracledb.connect(user="mb", password="mobridge", dsn=dsn)
# cursor = con.cursor()

# user_id = 1
# image_path = "user_face.jpg"

# # 이미지 파일을 바이너리로 읽기
# with open(image_path, "rb") as f:
#     photo_blob = f.read()

# # BLOB 저장
# cursor.execute("""
#     INSERT INTO USER_PHOTOS_DRT (user_id, photo_blob)
#     VALUES (:1, :2)
# """, (user_id, photo_blob))

# con.commit()
# cursor.close()
# con.close()

# print("✅ 사용자 얼굴사진이 성공적으로 업로드되었습니다.")
