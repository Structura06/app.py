# Streamlit app for Structura
import streamlit as st
import datetime
import json
import os

st.set_page_config(page_title="Structura", layout="wide")
st.title("🏗️ Structura – AD CALEUM – DREJT QIEJVE")

st.sidebar.header("📋 Shërbimet")
section = st.sidebar.radio("Përdor:", [
    "Kalendari i punës", "Llogaritësi i tarifave", "Mjete arkitekture", "Klientë dhe arkitektë", "Regjistrohu!"])

# Initialize session state for events
if "events" not in st.session_state:
    st.session_state["events"] = []

if "edit_index" not in st.session_state:
    st.session_state["edit_index"] = None

# 1. Kalendari i Punës (Work Calendar)
if section == "Kalendari i punës":
    st.header("📅 Kalendari i Punës")
    st.markdown("Shto ngjarjet dhe shiko afatet e projekteve që afrohesh.")

    # Form for adding or editing events
    with st.form(key="event_form"):
        if st.session_state["edit_index"] is None:
            start_date = st.date_input("Data e Fillimit (DD/MM/YYYY)", datetime.date.today())
            end_date = st.date_input("Data e Mbarimit (DD/MM/YYYY)", datetime.date.today())
            desc = st.text_input("Përshkrimi i Ngjarjes")
            submit = st.form_submit_button("Shto Ngjarjen")
        else:
            event = st.session_state["events"][st.session_state["edit_index"]]
            start_date = st.date_input("Data e Fillimit (DD/MM/YYYY)", datetime.datetime.strptime(event["start"], "%Y-%m-%d").date())
            end_date = st.date_input("Data e Mbarimit (DD/MM/YYYY)", datetime.datetime.strptime(event["end"], "%Y-%m-%d").date())
            desc = st.text_input("Përshkrimi i Ngjarjes", event["desc"])
            submit = st.form_submit_button("Përditëso")

        if submit:
            if start_date > end_date:
                st.error("Data e fillimit duhet të jetë përpara datës së mbarimit.")
            elif not desc:
                st.warning("Ju lutem vendosni një përshkrim.")
            else:
                new_event = {
                    "start": str(start_date),
                    "end": str(end_date),
                    "desc": desc
                }
                if st.session_state["edit_index"] is None:
                    st.session_state["events"].append(new_event)
                    st.success("Ngjarja u shtua!")
                else:
                    st.session_state["events"][st.session_state["edit_index"]] = new_event
                    st.success("Ngjarja u përditësua!")
                    st.session_state["edit_index"] = None

    # Display events
    st.markdown("### Ngjarjet e Ruajtura:")
    for i, event in enumerate(st.session_state["events"]):
        start_fmt = datetime.datetime.strptime(event["start"], "%Y-%m-%d").strftime("%d/%m/%Y")
        end_fmt = datetime.datetime.strptime(event["end"], "%Y-%m-%d").strftime("%d/%m/%Y")
        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            st.write(f"📌 {start_fmt} → {end_fmt}: {event['desc']}")
        with col2:
            if st.button("✏️", key=f"edit_{i}"):
                st.session_state["edit_index"] = i
        with col3:
            if st.button("🗑️", key=f"delete_{i}"):
                st.session_state["events"].pop(i)
                st.success("Ngjarja u fshi!")
                st.experimental_rerun()

# 2. Llogaritësi i tarifave
elif section == "Llogaritësi i tarifave":
    st.header("💰 Llogarit Pagesën")
    st.markdown("Vendos të dhënat për të llogaritur pagesën e arkitektit.")

    vështirësia = st.selectbox("Zgjidhni vështirësinë e punës:", ["e lehtë", "mesatare", "e vështirë"])
    madhesia_e_apartamentit = st.number_input("Vendosni madhësinë e apartamentit (në m²):", min_value=1)
    projekti = st.selectbox("Zgjidhni projektin:", ["projekt arkitektonik", "dizajn interieri"])

    if st.button("Llogarit"):
        tarifa_per_m2 = 500

        if vështirësia == "e lehtë":
            shumezues_vështirësie = 2
        elif vështirësia == "mesatare":
            shumezues_vështirësie = 3
        elif vështirësia == "e vështirë":
            shumezues_vështirësie = 4

        if projekti == "projekt arkitektonik":
            shumezues_projekti = 2
        elif projekti == "dizajn interieri":
            shumezues_projekti = 1

        pagesa = (madhesia_e_apartamentit * tarifa_per_m2) * shumezues_vështirësie * shumezues_projekti
        pagesa_me_takse = pagesa * (1 - 0.15)

        st.success(f"📊 Pagesa totale që përfitoni është: **{int(pagesa_me_takse):,} lekë**")

# 3. Manual & Resources
elif section == "Mjete arkitekture":
    st.header("📘 Manuali i Projektit & Burime")
    st.markdown("### Lidhje të dobishme:")
    st.link_button("Forumi i Arkitekturës", "https://www.archinect.com/forum")
    st.link_button("Frymëzim për Dizajn", "https://www.archdaily.com")

    st.markdown("### PDF të Projektit:")
    st.link_button("📄 Shkarko Manualin e Projektit", "https://example.com/brief.pdf")
    st.link_button("📄 Udhëzime Strukturore", "https://example.com/guidelines.pdf")

# 4. Client-Architect Match (Gale-Shapley)
elif section == "Klientë dhe arkitektë":
    st.header("🔗 Shembull i Përshtatjes Klient-Arkitekt")

    clients = {
        "Klienti A": ["Arkitekti X", "Arkitekti Y", "Arkitekti Z"],
        "Klienti B": ["Arkitekti Y", "Arkitekti X", "Arkitekti Z"],
        "Klienti C": ["Arkitekti X", "Arkitekti Z", "Arkitekti Y"]
    }

    architects = {
        "Arkitekti X": ["Klienti B", "Klienti A", "Klienti C"],
        "Arkitekti Y": ["Klienti A", "Klienti C", "Klienti B"],
        "Arkitekti Z": ["Klienti C", "Klienti B", "Klienti A"]
    }

    def stable_matching(clients, architects):
        free_clients = list(clients.keys())
        engagements = {}
        client_proposals = {client: [] for client in clients}

        while free_clients:
            client = free_clients[0]
            client_prefs = clients[client]

            for architect in client_prefs:
                if architect not in client_proposals[client]:
                    client_proposals[client].append(architect)

                    if architect not in engagements:
                        engagements[architect] = client
                        free_clients.pop(0)
                        break
                    else:
                        current = engagements[architect]
                        if architects[architect].index(client) < architects[architect].index(current):
                            engagements[architect] = client
                            free_clients.pop(0)
                            free_clients.append(current)
                            break
        return engagements

    if st.button("Trego Përshtatjet"):
        matches = stable_matching(clients, architects)
        for architect, client in matches.items():
            st.write(f"{architect} ↔ {client}")

# 5. Register Now
elif section == "Regjistrohu!":
    st.header("📝 Regjistrohu tani")
    st.markdown("Plotësoni formularin për t'u listuar si Arkitekt ose Klient.")
    st.markdown("[Regjistrohu përmes Formularit të Google](https://forms.gle/your-form-link)")
    st.markdown("### Përdorues të Regjistruar:")
    st.write("- Klienti A")
    st.write("- Arkitekti X")
    st.caption("(Për lidhjen e fletës së Google, përdorni API ose përditësoni manualisht listën)")

