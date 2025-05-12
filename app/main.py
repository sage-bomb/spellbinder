from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
from util.embedding_store import EmbeddingStore
from util.vector_search import VectorSearchIndex
from util.embedding import get_embedding, load_embedding, save_embedding, delete_embedding
from testing.test_embed_search import embed_new_documents, load_existing_embeddings

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

eid_to_text = {}
index = VectorSearchIndex()
store = EmbeddingStore()

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
        response.append({
            "eid": r["eid"],
            "file": entry["file"],
            "text": entry["text"][:300],
            "score": float(r["score"])
        })
    return JSONResponse(content={"results": response})

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