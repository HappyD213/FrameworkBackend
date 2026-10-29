from faker import Faker

from services.university.models.group_request import GroupRequest


class GroupFactory:
    faker = Faker()

    @classmethod
    def build(cls) -> GroupRequest:
        return GroupRequest(
            name=cls.faker.name(),
        )
