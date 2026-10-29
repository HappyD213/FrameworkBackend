from factories.group_factory import GroupFactory
from factories.student_factory import StudentFactory
from factories.teacher_factory import TeacherFactory
from services.university.models.grade_statistic_response import GradeStatisticResponse
from tests.steps.university_steps import UniversitySteps


class TestGetGradesStats:
    def test_get_grades_stats_with_combined_filters(
            self,
            university_service_admin,
            group,
            student_in_group,
            teacher,
    ):
        steps = UniversitySteps(university_service_admin)

        another_group_request = GroupFactory.build()
        another_group = university_service_admin.group.create_group(
            another_group_request
        )

        another_teacher_request = TeacherFactory.build()
        another_teacher = university_service_admin.teacher.create_teacher(
            another_teacher_request
        )

        another_student_request = StudentFactory.build()
        another_student_request.group_id = group.id
        another_student = university_service_admin.student.create_student(
            another_student_request
        )

        third_student_request = StudentFactory.build()
        third_student_request.group_id = another_group.id
        third_student = university_service_admin.student.create_student(
            third_student_request
        )

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=student_in_group.id,
            grades=[5, 4, 3],
        )

        steps.create_grades(
            teacher_id=another_teacher.id,
            student_id=student_in_group.id,
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

        actual_stats = university_service_admin.grade.get_grade_statistics(
            student_id=student_in_group.id,
            teacher_id=teacher.id,
            group_id=group.id,
        )

        assert actual_stats == expected_stats, (
            f"Expected: {expected_stats}, but got: {actual_stats}"
        )

        for student in (student_in_group, another_student, third_student):
            grades_response = university_service_admin.grade.grade_helper.get_grades(
                student_id=student.id,
            )
            for grade in grades_response.json():
                university_service_admin.grade.delete_grade(grade["id"])

        university_service_admin.student.delete_student(another_student.id)
        university_service_admin.student.delete_student(third_student.id)
        university_service_admin.teacher.delete_teacher(another_teacher.id)
        university_service_admin.group.delete_group(another_group.id)

    def test_get_grades_stats_with_teacher_and_group_filters(
            self,
            university_service_admin,
            group,
            student_in_group,
            teacher,
    ):
        steps = UniversitySteps(university_service_admin)

        another_group_request = GroupFactory.build()
        another_group = university_service_admin.group.create_group(
            another_group_request
        )
        another_teacher_request = TeacherFactory.build()
        another_teacher = university_service_admin.teacher.create_teacher(
            another_teacher_request
        )

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=student_in_group.id,
            grades=[5, 4, 3],
        )

        steps.create_grades(
            teacher_id=another_teacher.id,
            student_id=student_in_group.id,
            grades=[2, 2],
        )

        another_student_request = StudentFactory.build()
        another_student_request.group_id = another_group.id
        another_student = university_service_admin.student.create_student(
            another_student_request
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

        actual_stats = university_service_admin.grade.get_grade_statistics(
            teacher_id=teacher.id,
            group_id=group.id,
        )

        assert actual_stats == expected_stats, (
            f"Expected: {expected_stats}, but got: {actual_stats}"
        )

    def test_get_grades_stats_with_no_matching_grades(
            self,
            university_service_admin,
            group,
            teacher,
    ):
        student_request = StudentFactory.build()
        student_request.group_id = group.id

        student = university_service_admin.student.create_student(student_request)
        student_id = student.id

        university_service_admin.student.delete_student(student_id)

        expected_stats = GradeStatisticResponse(
            count=0,
            min=None,
            max=None,
            avg=None,
        )

        actual_stats = university_service_admin.grade.get_grade_statistics(
            student_id=student_id,
            teacher_id=teacher.id,
            group_id=group.id,
        )

        assert expected_stats == actual_stats, (
            f"Expected: '{expected_stats}', but got: '{actual_stats}'"
        )
