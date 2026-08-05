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

    st.metric(
        "Total Follow-ups",
        FollowupService.total_followups()
    )



with col2:

    st.metric(
        "Pending",
        FollowupService.total_pending_followups()
    )



with col3:

    st.metric(
        "Today's Follow-ups",
        FollowupService.total_today_followups()
    )



st.divider()



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



st.divider()



# -------------------------------------------------
# Today's Follow-ups
# -------------------------------------------------

st.subheader(
    "📅 Today's Follow-ups"
)


today_items = FollowupService.get_today_followups()



if today_items:


    st.dataframe(

        pd.DataFrame(today_items),

        use_container_width=True,

        hide_index=True

    )


else:


    st.info(

        "No follow-ups today."

    )



st.divider()



# -------------------------------------------------
# Pending Follow-ups
# -------------------------------------------------

st.subheader(
    "⏳ Pending Follow-ups"
)



pending = FollowupService.get_pending_followups()



if pending:


    for item in pending:


        with st.container(border=True):


            col1, col2 = st.columns(
                [5,1]
            )



            with col1:


                st.write(

                    f"### {item['full_name']}"

                )


                st.write(

                    f"📞 {item['mobile']}"

                )


                st.write(

                    f"📅 {item['followup_date']}"

                )


                st.write(

                    f"Type: {item['followup_type']}"

                )


                st.write(

                    item["discussion_notes"]

                )



            with col2:


                if st.button(

                    "✅ Complete",

                    key=f"complete_{item['followup_id']}"

                ):


                    FollowupService.mark_completed(

                        item["followup_id"]

                    )


                    st.rerun()



                if st.button(

                    "🗑 Delete",

                    key=f"delete_{item['followup_id']}"

                ):


                    st.session_state.delete_followup_id = (

                        item["followup_id"]

                    )



                if st.session_state.delete_followup_id == item["followup_id"]:


                    st.warning(

                        "Confirm?"

                    )


                    if st.button(

                        "Yes Delete",

                        key=f"yes_{item['followup_id']}"

                    ):


                        FollowupService.delete(

                            item["followup_id"]

                        )


                        st.session_state.delete_followup_id = None


                        st.rerun()



                    if st.button(

                        "Cancel",

                        key=f"cancel_{item['followup_id']}"

                    ):


                        st.session_state.delete_followup_id = None


                        st.rerun()



st.divider()



# -------------------------------------------------
# All Follow-ups
# -------------------------------------------------

st.subheader(
    "📋 All Follow-ups"
)


all_followups = FollowupService.get_all()



if all_followups:


    st.dataframe(

        pd.DataFrame(all_followups),

        use_container_width=True,

        hide_index=True

    )

else:


    st.info(

        "No follow-ups found."

    )