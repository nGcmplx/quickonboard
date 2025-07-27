import streamlit as st
import requests
import uuid

st.set_page_config(page_title="QuickOnboard Chat", layout="centered")

st.markdown("""
<style>
    .stTextInput input {
        border-radius: 8px;
        padding: 0.5rem;
    }
    .stChatMessage {
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    .stChatMessage.user {
        background-color: #ffecec;
    }
    .stChatMessage.assistant {
        background-color: #fffce8;
    }
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("QuickOnboard HR Assistant")

col1, col2 = st.columns([1.5, 3])

with col1:
    is_anon = st.toggle("Anonymous Mode", value=False)

with col2:
    if is_anon:
        name = "anon"
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <label style="font-weight: 600; font-size: 16px;">Name:</label>
                <input type="text" value="anon" disabled
                    style="flex: 1; padding: 0.4rem 0.6rem; border-radius: 8px; border: 1px solid #ccc; background-color: #eee;" />
            </div>
            """, unsafe_allow_html=True)
    else:
        name = st.text_input("Name:", key="name_input", label_visibility="collapsed", placeholder="Enter your name")

prompt = st.chat_input("Ask your HR question...")

if "history" not in st.session_state:
    st.session_state["history"] = []

for item in st.session_state["history"]:
    st.chat_message(item["role"]).markdown(item["content"])

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state["history"].append({"role": "user", "content": prompt})

    payload = {
        "prompt": prompt,
        "session_id": name if name.strip() else f"anon-{uuid.uuid4().hex[:8]}",
        "log": not is_anon
    }

    try:
        res = requests.post("http://api-service/chat", json=payload)
        res.raise_for_status()
        data = res.json()
        reply = data["response"]
        st.chat_message("assistant").markdown(reply)
        st.session_state["history"].append({"role": "assistant", "content": reply})

    except requests.exceptions.RequestException as e:
        st.error(f"⚠Cannot reach backend: {e}")
