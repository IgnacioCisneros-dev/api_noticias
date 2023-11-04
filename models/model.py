from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Tipo(str, Enum):
    Error = "Error"
    Warning = "Warning"


class Mensajes(BaseModel):
    descripcion: Optional[str] = None
    tipo_de_mensaje: Tipo = None


class StatusMensajes(BaseModel):
    mensajes: List[Mensajes] = None
