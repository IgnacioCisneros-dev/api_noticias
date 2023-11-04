from config.conexion_bd import crear_conexion
from sqlalchemy import text
from entities.entities import comentarios
from fastapi import HTTPException, status
import sys

# Funcion que obtiene todos los comentarios


def obtener_comentarios():
    try:
        # Se hace la conexion con la base de datos
        db = crear_conexion()
        conexion = db.connect()

        # Se crea la query para consultar a base de datos.
        consulta = text(""" SELECT id, contenido,
                        fechacomentario, usuarioid, noticiaid
                        FROM comentarios """)

        # Se ejecuta la consulta
        respuesta = conexion.execute(statement=consulta).fetchall()
        lista_comentarios = []
        if respuesta and len(respuesta) > 0:
            for i in respuesta:
                comentario = comentarios()
                comentario.id = i[0]
                comentario.contenido = i[1]
                comentario.fecha_comentario = i[2]
                comentario.usuario_id = i[3]
                comentario.usuario_id = i[4]
                lista_comentarios.append(comentario)
        return lista_comentarios
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Error al intentar obtener los comentarios de la base de datos.")

# Funcion que busca un comentario en base de datos por su id


def buscar_por_id(comentario_id: int):
    try:
        # Se crea la conexion con la base de datos
        db = crear_conexion()
        conexion = db.connect()

        # Se crea la consulta
        consulta = text(""" SELECT id, contenido,
                        fechacomentario, usuarioid, noticiaid
                        FROM comentarios
                        WHERE id = :comentario_id """)
        # Se crea el parametro para la consulta
        parametro = {
            "comentario_id": comentario_id
        }

        # Se ejecuta la consulta
        resultado = conexion.execute(
            statement=consulta, parameters=parametro).fetchall()

        list_comentario = []
        if resultado and len(resultado) > 0:
            for i in resultado:
                comentario = comentarios()
                comentario.id = i[0]
                comentario.contenido = i[1]
                comentario.fecha_comentario = i[2]
                comentario.usuario_id = i[3]
                comentario.usuario_id = i[4]
                list_comentario.append(comentario)
        return list_comentario
    except Exception:
        print("Ocurrio un error al buscar el comentario por el id {comentario_id}. ",
              sys.exc_info()[1])

# Funcion que se encarga de buscar un comentario por el id de la noticia


def buscar_por_noticia_id(noticia_id: int):
    try:
        db = crear_conexion()
        conexion = db.connect()
        # Se crea la consulta
        consulta = text(""" SELECT id, contenido,
                        fechacomentario, usuarioid, noticiaid
                        FROM comentarios
                        WHERE id = :noticia_id """)

        # Parametro para la consulta
        parametro = {
            "noticia_id": noticia_id
        }

        resultado = conexion.execute(statement=consulta, parameters=noticia_id)

        list_comentario = []
        if resultado and len(resultado) > 0:
            for i in resultado:
                comentario = comentarios()
                comentario.id = i[0]
                comentario.contenido = i[1]
                comentario.fecha_comentario = i[2]
                comentario.usuario_id = i[3]
                comentario.usuario_id = i[4]
                list_comentario.append(comentario)

        return list_comentario
    except Exception:
        print("Ocurrio un error al buscar el comentario. ",
              sys.exc_info()[1])
