import instagram
import time
import flask
from flask import Flask, render_template

app = Flask(__name__)

comentarios = []
stream = None
logado = False

@app.route("/login", methods=["POST"])
def fazerLogin():
    try:
        instagram.fazerLogin("USUARIO", "SENHA")
        return "Logado com sucesso!"
    except:
        return "Login invalido!"

@app.route("/stream/criar")
def criarStream():
    global stream
    stream = instagram.getStream()

    return {
        "live_id" : stream.id,
        "stream_url" : stream.url,
        "stream_key" : stream.key
    }

@app.route("/stream/iniciar")
def iniciarStream():
    if stream is None:
        return "Erro: Você deve criar o stream antes de iniciar"
    
    stream.iniciar()
    return "Stream Iniciado"

@app.route("/stream/encerrar")
def encerrarStream():
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
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=80, debug=True)