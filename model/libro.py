
class Libro:

    def __init__(self, id=None, titolo=None, autore=None, voto_medio=None, numero_recensioni=None, prezzo=None, anno=None, genere=None):
        self.id = id
        self.titolo = titolo
        self.autore = autore
        self.voto_medio = voto_medio
        self.numero_recensioni = numero_recensioni
        self.prezzo = prezzo
        self.anno = anno
        self.genere = genere


    def serializzazione(self):
        return {
            "titolo": self.titolo,
            "autore": self.autore.serializzazione_per_libro(),
            "voto_medio": self.voto_medio,
            "numero_recensioni": self.numero_recensioni,
            "prezzo": self.prezzo,
            "anno": self.anno,
            "genere": self.genere.serializzazione_per_libro()
        }

    def serializzazione_per_autore(self):
        return {
            "titolo": self.titolo,
            "voto_medio": self.voto_medio,
            "numero_recensioni": self.numero_recensioni,
            "prezzo": self.prezzo,
            "anno": self.anno,
            "genere": self.genere.serializzazione_per_libro()
        }