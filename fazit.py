import streamlit as st
import datetime
###########################################

#Main Funktion

###########################################

def start():
    st.header("Terminplaner")
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        d = st.date_input("Wann willst du den Film schauen?", datetime.date.today(),format="DD.MM.YYYY")
        st.write("Du willst den Film schauen:", d.strftime("%d.%m.%Y"))
    with col2:
        t = st.time_input("Uhrzeit des Films", datetime.time(8, 45))
        st.write("Uhrzeit des Films:", t.strftime("%H:%M"))
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    if st.button("Kalender eintragen"):
        st.write("Hallo")
        pass
###########################################

#Hilfsfunktionen

###########################################