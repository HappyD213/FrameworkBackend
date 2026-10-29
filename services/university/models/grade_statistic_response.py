from pydantic import BaseModel, ConfigDict, Field

MIN_GRADE = 0
MAX_GRADE = 5


class GradeStatisticResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    count: int = Field(ge=0)
    min: int | None = Field(ge=MIN_GRADE, le=MAX_GRADE)
    max: int | None = Field(ge=MIN_GRADE, le=MAX_GRADE)
    avg: float | None = Field(ge=MIN_GRADE, le=MAX_GRADE)
