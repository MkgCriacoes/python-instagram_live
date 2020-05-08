import instagram
import time
import flask
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

comentarios = []
stream = None
logado = False

@app.route("/login", methods=["GET"])
def login():
    if logado:
        return redirect("/")

    status = request.args.get("status")
    if status is None:
        status = ""

    return render_template("login.html", status=status)

@app.route("/login", methods=["POST"])
def fazerLogin():
    global logado

    if logado:
        return redirect("/")
    
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    try:
        instagram.fazerLogin(usuario, senha)
        logado = usuario

        print("Logado com sucesso!")
        return redirect("/")
    except:
        print("Login invalido!")
        return redirect("/login?status=Login invalido!")

@app.route("/stream/criar")
def criarStream():
    global stream

    if not logado:
        print("Erro: Faça o login antes de tentar criar uma stream")
        return redirect("/login")

    stream = instagram.getStream()

    return {
        "live_id" : stream.id,
        "stream_url" : stream.url,
        "stream_key" : stream.key
    }

@app.route("/stream/iniciar")
def iniciarStream():
    if not logado:
        print("Erro: Faça o login antes de tentar iniciar uma stream")
        return redirect("/login")

    if stream is None:
        return "Erro: Você deve criar o stream antes de iniciar"
    
    stream.iniciar()
    return "Stream Iniciado"

@app.route("/stream/encerrar")
def encerrarStream():
    if not logado:
        print("Erro: Faça o login antes de tentar encerrar uma stream")
        return redirect("/login")

    if stream is None:
        return "Erro: Não existe streams para encerrar"

    stream.encerrar()
    stream = None
    return "Stream Encerrado"

@app.route("/responder/<id>", methods=["POST"])
def responder(id):
    #instagram.responderComentario()
    pass

@app.route("/comentarios")
def getComentarios():
    global comentarios
    
    novosComentarios = [] #instagram.getComentarios()
    if comentarios == novosComentarios:
        time.sleep(0.5)
        return comentarios
    
    comentarios = novosComentarios
    print("Novo comentário")

    return comentarios

@app.route("/")
def index():
    if not logado:
        return redirect("/login")

    return render_template("index.html", login=logado)

if __name__ == '__main__':
    app.run(port=80, debug=True)