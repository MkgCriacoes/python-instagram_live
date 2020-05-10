import instagram
import time
import flask
from flask import Flask, render_template, request, redirect
import json

from login import Login
from stream import Stream

app = Flask(__name__)

login = Login(app)
stream = Stream(app, login)

@app.route("/comentarios")
def getComentarios():
    lastComent = request.args.get("lastComent")

    comentarios = instagram.getComentarios(stream.value, lastComent)
    if (len(comentarios) > 0):
        print("Novos comentários")

    return json.dumps(comentarios)

@app.route("/")
def index():
    if not login.value:
        return redirect("/login")

    erro = request.args.get("erro")
    mensagem = request.args.get("mensagem")

    return render_template("index.html", login=login.value, stream=stream.value, erro=erro, mensagem=mensagem)

if __name__ == '__main__':
    app.run(port=80, debug=True)