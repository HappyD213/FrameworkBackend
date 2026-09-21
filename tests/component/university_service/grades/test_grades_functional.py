from services.university.helpers.grade_helper import GradeHelper
from services.university.models.grade_statistic_response import GradeStatisticResponse
from services.university.university_service import UniversityService
from tests.steps.university_steps import UniversitySteps
from utils.api_utils import ApiUtils


class TestGradeFunctional:
    def test_get_grades_statistics(self, university_api_utils_admin, register_request, group_request, student_request,
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

        params = {
            "student_id": student.id,
            "teacher_id": teacher.id,
            "group_id": group.id,
        }

        actual_stats = university_service.get_grade_statistics(
            params=params
        )

        assert actual_stats == expected_stats, (
            f"Expected: {expected_stats}, but got: {actual_stats}"
        )

    def test_get_not_authorized(self):
        headers = {"Authorization": f"Bearer dawdadad"}
        api_utils = ApiUtils(url=UniversityService.SERVICE_URL, headers=headers)

        grade_helper = GradeHelper(api_utils)
        params = {
            "student_id": 1,
            "teacher_id": 1,
            "group_id": 1,
        }

        response = grade_helper.get_grades_stats(params=params)

        expected = {"detail": "Invalid JWT token"}
        actual = response.json()

        assert actual == expected, \
            f"Expected: {expected}, but got: {actual}"

    def test_get_grades_stats_forbidden(self, university_api_utils_anonym):
        grade_helper = GradeHelper(university_api_utils_anonym)
        params = {
            "student_id": 1,
            "teacher_id": 1,
            "group_id": 1,
        }

        response = grade_helper.get_grades_stats(params=params)

        expected = {"detail": "Access denied"}
        actual = response.json()

        assert actual == expected, \
            f"Expected: {expected}, but got: {actual}"
