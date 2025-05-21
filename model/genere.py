

class Genere:

    def __init__(self, id=None, genere=None):
        self.id = id
        self.genere = genere

    def serializzazione_per_libro(self):
        return {
            "genere": self.genere
        }