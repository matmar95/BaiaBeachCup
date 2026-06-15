import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configurazione Pagina
st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")

# 2. Iniezione CSS Personalizzato
st.markdown("""
    <style>
    /* Sfondo principale dell'app */
    .stApp {
        background-color: #2f0b3f;
        color: #ffffff;
    }
    
    /* Nasconde menu e footer Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Personalizzazione dei Titoli e Sottotitoli */
    h1 {
        color: #fbb03f !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
    }
    h2, h3, h4 {
        color: #7dcab2 !important;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Testo dei widget (es. selectbox) */
    .stSelectbox label p {
        color: #7dcab2 !important;
    }
    
    /* Stile dei TAB superiori */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #2f0b3f;
        padding: 10px 0;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #1a0526;
        border: 1px solid #fbb03f;
        border-radius: 8px 8px 0px 0px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        color: #7dcab2 !important;
    }
    /* Tab attivo */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #2f0b3f !important;
        color: #fbb03f !important;
        border-bottom: 2px solid #2f0b3f !important;
    }

    /* Stile IFRAME (Gironi e Tabellone) */
    iframe {
        border-radius: 12px;
        border: 3px solid #fbb03f !important;
        background-color: #2f0b3f;
    }

    /* SOVRASCRITTURA TABELLE (Streamlit Dataframe) -> ORA GIALLINE */
    [data-testid="stDataFrame"] div {
        background-color: #fbb03f !important;
    }
    /* Intestazione Tabella (Menta) */
    [data-testid="stDataFrame"] th {
        background-color: #7dcab2 !important;
        color: #2f0b3f !important;
        font-weight: bold;
        border: 1px solid #2f0b3f !important;
    }
    /* Righe della tabella (Sfondo giallino, testo viola, bordi viola) */
    [data-testid="stDataFrame"] td {
        background-color: #fbb03f !important;
        color: #2f0b3f !important;
        border: 1px solid #2f0b3f !important;
    }
    /* Forza il testo generico all'interno del dataframe ad essere scuro sul giallino */
    [data-testid="stDataFrame"] div div {
        color: #2f0b3f !important;
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

# Titolo Principale (diventerà #fbb03f)
st.title("🏐 Baia Beach Cup 2026")

tab1, tab2, tab3, tab4 = st.tabs(["📅 CALENDARIO", "📊 GIRONI", "🏆 FASI FINALI", "🔍 CERCA SQUADRA"])

with tab1:
    st.subheader("Match del Giorno")
    df_cal = carica_calendario("Calendario_gironi")
    if not df_cal.empty:
        st.dataframe(df_cal, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Situazione Gironi")
    # Ridotto a A1:V32 per stringere il frame ed evitare scrolling vuoto
    embed_gironi = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_GIRONI}&range=A1:V32&widget=false&chrome=false&headers=false&rm=minimal"
    st.components.v1.iframe(embed_gironi, height=680, scrolling=True)

with tab3:
    st.subheader("Tabellone ad Eliminazione")
    # Ridotto a A1:S32 per tagliare le righe vuote del tabellone
    embed_tabellone = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_TABELLONE}&range=A1:S32&widget=false&chrome=false&headers=false&rm=minimal"
    st.components.v1.iframe(embed_tabellone, height=750, scrolling=True)

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