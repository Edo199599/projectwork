import pandas as pd
from modello_base import ModelloBase
from collections import Counter
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

_FILE_PATH = "dataset/data_book.csv"

class ModelloBook(ModelloBase):

    def __init__(self):
        self.dataframe = pd.read_csv(_FILE_PATH)
        self.df_pulito = self.dataframe_sistemato()
        # self.df_sistemato_successo_libro = self.sistemazione_dataframe_uno()
        # self.df_sistemato_successo_autore = self.sistemazione_dataframe_due()
        # self.correlazione_spearman("voto_medio", "times_featured")
        # self.correlazione_spearman("numero_recensioni", "times_featured")
        # self.grafico_spearman("numero_recensioni", "times_featured")
        # self.individuazione_correlazioni()
        # self.individuazione_correlazioni_traccia2()
        # self.grafico_spearman_traccia2("avg_reviews", "books_count")
        # self.correlazione_spearman_traccia2("main_genre", "books_count")
        # self.grafico_spearman_traccia2("main_genre", "books_count")
        # self.grafico_ripartizione()
        # self.grafico_successo()
        # self.df_successo = self.dataframe_successo()
        # self.grafico_ripartizione_successo()
        self.creazione_colonne_id()


        # self.correlazione_spearman("prezzo", "times_featured")
        # self.grafico_spearman("voto_medio", "times_featured")
        # self.grafico_spearman("prezzo", "times_featured")
        # self.regressione_lineare_semplice("voto_medio")
        # self.regressione_lineare_semplice("numero_recensioni")
        # self.regressione_lineare_semplice("prezzo")

    def dataframe_sistemato(self):
        df_sistemato = self.dataframe.copy()
        df_sistemato = df_sistemato.rename(columns={"Name":"nome", "Author":"autore", "User Rating":"voto_medio","Reviews":"numero_recensioni" ,"Year":"anno","Price":"prezzo" , "Genre":"genere"})
        # metto la maiuscola alla prima lettera di ogni parola
        df_sistemato["nome"] = df_sistemato["nome"].str.title()
        return df_sistemato

    # metodo di sistemazione del dataframe (per 1^ traccia richiesta)
    def sistemazione_dataframe_uno(self):
        df_sistemato = self.df_pulito.copy()
        # aggiunta colonna di registrazione presenze libro tra best seller nel dataset
        df_sistemato["times_featured"] = df_sistemato["nome"].map(df_sistemato.groupby("nome")["anno"].nunique())
        # rimozione osservazioni per libri duplicati (manteniamo solo anno più recente)
        df_ordinato = df_sistemato.sort_values(by="anno", ascending=False)
        df_sistemato = df_ordinato.drop_duplicates(subset="nome", keep="first")
        return df_sistemato

    # metodo di sistemazione del dataframe (per 2^ traccia richiesta)
    def sistemazione_dataframe_due(self):
        df_sistemato = self.df_pulito.copy()
        # nuovo dataframe con aggregazione per autore e calcolo valori medi caratteristiche
        df_sistemato = df_sistemato.groupby("autore").agg(
            books_count=("nome", "count"),
            avg_price=("prezzo", "mean"),
            avg_rating=("voto_medio", "mean"),
            avg_reviews=("numero_recensioni", "mean"),
            main_genre=("genere", lambda x: Counter(x).most_common(1)[0][0]),
            avg_year=("anno", "mean")
        ).reset_index()
        df_sistemato["avg_year"] = df_sistemato["avg_year"].astype(int)
        return df_sistemato

    def correlazione_spearman(self, column, target):
        # calcolo correlazione di Spearman tra due colonne
        correlation, p_value = spearmanr(self.df_sistemato_successo_libro[column], self.df_sistemato_successo_libro[target])
        print(f"Correlazione di Spearman tra {column} e {target} è pari a {correlation}")
        print(f"Il p-value risultate dal test della correlazione di Spearman è {p_value}")


    def grafico_spearman(self, column, target):
        plt.figure(figsize=(10, 6))
        # grafico a linee è plt.plot()
        plt.scatter(self.df_sistemato_successo_libro[column], self.df_sistemato_successo_libro[target])
        plt.title(f"{column} e {target}")
        plt.xlabel(column)
        plt.ylabel(target)
        plt.show()

    def individuazione_correlazioni(self):
        colonne_da_escludere = ["nome", "autore", "genere"]
        df_sistemato_successo_libro_numeriche = self.df_sistemato_successo_libro.drop(columns=colonne_da_escludere)
        matrice_heatmap_correlazioni = df_sistemato_successo_libro_numeriche.corr(method="spearman")
        plt.figure(figsize=(15,10))
        sns.heatmap(matrice_heatmap_correlazioni, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Matrice di correlazione")
        plt.xticks(rotation=20, ha="right")
        plt.show()

    def regressione_lineare_semplice(self, col):
        y = self.df_sistemato_successo_libro[["times_featured"]].values.reshape(-1, 1)
        x = self.df_sistemato_successo_libro[[col]].values.reshape(-1, 1)
        regressione = LinearRegression()
        regressione.fit(x, y)
        print(f"Punteggio della regressione: {regressione.score(x, y)}")
        retta_regressione = regressione.predict(x)
        plt.scatter(x, y, color="blue", s=10, label="Regressione")
        plt.title(f"Regressione lineare semplice tra {col} e times featured")
        plt.xlabel(f"{col}")
        plt.ylabel("Times featured")
        plt.plot(x, retta_regressione, color="red", label="Regr. lineare")
        plt.show()


# ------------------------------- TRACCIA 2 -------------------------------

    def individuazione_correlazioni_traccia2(self):
        colonne_da_escludere = ["autore", "main_genre"]
        df_sistemato_successo_autore_numeriche = self.df_sistemato_successo_autore.drop(columns=colonne_da_escludere)
        matrice_heatmap_correlazioni = df_sistemato_successo_autore_numeriche.corr(method="spearman")
        plt.figure(figsize=(15,10))
        sns.heatmap(matrice_heatmap_correlazioni, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Matrice di correlazione")
        plt.xticks(rotation=20, ha="right")
        plt.show()

    def grafico_spearman_traccia2(self, column, target):
        plt.figure(figsize=(10, 6))
        # grafico a linee è plt.plot()
        if column == "main_genre":
            plt.bar(self.df_sistemato_successo_autore[column], self.df_sistemato_successo_autore[target])
        elif column == "avg_reviews":
            plt.scatter(self.df_sistemato_successo_autore[column], self.df_sistemato_successo_autore[target])
        plt.title(f"{column} e {target}")
        plt.xlabel(column)
        plt.ylabel(target)
        plt.show()

    def correlazione_spearman_traccia2(self, column, target):
        # calcolo correlazione di Spearman tra due colonne
        correlation, p_value = spearmanr(self.df_sistemato_successo_autore[column],self.df_sistemato_successo_autore[target])
        print(f"Correlazione di Spearman tra {column} e {target} è pari a {correlation}")
        print(f"Il p-value risultate dal test della correlazione di Spearman è {p_value}")

    def grafico_ripartizione(self):
        libri_fiction = self.df_sistemato_successo_autore["main_genre"].value_counts()
        libri_fiction.plot(kind="pie", autopct="%1.1f%%", startangle=90, colors=["red", "green"])
        plt.title("Genere prevalente")
        plt.ylabel("")
        plt.show()

    def grafico_successo(self):
        plt.figure(figsize=(10, 6))
        plt.scatter(self.df_sistemato_successo_autore["avg_rating"], self.df_sistemato_successo_autore["books_count"], s=60)
        plt.title("Successo libro")
        plt.xlabel("Voto medio")
        plt.ylabel("Times featured")
        plt.show()

    def dataframe_successo(self):
        df = self.df_sistemato_successo_autore.copy()
        df["indice_successo"] = df["avg_rating"] * (1-np.exp(-df["books_count"]/3))
        df = df.sort_values(by="indice_successo", ascending=False)
        df_successo = df[0:20]

        # creiamo un secondo database con solo gli autori che abbiano pubblicato più di 7 libri
        # df_successo = df[(df["books_count"] > 6) & (df["avg_rating"] > 4.5)]
        return df_successo

    def grafico_ripartizione_successo(self):
        libri_fiction = self.df_successo["main_genre"].value_counts()
        libri_fiction.plot(kind="pie", autopct="%1.1f%%", startangle=90, colors=["red", "green"])
        plt.title("Genere prevalente tra i Best Seller")
        plt.ylabel("")
        plt.show()

    def creazione_colonne_id(self):
        mappa_autori = dict(zip(self.df_pulito["autore"].unique(), range(self.df_pulito["autore"].nunique())))
        self.df_pulito["id_autore"] = self.df_pulito["autore"].map(mappa_autori) +1
        mappa_generi = dict(zip(self.df_pulito["genere"].unique(), range(self.df_pulito["genere"].nunique())))
        self.df_pulito["id_genere"] = self.df_pulito["genere"].map(mappa_generi) + 1
        # con pandas trasformare il dataframe in un file csv si fa con il metodo to_csv()
        # nel nostro caso diventa df_pulito.to_csv("dataset/data_book_pulito.csv", index=False)
        # index = False per non scrivere l'indice del dataframe nel file csv
        # df_autore = self.df_pulito["autore"].drop_duplicates()
        # df_autore.to_csv("dataset/tabella.autore.csv", index=False, header=False)
        colonne_da_droppare = ["autore", "genere"]
        colonne_da_reindexare = ["nome", "id_autore", "voto_medio", "numero_recensioni", "prezzo", "anno", "id_genere"]
        df_pulito = self.df_pulito.drop(columns=colonne_da_droppare)
        df_pulito = df_pulito.reindex(columns=colonne_da_reindexare)
        # df_pulito.to_csv("dataset/tabella_libri.csv", index=False, header=False)
        return 0

modello = ModelloBook()
# modello.analisi_generali(modello.df_sistemato_successo_autore)
# print(modello.df_sistemato.head().to_string())
# print(modello.df_sistemato.groupby("nome").count().sort_values("autore", ascending=True).to_string())
# modello.analisi_valori_univoci(modello.df_sistemato)

# per sostituire il valore in una cella usiamo la funzione loc
# df.loc[df["colonna"] == "valore", "colonna"] = "nuovo_valore"

# print(modello.df_sistemato_successo_libro.sort_values("times_featured", ascending=False).head().to_string())



