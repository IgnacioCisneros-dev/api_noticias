from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.response import RespuestaIncorrecta
from models.model import Mensajes, Tipo


def lanzar_http_exception_handler(app: FastAPI) -> None:
    """Funcion encargada de lanzar la excepciones de tipo HTTPException y 
    darle una respuesta al cliente personalizada con el detalle del error.

    Args:
        app (FastAPI): API que maneja las excepciones

    Returns:
        _type_: Muestra el mensaje de error al cliente
    """

    @app.exception_handler(HTTPException)
    async def http_handler_exception(request: Request, excepcion: HTTPException):
        # JSONResponse ayuda a decodificar los objetos para dar una respuesta en formato JSON al cliente, es este caso se esta
        # deserializando el objeto de RespuestaIncorrecta que a su vez tiene mas objetos dentro
        return JSONResponse(status_code=excepcion.status_code,
                            content=jsonable_encoder(RespuestaIncorrecta
                                                     (Error="Ocurrio un error interno al realizar la peticion.",
                                                      mensaje=Mensajes(
                                                          descripcion=excepcion.detail, tipo_de_mensaje=Tipo.Error
                                                      ))))
