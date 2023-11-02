from fastapi import APIRouter
import sys
from services.fuente_service import consultar_fuentes, buscar_fuente_por_id
from services.fuente_service import persistir_fuente, actualizar_fuentes
from services.fuente_service import eliminar_por_id
from models.request_fuente import requestFuente


fuentes_routers = APIRouter(prefix="/fuente",
                            tags=['Fuentes.'])


@fuentes_routers.get("/obtener",
                     summary="EndPoint que devuelve el listado de todas las fuentes existentes.")
def obtener_fuentes():
    return consultar_fuentes()


@fuentes_routers.get("/obtener_por_id/{fuente_id}",
                     summary="EndPoint que busca la fuente por un id")
def obtener_por_id(fuente_id: int):
    return buscar_fuente_por_id(fuente_id)


@fuentes_routers.post("/guardar",
                      summary="EndPoint que agrega una nueva fuenta a la base de datos.")
def guardar_fuente(request_fuente: requestFuente):
    return persistir_fuente(request_fuente)


@fuentes_routers.put("/actualizar/{fuente_id}",
                     summary="EndPoint que se utiliza para actualizar las fuentes.")
def actualizar_fuente(request_fuente: requestFuente, fuente_id: int):
    return actualizar_fuentes(request_fuente, fuente_id)


@fuentes_routers.delete("/eliminar/{fuente_id}",
                        summary="EndPoint que elimina una fuente de la base de datos.")
def eliminar_fuente(fuente_id: int):
    return eliminar_por_id(fuente_id)
