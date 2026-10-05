import requests

from services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    STATS_ENDPOINT = f"{ENDPOINT_PREFIX}/stats/"

    def post_grade(self, data: dict) -> requests.Response:
        return self.api_utils.post(
            self.ROOT_ENDPOINT,
            data=data,
        )

    def get_grades(self, student_id: int, teacher_id: int, group_id: int) -> requests.Response:
        params = {
            "student_id": student_id,
            "teacher_id": teacher_id,
            "group_id": group_id,
        }
        response = self.api_utils.get(
            self.ROOT_ENDPOINT,
            params=params,
        )
        return response

    def get_grades_stats(self, student_id: int, teacher_id: int, group_id: int) -> requests.Response:
        params = {
            "student_id": student_id,
            "teacher_id": teacher_id,
            "group_id": group_id,
        }
        response = self.api_utils.get(
            self.STATS_ENDPOINT,
            params=params,
        )
        return response
