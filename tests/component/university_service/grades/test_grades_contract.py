from services.university.helpers.grade_helper import GradeHelper
from services.university.university_service import UniversityService
from tests.steps.university_steps import UniversitySteps
from utils.api_utils import ApiUtils


class TestGradeContract:
    def test_get_grades_stats_success(
            self,
            university_api_utils_admin,
            group,
            student_in_group,
            teacher,
    ):
        university_service = UniversityService(university_api_utils_admin)

        steps = UniversitySteps(university_service)
        grades = [5, 4, 3]

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=student_in_group.id,
            grades=grades,
        )

        grade_helper = GradeHelper(university_api_utils_admin)
        response = grade_helper.get_grades_stats(
            student_id=student_in_group.id,
            teacher_id=teacher.id,
            group_id=group.id,
        )

        expected_code = 200

        assert response.status_code == expected_code, \
            f"Expected: '{expected_code}' but got '{response.status_code}'"

    def test_get_grades_stats_not_authorized(self):
        headers = {"Authorization": f"Bearer dawdadad"}
        api_utils = ApiUtils(url=UniversityService.SERVICE_URL, headers=headers)
        grade_helper = GradeHelper(api_utils)
        response = grade_helper.get_grades_stats(
            student_id=1,
            teacher_id=1,
            group_id=1,
        )

        expected_code = 401
        assert response.status_code == expected_code, \
            f"Expected: '{expected_code}', but got: '{response.status_code}'"

    def test_get_grades_stats_forbidden(
            self,
            university_api_utils_anonym,
    ):
        grade_helper = GradeHelper(university_api_utils_anonym)
        response = grade_helper.get_grades_stats(
            student_id=1,
            teacher_id=1,
            group_id=1,
        )

        expected_code = 403

        assert response.status_code == expected_code, \
            f"Expected: '{expected_code}', but got: '{response.status_code}'"

    def test_get_grades_stats_validation_error(
            self,
            university_api_utils_admin,
    ):
        grade_helper = GradeHelper(university_api_utils_admin)
        response = grade_helper.get_grades_stats(student_id="dwadadada")

        expected_code = 422

        assert response.status_code == expected_code, \
            f"Expected: '{expected_code}', but got: '{response.status_code}'"
