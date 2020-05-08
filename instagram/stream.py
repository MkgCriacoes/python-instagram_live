import requests

class Stream():
    def __init__(self, session):
        self.__session = session
        self.__live_id = None
        self.__stream_url = None
        self.__stream_key = None

        print("Obtendo chave do Stream")

        req = self.__session.post("https://i.instagram.com/api/v1/live/create/", data={
            "preview_height": 1794,
            "preview_width":  1080,
            "broadcast_type": "RTMP_SWAP_ENABLED",
            "internal_only": 0
        })
        res = req.json()

        self.__live_id = str(res["broadcast_id"])
        self.__stream_url = "rtmps://live-upload.instagram.com:443/rtmp/"
        self.__stream_key = res["upload_url"].replace(self.__stream_url, "")

        print("URL do Stream")
        print(self.__stream_url)
        print("")
        print("")

        print("Chave do Stream")
        print(self.__stream_key)
        print("")
        print("")

    def iniciar(self):
        print("Iniciando stream")
        #_csrftoken=KHYH0aAV1MAuodATGwQL6pSiViT79Im4&_uuid=c2e407d1-0c08-40a4-afd4-a90e00ec6251
        req = self.__session.post("https://i.instagram.com/api/v1/live/" + self.__live_id+ "/start/")
        print(req.json())
        print()

    def encerrar(self):
        print("Encerrando stream")
        #signed_body=d8495776e76a44abd12d7c6b753ebb7bbcf8b0fddb30b888fb6a8377a0404d21.{"_csrftoken":"KHYH0aAV1MAuodATGwQL6pSiViT79Im4","_uid":"32566605591","_uuid":"c2e407d1-0c08-40a4-afd4-a90e00ec6251","end_after_copyright_warning":"false"}&ig_sig_key_version=4
        req = self.__session.post("https://i.instagram.com/api/v1/live/" + self.__live_id+ "/end_broadcast/")
        print(req.json())
        print()