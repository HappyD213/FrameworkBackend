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

    def delete_grade(self, grade_id: int) -> requests.Response:
        endpoint = f"{self.ROOT_ENDPOINT}{grade_id}/"
        response = self.api_utils.delete(endpoint)
        return response

    def get_grades(self,
                   student_id: int | None = None,
                   teacher_id: int | None = None,
                   group_id: int | None = None) \
            -> requests.Response:
        params = {
            "student_id": student_id,
            "teacher_id": teacher_id,
            "group_id": group_id,
        }
        params = {
            key: value for key, value in params.items() if value is not None
        }
        response = self.api_utils.get(
            self.ROOT_ENDPOINT,
            params=params,
        )
        return response

    def get_grades_stats(self,
                         student_id: int | None = None,
                         teacher_id: int | None = None,
                         group_id: int | None = None) \
            -> requests.Response:
        params = {
            "student_id": student_id,
            "teacher_id": teacher_id,
            "group_id": group_id,
        }
        params = {
            key: value for key, value in params.items() if value is not None
        }
        response = self.api_utils.get(
            self.STATS_ENDPOINT,
            params=params,
        )
        return response
