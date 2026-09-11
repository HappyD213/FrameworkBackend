from services.auth.helpers.authorization_helper import AuthorizationHelper
from faker import Faker

faker = Faker()


class TestAuthContract:
    def test_user_register_success(self, auth_api_utils_anonym):
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

        response = authorization_helper.post_register(register_data)
        expected_code = 201

        assert response.status_code == expected_code, \
            (f"Wrong status code. "
             f"Actual: {response.status_code} "
             f"Expected: {expected_code}")

    def test_user_register_conflict(self, auth_api_utils_anonym):
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
        response = authorization_helper.post_register(register_data)
        expected_code = 409

        assert response.status_code == expected_code, \
            (f"Wrong status code. "
             f"Actual: {response.status_code} "
             f"Expected: {expected_code}")

    def test_user_register_validation_error(self, auth_api_utils_anonym):
        authorization_helper = AuthorizationHelper(auth_api_utils_anonym)

        response = authorization_helper.post_register({"username": "username"})
        expected_code = 422

        assert response.status_code == expected_code, \
            (f"Wrong status code. "
             f"Actual: {response.status_code} "
             f"Expected: {expected_code}")
