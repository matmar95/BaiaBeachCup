import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configurazione Pagina
st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")

# 2. CSS Blindato: Spazio azzerato, BARRA NASCOSTA e BORDO GIALLO FORZATO
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
    
    /* Configurazione Titolo Principale (H1) */
    h1 {
        color: #fbb03f !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        margin-top: 0rem !important;
        margin-bottom: 0rem !important;
        padding-top: 0.2rem !important;
        line-height: 1.1 !important;
    }
    
    /* Configurazione Sottotitolo (H2) */
    h2 {
        color: #7dcab2 !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        margin-top: 0.2rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    h3, h4 { color: #7dcab2 !important; font-family: 'Poppins', sans-serif; }
    .stTabs [data-baseweb="tab-list"] button { font-size: 18px; font-weight: bold; }
    
    /* Stile per gli Expander (Menu a scomparsa del Calendario) */
    .stDecoration { background-color: #fbb03f !important; }
    
    /* --- COPERTURA TOTALE PER IL BORDO GIALLO DEI TABELLONI --- */
    [data-testid="stHtml"] {
        width: 100% !important;
        overflow-x: auto !important; 
        overflow-y: hidden !important; 
        border-radius: 12px !important;            
        border: 2px solid #fbb03f !important; 
        background-color: #2f0b3f !important;      
        padding: 4px !important;
        height: auto !important;
        scrollbar-width: none;            
        -ms-overflow-style: none;         
    }
    
    .element-container:has(iframe) {
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    [data-testid="stHtml"]::-webkit-scrollbar {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        background: transparent !important;
    }

    [data-testid="stHtml"] iframe {
        display: block;
        vertical-align: bottom;
        border: none !important; 
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
        df = pd.read_csv(url, header=None, skiprows=1)
        return df
    except:
        return pd.DataFrame()

# --- BARRA DEL TITOLO SENZA LOGO ---
st.markdown("<h1>🏐 Baia Beach Cup 2026</h1>", unsafe_allow_html=True)
st.markdown("<h2>2x2 Maschile</h2>", unsafe_allow_html=True)
# ------------------------------------

# Definizione dei Tab
tab1, tab2, tab3, tab4 = st.tabs(["📅 CALENDARIO", "📊 GIRONI", "🏆 FASI FINALI", "🔍 CERCA SQUADRA"])

# --- TAB 1: CALENDARIO (Splittato su Campo 1 e Campo 2) ---
with tab1:
    df_raw = carica_calendario("Calendario_gironi")
    
    if not df_raw.empty:
        # Estrariamo e puliamo i dati per il CAMPO 1 (Colonne A, B, C, D, E, F)
        df_campo1 = df_raw[[0, 1, 2, 3, 4, 5]].dropna(subset=[0]).copy()
        df_campo1.columns = ["Orario", "Girone", "Squadra 1", "Set 1", "Set 2", "Squadra 2"]
        
        # Estrariamo e puliamo i dati per il CAMPO 2 (Colonne A, H, I, J, K, L)
        df_campo2 = df_raw[[0, 7, 8, 9, 10, 11]].dropna(subset=[0]).copy()
        df_campo2.columns = ["Orario", "Girone", "Squadra 1", "Set 1", "Set 2", "Squadra 2"]
        
        # --- MENU A SCOMPARSA CAMPO 1 ---
        with st.expander("🏟️ VISUALIZZA MATCH - CAMPO 1", expanded=True):
            st.dataframe(df_campo1, use_container_width=True, hide_index=True)
            
        # --- MENU A SCOMPARSA CAMPO 2 ---
        with st.expander("🏟️ VISUALIZZA MATCH - CAMPO 2", expanded=False):
            st.dataframe(df_campo2, use_container_width=True, hide_index=True)
    else:
        st.info("Il calendario è in fase di compilazione. Torna a controllare più tardi!")

# --- TAB 2: GIRONI ---
with tab2:
    st.subheader("Situazione Gironi")
    embed_gironi = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_GIRONI}&range=A1:V35&widget=false&chrome=false&headers=false&rm=minimal"
    st.components.v1.iframe(embed_gironi, height=730, scrolling=False)

# --- TAB 3: FASI FINALI ---
with tab3:
    st.subheader("Tabellone ad Eliminazione")
    embed_tabellone = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_TABELLONE}&range=A1:S35&widget=false&chrome=false&headers=false&rm=minimal"
    st.components.v1.iframe(embed_tabellone, height=730, scrolling=False)

# --- TAB 4: RICERCA SQUADRA ---
with tab4:
    st.subheader("Trova le tue Partite")
    df_partite = carica_calendario("Calendario_gironi")
    if not df_partite.empty:
        p1 = df_partite[[0, 1, 2, 3, 4, 5]].copy()
        p1.columns = ["Orario", "Girone", "Squadra 1", "Set 1", "Set 2", "Squadra 2"]
        p1["Campo"] = "Campo 1"
        
        p2 = df_partite[[0, 7, 8, 9, 10, 11]].copy()
        p2.columns = ["Orario", "Girone", "Squadra 1", "Set 1", "Set 2", "Squadra 2"]
        p2["Campo"] = "Campo 2"
        
        df_totale = pd.concat([p1, p2]).dropna(subset=["Orario", "Squadra 1"])
        
        squadre = sorted(list(set(df_totale["Squadra 1"].dropna().unique()) | set(df_totale["Squadra 2"].dropna().unique())))
        scelta = st.selectbox("Seleziona la tua Squadra per vedere i tuoi orari:", [""] + squadre)
        
        if scelta:
            filtro = df_totale[(df_totale["Squadra 1"] == scelta) | (df_totale["Squadra 2"] == scelta)].sort_values(by="Orario")
            filtro = filtro[["Orario", "Campo", "Girone", "Squadra 1", "Set 1", "Set 2", "Squadra 2"]]
            st.dataframe(filtro, use_container_width=True, hide_index=True)