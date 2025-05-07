# Streamlit app for Structura
import streamlit as st
import datetime

st.set_page_config(page_title="Structura App", layout="wide")
st.title("🏗️ Structura – Architecture Project Management")

st.sidebar.header("📋 Menu")
section = st.sidebar.radio("Go to:", [
    "Calendar", "Tariff Calculator", "Manual & Resources", "Client-Architect Match", "Register Now"])

# 1. Calendar Interface
if section == "Calendar":
    st.header("📅 Work Calendar")
    st.markdown("Add your events and view upcoming project deadlines.")
    event_date = st.date_input("Select Date")
    event_desc = st.text_input("Event Description")
    if st.button("Add Event"):
        st.success(f"Added event on {event_date}: {event_desc}")
    st.markdown("**Example Events:**")
    st.write("- 2025-05-12: Site Visit")
    st.write("- 2025-06-01: Draft Submission")

# 2. Tariff Calculator
elif section == "Tariff Calculator":
    st.header("💰 Tariff & Earnings Calculator")
    area = st.number_input("Area of the project (m²):", min_value=0.0)
    rate = st.number_input("Tariff per m² (€):", min_value=0.0)
    if st.button("Calculate Earnings"):
        earnings = area * rate
        st.success(f"Estimated Earnings: €{earnings:.2f}")

# 3. Manual & Resources
elif section == "Manual & Resources":
    st.header("📘 Project Manual & Resources")
    st.markdown("### Useful Links:")
    st.markdown("- [Architecture Forum](https://www.archinect.com/forum)")
    st.markdown("- [Design Inspiration](https://www.archdaily.com)")
    st.markdown("### Project PDFs:")
    st.write("[Download Project Brief](https://example.com/brief.pdf)")
    st.write("[Structural Guidelines](https://example.com/guidelines.pdf)")

# 4. Client-Architect Match (Gale-Shapley)
elif section == "Client-Architect Match":
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
elif section == "Register Now":
    st.header("📝 Register Now")
    st.markdown("Fill the form to be listed as an Architect or Client.")
    st.markdown("[Register via Google Form](https://forms.gle/your-form-link)")
    st.markdown("### Registered Users:")
    st.write("- Client A")
    st.write("- Architect X")
    st.caption("(Connect your Google Sheet via API or manually update list)")
