import instagram
from flask import request, redirect, render_template
import json

class Comentario:
    def __init__(self, app, login, stream):
        self.__login = login
        self.__stream = stream
        self.rotas(app)

    def rotas(self, app):
        @app.route("/comentarios", methods=["GET"])
        def getComentarios():
            lastComent = request.args.get("lastComent")

            ComentarioMgr = instagram.ComentarioMgr(instagram.getSession)

            comentarios = ComentarioMgr.getComentarios(self.__stream.value, lastComent)
            if (len(comentarios) > 0):
                if (len(comentarios["comentarios"]) > 0):
                    print("Novos comentários")

            return json.dumps(comentarios)

        @app.route("/comentarios/enviar", methods=["POST"])
        def enviarComentario():
            comentario = request.form.get("comentario")
            if comentario is None:
                raise Exception("Erro: Comentário Invalido!")

            ComentarioMgr = instagram.ComentarioMgr(instagram.getSession)
            comentario = ComentarioMgr.comentar(self.__stream.value, comentario)
            return json.dumps(comentario)

        @app.route("/comentarios/alternar", methods=["POST"])
        def alternarComentario():
            ocultar = request.form.get("ocultar")
            if ocultar is None:
                raise Exception("Erro: Comentário Invalido!")

            ocultar = (ocultar!="false")

            ComentarioMgr = instagram.ComentarioMgr(instagram.getSession)
            
            if ocultar:
                ComentarioMgr.ocultarComentarios(self.__stream.value)
                print("Comentarios desativados!")
            else:
                ComentarioMgr.exibirComentarios(self.__stream.value)
                print("Exibindo comentarios!")
            return str(ocultar)