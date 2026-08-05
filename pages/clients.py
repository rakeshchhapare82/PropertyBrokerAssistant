import streamlit as st

from models.client import Client
from services.client_service import ClientService


# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Clients",
    page_icon="👥",
    layout="wide"
)


st.title("👥 Client Management")


# -------------------------------------------------
# Session State
# -------------------------------------------------

if "delete_client_id" not in st.session_state:

    st.session_state.delete_client_id = None


if "client_search" not in st.session_state:

    st.session_state.client_search = ""



# -------------------------------------------------
# Search Client Section
# -------------------------------------------------

st.subheader("🔍 Search Clients")


col1, col2, col3 = st.columns(
    [5,1,1]
)


with col1:

    search_text = st.text_input(
        "Search by Name / Mobile / City",
        value=st.session_state.client_search,
        placeholder="Enter client name, mobile or city"
    )



with col2:

    search_clicked = st.button(
        "🔍 Search",
        use_container_width=True
    )



with col3:

    clear_clicked = st.button(
        "❌ Clear",
        use_container_width=True
    )



# -------------------------------------------------
# Search Action
# -------------------------------------------------

if search_clicked:

    st.session_state.client_search = search_text



if clear_clicked:

    st.session_state.client_search = ""

    st.rerun()



# -------------------------------------------------
# Load Clients
# -------------------------------------------------

if st.session_state.client_search:


    clients = ClientService.search(
        st.session_state.client_search
    )


else:


    clients = ClientService.get_all()



# -------------------------------------------------
# Search Result Count
# -------------------------------------------------

if st.session_state.client_search:


    st.info(
        f"Found {len(clients)} client(s) "
        f"for '{st.session_state.client_search}'"
    )


else:


    st.info(
        f"Total Clients: {len(clients)}"
    )



st.divider()



# -------------------------------------------------
# Add / Edit Mode
# -------------------------------------------------

mode = st.radio(
    "Select Action",
    [
        "Add New Client",
        "Edit Existing Client"
    ],
    horizontal=True
)



client_id = None


# Default values

full_name = ""

mobile = ""

alternate_mobile = ""

email = ""

city = ""

property_type = "Flat"

location_preferred = ""

budget_min = 0.0

budget_max = 0.0

source = "Website"

status = "New"

priority = "Normal"

remarks = ""



# -------------------------------------------------
# Prepare Client Dropdown
# -------------------------------------------------

client_map = {}


if clients:


    client_map = {

        f"{c['full_name']} ({c['mobile']})":

        c

        for c in clients

    }



# -------------------------------------------------
# Edit Mode Selection
# -------------------------------------------------

if mode == "Edit Existing Client":


    if not clients:

        st.warning(
            "No clients available for editing."
        )

        st.stop()



    selected_client = st.selectbox(
        "Select Client",
        list(client_map.keys())
    )


    client_data = client_map[selected_client]


    client_id = client_data["client_id"]


    full_name = client_data.get(
        "full_name",
        ""
    )


    mobile = client_data.get(
        "mobile",
        ""
    )


    alternate_mobile = client_data.get(
        "alternate_mobile",
        ""
    )


    email = client_data.get(
        "email",
        ""
    )


    city = client_data.get(
        "city",
        ""
    )


    # -------------------------------------------------
# Continue Edit Data Loading
# -------------------------------------------------

    property_type = client_data.get(
        "property_type",
        "Flat"
    )


    location_preferred = client_data.get(
        "location_preferred",
        ""
    )


    budget_min = float(
        client_data.get(
            "budget_min",
            0
        )
    )


    budget_max = float(
        client_data.get(
            "budget_max",
            0
        )
    )


    source = client_data.get(
        "source",
        "Website"
    )


    status = client_data.get(
        "status",
        "New"
    )


    priority = client_data.get(
        "priority",
        "Normal"
    )


    remarks = client_data.get(
        "remarks",
        ""
    )



# -------------------------------------------------
# Client Form
# -------------------------------------------------

st.subheader(
    "📝 Client Details"
)


