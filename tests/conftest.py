import pytest
import os
import psycopg
from dotenv import load_dotenv

from services.auth.auth_service import AuthService
from services.auth.helpers.authorization_helper import AuthorizationHelper
from services.auth.models.login_request import LoginRequest
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils
from factories.teacher_factory import TeacherFactory
from factories.student_factory import StudentFactory
from factories.group_factory import GroupFactory
from utils.test_data import TestData

load_dotenv()


# API Utils — without authentication

@pytest.fixture(scope="session", autouse=False)
def db_connection():
    connection = psycopg.connect(
        host="localhost",
        port=5431,
        dbname=os.getenv("POSTGRES_DB_UNIVERSITY"),
        user=os.getenv("POSTGRES_USER"),
        password=os.environ["POSTGRES_PASSWORD"],
    )

    try:
        yield connection
    finally:
        connection.close()


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_anonym():
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_anonym():
    api_utils = ApiUtils(url=AuthService.SERVICE_URL)
    return api_utils


# Helpers — without authentication

@pytest.fixture(scope="function", autouse=False)
def auth_helper_anonym(auth_api_utils_anonym):
    return AuthorizationHelper(auth_api_utils_anonym)


# Services — without authentication

@pytest.fixture(scope="function", autouse=False)
def auth_service_anonym(auth_api_utils_anonym):
    auth_service = AuthService(auth_api_utils_anonym)
    return auth_service


# Authentication

@pytest.fixture(scope="function", autouse=False)
def access_token(auth_service_anonym):
    register_request = TestData.register_request()

    auth_service_anonym.register_user(
        register_request=register_request
    )

    username = register_request.username
    password = register_request.password

    login_response = auth_service_anonym.login_user(login_request=LoginRequest(username=username,
                                                                               password=password))

    return login_response.access_token


# API Utils — with authentication

@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_admin(access_token):
    api_utils = ApiUtils(
        url=AuthService.SERVICE_URL,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_admin(access_token):
    api_utils = ApiUtils(
        url=UniversityService.SERVICE_URL,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return api_utils


# Services — with authentication

@pytest.fixture(scope="function", autouse=False)
def university_service_admin(university_api_utils_admin):
    university_service = UniversityService(university_api_utils_admin)
    return university_service


# Factories

@pytest.fixture(scope="function")
def student_factory(university_service_admin):
    factory = StudentFactory(university_service_admin)
    try:
        yield factory
    finally:
        factory.cleanup()


@pytest.fixture(scope="function")
def teacher_factory(university_service_admin):
    factory = TeacherFactory(university_service_admin)
    try:
        yield factory
    finally:
        factory.cleanup()


@pytest.fixture(scope="function")
def group_factory(university_service_admin):
    factory = GroupFactory(university_service_admin)
    try:
        yield factory
    finally:
        factory.cleanup()
