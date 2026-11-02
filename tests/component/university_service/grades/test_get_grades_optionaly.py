from services.university.models.grade_statistic_response import GradeStatisticResponse
from tests.steps.university_steps import UniversitySteps
from utils.test_data import TestData


class TestGetGradesOptional:

    def test_get_grades_stats_without_teacher_id(
            self,
            university_service_admin,
            group_factory,
            student_factory,
            teacher_factory,
    ):
        steps = UniversitySteps(university_service_admin)

        group = group_factory.create(
            group_request=TestData.group_request()
        )

        student_request = TestData.student_request()
        student_request.group_id = group.id
        student = student_factory.create(
            student_request=student_request
        )

        teacher = teacher_factory.create(
            teacher_request=TestData.teacher_request()
        )

        grades = [5, 4, 3]

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=student.id,
            grades=grades,
        )

        expected_stats = GradeStatisticResponse(
            count=3,
            min=3,
            max=5,
            avg=4.0,
        )

        actual_stats = university_service_admin.get_grade_statistics(
            student_id=student.id,
            group_id=group.id,
        )

        assert actual_stats == expected_stats, (
            f"Expected: {expected_stats}, but got: {actual_stats}"
        )
