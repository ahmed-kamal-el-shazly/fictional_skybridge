import streamlit as st
from dotenv import load_dotenv
import os
import base64

# Load env variables before importing modules
load_dotenv()

from corpbot import chat_with_corpbot, COMPANY_DATA
from defense import is_blocked

# Set page config for a cleaner, professional look
st.set_page_config(page_title="SkyBridge Airlines | Fly Beyond Boundaries", layout="wide", page_icon="✈️")


# --- Helper: Load image as base64 for use in custom HTML ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""


# Load all images as base64
HERO_IMG = get_base64_image("assets/hero_airplane.png")
STAFF_IMG = get_base64_image("assets/experienced_staff.png")
FLEET_IMG = get_base64_image("assets/modern_fleet.png")
DEST_IMG = get_base64_image("assets/destinations.png")
CABIN_IMG = get_base64_image("assets/business_class.png")
LOGO_IMG = get_base64_image("assets/skybridge_logo.png")


# --- Master CSS ---
st.markdown("""
<style>
    /* === GLOBAL RESETS === */
    .stApp > header { display: none; }
    .block-container { padding-top: 0 !important; max-width: 100% !important; padding-left: 0 !important; padding-right: 0 !important; }

    /* === TAB NAV BAR === */
    .stTabs [data-baseweb="tab-list"] {
        background: #0b2545;
        padding: 0 40px;
        gap: 0;
        border-bottom: none;
        justify-content: flex-end;
    }
    .stTabs [data-baseweb="tab"] {
        height: 52px;
        color: rgba(255,255,255,0.85) !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 0;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        padding: 0 22px;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff !important;
        background: rgba(255,255,255,0.08) !important;
    }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 3px solid #1abc9c !important;
        background: rgba(255,255,255,0.05) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* === NAVBAR === */
    .sb-navbar {
        background: #0b2545;
        padding: 14px 50px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .sb-navbar-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .sb-navbar-brand img {
        height: 44px;
        border-radius: 6px;
    }
    .sb-navbar-brand-text {
        color: white;
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 1.5px;
    }
    .sb-navbar-brand-sub {
        color: rgba(255,255,255,0.6);
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .sb-nav-links {
        display: flex;
        gap: 30px;
    }
    .sb-nav-links a {
        color: rgba(255,255,255,0.8);
        text-decoration: none;
        font-size: 13px;
        font-weight: 500;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        transition: color 0.3s;
        padding-bottom: 2px;
        border-bottom: 2px solid transparent;
    }
    .sb-nav-links a:hover {
        color: #1abc9c;
        border-bottom: 2px solid #1abc9c;
    }

    /* === HERO SECTION === */
    .sb-hero {
        position: relative;
        width: 100%;
        min-height: 520px;
        background-size: cover;
        background-position: center 40%;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }
    .sb-hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(11,37,69,0.82) 0%, rgba(13,49,92,0.55) 50%, rgba(29,78,137,0.3) 100%);
    }
    .sb-hero-content {
        position: relative;
        z-index: 2;
        padding: 60px 60px;
        max-width: 680px;
    }
    .sb-hero-content h1 {
        font-size: 48px;
        font-weight: 800;
        color: white;
        line-height: 1.15;
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .sb-hero-content p {
        color: rgba(255,255,255,0.85);
        font-size: 16px;
        line-height: 1.7;
        margin-bottom: 28px;
        letter-spacing: 0.5px;
    }
    .sb-hero-cta {
        display: inline-block;
        background: #1abc9c;
        color: white !important;
        padding: 14px 38px;
        border-radius: 4px;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        text-decoration: none;
        transition: all 0.3s ease;
        border: 2px solid #1abc9c;
    }
    .sb-hero-cta:hover {
        background: transparent;
        color: #1abc9c !important;
    }

    /* === SECTION HEADINGS === */
    .sb-section {
        padding: 60px 50px;
        text-align: center;
    }
    .sb-section-dark {
        background: #f8fafb;
    }
    .sb-section h2 {
        font-size: 32px;
        font-weight: 700;
        color: #0b2545;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }
    .sb-section .sb-subtitle {
        color: #6b7c93;
        font-size: 15px;
        max-width: 650px;
        margin: 0 auto 40px;
        line-height: 1.6;
    }

    /* === FEATURE CARDS === */
    .sb-features {
        display: flex;
        gap: 28px;
        justify-content: center;
        flex-wrap: wrap;
    }
    .sb-feature-card {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07);
        max-width: 340px;
        flex: 1;
        min-width: 280px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .sb-feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.12);
    }
    .sb-feature-card img {
        width: 100%;
        height: 210px;
        object-fit: cover;
    }
    .sb-feature-card-body {
        padding: 22px 24px 26px;
    }
    .sb-feature-card-body h3 {
        font-size: 18px;
        font-weight: 700;
        color: #0b2545;
        margin-bottom: 8px;
    }
    .sb-feature-card-body p {
        font-size: 13.5px;
        color: #6b7c93;
        line-height: 1.65;
        margin-bottom: 14px;
    }
    .sb-readmore {
        color: #1abc9c;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-decoration: none;
        border-bottom: 2px solid transparent;
        transition: border-color 0.3s;
    }
    .sb-readmore:hover {
        border-bottom: 2px solid #1abc9c;
    }

    /* === STATS BAR === */
    .sb-stats {
        background: linear-gradient(135deg, #0b2545 0%, #13315c 100%);
        padding: 50px 50px;
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 20px;
    }
    .sb-stat-item {
        text-align: center;
        min-width: 150px;
    }
    .sb-stat-number {
        font-size: 42px;
        font-weight: 800;
        color: #1abc9c;
        margin-bottom: 4px;
    }
    .sb-stat-label {
        color: rgba(255,255,255,0.75);
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* === EXPERIENCE SECTION === */
    .sb-experience {
        display: flex;
        align-items: center;
        gap: 50px;
        padding: 60px 50px;
        flex-wrap: wrap;
    }
    .sb-experience-img {
        flex: 1;
        min-width: 300px;
    }
    .sb-experience-img img {
        width: 100%;
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    .sb-experience-text {
        flex: 1;
        min-width: 300px;
    }
    .sb-experience-text h2 {
        font-size: 30px;
        font-weight: 700;
        color: #0b2545;
        margin-bottom: 16px;
        text-align: left;
    }
    .sb-experience-text p {
        color: #6b7c93;
        font-size: 14.5px;
        line-height: 1.7;
        margin-bottom: 20px;
    }
    .sb-experience-list {
        list-style: none;
        padding: 0;
    }
    .sb-experience-list li {
        color: #3d5272;
        font-size: 14px;
        padding: 8px 0;
        border-bottom: 1px solid #eef1f5;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sb-experience-list li .check {
        color: #1abc9c;
        font-weight: bold;
        font-size: 16px;
    }

    /* === CHAT SECTION === */
    .sb-chat-section {
        background: #f8fafb;
        padding: 50px 50px 30px;
        text-align: center;
    }
    .sb-chat-section h2 {
        font-size: 30px;
        font-weight: 700;
        color: #0b2545;
        margin-bottom: 8px;
    }
    .sb-chat-section .sb-subtitle {
        color: #6b7c93;
        font-size: 15px;
        margin-bottom: 20px;
    }

    /* === FOOTER === */
    .sb-footer {
        background: #091d36;
        padding: 40px 50px 25px;
        color: rgba(255,255,255,0.6);
    }
    .sb-footer-grid {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 30px;
        margin-bottom: 30px;
    }
    .sb-footer-col {
        min-width: 180px;
    }
    .sb-footer-col h4 {
        color: white;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .sb-footer-col p, .sb-footer-col a {
        color: rgba(255,255,255,0.5);
        font-size: 13px;
        line-height: 2;
        text-decoration: none;
        display: block;
    }
    .sb-footer-col a:hover {
        color: #1abc9c;
    }
    .sb-footer-bottom {
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 18px;
        text-align: center;
        font-size: 12px;
        color: rgba(255,255,255,0.35);
    }

    /* === LAB BANNER === */
    .lab-banner {
        background: #fff8e6;
        border: 1px solid #f0d98c;
        color: #7a5c00;
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 13px;
        margin: 10px 50px 0;
    }

    /* === ADMIN PANEL STYLES === */
    .admin-restricted-banner {
        background: #fef3f2;
        border: 1px solid #f5c6c6;
        color: #7a1a1a;
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* Fix inner container padding for tab content */
    .stTabs [data-baseweb="tab-panel"] {
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_log" not in st.session_state:
    st.session_state.last_log = None
if "defense_on" not in st.session_state:
    st.session_state.defense_on = False

# Main Layout with Tabs
tab1, tab2 = st.tabs(["✈️  SkyBridge Airlines", "🔒  Admin Panel"])

# ============================================================
# TAB 1 — PUBLIC AIRLINE WEBSITE
# ============================================================
with tab1:

    # --- Lab Disclaimer ---
    st.markdown("""
    <div class="lab-banner">
        🔬 <b>Educational simulation:</b> this is a fictional airline built for a cybersecurity capstone lab.
        No real company, passengers, or payment data are involved.
    </div>
    """, unsafe_allow_html=True)

    # --- Navbar ---
    st.markdown(f"""
    <div class="sb-navbar">
        <div class="sb-navbar-brand">
            <img src="data:image/png;base64,{LOGO_IMG}" alt="SkyBridge Logo" />
            <div>
                <div class="sb-navbar-brand-text">SKYBRIDGE</div>
                <div class="sb-navbar-brand-sub">Airlines</div>
            </div>
        </div>
        <div class="sb-nav-links">
            <a href="#">Home</a>
            <a href="#">About Us</a>
            <a href="#">Our Fleet</a>
            <a href="#">Destinations</a>
            <a href="#">Services</a>
            <a href="#">Contact</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Hero Section ---
    st.markdown(f"""
    <div class="sb-hero" style="background-image: url('data:image/png;base64,{HERO_IMG}');">
        <div class="sb-hero-overlay"></div>
        <div class="sb-hero-content">
            <h1>Flying Domestic and International Skies for Decades</h1>
            <p>Fast, frequent & direct flights. Experience world-class service with SkyBridge Airlines — your trusted partner in the sky since 1998.</p>
            <a href="#" class="sb-hero-cta">Book Now</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Features Section ---
    st.markdown(f"""
    <div class="sb-section">
        <h2>Let's Fly Away in Style!</h2>
        <p class="sb-subtitle">SkyBridge Airlines combines decades of experience with cutting-edge technology to deliver a premium flying experience across 40+ global destinations.</p>
        <div class="sb-features">
            <div class="sb-feature-card">
                <img src="data:image/png;base64,{STAFF_IMG}" alt="Experienced Staff" />
                <div class="sb-feature-card-body">
                    <h3>Experienced Staff</h3>
                    <p>Our award-winning cabin crew is trained to deliver exceptional service on every flight, ensuring your comfort and safety from takeoff to landing.</p>
                    <a href="#" class="sb-readmore">Read More →</a>
                </div>
            </div>
            <div class="sb-feature-card">
                <img src="data:image/png;base64,{FLEET_IMG}" alt="Modern Fleet" />
                <div class="sb-feature-card-body">
                    <h3>Modern Fleet</h3>
                    <p>We operate a fleet of state-of-the-art aircraft featuring the latest in fuel efficiency, passenger comfort, and in-flight entertainment systems.</p>
                    <a href="#" class="sb-readmore">Read More →</a>
                </div>
            </div>
            <div class="sb-feature-card">
                <img src="data:image/png;base64,{DEST_IMG}" alt="Global Destinations" />
                <div class="sb-feature-card-body">
                    <h3>Global Destinations</h3>
                    <p>From bustling cityscapes to serene tropical islands — explore 40+ destinations worldwide with SkyBridge's extensive route network.</p>
                    <a href="#" class="sb-readmore">Read More →</a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Stats Bar ---
    st.markdown("""
    <div class="sb-stats">
        <div class="sb-stat-item">
            <div class="sb-stat-number">40+</div>
            <div class="sb-stat-label">Destinations</div>
        </div>
        <div class="sb-stat-item">
            <div class="sb-stat-number">2M+</div>
            <div class="sb-stat-label">Passengers Yearly</div>
        </div>
        <div class="sb-stat-item">
            <div class="sb-stat-number">98%</div>
            <div class="sb-stat-label">On-Time Rate</div>
        </div>
        <div class="sb-stat-item">
            <div class="sb-stat-number">25+</div>
            <div class="sb-stat-label">Years of Excellence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Experience Section (image + text side by side) ---
    st.markdown(f"""
    <div class="sb-experience">
        <div class="sb-experience-img">
            <img src="data:image/png;base64,{CABIN_IMG}" alt="Business Class Cabin" />
        </div>
        <div class="sb-experience-text">
            <h2>A Premium Travel Experience</h2>
            <p>Whether you're flying Economy, Economy Plus, or Business Class, SkyBridge Airlines ensures every journey is comfortable, convenient, and memorable.</p>
            <ul class="sb-experience-list">
                <li><span class="check">✓</span> Complimentary meals on all international flights</li>
                <li><span class="check">✓</span> Free 23 kg checked baggage on Economy Plus & above</li>
                <li><span class="check">✓</span> In-seat power & high-speed Wi-Fi</li>
                <li><span class="check">✓</span> Priority boarding for loyalty members</li>
                <li><span class="check">✓</span> 24/7 customer support with Skye, our AI assistant</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Chat with Skye Section ---
    st.markdown("""
    <div class="sb-chat-section">
        <h2>💬 Chat with Skye</h2>
        <p class="sb-subtitle">Have a question about your flight, baggage, or booking? Skye is here to help 24/7.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Streamlit Chat UI ---
    chat_container = st.container()
    with chat_container:
        col_spacer_l, col_chat, col_spacer_r = st.columns([0.5, 3, 0.5])
        with col_chat:
            # Display chat messages
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            # Chat input
            user_input = st.chat_input("Ask Skye about your flight, booking, or travel plans...")

            if user_input:
                # 1. Add user message
                st.session_state.messages.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.markdown(user_input)

                # 2. Defense Layer Check
                blocked = False
                analysis = {"threat_score": 0, "reason": "Defense Layer Offline"}

                if st.session_state.defense_on:
                    with st.spinner("Skye's security layer is analyzing your message..."):
                        blocked, analysis = is_blocked(user_input)

                st.session_state.last_log = {
                    "prompt": user_input,
                    "defense_on": st.session_state.defense_on,
                    "blocked": blocked,
                    "analysis": analysis
                }

                # 3. Handle response
                if blocked:
                    bot_response = f"🚫 **MESSAGE BLOCKED BY SKYBRIDGE SECURITY**\n\nYour message was flagged by our automated defense system before reaching Skye.\n\n**Threat Score:** {analysis['threat_score']}/10\n**Reason:** {analysis['reason']}"
                else:
                    with st.spinner("Skye is typing..."):
                        # Filter out blocked messages from history
                        history_for_bot = [m for m in st.session_state.messages if "🚫 **MESSAGE BLOCKED" not in m["content"]]
                        bot_response = chat_with_corpbot(history_for_bot)

                # 4. Add bot response
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                with st.chat_message("assistant"):
                    st.markdown(bot_response)

    # --- Footer ---
    st.markdown(f"""
    <div class="sb-footer">
        <div class="sb-footer-grid">
            <div class="sb-footer-col">
                <h4>SkyBridge Airlines</h4>
                <p>Your trusted partner in the sky. Operating since 1998 with an unwavering commitment to safety, comfort, and reliability.</p>
            </div>
            <div class="sb-footer-col">
                <h4>Quick Links</h4>
                <a href="#">Flight Status</a>
                <a href="#">Check-in Online</a>
                <a href="#">Baggage Info</a>
                <a href="#">Loyalty Program</a>
            </div>
            <div class="sb-footer-col">
                <h4>Travel Services</h4>
                <a href="#">Book a Flight</a>
                <a href="#">Manage Booking</a>
                <a href="#">Travel Insurance</a>
                <a href="#">Airport Lounges</a>
            </div>
            <div class="sb-footer-col">
                <h4>Contact Us</h4>
                <p>📧 support@skybridge-air.com</p>
                <p>📞 +1-800-SKY-BRIDGE</p>
                <p>🕐 24/7 Customer Support</p>
            </div>
        </div>
        <div class="sb-footer-bottom">
            © 2026 SkyBridge Airlines. All rights reserved. | This is a fictional company created for educational purposes.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# TAB 2 — ADMIN PANEL (unchanged)
# ============================================================
with tab2:
    st.header("🔒 Admin Panel")
    st.markdown("""
    <div class="admin-restricted-banner">
        🔐 <b>Restricted Access</b> — This panel is for authorized SkyBridge IT administrators only. It is not accessible from the public website.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("🛡️ Defense Controls")
    st.write("Enable the AI security middleware that screens every incoming message before it reaches Skye.")
    # Toggle defense layer
    new_defense_state = st.toggle("Enable AI Defense Layer", value=st.session_state.defense_on)
    if new_defense_state != st.session_state.defense_on:
        st.session_state.defense_on = new_defense_state

    if st.session_state.defense_on:
        st.success("🟢 Defense Layer is ACTIVE — All messages are being screened.")
    else:
        st.error("🔴 Defense Layer is OFFLINE — Messages are passing through unfiltered.")

    st.write("")  # Spacer
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.last_log = None
        st.rerun()

    st.markdown("---")
    st.subheader("📊 Real-Time Request Logs")
    if st.session_state.last_log:
        log = st.session_state.last_log
        st.write("**Last User Prompt:**")
        st.code(log["prompt"], language="text")

        if log["defense_on"]:
            score = log['analysis']['threat_score']
            color = "red" if score >= 6 else "green"
            st.markdown(f"**Defense Analysis:** Threat Score :{color}[{score}/10]")
            st.write(f"**Reason:** {log['analysis']['reason']}")
            if log["blocked"]:
                st.error("Action: BLOCKED")
            else:
                st.success("Action: ALLOWED")
        else:
            st.warning("Defense layer was OFF during this request.")
    else:
        st.info("No logs available yet. Send a message in the Skye chat to start monitoring.")
