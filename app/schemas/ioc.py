from pydantic import BaseModel
from datetime import datetime


class IOCResponse(BaseModel):
    id: int
    type: str
    value: str
    source: str
    last_seen: datetime | None