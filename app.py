import streamlit as st
import pandas as pd
import requests

# --- CONFIGURATION INTERFACE MOBILE ---
st.set_page_config(page_title="TurfMaster AI", page_icon="🏇", layout="centered")

# Design personnalisé pour Android
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #28a745;
        color: white;
        font-weight: bold;
        font-size: 18px;
    }
    .stNumberInput input {
        font-size: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏇 TurfMaster AI")
st.write("Analyseur de Value Bet & Gestion de Mise")

# --- PARAMÈTRES DE CALCUL ---
with st.container():
    st.subheader("📊 Paramètres")
    capital = st.number_input("Capital disponible (€)", value=500, step=10)
    cote = st.number_input("Cote du cheval", value=2.0, min_value=1.01, step=0.1)
    
    # Bouton d'action
    if st.button("Lancer l'analyse"):
        # Logique de probabilité (IA simulée +12% d'avantage)
        prob_reelle = (1 / cote) * 1.12
        indice_value = prob_reelle * cote
        
        # Formule de Kelly (Prudence 25%)
        p = prob_reelle
        b = cote - 1
        fraction_kelly = (p * b - (1 - p)) / b
        mise_finale = max(0, capital * fraction_kelly * 0.25)

        # --- AFFICHAGE DES RÉSULTATS ---
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Indice Value", round(indice_value, 2))
        with col2:
            st.metric("Mise Conseillée", f"{round(mise_finale, 2)} €")

        if indice_value > 1.10:
            st.success("✅ Opportunité détectée !")
            st.balloons()
            
            # --- ENVOI AUTOMATIQUE TELEGRAM ---
            # Récupération sécurisée des tokens (via Streamlit Secrets)
            token = st.secrets.get("TELEGRAM_TOKEN", "MANQUANT")
            chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "MANQUANT")
            
            if token != "MANQUANT":
                msg = f"🏇 *ALERTE VALUE*\nCote: {cote}\nValue: {round(indice_value, 2)}\nMise: {round(mise_finale, 2)}€"
                url_tg = f"https://api.telegram.org/bot{token}/sendMessage"
                try:
                    requests.post(url_tg, data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
                    st.info("📲 Alerte envoyée sur Telegram")
                except:
                    st.error("⚠️ Échec de l'envoi Telegram")
        else:
            st.warning("❌ Pas assez de value pour parier.")

st.divider()
st.caption("Application automatisée via Streamlit Cloud")