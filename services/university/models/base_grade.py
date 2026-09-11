from pydantic import BaseModel, ConfigDict


class BaseGrade(BaseModel):
    model_config = ConfigDict(extra="forbid")

    teacher_id: int
    student_id: int
    grade: int
