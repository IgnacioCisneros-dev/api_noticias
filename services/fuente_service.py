from config.conexion_bd import crear_conexion
import sys
from sqlalchemy import text
from entities.entities import fuentes
from models.request_fuente import requestFuente


def consultar_fuentes():
    try:
        base_datos = crear_conexion()
        conexion = base_datos.connect()
        consulta = text(""" SELECT f.id, f.nombre, f.urlfuente, f.descripcion  
                        FROM fuentes f """)

        resultado = conexion.execute(consulta).fetchall()

        lista_fuentes = []
        if resultado is not None and len(resultado) > 0:
            for f in resultado:
                fuente = fuentes()
                fuente.id = f[0]
                fuente.nombre = f[1]
                fuente.url_fuente = f[2]
                fuente.descripcion = f[3]
                lista_fuentes.append(fuente)

            conexion.close()
            return lista_fuentes
        else:
            conexion.close()
            return lista_fuentes
    except Exception:
        print("Ocurrio un error al intentar consultar las fuentes en base de datos.",
              sys.exc_info()[1])


def buscar_fuente_por_id(fuente_id: int):
    try:
        base_datos = crear_conexion()
        conexion = base_datos.connect()
        consulta = text(""" SELECT f.id, f.nombre, f.urlfuente, f.descripcion  
                        FROM fuentes f
                        WHERE f.id = :fuente_id """)

        parametro = {
            "fuente_id": fuente_id
        }

        resultado = conexion.execute(
            statement=consulta, parameters=parametro).fetchall()

        list_fuente = []
        if resultado and len(resultado) > 0:
            for f in resultado:
                fuente = fuentes()
                fuente.id = f[0]
                fuente.nombre = f[1]
                fuente.url_fuente = f[2]
                fuente.descripcion = f[3]
                list_fuente.append(fuente)
            conexion.close()
            return list_fuente
        else:
            conexion.close()
            return list_fuente
    except Exception:
        print(
            f"Ocurrio un error al intentar buscar la fuente por el id {fuente_id}: ", sys.exc_info()[1])


def persistir_fuente(request_fuente: requestFuente):
    try:
        base_datos = crear_conexion()
        conexion = base_datos.connect()
        insert = text(""" INSERT INTO fuentes
                      (id, nombre, urlfuente, descripcion)
                      VALUES (:id, :nombre, :urlfuente, :descripcion) """)

        id = obtener_el_ultimo_id()
        parametros = {
            "id": id[-1] + 1,
            "nombre": request_fuente.nombre,
            "urlfuente": request_fuente.url_fuente,
            "descripcion": request_fuente.descripcion
        }

        conexion.execute(statement=insert, parameters=parametros)
        conexion.commit()
        conexion.close()
        return 'Fuente guardada exitosamente.'
    except Exception:
        print(
            f"Ocurrio un error al intentar guardar la fuente {request_fuente.nombre}: ", sys.exc_info()[1])


def obtener_el_ultimo_id():
    try:
        base_de_datos = crear_conexion()
        conexion = base_de_datos.connect()
        consulta = text(""" SELECT f.id
                        FROM fuentes f
                        ORDER BY id ASC """)

        ultimo_id = conexion.execute(statement=consulta).fetchall()
        list_id = []
        if ultimo_id and len(ultimo_id) > 0:
            # list_id.append(ultimo_id[-1])
            for i in ultimo_id:
                list_id.append(i[0])
        else:
            list_id.append(0)
        return list_id
    except Exception:
        print("Ocurrio un error al obtener el ultimo id.",
              sys.exc_info()[1])


def actualizar_fuentes(request_fuente: requestFuente, fuente_id: int):
    try:
        base_datos = crear_conexion()
        conexion = base_datos.connect()

        # Se busca en BD la fuente que se va a editar

        fuente = buscar_fuente_por_id(fuente_id)
        # Si la fuente se encuentra, se procede a actualizar
        if fuente:
            update = text(""" UPDATE fuentes
                        SET nombre = :nombre, urlfuente = :url_fuente, 
                        descripcion = :descripcion
                        WHERE id = :fuente_id """)

            parametros = {
                "nombre": request_fuente.nombre,
                "url_fuente": request_fuente.url_fuente,
                "descripcion": request_fuente.descripcion,
                "fuente_id": fuente_id
            }

            conexion.execute(statement=update, parameters=parametros)
            conexion.commit()
            conexion.close()
            return 'Fuente actualizada exitosamente.'
        else:
            return 'no se encontro la fuenta para actualizar.'
    except Exception:
        print(
            f"Ocurrio un error al intentar actualizar la fuente {request_fuente.nombre}: ", sys.exc_info()[1])


def eliminar_por_id(fuente_id: int):
    try:
        base_datos = crear_conexion()
        conexion = base_datos.connect()
        delete = text(""" DELETE FROM fuentes
                      WHERE id = :fuente_id """)

        parametro = {
            "fuente_id": fuente_id
        }

        conexion.execute(statement=delete, parameters=parametro)
        conexion.commit()
        conexion.close()
        return 'Fuente eliminada correctamente.'
    except Exception:
        print("Ocurrio un error al intentar eliminar la fuente ",
              sys.exc_info()[1])
