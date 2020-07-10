from .constants import Constants
import os

class Midia:
    def __init__(self, getSession):
        self.__getSession = getSession

    def info(self, stream_id):
        self.__session = self.__getSession()

        usuario = self.__session.cookies["ds_user"]

        req = self.__session.get("https://i.instagram.com/api/v1/live/%s/info" % stream_id)
        res = req.json()
        url = res["dash_playback_url"]

        req = self.__session.get(url)
        res = url + "\n"
        res += req.text
        return res

    def __lerMidia(self, url):
        url = "https://instagram.fnat1-1.fna.fbcdn.net/hvideo-" + url
        req = self.__session.get(url, stream=True, headers={
            'Accept': '*/*'
        })
        req.raise_for_status()
        return req.content

    def midia(self, url, stream_id, iniciado):
        self.__session = self.__getSession()
        
        initFile = os.path.expandvars("%temp%\\")
        initFile += ".midia_" + stream_id + "-init." + url[-3:]
        content = bytes()

        # Se o arquivo solicitado não for o init, retorne os bytes
        # Se o arquivo solicitado for o init e não tiver sido baixado, faça o download e retorne os bytes
        if not url[-8:].startswith("init"):
            content = self.__lerMidia(url)
        elif not os.path.isfile(initFile):
            content = self.__lerMidia(url)

            f = open(initFile, "wb")
            f.write(content)
            f.close()
            return content
        elif not iniciado: # Se o arquivo solicitado for o init e tiver sido baixado, leia e retorne os bytes
            f = open(initFile, "rb")
            content = f.read()
            f.close()

        return content 
