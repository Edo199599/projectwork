from flask import Flask
from service.libro_service import LibroService
from service.autori_service import AutoriService

app = Flask(__name__)
libro_service = LibroService()
autore_service = AutoriService()

# ------------------------------------------ ENDPOINT LIBRI ------------------------------------------- #

# endpoint #1 lista libri
# localhost:5050/libri/get
@app.get("/libri/get")
def endpoint_lista_libri():
    return libro_service.elenco_libri()

# endpoint #2 ricerca libro
# localhost:5050/libri/get/<string:parola_chiave>
@app.get("/libri/get/<string:parola_chiave>")
def endpoint_ricerca_libro(parola_chiave):
    return libro_service.ricerca_libri(parola_chiave)

# -------------------------------------------- ENDPOINT AUTORI ------------------------------------------- #

# endpoint #1 lista autori
# localhost:5050/autori/get
@app.get("/autori/get")
def endpoint_lista_autori():
    return autore_service.elenco_autori()

# endpoint #2 ricerca autore
# localhost:5050/autori/get/<string:parola_chiave>
@app.get("/autori/get/<string:parola_chiave>")
def endpoint_ricerca_autore(parola_chiave):
    return autore_service.ricerca_autore(parola_chiave)

# ---------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    app.run(port=5050)