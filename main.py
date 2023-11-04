from fastapi import FastAPI
from routers.categorias_routers import categorias_router
from routers.fuentes_routers import fuentes_routers
from routers.noticias_routers import noticias_router
from routers.comentarios_router import comentarios_router
from errors.handler_excepcion import lanzar_http_exception_handler

app = FastAPI(title='Noticias.',
              description='Api que muestra informacion de noticias.',
              version='0.0.1')

# Manejador de excepciones global
lanzar_http_exception_handler(app)

app.include_router(categorias_router)
app.include_router(fuentes_routers)
app.include_router(noticias_router)
app.include_router(comentarios_router)
