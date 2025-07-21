from faker import Faker
import requests

fake = Faker('ko_KR')

for _ in range(10):
    name = fake.name()
    birth_date = fake.date_of_birth(minimum_age=20, maximum_age=80).strftime('%Y-%m-%d')
    identifier = fake.unique.bothify(text='??######')

    payload = {
        "name": name,
        "birth_date": birth_date,
        "identifier_code": identifier
    }

    res = requests.post("http://localhost:3434/users/add", json=payload)
    print(res.json())

