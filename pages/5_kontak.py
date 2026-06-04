import streamlit as st
from data import db
from datetime import datetime

st.set_page_config(
    page_title="Hubungi Kami - LegalAssist",
    page_icon="📞",
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
    .info-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        height: 100%;
    }
    .info-item {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
        align-items: flex-start;
    }
    .info-icon {
        width: 48px;
        height: 48px;
        background: #e0e7ff;
        border-radius: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    .info-content h4 {
        margin: 0 0 0.25rem 0;
        color: #374151;
    }
    .info-content p {
        margin: 0;
        color: #6b7280;
    }
    .contact-form {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
    }
    .form-group {
        margin-bottom: 1rem;
    }
    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
        color: #374151;
    }
    .form-group input, .form-group textarea {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        font-family: inherit;
    }
    .form-group input:focus, .form-group textarea:focus {
        outline: none;
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    .map-placeholder {
        background: linear-gradient(135deg, #e0e7ff, #c7d2fe);
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        color: #4f46e5;
        margin-top: 1rem;
    }
    .business-hours {
        background: #f9fafb;
        border-radius: 0.75rem;
        padding: 1rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="page-header">
    <h1>📞 Hubungi Kami</h1>
    <p>Ada pertanyaan atau masukan? Kami siap membantu Anda</p>
</div>
""", unsafe_allow_html=True)

# Two column layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="info-card">
        <h3>Informasi Kontak</h3>
        
        <div class="info-item">
            <div class="info-icon">📞</div>
            <div class="info-content">
                <h4>Telepon</h4>
                <p>(021) 5678-9012</p>
                <p style="font-size: 0.75rem; color: #9ca3af;">Senin–Jumat, 08:00–17:00</p>
            </div>
        </div>
        
        <div class="info-item">
            <div class="info-icon">✉️</div>
            <div class="info-content">
                <h4>Email</h4>
                <p>info@legalassist.id</p>
                <p>support@legalassist.id</p>
            </div>
        </div>
        
        <div class="info-item">
            <div class="info-icon">📍</div>
            <div class="info-content">
                <h4>Alamat</h4>
                <p>Jl. Hukum No. 1, RT 001/RW 002</p>
                <p>Kelurahan Legal, Kecamatan Justice</p>
                <p>Jakarta Pusat, 10110</p>
            </div>
        </div>
        
        <div class="info-item">
            <div class="info-icon">🕒</div>
            <div class="info-content">
                <h4>Jam Layanan</h4>
                <p>Senin – Jumat: 08.00 – 17.00 WIB</p>
                <p>Sabtu – Minggu: Tutup</p>
                <p style="font-size: 0.75rem; color: #10b981;">Chatbot tersedia 24/7</p>
            </div>
        </div>
    </div>
    
    <div class="business-hours">
        <h4>💡 Layanan Konsultasi</h4>
        <p>Chatbot kami tersedia <strong>24 jam, 7 hari seminggu</strong> untuk konsultasi dasar.</p>
        <p style="margin-top: 0.5rem;">Untuk konsultasi mendalam, silakan hubungi advokat kami melalui direktori advokat.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    st.markdown("### Kirim Pesan")
    st.markdown("Isi form berikut untuk menghubungi tim kami.")
    
    with st.form("contact_form"):
        nama = st.text_input("Nama Lengkap", placeholder="Masukkan nama lengkap Anda")
        email = st.text_input("Email", placeholder="nama@email.com")
        subjek = st.text_input("Subjek", placeholder="Topik pesan Anda")
        pesan = st.text_area("Pesan", placeholder="Tuliskan pesan Anda di sini...", height=150)
        
        submitted = st.form_submit_button("Kirim Pesan", use_container_width=True)
        
        if submitted:
            if nama and email and subjek and pesan:
                new_pesan = {
                    "id": len(db["pesan"]) + 1,
                    "nama": nama,
                    "email": email,
                    "subjek": subjek,
                    "pesan": pesan,
                    "tanggal": datetime.now().strftime("%d %b %Y"),
                    "waktu": datetime.now().strftime("%H:%M"),
                    "status": "Belum dibaca"
                }
                db["pesan"].append(new_pesan)
                st.success("✅ Pesan berhasil dikirim! Kami akan segera menghubungi Anda.")
            else:
                st.error("Semua field harus diisi.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Map placeholder
st.markdown("---")
st.markdown("### 📍 Lokasi Kami")

st.markdown("""
<div class="map-placeholder">
    <div style="font-size: 3rem;">🗺️</div>
    <h4>Jl. Hukum No. 1, Jakarta Pusat</h4>
    <p>Google Maps akan segera tersedia</p>
</div>
""", unsafe_allow_html=True)

# Social Media
st.markdown("---")
st.markdown("### 🌐 Ikuti Kami")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 2rem;">📘</div>
        <p>Facebook</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 2rem;">📸</div>
        <p>Instagram</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 2rem;">🐦</div>
        <p>Twitter</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div style="text-align: center;">
        <div style="font-size: 2rem;">💼</div>
        <p>LinkedIn</p>
    </div>
    """, unsafe_allow_html=True)