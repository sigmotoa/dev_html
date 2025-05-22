from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from app.models.models import Sesion

templates = Jinja2Templates(directory="templates")
router = APIRouter()
csv_file = "data/capacitaciones_mintic.csv"

@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/info", response_class=HTMLResponse)
async def read_info(request:Request):
    #csv_file = "data/capacitaciones_mintic.csv"
    sesiones = pd.read_csv(csv_file)
    sesiones["id"] = sesiones.index
    lista = sesiones.to_dict(orient="records")
    return templates.TemplateResponse("info.html",{"request":request, "sesiones":lista, "titulo":"Datos en tabla"})


@router.get("/add", response_class=HTMLResponse)
async def show_form(request:Request):
    return templates.TemplateResponse("add.html", {"request":request})


@router.post("/add")
async def submit_info(
        tema: str = Form(...),
        fecha:str=Form(...),
        hora:str=Form(...),
        nombre_mentor:str=Form(...),
        link:str=Form(...)
):
    sesion = Sesion(tema=tema, fecha=fecha, hora=hora, nombre_mentor=nombre_mentor, link=link)

    df = pd.read_csv(csv_file)
    df.loc[len(df)] = [sesion.tema, sesion.fecha, sesion.hora, sesion.nombre_mentor, sesion.link]
    df.to_csv(csv_file, index=True)

    return RedirectResponse(url="/info", status_code=303)


@router.get("/detail/{id}", response_class=HTMLResponse)
def detalle_sesion(request: Request, id: int):
    df = pd.read_csv(csv_file)

    if id < 0 or id >= len(df):
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
        return HTMLResponse(content=html_content, status_code=404)

    fila = df.iloc[id]

    sesion = {
        "tema": fila["Tema"],
        "fecha": fila["Fecha"],
        "hora": fila["Hora"],
        "nombre_mentor": fila["Mentor"],
        "link": fila["Enlace"]
    }

    return templates.TemplateResponse("detail.html", {"request": request, "sesion": sesion})



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