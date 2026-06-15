import streamlit as st
import pandas as pd
import urllib.parse
import time
from datetime import datetime
import zoneinfo
import os

# 1. Configurazione Pagina
st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")

# 2. CSS Blindato
st.markdown("""
    <style>
    header { display: none !important; }
    .stApp { background-color: #0d3c31 !important; color: #ffffff !important; }
    #MainMenu, footer { visibility: hidden; }
    
    .main .block-container { padding: 0.5rem 1rem !important; }
    
    h2 {
        color: #fbb03f !important;
        font-family: 'Poppins', sans-serif;
        text-align: center;
        margin: 0.5rem 0 !important;
        font-size: 1.3rem !important;
        white-space: nowrap;
    }

    .refresh-text { color: #aaaaaa; font-size: 12px; text-align: center; margin-bottom: 0.5rem !important; }
    
    /* Fix Iframe e Sfondo */
    [data-testid="stHtml"], [data-testid="stIframe"], .element-container {
        background-color: #0d3c31 !important;
    }
    
    iframe {
        background-color: #0d3c31 !important;
        filter: invert(0.92) hue-rotate(110deg) brightness(0.9) contrast(1.1);
        zoom: 0.85;
        width: 118% !important;
        height: 860px !important;
    }

    .stTabs [aria-selected="true"] { color: #fbb03f !important; border-bottom-color: #fbb03f !important; }
    </style>
    """, unsafe_allow_html=True)

# Parametri Sheets
SHEET_ID = "1nCJXDT4HQiHKalAiUr__aYi9szcGCyFL"
GID_TABELLONE = "378239650"    

@st.cache_data(ttl=5)
def carica_dati_csv(nome_foglio):
    nome_encoded = urllib.parse.quote(nome_foglio)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nome_encoded}"
    try: return pd.read_csv(url, header=None)
    except: return pd.DataFrame()

# --- LOGO E TITOLO ---
logo_path = "logo.png"
if os.path.exists(logo_path):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(logo_path, width=40) # Dimensione fissa 40px
else:
    st.write("Logo non trovato")

st.markdown("<h2>Baia Beach Cup - 2x2 Maschile</h2>", unsafe_allow_html=True)

# --- APP ---
@st.fragment(run_every=60)
def rendering_applicazione():
    orario_attuale = datetime.now(zoneinfo.ZoneInfo("Europe/Rome")).strftime("%H:%M:%S")
    st.markdown(f"<div class='refresh-text'>🔄 Aggiornato: {orario_attuale}</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📅 CALENDARIO", "📊 GIRONI", "🏆 FASI FINALI", "🔍 CERCA"])

    with tab3:
        timestamp_cache = int(time.time())
        embed_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_TABELLONE}&range=A1:S35&widget=false&chrome=false&headers=false&rm=minimal&cb={timestamp_cache}"
        st.components.v1.iframe(embed_url, height=730, scrolling=True)

    # Nota: Aggiungi qui le altre Tab (Calendario, Gironi, Cerca) come nel codice precedente
    with tab1: st.write("Calendario...")
    with tab2: st.write("Gironi...")
    with tab4: st.write("Cerca...")

rendering_applicazione()