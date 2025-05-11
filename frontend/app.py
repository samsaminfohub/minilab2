import streamlit as st
import requests
import pandas as pd
import os
import json

# Configuration
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://fastapi:8000")

st.set_page_config(
    page_title="Application Streamlit avec FastAPI et MySQL",
    page_icon="🚀",
    layout="wide"
)

# Fonction pour vérifier la santé de l'API
def check_api_health():
    try:
        response = requests.get(f"{FASTAPI_URL}/health")
        if response.status_code == 200:
            return True, response.json()
        return False, response.json()
    except Exception as e:
        return False, {"error": str(e)}

# Fonction pour obtenir tous les éléments
def get_items():
    try:
        response = requests.get(f"{FASTAPI_URL}/items/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des éléments: {str(e)}")
        return []

# Fonction pour ajouter un élément
def add_item(name, description):
    try:
        response = requests.post(
            f"{FASTAPI_URL}/items/",
            json={"name": name, "description": description}
        )
        return response.status_code == 200 or response.status_code == 201, response.json()
    except Exception as e:
        return False, {"error": str(e)}

# Fonction pour supprimer un élément
def delete_item(item_id):
    try:
        response = requests.delete(f"{FASTAPI_URL}/items/{item_id}")
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"error": str(e)}

# Interface utilisateur
st.title("📝 Gestionnaire d'éléments")

# Vérification de la santé de l'API
health_status, health_details = check_api_health()
if health_status:
    st.success("✅ Connexion à l'API et à la base de données établie")
else:
    st.error("❌ Problème de connexion à l'API ou à la base de données")
    st.json(health_details)

# Barre latérale pour ajouter un nouvel élément
st.sidebar.header("Ajouter un nouvel élément")
with st.sidebar.form("add_item_form"):
    name = st.text_input("Nom", max_chars=100)
    description = st.text_area("Description", max_chars=255)
    submit_button = st.form_submit_button("Ajouter")
    
    if submit_button and name:
        success, result = add_item(name, description)
        if success:
            st.success(f"✅ Élément '{name}' ajouté avec succès!")
        else:
            st.error("❌ Erreur lors de l'ajout de l'élément")
            st.json(result)

# Affichage des éléments
st.header("Liste des éléments")
items = get_items()

if not items:
    st.info("Aucun élément trouvé. Ajoutez-en un dans le formulaire à gauche.")
else:
    # Créer un dataframe pour l'affichage
    df = pd.DataFrame(items)
    
    # Affichage avec possibilité de suppression
    for idx, item in enumerate(items):
        col1, col2, col3 = st.columns([3, 6, 1])
        with col1:
            st.subheader(item["name"])
        with col2:
            st.write(item["description"])
        with col3:
            if st.button("🗑️", key=f"delete_{item['id']}"):
                success, result = delete_item(item["id"])
                if success:
                    st.success(f"✅ Élément supprimé avec succès!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Erreur lors de la suppression")
                    st.json(result)
        st.divider()

# Information sur l'application
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **À propos**
    
    Cette application démontre l'utilisation de:
    - Streamlit pour l'interface utilisateur
    - FastAPI pour l'API backend
    - MySQL pour la base de données
    - Docker Compose pour orchestrer le tout
    """
)

# Affichage de la configuration de l'API
st.sidebar.markdown("---")
st.sidebar.subheader("Configuration")
st.sidebar.code(f"API URL: {FASTAPI_URL}")