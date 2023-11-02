from config.conexion_bd import crear_conexion
import sys
from sqlalchemy import text
from entities.entities import categorias, requestCategoria


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

        conexion.close()
        return lista_categorias
    except Exception:
        print("Error al consultar las categorias de base de datos. ",
              sys.exc_info()[1])


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
        conexion.close()
        return categoria
    except Exception:
        print("Error al consultar en base de datos ", sys.exc_info()[1])


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
        conexion.close()
        return 'Categoria registrada.'
    except Exception:
        print("Ocurrio un error al intentar guardar la categoria en BD. ",
              sys.exc_info()[1])


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
            print("Ocurrio un error al buscar el ultimo id de categorias.")
    except Exception:
        print("Ocurrio un error al buscar el ultimo id de categorias.",
              sys.exc_info()[1])


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
            conexion.close()
            return "Categoria actualizada exitosamente."
        else:
            Exception("No se encontro el registro para actualizar.")
    except Exception:
        print("Ocurrio un error al intentar actualizar la categoria.",
              sys.exc_info()[1])


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
        conexion.close()
        return "Categoria eliminada correctamente."
    except Exception:
        print("Ocurrio un error al eliminar la categoria.", sys.exc_info()[1])
