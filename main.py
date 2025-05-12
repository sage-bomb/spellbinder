from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

#testing out the comment injector
@app.get("/", response_class=HTMLResponse)
def root(request: Request): #this is also a comment
    return templates.TemplateResponse("index.html", {"request": request})


