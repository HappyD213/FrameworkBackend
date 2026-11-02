from services.university.models.teacher_request import TeacherRequest
from services.university.models.teacher_response import TeacherResponse
from services.university.university_service import UniversityService


class TeacherFactory:
    def __init__(self, university_service_admin: UniversityService):
        self.api = university_service_admin
        self.created_teachers: list[TeacherResponse] = []

    def create(self, teacher_request: TeacherRequest) -> TeacherResponse:
        teacher = self.api.create_teacher(teacher_request)
        self.created_teachers.append(teacher)
        return teacher

    def create_many(
            self,
            teacher_requests: list[TeacherRequest],
    ) -> list[TeacherResponse]:
        return [
            self.create(teacher_request)
            for teacher_request in teacher_requests
        ]

    def cleanup(self):
        for teacher in reversed(self.created_teachers):
            grades = self.api.get_grades(teacher_id=teacher.id)

            for grade in grades.root:
                self.api.delete_grade(grade.id)

            self.api.delete_teacher(teacher.id)
