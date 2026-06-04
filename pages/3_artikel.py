import streamlit as st
from data import db

st.set_page_config(
    page_title="Artikel Hukum - LegalAssist",
    page_icon="📚",
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
    .artikel-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e5e7eb;
        transition: all 0.3s;
        cursor: pointer;
    }
    .artikel-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
        border-color: #c7d2fe;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-pidana { background: #fee2e2; color: #ef4444; }
    .badge-perdata { background: #dbeafe; color: #3b82f6; }
    .badge-keluarga { background: #f3e8ff; color: #7c3aed; }
    .badge-ketenagakerjaan { background: #fef3c7; color: #f59e0b; }
    .artikel-meta {
        display: flex;
        gap: 1rem;
        margin: 0.75rem 0;
        color: #6b7280;
        font-size: 0.75rem;
    }
    .artikel-judul {
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0.5rem 0;
        color: #1f2937;
    }
    .artikel-ringkasan {
        color: #6b7280;
        line-height: 1.5;
        margin: 0.5rem 0;
    }
    .read-more {
        color: #4f46e5;
        font-weight: 500;
        text-decoration: none;
        margin-top: 0.5rem;
        display: inline-block;
    }
    .read-more:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="page-header">
    <h1>📚 Artikel Hukum</h1>
    <p>Perluas pengetahuan hukum Anda melalui artikel informatif dari para ahli</p>
</div>
""", unsafe_allow_html=True)

# Filter section
st.markdown("### 🔍 Filter Berdasarkan Kategori")

# Get unique categories
kategori_list = ["Semua"] + sorted(list(set([a["kategori"] for a in db["artikel"]])))

col1, col2 = st.columns([2, 1])
with col1:
    selected_kategori = st.selectbox("Pilih Kategori", kategori_list, label_visibility="collapsed")
with col2:
    if st.button("🔄 Reset Filter", use_container_width=True):
        selected_kategori = "Semua"
        st.rerun()

# Filter data
filtered_artikel = db["artikel"]
if selected_kategori != "Semua":
    filtered_artikel = [a for a in filtered_artikel if a["kategori"] == selected_kategori]

# Results count
st.markdown(f"<p style='color: #6b7280; margin-bottom: 1rem;'>Menampilkan {len(filtered_artikel)} artikel</p>", unsafe_allow_html=True)

# Session state for selected article
if "selected_article" not in st.session_state:
    st.session_state.selected_article = None

# Function to show article detail
def show_article_detail(artikel):
    st.session_state.selected_article = artikel
    st.rerun()

# Display articles
if st.session_state.selected_article is None:
    for artikel in filtered_artikel:
        badge_class = f"badge-{artikel['kategori'].lower()}"
        
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="artikel-card">
                    <span class="badge {badge_class}">{artikel['kategori']}</span>
                    <div class="artikel-judul">{artikel['judul']}</div>
                    <div class="artikel-meta">
                        <span>✍ {artikel['penulis']}</span>
                        <span>📅 {artikel['tanggal']}</span>
                        <span>👁 {artikel['baca']} dibaca</span>
                    </div>
                    <div class="artikel-ringkasan">{artikel['ringkasan']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("Baca →", key=f"read_{artikel['id']}"):
                    show_article_detail(artikel)
else:
    # Show article detail
    artikel = st.session_state.selected_article
    
    # Back button
    if st.button("← Kembali ke Daftar Artikel"):
        st.session_state.selected_article = None
        st.rerun()
    
    # Article detail
    badge_class = f"badge-{artikel['kategori'].lower()}"
    
    st.markdown(f"""
    <div style="background: white; border-radius: 1rem; padding: 2rem; border: 1px solid #e5e7eb;">
        <span class="badge {badge_class}">{artikel['kategori']}</span>
        <h1 style="margin: 1rem 0 0.5rem 0;">{artikel['judul']}</h1>
        <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem; color: #6b7280; font-size: 0.875rem;">
            <span>✍ {artikel['penulis']}</span>
            <span>📅 {artikel['tanggal']}</span>
            <span>👁 {artikel['baca']} dibaca</span>
        </div>
        <div style="border-top: 1px solid #e5e7eb; padding-top: 1.5rem; line-height: 1.8;">
            {artikel['isi']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div style="background: #f3f4f6; border-radius: 1rem; padding: 2rem; text-align: center; margin-top: 2rem;">
        <h3>Butuh konsultasi lebih lanjut?</h3>
        <p style="color: #6b7280;">Hubungi advokat kami atau gunakan chatbot konsultasi</p>
        <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 1rem;">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💬 Konsultasi dengan Chatbot", use_container_width=True):
            st.switch_page("pages/1_chatbot.py")
    with col2:
        if st.button("👨‍⚖️ Cari Advokat", use_container_width=True):
            st.switch_page("pages/2_advokat.py")
    
    st.markdown("</div></div>", unsafe_allow_html=True)

if not filtered_artikel and st.session_state.selected_article is None:
    st.info("Tidak ada artikel yang ditemukan untuk kategori ini.")