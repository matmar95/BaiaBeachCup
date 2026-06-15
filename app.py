import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configurazione Pagina e Rimozione Branding Streamlit
st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] button { font-size: 20px; font-weight: bold; }
    iframe { border-radius: 10px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_index=True)

# Parametri di configurazione del tuo Google Sheets
SHEET_ID = "1nCJXDT4HQiHKalAiUr__aYi9szcGCyFL"
GID_GIRONI = "1130118483"      # GID del foglio dei Gironi
GID_TABELLONE = "378239650"    # GID del Tabellone delle Fasi Finali

# Funzione per caricare il Calendario (che è una tabella standard e si legge bene in CSV)
@st.cache_data(ttl=15)
def carica_calendario(nome_foglio):
    nome_encoded = urllib.parse.quote(nome_foglio)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nome_encoded}"
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

st.title("🏐 Baia Beach Cup 2026")

# Creazione dei 4 Tab per la navigazione mobile-friendly
tab1, tab2, tab3, tab4 = st.tabs(["📅 Calendario", "📊 Gironi", "🏆 Fasi Finali", "🔍 Cerca Squadra"])

# --- TAB 1: CALENDARIO ---
with tab1:
    st.header("Calendario delle Gare")
    df_cal = carica_calendario("Calendario_gironi")
    if not df_cal.empty:
        st.dataframe(df_cal, use_container_width=True, hide_index=True)
    else:
        st.info("Calendario in fase di caricamento...")

# --- TAB 2: GIRONI (Risolto l'errore di lettura) ---
with tab2:
    st.header("Classifiche e Composizione Gironi")
    st.write("Aggiornato in tempo reale dal campo:")
    
    # Usiamo l'embed anche qui per mantenere la formattazione grafica delle tabelle dei gironi
    # Range A1:V40 copre ampiamente la visualizzazione dei gironi affiancati
    embed_gironi = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_GIRONI}&range=A1:V40&widget=false&chrome=false&headers=false"
    st.components.v1.iframe(embed_gironi, height=800, scrolling=True)

# --- TAB 3: FASI FINALI ---
with tab3:
    st.header("Tabellone Eliminazione Diretta")
    # Visualizzazione del tabellone grafico tramite il GID specifico comunicato
    embed_tabellone = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_TABELLONE}&range=A1:S40&widget=false&chrome=false&headers=false"
    st.components.v1.iframe(embed_tabellone, height=900, scrolling=True)

# --- TAB 4: RICERCA SQUADRA ---
with tab4:
    st.header("Le Tue Partite")
    df_partite = carica_calendario("Calendario_gironi")
    if not df_partite.empty:
        col1, col2 = "Squadra 1", "Squadra 2"
        # Controllo se le colonne esistono per evitare crash
        if col1 in df_partite.columns:
            squadre = sorted(list(set(df_partite[col1].dropna().unique()) | set(df_partite[col2].dropna().unique())))
            scelta = st.selectbox("Seleziona la tua squadra per vedere i tuoi orari:", [""] + squadre)
            if scelta:
                filtro = df_partite[(df_partite[col1] == scelta) | (df_partite[col2] == scelta)]
                st.dataframe(filtro, use_container_width=True, hide_index=True)
        else:
            st.info("La lista delle squadre sarà disponibile non appena il calendario sarà popolato.")