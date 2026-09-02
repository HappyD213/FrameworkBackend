from services.auth.models.login_request import LoginRequest
from services.auth.models.validation_error_response import ValidationErrorResponse
from services.general.models.success_response import SuccessResponse
from utils.soft_assert import SoftAssert


class TestAuthRegister:
    def test_user_created(self, auth_service_anonym, register_request):
        response = auth_service_anonym.register_user(register_request)
        expected_detail = "User registered"

        assert response.detail == expected_detail, \
            f'Expected: "{expected_detail}", but got: "{response.detail}"'

    def test_user_conflict(self, registered_user_data, auth_service_anonym):
        response = auth_service_anonym.register_user(registered_user_data)
        expected_detail = "Username is already taken"

        assert response.detail == expected_detail, \
            f"Expected: {expected_detail}, but got: {response.detail}"

    def test_user_validation_error(self, auth_helper_anonym):
        response = auth_helper_anonym.post_register(
            data={"username": "wrong username"}
        )

        error = ValidationErrorResponse.model_validate(response.json())
        detail = error.detail[0]

        actual = (
            detail.type,
            detail.loc,
            detail.msg,
        )

        expected = (
            "missing",
            ["body", "password"],
            "Field required",
        )

        assert actual == expected, \
            f"Expected: {expected}, but got: {actual}"


class TestAuthLogin:
    def test_user_login(self, auth_service_anonym, register_request):
        auth_service_anonym.register_user(register_request=register_request)
        login_response = auth_service_anonym.login_user(LoginRequest(username=register_request.username,
                                                                     password=register_request.password))

        with SoftAssert() as soft:
            soft.check(login_response.access_token != "")
            soft.check(login_response.token_type == "Bearer")

    def test_invalid_login_credentials(self, registered_user_data, auth_helper_anonym):
        response = auth_helper_anonym.post_login(
            data={"username": registered_user_data.username,
                  "password": "wrong password"}
        )
        expected_detail = "Invalid login credentials"

        error = SuccessResponse.model_validate(response.json())

        assert error.detail == expected_detail, \
            f"Expected: {expected_detail}, but got: {error.detail}"

    def test_validation_error(self, registered_user_data, auth_helper_anonym):
        response = auth_helper_anonym.post_login(data={"username": registered_user_data.username})
        error = ValidationErrorResponse.model_validate(response.json())
        detail = error.detail[0]

        expected = (
            "missing",
            ["body", "password"],
            "Field required",
        )

        actual = (
            detail.type,
            detail.loc,
            detail.msg,
        )

        assert actual == expected, \
            f"Expected: {expected}, but got: {actual}"
