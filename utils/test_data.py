from random import choice

from faker import Faker

from services.auth.models.register_request import RegisterRequest
from services.university.models.base_student import DegreeEnum
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.models.group_request import GroupRequest
from services.university.models.grade_request import GradeRequest
from services.university.models.base_teacher import SubjectEnum


class TestData:
    faker = Faker()

    @classmethod
    def register_request(cls) -> RegisterRequest:
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

    @classmethod
    def student_request(cls) -> StudentRequest:
        return StudentRequest(
            first_name=cls.faker.first_name(),
            last_name=cls.faker.last_name(),
            email=cls.faker.email(),
            degree=choice(list(DegreeEnum)),
            phone=cls.faker.numerify("+7##########"),
            group_id=1
        )

    @classmethod
    def teacher_request(cls) -> TeacherRequest:
        return TeacherRequest(
            first_name=cls.faker.first_name(),
            last_name=cls.faker.last_name(),
            subject=choice(list(SubjectEnum)),
        )

    @classmethod
    def group_request(cls) -> GroupRequest:
        return GroupRequest(
            name=cls.faker.word(),
        )

    @classmethod
    def grade_request(
            cls,
            teacher_id: int,
            student_id: int,
    ) -> GradeRequest:
        return GradeRequest(
            teacher_id=teacher_id,
            student_id=student_id,
            grade=cls.faker.random_int(min=0, max=5),
        )
