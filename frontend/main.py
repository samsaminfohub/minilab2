import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import os

def charger_fichier_csv():

    # Fonction spécifique pour charger un fichier CSV depuis la barre latérale
    fichier_csv = st.sidebar.file_uploader(
        label="Chargez votre fichier CSV", 
        type=['csv'],  # Limitation aux fichiers CSV
        accept_multiple_files=False,  # Un seul fichier à la fois
        help="Sélectionnez un fichier CSV à analyser"
    )
    
    return fichier_csv

def traiter_donnees_csv(fichier):
    """
    Fonction pour traiter le fichier CSV chargé
    """
    try:
        # Lecture du fichier CSV avec gestion des erreurs
        df = pd.read_csv(fichier)
        return df
    except Exception as e:
        st.sidebar.error(f"Erreur de chargement : {e}")
        return None

def main():
    st.title('Analyseur de Données CSV')
    
    # Chargement du fichier CSV
    fichier_csv = charger_fichier_csv()
        
    if fichier_csv is not None:

        st.sidebar.success('Fichier téléchargé avec succès')
        # Traitement des données
        df = traiter_donnees_csv(fichier_csv)
        
        if df is not None:
            # Affichage des informations de base
            st.header('📊 Aperçu des Données')
            st.dataframe(df.head())
            
            # Informations sur le dataset
            st.subheader('Détails du Dataset')
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Nombre de lignes", df.shape[0])
                st.metric("Nombre de colonnes", df.shape[1])
            
            with col2:
                st.write("Types de colonnes :")
                st.dataframe(df.dtypes)
            
            # Sélection de colonnes numériques
            colonnes_numeriques = df.select_dtypes(include=['float64']).columns.tolist()
            
            if colonnes_numeriques:
                # Menu de sélection de colonnes
                st.sidebar.header('📈 Visualisation')
                colonne_selectionnee = st.sidebar.selectbox(
                    'Choisissez une colonne numérique', 
                    colonnes_numeriques
                )
                
                # Type de graphique
                type_graphique = st.sidebar.radio(
                    'Type de graphique', 
                    ['Histogramme', 'Plot']
                )
                
                # Génération du graphique
                st.header(f'Visualisation de {colonne_selectionnee}')
                
                plt.figure(figsize=(10, 6))
                
                if type_graphique == 'Histogramme':
                    sns.histplot(df[colonne_selectionnee], kde=True)
                    plt.title(f'Histogramme de {colonne_selectionnee}')
                
                elif type_graphique == 'Plot':
                    if len(colonnes_numeriques) > 1:
                        deuxieme_colonne = st.sidebar.selectbox(
                            'Sélectionnez une deuxième colonne', 
                            [col for col in colonnes_numeriques if col != colonne_selectionnee]
                        )
                        # Création du graphique avec deux courbes de couleurs différentes
                        plt.figure(figsize=(10, 6))
                        plt.plot(df.index, df[colonne_selectionnee], color='red', label=colonne_selectionnee)
                        plt.plot(df.index, df[deuxieme_colonne], color='blue', label=deuxieme_colonne)
                        
                        plt.title(f'Graphique de lignes : {colonne_selectionnee} vs {deuxieme_colonne}')
                        plt.xlabel('Index')
                        plt.ylabel('Valeurs')
                        plt.legend()
                        plt.grid(True)
                
                st.pyplot(plt)
                plt.close()
                # Statistiques descriptives
                st.subheader("Statistiques Descriptives")
                st.write(df[colonne_selectionnee].describe())
                # Enregistrement dans MySQL
                if st.button("📥 Enregistrer les statistiques dans MySQL"):
                    stats = df[colonne_selectionnee].describe()
                    enregistrer_statistiques_mysql(colonne_selectionnee, stats)

            else:
                st.warning("Aucune colonne numérique trouvée dans le fichier.")



def enregistrer_statistiques_mysql(colonne, stats):
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "rootpass"),
            database=os.getenv("DB_NAME", "csvdb")
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistiques (
                id INT AUTO_INCREMENT PRIMARY KEY,
                colonne VARCHAR(100),
                moyenne FLOAT,
                ecart_type FLOAT,
                minimum FLOAT,
                maximum FLOAT
            )
        """)
        cursor.execute("""
            INSERT INTO statistiques (colonne, moyenne, ecart_type, minimum, maximum)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            colonne,
            stats['mean'],
            stats['std'],
            stats['min'],
            stats['max']
        ))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Statistiques enregistrées dans la base MySQL ✅")
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement dans MySQL : {e}")


if __name__ == "__main__":
    main()