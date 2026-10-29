import pytest
import os
import psycopg
from dotenv import load_dotenv

from services.auth.auth_service import AuthService
from services.auth.helpers.authorization_helper import AuthorizationHelper
from services.auth.models.login_request import LoginRequest
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils
from factories.user_factory import UserFactory
from factories.teacher_factory import TeacherFactory
from factories.student_factory import StudentFactory
from factories.group_factory import GroupFactory

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
    register_request = UserFactory.build()

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


# Test entities

@pytest.fixture(scope="function", autouse=False)
def student_in_group(university_service_admin, group):
    student_request = StudentFactory.build()
    student_request.group_id = group.id

    student = university_service_admin.student.create_student(student_request)
    try:
        yield student
    finally:
        grades_response = university_service_admin.grade.grade_helper.get_grades(
            student_id=student.id,
        )
        grades = grades_response.json()

        for grade in grades:
            university_service_admin.grade.delete_grade(grade["id"])

        university_service_admin.student.delete_student(student.id)


@pytest.fixture(scope="function", autouse=False)
def teacher(university_service_admin):
    teacher_request = TeacherFactory.build()
    teacher = university_service_admin.teacher.create_teacher(teacher_request)
    try:
        yield teacher
    finally:
        grades_response = university_service_admin.grade.grade_helper.get_grades(
            teacher_id=teacher.id
        )
        grades = grades_response.json()

        for grade in grades:
            university_service_admin.grade.delete_grade(grade["id"])

        university_service_admin.teacher.delete_teacher(teacher.id)


@pytest.fixture(scope="function", autouse=False)
def group(university_service_admin):
    group_request = GroupFactory.build()
    group = university_service_admin.group.create_group(group_request)
    try:
        yield group
    finally:
        university_service_admin.group.delete_group(group.id)
