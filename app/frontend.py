import streamlit as st
import requests

# Configuration de l'URL de ton API (celle qui tourne dans Docker)
API_URL = "http://localhost:8000"

st.set_page_config(page_title="CoDrive INPT", page_icon="🚗")
st.title("🚗 CoDrive - Plateforme de Covoiturage")

# Utilisation de la "session_state" de Streamlit pour garder le Token en mémoire
if "token" not in st.session_state:
    st.session_state.token = None

# Barre latérale pour la navigation
menu = ["Se connecter", "S'inscrire", "Voir les trajets", "Publier un trajet"]
choice = st.sidebar.selectbox("Menu", menu)

# --- LOGIQUE D'INSCRIPTION ---
if choice == "S'inscrire":
    st.subheader("Créer un compte académique")
    full_name = st.text_input("Nom complet")
    email = st.text_input("Email professionnel (@inpt.ac.ma, @intelcia.com...)")
    password = st.text_input("Mot de passe", type='password')
    
    if st.button("S'inscrire"):
        data = {"email": email, "password": password, "full_name": full_name}
        response = requests.post(f"{API_URL}/signup", json=data)
        if response.status_code == 200:
            st.success("Compte créé avec succès ! Connectez-vous maintenant.")
        else:
            st.error(f"Erreur : {response.json().get('detail')}")

# --- LOGIQUE DE CONNEXION ---
elif choice == "Se connecter":
    st.subheader("Connexion")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type='password')
    
    if st.button("Connexion"):
        # OAuth2 demande un format 'form-data'
        data = {"username": email, "password": password}
        response = requests.post(f"{API_URL}/login", data=data)
        
        if response.status_code == 200:
            st.session_state.token = response.json().get("access_token")
            st.success("Connecté !")
        else:
            st.error("Identifiants incorrects ou domaine non autorisé.")

# --- LOGIQUE D'AFFICHAGE ---
elif choice == "Voir les trajets":
    st.subheader("Trajets disponibles")
    response = requests.get(f"{API_URL}/trips/")
    if response.status_code == 200:
        trips = response.json()
        if trips:
            st.table(trips)
        else:
            st.info("Aucun trajet disponible pour le moment.")

# --- LOGIQUE DE PUBLICATION (SÉCURISÉE) ---
elif choice == "Publier un trajet":
    st.subheader("Proposer un nouveau trajet")
    if not st.session_state.token:
        st.warning("Vous devez être connecté pour publier un trajet.")
    else:
        dest = st.text_input("Destination")
        date = st.text_input("Date (ex: 2026-05-01)")
        
        if st.button("Publier"):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            payload = {"destination": dest, "date": date}
            response = requests.post(f"{API_URL}/trips/", json=payload, headers=headers)
            
            if response.status_code == 200:
                st.success("Trajet publié !")
            elif response.status_code == 403:
                st.error("Votre vérification mensuelle a expiré !")
            else:
                st.error("Erreur lors de la publication.")