from fastapi import HTTPException


class ExceptionPersonalizada(HTTPException):
    """Clase que sirve para generar excepciones personalizadas

    Args:
        Exception (string): Excepcion generada
    """

    def __init__(self, detail: str):
        super().__init(status_code=400, detail=detail)


class Error:
    """Clase encargada para mostrar los errores en las excepciones
    """
    # los () en str son para que al inicializar la clase ya tengan una cadena vacia

    def __init__(self, message: str, detail=str()):
        self.message = message
        self.detail = detail
