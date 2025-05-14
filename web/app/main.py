from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at root
@app.get("/")
def read_root():
    return FileResponse("templates/index.html")

# Simulated flat entity store
fake_db: Dict[str, Dict] = {}

# Dummy data to simulate stacked outliner (but flat stored)
def seed_data():
    act_id = str(uuid.uuid4())
    scene1_id = str(uuid.uuid4())
    scene2_id = str(uuid.uuid4())
    char_id = str(uuid.uuid4())

    fake_db[act_id] = {
        "edi": act_id, "type": "Act", "name": "Act I", "description": "First act.",
        "children": [scene1_id, scene2_id], "parent": None
    }
    fake_db[scene1_id] = {
        "edi": scene1_id, "type": "Scene", "name": "Opening Scene", "description": "",
        "children": [], "parent": act_id
    }
    fake_db[scene2_id] = {
        "edi": scene2_id, "type": "Scene", "name": "Climax Scene", "description": "",
        "children": [], "parent": act_id
    }
    fake_db[char_id] = {
        "edi": char_id, "type": "Character", "name": "Tanen", "description": "Mysterious figure.",
        "children": [], "parent": None
    }

seed_data()

@app.get("/api/entities")
def get_entities():
    return list(fake_db.values())

@app.patch("/api/entity/{edi}")
def update_entity(edi: str, entity: Dict):
    if edi not in fake_db:
        raise HTTPException(status_code=404, detail="Entity not found")
    fake_db[edi] = entity
    return entity

@app.post("/api/entity")
def create_entity(entity: Dict):
    new_id = str(uuid.uuid4())
    entity["edi"] = new_id
    entity.setdefault("children", [])
    entity.setdefault("parent", None)
    fake_db[new_id] = entity
    return entity

@app.delete("/api/entity/{edi}")
def delete_entity(edi: str):
    if edi not in fake_db:
        raise HTTPException(status_code=404, detail="Entity not found")

    parent_id = fake_db[edi].get("parent")
    if parent_id and parent_id in fake_db:
        fake_db[parent_id]["children"] = [
            cid for cid in fake_db[parent_id]["children"] if cid != edi
        ]

    def delete_children(edi):
        children = fake_db[edi].get("children", [])
        for child_id in children:
            if child_id in fake_db:
                delete_children(child_id)
        del fake_db[edi]

    delete_children(edi)
    return {"status": "deleted"}

@app.post("/api/entity_order")
def update_entity_order(order: List[str]):
    return {"status": "ok"}