import streamlit as st
import requests
import json
import time

# Force wide layout config to maximize the input container fields
st.set_page_config(page_title="Automated WhatsApp Engine", page_icon="🤖", layout="wide")

st.title("🤖 Official Multi-User WhatsApp Broadcast Engine")
st.write("Production-ready pipeline featuring extra-wide text blocks and high-readability logs.")

# --- SIDEBAR SETUPS FOR ACCURATE ID DISCOVERY ---
st.sidebar.header("🔑 User Session Credentials")
ACCESS_TOKEN = st.sidebar.text_input("Your Meta Access Token", type="password", key="user_token")
PHONE_NUMBER_ID = st.sidebar.text_input("Your Phone Number ID (NOT Account ID)", key="user_phone_id")

st.sidebar.markdown("""
---
⚠️ **How to fix 404:**
1. Check your sidebar **Phone Number ID**. Ensure it matches the ID listed right under your test phone dropdown on Meta. 
2. Do **not** use the Business Account ID.
""")

# --- EXPANDED LAYOUT CONFIGURATION FOR TEXT FIELDS ---
st.subheader("¼ Dispatch Details")

col_left, col_right = st.columns(2)

with col_left:
    numbers_input = st.text_area(
        "Receiver Phone Numbers (One per line with Country Code, e.g., 918806797480)",
        placeholder="918806797480\n919876543210",
        height=250,
        key="user_numbers"
    )

with col_right:
    # 2. EXTRA WIDE CONTAINER FOR MULTIMEDIA LABELS
    template_name = st.text_input(
        "Template Name String", 
        value="hello_world", 
        help="Free testing numbers must use pre-approved templates like hello_world."
    )
    st.info("💡 Note: Meta sandbox account blocks custom raw texts until the recipient sends you a text first. Keep 'hello_world' active for testing.")

# --- TRACKING DICTIONARY SETUPS ---
if "dispatched_log" not in st.session_state:
    st.session_state.dispatched_log = []

# --- BACKGROUND AUTOMATION DISPATCHER ---
if st.button("🚀 Run Background Automated Broadcast", use_container_width=True):
    if not ACCESS_TOKEN or not PHONE_NUMBER_ID:
        st.error("Missing Credentials! Please supply your Meta Token and Phone ID in the left sidebar.")
    elif not numbers_input.strip():
        st.warning("Missing Fields! Please input target numbers to begin.")
    else:
        # Reset current run tracking history
        st.session_state.dispatched_log = []
        
        # Clean string rows into array items
        phone_list = [num.strip() for num in numbers_input.split("\n") if num.strip()]
        
        # Absolute correct API endpoint URL path structure
        #url = f"https://facebook.com/{PHONE_NUMBER_ID}/messages"
        
        url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

        #https://graph.facebook.com/v25.0/1239100782623541/messages

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        progress_bar = st.progress(0)
        status_banner = st.empty()
        
        # 1. LOOP PROCESS FOR MULTIPLE USERS
        for index, number in enumerate(phone_list):
            clean_number = "".join(filter(str.isdigit, number))
            status_banner.text(f"Syncing connection pipeline to: {clean_number} ({index + 1}/{len(phone_list)})...")
            
            # Send via structural template rules to prevent sandbox policy blockages
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": clean_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": "en_US"
                    }
                }
            }
            
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                
                if response.status_code == 200:
                    st.session_state.dispatched_log.append({"phone": clean_number, "status": "✅ Sent Successfully"})
                else:
                    # Capture exact internal subcodes if rejected
                    try:
                        err_msg = response.json().get('error', {}).get('message', f'Status {response.status_code}')
                    except:
                        err_msg = f"Status {response.status_code}"
                    st.session_state.dispatched_log.append({"phone": clean_number, "status": f"❌ Rejected ({err_msg})"})
            except Exception as e:
                st.session_state.dispatched_log.append({"phone": clean_number, "status": f"💥 Network Error: {e}"})
                
            progress_bar.progress((index + 1) / len(phone_list))
            time.sleep(0.4) 
            
        status_banner.empty()
        
        # 3. HIGH-READABILITY OUTCOMES WITH CLEAN LOGGING (NO RAW JSON SHOWN)
        st.markdown("---")
        st.success("🏁 Automation Session Complete! Delivery logs outlined below:")
        
        # Clean custom parsed output list logs mapping
        for log_entry in st.session_state.dispatched_log:
            st.markdown(f"**Phone Number:** `+{log_entry['phone']}` &nbsp;|&nbsp; **Delivery Status:** {log_entry['status']}")
