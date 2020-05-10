class Usuario:
    def __init__(self, id, nome, img):
        self.id = id
        self.nome = nome
        self.img = img

    def toJson(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "img": self.img
        }