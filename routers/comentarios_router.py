from fastapi import APIRouter
from services.comentario_service import obtener_comentarios, buscar_por_id

comentarios_router = APIRouter(prefix="/comentario",
                               tags=["Comentarios."])


@comentarios_router.get("/obtener",
                        summary="EndPoint que muestra todos los comentarios.")
def obtener():
    return obtener_comentarios()


@comentarios_router.get("/obtener_por_id/{comentario_id}",
                        summary="EndPoint que busca un comentario por el id.")
def obtener_por_id(comentario_id: int):
    return buscar_por_id(comentario_id)


@comentarios_router.get("/obtener_por_noticia_id/{noticia_id}",
                        summary="EndPoint que busca un comentario por el id de la noticia.")
def obtener_por_noticia_id(noticia_id: int):
    return "OK"
