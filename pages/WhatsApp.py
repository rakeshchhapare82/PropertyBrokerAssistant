import streamlit as st
import pandas as pd

from services.client_service import ClientService
from services.whatsapp_service import WhatsAppService


# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="WhatsApp Campaign",
    page_icon="💬",
    layout="wide"
)

st.title("💬 WhatsApp Campaign Manager")

st.caption(
    "Select one or more clients and generate personalized WhatsApp messages."
)

st.divider()


# ----------------------------------------------------
# Session State
# ----------------------------------------------------

if "selected_clients" not in st.session_state:
    st.session_state.selected_clients = []

if "search_text" not in st.session_state:
    st.session_state.search_text = ""

if "city_filter" not in st.session_state:
    st.session_state.city_filter = "All"

if "status_filter" not in st.session_state:
    st.session_state.status_filter = "All"

if "property_filter" not in st.session_state:
    st.session_state.property_filter = "All"


# ----------------------------------------------------
# Load Clients
# ----------------------------------------------------

clients = ClientService.get_all()

if not clients:
    st.warning("No clients available.")
    st.stop()

client_df = pd.DataFrame(clients)


# ----------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------

st.sidebar.header("🔍 Search & Filters")

search_text = st.sidebar.text_input(
    "Search",
    placeholder="Name / Mobile",
    value=st.session_state.search_text
)

cities = ["All"] + sorted(
    client_df["city"].dropna().unique().tolist()
)

statuses = ["All"] + sorted(
    client_df["status"].dropna().unique().tolist()
)

property_types = ["All"] + sorted(
    client_df["property_type"].dropna().unique().tolist()
)

city = st.sidebar.selectbox(
    "City",
    cities
)

status = st.sidebar.selectbox(
    "Status",
    statuses
)

property_type = st.sidebar.selectbox(
    "Property Type",
    property_types
)


# ----------------------------------------------------
# Apply Filters
# ----------------------------------------------------

filtered = client_df.copy()

if search_text:

    search = search_text.lower()

    filtered = filtered[
        filtered["full_name"].str.lower().str.contains(search)
        |
        filtered["mobile"].astype(str).str.contains(search)
    ]

if city != "All":
    filtered = filtered[
        filtered["city"] == city
    ]

if status != "All":
    filtered = filtered[
        filtered["status"] == status
    ]

if property_type != "All":
    filtered = filtered[
        filtered["property_type"] == property_type
    ]


# ----------------------------------------------------
# Header
# ----------------------------------------------------

col1, col2, col3 = st.columns([2,1,1])

with col1:
    st.subheader("👥 Client Selection")

with col2:
    if st.button("✅ Select All"):

        st.session_state.selected_clients = (
            filtered["client_id"].tolist()
        )

        st.rerun()

with col3:
    if st.button("❌ Clear All"):

        st.session_state.selected_clients = []

        st.rerun()


st.write(
    f"Showing **{len(filtered)}** clients"
)

st.divider()


# ----------------------------------------------------
# Client List
# ----------------------------------------------------

for _, client in filtered.iterrows():

    selected = (
        client["client_id"]
        in
        st.session_state.selected_clients
    )

    with st.container(border=True):

        c1, c2 = st.columns([1,8])

        with c1:

            checked = st.checkbox(
                "",
                value=selected,
                key=f"chk_{client['client_id']}"
            )

        with c2:

            st.markdown(
                f"### {client['full_name']}"
            )

            colA, colB, colC = st.columns(3)

            with colA:
                st.write(f"📞 {client['mobile']}")

            with colB:
                st.write(f"🏙 {client['city']}")

            with colC:
                st.write(
                    f"🏠 {client['property_type']}"
                )

            st.caption(
                f"Status : {client['status']}"
            )

        if checked:

            if client["client_id"] not in st.session_state.selected_clients:

                st.session_state.selected_clients.append(
                    client["client_id"]
                )

        else:

            if client["client_id"] in st.session_state.selected_clients:

                st.session_state.selected_clients.remove(
                    client["client_id"]
                )


st.divider()


# ----------------------------------------------------
# Selected Count
# ----------------------------------------------------

st.success(
    f"Selected Clients : {len(st.session_state.selected_clients)}"
)

# ----------------------------------------------------
# Campaign Details
# ----------------------------------------------------

st.header("📝 WhatsApp Campaign")

campaign_name = st.text_input(
    "Campaign Name",
    placeholder="Example: New Property Launch - Vijay Nagar"
)

default_message = """Hello {ClientName},

I hope you are doing well.

I found a property matching your requirement.

📍 Location : {PreferredLocation}

🏠 Property Type : {PropertyType}

💰 Budget :
{BudgetMin} - {BudgetMax}

Please let me know if you would like to schedule a site visit.

Regards,
Rakesh
"""

message_template = st.text_area(
    "Message Template",
    value=default_message,
    height=250
)

st.divider()


# ----------------------------------------------------
# Placeholders
# ----------------------------------------------------

left, right = st.columns([1, 2])

with left:

    st.subheader("📌 Available Placeholders")

    placeholders = WhatsAppService.available_placeholders()

    for item in placeholders:
        st.code(item)


with right:

    st.info(
        """
Use these placeholders anywhere in the message.

Example:

Hello {ClientName}

Budget : {BudgetMax}

Location : {PreferredLocation}
"""
    )


st.divider()


# ----------------------------------------------------
# Preview Client
# ----------------------------------------------------

st.subheader("👀 Message Preview")

selected_clients = client_df[
    client_df["client_id"].isin(
        st.session_state.selected_clients
    )
]

if selected_clients.empty:

    st.warning(
        "Select at least one client to preview the message."
    )

else:

    preview_client_name = st.selectbox(

        "Preview For",

        selected_clients["full_name"].tolist()

    )

    preview_client = selected_clients[
        selected_clients["full_name"]
        ==
        preview_client_name
    ].iloc[0].to_dict()

    preview_message = WhatsAppService.preview(
        message_template,
        preview_client
    )

    st.text_area(
        "Preview",
        value=preview_message,
        height=300,
        disabled=True
    )


st.divider()


# ----------------------------------------------------
# Campaign Summary
# ----------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Selected Clients",
        len(st.session_state.selected_clients)
    )

with col2:

    st.metric(
        "Available Clients",
        len(client_df)
    )


st.success(
    f"Ready to generate personalized WhatsApp messages for "
    f"{len(st.session_state.selected_clients)} client(s)."
)