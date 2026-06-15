import streamlit as st
import pandas as pd

# Configurazione iniziale della pagina sportiva
st.set_page_config(page_title="Baia Beach Cup 2026", page_icon="🏐", layout="wide")

st.title("🏐 Baia Beach Cup 2026 - Risultati Live")

# ID del tuo foglio Google ricavato dal tuo URL
SHEET_ID = "1nCJXDT4HQiHKalAiUr__aYi9szcGCyFL"

# Funzione per leggere i gironi convertendo al volo il foglio in CSV
@st.cache_data(ttl=15) # Aggiorna i dati ogni 15 secondi automaticamente
def carica_gironi():
    # GID 1130118483 corrisponde alla tab dei Gironi
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1130118483"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Errore nel recupero dati: {e}")
        return None

# Menu di Navigazione
scelta = st.sidebar.radio("Navigazione Torneo:", ["Gironi & Classifiche", "Fasi Finali (Tabellone)"])

if scelta == "Gironi & Classifiche":
    st.header("🏆 Situazione Gironi")
    st.write("I dati si aggiornano automaticamente ogni 15 secondi.")
    
    df_gironi = carica_gironi()
    
    if df_gironi is not None:
        # Mostriamo l'intera tabella strutturata dei gironi
        # Streamlit la formatterà in modo pulito e scorrevole
        st.dataframe(df_gironi, use_container_width=True, hide_index=True)

elif scelta == "Fasi Finali (Tabellone)":
    st.header("🌳 Tabellone Ad Eliminazione Diretta")
    st.write("Visualizzazione in tempo reale dal centro della regia:")
    
    # TRUCCO: Invece di ricostruire la grafica in Python, incorporiamo il foglio Google 
    # focalizzato esattamente sulla porzione del Tabellone Finali.
    # Usiamo un iframe HTML per mostrare in tempo reale la tua struttura ad albero.
    embed_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlembed?gid=1130118483&widget=false&chrome=false"
    
    st.components.v1.iframe(embed_url, height=600, scrolling=True)
