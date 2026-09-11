from services.auth.helpers.authorization_helper import AuthorizationHelper
from faker import Faker

faker = Faker()


class TestLoginContract:
    def test_login_success(self, auth_api_utils_anonym):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)
        password = faker.password(
            length=30,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )

        register_data = {
            "username": faker.user_name(),
            "password": password,
            "password_repeat": password,
            "email": faker.email(),
        }
        authorization_helper.post_register(register_data)

        response = authorization_helper.post_login({
            "username": register_data.get("username"),
            "password": register_data.get("password")
        })
        expected_code = 200

        assert response.status_code == expected_code, \
            (f"Wrong status code. "
             f"Actual: {response.status_code} "
             f"Expected: {expected_code}")

    def test_login_invalid_login_credentials(self, auth_api_utils_anonym):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)
        password = faker.password(
            length=30,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )

        register_data = {
            "username": faker.user_name(),
            "password": password,
            "password_repeat": password,
            "email": faker.email(),
        }
        authorization_helper.post_register(register_data)

        username = register_data.get("username")

        response = authorization_helper.post_login({
            "username": username,
            "password": "wrong password"
        })
        expected_code = 401

        assert response.status_code == expected_code, \
            (f"Wrong status code. "
             f"Actual: {response.status_code} "
             f"Expected: {expected_code}")

    def test_login_validation_error(self, auth_api_utils_anonym):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)
        password = faker.password(
            length=30,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )

        register_data = {
            "username": faker.user_name(),
            "password": password,
            "password_repeat": password,
            "email": faker.email(),
        }
        authorization_helper.post_register(register_data)

        response = authorization_helper.post_login({"username": "username"})
        expected_code = 422

        assert response.status_code == expected_code, \
            (f"Wrong status code. "
             f"Actual: {response.status_code} "
             f"Expected: {expected_code}")
