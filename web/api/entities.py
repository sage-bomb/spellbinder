# web/api/entities.py

from fastapi import APIRouter, HTTPException
from core import datalayer

router = APIRouter(prefix="/api/entities")

@router.get("/")
def get_all_entities():
    return datalayer.get_entities()

@router.get("/{eid}")
def get_entity(eid: str):
    entity = datalayer.get_entity(eid)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity

@router.post("/")
def add_entity(entity: dict):
    return datalayer.add_entity(entity)

@router.put("/{eid}")
def update_entity(eid: str, entity: dict):
    updated = datalayer.update_entity(eid, entity)
    if not updated:
        raise HTTPException(status_code=404, detail="Entity not found")
    return updated

@router.delete("/{eid}")
def delete_entity(eid: str):
    datalayer.delete_entity(eid)
    return {"success": True}