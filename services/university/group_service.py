from services.university.helpers.group_helper import GroupHelper
from services.university.models.group_request import GroupRequest
from services.university.models.group_response import GroupResponse
from services.general.models.success_response import SuccessResponse


class GroupService:
    def __init__(self, group_helper: GroupHelper):
        self.group_helper = group_helper

    def create_group(self, group_request: GroupRequest) -> GroupResponse:
        response = self.group_helper.post_group(
            json=group_request.model_dump()
        )
        return GroupResponse(**response.json())

    def delete_group(self, group_id: int) -> SuccessResponse:
        response = self.group_helper.delete_group(group_id)
        return SuccessResponse(**response.json())
