import streamlit as st
import pandas as pd
import numpy as np
import cufflinks as cf
import seaborn as sns
import plotly.express as px
import gzip
import matplotlib.pyplot as plt


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
page = st.sidebar.radio("Choose a page", ("Description du jeu de données", "Statistiques descriptives", "Visualisations", "Wordcloud"))


if page == "Description du jeu de données":
    # Page 1: Description du jeu de données

    st.header('1. Description du jeu de données')

    # Origin of the data
    st.subheader('Origine des données')
    st.write("""
    Ces données représentent toutes les collections des bibliothèques de prêt, telles qu'elles étaient le 27 juillet 2018. Elles contiennent des informations sur les livres disponibles dans 
    ces bibliothèques, telles que le titre, l'auteur, le nombre de prêts, etc.
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
    - **Ancienneté de publication** : L'âge du livre en années depuis sa publication.
    - **Taux de prêt moyen** : Le taux moyen de prêt par exemplaire.
    """)

    # Missing values per variable
    st.subheader('Nombre de valeurs manquantes par variable')
    missing_values = df.isnull().sum()
    st.write(missing_values)

elif page == "Statistiques descriptives":
    # Page 2: Statistiques descriptives

    st.header('2. Statistiques descriptives')

    # Show summary statistics for numerical columns
    st.subheader('Statistiques descriptives pour les variables numériques')
    st.write(df.describe())

    # Show value counts for categorical columns
    st.subheader('Comptage des valeurs pour les variables catégorielles')
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        st.write(f"**{col}**:")
        st.write(df[col].value_counts())

    # Show missing values
    st.subheader('Valeurs manquantes')
    st.write(df.isnull().sum())

elif page == "Visualisations":
    # Page 3: Visualisations

    st.header('3. Visualisations')

    # Multiselect pour plusieurs langues
    langues_selectionnees = st.multiselect('Sélectionner les langues', df['Langue'].unique())

    # Filtrer les données en fonction des langues sélectionnées
    df_filtré = df[df['Langue'].isin(langues_selectionnees)]
    st.write(df_filtré)

    # Slider pour filtrer les données selon le nombre de prêts total
    nombre_pret_min, nombre_pret_max = st.slider(
    'Sélectionner une plage de nombre de prêts',
    min_value=int(df['Nombre de prêt total'].min()),
    max_value=int(df['Nombre de prêt total'].max()),
    value=(int(df['Nombre de prêt total'].min()), int(df['Nombre de prêt total'].max())))

    # Filtrer les données selon la plage sélectionnée
    df_filtré = df[(df['Nombre de prêt total'] >= nombre_pret_min) & (df['Nombre de prêt total'] <= nombre_pret_max)]
    st.write(df_filtré)
    
    langue_selectionnee = st.selectbox("Choisir une langue", df["Langue"].unique())
    df_filtré = df[df["Langue"] == langue_selectionnee]
    
    # Créer un graphique avec Plotly
    fig = px.bar(df_filtré, x="Date", y="Nombre de prêt total", title=f"Nombre de prêts pour {langue_selectionnee}")

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

    # Sélecteur interactif pour la langue
    autheur_selectionne = st.selectbox("Choisir un autheur", df["Auteur Nom"].unique())

    # Filtrer les données
    df_filtré = df[df["Auteur Nom"] == autheur_selectionne]

    # Créer un histogramme avec Seaborn
    fig, ax = plt.subplots()
    sns.barplot(data=df_filtré, x="Date", y="Nombre de prêts", ax=ax)
    ax.set_title(f"Histogramme pour {autheur_selectionne}")

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)

