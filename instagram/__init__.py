from .stream import Stream
import requests

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