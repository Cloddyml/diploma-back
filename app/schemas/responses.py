from pydantic import BaseModel

SUCCESS_RESPONSE = {"status": "OK"}


class ErrorResponse(BaseModel):
    detail: str


class StatusResponse(BaseModel):
    status: str = "OK"
