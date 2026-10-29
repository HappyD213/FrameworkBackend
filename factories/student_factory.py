from random import choice

from faker import Faker

from services.university.models.base_student import DegreeEnum
from services.university.models.student_request import StudentRequest


class StudentFactory:
    faker = Faker()

    @classmethod
    def build(cls) -> StudentRequest:
        return StudentRequest(
            first_name=cls.faker.first_name(),
            last_name=cls.faker.last_name(),
            email=cls.faker.email(),
            degree=choice(list(DegreeEnum)),
            phone=cls.faker.numerify("+7##########"),
            group_id=1,
        )
