import streamlit as st
from fsm import LegalFSM

st.set_page_config(
    page_title="Chatbot Konsultasi - LegalAssist",
    page_icon="💬",
    layout="wide"
)

# Custom CSS untuk chatbot
st.markdown("""
<style>
    .chat-header {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
    }
    .chat-header h1 {
        margin: 0;
        font-size: 2rem;
    }
    .chat-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .chat-message-user {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 1rem 1rem 0.25rem 1rem;
        margin: 0.5rem 0;
        display: inline-block;
        max-width: 80%;
        float: right;
    }
    .chat-message-bot {
        background: #f3f4f6;
        color: #1f2937;
        padding: 0.75rem 1rem;
        border-radius: 0.25rem 1rem 1rem 1rem;
        margin: 0.5rem 0;
        display: inline-block;
        max-width: 80%;
        float: left;
    }
    .chat-container {
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background: white;
        border-radius: 1rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    .clearfix::after {
        content: "";
        clear: both;
        display: table;
    }
    .option-btn {
        background: #f3f4f6;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.2s;
        display: inline-block;
    }
    .option-btn:hover {
        background: #e0e7ff;
        border-color: #4f46e5;
        transform: translateX(2px);
    }
    .result-card {
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .dokumen-list {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #e5e7eb;
    }
    .stButton button {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "fsm" not in st.session_state:
    st.session_state.fsm = LegalFSM()
    st.session_state.messages = []
    st.session_state.waiting_response = False

# Header
st.markdown("""
<div class="chat-header">
    <h1>💬 Konsultasi Hukum</h1>
    <p>Chatbot berbasis Finite State Automata untuk membantu Anda memahami masalah hukum secara terstruktur</p>
</div>
""", unsafe_allow_html=True)

# Sidebar info
with st.sidebar:
    st.markdown("### ℹ️ Informasi")
    st.markdown("---")
    st.markdown("#### 📋 Kategori Tersedia")
    st.markdown("""
    - ⚖️ **Pidana** (Penipuan, Pencurian)
    - 📋 **Perdata** (Hutang, Wanprestasi)
    - 👨‍👩‍👧 **Keluarga** (Perceraian, Hak Asuh)
    - 💼 **Ketenagakerjaan** (PHK, Perselisihan)
    """)
    st.markdown("---")
    st.markdown("#### 📌 Cara Penggunaan")
    st.markdown("""
    1. Pilih kategori hukum (1-4)
    2. Jawab pertanyaan chatbot
    3. Terima hasil & rekomendasi
    4. Hubungi advokat jika perlu
    """)
    st.markdown("---")
    if st.button("🔄 Mulai Ulang Konsultasi", use_container_width=True):
        st.session_state.fsm.reset()
        st.session_state.messages = []
        st.session_state.waiting_response = False
        st.rerun()

# Display chat messages
chat_container = st.container()

with chat_container:
    # Create a container for messages
    message_placeholder = st.empty()
    
    # Render all messages
    messages_html = '<div class="chat-container">'
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            messages_html += f'<div class="clearfix"><div class="chat-message-user">{msg["content"]}</div></div>'
        else:
            messages_html += f'<div class="clearfix"><div class="chat-message-bot">{msg["content"]}</div></div>'
    messages_html += '</div>'
    
    message_placeholder.markdown(messages_html, unsafe_allow_html=True)

# Function to render menu options as buttons
def render_menu_options(options):
    cols = st.columns(len(options))
    for idx, opt in enumerate(options):
        with cols[idx]:
            if st.button(f"{opt['key']}. {opt['label']}", key=f"opt_{opt['key']}"):
                return opt['key']
    return None

# Function to render result
def render_result(response):
    kategori_colors = {
        "pidana": "🔴",
        "perdata": "🔵",
        "keluarga": "🟣",
        "ketenagakerjaan": "🟡"
    }
    color = kategori_colors.get(response["kategori"], "⚪")
    
    result_html = f"""
    <div class="result-card">
        <div style="font-size: 1.25rem; font-weight: bold; margin-bottom: 0.5rem;">
            {color} {response['title']}
        </div>
        <div style="font-size: 0.875rem; color: #6b7280; margin-bottom: 1rem;">
            {response['pasal']}
        </div>
        <p>{response['text']}</p>
        <div class="dokumen-list">
            <strong>📄 Dokumen yang diperlukan:</strong>
            <ul style="margin: 0.5rem 0 0 1rem;">
    """
    for doc in response["dokumen"]:
        result_html += f"<li>{doc}</li>"
    
    result_html += f"""
            </ul>
        </div>
        <div style="background: #dbeafe; padding: 0.5rem; border-radius: 0.5rem; margin-top: 0.5rem;">
            👨‍⚖️ <strong>Rekomendasi:</strong> {response['advokat']}
        </div>
    </div>
    """
    
    if st.button("🔄 Mulai Konsultasi Baru", key="new_consultation"):
        st.session_state.fsm.reset()
        st.session_state.messages = []
        st.rerun()
    
    return result_html

# Chat input
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("Ketik pesan atau nomor pilihan:", key="chat_input", placeholder="Contoh: 1 (untuk Pidana) atau 'reset' untuk mulai ulang")
with col2:
    send_button = st.button("📤 Kirim", use_container_width=True)

# Process input
if (send_button or user_input) and user_input and not st.session_state.waiting_response:
    user_message = user_input
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    # Reset input
    st.session_state.waiting_response = True
    
    # Process response
    if user_message.lower() in ["reset", "mulai ulang", "restart", "baru"]:
        st.session_state.fsm.reset()
        response = st.session_state.fsm._menu_utama("✨ Sesi direset. Mulai konsultasi baru:")
    else:
        response = st.session_state.fsm.transition(user_message)
    
    # Format response based on type
    if response["type"] == "menu":
        menu_text = f"**{response['title']}**\n\n{response['text']}\n\n"
        for opt in response["options"]:
            menu_text += f"`{opt['key']}` {opt['label']}\n"
        st.session_state.messages.append({"role": "bot", "content": menu_text})
    
    elif response["type"] == "result":
        result_text = f"""
**📋 HASIL KONSULTASI**

**{response['title']}** ({response['pasal']})

{response['text']}

**📄 Dokumen yang diperlukan:**
{chr(10).join(['• ' + d for d in response['dokumen']])}

**👨‍⚖️ Rekomendasi:** {response['advokat']}

---
Ketik `reset` untuk konsultasi baru.
"""
        st.session_state.messages.append({"role": "bot", "content": result_text})
    
    else:
        st.session_state.messages.append({"role": "bot", "content": response.get("text", "Maaf, saya tidak mengerti. Silakan coba lagi.")})
    
    st.session_state.waiting_response = False
    st.rerun()

# Quick action buttons
st.markdown("---")
st.markdown("### ⚡ Pilihan Cepat")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("⚖️ Pidana", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "1"})
        response = st.session_state.fsm.transition("1")
        if response["type"] == "menu":
            menu_text = f"**{response['title']}**\n\n{response['text']}\n\n"
            for opt in response["options"]:
                menu_text += f"`{opt['key']}` {opt['label']}\n"
            st.session_state.messages.append({"role": "bot", "content": menu_text})
        st.rerun()
with col2:
    if st.button("📋 Perdata", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "2"})
        response = st.session_state.fsm.transition("2")
        if response["type"] == "menu":
            menu_text = f"**{response['title']}**\n\n{response['text']}\n\n"
            for opt in response["options"]:
                menu_text += f"`{opt['key']}` {opt['label']}\n"
            st.session_state.messages.append({"role": "bot", "content": menu_text})
        st.rerun()
with col3:
    if st.button("👨‍👩‍👧 Keluarga", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "3"})
        response = st.session_state.fsm.transition("3")
        if response["type"] == "menu":
            menu_text = f"**{response['title']}**\n\n{response['text']}\n\n"
            for opt in response["options"]:
                menu_text += f"`{opt['key']}` {opt['label']}\n"
            st.session_state.messages.append({"role": "bot", "content": menu_text})
        st.rerun()
with col4:
    if st.button("💼 Tenaga Kerja", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "4"})
        response = st.session_state.fsm.transition("4")
        if response["type"] == "menu":
            menu_text = f"**{response['title']}**\n\n{response['text']}\n\n"
            for opt in response["options"]:
                menu_text += f"`{opt['key']}` {opt['label']}\n"
            st.session_state.messages.append({"role": "bot", "content": menu_text})
        st.rerun()
with col5:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.fsm.reset()
        st.session_state.messages = []
        st.rerun()

# Instructions
st.markdown("---")
st.markdown("""
<div style="background: #f3f4f6; padding: 1rem; border-radius: 0.5rem; font-size: 0.875rem; color: #6b7280;">
    <strong>💡 Tips:</strong> Ketik angka pilihan (1-4) untuk memilih kategori, atau ketik "reset" untuk memulai konsultasi baru.
</div>
""", unsafe_allow_html=True)