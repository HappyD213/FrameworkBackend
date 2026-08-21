import requests.status_codes

from services.auth.helpers.authorization_helper import AuthorizationHelper


class TestAuthContract:
    def test_user_register_success(self, auth_api_utils_anonym, data_for_success_register):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)

        response = authorization_helper.post_register(data_for_success_register)

        assert response.status_code == 201, \
            (f"Wrong status code. "
             f"Actual: {response.status_code} "
             f"Expected: 201")

    def test_user_register_conflict(self, auth_api_utils_anonym, data_for_success_register):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)
        authorization_helper.post_register(data_for_success_register)
        response = authorization_helper.post_register(data_for_success_register)

        assert response.status_code == requests.status_codes.codes.conflict, \
            (f"Wrong status code. "
             f"Actual: {response.status_code} "
             f"Expected: 409")

    def test_user_register_validation_error(self, auth_api_utils_anonym):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)

        response = authorization_helper.post_register({"username": "username"})

        assert response.status_code == requests.status_codes.codes.unprocessable, \
            (f"Wrong status code. "
             f"Actual: {response.status_code} "
             f"Expected: 422")


class TestLoginContract:
    def test_login_success(self, auth_api_utils_anonym, data_for_success_register):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)
        authorization_helper.post_register(data_for_success_register)

        response = authorization_helper.post_login({
            "username": data_for_success_register.get("username"),
            "password": data_for_success_register.get("password")
        })

        assert response.status_code == requests.status_codes.codes.ok, \
            (f"Wrong status code. "
             f"Actual: {response.status_code} "
             f"Expected: 422")

    def test_login_invalid_login_credentials(self, auth_api_utils_anonym, data_for_success_register):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)
        authorization_helper.post_register(data_for_success_register)

        username = data_for_success_register.get("username")

        response = authorization_helper.post_login({
            "username": username,
            "password": "wrong password"
        })

        assert response.status_code == requests.status_codes.codes.unauthorized, \
            (f"Wrong status code. "
             f"Actual: {response.status_code} "
             f"Expected: 422")

    def test_login_validation_error(self, auth_api_utils_anonym, data_for_success_register):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)
        authorization_helper.post_register(data_for_success_register)

        response = authorization_helper.post_login({"username": "username"})

        assert response.status_code == requests.status_codes.codes.unprocessable, \
            (f"Wrong status code. "
             f"Actual: {response.status_code} "
             f"Expected: 422")
