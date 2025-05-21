import streamlit as st
import datetime
import json
import os
import pandas as pd

# Set up page config
st.set_page_config(page_title="Structura", layout="wide")
st.title("🏗️ Structura – AD CALEUM – DREJT QIEJVE")

# Sidebar for navigation
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
    st.markdown("Takim pune? Afate të ngjeshura? Përdorni Kalendarin tonë të Punës!")

    # Form for adding or editing events
    with st.form(key="event_form"):
        if st.session_state["edit_index"] is None:
            start_date = st.date_input("Data e Fillimit (Ditë/Muaj/Vit)", datetime.date.today())
            end_date = st.date_input("Data e Mbarimit (Ditë/Muaj/Vit)", datetime.date.today())
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
    st.header("💰 Llogarit Tarifën")
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

        st.success(f"📊 Kuota është **{int(pagesa):,} lekë**")
        st.success(f"📊 Kuota pas taksave është **{int(pagesa_me_takse):,} lekë**")

# 3. Mjete arkitekture
elif section == "Mjete arkitekture":
    st.markdown("### Lidhje të dobishme:")
    st.link_button("Forumi Archinect", "https://www.archinect.com/forum")
    st.link_button("r/architecture", "https://www.reddit.com/r/architecture/")
    st.link_button("Qiellgërvishtësja", "https://www.skyscrapercity.com/forums/architecture.4/")

    st.markdown("### Manuale përdorimi:")
    st.link_button("📄 Ornamenti dhe krimi - Loos, Adolf", "https://www2.gwu.edu/~art/Temporary_SL/177/pdfs/Loos.pdf")
    st.link_button("📄 Modernizmi, armiku ynë - van der Rohe, Mies", "https://newcriterion.com/article/is-modernism-the-enemy-the-case-of-mies-van-der-rohe/")

    st.markdown("### Puna e arkitektëve nëpër botë:")
    st.link_button("Studim i Pezo von Erlichshausen", "https://www.instagram.com/p/DIGX6dzt8Js/?igsh=MTRzYTlieGFvd2E0cw%3D%3D")
    st.link_button("Hapësira dhe vëllimi", "https://www.instagram.com/p/C7MPI-lNk-D/?img_index=1&igsh=aW9jMzRjNmhmbjB0")
    st.link_button("Guggenheim, Bilbao", "https://www.guggenheim-bilbao.eus/en")

# 4. Klientë dhe arkitektë (First-Come, First-Serve Matching)
elif section == "Klientë dhe arkitektë":
    st.header("🔗 Përshtatja Klient–Arkitekt")

    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQOB4uubKZ9g9BBv2NCTcluURvS_mmqvyax5yL926N6qWrj3SeGEuyFCWI3lUGvyffxRWcUrSM5-2gd/pub?gid=661964427&single=true&output=csv"

    try:
        data = pd.read_csv(sheet_url)

        required_columns = {"Emri dhe mbiemri", "Sektori"}
        if not required_columns.issubset(set(data.columns)):
            st.error("Të dhënat në Google Sheet nuk kanë kolonat e kërkuara: 'Emri dhe mbiemri' dhe 'Sektori'.")
        else:
            # Normalize sector column
            data["Sektori"] = data["Sektori"].str.strip().str.lower()

            # Separate by role
            clients = data[data["Sektori"] == "klient"].reset_index(drop=True)
            architects = data[data["Sektori"] == "arkitekt"].reset_index(drop=True)

            # Show full lists
            st.subheader("📋 Lista e klientëve")
            if not clients.empty:
                st.write(clients["Emri dhe mbiemri"])
            else:
                st.info("Asnjë klient nuk është regjistruar.")

            st.subheader("📋 Lista e arkitektëve")
            if not architects.empty:
                st.write(architects["Emri dhe mbiemri"])
            else:
                st.info("Asnjë arkitekt nuk është regjistruar.")

            # FCFS Matching
            st.subheader("🧩 Përshtatjet")
            min_len = min(len(clients), len(architects))
            matches = []

            for i in range(min_len):
                matches.append({
                    "Klient": clients.loc[i, "Emri dhe mbiemri"],
                    "Arkitekt": architects.loc[i, "Emri dhe mbiemri"]
                })

            if matches:
                for pair in matches:
                    st.write(f"👤 {pair['Klient']} ↔ 👷 {pair['Arkitekt']}")
            else:
                st.info("Nuk ka të dhëna të mjaftueshme për të bërë përshtatje.")

            # Remaining unmatched
            if len(clients) > len(architects):
                st.subheader("👤 Klientë pa arkitekt:")
                for name in clients["Emri dhe mbiemri"].iloc[min_len:]:
                    st.write(name)

            elif len(architects) > len(clients):
                st.subheader("👷 Arkitektë pa klient:")
                for name in architects["Emri dhe mbiemri"].iloc[min_len:]:
                    st.write(name)

    except Exception as e:
        st.error("❌ Nuk mund të lexoj të dhënat nga Google Sheets.")
        st.exception(e)


# 5. Regjistrohu!
elif section == "Regjistrohu!":
    st.header("📝 Regjistrohu tani")
    st.markdown("Plotësoni formularin për t'u listuar si Arkitekt ose Klient.")
    st.markdown("[Regjistrohu përmes Formularit të Google](https://forms.gle/74xSDLR7o6kzr1cD6)")



