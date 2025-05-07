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

st.header("📅 Work Calendar")
st.markdown("Add your events and view upcoming project deadlines.")

# Form for adding or editing events
with st.form(key="event_form"):
    if st.session_state["edit_index"] is None:
        start_date = st.date_input("Start Date (DD/MM/YYYY)", datetime.date.today())
        end_date = st.date_input("End Date (DD/MM/YYYY)", datetime.date.today())
        desc = st.text_input("Event Description")
        submit = st.form_submit_button("Add Event")
    else:
        event = st.session_state["events"][st.session_state["edit_index"]]
        start_date = st.date_input("Start Date (DD/MM/YYYY)", datetime.datetime.strptime(event["start"], "%Y-%m-%d").date())
        end_date = st.date_input("End Date (DD/MM/YYYY)", datetime.datetime.strptime(event["end"], "%Y-%m-%d").date())
        desc = st.text_input("Event Description", event["desc"])
        submit = st.form_submit_button("Update Event")

    if submit:
        if start_date > end_date:
            st.error("Start date must be before end date.")
        elif not desc:
            st.warning("Please provide a description.")
        else:
            new_event = {
                "start": str(start_date),
                "end": str(end_date),
                "desc": desc
            }
            if st.session_state["edit_index"] is None:
                st.session_state["events"].append(new_event)
                st.success("Event added!")
            else:
                st.session_state["events"][st.session_state["edit_index"]] = new_event
                st.success("Event updated!")
                st.session_state["edit_index"] = None

# Display events
st.markdown("### Saved Events:")
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
            st.success("Event deleted!")
            st.experimental_rerun()


# 2. Llogaritësi i tarifave
if section == "Llogaritësi i tarifave":
    st.header("💰 Llogarit Pagesën")
    st.markdown("Vendos të dhënat për të llogaritur pagesën e arkitektit.")

    vështirësia = st.selectbox("Zgjidhni vështirësinë e punës:", ["lehtë", "mesatarë", "e vështirë"])
    madhesia_e_apartamentit = st.number_input("Vendosni madhësinë e apartamentit (në m²):", min_value=1)
    projekti = st.selectbox("Zgjidhni projektin:", ["projekt i ri", "dizajn interieri"])

    if st.button("Llogarit"):
        tarifa_per_m2 = 500

        if vështirësia == "lehtë":
            shumezues_vështirësie = 2
        elif vështirësia == "mesatarë":
            shumezues_vështirësie = 3
        elif vështirësia == "e vështirë":
            shumezues_vështirësie = 4

        if projekti == "projekt i ri":
            shumezues_projekti = 2
        elif projekti == "dizajn interieri":
            shumezues_projekti = 1

        pagesa = (madhesia_e_apartamentit * tarifa_per_m2) * shumezues_vështirësie * shumezues_projekti
        pagesa_me_takse = pagesa * (1 - 0.15)

        st.success(f"📊 Pagesa totale që përfitoni është: **{int(pagesa_me_takse):,} lekë**")

# 3. Manual & Resources
elif section == "Mjete arkitekture":
    st.header("📘 Project Manual & Resources")
    st.markdown("### Useful Links:")
    st.markdown("- [Architecture Forum](https://www.archinect.com/forum)")
    st.markdown("- [Design Inspiration](https://www.archdaily.com)")
    st.markdown("### Project PDFs:")
    st.write("[Download Project Brief](https://example.com/brief.pdf)")
    st.write("[Structural Guidelines](https://example.com/guidelines.pdf)")

# 4. Client-Architect Match (Gale-Shapley)
elif section == "Klientë dhe arkitektë":
    st.header("🔗 Client-Architect Matching Example")

    clients = {
        "Client A": ["Architect X", "Architect Y", "Architect Z"],
        "Client B": ["Architect Y", "Architect X", "Architect Z"],
        "Client C": ["Architect X", "Architect Z", "Architect Y"]
    }

    architects = {
        "Architect X": ["Client B", "Client A", "Client C"],
        "Architect Y": ["Client A", "Client C", "Client B"],
        "Architect Z": ["Client C", "Client B", "Client A"]
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

    if st.button("Show Matches"):
        matches = stable_matching(clients, architects)
        for architect, client in matches.items():
            st.write(f"{architect} ↔ {client}")

# 5. Register Now
elif section == "Regjistrohu!":
    st.header("📝 Register Now")
    st.markdown("Fill the form to be listed as an Architect or Client.")
    st.markdown("[Register via Google Form](https://forms.gle/your-form-link)")
    st.markdown("### Registered Users:")
    st.write("- Client A")
    st.write("- Architect X")
    st.caption("(Connect your Google Sheet via API or manually update list)")

