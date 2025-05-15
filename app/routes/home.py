from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/info", response_class=HTMLResponse)
async def read_info(request:Request):
    csv_file = "data/capacitaciones_mintic.csv"
    sesiones = pd.read_csv(csv_file)
    lista = sesiones.to_dict(orient="records")
    return templates.TemplateResponse("info.html",{"request":request, "sesiones":lista})
    return templates.TemplateResponse("home.html", {"request": request, "title":"@sigmotoa", "name":10})


@router.get("/html", response_class=HTMLResponse)
async def pure_html():
    html_content = """
        <html>
            <head>
                <title>sigmotoa</title>
            </head>
            <body>
                <h1>Look ma! HTML!</h1>
            </body>
        </html>
        """
    return HTMLResponse(content=html_content, status_code=200)