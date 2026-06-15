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

# --- BARRA DEL TITOLO ---
st.markdown("<h1>🏐 Baia Beach Cup 2026</h1>", unsafe_allow_html=True)
st.markdown("<h2>2x2 Maschile</h2>", unsafe_allow_html=True)

# Definizione dei Tab
tab1, tab2, tab3, tab4 = st.tabs(["📅 CALENDARIO", "📊 GIRONI", "🏆 FASI FINALI", "🔍 CERCA SQUADRA"])

# --- CONFIGURAZIONE COLONNE COMPATTE E ORDINATE ---
config_colonne_campi = {
    "Orario": st.column_config.TextColumn("Orario", width=65),
    "Girone": st.column_config.TextColumn("Girone", width=50), # Ridotto ulteriormente a 50px
    "Squadra 1": st.column_config.TextColumn("Squadra 1", width=140),
    "Squadra 2": st.column_config.TextColumn("Squadra 2", width=140),
    "Risultato": st.column_config.TextColumn("Risultato", width=85), # Pronto per andare in fondo
}

# Funzione d'appoggio per formattare il punteggio
def formatta_punteggio(row, col_s1, col_s2):
    s1 = str(row[col_s1]).strip() if pd.notna(row[col_s1]) else ""
    s2 = str(row[col_s2]).strip() if pd.notna(row[col_s2]) else ""
    if s1 != "" and s2 != "" and s1 != "nan" and s2 != "nan":
        s1 = s1.split('.')[0] if '.' in s1 else s1
        s2 = s2.split('.')[0] if '.' in s2 else s2
        return f"{s1}-{s2}"
    return "-"

# --- TAB 1: CALENDARIO ---
with tab1:
    df_raw = carica_calendario("Calendario_gironi")
    
    if not df_raw.empty:
        # --- ELABORAZIONE CAMPO 1 ---
        df_campo1 = df_raw[[0, 1, 2, 3, 4, 5]].dropna(subset=[0]).copy()
        df_campo1["Risultato"] = df_campo1.apply(lambda r: formatta_punteggio(r, 3, 4), axis=1)
        # Nuovo ordinamento: Risultato spostato alla fine (indice 5 è Squadra 2)
        df_campo1_final = df_campo1[[0, 1, 2, 5, "Risultato"]].copy()
        df_campo1_final.columns = ["Orario", "Girone", "Squadra 1", "Squadra 2", "Risultato"]
        
        # --- ELABORAZIONE CAMPO 2 ---
        df_campo2 = df_raw[[0, 7, 8, 9, 10, 11]].dropna(subset=[0]).copy()
        df_campo2["Risultato"] = df_campo2.apply(lambda r: formatta_punteggio(r, 9, 10), axis=1)
        # Nuovo ordinamento: Risultato spostato alla fine (indice 11 è Squadra 2)
        df_campo2_final = df_campo2[[0, 7, 8, 11, "Risultato"]].copy()
        df_campo2_final.columns = ["Orario", "Girone", "Squadra 1", "Squadra 2", "Risultato"]
        
        # --- MENU A SCOMPARSA CAMPO 1 ---
        with st.expander("🏟️ VISUALIZZA MATCH - CAMPO 1", expanded=True):
            st.dataframe(
                df_campo1_final, 
                use_container_width=False, 
                hide_index=True,
                column_config=config_colonne_campi
            )
            
        # --- MENU A SCOMPARSA CAMPO 2 ---
        with st.expander("🏟️ VISUALIZZA MATCH - CAMPO 2", expanded=False):
            st.dataframe(
                df_campo2_final, 
                use_container_width=False, 
                hide_index=True,
                column_config=config_colonne_campi
            )
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
        p1["Risultato"] = p1.apply(lambda r: formatta_punteggio(r, 3, 4), axis=1)
        p1_f = p1[[0, 1, 2, 5, "Risultato"]].copy()
        p1_f.columns = ["Orario", "Girone", "Squadra 1", "Squadra 2", "Risultato"]
        p1_f["Campo"] = "Campo 1"
        
        p2 = df_partite[[0, 7, 8, 9, 10, 11]].copy()
        p2["Risultato"] = p2.apply(lambda r: formatta_punteggio(r, 9, 10), axis=1)
        p2_f = p2[[0, 7, 8, 11, "Risultato"]].copy()
        p2_f.columns = ["Orario", "Girone", "Squadra 1", "Squadra 2", "Risultato"]
        p2_f["Campo"] = "Campo 2"
        
        df_totale = pd.concat([p1_f, p2_f]).dropna(subset=["Orario", "Squadra 1"])
        
        squadre = sorted(list(set(df_totale["Squadra 1"].dropna().unique()) | set(df_totale["Squadra 2"].dropna().unique())))
        scelta = st.selectbox("Seleziona la tua Squadra per vedere i tuoi orari:", [""] + squadre)
        
        if scelta:
            filtro = df_totale[(df_totale["Squadra 1"] == scelta) | (df_totale["Squadra 2"] == scelta)].sort_values(by="Orario")
            # Anche qui, Risultato va in fondo a destra dopo Squadra 2
            filtro = filtro[["Orario", "Campo", "Girone", "Squadra 1", "Squadra 2", "Risultato"]]
            
            config_colonne_ricerca = config_colonne_campi.copy()
            config_colonne_ricerca["Campo"] = st.column_config.TextColumn("Campo", width=75)
            
            st.dataframe(
                filtro, 
                use_container_width=False, 
                hide_index=True,
                column_config=config_colonne_ricerca
            )