from services.university.models.grade_statistic_response import GradeStatisticResponse
from tests.steps.university_steps import UniversitySteps
import pytest


class TestGetGradesStats:
    def test_get_grades_stats_with_combined_filters(
            self,
            university_service_admin,
            register_request,
            group_request,
            student_request,
            teacher_request,
    ):
        group = university_service_admin.create_group(group_request)
        student_request.group_id = group.id

        student = university_service_admin.create_student(student_request)
        teacher = university_service_admin.create_teacher(teacher_request)

        steps = UniversitySteps(university_service_admin)
        grades = [5, 4, 3]
        steps.create_grades(
            teacher_id=teacher.id,
            student_id=student.id,
            grades=grades,
        )

        expected_stats = GradeStatisticResponse(
            count=len(grades),
            min=min(grades),
            max=max(grades),
            avg=sum(grades) / len(grades),
        )

        actual_stats = university_service_admin.get_grade_statistics(
            student_id=student.id,
            teacher_id=teacher.id,
            group_id=group.id)

        assert actual_stats == expected_stats, (
            f"Expected: {expected_stats}, but got: {actual_stats}"
        )

    def test_get_grades_stats_with_teacher_and_group_filters(
            self,
            university_service_admin,
            register_request,
            group_request,
            student_request,
            teacher_request,
    ):
        group = university_service_admin.create_group(group_request)
        student_request.group_id = group.id

        student = university_service_admin.create_student(student_request)
        teacher = university_service_admin.create_teacher(teacher_request)

        steps = UniversitySteps(university_service_admin)
        grades = [5, 4, 3]

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=student.id,
            grades=grades,
        )

        expected_stats = GradeStatisticResponse(
            count=len(grades),
            min=min(grades),
            max=max(grades),
            avg=sum(grades) / len(grades),
        )

        actual_stats = university_service_admin.get_grade_statistics(
            teacher_id=teacher.id,
            group_id=group.id,
        )

        assert actual_stats == expected_stats, (
            f"Expected: {expected_stats}, but got: {actual_stats}"
        )

    def test_get_grades_stats_with_no_matching_grades(
            self,
            university_service_admin,
    ):
        expected_stats = GradeStatisticResponse(
            count=0,
            min=None,
            max=None,
            avg=None,
        )
        actual_stats = university_service_admin.get_grade_statistics(
            student_id=3525252,
            teacher_id=3525253,
            group_id=3525254
        )
        assert expected_stats == actual_stats, \
            f"Expected: '{expected_stats}', but got: '{actual_stats}'"
