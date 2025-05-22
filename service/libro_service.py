from repository.repository import Repository
from model.libro import Libro
from model.autore import Autore
from model.genere import Genere

class LibroService:

    def __init__(self):
        self.repository = Repository()

    def elenco_libri(self):
        sql = "SELECT * FROM lista_libri"
        ottenuto_db = self.repository.recupero_multiplo(sql)
        print(ottenuto_db)
        if isinstance(ottenuto_db, str):
            return {"codice": 500, "messaggio": ottenuto_db}, 500
        libri = []
        for record in ottenuto_db:
            genere = Genere(genere=record[6])
            autore = Autore(nome=record[1])
            libro = Libro(titolo=record[0], autore=autore, genere=genere, voto_medio=record[2],
                          numero_recensioni=record[3], prezzo=record[4], anno=record[5])
            libri.append(libro)
        return [libro.serializzazione() for libro in libri], 200

    def ricerca_libri(self, parola_chiave):
        sql = "SELECT * FROM lista_libri WHERE titolo LIKE %s"
        ottenuto_db = self.repository.recupero_multiplo(sql, (f'%{parola_chiave}%',))
        if isinstance(ottenuto_db, str):
            return {"codice": 500, "messaggio": ottenuto_db}, 500
        if not ottenuto_db:
            return {"codice": 204, "messaggio": "Nessun libro trovato"}, 204
        libri = []
        for record in ottenuto_db:
            genere = Genere(genere=record[6])
            autore = Autore(nome=record[1])
            libro = Libro(titolo=record[0], autore=autore, genere=genere, voto_medio=record[2],
                          numero_recensioni=record[3], prezzo=record[4], anno=record[5])
            libri.append(libro)
        return [libro.serializzazione() for libro in libri], 200