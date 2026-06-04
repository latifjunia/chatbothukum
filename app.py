import streamlit as st
from streamlit_option_menu import option_menu
from data import db
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="LegalAssist - Konsultasi Hukum Digital",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS
st.markdown("""
<style>
    /* Main styling */
    .stApp {
        background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        padding: 3rem 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid #e5e7eb;
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
        border-color: #c7d2fe;
    }
    
    /* Stat card */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #4f46e5;
    }
    
    .stat-label {
        color: #6b7280;
        font-size: 0.875rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    
    /* Badge */
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
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid #e5e7eb;
        color: #6b7280;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/law.png", width=60)
    st.markdown("### ⚖️ LegalAssist")
    st.markdown("---")
    
    selected = option_menu(
        menu_title="Menu Utama",
        options=["Beranda", "💬 Chatbot", "👨‍⚖️ Advokat", "📚 Artikel", "❓ FAQ", "📞 Kontak", "🔒 Admin"],
        icons=["house", "chat", "people", "book", "question-circle", "envelope", "shield"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#4f46e5", "font-size": "1rem"},
            "nav-link": {"font-size": "0.9rem", "text-align": "left", "margin": "0.2rem 0"},
            "nav-link-selected": {"background-color": "#4f46e5"},
        }
    )
    
    st.markdown("---")
    st.caption("© 2025 LegalAssist")
    st.caption("Solusi Hukum Digital Terpercaya")

# ============================================================
# BERANDA PAGE
# ============================================================
if selected == "Beranda":
    # Hero Section
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ Solusi Hukum <span style="color: #fbbf24;">Ada di Sini</span></h1>
        <p>Konsultasi masalah hukum Anda dengan cepat, mudah, dan terpercaya</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{db['stats']['konsultasi']}+</div>
            <div class="stat-label">Konsultasi Selesai</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{db['stats']['advokat']}+</div>
            <div class="stat-label">Advokat Terdaftar</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{db['stats']['artikel']}+</div>
            <div class="stat-label">Artikel Hukum</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{db['stats']['pengguna']}+</div>
            <div class="stat-label">Pengguna Aktif</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Layanan
    st.markdown("## 🎯 Layanan Kami")
    st.markdown("Apa yang bisa kami bantu?")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container():
            st.markdown("""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2rem;">💬</div>
                <h3>Chatbot Konsultasi</h3>
                <p style="color: #6b7280;">Konsultasi 24/7 dengan chatbot cerdas</p>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        with st.container():
            st.markdown("""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2rem;">👨‍⚖️</div>
                <h3>Direktori Advokat</h3>
                <p style="color: #6b7280;">Temukan advokat berpengalaman</p>
            </div>
            """, unsafe_allow_html=True)
    with col3:
        with st.container():
            st.markdown("""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2rem;">📚</div>
                <h3>Artikel Hukum</h3>
                <p style="color: #6b7280;">Perluas pengetahuan hukum Anda</p>
            </div>
            """, unsafe_allow_html=True)
    with col4:
        with st.container():
            st.markdown("""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2rem;">❓</div>
                <h3>FAQ Hukum</h3>
                <p style="color: #6b7280;">Jawaban pertanyaan umum</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Artikel Terbaru
    st.markdown("## 📰 Artikel Hukum Terbaru")
    cols = st.columns(3)
    for idx, artikel in enumerate(db['artikel'][:3]):
        with cols[idx]:
            badge_class = f"badge-{artikel['kategori'].lower()}"
            st.markdown(f"""
            <div class="card">
                <span class="badge {badge_class}">{artikel['kategori']}</span>
                <h4>{artikel['judul']}</h4>
                <p style="color: #6b7280; font-size: 0.875rem;">{artikel['ringkasan'][:100]}...</p>
                <p style="color: #9ca3af; font-size: 0.75rem;">✍ {artikel['penulis']} · 📅 {artikel['tanggal']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # CTA
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e1b4b, #312e81); padding: 3rem; border-radius: 1rem; text-align: center; color: white;">
        <h2>Siap Konsultasi Sekarang?</h2>
        <p>Chatbot kami siap membantu Anda 24/7, gratis, dan tanpa perlu mendaftar.</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# CHATBOT PAGE - akan dibuat di pages/chatbot.py
# ============================================================
elif selected == "💬 Chatbot":
    from fsm import LegalFSM
    
    if "fsm" not in st.session_state:
        st.session_state.fsm = LegalFSM()
        st.session_state.messages = []
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem;">
        <h1 style="margin: 0;">💬 Konsultasi Hukum</h1>
        <p style="margin: 0.5rem 0 0 0;">Chatbot berbasis FSA untuk membantu Anda memahami masalah hukum</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant", avatar="⚖️").write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ketik nomor pilihan atau pesan..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        if prompt.lower() in ["reset", "mulai ulang", "baru"]:
            st.session_state.fsm.reset()
            response = st.session_state.fsm._menu_utama("✨ Sesi direset. Mulai konsultasi baru:")
        else:
            response = st.session_state.fsm.transition(prompt)
        
        if response["type"] == "menu":
            msg_text = f"**{response['title']}**\n\n{response['text']}\n\n"
            for opt in response["options"]:
                msg_text += f"`{opt['key']}` {opt['label']}\n"
            st.chat_message("assistant", avatar="⚖️").write(msg_text)
            st.session_state.messages.append({"role": "assistant", "content": msg_text})
        elif response["type"] == "result":
            msg_text = f"""
**📋 HASIL KONSULTASI**

**{response['title']}** ({response['pasal']})

{response['text']}

**📄 Dokumen yang diperlukan:**
{chr(10).join(['• ' + d for d in response['dokumen']])}

**👨‍⚖️ Rekomendasi:** {response['advokat']}

---
Ketik `reset` untuk konsultasi baru.
"""
            st.chat_message("assistant", avatar="⚖️").write(msg_text)
            st.session_state.messages.append({"role": "assistant", "content": msg_text})
        else:
            st.chat_message("assistant", avatar="⚖️").write(response.get("text", "Maaf, saya tidak mengerti."))
            st.session_state.messages.append({"role": "assistant", "content": response.get("text", "Maaf, saya tidak mengerti.")})

# ============================================================
# ADVOKAT PAGE
# ============================================================
elif selected == "👨‍⚖️ Advokat":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem;">
        <h1 style="margin: 0;">👨‍⚖️ Informasi Advokat</h1>
        <p style="margin: 0.5rem 0 0 0;">Temukan advokat berpengalaman dan berlisensi sesuai kebutuhan hukum Anda</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter
    spesialisasi_list = ["Semua"] + list(set([a["spesialisasi"] for a in db["advokat"]]))
    selected_spesialisasi = st.selectbox("Filter Spesialisasi", spesialisasi_list)
    
    filtered_advokat = db["advokat"] if selected_spesialisasi == "Semua" else [a for a in db["advokat"] if a["spesialisasi"] == selected_spesialisasi]
    
    for adv in filtered_advokat:
        badge_class = f"badge-{adv['spesialisasi'].lower()}"
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"""
                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #4f46e5, #7c3aed); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; font-weight: bold;">
                    {adv['nama'][0]}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <h3 style="margin: 0;">{adv['nama']}</h3>
                        <span class="badge {badge_class}">{adv['spesialisasi']}</span>
                    </div>
                    <div style="display: flex; gap: 1rem; margin: 0.5rem 0; color: #6b7280; font-size: 0.875rem;">
                        <span>📍 {adv['kota']}</span>
                        <span>⏱ {adv['pengalaman']}</span>
                        <span>⭐ {adv['rating']}</span>
                        <span>📁 {adv['kasus']} kasus</span>
                    </div>
                    <div style="display: flex; gap: 1rem;">
                        <a href="tel:{adv['telepon']}" style="text-decoration: none;">
                            <code>📞 {adv['telepon']}</code>
                        </a>
                        <a href="mailto:{adv['email']}" style="text-decoration: none;">
                            <code>✉️ {adv['email']}</code>
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# ARTIKEL PAGE
# ============================================================
elif selected == "📚 Artikel":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem;">
        <h1 style="margin: 0;">📚 Artikel Hukum</h1>
        <p style="margin: 0.5rem 0 0 0;">Perluas pengetahuan hukum Anda melalui artikel informatif dari para ahli</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter
    kategori_list = ["Semua"] + list(set([a["kategori"] for a in db["artikel"]]))
    selected_kategori = st.selectbox("Filter Kategori", kategori_list)
    
    filtered_artikel = db["artikel"] if selected_kategori == "Semua" else [a for a in db["artikel"] if a["kategori"] == selected_kategori]
    
    for artikel in filtered_artikel:
        badge_class = f"badge-{artikel['kategori'].lower()}"
        with st.expander(f"📄 {artikel['judul']}"):
            st.markdown(f"""
            <div>
                <span class="badge {badge_class}">{artikel['kategori']}</span>
                <p style="color: #6b7280; margin: 0.5rem 0;">✍ {artikel['penulis']} · 📅 {artikel['tanggal']} · 👁 {artikel['baca']} dibaca</p>
                <p>{artikel['isi']}</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# FAQ PAGE
# ============================================================
elif selected == "❓ FAQ":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem;">
        <h1 style="margin: 0;">❓ Pertanyaan Umum (FAQ)</h1>
        <p style="margin: 0.5rem 0 0 0;">Temukan jawaban dari pertanyaan yang paling sering ditanyakan</p>
    </div>
    """, unsafe_allow_html=True)
    
    for faq in db["faq"]:
        with st.expander(f"📌 {faq['pertanyaan']}"):
            st.markdown(f"<p>{faq['jawaban']}</p>", unsafe_allow_html=True)
            st.caption(f"Kategori: {faq['kategori']}")

# ============================================================
# KONTAK PAGE
# ============================================================
elif selected == "📞 Kontak":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem;">
        <h1 style="margin: 0;">📞 Hubungi Kami</h1>
        <p style="margin: 0.5rem 0 0 0;">Ada pertanyaan atau masukan? Kami siap membantu Anda</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 1rem; border: 1px solid #e5e7eb;">
            <h3>Informasi Kontak</h3>
            <p><strong>📞 Telepon:</strong> (021) 5678-9012</p>
            <p><strong>✉️ Email:</strong> info@legalassist.id</p>
            <p><strong>📍 Alamat:</strong> Jl. Hukum No. 1, Jakarta Pusat</p>
            <p><strong>🕒 Jam Layanan:</strong> Senin–Jumat, 08:00–17:00</p>
            <hr>
            <p><strong>💬 Chatbot</strong> tersedia 24/7 untuk konsultasi dasar.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("kontak_form"):
            st.markdown("<h3>Kirim Pesan</h3>", unsafe_allow_html=True)
            nama = st.text_input("Nama Lengkap")
            email = st.text_input("Email")
            subjek = st.text_input("Subjek")
            pesan = st.text_area("Pesan", height=150)
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
                        "status": "Belum dibaca"
                    }
                    db["pesan"].append(new_pesan)
                    st.success("✅ Pesan berhasil dikirim! Kami akan segera menghubungi Anda.")
                else:
                    st.error("Semua field harus diisi.")

# ============================================================
# ADMIN PAGE
# ============================================================
elif selected == "🔒 Admin":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem;">
        <h1 style="margin: 0;">🔒 Panel Admin</h1>
        <p style="margin: 0.5rem 0 0 0;">Kelola advokat, artikel, FAQ, dan pesan</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.admin_logged_in:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                if username == db["admin"]["username"] and password == db["admin"]["password"]:
                    st.session_state.admin_logged_in = True
                    st.success("Login berhasil!")
                    st.rerun()
                else:
                    st.error("Username atau password salah.")
    else:
        st.success(f"Selamat datang, Admin!")
        
        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👨‍⚖️ Advokat", "📚 Artikel", "❓ FAQ"])
        
        with tab1:
            st.markdown("### Statistik")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Konsultasi", db["stats"]["konsultasi"])
            with col2:
                st.metric("Total Advokat", db["stats"]["advokat"])
            with col3:
                st.metric("Total Artikel", db["stats"]["artikel"])
            with col4:
                st.metric("Total Pengguna", db["stats"]["pengguna"])
            
            st.markdown("### Pesan Masuk")
            for p in db["pesan"][::-1]:
                with st.expander(f"📧 {p['subjek']} - {p['nama']} ({p['tanggal']})"):
                    st.write(f"**Email:** {p['email']}")
                    st.write(f"**Pesan:** {p['pesan']}")
                    st.caption(f"Status: {p['status']}")
        
        with tab2:
            st.markdown("### Daftar Advokat")
            for adv in db["advokat"]:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{adv['nama']}** - {adv['spesialisasi']} - {adv['kota']}")
                with col2:
                    if st.button(f"Hapus", key=f"del_adv_{adv['id']}"):
                        db["advokat"] = [a for a in db["advokat"] if a["id"] != adv["id"]]
                        st.rerun()
            
            st.markdown("---")
            st.markdown("### Tambah Advokat")
            with st.form("tambah_advokat"):
                nama = st.text_input("Nama")
                spesialisasi = st.selectbox("Spesialisasi", ["Pidana", "Perdata", "Keluarga", "Ketenagakerjaan"])
                pengalaman = st.text_input("Pengalaman (contoh: 10 Tahun)")
                kota = st.text_input("Kota")
                telepon = st.text_input("Telepon")
                email = st.text_input("Email")
                
                if st.form_submit_button("Tambah Advokat"):
                    baru = {
                        "id": len(db["advokat"]) + 1,
                        "nama": nama,
                        "spesialisasi": spesialisasi,
                        "pengalaman": pengalaman,
                        "kota": kota,
                        "telepon": telepon,
                        "email": email,
                        "rating": 5.0,
                        "kasus": 0
                    }
                    db["advokat"].append(baru)
                    st.success("Advokat berhasil ditambahkan!")
                    st.rerun()
        
        with tab3:
            st.markdown("### Daftar Artikel")
            for art in db["artikel"]:
                with st.expander(f"📄 {art['judul']} - {art['kategori']}"):
                    st.write(f"**Penulis:** {art['penulis']}")
                    st.write(f"**Tanggal:** {art['tanggal']}")
                    st.write(f"**Isi:** {art['isi'][:200]}...")
                    if st.button(f"Hapus", key=f"del_art_{art['id']}"):
                        db["artikel"] = [a for a in db["artikel"] if a["id"] != art["id"]]
                        st.rerun()
            
            st.markdown("---")
            st.markdown("### Tambah Artikel")
            with st.form("tambah_artikel"):
                judul = st.text_input("Judul")
                kategori = st.selectbox("Kategori", ["Pidana", "Perdata", "Keluarga", "Ketenagakerjaan"])
                isi = st.text_area("Isi Artikel", height=200)
                
                if st.form_submit_button("Tambah Artikel"):
                    baru = {
                        "id": len(db["artikel"]) + 1,
                        "judul": judul,
                        "kategori": kategori,
                        "isi": isi,
                        "ringkasan": isi[:150] + "...",
                        "tanggal": datetime.now().strftime("%d %b %Y"),
                        "penulis": "Admin",
                        "baca": 0
                    }
                    db["artikel"].append(baru)
                    st.success("Artikel berhasil ditambahkan!")
                    st.rerun()
        
        with tab4:
            st.markdown("### Daftar FAQ")
            for faq in db["faq"]:
                with st.expander(f"❓ {faq['pertanyaan']}"):
                    st.write(f"**Jawaban:** {faq['jawaban']}")
                    st.write(f"**Kategori:** {faq['kategori']}")
                    if st.button(f"Hapus", key=f"del_faq_{faq['id']}"):
                        db["faq"] = [f for f in db["faq"] if f["id"] != faq["id"]]
                        st.rerun()
            
            st.markdown("---")
            st.markdown("### Tambah FAQ")
            with st.form("tambah_faq"):
                pertanyaan = st.text_input("Pertanyaan")
                jawaban = st.text_area("Jawaban")
                kategori = st.text_input("Kategori", value="Umum")
                
                if st.form_submit_button("Tambah FAQ"):
                    baru = {
                        "id": len(db["faq"]) + 1,
                        "pertanyaan": pertanyaan,
                        "jawaban": jawaban,
                        "kategori": kategori
                    }
                    db["faq"].append(baru)
                    st.success("FAQ berhasil ditambahkan!")
                    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 LegalAssist — Layanan Konsultasi Advokat Berbasis Web</p>
    <p style="font-size: 0.75rem;">Informasi bersifat edukatif, bukan nasihat hukum resmi.</p>
</div>
""", unsafe_allow_html=True)