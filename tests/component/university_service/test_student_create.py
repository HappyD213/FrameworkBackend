from random import choice
from faker import Faker
from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestStudent:
    def test_student_create(self, university_api_utils_admin):
        Logger.info(f"### Step 1. Create group")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group)

        Logger.info(f"### Step 2. Create group")
        student = StudentRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 email=faker.email(),
                                 degree=choice([option for option in DegreeEnum]),
                                 phone=faker.numerify("+7##########"),
                                 group_id=group_response.id)
        student_response = university_service.create_student(student)

        assert student_response.group_id == group_response.id
