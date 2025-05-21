from repository.repository import Repository
from model.libro import Libro

class LibroService:

    def __init__(self):
        self.repository = Repository()

    def elenco_libri(self):
        sql = "SELECT l.titolo, l.voto_medio, l.numero_recensioni, l.prezzo, l.anno FROM libri l JOIN generi g ON l.fk_id_genere=g.id_genere JOIN autori a ON l.fk_id_autore=a.id_autore;"
        ottenuto_db = self.repository.recupero_multiplo(sql)
        print(ottenuto_db)
        if isinstance(ottenuto_db, str):
            return {"codice": 500, "messaggio": ottenuto_db}, 500
        return [Libro(*record).serializzazione() for record in ottenuto_db], 200