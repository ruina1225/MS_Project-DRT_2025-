from faker import Faker
import requests


fake = Faker('ko_KR')

for _ in range(30):
    name = fake.name()
    birth_date = fake.date_of_birth(minimum_age=1, maximum_age=80).strftime('%Y-%m-%d')
    identifier = fake.unique.bothify(text='??######')

    payload = {
        "name": name,
        "birth_date": birth_date,
        "identifier_code": identifier
    }

    try:
        res = requests.post("http://localhost:3434/users/add", json=payload)
        print(res.json())
    except requests.exceptions.ConnectionError:
        print("❌ 서버가 실행 중이 아닙니다. FastAPI를 먼저 실행하세요.")
        break
