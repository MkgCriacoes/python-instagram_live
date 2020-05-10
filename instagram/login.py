class LoginMgr:
    def __init__(self, session):
        self.__session = session

    def atualizarCSRFToken(self, token):
        self.__session.headers.update({"X-CSRFToken": token})

    def fazerLogin(self, usuario, senha):
        print("Fazendo login no instagram @%s...." % usuario)

        req = self.__session.get("https://www.instagram.com/")
        self.atualizarCSRFToken(req.cookies["csrftoken"])

        req = self.__session.post("https://www.instagram.com/accounts/login/ajax/", data={
            "username": usuario,
            "password": senha
        })
        res = req.json()
        self.atualizarCSRFToken(req.cookies["csrftoken"])

        if res["status"] != "ok" or res["authenticated"] != True:
            raise Exception("Erro no login: %s" % res)

        print("Logado com sucesso!")
        print()

    def desconectar(self):
        req = self.__session.post("https://www.instagram.com/accounts/logout/ajax/")
        res = req.text
        print(res)