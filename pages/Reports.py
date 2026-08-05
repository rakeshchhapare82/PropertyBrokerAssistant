import streamlit as st
import pandas as pd

from services.client_service import ClientService
from services.followup_service import FollowupService


# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Reports",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Reports")



# -------------------------------------------------
# Load Data
# -------------------------------------------------

clients = ClientService.get_all()

followups = FollowupService.get_all()



# Convert to DataFrame

client_df = pd.DataFrame(
    clients
)


followup_df = pd.DataFrame(
    followups
)



# -------------------------------------------------
# Report Selection
# -------------------------------------------------

report_type = st.selectbox(

    "Select Report",

    [
        "Client Report",
        "Interested Clients",
        "Follow-up Report",
        "Pending Follow-ups"
    ]

)



st.divider()



# -------------------------------------------------
# Client Report
# -------------------------------------------------

if report_type == "Client Report":


    st.subheader(
        "👥 Client Report"
    )


    if not client_df.empty:


        st.metric(
            "Total Clients",
            len(client_df)
        )


        st.dataframe(

            client_df,

            use_container_width=True,

            hide_index=True

        )


        csv = client_df.to_csv(
            index=False
        )


        st.download_button(

            label="⬇ Download Client Report",

            data=csv,

            file_name="client_report.csv",

            mime="text/csv"

        )


    else:


        st.info(
            "No client data available."
        )



# -------------------------------------------------
# Interested Clients
# -------------------------------------------------

elif report_type == "Interested Clients":


    st.subheader(
        "⭐ Interested Clients"
    )


    if not client_df.empty:


        interested = client_df[
            client_df["status"]
            ==
            "Interested"
        ]


        st.metric(

            "Interested Clients",

            len(interested)

        )


        st.dataframe(

            interested,

            use_container_width=True,

            hide_index=True

        )


        csv = interested.to_csv(
            index=False
        )


        st.download_button(

            "⬇ Download Interested Clients",

            csv,

            "interested_clients.csv",

            "text/csv"

        )


    else:


        st.info(
            "No interested clients."
        )



# -------------------------------------------------
# Follow-up Report
# -------------------------------------------------

elif report_type == "Follow-up Report":


    st.subheader(
        "📅 Follow-up Report"
    )


    if not followup_df.empty:


        st.metric(

            "Total Follow-ups",

            len(followup_df)

        )


        st.dataframe(

            followup_df,

            use_container_width=True,

            hide_index=True

        )


        csv = followup_df.to_csv(
            index=False
        )


        st.download_button(

            "⬇ Download Follow-up Report",

            csv,

            "followup_report.csv",

            "text/csv"

        )


    else:


        st.info(
            "No follow-up data available."
        )



# -------------------------------------------------
# Pending Follow-ups
# -------------------------------------------------

elif report_type == "Pending Follow-ups":


    st.subheader(
        "⏳ Pending Follow-ups"
    )


    pending = (
        FollowupService
        .get_pending_followups()
    )


    pending_df = pd.DataFrame(
        pending
    )



    if not pending_df.empty:


        st.metric(

            "Pending Follow-ups",

            len(pending_df)

        )


        st.dataframe(

            pending_df,

            use_container_width=True,

            hide_index=True

        )


        csv = pending_df.to_csv(
            index=False
        )


        st.download_button(

            "⬇ Download Pending Follow-ups",

            csv,

            "pending_followups.csv",

            "text/csv"

        )


    else:


        st.info(
            "No pending follow-ups."
        )