# core/datalayer.py

from core.models import Entity
from util.db import get_db

db = get_db()

def get_entities():
    return db.all()

def get_entity(eid):
    return db.get(eid=eid)

def add_entity(data):
    entity = Entity(**data)
    db.insert(entity.dict())
    return entity

def update_entity(eid, data):
    entity = db.get(eid=eid)
    if entity:
        entity.update(data)
        db.update(entity, eid=eid)
        return entity
    return None

def delete_entity(eid):
    db.remove(eid=eid)