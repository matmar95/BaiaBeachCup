import streamlit as st
import pandas as pd
import urllib.parse
import time
from datetime import datetime
import zoneinfo
import os
from PIL import Image

# 1. Configurazione Pagina (Caricamento Logo come Favicon se presente)
logo_path = "logo.png"
if os.path.exists(logo_path):
    try:
        img_logo = Image.open(logo_path)
        st.set_page_config(page_title="Baia Beach Cup 2026", page_icon=img_logo, layout="wide")
    except:
        st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")
else:
    st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")

# 2. CSS Blindato: Ottimizzazione Mobile, Centratura Totale e Spazi Compatti
st.markdown("""
    <style>
    header { display: none !important; height: 0px !important; }
    .stApp { background-color: #0d3c31 !important; color: #ffffff !important; }
    
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* --- CONTENITORE UNICO PER LOGO E TITOLI CENTRATI --- */
    .header-completo-centrato {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
        margin-top: 5px;
        margin-bottom: 2px;
    }
    
    /* Logo un pelo più grande (65px) e centrato */
    .logo-centrato-img {
        width: 65px !important;
        height: auto !important;
        margin-bottom: 2px !important;
    }

    /* Titolo Giallo senza margini extra */
    .titolo-giallo { 
        color: #fbb03f !important; 
        font-family: 'Poppins', sans-serif;
        font-size: 1.6rem !important; 
        font-weight: 700; 
        margin: 0 !important; 
        padding: 0 !important; 
        line-height: 1.1 !important;
        white-space: nowrap; 
    }
    
    /* Sottotitolo Azzurrino appiccicato al titolo */
    .sottotitolo-azzurro { 
        color: #7dcab2 !important; 
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem !important; 
        font-weight: 600; 
        margin: 2px 0 0 0 !important; 
        padding: 0 !important; 
        line-height: 1.1 !important;
    }

    /* Testo Ultimo Refresh Centrato */
    .refresh-text { 
        color: #aaaaaa; 
        font-size: 13px; 
        font-family: 'Poppins', sans-serif;
        text-align: center; 
        margin-bottom: 0.8rem !important; 
        margin-top: 10px;
        width: 100%;
    }
    
    /* --- COSTRUTTORE DI TAB PERFETTAMENTE CENTRATO --- */
    .stTabs [data-baseweb="tab-list"] { 
        justify-content: center !important; 
        display: flex !important;
        gap: 8px;
        width: 100% !important;
    }

    .stTabs [data-baseweb="tab"] { 
        font-size: 15px !important; 
        font-weight: bold !important; 
        color: #aaaaaa !important; 
        padding: 8px 10px !important; 
    }

    .stTabs [aria-selected="true"] { 
        color: #fbb03f !important; 
        border-bottom-color: #fbb03f !important; 
    }

    /* Fix Iframe e tabelle */
    [data-testid="stHtml"] { background-color: #0d3c31 !important; border-radius: 12px !important; }
    [data-testid="stHtml"] iframe { background-color: #0d3c31 !important; filter: invert(0.92) hue-rotate(110deg) brightness(0.9) contrast(1.1); zoom: 0.85; width: 118% !important; height: 860px !important; }
    </style>
""", unsafe_allow_html=True)

# Parametri Sheets
SHEET_ID = "1nCJXDT4HQiHKalAiUr__aYi9szcGCyFL"
GID_GIRONI_DATI = "1130118483"
GID_TABELLONE = "378239650"    

@st.cache_data(ttl=5)
def carica_dati_csv(nome_foglio):
    nome_encoded = urllib.parse.quote(nome_foglio)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nome_encoded}"
    try:
        df = pd.read_csv(url, header=None)
        return df
    except:
        return pd.DataFrame()

