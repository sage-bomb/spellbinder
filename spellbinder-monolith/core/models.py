# core/models.py

from pydantic import BaseModel
from typing import Optional

class Entity(BaseModel):
    eid: str
    type: str
    name: str
    summary: Optional[str] = ""