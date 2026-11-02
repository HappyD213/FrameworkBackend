from pydantic import RootModel

from services.university.models.grade_response import GradeResponse


class GradesListResponse(RootModel[list[GradeResponse]]):
    pass
