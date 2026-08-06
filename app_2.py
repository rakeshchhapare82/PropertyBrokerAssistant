import streamlit as st
import urllib.parse

st.set_page_config(page_title="Universal WhatsApp Sender", page_icon="📱", layout="centered")

st.title("📱 Cross-Platform WhatsApp Sender")
st.write("This app works natively on both Laptops (Browsers) and Mobile Phones (Apps).")

# Input section
phone_number = st.text_input("Receiver Phone Number", value="+91", help="Include country code, e.g., +919876543210")
message = st.text_area("Your Message", placeholder="Type your text here...")

if phone_number and message:
    # 1. Strip everything except numbers to ensure the API link doesn't break
    clean_number = "".join(filter(str.isdigit, phone_number))
    
    # 2. Safely encode spaces and special characters for the browser URL
    encoded_message = urllib.parse.quote(message)
    
    # 3. CORRECT LINK: The forward slash (/) is explicitly placed here
    whatsapp_url = f"https://wa.me/{clean_number}?text={encoded_message}"
    
    st.markdown("### 🔗 Launch Link Generated")
    
    # 4. Clean HTML implementation to mimic a native app button UI
    button_html = f"""
        <a href="{whatsapp_url}" target="_blank" style="
            text-decoration: none;
            background-color: #25D366;
            color: white;
            padding: 14px 28px;
            font-weight: bold;
            font-size: 16px;
            border-radius: 8px;
            display: inline-block;
            text-align: center;
            width: 100%;
            box-shadow: 0px 4px 10px rgba(37, 211, 102, 0.3);
            transition: 0.3s;
        ">🟢 Open in WhatsApp & Send</a>
    """
    
    st.markdown(button_html, unsafe_allow_html=True)
    st.caption("ℹ️ Due to platform security restrictions, you just need to tap the native 'Send' arrow inside WhatsApp once the app/tab opens.")
else:
    st.warning("Please input both a valid phone number and message text above.")
