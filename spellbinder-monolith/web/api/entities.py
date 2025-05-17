# === web/api/entities.py ===

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from spellbinder_util.db import TinyInterface
from tinydb import Query
import uuid

# Set up router
router = APIRouter(prefix="/entities", tags=["entities"])

# Connect to the centralized TinyDB table
db = TinyInterface(table_name="entities")

# Pydantic model for validation
class Entity(BaseModel):
    edi: Optional[str] = None
    type: str
    name: str
    description: Optional[str] = None

# === CRUD routes ===

@router.get("/", response_model=List[Entity])
def list_entities():
    return db.all()   # 👈 FIX THIS


@router.get("/{edi}", response_model=Entity)
def get_entity(edi: str):
    result = db.get(edi=edi)
    if not result:
        raise HTTPException(status_code=404, detail="Entity not found")
    return result[0]

@router.post("/", response_model=Entity)
def create_entity(entity: Entity):
    entity_data = entity.dict(exclude_unset=True)
    entity_data["edi"] = str(uuid.uuid4())  # Server-generated eid
    db.add(entity_data)
    return entity_data

@router.put("/{edi}", response_model=Entity)
def update_entity(edi: str, entity: Entity):
    q = Query()
    entity_data = entity.dict(exclude_unset=True)
    entity_data["edi"] = edi  # Enforce consistency
    if db.table.update(entity_data, q.edi == edi) == 0:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity_data

@router.delete("/{edi}")
def delete_entity(edi: str):
    q = Query()
    if db.table.remove(q.edi == edi) == 0:
        raise HTTPException(status_code=404, detail="Entity not found")
    return {"detail": "Entity deleted"}
