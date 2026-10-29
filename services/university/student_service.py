from services.general.models.success_response import SuccessResponse
from services.university.helpers.student_helper import StudentHelper
from services.university.models.student_request import StudentRequest
from services.university.models.student_response import StudentResponse


class StudentService:
    def __init__(self, student_helper: StudentHelper):
        self.student_helper = student_helper

    def create_student(self, student_request: StudentRequest) -> StudentResponse:
        response = self.student_helper.post_student(
            json=student_request.model_dump()
        )
        return StudentResponse(**response.json())

    def delete_student(self, student_id: int) -> SuccessResponse:
        response = self.student_helper.delete_student(student_id)
        return SuccessResponse(**response.json())
