import streamlit as st
import pandas as pd
import gzip

# Function to load a gzipped CSV file
def load_data():
    with gzip.open('cleaned_data.csv.gz', 'rt', encoding='utf-8') as f:
        df = pd.read_csv(f)
    return df

# Load the cleaned dataset
df = load_data()

# Streamlit app setup
st.set_page_config(page_title="Data Analysis App", page_icon="📊", layout="wide")
st.title('Data Analysis App')

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", ("Description du jeu de données", "Statistiques descriptives", "Visualisations"))

if page == "Description du jeu de données":
    # Page 1: Description du jeu de données

    st.header('1. Description du jeu de données')

    # Origin of the data
    st.subheader('Origine des données')
    st.write("""
    Ces données proviennent d'un jeu de données sur les bibliothèques. Elles contiennent des informations sur les livres disponibles dans 
    différentes bibliothèques, telles que le titre, l'auteur, le nombre de prêts, etc.
    """)

    # Number of observations and variables
    st.subheader('Nombre d\'observations et de variables')
    st.write(f"Le jeu de données contient {df.shape[0]} observations et {df.shape[1]} variables.")

    # Types of variables
    st.subheader('Types de variables')
    st.write(df.dtypes)

    # Meaning of each variable
    st.subheader('Signification de chaque variable')
    st.write("""
    - **Langue** : La langue du livre.
    - **Titre** : Le titre du livre.
    - **Editeur** : L'éditeur du livre.
    - **Date** : La date de publication du livre.
    - **Format** : Le format du livre (papier, numérique, etc.).
    - **Auteur Nom** : Le nom de l'auteur.
    - **Auteur Prénom** : Le prénom de l'auteur.
    - **Type de document** : Le type de document (par exemple, livre, article, etc.).
    - **Nombre de localisations** : Le nombre de bibliothèques où le livre est disponible.
    - **Nombre de prêt total** : Le nombre total de fois que le livre a été emprunté.
    - **Nombre de prêts 2017** : Le nombre de prêts en 2017.
    - **Nombre d'exemplaires** : Le nombre d'exemplaires du livre dans les bibliothèques.
    - **Catégorie statistique 1** : Une catégorie supplémentaire pour le livre.
    - **Date_cleaned** : La date de publication nettoyée.
    - **Ancienneté de publication** : L'âge du livre en années depuis sa publication.
    - **Taux de prêt moyen** : Le taux moyen de prêt par exemplaire.
    """)

    # Missing values per variable
    st.subheader('Nombre de valeurs manquantes par variable')
    missing_values = df.isnull().sum()
    st.write(missing_values)
