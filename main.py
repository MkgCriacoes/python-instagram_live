import instagram
import time
import flask
from flask import Flask, render_template, request, redirect
import json

from login import Login
from stream import Stream
from comentario import Comentario
from midia import Midia

app = Flask(__name__)

login = Login(app)
stream = Stream(app, login)
comentario = Comentario(app, login, stream)
midia = Midia(app, stream)

@app.route("/")
def index():
    sair = request.args.get("sair")
    if sair is not None:
        stream.refreshStream()

    if not login.value:
        return redirect("/login")

    erro = request.args.get("erro")
    mensagem = request.args.get("mensagem")

    return render_template("index.html", login=login.value, stream=stream.value, erro=erro, mensagem=mensagem)

if __name__ == '__main__':
    app.run(port=80, debug=False)