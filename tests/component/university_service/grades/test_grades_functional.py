from services.university.helpers.grade_helper import GradeHelper
from services.university.models.grade_statistic_response import GradeStatisticResponse
from services.university.university_service import UniversityService
from tests.steps.university_steps import UniversitySteps
from utils.api_utils import ApiUtils


class TestGradeFunctional:
    def test_get_not_authorized(self):
        headers = {"Authorization": f"Bearer dawdadad"}
        api_utils = ApiUtils(url=UniversityService.SERVICE_URL, headers=headers)

        grade_helper = GradeHelper(api_utils)

        response = grade_helper.get_grades_stats(student_id=1, teacher_id=1, group_id=1)

        expected = {"detail": "Invalid JWT token"}
        actual = response.json()

        assert actual == expected, \
            f"Expected: {expected}, but got: {actual}"

    def test_get_grades_stats_forbidden(self, university_api_utils_anonym):
        grade_helper = GradeHelper(university_api_utils_anonym)

        response = grade_helper.get_grades_stats(student_id=1, teacher_id=1, group_id=1)

        expected = {"detail": "Access denied"}
        actual = response.json()

        assert actual == expected, \
            f"Expected: {expected}, but got: {actual}"
