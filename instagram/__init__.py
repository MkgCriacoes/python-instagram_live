import requests

#https://i.instagram.com/api/v1/live/" + live_id+ "/get_comment/?last_comment_ts=0
#https://i.instagram.com/api/v1/live/" + live_id+ "/get_final_viewer_list/

URL = "https://www.instagram.com/"
USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; Moto C Plus; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 Instagram 139.0.0.33.121 Android (24/7.0; 294dpi; 720x1280; moto; Moto C Plus; Moto C Plus; qcom; pt_BR)"
session = requests.Session()

live_id = None
stream_url = None
stream_key = None

def atualizarCSRFToken(session, token):
    session.headers.update({"X-CSRFToken": token})

def fazerLogin(usuario, senha):
    session.headers = {
        "user-agent" : USER_AGENT,
        "Referer" : URL
    }

    req = session.get(URL)
    atualizarCSRFToken(session, req.cookies["csrftoken"])

    req = session.post(URL + "accounts/login/ajax/", data={
        "username": usuario,
        "password": senha
    })
    res = req.json()
    atualizarCSRFToken(session, req.cookies["csrftoken"])

def getJoinRequests():
    req = session.get("https://i.instagram.com/api/v1/live/" + live_id+ "/get_join_request_counts/", data={
        "last_total_count": 0,
        "last_seen_ts": 0,
        "last_fetch_ts": 0
    })
    res = req.json()
    print(res)

def getStream():
    global live_id
    global stream_url
    global stream_key

    req = session.post("https://i.instagram.com/api/v1/live/create/", data={
        "preview_height": 1794,
        "preview_width":  1080,
        "broadcast_type": "RTMP_SWAP_ENABLED",
        "internal_only": 0
    })
    res = req.json()

    live_id = str(res["broadcast_id"])
    stream_url = "rtmps://live-upload.instagram.com:443/rtmp/"
    stream_key = res["upload_url"].replace(stream_url, "")

    print("URL do Stream")
    print(stream_url)
    print("")
    print("")

    print("Chave do Stream")
    print(stream_key)
    print("")
    print("")

    return {
        "live_id": live_id,
        "stream_url": stream_url,
        "stream_key": stream_key
    }

def iniciarStream():
    print("Iniciando stream")
    #_csrftoken=KHYH0aAV1MAuodATGwQL6pSiViT79Im4&_uuid=c2e407d1-0c08-40a4-afd4-a90e00ec6251
    req = session.post("https://i.instagram.com/api/v1/live/" + live_id+ "/start/")
    print(req.json())

def encerrarStream():
    print("Encerrando stream")
    #signed_body=d8495776e76a44abd12d7c6b753ebb7bbcf8b0fddb30b888fb6a8377a0404d21.{"_csrftoken":"KHYH0aAV1MAuodATGwQL6pSiViT79Im4","_uid":"32566605591","_uuid":"c2e407d1-0c08-40a4-afd4-a90e00ec6251","end_after_copyright_warning":"false"}&ig_sig_key_version=4
    req = session.post("https://i.instagram.com/api/v1/live/" + live_id+ "/end_broadcast/")
    print(req.json())