import instagram
from flask import request, redirect, render_template

class Stream:
    def __init__(self, app, login):
        self.__stream = None
        self.__login = login
        self.rotas(app)

    @property
    def value(self):
        self.__stream = instagram.getStream(False)
        return self.__stream

    def refreshStream(self):
        self.__stream = None

    def rotas(self, app):
        @app.route("/stream/criar")
        def criarStream():
            if not self.__login.value:
                print("Erro: Faça o login antes de tentar criar uma stream")
                return redirect("/login")

            self.__stream = instagram.getStream()

            res = redirect("/")
            res.set_cookie("stream_id", self.__stream.id)
            res.set_cookie("stream_url", self.__stream.url)
            res.set_cookie("stream_key", self.__stream.key)
            res.set_cookie("stream_status", "criado")

            cookies = self.__stream.getCookies()
            for c in cookies:
                if ".com" not in c.domain:
                    res.set_cookie(c.name, c.value)
                else:
                    res.set_cookie("i." + c.name, c.value)

            return res

        @app.route("/stream/iniciar")
        def iniciarStream():
            if not self.__login.value:
                print("Erro: Faça o login antes de tentar iniciar uma stream")
                return redirect("/login")

            self.__stream = self.value
            if self.__stream is None:
                print("Erro: Você deve criar o stream antes de iniciar")
                return redirect("/?erro&mensagem=Você deve criar o stream antes de iniciar")
            
            self.__stream.iniciar()

            res = redirect("/")
            res.set_cookie("stream_status", "iniciado")
            res.set_cookie("stream_startTime", str(self.__stream.startTime))

            cookies = self.__stream.getCookies()
            for c in cookies:
                if ".com" not in c.domain:
                    res.set_cookie(c.name, c.value)
                else:
                    res.set_cookie("i." + c.name, c.value)

            return res

        @app.route("/stream/encerrar")
        def encerrarStream():
            if not self.__login.value:
                print("Erro: Faça o login antes de tentar encerrar uma stream")
                return redirect("/login")

            self.__stream = self.value
            if self.__stream is None:
                print("Erro: Não existe streams para encerrar")
                return redirect("/?erro&mensagem=Não existe streams para encerrar")

            self.__stream.encerrar()

            res = redirect ("/?mensagem=Stream encerrado!")
            res.delete_cookie("stream_id")
            res.delete_cookie("stream_url")
            res.delete_cookie("stream_key")
            res.delete_cookie("stream_status")

            cookies = self.__stream.getCookies()
            for c in cookies:
                if ".com" not in c.domain:
                    res.set_cookie(c.name, c.value)
                else:
                    res.set_cookie("i." + c.name, c.value)

            self.__stream = None
            return res

        @app.route("/stream/info")
        def getInfo():
            self.__stream = self.value
            return instagram.getInfo(self.__stream)