import instagram
from flask import request, redirect, render_template

class Login:
    def __init__(self, app):
        self.rotas(app)

    @property
    def value(self):
        logado = request.cookies.get("usuario")
        if logado is None:
            return False
        return logado

    def rotas(self, app):
        @app.route("/login", methods=["GET"])
        def login():
            if self.value:
                return redirect("/")

            status = request.args.get("status")
            if status is None:
                status = ""

            return render_template("login.html", status=status)

        @app.route("/login", methods=["POST"])
        def fazerLogin():
            if self.value:
                return redirect("/")
            
            usuario = request.form.get("usuario")
            senha = request.form.get("senha")

            loginMgr = instagram.LoginMgr(instagram.getSession)

            try:
                loginMgr.fazerLogin(usuario, senha)

                res = redirect("/")
                cookies = loginMgr.getCookies()
                for c in cookies:
                    if ".com" not in c.domain:
                        res.set_cookie(c.name, c.value)
                    else:
                        res.set_cookie("i." + c.name, c.value)

                return res
            except Exception as e:
                print("Erro no login: %s" % e)
                return redirect("/login?status=Login invalido!")

        @app.route("/login/sair", methods=["GET"])
        def desconectar():
            if not self.value:
                return redirect("/")

            res = redirect("/?sair=true")
            for c in request.cookies:
                print("Deletando cookie: " + c)
                res.delete_cookie(c)
            
            instagram.desconectar()

            return res