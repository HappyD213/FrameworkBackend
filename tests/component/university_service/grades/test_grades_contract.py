from services.university.helpers.grade_helper import GradeHelper
from services.university.university_service import UniversityService
from tests.steps.university_steps import UniversitySteps
from utils.api_utils import ApiUtils


class TestGradeContract:
    def test_get_grades_stats_success(self, university_api_utils_admin, register_request, group_request,
                                      student_request, teacher_request):
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

        params = {
            "student_id": student.id,
            "teacher_id": teacher.id,
            "group_id": group.id,
        }

        grade_helper = GradeHelper(university_api_utils_admin)
        response = grade_helper.get_grades_stats(params=params)

        expected_code = 200

        assert response.status_code == expected_code, \
            f"Expected: '{expected_code}' but got '{response.status_code}'"

    def test_get_grades_stats_not_authorized(self):
        headers = {"Authorization": f"Bearer dawdadad"}
        api_utils = ApiUtils(url=UniversityService.SERVICE_URL, headers=headers)

        grade_helper = GradeHelper(api_utils)
        params = {
            "student_id": 1,
            "teacher_id": 1,
            "group_id": 1,
        }

        response = grade_helper.get_grades_stats(params=params)

        expected_code = 401

        assert response.status_code == expected_code, \
            f"Expected: '{expected_code}', but got: '{response.status_code}'"

    def test_get_grades_stats_forbidden(self, university_api_utils_anonym):
        grade_helper = GradeHelper(university_api_utils_anonym)
        params = {
            "student_id": 1,
            "teacher_id": 1,
            "group_id": 1,
        }

        response = grade_helper.get_grades_stats(params=params)

        expected_code = 403

        assert response.status_code == expected_code, \
            f"Expected: '{expected_code}', but got: '{response.status_code}'"

    def test_get_grades_stats_validation_error(self, university_api_utils_admin):
        grade_helper = GradeHelper(university_api_utils_admin)
        params = {
            "teacher_id": 3,
        }

        response = grade_helper.get_grades_stats(params=params)

        expected_code = 422

        assert response.status_code == expected_code, \
            f"Expected: '{expected_code}', but got: '{response.status_code}'"
