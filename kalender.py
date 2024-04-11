import streamlit as st
import datetime
import win32com.client
import os
import time
import psutil
import pythoncom
import win32gui
import win32con
import pywhatkit as kit
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
    #Datum zusammensetzen
    start = datetime.datetime.combine(d,t)
    end = start + datetime.timedelta(hours=2)
    film = st.text_input("Filmtitel:", "The Lord of the Rings: The Fellowship of the Ring")
    auswahl = st.selectbox("Was möchtest du erstellen?", ["Kalendertermin", "E-Mail", "Whatsapp"])
    if auswahl == "Kalendertermin":
        if st.button("Kalender eintragen"):
            outlook_kalender(f"{film} schauen",start, end,"Büro", "Hi")
            st.success("Kalendereintrag erfolgreich!")
            #Code
            st.subheader("Code:")
            markdown_text = """
            def outlook_run():
                for process in psutil.process_iter(['pid', 'name']):
                    if 'OUTLOOK.EXE' in process.info['name']:
                    return True
                return False

            def outlook_kalender(betreff, start, ende, ort=None, text=None):
                pythoncom.CoInitialize()
                if outlook_run():
                    outlook = win32com.client.Dispatch("Outlook.Application")
                else:
                    # Pfad zur Outlook-EXE-Datei
                    outlook_exe_path = r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE" 
                    os.startfile(outlook_exe_path)
                    time.sleep(5)  # Warte 5 Sekunden
                    outlook = win32com.client.Dispatch("Outlook.Application")

                    termin = outlook.CreateItem(1)  # 1 bedeutet Termin, 2 bedeutet Besprechung
                    termin.Subject = betreff
                    termin.Start = start
                    termin.End = ende
                    termin.Location = ort
                    termin.Body = text
                    termin.Save()
                    pythoncom.CoUninitialize()
            """
            st.code(markdown_text)
            #Trennlinie
            st.markdown(
            """<hr style="border-top: 4px solid white;">""",
            unsafe_allow_html=True)
    elif auswahl =="E-Mail":
        #Eingabe für Mail
        st.subheader("E-Mail erstellen")
        betreff = st.text_input("Betreff")
        text = st.text_area("Text")
        empfänger = st.text_input("Empfänger (E-Mail-Adressen, durch Komma getrennt)")
        #Mail senden
        if st.button("E-Mail senden"):
            mail(betreff, text, empfänger)
            st.success("E-Mail erfolgreich versendet!")
            #Code
            st.subheader("Code:")
            markdown_text = """
            def mail(betreff, text, empfänger):
                pythoncom.CoInitialize()
                if outlook_run():
                    outlook = win32com.client.Dispatch("Outlook.Application")
                else:
                    # Pfad zur Outlook-EXE-Datei
                    outlook_exe_path = r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE"  
                    os.startfile(outlook_exe_path)
                    time.sleep(5)  # Warte 5 Sekunden
                    outlook = win32com.client.Dispatch("Outlook.Application")

                mail = outlook.CreateItem(0)  
                mail.Subject = betreff
                mail.Body = text
                mail.To = empfänger  
                mail.Display()
                # Beispielaufruf für Outlook-Kalender/Mail
                titel = fenstertitel("rctrl_renwnd32")
                if titel is not None:
                    st.info(f"Fenstertitel gefunden: {titel}")
                    vollbildmodus("rctrl_renwnd32")
                else:
                    st.info("Fenster nicht gefunden.")
                pythoncom.CoUninitialize()
            
            
            def vollbildmodus(fensterklasse):
                hwnd = win32gui.FindWindow(fensterklasse, None)
                if hwnd != 0:
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    #Fenster in den Vordergrund + Vollbild
                    win32gui.SetForegroundWindow(hwnd)
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    return True
                else:
                    return False
                
                
            def fenstertitel(fensterklasse):
                hwnd = win32gui.FindWindow(fensterklasse, None)
                if hwnd != 0:
                    return win32gui.GetWindowText(hwnd)
                else:
                    return None
                        """
            st.code(markdown_text)
            #Trennlinie
            st.markdown(
            """<hr style="border-top: 4px solid white;">""",
            unsafe_allow_html=True)
    else:
        st.subheader("Whatsapp erstellen")
        text = st.text_area("Text")
        empfänger = st.text_input("Nummer oder Name")
        #Code
        st.subheader("Code:")
        markdown_text = """def whatsapp(nummer, text):
            receiver_number = nummer
             message = text
            now = datetime.datetime.now()
            send_time = now + datetime.timedelta(seconds=60)
            kit.sendwhatmsg(receiver_number, message,  send_time.hour, send_time.minute)"""
        st.code(markdown_text)
        #Trennlinie
        st.markdown(
        """<hr style="border-top: 4px solid white;">""",
        unsafe_allow_html=True)
        
        if st.button("Whatsapp senden"):
            whatsapp(empfänger, text)
            st.success("Whatsapp erfolgreich versendet!")

