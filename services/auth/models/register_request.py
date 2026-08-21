from pydantic import BaseModel, ConfigDict, EmailStr, model_validator, Field


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    password: str = Field(min_length=7, max_length=100)
    password_repeat: str = Field(min_length=7, max_length=100)
    email: EmailStr

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')

        return self
