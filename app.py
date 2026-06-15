import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configurazione Pagina e Rimozione Branding
st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")

# Nascondiamo i menu di Streamlit per un look pulito
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] button { font-size: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_index=True)

# Parametri Sheets
SHEET_ID = "1nCJXDT4HQiHKalAiUr__aYi9szcGCyFL"
# NUOVO GID CORRETTO per il "Tabellone Finali"
GID_TABELLONE = "378239650"

@st.cache_data(ttl=15)
def carica_foglio_csv(nome_foglio):
    nome_encoded = urllib.parse.quote(nome_foglio)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nome_encoded}"
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

st.title("🏐 Baia Beach Cup 2026")

# Creazione dei Tab
tab1, tab2, tab3, tab4 = st.tabs(["📅 Calendario", "📊 Gironi", "🏆 Fasi Finali", "🔍 Cerca Squadra"])

with tab1:
    st.header("Calendario delle Gare")
    df_cal = carica_foglio_csv("Calendario_gironi")
    if not df_cal.empty:
        st.dataframe(df_cal, use_container_width=True, hide_index=True)

with tab2:
    st.header("Classifiche Gironi")
    df_gironi = carica_foglio_csv("Gironi")
    if not df_gironi.empty:
        st.dataframe(df_gironi, use_container_width=True, hide_index=True)

with tab3:
    st.header("Tabellone Eliminazione Diretta")
    # Inserito il nuovo GID. Manteniamo range=A1:S40 per centrare la struttura ad albero
    embed_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_TABELLONE}&range=A1:S40&widget=false&chrome=false&headers=false"
    
    st.components.v1.iframe(embed_url, height=900, scrolling=True)

with tab4:
    st.header("Le Tue Partite")
    df_partite = carica_foglio_csv("Calendario_gironi")
    if not df_partite.empty:
        col1, col2 = "Squadra 1", "Squadra 2"
        if col1 in df_partite.columns:
            squadre = sorted(list(set(df_partite[col1].dropna().unique()) | set(df_partite[col2].dropna().unique())))
            scelta = st.selectbox("Seleziona la tua squadra:", [""] + squadre)
            if scelta:
                filtro = df_partite[(df_partite[col1] == scelta) | (df_partite[col2] == scelta)]
                st.table(filtro)