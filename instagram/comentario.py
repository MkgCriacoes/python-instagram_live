from flask import request

from .model.usuario import Usuario
from .model.comentario import Comentario
from .constants import Constants

class ComentarioMgr:
    def __init__(self, getSession):
        self.__session = None
        self.__getSession = getSession

    def getComentarios(self, stream, last_comment):
        self.__session = self.__getSession()
        self.__session.headers.update({"X-CSRFToken": request.cookies.get("csrf_token")})

        req = self.__session.get("https://i.instagram.com/api/v1/live/" + stream.id+ "/get_comment/", data={
            "last_comment_ts" : last_comment
        })
        res = req.json()

        if res["status"] != "ok":
            return []

        ativo = not bool(res["comment_muted"])
        comentarios = []
        
        if ativo and res["comments"] is not None:
            for c in res["comments"]:
                c_id = c["pk"]
                c_dt_envio = c["created_at"]
                c_texto = c["text"]
                
                u = c["user"]
                u_id = u["pk"]
                u_nome = u["username"]
                u_img = u["profile_pic_url"]

                if (int(c_dt_envio) <= int(last_comment)):
                    continue

                usuario = Usuario(u_id, u_nome, u_img)
                comentario = Comentario(c_id, c_dt_envio, c_texto, usuario)
                
                comentarios.append(comentario.toJson())

        if ativo and res["system_comments"] is not None:
            for c in res["system_comments"]:
                c_id = c["pk"]
                c_dt_envio = c["created_at"]
                c_texto = c["text"].replace("joined", "entrou")
                
                u = c["user"]
                u_img = u["profile_pic_url"]

                if (int(c_dt_envio) <= int(last_comment)):
                    continue

                usuario = Usuario("", "", u_img)
                comentario = Comentario(c_id, c_dt_envio, c_texto, usuario)
                
                comentarios.append(comentario.toJson())

        return {
            "comentarios": comentarios,
            "ativo": ativo
        }

    def ocultarComentarios(self, stream):
        self.__session = self.__getSession()
        self.__session.headers.update({"X-CSRFToken": request.cookies.get("csrf_token")})

        req = self.__session.post("https://i.instagram.com/api/v1/live/" + stream.id + "/mute_comment/")
        res = req.json()
        return res

    def exibirComentarios(self, stream):
        self.__session = self.__getSession()
        self.__session.headers.update({"X-CSRFToken": request.cookies.get("csrf_token")})

        req = self.__session.post("https://i.instagram.com/api/v1/live/" + stream.id + "/unmute_comment/")
        res = req.json()
        return res

    def comentar(self, stream, texto):
        self.__session = self.__getSession()
        self.__session.headers.update({"X-CSRFToken": request.cookies.get("csrf_token")})

        req = self.__session.post("https://i.instagram.com/api/v1/live/" + stream.id + "/comment/", data={
            "comment_text": texto,
            "live_or_vod": 1,
            "offset_to_video_start": 0,
            "idempotence_token": Constants.DEVICE
        })
        res = req.json()

        return res