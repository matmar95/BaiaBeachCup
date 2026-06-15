import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configurazione Pagina
st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")

# 2. Personalizzazione Estetica (Sfondo e Tab)
st.markdown("""
    <style>
    /* Cambia lo sfondo di tutta l'app (Colore Sabbia Chiarissimo) */
    .stApp {
        background-color: #fdf5e6; 
    }
    
    /* Se vuoi un'immagine di sfondo, usa questa riga invece di quella sopra:
    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/sandpaper.png");
    } */

    /* Nasconde menu e footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Migliora l'estetica dei Tab */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #ffffff;
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px;
        font-size: 18px;
        font-weight: bold;
        color: #5d4037;
    }
    
    /* Riquadro per gli iframe */
    iframe {
        border-radius: 15px;
        border: 2px solid #e8d5b5;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Parametri Sheets
SHEET_ID = "1nCJXDT4HQiHKalAiUr__aYi9szcGCyFL"
GID_GIRONI = "1130118483"      # GID Gironi
GID_TABELLONE = "378239650"    # GID Tabellone Finali

@st.cache_data(ttl=15)
def carica_calendario(nome_foglio):
    nome_encoded = urllib.parse.quote(nome_foglio)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nome_encoded}"
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

st.title("🏐 Baia Beach Cup 2026")

tab1, tab2, tab3, tab4 = st.tabs(["📅 CALENDARIO", "📊 GIRONI", "🏆 FASI FINALI", "🔍 CERCA SQUADRA"])

with tab1:
    st.subheader("Match del Giorno")
    df_cal = carica_calendario("Calendario_gironi")
    if not df_cal.empty:
        st.dataframe(df_cal, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Situazione Gironi")
    # RIDUZIONE FRAME: Ho limitato il range a A1:V35 per togliere il vuoto sotto
    embed_gironi = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_GIRONI}&range=A1:V35&widget=false&chrome=false&headers=false&rm=minimal"
    st.components.v1.iframe(embed_gironi, height=700, scrolling=True)

with tab3:
    st.subheader("Tabellone ad Eliminazione")
    # RIDUZIONE FRAME: Qui usiamo il range A1:S35 per focalizzare il tabellone grafico
    embed_tabellone = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_TABELLONE}&range=A1:S35&widget=false&chrome=false&headers=false&rm=minimal"
    st.components.v1.iframe(embed_tabellone, height=800, scrolling=True)

with tab4:
    st.subheader("Trova le tue Partite")
    df_partite = carica_calendario("Calendario_gironi")
    if not df_partite.empty:
        col1, col2 = "Squadra 1", "Squadra 2"
        if col1 in df_partite.columns:
            squadre = sorted(list(set(df_partite[col1].dropna().unique()) | set(df_partite[col2].dropna().unique())))
            scelta = st.selectbox("Seleziona Squadra:", [""] + squadre)
            if scelta:
                filtro = df_partite[(df_partite[col1] == scelta) | (df_partite[col2] == scelta)]
                st.dataframe(filtro, use_container_width=True, hide_index=True)