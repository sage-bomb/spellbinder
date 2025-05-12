from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import os


from util.embedding_store import EmbeddingStore
from util.vector_search import VectorSearchIndex
from util.embedding import get_embedding, load_embedding, save_embedding, delete_embedding
from testing.test_embed_search import embed_new_documents, load_existing_embeddings
from fastapi import Form
from util.file_registry import add_tag, remove_tag
from fastapi.responses import RedirectResponse
from util.file_registry import get_file_by_filename


from util.file_registry import (
    list_files as list_registered_files,
    add_tag,
    remove_tag,
    get_file_by_eid
)

EMBED_FOLDER = "../test_docs/test_search"  # <-- or configurable

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

eid_to_text = {}
index = VectorSearchIndex()
store = EmbeddingStore()


@app.get("/favicon.ico", include_in_schema=False)
async def redirect_favicon():
    return RedirectResponse(url="/static/favicon.ico")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search")
async def search(query: str = Form(...), top_k: int = Form(5)):
    global index, eid_to_text
    query_vec = np.array(get_embedding(query), dtype=np.float32)
    results = index.search(query_vec, top_k=top_k)
    response = []

    for r in results:
        entry = eid_to_text.get(r["eid"], {"file": "unknown", "text": ""})

        tags = []
        record = get_file_by_filename(entry["file"])
        file_eid = record["eid"] if record else None
        if record:
            tags = record.get("tags", [])

        response.append({
            "eid": r["eid"],
            "file_eid": file_eid,              
            "file": entry["file"],
            "text": entry["text"][:300],
            "score": float(r["score"]),
            "tags": tags
        })

    return JSONResponse(content={"results": response})


@app.post("/add_tag")
async def add_tag_api(eid: str = Form(...), tag: str = Form(...)):
    add_tag(eid, tag)
    return {"status": "ok"}

@app.post("/remove_tag")
async def remove_tag_api(eid: str = Form(...), tag: str = Form(...)):
    remove_tag(eid, tag)
    return {"status": "ok"}


@app.post("/embed")
async def embed(directory_path: str = Form(...), memory_only: bool = Form(False)):
    global eid_to_text, index
    eid_to_text, _, index = embed_new_documents(memory_only, store, directory_path)
    return {"status": "success", "embedded_segments": len(eid_to_text)}

@app.post("/load")
async def load(force_reload: bool = Form(False)):
    global eid_to_text, index
    eid_to_text, index = load_existing_embeddings()
    return {"status": "success", "loaded_segments": len(eid_to_text)}

@app.get("/read")
async def read_file(file: str):
    safe_path = os.path.abspath(os.path.join(EMBED_FOLDER, file))
    if not safe_path.startswith(os.path.abspath(EMBED_FOLDER)):
        return PlainTextResponse("Access denied.", status_code=403)

    try:
        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
        return PlainTextResponse(content)
    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)



from util.file_registry import list_files as list_registered_files

@app.get("/list_files")
async def list_files():
    return {"files": list_registered_files()}

@app.get("/open_file")
async def open_file(eid: str):
    record = get_file_by_eid(eid)
    if not record:
        return PlainTextResponse("File not found.", status_code=404)

    safe_path = record["path"]
    try:
        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
        return JSONResponse({"filename": record["filename"], "content": content})
    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}", status_code=500)

@app.get("/get_file_metadata")
async def get_file_metadata(eid: str):
    record = get_file_by_eid(eid)
    if not record:
        return PlainTextResponse("File not found.", status_code=404)
    return JSONResponse(record)