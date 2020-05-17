from .constants import Constants
import requests
from flask import request

class Stream():
    def __init__(self, getSession, criarStream=True):
        self.__getSession = getSession
        self.id = None
        self.url = None
        self.key = None
        self.iniciado = False
        self.__cookies = {}

        if not criarStream:
            self.id = request.cookies.get("stream_id")
            self.url = request.cookies.get("stream_url")
            self.key = request.cookies.get("stream_key")
            self.iniciado = request.cookies.get("stream_status")

            self.iniciado = (self.iniciado == "iniciado")

            if self.id is None or self.url is None or self.key is None:
                raise Exception("Não existe chave de Stream no cookie")

            return

        token = request.cookies.get("csrf_token")

        self.__session = self.__getSession()
        self.__session.headers.update({"X-CSRFToken": token})

        print("Obtendo chave do Stream")

        req = self.__session.post("https://i.instagram.com/api/v1/live/create/", data={
            "_uuid": Constants.DEVICE,
            "_csrftoken": token,
            "preview_height": 1794,
            "preview_width":  1080,
            "broadcast_type": "RTMP_SWAP_ENABLED",
            "internal_only": 0
        })
        token = self.__session.atualizarCSRFToken(req.cookies["csrftoken"])
        
        res = req.json()

        self.id = str(res["broadcast_id"])
        self.url = "rtmps://live-upload.instagram.com:443/rtmp/"
        self.key = res["upload_url"].replace(self.url, "")

        print("URL do Stream")
        print(self.url)
        print("")
        print("")

        print("Chave do Stream")
        print(self.key)
        print("")
        print("")

        self.__cookies = self.__session.cookies.copy()
        self.__cookies.update({"csrf_token": token})
    
    def getCookies(self):
        return self.__cookies

    def iniciar(self):
        self.__session = self.__getSession()
        print("Iniciando stream")
        #_csrftoken=KHYH0aAV1MAuodATGwQL6pSiViT79Im4&_uuid=c2e407d1-0c08-40a4-afd4-a90e00ec6251
        req = self.__session.post("https://i.instagram.com/api/v1/live/" + self.id+ "/start/")
        token = self.__session.atualizarCSRFToken(req.cookies["csrftoken"])
        
        print(req.json())
        print()

        self.__cookies = self.__session.cookies.copy()
        self.__cookies.update({"csrf_token": token})

        self.iniciado = True

    def encerrar(self):
        self.__session = self.__getSession()
        print("Encerrando stream")
        #signed_body=d8495776e76a44abd12d7c6b753ebb7bbcf8b0fddb30b888fb6a8377a0404d21.{"_csrftoken":"KHYH0aAV1MAuodATGwQL6pSiViT79Im4","_uid":"32566605591","_uuid":"c2e407d1-0c08-40a4-afd4-a90e00ec6251","end_after_copyright_warning":"false"}&ig_sig_key_version=4
        req = self.__session.post("https://i.instagram.com/api/v1/live/" + self.id+ "/end_broadcast/")
        token = self.__session.atualizarCSRFToken(req.cookies["csrftoken"])
        
        print(req.json())
        print()

        self.__cookies = self.__session.cookies.copy()
        self.__cookies.update({"csrf_token": token})

        self.iniciado = False