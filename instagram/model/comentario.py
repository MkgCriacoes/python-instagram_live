class Comentario:
    def __init__(self, id, dt_envio, texto, usuario):
        self.id = id
        self.dt_envio = dt_envio
        self.texto = texto
        self.usuario = usuario

    def ocultar(self):
        pass

    def toJson(self):
        return {
            "id": self.id,
            "dt_envio": self.dt_envio,
            "texto": self.texto,
            "usuario": self.usuario.toJson()
        }