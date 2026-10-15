from pydantic import BaseModel, ConfigDict, Field
from typing import ClassVar


class BaseGrade(BaseModel):
    MIX_GRADE_VALUE: ClassVar[int] = 0
    MAX_GRADE_VALUE: ClassVar[int] = 5

    model_config = ConfigDict(extra="forbid")

    teacher_id: int
    student_id: int
    grade: int = Field(ge=0, le=5)
