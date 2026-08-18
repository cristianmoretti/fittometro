import pandas as pd 
import streamlit as st 
import time 

st.set_page_config(layout="wide", page_title="fitto-metro")

st.title("Fitto-Metro")
st.write("Inserisci i costi per ogni voce e calcola il tuo prospetto")

st.info("Sia il fitto che i costi inseriti devono essere annuali!")
fitto = st.number_input(label="Fitto 🏠", step=1, min_value=0, format="%d")

col1, col2, col3 = st.columns(3)
with col1:  
    gas = st.number_input(label="Gas 🔥", step=1, min_value=0, format="%d")
with col2:
    luce = st.number_input(label="Luce 💡", step=1, min_value=0, format="%d")
with col3:
    acqua = st.number_input(label="Acqua 💧", step=1, min_value=0, format="%d")

if "primo_subtotale_valore" not in st.session_state: 
    st.session_state.primo_subtotale_valore = 0

col1,col2 = st.columns([8,2])
with col1: 
    primo_subtotale = st.empty() 
    primo_subtotale.metric("Primo subtotale (fitto netto)", f"{st.session_state.primo_subtotale_valore} €")
with col2:
    primo_button = st.button("Calcola il primo subtotale") 

if primo_button: 
    with st.spinner("Calcolo in corso del primo subtotale..."):
        time.sleep(1) 
    st.session_state.primo_subtotale_valore = fitto - gas - luce - acqua 
    
    if st.session_state.primo_subtotale_valore >= 0:
        primo_messaggio_successo = st.success("Primo subtotale calcolato con successo!") 
        primo_subtotale.metric("Primo subtotale (fitto netto)", f"{st.session_state.primo_subtotale_valore} €")
        time.sleep(3) 
        primo_messaggio_successo.empty() 
    else: 
        primo_messaggio_errore = st.error("Il primo subtotale non può essere negativo!") 
        time.sleep(3) 
        primo_messaggio_errore.empty()

if "secondo_subtotale_valore" not in st.session_state:
    st.session_state.secondo_subtotale_valore = 0
col1, col2 = st.columns(2) 
with col1: 
    internet = st.number_input(label="Internet 🌐", step=1, min_value=0, format="%d")
with col2: 
    allarme = st.number_input(label="Allarme 🚨", step=1, min_value=0, format="%d")

col1, col2 = st.columns([8,2])
with col1: 
    secondo_subtotale = st.empty() 
    secondo_subtotale.metric("Secondo subtotale (fitto netto)", f"{st.session_state.secondo_subtotale_valore} €")
with col2: 
    secondo_subtotale_button = st.button("Calcola il secondo subtotale") 

if secondo_subtotale_button:
    with st.spinner("Calcolo in corso del secondo subtotale..."): 
        time.sleep(1) 
    st.session_state.secondo_subtotale_valore = st.session_state.primo_subtotale_valore - internet - allarme
    if st.session_state.secondo_subtotale_valore >= 0: 
        secondo_messaggio_successo = st.success("Secondo subtotale calcolato con successo!")
        secondo_subtotale.metric("Secondo subtotale (fitto netto)", f"{st.session_state.secondo_subtotale_valore} €")
        time.sleep(3)
        secondo_messaggio_successo.empty()
    else: 
        secondo_messaggio_errore = st.error("Il secondo subtotale non può essere negativo!")
        time.sleep(3) 
        secondo_messaggio_errore.empty() 

col1, col2 = st.columns(2)
with col1:
    tari = st.number_input(label="TARI 🏷️", step=1, min_value=0, format="%d")
with col2:
    ascensore = st.number_input(label="Ascensore 🛗", step=1, min_value=0, format="%d")

col1, col2, col3 = st.columns([8, 0.9, 1])
with col1: 
    totale = st.empty() 
    totale.metric("Totale (fitto netto)", f"{st.session_state.get('totale_valore', 0)} €")
with col2: 
    button = st.button("Calcola")
with col3: 
    dettaglio = st.toggle("Dettaglio") 

if "totale_valore" not in st.session_state:
    st.session_state.totale_valore = 0

if button: 
    with st.spinner("Calcolo in corso..."): 
        time.sleep(1)
    st.session_state.primo_subtotale_valore = fitto - gas - luce - acqua
    st.session_state.secondo_subtotale_valore = (
        st.session_state.primo_subtotale_valore - internet - allarme
    )
    st.session_state.totale_valore = (
        st.session_state.secondo_subtotale_valore - tari - ascensore
    )
    totale.metric("Totale (fitto netto)", f"{st.session_state.totale_valore} €")
    if st.session_state.totale_valore >= 0:
        primo_subtotale.metric("Primo subtotale (fitto netto)", f"{st.session_state.primo_subtotale_valore} €")
        secondo_subtotale.metric("Secondo subtotale (fitto netto)", f"{st.session_state.secondo_subtotale_valore} €")
        totale.metric("Totale (fitto netto)", f"{st.session_state.totale_valore} €")
        messaggio_successo = st.success("Calcolo eseguito correttamente!")
        time.sleep(3) 
        messaggio_successo.empty() 
    else:
        messaggio_errore = st.error("Il totale non può essere negativo!")
        time.sleep(3)
        messaggio_errore.empty()

col1, col2 = st.columns([4,6])
with col1: 
    affitto_cedolare_secca = st.number_input(label="Affitto cedolare secca 💰", step=1, min_value=0, format="%d")
with col2:
    st.empty() 

def evidenzia_riga(riga): 
    if riga["voce"] in ["subtotale", "totale", "totale dopo le tasse"]: 
        return ["font-weight: bold"] * len(riga)
    return [""] * len(riga)

if dettaglio: 
    st.session_state.primo_subtotale_valore = fitto - gas - luce - acqua
    st.session_state.secondo_subtotale_valore = (
        st.session_state.primo_subtotale_valore - internet - allarme
    )
    st.session_state.totale_valore = (
        st.session_state.secondo_subtotale_valore - tari - ascensore
    )
    #create a dataframe in pandas 
    dettaglio = pd.DataFrame({"voce": ["fitto", "gas", "luce", "acqua", "subtotale", "internet", "allarme", "subtotale", "tari", "ascensore", "totale", "cedolare secca", "totale dopo le tasse"],
                "costo annuale": [fitto, gas, luce, acqua, st.session_state.primo_subtotale_valore, internet, allarme, st.session_state.secondo_subtotale_valore, tari, ascensore, st.session_state.totale_valore, affitto_cedolare_secca*0.21, st.session_state.totale_valore - affitto_cedolare_secca*0.21]})
    dettaglio["costo annuale"] = dettaglio["costo annuale"].astype(int)
    dettaglio["costo mensile"] = (dettaglio["costo annuale"] / 12).astype(int) 
    dettaglio["Costo mensile (2 persone)"] = dettaglio.apply(
        lambda riga: riga["costo annuale"] / 12 
        if riga["voce"] == "fitto"
        else riga["costo annuale"] / (12 * 2), 
        axis=1 
    ).astype(int) 
    st.dataframe(dettaglio.style.apply(evidenzia_riga, axis=1), use_container_width=True)