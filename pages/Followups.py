import streamlit as st
import pandas as pd
from datetime import date
from models.followup import Followup
from services.followup_service import FollowupService
from services.client_service import ClientService



# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Follow-ups",
    page_icon="📅",
    layout="wide"
)

st.title("📅 Follow-up Management")
# -------------------------------------------------
# Session State
# -------------------------------------------------

if "delete_followup_id" not in st.session_state:

    st.session_state.delete_followup_id = None

# -------------------------------------------------
# Dashboard Cards
# -------------------------------------------------

col1, col2, col3 = st.columns(3)
with col1:

    total = FollowupService.total_followups()

    st.markdown(
        f"""
        <div style="
            font-size:18px;
            font-weight:600;
            padding-top:8px;
        ">
            📅 Total Follow-ups:
            <span style="color:#1f77b4;">
                {total}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    pending = FollowupService.total_pending_followups()

    st.markdown(
        f"""
<div style="
    font-size:16px;
    font-weight:bold;
    padding-top:8px;
">
⏳ Pending:
<span style="color:orange;">
{pending}
</span>
</div>
""",
        unsafe_allow_html=True
    )

with col3:

    today = FollowupService.total_today_followups()

    st.markdown(
        f"""
<div style="
    font-size:16px;
    font-weight:bold;
    padding-top:8px;
">
📅 Today's Follow-ups:
<span style="color:green;">
{today}
</span>
</div>
""",
        unsafe_allow_html=True
    )    


# -------------------------------------------------
# Total Follow-ups
# -------------------------------------------------

st.subheader("📋 Total Follow-ups")

all_followups = FollowupService.get_all()

if all_followups:

    # Create DataFrame
    display_df = pd.DataFrame(all_followups)

    # Keep followup_id internally for delete operation
    display_df = display_df[
        [
            "followup_id",
            "full_name",
            "mobile",
            "discussion_notes",
            "followup_date",
            "status",
            "followup_type",
        ]
    ].copy()

    # Add checkbox column
    display_df.insert(0, "Select", False)

    # Rename columns
    display_df.rename(
        columns={
            "full_name": "Client Name",
            "mobile": "Phone",
            "discussion_notes": "Discussion",
            "followup_date": "Date",
            "status": "Status",
            "followup_type": "Type",
        },
        inplace=True,
    )

    # Editable table
    edited_df = st.data_editor(
        display_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "followup_id": None,  # Hide ID column
            "Select": st.column_config.CheckboxColumn(
                "✓",
                help="Select Follow-up(s)"
            ),
            "Discussion": st.column_config.TextColumn(
                "Discussion",
                width="large",
            ),
        },
        disabled=[
            "followup_id",
            "Client Name",
            "Phone",
            "Discussion",
            "Date",
            "Status",
            "Type",
        ],
    )

    # Selected rows
    selected_rows = edited_df[edited_df["Select"]]

    if not selected_rows.empty:

        st.warning(
            f"⚠️ {len(selected_rows)} follow-up(s) selected."
        )

        col1, col2 = st.columns([1, 4])

        with col1:
            if st.button(
                "🗑 Delete Selected",
                type="primary",
                use_container_width=True,
            ):

                for followup_id in selected_rows["followup_id"]:
                    FollowupService.delete(int(followup_id))

                st.success("Selected follow-up(s) deleted successfully.")

                st.rerun()

else:
    st.info("No follow-ups found.")


# -------------------------------------------------
# Mode Selection
# -------------------------------------------------

mode = st.radio(

    "Select Action",

    [
        "Add New Follow-up",
        "Edit Follow-up"
    ],

    horizontal=True
)

followup_id = None

# -------------------------------------------------
# Load Clients
# -------------------------------------------------
clients = ClientService.get_all()
if not clients:

    st.warning(
        "Please add clients first."
    )

    st.stop()

client_map = {

    f"{c['full_name']} ({c['mobile']})":
    c["client_id"]
    for c in clients
}


# Default Values
selected_client = list(client_map.keys())[0]
followup_date = date.today()
followup_time = None
followup_type = "Phone Call"
discussion_notes = ""
next_followup_date = date.today()
reminder = True
status = "Pending"

# -------------------------------------------------
# Edit Existing Follow-up
# -------------------------------------------------

if mode == "Edit Follow-up":
    followups = FollowupService.get_all()

    if not followups:
        st.warning(
            "No follow-ups available."
        )

        st.stop()

    followup_map = {
        f"{f['full_name']} - {f['followup_date']}":
        f
        for f in followups
    }

    selected_followup = st.selectbox(
        "Select Follow-up",
        list(followup_map.keys())
    )

    data = followup_map[selected_followup]
    followup_id = data["followup_id"]

    # Existing values
    for key, value in client_map.items():
        if value == data["client_id"]:
            selected_client = key

    followup_date = data["followup_date"]
    followup_time = data["followup_time"]
    followup_type = data["followup_type"]
    discussion_notes = data["discussion_notes"]
    next_followup_date = data["next_followup_date"]
    reminder = data["reminder"]
    status = data["status"]

# -------------------------------------------------
# Follow-up Form
# -------------------------------------------------

st.subheader(
    "📝 Follow-up Details"
)

with st.form(
    "followup_form"
):

    col1, col2 = st.columns(2)
    with col1:
        selected_client = st.selectbox(
            "Client",
            list(client_map.keys()),
            index=list(client_map.keys()).index(
                selected_client
            )
        )

        followup_date = st.date_input(
            "Follow-up Date",
            value=followup_date
        )

        followup_type = st.selectbox(
            "Follow-up Type",
            [
                "Phone Call",
                "Meeting",
                "WhatsApp",
                "Email"
            ],

            index=[
                "Phone Call",
                "Meeting",
                "WhatsApp",
                "Email"
            ].index(followup_type)
        )

        reminder = st.checkbox(
            "Reminder",
            value=reminder
        )

    with col2:
        followup_time = st.time_input(
            "Follow-up Time",
            value=followup_time
        )

        next_followup_date = st.date_input(
            "Next Follow-up Date",
            value=next_followup_date
        )

        status = st.selectbox(
            "Status",
            [
                "Pending",
                "Completed",
                "Cancelled"
            ],

            index=[
                "Pending",
                "Completed",
                "Cancelled"
            ].index(status)
        )

    discussion_notes = st.text_area(
        "Discussion Notes",
        value=discussion_notes
    )

    save = st.form_submit_button(
        "💾 Save Follow-up",
        use_container_width=True
    )

# -------------------------------------------------
# Save / Update
# -------------------------------------------------
if save:
    try:
        followup = Followup(
            client_id =
            client_map[selected_client],
            followup_date =
            followup_date,
            followup_time =
            followup_time,
            followup_type =
            followup_type,
            discussion_notes =
            discussion_notes,
            next_followup_date =
            next_followup_date,
            reminder =
            reminder,
            status =
            status
        )

        if mode == "Add New Follow-up":
            FollowupService.add(
                followup
            )
            st.success(
                "Follow-up added successfully."
            )
        else:
            FollowupService.update(
                followup_id,
                followup
            )
            st.success(
                "Follow-up updated successfully."
            )
        st.rerun()

    except Exception as ex:
        st.error(
            str(ex)
        )
