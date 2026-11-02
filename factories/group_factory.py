from services.university.models.group_request import GroupRequest
from services.university.models.group_response import GroupResponse
from services.university.university_service import UniversityService


class GroupFactory:
    def __init__(self, university_service_admin: UniversityService):
        self.api = university_service_admin
        self.created_groups = []

    def create(self, group_request: GroupRequest) -> GroupResponse:
        group = self.api.create_group(group_request)
        self.created_groups.append(group)
        return group

    def create_many(self, groups_requests: list[GroupRequest]) -> list[GroupResponse]:
        return [
            self.create(group_request)
            for group_request in groups_requests
        ]

    def cleanup(self):
        for group in self.created_groups:
            self.api.delete_group(group.id)
