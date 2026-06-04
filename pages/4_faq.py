import streamlit as st
from data import db

st.set_page_config(
    page_title="FAQ - LegalAssist",
    page_icon="❓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .page-header {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
    }
    .page-header h1 {
        margin: 0;
        font-size: 2rem;
    }
    .page-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .faq-item {
        background: white;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        border: 1px solid #e5e7eb;
        overflow: hidden;
        transition: all 0.3s;
    }
    .faq-question {
        padding: 1rem 1.5rem;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: white;
        transition: background 0.2s;
    }
    .faq-question:hover {
        background: #f9fafb;
    }
    .faq-answer {
        padding: 0 1.5rem 1rem 1.5rem;
        color: #6b7280;
        line-height: 1.6;
        border-top: 1px solid #e5e7eb;
        background: #f9fafb;
    }
    .faq-arrow {
        transition: transform 0.3s;
    }
    .faq-arrow.open {
        transform: rotate(180deg);
    }
    .faq-cta {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        color: white;
        margin-top: 2rem;
    }
    .faq-cta h3 {
        margin: 0 0 0.5rem 0;
    }
    .faq-cta p {
        margin: 0 0 1rem 0;
        opacity: 0.9;
    }
    .category-filter {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    .filter-chip {
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        background: #f3f4f6;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.875rem;
    }
    .filter-chip:hover, .filter-chip.active {
        background: #4f46e5;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="page-header">
    <h1>❓ Pertanyaan Umum (FAQ)</h1>
    <p>Temukan jawaban dari pertanyaan yang paling sering ditanyakan</p>
</div>
""", unsafe_allow_html=True)

# Get unique categories
kategori_list = ["Semua"] + sorted(list(set([f["kategori"] for f in db["faq"]])))

# Category filter
st.markdown("### 🔍 Filter Kategori")

cols = st.columns(len(kategori_list))
for idx, kat in enumerate(kategori_list):
    with cols[idx]:
        if st.button(kat, key=f"cat_{kat}", use_container_width=True):
            st.session_state.selected_faq_category = kat
            st.rerun()

# Initialize session state for selected category
if "selected_faq_category" not in st.session_state:
    st.session_state.selected_faq_category = "Semua"

# Filter FAQs
filtered_faq = db["faq"]
if st.session_state.selected_faq_category != "Semua":
    filtered_faq = [f for f in filtered_faq if f["kategori"] == st.session_state.selected_faq_category]

# Results count
st.markdown(f"<p style='color: #6b7280; margin-bottom: 1rem;'>Menampilkan {len(filtered_faq)} pertanyaan</p>", unsafe_allow_html=True)

# Initialize FAQ open state
if "faq_open" not in st.session_state:
    st.session_state.faq_open = {}

# Display FAQs
for idx, faq in enumerate(filtered_faq):
    faq_id = faq["id"]
    
    # Check if this FAQ is open
    is_open = st.session_state.faq_open.get(faq_id, False)
    
    # FAQ item
    with st.container():
        col1, col2 = st.columns([10, 1])
        with col1:
            if st.button(f"📌 {faq['pertanyaan']}", key=f"q_{faq_id}", use_container_width=True):
                st.session_state.faq_open[faq_id] = not st.session_state.faq_open.get(faq_id, False)
                st.rerun()
        with col2:
            st.markdown(f"<span style='font-size: 0.7rem; color: #9ca3af;'>{faq['kategori']}</span>", unsafe_allow_html=True)
        
        if is_open:
            st.markdown(f"""
            <div style="background: #f9fafb; padding: 1rem 1.5rem; border-radius: 0.5rem; margin: 0.5rem 0 1rem 0; border-left: 3px solid #4f46e5;">
                {faq['jawaban']}
            </div>
            """, unsafe_allow_html=True)

# Alternative display using expander
st.markdown("### 📋 Semua Pertanyaan")

for faq in filtered_faq:
    with st.expander(f"📌 {faq['pertanyaan']}"):
        st.markdown(f"<p>{faq['jawaban']}</p>", unsafe_allow_html=True)
        st.caption(f"Kategori: {faq['kategori']}")

# CTA Section
st.markdown("""
<div class="faq-cta">
    <h3>Tidak menemukan jawaban?</h3>
    <p>Hubungi kami langsung atau gunakan chatbot konsultasi kami</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("📞 Hubungi Kami", use_container_width=True):
        st.switch_page("pages/5_kontak.py")
with col2:
    if st.button("💬 Chatbot Konsultasi", use_container_width=True):
        st.switch_page("pages/1_chatbot.py")