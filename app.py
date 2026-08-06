import streamlit as st
import requests
import json
import time
import pandas as pd

from services.client_service import ClientService

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Automated WhatsApp Engine",
    page_icon="💬",
    layout="wide"
)

st.title("💬 WhatsApp Broadcast Engine")
st.caption("Broadcast WhatsApp template messages to selected clients.")

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("Meta Credentials")

DEFAULT_ACCESS_TOKEN = "EAAZAjHUZBkRygBSGZByYHGHqQmcWlZALRI4KqV6PLZCODqmvcQnh0GmcIgpbiZBUrHKXdv9C7eXPFN2HB6nwZAXZAqGiPsZCtKlsD3MtM9XyCCLOnbs42ZAPSpkI4v9WOOZAeDUqv1ZA5XOyR3GZB7fAuEESyw5TS0Cqlyf5H4i6xcFaMea6q2bsTmNDdS0KDcBvqwLSXfW6h0GtSpssrevrjcJNibl9Bu5ZA23yIEJHwkt6TZCCfEZBfWvU3DSBA7n1yZBifEODFJ4itRU3RwHhqthVGpAZDZD"
DEFAULT_PHONE_NUMBER_ID = "1239100782623541"

ACCESS_TOKEN = st.sidebar.text_input(
    "Access Token",
    value=DEFAULT_ACCESS_TOKEN,
    type="password"
)

PHONE_NUMBER_ID = st.sidebar.text_input(
    "Phone Number ID",
    value=DEFAULT_PHONE_NUMBER_ID
)

# ==========================================================
# SESSION STATE
# ==========================================================

if "selected_clients" not in st.session_state:
    st.session_state.selected_clients = []

if "logs" not in st.session_state:
    st.session_state.logs = []

# ==========================================================
# LOAD CLIENTS FROM DATABASE
# ==========================================================

clients = ClientService.get_all()

if not clients:

    st.warning("No clients found.")

    st.stop()

df = pd.DataFrame(clients)

# ==========================================================
# SEARCH
# ==========================================================

search = st.text_input(
    "Search Client",
    placeholder="Name or Mobile..."
)

filtered = df.copy()

if search:

    filtered = filtered[
        filtered["full_name"].str.lower().str.contains(
            search.lower(),
            na=False
        )
        |
        filtered["mobile"].astype(str).str.contains(
            search,
            na=False
        )
    ]

# ==========================================================
# SELECT BUTTONS
# ==========================================================

c1,c2,c3 = st.columns([1,1,2])

with c1:

    if st.button("Select All"):

        st.session_state.selected_clients = (
            filtered["client_id"].tolist()
        )

        st.rerun()

with c2:

    if st.button("Clear All"):

        st.session_state.selected_clients = []

        st.rerun()

with c3:

    st.success(
        f"Selected : {len(st.session_state.selected_clients)}"
    )

#st.divider()
# ==========================================================
# RECIPIENTS TABLE
# ==========================================================
col1, col2 = st.columns([4,1])

with col1:
    st.subheader("👥 Recipients")

with col2:
    st.markdown(
        f"""
<div style="text-align:right;
            font-size:15px;
            font-weight:bold;
            margin-top:12px;">
Selected Clients :
<span style="color:green;">
{len(st.session_state.selected_clients)}
</span>
</div>
""",
        unsafe_allow_html=True
    )

# Create display dataframe
display_df = filtered[
    ["client_id", "full_name", "mobile"]
].copy()

display_df.rename(
    columns={
        "full_name": "Client Name",
        "mobile": "Mobile Number"
    },
    inplace=True
)

# Add checkbox column
display_df.insert(
    0,
    "Select",
    display_df["client_id"].isin(
        st.session_state.selected_clients
    )
)

# Dynamic table height
row_height = 35
header_height = 40

table_height = min(
    550,
    max(
        150,
        (len(display_df) * row_height) + header_height
    )
)

# Editable table
edited_df = st.data_editor(

    display_df,

    hide_index=True,

    use_container_width=True,

    height=table_height,

    column_config={

        "Select": st.column_config.CheckboxColumn(
            "✓"
        ),

        "client_id": None,

        "Client Name": st.column_config.TextColumn(
            "Client Name",
            width="medium"
        ),

        "Mobile Number": st.column_config.TextColumn(
            "Mobile Number",
            width="medium"
        )

    },

    disabled=[
        "Client Name",
        "Mobile Number"
    ]
)

# Update selected clients
st.session_state.selected_clients = edited_df.loc[
    edited_df["Select"] == True,
    "client_id"
].tolist()



template_name = st.text_area(
    "Template Name",
    value="hello_world",
    height=120
)

