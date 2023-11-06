from config.conexion_bd import crear_conexion
from sqlalchemy import text
from entities.entities import noticias
from models.request_fuente import requestNoticia
import sys
from models.response import RespuestaExitosa
from models.model import Mensajes, Tipo
from fastapi import HTTPException, status


def consultar_noticias():
    try:
        # Se crea la conexion con la base de datos.
        base_datos = crear_conexion()
        conexion = base_datos.connect()
        consulta = text(""" SELECT n.id, n.titulo, n.contenido, n.fechapublicacion,
                        n.fuenteid, n.categorianoticiaid, n.url
                        FROM noticias n """)
        # Se ejecuta la consulta
        respuesta = conexion.execute(statement=consulta).fetchall()

        # Se valida que si exitan noticias
        lista_de_noticias = []
        if respuesta and len(respuesta) > 0:
            for i in respuesta:
                noticia = noticias()
                noticia.id = i[0]
                noticia.tituto = i[1]
                noticia.contenido = i[2]
                noticia.fecha_publicacion = i[3]
                noticia.fuente_id = i[4]
                noticia.categoria_noticia_id = i[5]
                noticia.url = i[6]
                lista_de_noticias.append(noticia)
            return lista_de_noticias
        else:
            return lista_de_noticias

    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al consultar las noticias de la base de datos."
        )


def buscar_por_id(noticia_id: int):
    try:
        bd = crear_conexion()
        conexion = bd.connect()
        consulta = text(""" SELECT n.id, n.titulo, n.contenido, n.fechapublicacion,
                        n.fuenteid, n.categorianoticiaid, n.url
                        FROM noticias n 
                        WHERE n.id = :noticia_id""")
        parametro = {
            "noticia_id": noticia_id
        }
        respuesta = conexion.execute(
            statement=consulta, parameters=parametro).fetchall()

        list_noticia = []
        if respuesta and len(respuesta) > 0:
            for i in respuesta:
                noticia = noticias()
                noticia.id = i[0]
                noticia.tituto = i[1]
                noticia.contenido = i[2]
                noticia.fecha_publicacion = i[3]
                noticia.fuente_id = i[4]
                noticia.categoria_noticia_id = i[5]
                noticia.url = i[6]
                list_noticia.append(noticia)
            return list_noticia
        else:
            return list_noticia
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al buscar por id la noticia."
        )


def agregar_noticia(request_noticias: requestNoticia):
    try:
        # Se hace la conexion con la base de datos
        db = crear_conexion()
        conexion = db.connect()

        # Se crea el insert para guardar la nueva noticia
        insert = text(""" INSERT INTO  noticias
                      (id, titulo, contenido, fechapublicacion, fuenteid, 
                      categorianoticiaid, url)
                      VALUES (:id, :titulo, :contenido, :fecha_publicacion,
                       :fuente_id, :categoria_noticia_id, :url) """)

        # Se obtiene el ultimo id para aumentar en 1 y obtener el id
        ultimo_id = obtener_ultimo_id()
        id = 0
        if len(ultimo_id) > 0:
            id = ultimo_id[-1]
        else:
            id = 1

        # Se forman los parametros para el insert
        values = {
            "id": id + 1,
            "titulo": request_noticias.tituto,
            "contenido": request_noticias.contenido,
            "fecha_publicacion": request_noticias.fecha_publicacion,
            "fuente_id": request_noticias.fuente_id,
            "categoria_noticia_id": request_noticias.categoria_noticia_id,
            "url": request_noticias.url
        }

        # Se ejecuta el query
        conexion.execute(statement=insert, parameters=values)
        conexion.commit()
        conexion.close()

        # Se genera la respuesta para el cliente
        respuesta = RespuestaExitosa(
            mensaje="Peticion Exitosa.",
            detalle=Mensajes(
                descripcion="Noticia guardada exitosamente en la Base.",
                tipo_de_mensaje=Tipo.Suceessful
            ))

        return respuesta
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al crear una nueva noticia.")


def obtener_ultimo_id():
    try:
        # Se crea la conexion con la base de datos y la consulta que se va a ejecutar
        db = crear_conexion()
        conexion = db.connect()
        consulta = text(""" SELECT id
                        FROM noticias
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
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al obtener el ultimo elemento de noticias."
        )


def actualizar_noticia(request_noticia: requestNoticia, noticia_id: int):
    try:
        # Se crea la conexion con la base de datos
        db = crear_conexion()
        conexion = db.connect()

        # Se crea la query del update
        update = text(""" UPDATE noticias 
                      SET titulo = :titulo, contenido = :contenido, fechapublicacion = :fecha_publicacion,
                       fuenteid = :fuente_id, categorianoticiaid = :categoria_noticia_id,
                      url = :url
                      WHERE id = :noticia_id""")

        # Se crea los parametros para el update
        parametros = {
            "titulo": request_noticia.tituto,
            "contenido": request_noticia.contenido,
            "fecha_publicacion": request_noticia.fecha_publicacion,
            "fuente_id": request_noticia.fuente_id,
            "categoria_noticia_id": request_noticia.categoria_noticia_id,
            "url": request_noticia.url,
            "noticia_id": noticia_id
        }

        # Se ejecuta el update
        conexion.execute(statement=update, parameters=parametros)
        conexion.commit()
        conexion.close()

        # Se forma la respuesta para el usuario
        respuesta = RespuestaExitosa(
            mensaje="Peticion Exitosa.",
            detalle=Mensajes(
                descripcion="Noticia actualizada exitosamente.",
                tipo_de_mensaje=Tipo.Suceessful
            )
        )

        return respuesta

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al actualizar la noticia en base de datos."
        )

# Funcion que hace la eliminacion de una noticia en base de datos


def eliminar_noticia(noticia_id: int):
    try:
        # Se crea la conexion con la base de datos
        db = crear_conexion()
        conexion = db.connect()

        # Se crea la sentencia delete
        delete = text(""" DELETE FROM noticias
                      WHERE id = :noticia_id """)

        # se forma el id para el WHERE
        parametro = {
            "noticia_id": noticia_id
        }

        # Se ejecuta el delete y se hace commit
        conexion.execute(statement=delete, parameters=parametro)
        conexion.commit()

        # Se cierra la conexion con la base de datos
        conexion.close()

        # Se genera la respuesta al cliente
        respuesta = RespuestaExitosa(
            mensaje="Peticion Exitosa.",
            detalle=Mensajes(
                descripcion="Noticia eliminada exitosamente.",
                tipo_de_mensaje=Tipo.Suceessful
            )
        )

        return respuesta
    except HTTPException as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error al eliminar la noticia de base de datos."
        )
