from fastapi import APIRouter
import sys
from services.categoria_service import consultar_categorias, consultar_categoria_por_id
from services.categoria_service import agregar_categoria, actualizar_categoria_por_id
from services.categoria_service import eliminar_por_id
from entities.entities import requestCategoria


categorias_router = APIRouter(prefix='/categoria',
                              tags=['Categorias.'])


@categorias_router.get('/obtener',
                       summary='EndPoint que muestra la informacion de las categorias.')
def obtener_categorias():
    try:
        return consultar_categorias()
    except Exception:
        print("Ocurrio un error al consultar las categorias. ",
              sys.exc_info()[1])


@categorias_router.get('/obtener_por_id/{categoria_id}',
                       summary='EndPoint que regresa una categoria en especifico por el id ingresado')
def obtener_por_id(categoria_id: int):
    try:
        return consultar_categoria_por_id(categoria_id=categoria_id)
    except Exception:
        print(
            f"Ocurrio un error al consultar la categoria por el id {categoria_id}", sys.exc_info()[1])


@categorias_router.post('/guardar',
                        summary='EndPoint que guarda nuevas categorias.')
def guardar_categoria(categoria: requestCategoria):
    return agregar_categoria(categoria=categoria)


@categorias_router.put("/actualizar/{categoria_id}",
                       summary="EndPoint que actualiza una categoria.")
def actualizar_categoria(categoria_id: int, categoria: requestCategoria):
    return actualizar_categoria_por_id(categoria_id, categoria)


@categorias_router.delete("/eliminar/{categoria_id}",
                          summary="EndPoint que elimina una categoria de la BD")
def eliminar_categoria(categoria_id):
    return eliminar_por_id(categoria_id)
