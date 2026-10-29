from services.general.models.success_response import SuccessResponse
from services.university.helpers.grade_helper import GradeHelper
from services.university.models.grade_request import GradeRequest
from services.university.models.grade_response import GradeResponse
from services.university.models.grade_statistic_response import GradeStatisticResponse
from services.university.models.grades_list_response import GradesListResponse


class GradeService:
    def __init__(self, grade_helper: GradeHelper):
        self.grade_helper = grade_helper

    def create_grade(self, grade_request: GradeRequest) -> GradeResponse:
        response = self.grade_helper.post_grade(
            data=grade_request.model_dump()
        )
        return GradeResponse.model_validate(response.json())

    def delete_grade(self, grade_id: int) -> SuccessResponse:
        response = self.grade_helper.delete_grade(grade_id)
        return SuccessResponse(**response.json())

    def get_grades(
            self,
            student_id: int | None = None,
            teacher_id: int | None = None,
            group_id: int | None = None
    ) -> GradesListResponse:
        filters = {
            "student_id": student_id,
            "teacher_id": teacher_id,
            "group_id": group_id,
        }
        filters = {
            key: value for key, value in filters.items() if value is not None
        }
        response = self.grade_helper.get_grades(**filters)
        return GradesListResponse.model_validate(response.json())

    def get_grade_statistics(
            self,
            student_id: int | None = None,
            teacher_id: int | None = None,
            group_id: int | None = None,
    ) -> GradeStatisticResponse:
        filters = {
            "student_id": student_id,
            "teacher_id": teacher_id,
            "group_id": group_id,
        }
        filters = {
            key: value for key, value in filters.items() if value is not None
        }
        response = self.grade_helper.get_grades_stats(**filters)
        return GradeStatisticResponse.model_validate(response.json())
