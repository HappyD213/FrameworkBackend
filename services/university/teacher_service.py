from services.general.models.success_response import SuccessResponse
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.teacher_request import TeacherRequest
from services.university.models.teacher_response import TeacherResponse


class TeacherService:
    def __init__(self, teacher_helper: TeacherHelper):
        self.teacher_helper = teacher_helper

    def create_teacher(
            self, teacher_request: TeacherRequest
    ) -> TeacherResponse:
        response = self.teacher_helper.post_teacher(
            json=teacher_request.model_dump()
        )
        return TeacherResponse(**response.json())

    def delete_teacher(self, teacher_id: int) -> SuccessResponse:
        response = self.teacher_helper.delete_teacher(teacher_id)
        return SuccessResponse(**response.json())
