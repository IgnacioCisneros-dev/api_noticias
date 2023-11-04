from pydantic import BaseModel
from models.model import Mensajes
from typing import Optional


class RespuestaIncorrecta(BaseModel):
    Error: Optional[str] = None
    mensaje: Mensajes


class RespuestaExitosa(BaseModel):
    mensaje: Optional[str] = None
    detalle: Mensajes
