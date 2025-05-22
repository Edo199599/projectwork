
class Autore:

    def __init__(self, id=None, nome=None, libri=None):
        self.id = id
        self.nome = nome
        self.libri = libri if libri else []

    def serializzazione(self):
        return {
            "nome": self.nome,
            "libri": [libro.serializzazione_per_autore() for libro in self.libri]
        }

    def serializzazione_per_libro(self):
        return {
            "nome": self.nome
        }

