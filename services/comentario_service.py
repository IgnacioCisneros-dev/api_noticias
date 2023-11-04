from config.conexion_bd import crear_conexion
from sqlalchemy import text
from entities.entities import comentarios
from fastapi import HTTPException, status
from models.request_fuente import requestComentario
from models.response import RespuestaExitosa
from models.response import Mensajes
from models.model import Tipo

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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Error al buscar el comentario por el id {comentario_id}.")

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
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No se encontro el comentario por noticia_id {noticia_id}")
    except HTTPException as e:
        raise HTTPException(e.status_code, detail=e.detail)


def guardar_comentario(request_comentario: requestComentario):
    try:
        # Se crea la conexion con la base de datos
        db = crear_conexion()
        conexion = db.connect()

        # Se crea el query para hacer el insert
        query = text(""" INSERT INTO comentarios (id, contenido, fechacomentario, usuarioid, noticiaid)
                     VALUES (:id, :contenido, :fecha_comentario, :usuario_id, :noticia_id) """)

        # Se obtiene el ultimo ID
        ultimo_id = obtener_ultimo_id()
        id = 0

        if len(ultimo_id) > 0:
            id = ultimo_id[-1]
        else:
            id = 1

        # Se forman los parametros para el insert
        parametros = {
            "id": id + 1,
            "contenido": request_comentario.contenido,
            "fecha_comentario": request_comentario.fecha_comentario,
            "usuario_id": request_comentario.usuario_id,
            "noticia_id": request_comentario.noticia_id
        }

        # Se ejecuta la consulta
        conexion.execute(statement=query, parameters=parametros)
        conexion.commit()
        conexion.close()

        # Se crea instancia del objeto de respuesta
        respuesta = RespuestaExitosa(mensaje="Peticion Exitosa.",
                                     detalle=Mensajes(descripcion="Se guardo exitosamente el comentario en base de datos.",
                                                      tipo_de_mensaje=Tipo.Suceessful))
        return respuesta

    except Exception as error:
        print(f"Error: {error.__dict__}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Error al guardar el comentario en la base.")


def obtener_ultimo_id():
    try:
        # Se crea la conexion con la base de datos y la consulta que se va a ejecutar
        db = crear_conexion()
        conexion = db.connect()
        consulta = text(""" SELECT id
                        FROM comentarios
                        ORDER BY ID ASC """)

        # Se ejecuta la query
        ultimo_id = conexion.execute(statement=consulta).fetchall()

        # Se valida que si exista el id
        list_ultimo_id = []
        if ultimo_id and len(ultimo_id) > 0:
            for i in ultimo_id:
                list_ultimo_id.append(i[0])
        return list_ultimo_id

    except HTTPException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Error al obtener el ultimo registro del id.")
