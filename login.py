import instagram
from flask import request, redirect, render_template

class Login:
    def __init__(self, app):
        self.__logado = False
        self.rotas(app)

    @property
    def value(self):
        return self.__logado

    def rotas(self, app):
        @app.route("/login", methods=["GET"])
        def login():
            if self.__logado:
                return redirect("/")

            status = request.args.get("status")
            if status is None:
                status = ""

            return render_template("login.html", status=status)

        @app.route("/login", methods=["POST"])
        def fazerLogin():
            if self.__logado:
                return redirect("/")
            
            usuario = request.form.get("usuario")
            senha = request.form.get("senha")

            try:
                instagram.fazerLogin(usuario, senha)
                self.__logado = usuario

                return redirect("/")
            except Exception as e:
                print (e)
                return redirect("/login?status=Login invalido!")

        @app.route("/login/sair", methods=["GET"])
        def desconectar():
            if not self.__logado:
                return redirect("/")
            
            instagram.desconectar()
            self.__logado = False
            return redirect("/?sair=true")