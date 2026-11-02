from services.university.models.grade_request import GradeRequest
from services.university.models.grade_response import GradeResponse
from services.university.university_service import UniversityService


class GradeFactory:
    def __init__(self, university_service_admin: UniversityService):
        self.api = university_service_admin
        self.created_grades = []

    def create(self, grade_request: GradeRequest) -> GradeResponse:
        grade = self.api.create_grade(grade_request)
        self.created_grades.append(grade)
        return grade

    def create_many(
            self,
            grades_requests: list[GradeRequest],
    ) -> list[GradeResponse]:
        return [
            self.create(grade_request)
            for grade_request in grades_requests
        ]

    def cleanup(self):
        for grade in self.created_grades:
            self.api.delete_grade(grade.id)
