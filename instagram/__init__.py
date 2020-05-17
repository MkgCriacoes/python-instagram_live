from .constants import Constants
import requests
from flask import request

def getSession():
    session = requests.Session()
    session.headers = {
        "user-agent" : Constants.USER_AGENT,
        "Referer" : "https://i.instagram.com/"
    }

    def atualizarCSRFToken(token):
        if token is None:
            return
        
        session.headers.update({"X-CSRFToken": token})
        return token

    session.atualizarCSRFToken = atualizarCSRFToken
    session.atualizarCSRFToken(request.cookies.get("csrf_token"))
    
    cookies = request.cookies.to_dict()
    for c in cookies:
        if c.startswith("i."):
            cookie = requests.cookies.create_cookie(c[2:], cookies[c], domain=".instagram.com")
            session.cookies.set_cookie(cookie)

    return session

from .login import LoginMgr
from .comentario import ComentarioMgr
from .stream import Stream
from .model.usuario import Usuario

#https://instagram.fnat1-1.fna.fbcdn.net/hvideo-vll2/_nc_cat-110/v/r-ggunUiM2nPQW78cwTI2/live-dash/live-hd-a/17943426871352037_0-3521800.m4a
#https://i.instagram.com/api/v1/live/" + live_id+ "/get_final_viewer_list/

def getJoinRequests(self, stream, last_joinRequest):
    session = getSession()

    req = session.get("https://i.instagram.com/api/v1/live/" + stream.id+ "/get_join_request_counts/", data={
        "last_seen_ts": last_joinRequest,
        "last_fetch_ts": last_joinRequest
    })
    res = req.json()

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

def getStream(criarStream=True):
    try:
        stream = Stream(getSession, criarStream)
        return stream
    except Exception as e:
        print(e)
        return None

def getInfo(stream):
    session = getSession()

    req = session.post("https://i.instagram.com/api/v1/live/" + stream.id + "/heartbeat_and_get_viewer_count/")
    res = req.json()

    return res