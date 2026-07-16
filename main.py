import requests
from faker import Faker
from random import choice

AUTH_URL = "http://127.0.0.1:8000"
UNIVERSITY_URL = "http://127.0.0.1:8001"

REGISTER_ENDPOINT = "/auth/register/"
LOGIN_ENDPOINT = "/auth/login/"
ME_ENDPOINT = "/users/me/"

GROUPS_ENDPOINT = "/groups/"
STUDENTS_ENDPOINT = "/students/"

faker = Faker()
username = faker.user_name()
password = "aZ!$<>123" + faker.word()
response = requests.post(AUTH_URL + REGISTER_ENDPOINT,
                         data={"username": username,
                               "password": password,
                               "password_repeat": password,
                               "email": faker.email()})

response = requests.post(AUTH_URL + LOGIN_ENDPOINT,
                         data={"username": username,
                               "password": password})

access_token = response.json()["access_token"]
response = requests.get(AUTH_URL + ME_ENDPOINT,
                        headers={"Authorization": f"Bearer {access_token}"})

response = requests.post(UNIVERSITY_URL + GROUPS_ENDPOINT,
                         json={"name": faker.name()},
                         headers={"Authorization": f"Bearer {access_token}"})

response = requests.post(UNIVERSITY_URL + STUDENTS_ENDPOINT,
                         json={"first_name": faker.first_name(),
                               "last_name": faker.last_name(),
                               "email": faker.email(),
                               "degree": choice(["Associate",
                                                 "Bachelor",
                                                 "Master",
                                                 "Doctorate", ]),
                               "phone": faker.numerify("+7##########"),
                               "group_id": response.json()["id"]},
                         headers={"Authorization": f"Bearer {access_token}"})
