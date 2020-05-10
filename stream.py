import instagram
from flask import request, redirect, render_template

class Stream:
    def __init__(self, app, login):
        self.__stream = None
        self.__login = login
        self.rotas(app)

    @property
    def value(self):
        return self.__stream

    def rotas(self, app):
        @app.route("/stream/criar")
        def criarStream():
            if not self.__login.value:
                print("Erro: Faça o login antes de tentar criar uma stream")
                return redirect("/login")

            self.__stream = instagram.getStream()

            return redirect("/")

        @app.route("/stream/iniciar")
        def iniciarStream():
            if not self.__login.value:
                print("Erro: Faça o login antes de tentar iniciar uma stream")
                return redirect("/login")

            if self.__stream is None:
                print("Erro: Você deve criar o stream antes de iniciar")
                return redirect("/?erro&mensagem=Você deve criar o stream antes de iniciar")
            
            self.__stream.iniciar()
            return redirect("/")

        @app.route("/stream/encerrar")
        def encerrarStream():
            if not self.__login.value:
                print("Erro: Faça o login antes de tentar encerrar uma stream")
                return redirect("/login")

            if self.__stream is None:
                print("Erro: Não existe streams para encerrar")
                return redirect("/?erro&mensagem=Não existe streams para encerrar")

            self.__stream.encerrar()
            self.__stream = None
            return redirect ("/?mensagem=Stream encerrado!")

        @app.route("/stream/info")
        def getInfo():
            return instagram.getInfo(self.__stream)