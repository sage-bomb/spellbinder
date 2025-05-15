# web/api/state.py

from fastapi import APIRouter
from util import db

router = APIRouter(prefix="/api/state")

@router.get("/")
def get_state():
    return db.get_state()

@router.post("/")
def update_state(state: dict):
    db.set_state(state)
    return {"success": True}