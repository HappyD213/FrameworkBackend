from faker import Faker

from services.auth.models.register_request import RegisterRequest


class UserFactory:
    faker = Faker()

    @classmethod
    def build(cls) -> RegisterRequest:
        password = cls.faker.password(
            length=30,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )

        return RegisterRequest(
            username=cls.faker.user_name(),
            password=password,
            password_repeat=password,
            email=cls.faker.email(),
        )
