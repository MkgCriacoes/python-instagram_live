from .model.usuario import Usuario
from .model.comentario import Comentario

class ComentarioMgr:
    def __init__(self, session):
        self.__session = session

    def getComentarios(self, stream, last_comment):
        req = self.__session.get("https://i.instagram.com/api/v1/live/" + stream.id+ "/get_comment/", data={
            "last_comment_ts" : last_comment
        })
        res = req.json()

        print(res)
        print()

        if res["status"] != "ok":
            return []

        comentarios = []
        
        if res["comments"] is not None:
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

        if res["system_comments"] is not None:
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

        return comentarios