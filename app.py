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

    # Sélecteur de langue
    langue_selectionnee = st.selectbox('Sélectionner une langue', df['Langue'].unique(), key="selectbox_langue6")

    # Filtrer les données en fonction de la langue choisie
    df_filtré3 = df[df['Langue'] == langue_selectionnee]
    st.write(df_filtré)


    # Slider pour filtrer les données selon le nombre de prêts total
    nombre_pret_min, nombre_pret_max = st.slider(
    'Sélectionner une plage de nombre de prêts',
    min_value=int(df['Nombre de prêt total'].min()),
    max_value=int(df['Nombre de prêt total'].max()),
    value=(int(df['Nombre de prêt total'].min()), int(df['Nombre de prêt total'].max())))

    ### Graph interactif 1
    # Filtrer les données selon la plage sélectionnée
    df_filtré = df[(df['Nombre de prêt total'] >= nombre_pret_min) & (df['Nombre de prêt total'] <= nombre_pret_max)]
    st.write(df_filtré)
    
    langue_selectionnee = st.selectbox("Choisir une langue", df["Langue"].unique())
    df_filtré = df[df["Langue"] == langue_selectionnee]
    
    # Créer un graphique avec Plotly
    fig = px.bar(df_filtré, x="Date", y="Nombre de prêt total", title=f"Nombre de prêts pour {langue_selectionnee}")

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

    ### Graph interactif 2
    # Slider pour filtrer le nombre d'exemplaires
    nombre_exemplaires_min, nombre_exemplaires_max = st.slider(
    'Sélectionner une plage de nombre d\'exemplaires',
    min_value=int(df['Nombre d\'exemplaires'].min()),
    max_value=int(df['Nombre d\'exemplaires'].max()),
    value=(int(df['Nombre d\'exemplaires'].min()), int(df['Nombre d\'exemplaires'].max())))

    # Filtrer les données selon la plage sélectionnée
    df_filtré_exemplaires = df[(df['Nombre d\'exemplaires'] >= nombre_exemplaires_min) & 
                            (df['Nombre d\'exemplaires'] <= nombre_exemplaires_max)]

    # Créer un graphique de type scatter pour voir la relation
    fig_exemplaires = px.scatter(df_filtré_exemplaires, 
                             x='Nombre de prêt total', 
                             y='Nombre d\'exemplaires',
                             title="Relation entre Nombre de prêts total et Nombre d'exemplaires")

    # Afficher le graphique
    st.plotly_chart(fig_exemplaires)

    ### Graph interactif 3
    # Filtrer les données selon le type de document
    type_document_selectionne = st.selectbox("Choisir un type de document", df["Type de document"].unique())

    # Filtrer les données
    df_filtré_document = df[df["Type de document"] == type_document_selectionne]

    # Créer un histogramme pour les prêts totaux par type de document
    fig_document = px.histogram(df_filtré_document, 
                             x='Nombre de prêt total', 
                             title=f"Histogramme des prêts totaux pour le type de document {type_document_selectionne}",
                             labels={'Nombre de prêt total': 'Nombre de prêts total'})

    # Afficher le graphique
    st.plotly_chart(fig_document)

    ### Graph interactif 4
    # Sélectionner la langue via un filtre interactif
    langue_selectionnee_scatter = st.selectbox("Choisir une langue", df["Langue"].unique(), key="selectbox_langue")

    # Filtrer les données selon la langue choisie
    df_filtré_scatter = df[df["Langue"] == langue_selectionnee_scatter]

    # Créer un scatter plot pour Nombre de prêt total vs Nombre de localisations
    fig_scatter = px.scatter(df_filtré_scatter, 
                         x="Nombre de prêt total", 
                         y="Nombre de localisations", 
                         title=f"Relation entre Nombre de prêt total et Nombre de localisations pour {langue_selectionnee_scatter}",
                         labels={'Nombre de prêt total': 'Nombre de prêt total', 'Nombre de localisations': 'Nombre de localisations'})
    
    # Afficher le graphique
    st.plotly_chart(fig_scatter)

    ### Graph interactif 5
    # Sélectionner la langue via un filtre interactif
    langue_selectionnee_anciennete = st.selectbox("Choisir une langue", df["Langue"].unique(), key="selectbox_langue1")

    # Filtrer les données selon la langue choisie
    df_filtré_anciennete = df[df["Langue"] == langue_selectionnee_anciennete]

    # Créer un histogramme pour l'ancienneté de publication
    fig_anciennete = px.histogram(df_filtré_anciennete, 
                               x='Ancienneté de publication', 
                               title=f"Ancienneté de publication pour {langue_selectionnee_anciennete}",
                               labels={'Ancienneté de publication': 'Ancienneté de publication'})

    # Afficher le graphique
    st.plotly_chart(fig_anciennete)


