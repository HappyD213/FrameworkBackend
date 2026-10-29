from random import choice

from faker import Faker

from services.university.models.base_teacher import SubjectEnum
from services.university.models.teacher_request import TeacherRequest


class TeacherFactory:
    faker = Faker()

    @classmethod
    def build(cls) -> TeacherRequest:
        return TeacherRequest(
            first_name=cls.faker.first_name(),
            last_name=cls.faker.last_name(),
            subject=choice(list(SubjectEnum)),
        )
