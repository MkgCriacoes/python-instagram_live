USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; Moto C Plus; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 Instagram 139.0.0.33.121 Android (24/7.0; 294dpi; 720x1280; moto; Moto C Plus; Moto C Plus; qcom; pt_BR)"

import requests

session = requests.Session()
session.headers = {
    "user-agent" : USER_AGENT,
    "Referer" : "https://www.instagram.com/"
}

from .login import LoginMgr
from .comentario import ComentarioMgr
from .stream import Stream
from .model.usuario import Usuario

LoginMgr = LoginMgr(session)
ComentarioMgr = ComentarioMgr(session)

#https://instagram.fnat1-1.fna.fbcdn.net/hvideo-vll2/_nc_cat-110/v/r-ggunUiM2nPQW78cwTI2/live-dash/live-hd-a/17943426871352037_0-3521800.m4a
#https://i.instagram.com/api/v1/live/" + live_id+ "/get_final_viewer_list/

def fazerLogin(usuario, senha):
    return LoginMgr.fazerLogin(usuario, senha)

def desconectar():
    LoginMgr.desconectar()

    session.cookies.clear_session_cookies()
    session.headers.clear()
    session.headers = {
        "user-agent" : USER_AGENT,
        "Referer" : "https://www.instagram.com/"
    }

def getJoinRequests(self, stream, last_joinRequest):
    req = session.get("https://i.instagram.com/api/v1/live/" + stream.id+ "/get_join_request_counts/", data={
        "last_seen_ts": last_joinRequest,
        "last_fetch_ts": last_joinRequest
    })
    res = req.json()
    print(res)
    print()

    joinRequests = []
    j_dt_envio = res["fetch_ts"]
    if (j_dt_envio is None) or (int(j_dt_envio) <= int(last_joinRequest)):
        return joinRequests
    
    if res["users"]:
        for j in res["users"]:
            u_id = j["pk"]
            u_nome = j["username"]
            u_img = j["profile_pic_url"]

            usuario = Usuario(u_id, u_nome, u_img)
            joinRequests.append(usuario.toJson())
    
    return joinRequests

def getStream():
    stream = Stream(session)
    return stream

def getComentarios(stream, last_comment):
    return ComentarioMgr.getComentarios(stream, last_comment)

def getInfo(stream):
    req = session.post("https://i.instagram.com/api/v1/live/" + stream.id + "/heartbeat_and_get_viewer_count/")
    res = req.json()

    print(res)

    return res