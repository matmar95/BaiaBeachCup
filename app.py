import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configurazione Pagina
st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")

# 2. CSS Blindato: Spazio in cima azzerato e bordi gialli precisi
st.markdown("""
    <style>
    header { display: none !important; height: 0px !important; }
    
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    
    [data-testid="stVerticalBlock"] > div:first-child {
        margin-top: 0rem !important;
        padding-top: 0rem !important;
    }
    
    .stApp { background-color: #2f0b3f; color: #ffffff; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    h1 {
        color: #fbb03f !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        margin-top: 0rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2, h3, h4 { color: #7dcab2 !important; font-family: 'Poppins', sans-serif; }
    .stTabs [data-baseweb="tab-list"] button { font-size: 18px; font-weight: bold; }
    
    /* Container per l'iframe: altezza fissa per evitare il bianco sotto */
    [data-testid="stHtml"] {
        width: 100% !important;
        overflow-x: auto !important; 
        overflow-y: hidden !important; 
        border-radius: 12px;            
        border: 2px solid #fbb03f !important; 
        background-color: #2f0b3f;      
        padding: 4px;
        height: auto !important; /* Permette al container di adattarsi all'altezza dell'iframe */
    }

    [data-testid="stHtml"] iframe {
        display: block;
        vertical-align: bottom;
        border: none !important; 
    }
    </style>
    """, unsafe_allow_html=True)

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

st.title("🏐 Baia Beach Cup 2026")

tab1, tab2, tab3, tab4 = st.tabs(["📅 CALENDARIO", "📊 GIRONI", "🏆 FASI FINALI", "🔍 CERCA SQUADRA"])

with tab1:
    st.subheader("Match del Giorno")
    df_cal = carica_calendario("Calendario_gironi")
    if not df_cal.empty:
        st.dataframe(df_cal, use_container_width=True, hide_index=True)

# --- TAB 2: GIRONI ---
with tab2:
    st.subheader("Situazione Gironi")
    # Range impostato a V33 e altezza a 715
    embed_gironi = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_GIRONI}&range=A1:V33&widget=false&chrome=false&headers=false&rm=minimal"
    st.components.v1.iframe(embed_gironi, height=715, scrolling=False)

# --- TAB 3: FASI FINALI ---
with tab3:
    st.subheader("Tabellone ad Eliminazione")
    # Range impostato a S33 e altezza a 715 per tagliare il bianco
    embed_tabellone = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_TABELLONE}&range=A1:S33&widget=false&chrome=false&headers=false&rm=minimal"
    st.components.v1.iframe(embed_tabellone, height=690, scrolling=False)

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