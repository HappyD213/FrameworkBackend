from services.university.models.get_grades_request import GetGradesRequest
from services.university.models.grade_statistic_response import GradeStatisticResponse
from services.university.university_service import UniversityService
from tests.steps.university_steps import UniversitySteps


def test_get_grades_statistics(university_api_utils_admin, register_request, group_request, student_request,
                               teacher_request):
    university_service = UniversityService(university_api_utils_admin)
    group = university_service.create_group(group_request)
    student_request.group_id = group.id

    student = university_service.create_student(student_request)
    teacher = university_service.create_teacher(teacher_request)

    steps = UniversitySteps(university_service)

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

    actual_stats = university_service.get_grade_statistics(
        request=GetGradesRequest(
            student_id=student.id,
            teacher_id=teacher.id,
            group_id=group.id,
        )
    )

    assert actual_stats == expected_stats, (
        f"Expected: {expected_stats}, but got: {actual_stats}"
    )
