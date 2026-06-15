import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configurazione Pagina
st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")

# 2. Iniezione CSS per Sfondo, Titoli, Tab e Tabelle custom
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
    h2, h3, h4, .stSubheader {
        color: #7dcab2 !important;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Testo dei widget */
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

    /* STILE DELLE TABELLE HTML CUSTOM (Giallina, testo viola) */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        background-color: #fbb03f;
        color: #2f0b3f;
        border-radius: 8px;
        overflow: hidden;
        margin-top: 15px;
    }
    .custom-table th {
        background-color: #7dcab2;
        color: #2f0b3f;
        padding: 12px;
        font-weight: bold;
        text-align: left;
        border: 1px solid #2f0b3f;
    }
    .custom-table td {
        padding: 12px;
        border: 1px solid #2f0b3f;
        font-size: 16px;
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
        # Carichiamo i dati riempiendo i valori vuoti per evitare scritte "NaN" nella tabella HTML
        return pd.read_csv(url).fillna("")
    except:
        return pd.DataFrame()

# Titolo Principale
st.title("🏐 Baia Beach Cup 2026")

tab1, tab2, tab3, tab4 = st.tabs(["📅 CALENDARIO", "📊 GIRONI", "🏆 FASI FINALI", "🔍 CERCA SQUADRA"])

with tab1:
    st.subheader("Match del Giorno")
    df_cal = carica_calendario("Calendario_gironi")
    if not df_cal.empty:
        # Trasformiamo il dataframe in una tabella HTML pulita usando la nostra classe CSS giallina
        html_table = df_cal.to_html(index=False, classes="custom-table")
        st.markdown(html_table, unsafe_allow_html=True)
    else:
        st.info("Calendario in fase di caricamento...")

with tab2:
    st.subheader("Situazione Gironi")
    embed_gironi = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_GIRONI}&range=A1:V32&widget=false&chrome=false&headers=false&rm=minimal"
    st.components.v1.iframe(embed_gironi, height=680, scrolling=True)

with tab3:
    st.subheader("Tabellone ad Eliminazione")
    embed_tabellone = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_TABELLONE}&range=A1:S32&widget=false&chrome=false&headers=false&rm=minimal"
    st.components.v1.iframe(embed_tabellone, height=750, scrolling=True)

with tab4:
    st.subheader("Trova le tue Partite")
    df_partite = carica_calendario("Calendario_gironi")
    if not df_partite.empty:
        col1, col2 = "Squadra 1", "Squadra 2"
        if col1 in df_partite.columns:
            squadre = sorted(list(set(df_partite[col1].dropna().unique()) | set(df_partite[col2].dropna().unique())))
            # Rimuoviamo eventuali stringhe vuote dalla lista di selezione
            squadre = [s for s in squadre if s != ""]
            scelta = st.selectbox("Seleziona la tua Squadra:", [""] + squadre)
            if scelta:
                filtro = df_partite[(df_partite[col1] == scelta) | (df_partite[col2] == scelta)]
                html_filtro = filtro.to_html(index=False, classes="custom-table")
                st.markdown(html_filtro, unsafe_allow_html=True)