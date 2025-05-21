from flask import Flask
from service.libro_service import LibroService

app = Flask(__name__)
libro_service = LibroService()

# endpoint #1 lista libri
# localhost:5050/libri/get
@app.get("/libri/get")
def endpoint_lista_libri():
    return libro_service.elenco_libri()



if __name__ == "__main__":
    app.run(port=5050)