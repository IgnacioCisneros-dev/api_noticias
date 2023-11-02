from typing import Optional
from pydantic import BaseModel
from datetime import date


class categorias(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class requestCategoria(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class fuentes(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str] = None
    url_fuente: Optional[str] = None
    descripcion: Optional[str] = None


class noticias(BaseModel):
    id: Optional[int] = None
    tituto: Optional[str] = None
    contenido: Optional[str] = None
    fecha_publicacion: Optional[date] = None
    fuente_id: Optional[int] = None
    categoria_noticia_id: Optional[int] = None
    url: Optional[str] = None


class comentarios(BaseModel):
    id: Optional[int] = None
    contenido: Optional[str] = None
    fecha_comentario: Optional[date] = None
    usuario_id: Optional[int] = None
    noticia_id: Optional[int] = None


class noticiascategorias(BaseModel):
    noticia_id: Optional[int] = None
    categoria_id: Optional[int] = None
