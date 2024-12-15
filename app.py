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

    # 1. Histogram for numerical variables using Matplotlib
    st.subheader('Histogramme des variables numériques')
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numerical_columns:
        st.write(f"**{col}** Histogramme:")
        fig, ax = plt.subplots()
        ax.hist(df[col].dropna(), bins=30, color='skyblue', edgecolor='black')
        ax.set_title(f'Histogramme de {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Fréquence')
        st.pyplot(fig)

    # 2. Bar chart for categorical variables using Matplotlib
    st.subheader('Diagrammes en barres pour les variables catégorielles')
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        st.write(f"**{col}** Diagramme en barres:")
        fig = plt.figure(figsize=(8, 4))
        df[col].value_counts().plot(kind='bar', color='lightcoral')
        plt.title(f'Diagramme en barres de {col}')
        plt.xlabel(col)
        plt.ylabel('Fréquence')
        st.pyplot(fig)

    # 3. Correlation Heatmap using Seaborn
    st.subheader('Carte de chaleur des corrélations')
    correlation_matrix = df[numerical_columns].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax, cbar=True)
    ax.set_title('Carte de chaleur des corrélations')
    st.pyplot(fig)

    # 4. Bar chart for total loan count per year using Plotly
    st.subheader('Graphique interactif des prêts totaux par année')
    # Ensure the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert to datetime if not already
    df['Year'] = df['Date'].dt.year  # Extract year
    fig = px.bar(df, x="Year", y="Nombre de prêt total", title="Prêts totaux par année", labels={"Year": "Année", "Nombre de prêt total": "Total des prêts"})
    st.plotly_chart(fig)

    # 5. Another Plotly Chart (Example: Total Loans by Book Title)
    st.subheader('Graphique interactif des prêts totaux par titre de livre')
    book_loans = df.groupby('Titre')['Nombre de prêt total'].sum().reset_index()
    fig2 = px.bar(book_loans, x='Titre', y='Nombre de prêt total', title="Prêts totaux par titre de livre", labels={'Titre': 'Titre du livre', 'Nombre de prêt total': 'Total des prêts'})
    st.plotly_chart(fig2)

