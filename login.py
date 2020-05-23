import instagram
from flask import request, redirect, render_template

class Login:
    def __init__(self, app):
        self.rotas(app)

    @property
    def value(self):
        logado = request.cookies.get("usuario")
        
        if not self.precisaAutentificar:
            if logado is not None:
                return logado

        return False

    @property
    def precisaAutentificar(self):
        auth = request.cookies.get("a")

        if auth is None or auth==False:
            return False
        return True

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
                if loginMgr.auth:
                    res = redirect("/login/auth")
                    cookies = loginMgr.getCookies()
                    for c in cookies:
                        if ".com" not in c.domain:
                            res.set_cookie(c.name, c.value)
                        else:
                            res.set_cookie("i." + c.name, c.value)
                    
                    return res

                print("Erro no login: %s" % e)
                return redirect("/login?status=Login invalido!")

        @app.route("/login/sair", methods=["GET"])
        def desconectar():
            if not self.value:
                return redirect("/")

            res = redirect("/?sair=true")
            print("Deletando cookies...")
            for c in request.cookies:
                res.delete_cookie(c)
            
            loginMgr = instagram.LoginMgr(instagram.getSession)
            loginMgr.desconectar()

            return res

        @app.route("/login/auth", methods=["GET"])
        def pedirAutentificacao():
            if not self.precisaAutentificar:
                return redirect("/")

            formaVerificacao = request.args.get("formaVerificacao")
            if formaVerificacao is not None:
                formaVerificacao = int(formaVerificacao)
                loginMgr = instagram.LoginMgr(instagram.getSession)
                loginMgr.auth = request.cookies.get("a")

                ultimosDigitos = loginMgr.enviarCodigo(formaVerificacao)
                return render_template("auth.html", formaVerificacao=formaVerificacao, ultimosDigitos=ultimosDigitos)

            return render_template("auth.html", formaVerificacao=formaVerificacao)

        @app.route("/login/auth", methods=["POST"])
        def autentificar():
            if not self.precisaAutentificar:
                return redirect("/")
                
            codigo = request.form.get("codigo")

            loginMgr = instagram.LoginMgr(instagram.getSession)
            loginMgr.auth = request.cookies.get("a")

            verificado = loginMgr.verificar(codigo)

            if verificado:
                res = redirect("/")

                cookies = loginMgr.getCookies()
                for c in cookies:
                    if ".com" not in c.domain:
                        res.set_cookie(c.name, c.value)
                    else:
                        res.set_cookie("i." + c.name, c.value)

                res.delete_cookie("a")

                return res
            return redirect("/login?status=Não Foi possivel verificar!")