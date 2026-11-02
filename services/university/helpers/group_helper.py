import requests

from services.general.helpers.base_helper import BaseHelper


class GroupHelper(BaseHelper):
    ENDPOINT_PREFIX = "/groups"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def post_group(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def delete_group(self, group_id: int | None = None) -> requests.Response:
        endpoint = f"{self.ROOT_ENDPOINT}{group_id}/"
        response = self.api_utils.delete(endpoint)
        return response
