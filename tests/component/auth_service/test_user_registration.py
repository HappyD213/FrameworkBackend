from services.auth.models.validation_error_response import ValidationErrorResponse
from factories.user_factory import UserFactory


class TestUserRegistration:
    def test_user_created(self, auth_service_anonym):
        register_request = UserFactory.build()
        response = auth_service_anonym.register_user(register_request)
        expected_detail = "User registered"

        assert response.detail == expected_detail, \
            f'Expected: "{expected_detail}", but got: "{response.detail}"'

    def test_user_conflict(self, auth_service_anonym):
        register_request = UserFactory.build()
        auth_service_anonym.register_user(register_request=register_request)

        response = auth_service_anonym.register_user(register_request=register_request)
        expected_detail = "Username is already taken"

        assert response.detail == expected_detail, \
            f"Expected: '{expected_detail}', but got: '{response.detail}'"

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
            f"Expected: '{expected}', but got: '{actual}'"
