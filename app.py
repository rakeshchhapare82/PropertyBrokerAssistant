import os
from pathlib import Path
import streamlit as st
import requests
import json
import time
import pandas as pd
from dotenv import load_dotenv

from services.client_service import ClientService

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

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
st.sidebar.caption("Using values from .env or your manual entry.")

ACCESS_TOKEN = (
    st.sidebar.text_input(
        "Access Token",
        value=os.getenv("WHATSAPP_ACCESS_TOKEN", "").strip(),
        type="password",
    ) or ""
).strip()

PHONE_NUMBER_ID = (
    st.sidebar.text_input(
        "Phone Number ID",
        value=os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip(),
    ) or ""
).strip()

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



send_mode = st.radio(
    "Send as",
    ["Text Message", "Template Message"],
    horizontal=True,
    index=0,
)

message_text = st.text_area(
    "Message Text",
    value="Hi there! This is a test message from the Property Broker Assistant.",
    height=120,
    help="Use this for normal WhatsApp text messages. Any non-empty message works here."
)

if send_mode == "Text Message":
    st.info(
        "For normal text messages, WhatsApp usually requires the recipient to have messaged your business before or to be within the 24-hour customer service window. Otherwise, use a template message."
    )

template_name = st.text_input(
    "Template Name",
    value="hello_world",
    help="Only needed when using a WhatsApp template message."
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

        st.error("Please enter a valid Access Token from your WhatsApp Business account.")
        st.stop()

    if not PHONE_NUMBER_ID:

        st.error("Please enter your WhatsApp Phone Number ID.")
        st.stop()

    if not PHONE_NUMBER_ID.isdigit():

        st.error("Phone Number ID must contain only digits.")
        st.stop()

    if len(st.session_state.selected_clients) == 0:

        st.warning("Please select at least one client.")
        st.stop()

    if send_mode == "Text Message":

        if not message_text.strip():

            st.warning("Please enter a message to send.")
            st.stop()

    else:

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

        if send_mode == "Text Message":

            payload = {

                "messaging_product": "whatsapp",

                "recipient_type": "individual",

                "to": phone,

                "type": "text",

                "text": {

                    "body": message_text.strip()

                }

            }

        else:

            payload = {

                "messaging_product": "whatsapp",

                "recipient_type": "individual",

                "to": phone,

                "type": "template",

                "template": {

                    "name": template_name.strip(),

                    "language": {

                        "code": "en_US"

                    }

                }

            }

        try:

            response = requests.post(

                url,

                headers=headers,

                json=payload,

                timeout=30

            )

            if response.status_code == 200:

                st.session_state.logs.append(

                    {

                        "Client":

                            client["full_name"],

                        "Phone":

                            phone,

                        "Status":

                            "✅ Accepted by Meta",

                        "Response":

                            "The WhatsApp API accepted the message request. Delivery still depends on recipient opt-in and WhatsApp business rules."

                    }

                )

            else:

                try:

                    error_message = response.json() \
                        .get("error", {}) \
                        .get("message", "")

                except Exception:

                    error_message = response.text.strip() or (
                        f"Status {response.status_code}"
                    )

                if response.status_code in (401, 403):

                    error_message = (
                        f"{error_message} "
                        "(Authentication failed. Check that the access token is valid and that the phone number ID belongs to the same WhatsApp Business account.)"
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
            logs_df["Status"].isin(["✅ Sent", "✅ Accepted by Meta"])
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
            f"All {sent} WhatsApp message requests were accepted by Meta."
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