from services.university.helpers.grade_helper import GradeHelper
from tests.steps.university_steps import UniversitySteps


class TestGetGradesOptional:
    def test_get_grades_stats_without_teacher_id(
            self,
            university_api_utils_admin,
            university_service_admin,
            group,
            student_in_group,
            teacher,
    ):
        steps = UniversitySteps(university_service_admin)
        grade_helper = GradeHelper(university_api_utils_admin)

        grades = [5, 4, 3]

        steps.create_grades(
            teacher_id=teacher.id,
            student_id=student_in_group.id,
            grades=grades,
        )

        response = grade_helper.get_grades_stats(
            student_id=student_in_group.id,
            group_id=group.id,
        )

        assert response.status_code == 200
        assert response.json() == {
            "count": 3,
            "min": 3,
            "max": 5,
            "avg": 4.0,
        }
