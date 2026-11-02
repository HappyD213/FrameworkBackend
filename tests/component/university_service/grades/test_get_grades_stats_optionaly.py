from services.university.models.grade_statistic_response import GradeStatisticResponse
from tests.steps.university_steps import UniversitySteps
from utils.test_data import TestData


class TestGetGradesStats:

    def test_get_grades_stats_with_student_filter(
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

        another_student_request = TestData.student_request()
        another_student_request.group_id = group.id
        another_student = student_factory.create(
            student_request=another_student_request
        )

        teacher = teacher_factory.create(
            teacher_request=TestData.teacher_request()
        )

        another_teacher = teacher_factory.create(
            teacher_request=TestData.teacher_request()
        )

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=student.id,
            grades=[5, 4, 3],
        )

        steps.create_grades(
            teacher_id=another_teacher.id,
            student_id=student.id,
            grades=[2, 2],
        )

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=another_student.id,
            grades=[1, 1],
        )

        expected_stats = GradeStatisticResponse(
            count=5,
            min=2,
            max=5,
            avg=3.2,
        )

        actual_stats = university_service_admin.get_grade_statistics(
            student_id=student.id,
        )

        assert actual_stats == expected_stats, (
            f"Expected: {expected_stats}, but got: {actual_stats}"
        )

    def test_get_grades_stats_with_teacher_filter(
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

        another_teacher = teacher_factory.create(
            teacher_request=TestData.teacher_request()
        )

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=student.id,
            grades=[5, 4, 3],
        )

        steps.create_grades(
            teacher_id=another_teacher.id,
            student_id=student.id,
            grades=[2, 2],
        )

        expected_stats = GradeStatisticResponse(
            count=3,
            min=3,
            max=5,
            avg=4.0,
        )

        actual_stats = university_service_admin.get_grade_statistics(
            teacher_id=teacher.id,
        )

        assert actual_stats == expected_stats, (
            f"Expected: {expected_stats}, but got: {actual_stats}"
        )

    def test_get_grades_stats_with_group_filter(
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

        another_group = group_factory.create(
            group_request=TestData.group_request()
        )

        student_request = TestData.student_request()
        student_request.group_id = group.id
        student = student_factory.create(
            student_request=student_request
        )

        another_student_request = TestData.student_request()
        another_student_request.group_id = another_group.id
        another_student = student_factory.create(
            student_request=another_student_request
        )

        teacher = teacher_factory.create(
            teacher_request=TestData.teacher_request()
        )

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=student.id,
            grades=[5, 4, 3],
        )

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=another_student.id,
            grades=[1, 1],
        )

        expected_stats = GradeStatisticResponse(
            count=3,
            min=3,
            max=5,
            avg=4.0,
        )

        actual_stats = university_service_admin.get_grade_statistics(
            group_id=group.id,
        )

        assert actual_stats == expected_stats, (
            f"Expected: {expected_stats}, but got: {actual_stats}"
        )

    def test_get_grades_stats_with_combined_filters(
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

        another_group = group_factory.create(
            group_request=TestData.group_request()
        )

        another_teacher = teacher_factory.create(
            teacher_request=TestData.teacher_request()
        )

        another_student_request = TestData.student_request()
        another_student_request.group_id = group.id
        another_student = student_factory.create(
            student_request=another_student_request
        )

        third_student_request = TestData.student_request()
        third_student_request.group_id = another_group.id
        third_student = student_factory.create(
            student_request=third_student_request
        )

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=student.id,
            grades=[5, 4, 3],
        )

        steps.create_grades(
            teacher_id=another_teacher.id,
            student_id=student.id,
            grades=[2, 2],
        )

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=another_student.id,
            grades=[1, 1],
        )

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=third_student.id,
            grades=[2, 1],
        )

        expected_stats = GradeStatisticResponse(
            count=3,
            min=3,
            max=5,
            avg=4.0,
        )

        actual_stats = university_service_admin.get_grade_statistics(
            student_id=student.id,
            teacher_id=teacher.id,
            group_id=group.id,
        )

        assert actual_stats == expected_stats, (
            f"Expected: {expected_stats}, but got: {actual_stats}"
        )

    def test_get_grades_stats_with_teacher_and_group_filters(
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

        another_group = group_factory.create(
            group_request=TestData.group_request()
        )

        another_teacher = teacher_factory.create(
            teacher_request=TestData.teacher_request()
        )

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=student.id,
            grades=[5, 4, 3],
        )

        steps.create_grades(
            teacher_id=another_teacher.id,
            student_id=student.id,
            grades=[2, 2],
        )

        another_student_request = TestData.student_request()
        another_student_request.group_id = another_group.id
        another_student = student_factory.create(
            student_request=another_student_request
        )

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=another_student.id,
            grades=[1, 1],
        )

        expected_stats = GradeStatisticResponse(
            count=3,
            min=3,
            max=5,
            avg=4.0,
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
            group_factory,
            student_factory,
            teacher_factory,
    ):
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

        expected_stats = GradeStatisticResponse(
            count=0,
            min=None,
            max=None,
            avg=None,
        )

        actual_stats = university_service_admin.get_grade_statistics(
            student_id=student.id,
            teacher_id=teacher.id,
            group_id=group.id,
        )

        assert expected_stats == actual_stats, (
            f"Expected: {expected_stats}, but got: {actual_stats}"
        )