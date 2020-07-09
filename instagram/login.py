from .constants import Constants
from flask import request

class LoginMgr:
    def __init__(self, getSession):
        self.__cookies = {}
        self.__session = None
        self.__getSession = getSession
        self.auth = False

    def getCookies(self):
        return self.__cookies

    def fazerLogin(self, usuario, senha):
        print("Fazendo login no instagram @%s...." % usuario)

        self.__session = self.__getSession()
        self.__session.cookies.clear_session_cookies()

        req = self.__session.get("https://i.instagram.com/")
        token = self.__session.atualizarCSRFToken(req.cookies["csrftoken"])

        req = self.__session.post("https://i.instagram.com/api/v1/accounts/login/", data={
            "guid": Constants.DEVICE,
            "device_id": Constants.ANDROID_DEVICE,
            "username": usuario,
            "password": senha
        })
        token = self.__session.atualizarCSRFToken(req.cookies["csrftoken"])

        res = req.json()
        
        self.__cookies = self.__session.cookies.copy()
        self.__cookies.update({"usuario": req.cookies["ds_user"]})
        self.__cookies.update({"csrf_token": token})

        if res["status"] != "ok" or res["logged_in_user"] is None:
            if res["message"] == "challenge_required":
                self.auth = res["challenge"]["api_path"]
                self.__cookies.update({"a": self.auth})
                raise Exception("Erro no login: Necessário autentificar!")
            raise Exception("Erro no login: %s" % res)

        print("Logado com sucesso!")
        print()

    def enviarCodigo(self, por):
        if por < 0 or por > 1:
            print("Escolha invalida!")
            return
            
        self.__session = self.__getSession()

        req = self.__session.post("https://i.instagram.com/api/v1" + self.auth, data={
            "choice": por,
            "_csrftoken": self.__session.headers.get("X-CSRFToken"),
            "guid": Constants.DEVICE,
            "device_id": Constants.ANDROID_DEVICE
        })
        token = self.__session.atualizarCSRFToken(req.cookies["csrftoken"])
        res = req.json()

        self.__cookies.update({"csrf_token": token})

        if por == 0:
            return res["step_data"]["phone_number_preview"]

        return res["step_data"]["contact_point"]

    def verificar(self, codigo):
        self.__session = self.__getSession()

        req = self.__session.post("https://i.instagram.com/api/v1" + self.auth, data={
            "security_code": codigo,
            "_csrftoken": self.__session.headers.get("X-CSRFToken"),
            "guid": Constants.DEVICE,
            "device_id": Constants.ANDROID_DEVICE
        })
        token = self.__session.atualizarCSRFToken(req.cookies["csrftoken"])
        res = req.json()

        if res["status"] == "ok":
            logado = res["logged_in_user"]
            if logado is not None and len(logado) > 0:
                self.__cookies = self.__session.cookies.copy()
                self.__cookies.update({"csrf_token": token})

                return True

        return False

    def desconectar(self):
        self.__session = self.__getSession()

        req = self.__session.post("https://www.instagram.com/accounts/logout/ajax/")
        self.__cookies.clear()