from pydantic import BaseModel, Field, field_validator


class TaskTestAddRequestDto(BaseModel):
    test_code: str
    is_hidden: bool = Field(False)
    order_index: int = Field(0, ge=0)
    task_id: int | None = Field(None)

    @field_validator("test_code", mode="before")
    @classmethod
    def strip_whitespaces(cls, v: str) -> str:
        return v.strip()

    @field_validator("test_code")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v:
            raise ValueError(
                "Поле не может быть пустым или состоять только из пробелов"
            )
        return v


class TaskTestPutRequestDto(BaseModel):
    test_code: str
    is_hidden: bool
    order_index: int = Field(ge=0)
    task_id: int | None = Field(None)

    @field_validator("test_code", mode="before")
    @classmethod
    def strip_whitespaces(cls, v: str) -> str:
        return v.strip()

    @field_validator("test_code")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v:
            raise ValueError(
                "Поле не может быть пустым или состоять только из пробелов"
            )
        return v


class TaskTestPatchRequestDto(BaseModel):
    test_code: str | None = None
    is_hidden: bool | None = None
    order_index: int | None = Field(None, ge=0)
    task_id: int | None = Field(None)

    @field_validator("test_code", mode="before")
    @classmethod
    def strip_whitespaces(cls, v: str | None) -> str | None:
        if v is not None:
            return v.strip() or None
        return v

    @field_validator("test_code")
    @classmethod
    def not_blank(cls, v: str | None) -> str | None:
        if v is not None and not v:
            raise ValueError(
                "Поле не может быть пустым или состоять только из пробелов"
            )
        return v


class TaskTestDto(BaseModel):
    id: int
    task_id: int
    test_code: str
    is_hidden: bool = Field(False)
    order_index: int = Field(0)
