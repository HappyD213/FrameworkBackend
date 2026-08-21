from services.auth.models.validation_error_response import ValidationErrorResponse
from services.general.models.success_response import SuccessResponse


class TestAuthRegister:
    def test_user_created(self, auth_service_anonym, register_request):
        response = auth_service_anonym.register_user(register_request)

        assert response.detail == "User registered", \
            f"Wrong detail: {response.detail}"

    def test_user_conflict(self, registered_user_data, auth_service_anonym):
        response = auth_service_anonym.register_user(registered_user_data)

        assert response.detail == "Username is already taken"

    def test_user_validation_error(self, auth_helper_anonym):
        response = auth_helper_anonym.post_register(
            data={"username": "wrong username"}
        )

        error = ValidationErrorResponse.model_validate(response.json())

        locations = [item.loc for item in error.detail]

        assert ["body", "password"] in locations


class TestAuthLogin:
    def test_user_login(self, login_response):
        assert login_response.access_token != ""
        assert login_response.token_type == "Bearer"

    def test_invalid_login_credentials(self, registered_user_data, auth_helper_anonym):
        response = auth_helper_anonym.post_login(
            data={"username": registered_user_data.username,
                  "password": "wrong password"}
        )

        error = SuccessResponse.model_validate(response.json())

        assert error.detail == "Invalid login credentials"

    def test_validation_error(self, registered_user_data, auth_helper_anonym):
        response = auth_helper_anonym.post_login(data={"username": registered_user_data.username})

        error = ValidationErrorResponse.model_validate(response.json())

        errors = [item.loc for item in error.detail]

        assert ["body", "password"] in errors
