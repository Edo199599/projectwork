from model.genere import Genere
from repository.repository import Repository
from model.autore import Autore
from model.libro import Libro

class AutoriService:

    def __init__(self):
        self.repository = Repository()


    def elenco_autori(self):
        sql = "SELECT * FROM autori"
        ottenuto_db = self.repository.recupero_multiplo(sql)
        if isinstance(ottenuto_db, str):
            return {"codice": 500, "messaggio": ottenuto_db}, 500
        sql_libri = "SELECT * FROM lista_libri"
        ottenuto_db_libri = self.repository.recupero_multiplo(sql_libri)
        autori = []
        for record in ottenuto_db:
            libri_autore = []
            autore = Autore(id=record[0], nome=record[1])
            for record_libro in ottenuto_db_libri:
                if autore.nome == record_libro[1]:
                    genere = Genere(genere=record_libro[6])
                    libro = Libro(titolo=record_libro[0], genere=genere, voto_medio=record_libro[2], numero_recensioni=record_libro[3],
                                  prezzo=record_libro[4], anno=record_libro[5])
                    libri_autore.append(libro)
            autore.libri = libri_autore
            autori.append(autore)
        return [autore.serializzazione() for autore in autori], 200

    def ricerca_autore(self, parola_chiave):
        sql = 'SELECT * FROM autori WHERE nome LIKE %s'
        ottenuto_db = self.repository.recupero_multiplo(sql, (f'%{parola_chiave}%',))
        if isinstance(ottenuto_db, str):
            return {"codice": 500, "messaggio": ottenuto_db}, 500
        if not ottenuto_db:
            return {"codice": 204, "messaggio": "Autore non trovato"}, 204
        sql_libri = "SELECT * FROM lista_libri"
        ottenuto_db_libri = self.repository.recupero_multiplo(sql_libri)
        autori = []
        for record in ottenuto_db:
            libri_autore = []
            autore = Autore(nome=record[1])
            for record_libro in ottenuto_db_libri:
                if autore.nome == record_libro[1]:
                    genere = Genere(genere=record_libro[6])
                    libro = Libro(titolo=record_libro[0], genere=genere, voto_medio=record_libro[2], numero_recensioni=record_libro[3],
                                  prezzo=record_libro[4], anno=record_libro[5])
                    libri_autore.append(libro)
            autore.libri = libri_autore
            autori.append(autore)
        return [autore.serializzazione() for autore in autori], 200