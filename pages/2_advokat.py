import streamlit as st
from data import db

st.set_page_config(
    page_title="Informasi Advokat - LegalAssist",
    page_icon="👨‍⚖️",
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
    .advokat-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e5e7eb;
        transition: all 0.3s;
    }
    .advokat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
        border-color: #c7d2fe;
    }
    .advokat-avatar {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
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
    .stat-detail {
        display: flex;
        gap: 1rem;
        margin: 0.75rem 0;
        color: #6b7280;
        font-size: 0.875rem;
        flex-wrap: wrap;
    }
    .contact-info {
        display: flex;
        gap: 1rem;
        margin-top: 0.75rem;
        flex-wrap: wrap;
    }
    .contact-link {
        background: #f3f4f6;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        text-decoration: none;
        color: #374151;
        font-size: 0.875rem;
        transition: all 0.2s;
    }
    .contact-link:hover {
        background: #e0e7ff;
        color: #4f46e5;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="page-header">
    <h1>👨‍⚖️ Informasi Advokat</h1>
    <p>Temukan advokat berpengalaman dan berlisensi sesuai kebutuhan hukum Anda</p>
</div>
""", unsafe_allow_html=True)

# Filter section
st.markdown("### 🔍 Filter Berdasarkan Spesialisasi")

# Get unique spesialisasi
spesialisasi_list = ["Semua"] + sorted(list(set([a["spesialisasi"] for a in db["advokat"]])))

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    selected_spesialisasi = st.selectbox("Pilih Spesialisasi", spesialisasi_list, label_visibility="collapsed")
with col2:
    search_query = st.text_input("Cari nama advokat", placeholder="Ketik nama advokat...", label_visibility="collapsed")
with col3:
    if st.button("🔄 Reset Filter", use_container_width=True):
        selected_spesialisasi = "Semua"
        search_query = ""
        st.rerun()

# Filter data
filtered_advokat = db["advokat"]
if selected_spesialisasi != "Semua":
    filtered_advokat = [a for a in filtered_advokat if a["spesialisasi"] == selected_spesialisasi]
if search_query:
    filtered_advokat = [a for a in filtered_advokat if search_query.lower() in a["nama"].lower()]

# Results count
st.markdown(f"<p style='color: #6b7280; margin-bottom: 1rem;'>Menampilkan {len(filtered_advokat)} advokat</p>", unsafe_allow_html=True)

# Display advokat cards
for adv in filtered_advokat:
    badge_class = f"badge-{adv['spesialisasi'].lower()}"
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown(f"""
        <div class="advokat-avatar">
            {adv['nama'][0]}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="advokat-card">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <h3 style="margin: 0;">{adv['nama']}</h3>
                <span class="badge {badge_class}">{adv['spesialisasi']}</span>
            </div>
            <div class="stat-detail">
                <span>📍 {adv['kota']}</span>
                <span>⏱ {adv['pengalaman']}</span>
                <span>⭐ {adv['rating']} / 5.0</span>
                <span>📁 {adv['kasus']} kasus ditangani</span>
            </div>
            <div class="contact-info">
                <a href="tel:{adv['telepon']}" class="contact-link">📞 {adv['telepon']}</a>
                <a href="mailto:{adv['email']}" class="contact-link">✉️ {adv['email']}</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

if not filtered_advokat:
    st.info("Tidak ada advokat yang ditemukan dengan kriteria tersebut.")

# Footer stats
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Advokat", len(db["advokat"]))
with col2:
    st.metric("Spesialisasi Tersedia", len(set([a["spesialisasi"] for a in db["advokat"]])))
with col3:
    rata_rating = sum([a["rating"] for a in db["advokat"]]) / len(db["advokat"])
    st.metric("Rata-rata Rating", f"{rata_rating:.1f} / 5.0")
with col4:
    total_kasus = sum([a["kasus"] for a in db["advokat"]])
    st.metric("Total Kasus Ditangani", total_kasus)