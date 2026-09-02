import pytest

from faker import Faker
from services.auth.auth_service import AuthService
from services.auth.helpers.authorization_helper import AuthorizationHelper
from services.auth.models.login_request import LoginRequest
from services.auth.models.register_request import RegisterRequest
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils

faker = Faker()


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_anonym():
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_anonym():
    api_utils = ApiUtils(url=AuthService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def auth_service_anonym(auth_api_utils_anonym):
    auth_service = AuthService(auth_api_utils_anonym)
    return auth_service


@pytest.fixture(scope="function", autouse=False)
def auth_helper_anonym(auth_api_utils_anonym):
    return AuthorizationHelper(auth_api_utils_anonym)


@pytest.fixture(scope="function", autouse=False)
def register_request():
    password = faker.password(
        length=30,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True,
    )

    return RegisterRequest(
        username=faker.user_name(),
        password=password,
        password_repeat=password,
        email=faker.email(),
    )


@pytest.fixture(scope="function", autouse=False)
def registered_user_data(auth_service_anonym, register_request):
    auth_service_anonym.register_user(register_request=register_request)

    return register_request


@pytest.fixture(scope="function", autouse=False)
def access_token(auth_service_anonym, registered_user_data):
    username = registered_user_data.username
    password = registered_user_data.password

    login_response = auth_service_anonym.login_user(login_request=LoginRequest(username=username,
                                                                               password=password))
    return login_response.access_token


@pytest.fixture(scope="function", autouse=False)
def login_response(auth_service_anonym, registered_user_data):
    username = registered_user_data.username
    password = registered_user_data.password

    login_response = auth_service_anonym.login_user(login_request=LoginRequest(username=username,
                                                                               password=password))
    return login_response


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_admin(access_token):
    api_utils = ApiUtils(url=AuthService.SERVICE_URL, headers={"Authorization": f"Bearer {access_token}"})
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_admin(access_token):
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL, headers={"Authorization": f"Bearer {access_token}"})
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def data_for_success_register():
    password = faker.password(
        length=30,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True,
    )
    return {
        "username": faker.user_name(),
        "password": password,
        "password_repeat": password,
        "email": faker.email(),
    }
