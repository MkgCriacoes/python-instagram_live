from .stream import Stream
from .model.usuario import Usuario
from .model.comentario import Comentario
import requests

#https://instagram.fnat1-1.fna.fbcdn.net/hvideo-vll2/_nc_cat-110/v/r-ggunUiM2nPQW78cwTI2/live-dash/live-hd-a/17943426871352037_0-3521800.m4a
#https://i.instagram.com/api/v1/live/" + live_id+ "/get_comment/?last_comment_ts=0
#https://i.instagram.com/api/v1/live/" + live_id+ "/get_final_viewer_list/

URL = "https://www.instagram.com/"
USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; Moto C Plus; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 Instagram 139.0.0.33.121 Android (24/7.0; 294dpi; 720x1280; moto; Moto C Plus; Moto C Plus; qcom; pt_BR)"

session = requests.Session()
session.headers = {
    "user-agent" : USER_AGENT,
    "Referer" : URL
}

def atualizarCSRFToken(session, token):
    session.headers.update({"X-CSRFToken": token})

def fazerLogin(usuario, senha):
    print("Fazendo login no instagram @%s...." % usuario)

    req = session.get(URL)
    atualizarCSRFToken(session, req.cookies["csrftoken"])

    req = session.post(URL + "accounts/login/ajax/", data={
        "username": usuario,
        "password": senha
    })
    res = req.json()
    atualizarCSRFToken(session, req.cookies["csrftoken"])

    if res["status"] != "ok" or res["authenticated"] != True:
        raise Exception("Erro no login: %s" % res)

    print("Logado com sucesso!")
    print()

def getJoinRequests():
    req = session.get("https://i.instagram.com/api/v1/live/" + live_id+ "/get_join_request_counts/", data={
        "last_total_count": 0,
        "last_seen_ts": 0,
        "last_fetch_ts": 0
    })
    res = req.json()
    print(res)
    print()

def getStream():
    stream = Stream(session)
    return stream

def getComentarios(stream, last_comment):
    req = session.get("https://i.instagram.com/api/v1/live/" + stream.id+ "/get_comment/", data={
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

def getInfo(stream):
    req = session.post("https://i.instagram.com/api/v1/live/" + stream.id + "/heartbeat_and_get_viewer_count/")
    res = req.json()

    print(res)

    return res