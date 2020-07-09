from .constants import Constants

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
