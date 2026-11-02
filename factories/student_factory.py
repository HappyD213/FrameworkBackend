from services.university.models.student_request import StudentRequest
from services.university.models.student_response import StudentResponse
from services.university.university_service import UniversityService


class StudentFactory:
    def __init__(self, university_service_admin: UniversityService):
        self.api = university_service_admin
        self.created_students = []

    def create(self, student_request: StudentRequest) -> StudentResponse:
        student = self.api.create_student(student_request)
        self.created_students.append(student)
        return student

    def create_many(self, student_requests: list[StudentRequest]) -> list[StudentResponse]:
        return [
            self.create(student_request)
            for student_request in student_requests
        ]

    def cleanup(self):
        for student in reversed(self.created_students):
            grades = self.api.get_grades(student_id=student.id)

            for grade in grades.root:
                self.api.delete_grade(grade.id)

            self.api.delete_student(student.id)
