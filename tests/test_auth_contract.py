import requests.status_codes

from main import username, password
from services.auth.helpers.authorization_helper import AuthorizationHelper


class TestAuthContract:
    def test_user_register_success(self, auth_api_utils_anonym, register_data_success):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)

        response = authorization_helper.post_register(register_data_success)

        assert response.status_code == requests.status_codes.codes.created, \
            f"Wrong status code: {response.status_code}"

    def test_user_register_validation_error(self, auth_api_utils_anonym, register_data_error):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)

        response = authorization_helper.post_register(register_data_error)

        assert response.status_code == requests.status_codes.codes.unprocessable, \
            f"Wrong status code: {response.status_code}"

    def test_user_register_conflict(self, auth_api_utils_anonym, register_data_success):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)
        authorization_helper.post_register(register_data_success)
        response = authorization_helper.post_register(register_data_success)

        assert response.status_code == requests.status_codes.codes.conflict, \
            f"Wrong status code: {response.status_code}"


class TestLoginContract:
    def test_login_success(self, auth_api_utils_anonym, register_data_success):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)
        authorization_helper.post_register(register_data_success)

        response = authorization_helper.post_login({
            "username": register_data_success.get("username"),
            "password": register_data_success.get("password")
        })

        assert response.status_code == requests.status_codes.codes.ok, \
            f"Wrong status code: {response.status_code}"

    def test_login_invalid_login_credentials(self, auth_api_utils_anonym, register_data_success, register_data_error):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)
        authorization_helper.post_register(register_data_success)

        response = authorization_helper.post_login(register_data_error)

        assert response.status_code == requests.status_codes.codes.unauthorized, \
            f"Wrong status code: {response.status_code}"

    def test_login_validation_error(self, auth_api_utils_anonym, register_data_success, register_data_validation_error):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)
        authorization_helper.post_register(register_data_success)

        response = authorization_helper.post_login(register_data_validation_error)

        assert response.status_code == requests.status_codes.codes.unprocessable, \
            f"Wrong status code: {response.status_code}"