send_clicked = st.button(
    "🚀 Broadcast",
    use_container_width=True
)

# ==========================================================
# SEND BROADCAST
# ==========================================================

if send_clicked:

    # -----------------------------
    # Validation
    # -----------------------------

    if not ACCESS_TOKEN:

        st.error("Please enter Access Token.")
        st.stop()

    if not PHONE_NUMBER_ID:

        st.error("Please enter Phone Number ID.")
        st.stop()

    if len(st.session_state.selected_clients) == 0:

        st.warning("Please select at least one client.")
        st.stop()

    if not template_name.strip():

        st.warning("Please enter Template Name.")
        st.stop()

    # -----------------------------
    # Selected Clients
    # -----------------------------

    selected_df = df[
        df["client_id"].isin(
            st.session_state.selected_clients
        )
    ]

    if selected_df.empty:

        st.warning("No clients selected.")

        st.stop()

    selected_clients = selected_df.to_dict(
        "records"
    )

    total_clients = len(selected_clients)

    st.session_state.logs = []

    progress = st.progress(0)

    current_status = st.empty()

    # -----------------------------
    # API URL
    # -----------------------------

    url = (
        f"https://graph.facebook.com/"
        f"v25.0/{PHONE_NUMBER_ID}/messages"
    )

    headers = {

        "Authorization":

            f"Bearer {ACCESS_TOKEN}",

        "Content-Type":

            "application/json"

    }

    # -----------------------------
    # Sending Loop
    # -----------------------------

    for index, client in enumerate(
        selected_clients,
        start=1
    ):

        phone = (
            str(client["mobile"])
            .replace("+", "")
            .replace(" ", "")
            .replace("-", "")
        )

        if not phone.startswith("91"):

            phone = "91" + phone

        current_status.info(

            f"""
Sending {index} of {total_clients}

👤 {client['full_name']}

📞 {phone}
"""

        )

        payload = {

            "messaging_product": "whatsapp",

            "recipient_type": "individual",

            "to": phone,

            "type": "template",

            "template": {

                "name": template_name,

                "language": {

                    "code": "en_US"

                }

            }

        }

        try:

            response = requests.post(

                url,

                headers=headers,

                data=json.dumps(payload)

            )

            if response.status_code == 200:

                st.session_state.logs.append(

                    {

                        "Client":

                            client["full_name"],

                        "Phone":

                            phone,

                        "Status":

                            "✅ Sent",

                        "Response":

                            "Success"

                    }

                )

            else:

                try:

                    error_message = response.json() \
                        .get("error", {}) \
                        .get("message")

                except Exception:

                    error_message = (
                        f"Status {response.status_code}"
                    )

                st.session_state.logs.append(

                    {

                        "Client":

                            client["full_name"],

                        "Phone":

                            phone,

                        "Status":

                            "❌ Failed",

                        "Response":

                            error_message

                    }

                )

        except Exception as ex:

            st.session_state.logs.append(

                {

                    "Client":

                        client["full_name"],

                    "Phone":

                        phone,

                    "Status":

                        "💥 Error",

                    "Response":

                        str(ex)

                }

            )

        progress.progress(
            index / total_clients
        )

        time.sleep(0.40)

    current_status.empty()

    # ==========================================================
# DELIVERY SUMMARY
# ==========================================================

logs_df = pd.DataFrame(st.session_state.logs)

if not logs_df.empty:

    total = len(logs_df)

    sent = len(
        logs_df[
            logs_df["Status"] == "✅ Sent"
        ]
    )

    failed = total - sent

    st.subheader("📋 Delivery Logs")

    st.dataframe(
        logs_df,
        use_container_width=True,
        hide_index=True
    )

    csv = logs_df.to_csv(index=False).encode("utf-8")

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "📥 Download Delivery Report",
            data=csv,
            file_name="whatsapp_delivery_report.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:

        if st.button(
            "🔄 Reset Campaign",
            use_container_width=True
        ):

            st.session_state.logs = []
            st.session_state.selected_clients = []

            st.success(
                "Campaign has been reset."
            )

            st.rerun()

    st.divider()

    if failed == 0:

        st.success(
            f"🎉 Broadcast completed successfully.\n\n"
            f"All {sent} WhatsApp template messages "
            f"were processed successfully."
        )

    elif sent == 0:

        st.error(
            "No messages were sent successfully."
        )

    else:

        st.warning(
            f"Broadcast completed.\n\n"
            f"{sent} sent successfully and "
            f"{failed} failed."
        )

else:

    st.info(
        "Delivery logs will appear here after broadcasting."
    )