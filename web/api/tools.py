# web/api/tools.py

from fastapi import APIRouter
from tools import bookshaper, compile

router = APIRouter(prefix="/api/tools")

@router.post("/bookshaper")
def run_bookshaper():
    return bookshaper.run()

@router.post("/compile")
def run_compile():
    return compile.run()