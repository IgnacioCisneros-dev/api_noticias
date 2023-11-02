from fastapi import APIRouter
from services.noticia_service import consultar_noticias, buscar_por_id
from services.noticia_service import agregar_noticia, actualizar_noticia
from services.noticia_service import eliminar_noticia
from models.request_fuente import requestNoticia

noticias_router = APIRouter(prefix="/noticia",
                            tags=['Noticias.'])


@noticias_router.get("/obtener/",
                     summary="EndPoint que muestra todas las noticias registradas en BD")
def obtener_noticias():
    return consultar_noticias()


@noticias_router.get("/obtener_por_id/{noticia_id}")
def obtener_por_id(noticia_id):
    return buscar_por_id(noticia_id)


@noticias_router.post("/agregar",
                      summary="EndPoint para agregar una nueva noticia.")
def guardar(request_noticia: requestNoticia):
    return agregar_noticia(request_noticia)


@noticias_router.put("/actualizar/{noticia_id}",
                     summary="EndPoint que actualiza una noticia.")
def actualizar(requet_noticia: requestNoticia, noticia_id: int):
    return actualizar_noticia(requet_noticia, noticia_id)


@noticias_router.delete("/eliminar/{noticia_id}",
                        summary="EndPoint que elimina una noticia de base de datos.")
def eliminar(noticia_id: int):
    return eliminar_noticia(noticia_id)
