from flask import request

class LoginMgr:
    def __init__(self, getSession):
        self.__cookies = {}
        self.__session = None
        self.__getSession = getSession

    def getCookies(self):
        return self.__cookies

    def fazerLogin(self, usuario, senha):
        print("Fazendo login no instagram @%s...." % usuario)

        self.__session = self.__getSession()
        self.__session.cookies.clear_session_cookies()

        req = self.__session.get("https://www.instagram.com/")
        token = self.__session.atualizarCSRFToken(req.cookies["csrftoken"])

        req = self.__session.post("https://www.instagram.com/accounts/login/ajax/", data={
            "username": usuario,
            "password": senha
        })
        token = self.__session.atualizarCSRFToken(req.cookies["csrftoken"])

        res = req.json()
        
        self.__cookies = self.__session.cookies.copy()
        self.__cookies.update({"usuario": usuario})
        self.__cookies.update({"csrf_token": token})

        if res["status"] != "ok" or res["authenticated"] != True:
            raise Exception("Erro no login: %s" % res)

        print("Logado com sucesso!")
        print()

    def desconectar(self):
        self.__session = self.__getSession()

        req = self.__session.post("https://www.instagram.com/accounts/logout/ajax/")
        res = req.text
        print(res)
        self.__cookies.clear()