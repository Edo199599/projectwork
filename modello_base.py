from abc import ABC

# per una descrizione più dettagliata dei singoli metodi guardare il file machine_learning/introduzione/analisi_dataframe.py


# definizione di una classe astratta per la centralizzazione delle operazioni comuni
class ModelloBase(ABC):

# metodi di istanza: hanno accesso alle variabili di istanza, possono essere sovrascritti
# metodi di classe: hanno accesso solo alle variabili di classe, non possono essere sovrascritti
# metodi statici: non hanno accesso a variabili di istanza o di classe, non possono essere sovrascritti

# per non sovrascribilità si intende che non possono essere ridefiniti in una sottoclasse

    @staticmethod
    def analisi_generali(df):
        print("******** ANALISI GENERALE DEL DATAFRAME ********")
        print("Prime cinque osservazioni:", df.head().to_string(), sep="\n")
        print("Ultime cinque osservazioni:", df.tail().to_string(), sep="\n")
        print("Informazioni generali:")
        df.info()

    @staticmethod
    # metodo per controllo valori univoci variabili categoriali
    def analisi_valori_univoci(df, variabili_da_droppare = None):
    # variabili_da_droppare = None indica che se non viene passato nessun argomento non droppo nessuna variabile
        print("******** VALORI UNIVOCI DATAFRAME ********")
        if variabili_da_droppare:
            df = df.drop(variabili_da_droppare, axis=1)
            # axis = 1 indica che sto eliminando colonne altrimenti 0 per le righe
        for col in df.columns:
            print(f"In colonna {col} abbiamo {df[col].nunique()} valori univoci:")
            # nunique() restituisce il numero di valori univoci presenti nella colonna
            # unique() restituisce i valori univoci presenti nella colonna
            for value in df[col].unique():
                print(value)

    @staticmethod
    def analisi_indici_statistici(df):
        print("******** INDICI STATISTICI DATAFRAME ********")
        indici_generali = df.describe()
        print("Indici statistici generali delle variabili quantitative:", indici_generali.to_string(), sep="\n")
        # esegue solo per le variabili quantitative riconoscendole automaticamente
        # se ci fosse una colonna numerica da non considerare dovrei fare un filtro come sopra:
        # moda variabili quantitative e categoriali
        for col in df.columns:
            # anche mode ritorna una Series che ci presenta più informazioni
            print(f"Moda colonna {col}:", df[col].mode().iloc[0])
            # di tutte le info che la funzione mode() restituisce prendo la prima (il velore più frequente)

    @staticmethod
    def individuazione_outliers(df, variabili_da_droppare = None):
        print("******** INDIVIDUAZIONE OUTLIERS ********")
        if variabili_da_droppare:
            df = df.drop(variabili_da_droppare, axis=1)
        for col in df.columns:
            #calcolo range interquartile
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            # calcolo limiti inferiore e superiore outliers
            limite_inferiore = q1 - 1.5 * iqr
            limite_superiore = q3 + 1.5 * iqr
            outliers = df[(df[col] < limite_inferiore) | (df[col] > limite_superiore)]
            print(f"Nella colonna {col} sono presenti n° {len(outliers)} ({len(outliers) / len(df) * 100}% di outliers)")