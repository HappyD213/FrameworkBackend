from pydantic import BaseModel, ConfigDict, EmailStr, model_validator, Field
from typing import ClassVar


class RegisterRequest(BaseModel):
    MIN_PASSWORD_LENGTH: ClassVar[int] = 7
    MAX_PASSWORD_LENGTH: ClassVar[int] = 100

    model_config = ConfigDict(extra="forbid")

    username: str
    password: str = Field(
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH
    )
    password_repeat: str = Field(
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH
    )
    email: EmailStr

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')

        return self