# --- PREPARAZIONE E RENDERING DELL'HEADER UNIFICATO ---
encoded_logo = ""
if os.path.exists(logo_path):
    import base64
    with open(logo_path, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()

if encoded_logo:
    # Stampa tutto unito: Logo, Titolo e Sottotitolo nello stesso blocco HTML
    st.markdown(f"""
        <div class="header-completo-centrato">
            <img src="data:image/png;base64,{encoded_logo}" class="logo-centrato-img">
            <h1 class="titolo-giallo">Baia Beach Cup</h1>
            <h2 class="sottotitolo-azzurro">2x2 Maschile</h2>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="header-completo-centrato">
            <h1 class="titolo-giallo">Baia Beach Cup</h1>
            <h2 class="sottotitolo-azzurro">2x2 Maschile</h2>
        </div>
    """, unsafe_allow_html=True)

# --- CONFIGURAZIONE COLONNE ---
config_colonne_campi = {
    "Orario": st.column_config.TextColumn("Orario", width=65),
    "Girone": st.column_config.TextColumn("Girone", width=50),
    "Squadra 1": st.column_config.TextColumn("Squadra 1", width=140),
    "Squadra 2": st.column_config.TextColumn("Squadra 2", width=140),
    "Risultato": st.column_config.TextColumn("Risultato", width=85),
}

config_colonne_gironi = {
    "Squadra": st.column_config.TextColumn("Squadra", width=150),
    "Giocate": st.column_config.NumberColumn("PG", width=45, format="%d"),
    "Vittorie": st.column_config.NumberColumn("V", width=45, format="%d"),
    "Sconfitte": st.column_config.NumberColumn("S", width=45, format="%d"),
    "Punti Fatti": st.column_config.NumberColumn("PF", width=50, format="%d"),
    "Punti Subiti": st.column_config.NumberColumn("PS", width=50, format="%d"),
    "Diff Punti": st.column_config.NumberColumn("DP", width=50, format="%d"),
    "Punti Totali": st.column_config.NumberColumn("Score", width=55, format="%.1f"),
    "Quoziente Punti": st.column_config.NumberColumn("Quot. Punti", width=85, format="%.4f"),
}

def formatta_punteggio(row, col_s1, col_s2):
    s1 = str(row[col_s1]).strip() if pd.notna(row[col_s1]) else ""
    s2 = str(row[col_s2]).strip() if pd.notna(row[col_s2]) else ""
    if s1 != "" and s2 != "" and s1 != "nan" and s2 != "nan":
        s1 = s1.split('.')[0] if '.' in s1 else s1
        s2 = s2.split('.')[0] if '.' in s2 else s2
        return f"{s1}-{s2}"
    return "-"

# --- LOGICA DI REFRESH AUTOMATICO (Ogni 60 secondi) ---
@st.fragment(run_every=60)
def rendering_applicazione():
    
    fuso_roma = zoneinfo.ZoneInfo("Europe/Rome")
    orario_attuale = datetime.now(fuso_roma).strftime("%H:%M:%S")
    st.markdown(f"<div class='refresh-text'>🔄 Ultimo aggiornamento dati: {orario_attuale}</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📅 CALENDARIO", "📊 GIRONI", "🏆 FASI FINALI", "🔍 CERCA SQUADRA"])

    # --- TAB 1: CALENDARIO ---
    with tab1:
        df_raw = carica_dati_csv("Calendario_gironi")
        if not df_raw.empty:
            if "orario" in str(df_raw.iloc[0, 0]).lower():
                df_raw = df_raw.iloc[1:].reset_index(drop=True)
                
            df_campo1 = df_raw[[0, 1, 2, 3, 4, 5]].dropna(subset=[0]).copy()
            df_campo1["Risultato"] = df_campo1.apply(lambda r: formatta_punteggio(r, 3, 4), axis=1)
            df_campo1_final = df_campo1[[0, 1, 2, 5, "Risultato"]].copy()
            df_campo1_final.columns = ["Orario", "Girone", "Squadra 1", "Squadra 2", "Risultato"]
            
            df_campo2 = df_raw[[0, 7, 8, 9, 10, 11]].dropna(subset=[0]).copy()
            df_campo2["Risultato"] = df_campo2.apply(lambda r: formatta_punteggio(r, 9, 10), axis=1)
            df_campo2_final = df_campo2[[0, 7, 8, 11, "Risultato"]].copy()
            df_campo2_final.columns = ["Orario", "Girone", "Squadra 1", "Squadra 2", "Risultato"]
            
            with st.expander("CAMPO MARE (1)", expanded=True):
                st.dataframe(df_campo1_final, use_container_width=False, hide_index=True, column_config=config_colonne_campi)
                
            with st.expander("CAMPO MONTE (2)", expanded=False):
                st.dataframe(df_campo2_final, use_container_width=False, hide_index=True, column_config=config_colonne_campi)
        else:
            st.info("Il calendario è in fase di compilazione.")

    # --- TAB 2: GIRONI ---
    with tab2:
        df_gironi_raw = carica_dati_csv("Gironi")
        
        if not df_gironi_raw.empty:
            gironi_validi = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
            
            for i in range(len(df_gironi_raw)):
                valore_cella = str(df_gironi_raw.iloc[i, 0]).strip()
                
                if valore_cella in gironi_validi:
                    nome_girone = valore_cella
                    
                    start_idx = i + 1
                    end_idx = min(start_idx + 4, len(df_gironi_raw))
                    
                    block = df_gironi_raw.iloc[start_idx:end_idx].copy()
                    
                    if block.shape[1] >= 8:
                        block = block.iloc[:, 0:8]
                        block.columns = ["Squadra", "Giocate", "Vittorie", "Sconfitte", "Punti Fatti", "Punti Subiti", "Diff Punti", "Punti Totali"]
                        
                        for col in ["Giocate", "Vittorie", "Sconfitte", "Punti Fatti", "Punti Subiti", "Diff Punti", "Punti Totali"]:
                            block[col] = pd.to_numeric(block[col], errors='coerce').fillna(0)
                        
                        block["Quoziente Punti"] = block.apply(
                            lambda r: float(r["Punti Fatti"]) / float(r["Punti Subiti"]) if float(r["Punti Subiti"]) > 0 else float(r["Punti Fatti"]), 
                            axis=1
                        )
                        
                        block = block.sort_values(by=["Punti Totali", "Vittorie", "Quoziente Punti"], ascending=[False, False, False])
                        
                        st.markdown(f"### GIRONE {nome_girone}")
                        st.dataframe(
                            block[["Squadra", "Giocate", "Vittorie", "Sconfitte", "Punti Fatti", "Punti Subiti", "Diff Punti", "Punti Totali", "Quoziente Punti"]],
                            use_container_width=False,
                            hide_index=True,
                            column_config=config_colonne_gironi
                        )
        else:
            st.info("Le classifiche dei gironi saranno disponibili all'inizio dei match.")

    # --- TAB 3: FASI FINALI ---
    with tab3:
        timestamp_cache = int(time.time())
        embed_tabellone = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid={GID_TABELLONE}&range=A1:S35&widget=false&chrome=false&headers=false&rm=minimal&cb={timestamp_cache}"
        st.components.v1.iframe(embed_tabellone, height=730, scrolling=False)

    # --- TAB 4: RICERCA SQUADRA ---
    with tab4:
        df_partite = carica_dati_csv("Calendario_gironi")
        if not df_partite.empty:
            if "orario" in str(df_partite.iloc[0, 0]).lower():
                df_partite = df_partite.iloc[1:].reset_index(drop=True)
                
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
                filtro = filtro[["Orario", "Campo", "Girone", "Squadra 1", "Squadra 2", "Risultato"]]
                
                config_colonne_ricerca = config_colonne_campi.copy()
                config_colonne_ricerca["Campo"] = st.column_config.TextColumn("Campo", width=75)
                
                st.dataframe(filtro, use_container_width=False, hide_index=True, column_config=config_colonne_ricerca)

# Esecuzione
rendering_applicazione()