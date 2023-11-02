from typing import Optional
from pydantic import BaseModel
from datetime import date


class requestFuente(BaseModel):
    nombre: Optional[str] = None
    url_fuente: Optional[str] = None
    descripcion: Optional[str] = None


class requestNoticia(BaseModel):
    tituto: Optional[str] = None
    contenido: Optional[str] = None
    fecha_publicacion: Optional[date] = None
    fuente_id: Optional[int] = None
    categoria_noticia_id: Optional[int] = None
    url: Optional[str] = None
