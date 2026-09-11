from pydantic import BaseModel, ConfigDict


class GetGradesRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    student_id: int
    teacher_id: int
    group_id: int
