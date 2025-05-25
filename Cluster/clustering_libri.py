import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

dataset = pd.read_csv('data_book.csv')

#traformo le categoriali in numeriche
lb_1 = LabelEncoder()
dataset['Name'] = lb_1.fit_transform(dataset['Name'])
lb_2 = LabelEncoder()
dataset['Author'] = lb_2.fit_transform(dataset['Author'])
lb_3 = LabelEncoder()
dataset['Genre'] = lb_3.fit_transform(dataset['Genre'])


X = dataset.values
X_train, X_test = train_test_split(X, test_size=0.2, random_state=0)

#Utilicco il metodo del Gomito per trovare il numero ottimale di cluster
model = KMeans(random_state=10)
visualizer = KElbowVisualizer(model, k=(2, 15), metric='calinski_harabasz', locate_elbow=True, timings=False)
visualizer.fit(X_train)
visualizer.show()
valore_k_ottimo = visualizer.elbow_value_
print(f"Numero ottimale di cluster trovato: {valore_k_ottimo}")

# trovato il numero di cluster (k) con KMeans assegno i gruppi al dataset:
kmeans = KMeans(n_clusters=valore_k_ottimo, random_state=10)
dataset['Cluster'] = kmeans.fit_predict(X)  # Ora assegna i cluster a tutto il dataset
#adesso visualizzo come è stato diviso il dataset trovando le divisioni più forti:
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

#vediamo il peso di ciascuna colonna qual è per formare le due variabili (da cui si ha la variazione massima)

# Creiamo un DataFrame con i pesi delle variabili
pca_components = pd.DataFrame(
    pca.components_,
    columns=dataset.columns[:-1],  # Escludiamo la colonna 'Cluster' se presente
    index=['PCA1', 'PCA2']
)


print("\n Pesi delle variabili per le prime due componenti PCA:")
print(pca_components)


plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=dataset['Cluster'], cmap='viridis')
plt.xlabel("PCA1")
plt.ylabel("PCA2")
plt.title(f"Distribuzione dei libri nei {valore_k_ottimo} cluster")
plt.colorbar(label="Cluster")
plt.show()

#vediamo la distribuzione dei dati in base alle coppie di colonne
sns.pairplot(dataset, hue="Cluster", palette="viridis")
plt.show()