###########################################

#Hilfsfunktionen

###########################################
#Kalendereintrag
def outlook_kalender(betreff, start, ende, ort=None, text=None):
    pythoncom.CoInitialize()
    if outlook_run():
        outlook = win32com.client.Dispatch("Outlook.Application")
    else:
    # Pfad zur Outlook-EXE-Datei
        outlook_exe_path = r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE"  
        os.startfile(outlook_exe_path)
        time.sleep(5)  # Warte 5 Sekunden
        outlook = win32com.client.Dispatch("Outlook.Application")

    termin = outlook.CreateItem(1)  # 1 bedeutet Termin, 2 bedeutet Besprechung
    termin.Subject = betreff
    termin.Start = start
    termin.End = ende
    termin.Location = ort
    termin.Body = text
    termin.Save()
    pythoncom.CoUninitialize()
###########################################
#Mail erstellen
def mail(betreff, text, empfänger):
    pythoncom.CoInitialize()
    if outlook_run():
        outlook = win32com.client.Dispatch("Outlook.Application")
    else:
    # Pfad zur Outlook-EXE-Datei
        outlook_exe_path = r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE"  
        os.startfile(outlook_exe_path)
        time.sleep(5)  # Warte 5 Sekunden
        outlook = win32com.client.Dispatch("Outlook.Application")

    mail = outlook.CreateItem(0)  
    mail.Subject = betreff
    mail.Body = text
    mail.To = empfänger  
    mail.Display()
    # Beispielaufruf für Outlook-Kalender/Mail
    titel = fenstertitel("rctrl_renwnd32")
    if titel is not None:
        st.info(f"Fenstertitel gefunden: {titel}")
        vollbildmodus("rctrl_renwnd32")
    else:
        st.info("Fenster nicht gefunden.")
    pythoncom.CoUninitialize()
###########################################
#Alle Läufenden Prozesse (Id, Name) überprüfen
def outlook_run():
    for process in psutil.process_iter(['pid', 'name']):
        if 'OUTLOOK.EXE' in process.info['name']:
            return True
    return False
###########################################
#Vollbildmodus + Vordergrund
def vollbildmodus(fensterklasse):
    #Handle to a Window -> Identifiaktor für das Window Fenster
    hwnd = win32gui.FindWindow(fensterklasse, None)
    if hwnd != 0:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        #Fenster in den Vordergrund + Vollbild
        print(hwnd)
        win32gui.SetForegroundWindow(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        return True
    else:
        return False
###########################################
#Fenstertitel vorhanden?
def fenstertitel(fensterklasse):
    hwnd = win32gui.FindWindow(fensterklasse, None)
    if hwnd != 0:
        return win32gui.GetWindowText(hwnd)
    else:
        return None
###########################################
#Whatsapp
def whatsapp(nummer, text):
    receiver_number = nummer
    message = text
    now = datetime.datetime.now()
    send_time = now + datetime.timedelta(seconds=60)

    kit.sendwhatmsg(receiver_number, message,  send_time.hour, send_time.minute)
