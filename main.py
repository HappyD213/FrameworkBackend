import requests
from faker import Faker
from random import choice

from utils.api_utils import ApiUtils

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

auth_api_utils = ApiUtils(AUTH_URL)
response = auth_api_utils.post(REGISTER_ENDPOINT,
                               data={"username": username,
                                     "password": password,
                                     "password_repeat": password,
                                     "email": faker.email()})

response = auth_api_utils.post(LOGIN_ENDPOINT,
                               data={"username": username,
                                     "password": password})
access_token = response.json()["access_token"]

admin_auth_api_utils = ApiUtils(AUTH_URL, headers={"Authorization": f"Bearer {access_token}"})
response = admin_auth_api_utils.get(ME_ENDPOINT)

admin_university_api_utils = ApiUtils(UNIVERSITY_URL, headers={"Authorization": f"Bearer {access_token}"})
response = admin_university_api_utils.post(GROUPS_ENDPOINT,
                                           json={"name": faker.name()})

response = admin_university_api_utils.post(STUDENTS_ENDPOINT,
                                           json={"first_name": faker.first_name(),
                                                 "last_name": faker.last_name(),
                                                 "email": faker.email(),
                                                 "degree": choice(["Associate",
                                                                   "Bachelor",
                                                                   "Master",
                                                                   "Doctorate", ]),
                                                 "phone": faker.numerify("+7##########"),
                                                 "group_id": response.json()["id"]})
