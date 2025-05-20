from pydantic import BaseModel

class Sesion(BaseModel):
    tema:str
    fecha:str
    hora:str
    nombre_mentor:str
    link:str