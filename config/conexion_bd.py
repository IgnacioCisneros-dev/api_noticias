from sqlalchemy import create_engine
import cfn
import sys


def crear_conexion():
    bandera = False
    intento = 0

    while not bandera or intento <= 5:
        try:
            conexion = cfn.url_conexion
            engine = create_engine(conexion)
            with engine.connect() as conexion:                
                bandera = True
            return engine
        except Exception as e:
            print(
                f'Ocurrio un error al intentar conectar a la BD {str(sys.exc_info()[1])}')
