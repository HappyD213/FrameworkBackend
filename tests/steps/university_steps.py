from services.university.models.grade_request import GradeRequest
from services.university.university_service import UniversityService


class UniversitySteps:

    def __init__(self, university_service: UniversityService):
        self.university_service = university_service

    def create_grades(
            self,
            teacher_id: int,
            student_id: int,
            grades: list[int],
    ) -> None:
        for grade in grades:
            grade_request = GradeRequest(
                teacher_id=teacher_id,
                student_id=student_id,
                grade=grade,
            )

            self.university_service.create_grade(grade_request)
