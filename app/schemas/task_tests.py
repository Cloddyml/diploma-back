from pydantic import BaseModel, Field


class TaskTestDto(BaseModel):
    id: int
    task_id: int
    test_code: str
    is_hidden: bool = Field(False)
    order_index: int = Field(0)
