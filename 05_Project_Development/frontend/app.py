import os
import requests
import streamlit as st

# Configure Streamlit page settings
st.set_page_config(
    page_title="NetConnect - Personalized Networking Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Load and inject custom CSS stylesheet
css_path = os.path.join(os.path.dirname(__file__), "styles", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("Custom CSS file not found. Falling back to default layout styling.")

# Initialize session state keys if not present
if "gemini_api_key" not in st.session_state:
    st.session_state["gemini_api_key"] = ""
if "latest_generation" not in st.session_state:
    st.session_state["latest_generation"] = None

# Sidebar Logo and Navigation
st.sidebar.markdown(
    """
    <div class="sidebar-logo">
        <span style="font-size: 2.2rem;">🤝</span>
        <span class="logo-text">NetConnect</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.subheader("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["💡 Starter Generator", "🔍 Quick Fact Verification", "📜 History & Feedback"],
    label_visibility="collapsed"
)

st.sidebar.divider()

# Sidebar settings (API Key management)
st.sidebar.subheader("Settings")
user_api_key = st.sidebar.text_input(
    "Gemini API Key (Optional)",
    value=st.session_state["gemini_api_key"],
    type="password",
    help="Enter your Gemini API key to enable AI-powered conversation starters. Leave empty to use fallback template mode."
)

if user_api_key != st.session_state["gemini_api_key"]:
    st.session_state["gemini_api_key"] = user_api_key
    st.toast("API key updated for this session!", icon="🔑")

st.sidebar.markdown(
    """
    <div style="font-size: 0.8rem; color: #64748b; margin-top: 2rem;">
        <strong>Mode Status:</strong><br>
        {}
    </div>
    """.format(
        "<span style='color: #10b981; font-weight: 600;'>🤖 AI Generation Active</span>" 
        if st.session_state["gemini_api_key"] 
        else "<span style='color: #f59e0b; font-weight: 600;'>📝 Template Fallback Active</span>"
    ),
    unsafe_allow_html=True
)

# ----------------- PAGE 1: STARTER GENERATOR -----------------
if page == "💡 Starter Generator":
    st.markdown('<h1 class="gradient-text">Starter Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Generate smart, personalized conversation starters based on the event description and your professional interests.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        event_desc = st.text_area(
            "Event Description",
            placeholder="e.g. AI for Sustainable Cities. Discussing urban mobility, carbon reductions, and smart infrastructure.",
            height=120,
            help="Describe the event, conference, panel or networking meetup you are attending."
        )
    with col2:
        interests = st.text_area(
            "Your Interests / Expertise",
            placeholder="e.g. climate change, smart infrastructure, machine learning models",
            height=120,
            help="Provide keywords or a short description of topics you're interested in talking about."
        )
        
    generate_btn = st.button("✨ Generate Starters", use_container_width=True)
    
    if generate_btn:
        if not event_desc.strip() or not interests.strip():
            st.error("Please fill in both the event description and your interests!")
        else:
            with st.spinner("Generating conversation starters..."):
                try:
                    payload = {
                        "event_description": event_desc,
                        "interests": interests,
                        "gemini_api_key": st.session_state["gemini_api_key"] or None
                    }
                    response = requests.post(f"{BACKEND_URL}/api/starters/generate", json=payload)
                    
                    if response.status_code == 201:
                        st.session_state["latest_generation"] = response.json()
                        st.success("Generation completed!")
                    else:
                        st.error(f"Error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Failed to connect to backend API: {str(e)}. Make sure the backend server is running!")
                    
    # Render latest generation if available in session_state
    if st.session_state["latest_generation"] is not None:
        data = st.session_state["latest_generation"]
        
        st.markdown("### Extracted Themes")
        # Display themes as badges
        themes_html = "".join([f'<span class="theme-badge">{t}</span>' for t in data["themes"]])
        st.markdown(f'<div style="margin-bottom: 1.5rem;">{themes_html}</div>', unsafe_allow_html=True)
        
        st.markdown("### Generated Conversation Starters")
        for idx, starter in enumerate(data["generated_starters"], 1):
            st.markdown(
                f"""
                <div class="starter-card">
                    <div class="starter-text">"{starter}"</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Add a copy button for the starter text
            st.code(starter, language="")
            
        st.divider()
        
        # Feedback section
        st.write("Was this generation helpful?")
        col_up, col_down = st.columns([1, 4])
        session_id = data["id"]
        current_feedback = data.get("feedback")
        
        with col_up:
            if st.button("👍 Helpful", key="btn_thumbs_up"):
                try:
                    res = requests.put(
                        f"{BACKEND_URL}/api/history/{session_id}/feedback", 
                        json={"feedback": "thumbs_up"}
                    )
                    if res.status_code == 200:
                        st.session_state["latest_generation"]["feedback"] = "thumbs_up"
                        st.toast("Thank you! Feedback saved. This will improve future suggestions.", icon="👍")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error sending feedback: {e}")
                    
        with col_down:
            if st.button("👎 Unhelpful", key="btn_thumbs_down"):
                try:
                    res = requests.put(
                        f"{BACKEND_URL}/api/history/{session_id}/feedback", 
                        json={"feedback": "thumbs_down"}
                    )
                    if res.status_code == 200:
                        st.session_state["latest_generation"]["feedback"] = "thumbs_down"
                        st.toast("Feedback saved. We'll adjust future suggestions.", icon="👎")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error sending feedback: {e}")
                    
        if current_feedback:
            status_text = "👍 Marked as Helpful" if current_feedback == "thumbs_up" else "👎 Marked as Unhelpful"
            st.info(f"Current Rating: {status_text}")

# ----------------- PAGE 2: QUICK FACT VERIFICATION -----------------
elif page == "🔍 Quick Fact Verification":
    st.markdown('<h1 class="gradient-text">Quick Fact Checker</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Instantly verify technical concepts, trends, or industry terms on Wikipedia before jumping into conversations.</p>', unsafe_allow_html=True)
    
    topic = st.text_input(
        "Search Topic",
        placeholder="e.g. blockchain in healthcare, zero knowledge proofs, green hydrogen",
        help="Enter the concept, acronym, or trend you want to quickly research."
    )
    
    search_btn = st.button("🔍 Search Wikipedia", use_container_width=True)
    
    if search_btn and topic.strip():
        with st.spinner(f"Searching Wikipedia for '{topic}'..."):
            try:
                response = requests.post(f"{BACKEND_URL}/api/facts/verify", json={"topic": topic})
                if response.status_code == 200:
                    res_data = response.json()
                    
                    if res_data["found"]:
                        st.markdown(
                            f"""
                            <div class="fact-card">
                                <div class="fact-title">
                                    <span>📚</span> {res_data['topic']}
                                </div>
                                <div class="fact-body">
                                    {res_data['summary']}
                                </div>
                                {f'<a href="{res_data["source_url"]}" target="_blank" class="fact-source">🔗 Read full Wikipedia article</a>' if res_data["source_url"] else ''}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.warning(res_data["summary"])
                else:
                    st.error(f"Error: {response.json().get('detail', 'Failed to retrieve information.')}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {str(e)}")

# ----------------- PAGE 3: HISTORY & FEEDBACK -----------------
elif page == "📜 History & Feedback":
    st.markdown('<h1 class="gradient-text">Conversation History</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Review your past generated conversation starters and update ratings to continuously train the generator.</p>', unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/history")
        if response.status_code == 200:
            history_data = response.json()
            
            if not history_data:
                st.info("No conversation starters generated yet! Go to the Generator tab to create your first session.")
            else:
                for idx, session in enumerate(history_data):
                    date_str = session["created_at"]
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                        date_formatted = dt.strftime("%b %d, %Y - %I:%M %p")
                    except Exception:
                        date_formatted = date_str
                        
                    feedback_indicator = ""
                    if session["feedback"] == "thumbs_up":
                        feedback_indicator = " 👍"
                    elif session["feedback"] == "thumbs_down":
                        feedback_indicator = " 👎"
                        
                    expander_label = f"📍 Event: {session['event_description'][:60]}... | {date_formatted}{feedback_indicator}"
                    
                    with st.expander(expander_label, expanded=(idx == 0)):
                        st.write(f"**Event Description:** {session['event_description']}")
                        st.write(f"**Your Interests:** {session['interests']}")
                        
                        # Display themes as badges
                        themes_html = "".join([f'<span class="theme-badge">{t}</span>' for t in session["themes"]])
                        st.markdown(f'<div style="margin-top:0.5rem; margin-bottom:1rem;">{themes_html}</div>', unsafe_allow_html=True)
                        
                        st.markdown("**Generated Starters:**")
                        for starter in session["generated_starters"]:
                            st.markdown(
                                f"""
                                <div class="starter-card">
                                    <div class="starter-text">"{starter}"</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            st.code(starter, language="")
                            
                        # Manage feedback
                        session_id = session["id"]
                        curr_feedback = session["feedback"]
                        
                        st.write("Rate this generation:")
                        col_up, col_down = st.columns([1, 4])
                        
                        with col_up:
                            btn_label_up = "👍 Helpful" + (" (Active)" if curr_feedback == "thumbs_up" else "")
                            if st.button(btn_label_up, key=f"up_{session_id}"):
                                try:
                                    res = requests.put(
                                        f"{BACKEND_URL}/api/history/{session_id}/feedback",
                                        json={"feedback": "thumbs_up"}
                                    )
                                    if res.status_code == 200:
                                        st.toast("Rating updated to Helpful!", icon="👍")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Error updating rating: {e}")
                                    
                        with col_down:
                            btn_label_down = "👎 Unhelpful" + (" (Active)" if curr_feedback == "thumbs_down" else "")
                            if st.button(btn_label_down, key=f"down_{session_id}"):
                                try:
                                    res = requests.put(
                                        f"{BACKEND_URL}/api/history/{session_id}/feedback",
                                        json={"feedback": "thumbs_down"}
                                    )
                                    if res.status_code == 200:
                                        st.toast("Rating updated to Unhelpful!", icon="👎")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Error updating rating: {e}")
        else:
            st.error(f"Failed to fetch history (Status {response.status_code})")
    except Exception as e:
        st.error(f"Failed to connect to history API: {str(e)}")