with st.form(
    "client_form"
):


    col1, col2 = st.columns(2)


    with col1:


        full_name = st.text_input(
            "Full Name",
            value=full_name
        )


        mobile = st.text_input(
            "Mobile",
            value=mobile
        )


        alternate_mobile = st.text_input(
            "Alternate Mobile",
            value=alternate_mobile
        )


        email = st.text_input(
            "Email",
            value=email
        )


        city = st.text_input(
            "City",
            value=city
        )



    with col2:


        property_options = [
            "Flat",
            "House",
            "Plot",
            "Commercial"
        ]


        property_type = st.selectbox(
            "Property Type",
            property_options,

            index=
            property_options.index(property_type)
            if property_type in property_options
            else 0
        )


        location_preferred = st.text_input(
            "Preferred Location",
            value=location_preferred
        )


        budget_min = st.number_input(
            "Minimum Budget",
            min_value=0.0,
            value=budget_min
        )


        budget_max = st.number_input(
            "Maximum Budget",
            min_value=0.0,
            value=budget_max
        )


        source_options = [
            "Website",
            "Reference",
            "WhatsApp",
            "Walk-in"
        ]


        source = st.selectbox(
            "Source",
            source_options,

            index=
            source_options.index(source)
            if source in source_options
            else 0
        )



    status_options = [
        "New",
        "Interested",
        "Not Interested",
        "Closed"
    ]


    status = st.selectbox(
        "Status",
        status_options,

        index=
        status_options.index(status)
        if status in status_options
        else 0
    )


    priority_options = [
        "High",
        "Normal",
        "Low"
    ]


    priority = st.selectbox(
        "Priority",
        priority_options,

        index=
        priority_options.index(priority)
        if priority in priority_options
        else 1
    )


    remarks = st.text_area(
        "Remarks",
        value=remarks
    )


    submit = st.form_submit_button(
        "💾 Save Client",
        use_container_width=True
    )



# -------------------------------------------------
# Add / Update Client
# -------------------------------------------------

if submit:


    try:


        client = Client(

            full_name=full_name,

            mobile=mobile,

            alternate_mobile=alternate_mobile,

            email=email,

            city=city,

            property_type=property_type,

            location_preferred=location_preferred,

            budget_min=budget_min,

            budget_max=budget_max,

            source=source,

            status=status,

            priority=priority,

            remarks=remarks

        )


        if mode == "Add New Client":


            ClientService.add(
                client
            )


            st.success(
                "✅ Client added successfully."
            )


        else:


            ClientService.update(
                client_id,
                client
            )


            st.success(
                "✅ Client updated successfully."
            )


        st.rerun()



    except Exception as ex:


        st.error(
            str(ex)
        )



st.divider()



# -------------------------------------------------
# Client List
# -------------------------------------------------

st.subheader(
    "📋 Client List"
)



if clients:


    for client in clients:


        with st.container(
            border=True
        ):


            col1, col2 = st.columns(
                [5,1]
            )



            with col1:


                st.write(
                    f"### 👤 {client['full_name']}"
                )


                st.write(
                    f"📞 Mobile: {client['mobile']}"
                )


                st.write(
                    f"🏙 City: {client.get('city','')}"
                )


                st.write(
                    f"🏠 Property: {client.get('property_type','')}"
                )


                st.write(
                    f"Status: {client.get('status','')}"
                )



            with col2:


                if st.button(
                    "🗑 Delete",
                    key=f"delete_{client['client_id']}"
                ):


                    st.session_state.delete_client_id = (
                        client["client_id"]
                    )



                if (
                    st.session_state.delete_client_id
                    ==
                    client["client_id"]
                ):


                    st.warning(
                        "Confirm delete?"
                    )



                    if st.button(
                        "✅ Yes Delete",
                        key=f"confirm_{client['client_id']}"
                    ):


                        try:


                            ClientService.delete(
                                client["client_id"]
                            )


                            st.session_state.delete_client_id = None


                            st.success(
                                "Client deleted successfully."
                            )


                            st.rerun()



                        except Exception as ex:


                            st.error(
                                str(ex)
                            )



                    if st.button(
                        "❌ Cancel",
                        key=f"cancel_{client['client_id']}"
                    ):


                        st.session_state.delete_client_id = None


                        st.rerun()



else:


    st.info(
        "No clients found."
    )