from config.conexion_bd import crear_conexion
import sys
from sqlalchemy import text
from entities.entities import categorias, requestCategoria
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from models.response import RespuestaExitosa
from models.model import Mensajes, Tipo


def consultar_categorias():
    try:
        base_de_datos = crear_conexion()
        conexion = base_de_datos.connect()
        consulta = text(
            f""" SELECT c.id, c.nombre, c.descripcion FROM categorias c """)
        respuesta = conexion.execute(consulta).fetchall()

        if respuesta is not None and len(respuesta) > 0:
            lista_categorias = []
            for i in respuesta:
                categoria = categorias()
                categoria.id = i[0]
                categoria.nombre = i[1]
                categoria.descripcion = i[2]
                lista_categorias.append(categoria)
        else:
            lista_categorias = []

        return lista_categorias
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al consultar las categorias."
        )
    finally:
        conexion.close()


def consultar_categoria_por_id(categoria_id: int):
    try:
        base_de_datos = crear_conexion()
        conexion = base_de_datos.connect()
        consulta = text(""" SELECT c.id, c.nombre, c.descripcion 
                        FROM categorias c 
                        WHERE c.id = :categoria_id """)

        parametros = {'categoria_id': categoria_id}

        resultado = conexion.execute(
            consulta, parametros).fetchall()

        categoria = categorias()

        if resultado is not None and len(resultado) > 0:
            for i in resultado:
                categoria.id = i[0]
                categoria.nombre = i[1]
                categoria.descripcion = i[2]
        else:
            categoria = []

        return categoria
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al consultar categoria."
        )
    finally:
        conexion.close()


def agregar_categoria(categoria: requestCategoria):
    try:
        bd = crear_conexion()
        conexion = bd.connect()
        insert = text(""" INSERT INTO categorias
                       (id, nombre, descripcion) VALUES (:id, :nombre, :descripcion)""")

        id = recuperar_ultimo_registro()

        values = {
            'id': id + 1,
            'nombre': categoria.nombre,
            'descripcion': categoria.descripcion}

        conexion.execute(insert, values)
        conexion.commit()

        # Se genera la respuesta para el cliente
        respuesta = RespuestaExitosa(
            mensaje="Peticion Exitosa.",
            detalle=Mensajes(
                descripcion="Categoria creada exitosamente.",
                tipo_de_mensaje=Tipo.Suceessful
            )
        )
        return respuesta
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al crear la categoria."
        )
    finally:
        conexion.close()


def recuperar_ultimo_registro():
    try:
        db = crear_conexion()
        conexion = db.connect()
        query = text(""" SELECT c.id 
                    FROM categorias c
                    ORDER BY ID DESC """)

        respuesta = conexion.execute(query).first()

        if respuesta is not None and len(respuesta) > 0:
            return respuesta[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La tabla de categorias esta vacia."
            )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al obtener el ultimo registro de categorias."
        )
    finally:
        conexion.close()


def actualizar_categoria_por_id(categoria_id, categoria_request: requestCategoria):
    try:
        # Se busca esa categoria para validar que exista
        categoria = consultar_categoria_por_id(categoria_id)
        if categoria:
            # En este punto, ya categoria se encuentra, se procede a actualizar
            db = crear_conexion()
            conexion = db.connect()
            update = text(""" UPDATE categorias 
                          SET nombre = :nombre, descripcion = :descripcion
                          WHERE id = :id """)

            parametros = {"nombre": categoria_request.nombre,
                          "descripcion": categoria_request.descripcion,
                          "id": categoria_id}

            conexion.execute(update, parametros)
            conexion.commit()

            # Se genera la respuesta para el cliente
            respuesta = RespuestaExitosa(
                mensaje="Peticion Exitosa.",
                detalle=Mensajes(
                    descripcion="Categoria actualizada exitosamente.",
                    tipo_de_mensaje=Tipo.Suceessful
                )
            )
            return respuesta
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontro la categoria para actualizar."
            )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al actualizar la categoria."
        )
    finally:
        conexion.close()


def eliminar_por_id(categoria_id: int):
    try:
        bd = crear_conexion()
        conexion = bd.connect()
        delete = text(""" DELETE FROM categorias
                      WHERE id = :categoria_id """)

        parametro = {
            "categoria_id": categoria_id
        }

        conexion.execute(delete, parameters=parametro)
        conexion.commit()

        # Se forma la respuesta para el cliente
        respuesta = RespuestaExitosa(
            mensaje="Peticion Exitosa",
            detalle=Mensajes(
                descripcion="Categoria eliminada exitosamente.",
                tipo_de_mensaje=Tipo.Suceessful
            )
        )

        return respuesta
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al eliminar la categoria."
        )

    finally:
        conexion.close()
