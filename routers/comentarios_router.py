from fastapi import APIRouter
from services.comentario_service import obtener_comentarios, buscar_por_id, buscar_por_noticia_id
from services.comentario_service import guardar_comentario, actualizar_comentario
from services.comentario_service import eliminar_comentario
from models.request_fuente import requestComentario
from models.response import RespuestaExitosa

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
    return buscar_por_noticia_id(noticia_id)


@comentarios_router.post("/guardar",
                         summary="EndPoint que sirve para guardar nuevos comentarios en la base de datos.",
                         response_model=RespuestaExitosa)
def guardar(request_cometario: requestComentario):
    return guardar_comentario(request_cometario)


@comentarios_router.put("/actualizar/{comentario_id}",
                        summary="EndPoint que sirve para actualizar un comentario.",
                        response_model=RespuestaExitosa)
def actualizar(request_comentario: requestComentario, comentario_id: int):
    return actualizar_comentario(request_comentario, comentario_id)


@comentarios_router.delete("/eliminar/{comentario_id}",
                           summary="EndPoint que elimina un comentario de la base de datos",
                           response_model=RespuestaExitosa)
def eliminar(comentario_id: int):
    return eliminar_comentario(comentario_id)
