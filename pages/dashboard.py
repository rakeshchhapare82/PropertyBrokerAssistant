import streamlit as st
import pandas as pd

from services.dashboard_service import DashboardService


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Property Broker CRM Dashboard")

st.divider()

# ---------------------------------------------------------
# Refresh Button
# ---------------------------------------------------------

if st.button("🔄 Refresh Dashboard"):
    st.rerun()

# ---------------------------------------------------------
# Dashboard Summary
# ---------------------------------------------------------

summary = DashboardService.get_dashboard_summary()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Clients",
        summary["total_clients"]
    )

with col2:
    st.metric(
        "❤️ Interested Clients",
        summary["interested_clients"]
    )

with col3:
    st.metric(
        "📅 Today's Follow-ups",
        summary["today_followups"]
    )

with col4:
    st.metric(
        "⏳ Pending Follow-ups",
        summary["pending_followups"]
    )

st.divider()

# ---------------------------------------------------------
# Today's Follow-ups
# ---------------------------------------------------------

st.subheader("📅 Today's Follow-ups")

today_followups = DashboardService.get_today_followups()

if today_followups:

    df_today = pd.DataFrame(today_followups)

    st.dataframe(
        df_today,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No follow-ups scheduled for today.")

st.divider()

# ---------------------------------------------------------
# Pending Follow-ups
# ---------------------------------------------------------

st.subheader("⏳ Pending Follow-ups")

pending_followups = DashboardService.get_pending_followups()

if pending_followups:

    df_pending = pd.DataFrame(pending_followups)

    st.dataframe(
        df_pending,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No pending follow-ups.")

st.divider()

# ---------------------------------------------------------
# Recently Added Clients
# ---------------------------------------------------------

st.subheader("👥 Recently Added Clients")

recent_clients = DashboardService.get_recent_clients()

if recent_clients:

    df_clients = pd.DataFrame(recent_clients)

    st.dataframe(
        df_clients,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No clients available.")

st.divider()

# ---------------------------------------------------------
# Recent Follow-up Activity
# ---------------------------------------------------------

st.subheader("📝 Recent Follow-up Activity")

recent_followups = DashboardService.get_recent_followups()

if recent_followups:

    df_recent = pd.DataFrame(recent_followups)

    st.dataframe(
        df_recent,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No follow-up activity found.")

st.divider()

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.caption(
    "AI Property Broker CRM | Phase 1 Dashboard"
)