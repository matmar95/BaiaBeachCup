import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configurazione Pagina e Rimozione Icone/Footer
st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")

# CSS per nascondere il menu (hamburger) e il footer "Made with Streamlit"
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Rende i tab più grandi e leggibili su mobile */
            .stTabs [data-baseweb="tab-list"] button {
                font-size: 20px;
                font-weight: bold;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. Parametri Google Sheets
SHEET_ID = "1nCJXDT4HQiHKalAiUr__aYi9szcGCyFL"

@st.cache_data(ttl=15)
def carica_foglio(nome_foglio):
    nome_encoded = urllib.parse.quote(nome_foglio)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nome_encoded}"
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# 3. Titolo Principale
st.title("🏐 Baia Beach Cup 2026")

# 4. Creazione dei Tab
tab1, tab2, tab3, tab4 = st.tabs(["📅 Calendario", "📊 Gironi", "🏆 Fasi Finali", "🔍 Partite Squadra"])

# --- TAB 1: CALENDARIO ---
with tab1:
    st.header("Calendario Completo")
    df_cal = carica_foglio("Calendario_gironi") # Assicurati che il nome sia corretto
    if not df_cal.empty:
        st.dataframe(df_cal, use_container_width=True, hide_index=True)
    else:
        st.info("Calendario in fase di caricamento...")

# --- TAB 2: GIRONI ---
with tab2:
    st.header("Classifiche Gironi")
    df_gironi = carica_foglio("Gironi")
    if not df_gironi.empty:
        st.dataframe(df_gironi, use_container_width=True, hide_index=True)
    else:
        st.info("I gironi verranno pubblicati a breve.")

# --- TAB 3: FASI FINALI ---
with tab3:
    st.header("Tabellone Fasi Finali")
    #nome_finali_encoded = urllib.parse.quote("Tabellone Finali")
    GID_TABELLONE = "1130118483"

    embed_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_TABELLONE}&range=A1:S40&widget=false&chrome=false&headers=false&rm=minimal"
    
    st.components.v1.iframe(embed_url, height=900, scrolling=True)

# --- TAB 4: LISTA PARTITE PER SQUADRA ---
with tab4:
    st.header("Cerca le tue partite")
    df_partite = carica_foglio("Calendario_gironi")
    
    if not df_partite.empty:
        # Cerchiamo di capire quali colonne contengono i nomi delle squadre (es. 'Squadra 1', 'Squadra 2')
        # Modifica i nomi qui sotto se nel tuo foglio si chiamano diversamente
        col_s1 = "Squadra 1" 
        col_s2 = "Squadra 2"
        
        if col_s1 in df_partite.columns and col_s2 in df_partite.columns:
            elenco_squadre = sorted(list(set(df_partite[col_s1].dropna().unique()) | set(df_partite[col_s2].dropna().unique())))
            squadra_scelta = st.selectbox("Seleziona la tua squadra:", [""] + elenco_squadre)
            
            if squadra_scelta:
                filtro = df_partite[(df_partite[col_s1] == squadra_scelta) | (df_partite[col_s2] == squadra_scelta)]
                st.table(filtro)
        else:
            st.warning("Verifica che le colonne 'Squadra 1' e 'Squadra 2' siano presenti nel foglio Calendario.")