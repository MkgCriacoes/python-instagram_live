import instagram
from flask import request, redirect, render_template
import json

class Comentario:
    def __init__(self, app, login, stream):
        self.__login = login
        self.__stream = stream
        self.rotas(app)

    def rotas(self, app):
        @app.route("/comentarios")
        def getComentarios():
            lastComent = request.args.get("lastComent")

            ComentarioMgr = instagram.ComentarioMgr(instagram.getSession)

            comentarios = ComentarioMgr.getComentarios(self.__stream.value, lastComent)
            if (len(comentarios) > 0):
                print("Novos comentários")

            return json.dumps(comentarios)