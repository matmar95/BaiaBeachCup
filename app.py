import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configurazione Pagina Originale
st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")

# 2. CSS Minimale solo per Sfondo e Titoli (senza toccare le tabelle)
st.markdown("""
    <style>
    /* Sfondo principale dell'app */
    .stApp {
        background-color: #2f0b3f;
        color: #ffffff;
    }
    
    /* Nasconde menu e footer di default */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Colori puliti per Titoli e scritte dei Tab */
    h1 {
        color: #fbb03f !important;
        font-family: 'Poppins', sans-serif;
    }
    h2, h3, h4 {
        color: #7dcab2 !important;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 18px;
        font-weight: bold;
    }
    
    /* Bordi puliti per i fogli embedded */
    iframe {
        border-radius: 10px;
        border: 2px solid #fbb03f;
    }
    </style>
    """, unsafe_allow_html=True)

# Parametri Sheets
SHEET_ID = "1nCJXDT4HQiHKalAiUr__aYi9szcGCyFL"
GID_GIRONI = "1130118483"      
GID_TABELLONE = "378239650"    

@st.cache_data(ttl=15)
def carica_calendario(nome_foglio):
    nome_encoded = urllib.parse.quote(nome_foglio)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nome_encoded}"
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# Struttura e Titoli Originali
st.title("🏐 Baia Beach Cup 2026")

tab1, tab2, tab3, tab4 = st.tabs(["📅 CALENDARIO", "📊 GIRONI", "🏆 FASI FINALI", "🔍 CERCA SQUADRA"])

# --- TAB 1: CALENDARIO (Ripristinato nativo) ---
with tab1:
    st.subheader("Match del Giorno")
    df_cal = carica_calendario("Calendario_gironi")
    if not df_cal.empty:
        st.dataframe(df_cal, use_container_width=True, hide_index=True)

# --- TAB 2: GIRONI ---
with tab2:
    st.subheader("Situazione Gironi")
    embed_gironi = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_GIRONI}&range=A1:V32&widget=false&chrome=false&headers=false&rm=minimal"
    st.components.v1.iframe(embed_gironi, height=680, scrolling=True)

# --- TAB 3: FASI FINALI ---
with tab3:
    st.subheader("Tabellone ad Eliminazione")
    embed_tabellone = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_TABELLONE}&range=A1:S32&widget=false&chrome=false&headers=false&rm=minimal"
    st.components.v1.iframe(embed_tabellone, height=600, scrolling=True)

# --- TAB 4: RICERCA SQUADRA (Ripristinato nativo) ---
with tab4:
    st.subheader("Trova le tue Partite")
    df_partite = carica_calendario("Calendario_gironi")
    if not df_partite.empty:
        col1, col2 = "Squadra 1", "Squadra 2"
        if col1 in df_partite.columns:
            squadre = sorted(list(set(df_partite[col1].dropna().unique()) | set(df_partite[col2].dropna().unique())))
            scelta = st.selectbox("Seleziona la tua Squadra:", [""] + squadre)
            if scelta:
                filtro = df_partite[(df_partite[col1] == scelta) | (df_partite[col2] == scelta)]
                st.dataframe(filtro, use_container_width=True, hide_index=True)