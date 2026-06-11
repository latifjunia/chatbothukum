import streamlit as st
from streamlit_option_menu import option_menu
from data import db
from datetime import datetime
from fsm import LegalFSM, ARTIKEL_LINK

# Page configuration
st.set_page_config(
    page_title="LegalAssist - Konsultasi Hukum Digital",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="auto"
)

# Fungsi untuk mencari artikel berdasarkan kata kunci
def cari_artikel_by_keyword(keyword):
    """Mencari artikel berdasarkan kata kunci yang diketik user"""
    keyword_lower = keyword.lower()
    mapping_keyword = {
        # KDRT dan Kekerasan
        "pelecehan": 5, "kekerasan seksual": 5, "tpks": 5,
        "kdrt": 3, "kekerasan rumah tangga": 3,
        
        # Penipuan
        "penipuan": 2, "penipuan online": 2, "belanja online": 2,
        
        # PHK
        "phk": 4, "dipecat": 4, "pesangon": 4,
        
        # Lowongan kerja palsu
        "loker palsu": 6, "tipu loker": 6, "lowongan kerja": 6,
        
        # Pencemaran nama baik
        "pencemaran nama baik": 7, "dihina": 7, "ite": 7,
        
        # Tanah
        "tanah": 8, "sengketa tanah": 8, "warisan": 8,
        
        # Pinjol
        "pinjol": 1, "pinjaman online": 1,
        
        # Pencurian
        "pencurian": 9, "dicuri": 9, "maling": 9,
        
        # Perceraian
        "perceraian": 10, "cerai": 10,
    }
    
    for kata, artikel_id in mapping_keyword.items():
        if kata in keyword_lower:
            for artikel in db["artikel"]:
                if artikel["id"] == artikel_id:
                    return artikel
    return None

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
    
    /* Chat message styling */
    .chat-message-user {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 1rem 1rem 0.25rem 1rem;
        margin: 0.5rem 0;
    }
    
    .chat-message-bot {
        background: #f3f4f6;
        color: #1f2937;
        padding: 0.75rem 1rem;
        border-radius: 0.25rem 1rem 1rem 1rem;
        margin: 0.5rem 0;
    }
    
    /* Article card */
    .article-card {
        border: 1px solid #e5e7eb;
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 1rem;
        background: white;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .article-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "fsm" not in st.session_state:
    st.session_state.fsm = LegalFSM()
    st.session_state.messages = []
if "selected_article" not in st.session_state:
    st.session_state.selected_article = None
if "selected_faq_category" not in st.session_state:
    st.session_state.selected_faq_category = "Semua"
if "chatbot_selected_article" not in st.session_state:
    st.session_state.chatbot_selected_article = None
if "show_article_list" not in st.session_state:
    st.session_state.show_article_list = False

# Sidebar Navigation
with st.sidebar:
    st.markdown("### ⚖️ LegalAssist")
    st.markdown("---")
    
    selected = option_menu(
        menu_title="Menu Utama",
        options=["Beranda", "Chatbot", "Advokat", "Artikel", "FAQ", "Kontak", "Admin"],
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
    st.caption("© 2026 LegalAssist")
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
    
    # Stats (DIHAPUS TANDA +)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{db['stats']['konsultasi']}</div>
            <div class="stat-label">Konsultasi Selesai</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{db['stats']['advokat']}</div>
            <div class="stat-label">Advokat Terdaftar</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{db['stats']['artikel']}</div>
            <div class="stat-label">Artikel Hukum</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{db['stats']['pengguna']}</div>
            <div class="stat-label">Kasus Tertangani</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Layanan
    st.markdown("## 🎯 Layanan Kami")
    st.markdown("Apa yang bisa kami bantu?")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem;">💬</div>
            <h3>Chatbot Konsultasi</h3>
            <p style="color: #6b7280;">Konsultasi 24/7 dengan chatbot cerdas</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem;">👨‍⚖️</div>
            <h3>Direktori Advokat</h3>
            <p style="color: #6b7280;">Temukan advokat berpengalaman</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div style="font-size: 2rem;">📚</div>
            <h3>Artikel Hukum</h3>
            <p style="color: #6b7280;">Perluas pengetahuan hukum Anda</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
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
# CHATBOT PAGE
# ============================================================
elif selected == "Chatbot":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); padding: 2rem; border-radius: 3rem; color: white; margin-bottom: 2rem;">
        <h1 style="margin: 0;">💬 Konsultasi Hukum</h1>
        <p style="margin: 0.5rem 0 0 0;">Chatbot untuk membantu Anda memahami masalah hukum</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cek apakah sedang menampilkan artikel dari chatbot
    if st.session_state.get("chatbot_selected_article"):
        artikel = st.session_state.chatbot_selected_article
        
        # Tombol kembali
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Kembali ke Chatbot", key="back_from_article"):
                st.session_state.chatbot_selected_article = None
                st.rerun()
        with col2:
            if st.button("📚 Daftar Artikel", key="list_from_article"):
                st.session_state.chatbot_selected_article = None
                st.session_state.show_article_list = True
                st.rerun()
        
        # Tampilkan artikel lengkap
        badge_class = f"badge-{artikel['kategori'].lower()}"
        st.markdown(f"""
        <div style="background: white; border-radius: 1rem; padding: 2rem; border: 1px solid #e5e7eb; margin-top: 1rem;">
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
    
    elif st.session_state.get("show_article_list"):
        # Tampilkan daftar artikel yang bisa dibaca
        st.markdown("## 📚 Daftar Artikel Hukum")
        st.markdown("Pilih artikel yang ingin Anda baca:")
        
        # Tombol kembali ke chatbot
        if st.button("← Kembali ke Chatbot", key="back_from_list"):
            st.session_state.show_article_list = False
            st.rerun()
        
        st.markdown("---")
        
        # Filter kategori artikel
        kategori_list = ["Semua"] + sorted(list(set([a["kategori"] for a in db["artikel"]])))
        selected_kategori = st.selectbox("Filter Kategori", kategori_list, key="chatbot_article_filter")
        
        filtered_artikel = db["artikel"] if selected_kategori == "Semua" else [a for a in db["artikel"] if a["kategori"] == selected_kategori]
        
        st.markdown(f"<p style='color: #6b7280; margin-bottom: 1rem;'>Menampilkan {len(filtered_artikel)} artikel</p>", unsafe_allow_html=True)
        
        # Tampilkan artikel dalam bentuk list
        for idx, artikel in enumerate(filtered_artikel):
            badge_class = f"badge-{artikel['kategori'].lower()}"
            with st.container():
                st.markdown(f"""
                <div style="border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 1rem; margin-bottom: 1rem; background: white;">
                    <span class="badge {badge_class}">{artikel['kategori']}</span>
                    <h4 style="margin: 0.5rem 0;">{artikel['judul']}</h4>
                    <p style="color: #6b7280; font-size: 0.875rem; margin: 0.5rem 0;">{artikel['ringkasan']}</p>
                    <p style="color: #9ca3af; font-size: 0.75rem;">✍ {artikel['penulis']} · 📅 {artikel['tanggal']} · 👁 {artikel['baca']} dibaca</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"📖 Baca Selengkapnya", key=f"read_artikel_{artikel['id']}_{idx}"):
                    st.session_state.chatbot_selected_article = artikel
                    st.session_state.show_article_list = False
                    st.rerun()
        
        st.markdown("---")
        if st.button("← Kembali ke Chatbot", key="back_from_list_bottom", use_container_width=True):
            st.session_state.show_article_list = False
            st.rerun()
    
    else:
        # Sidebar info untuk chatbot
        with st.sidebar:
            st.markdown("### ℹ️ Informasi Chatbot")
            st.markdown("---")
            st.markdown("#### 📋 Kategori Tersedia")
            st.markdown("""
            - ⚖️ **Pidana** (Penipuan, Pencurian)
            - 📋 **Perdata** (Hutang, Wanprestasi)
            - 👨‍👩‍👧 **Keluarga** (Perceraian, Hak Asuh)
            - 💼 **Ketenagakerjaan** (PHK, Perselisihan)
            """)
            st.markdown("---")
            st.markdown("#### 📚 Baca Artikel")
            st.markdown("""
            **Contoh perintah:**
            - `baca artikel pelecehan`
            - `artikel KDRT`
            - `baca artikel penipuan online`
            - `artikel PHK`
            """)
            if st.button("📖 Baca Artikel Hukum", use_container_width=True, key="sidebar_article_btn"):
                st.session_state.show_article_list = True
                st.rerun()
            st.markdown("---")
            st.markdown("#### 📌 Cara Penggunaan")
            st.markdown("""
            1. Ceritakan masalah hukum Anda
            2. Jawab pertanyaan chatbot
            3. Terima hasil & rekomendasi
            """)
            st.markdown("---")
            if st.button("🔄 Mulai Ulang Konsultasi", use_container_width=True):
                st.session_state.fsm.reset()
                st.session_state.messages = []
                st.rerun()
        
        st.markdown("---")
        
        # Display chat history
        for idx, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant", avatar="⚖️"):
                    st.write(msg["content"])
                    
                    # Jika ada tombol artikel di pesan, tampilkan
                    if "artikel_link" in msg and msg["artikel_link"]:
                        if msg["artikel_link"] in ARTIKEL_LINK:
                            artikel_info = ARTIKEL_LINK[msg["artikel_link"]]
                            for artikel in db["artikel"]:
                                if artikel["id"] == artikel_info["id"]:
                                    if st.button(f"📖 Baca Artikel: {artikel['judul']}", key=f"btn_artikel_{artikel['id']}_{idx}"):
                                        st.session_state.chatbot_selected_article = artikel
                                        st.rerun()
                                    break
        
        # Chat input
        prompt = st.chat_input("Ceritakan masalah hukum anda... Atau ketik 'baca artikel [topik]' untuk membaca artikel")
        
        if prompt:
            # CEK PERINTAH BACA ARTIKEL DENGAN KATA KUNCI TERTENTU
            if prompt.lower().startswith("baca artikel") or prompt.lower().startswith("artikel"):
                # Ekstrak kata kunci setelah "baca artikel" atau "artikel"
                kata_kunci = prompt.lower().replace("baca artikel", "").replace("artikel", "").strip()
                
                if kata_kunci:
                    # Cari artikel berdasarkan kata kunci
                    artikel_ditemukan = cari_artikel_by_keyword(kata_kunci)
                    
                    if artikel_ditemukan:
                        # Tambahkan pesan user ke history
                        with st.chat_message("user"):
                            st.write(prompt)
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        
                        # Tampilkan artikel
                        st.session_state.chatbot_selected_article = artikel_ditemukan
                        st.rerun()
                    else:
                        # Jika tidak ditemukan, beri respons
                        with st.chat_message("user"):
                            st.write(prompt)
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        
                        with st.chat_message("assistant", avatar="⚖️"):
                            st.write(f"Maaf, saya tidak menemukan artikel tentang '{kata_kunci}'. Berikut topik artikel yang tersedia:\n\n"
                                    f"- pelecehan / kekerasan seksual\n"
                                    f"- KDRT / kekerasan rumah tangga\n"
                                    f"- penipuan online\n"
                                    f"- PHK / pesangon\n"
                                    f"- tipu lowongan kerja\n"
                                    f"- pencemaran nama baik / ITE\n"
                                    f"- sengketa tanah / warisan\n"
                                    f"- pinjol ilegal\n"
                                    f"- pencurian\n"
                                    f"- perceraian\n\n"
                                    f"Ketik `baca artikel [topik]` dengan topik yang sesuai.")
                        
                        st.session_state.messages.append({"role": "assistant", "content": f"Maaf, saya tidak menemukan artikel tentang '{kata_kunci}'."})
                else:
                    # Jika hanya "baca artikel" tanpa kata kunci
                    with st.chat_message("user"):
                        st.write(prompt)
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    
                    with st.chat_message("assistant", avatar="⚖️"):
                        st.write("Silakan tentukan topik artikel yang ingin Anda baca. Contoh:\n\n"
                                f"- `baca artikel pelecehan`\n"
                                f"- `baca artikel KDRT`\n"
                                f"- `baca artikel penipuan online`\n"
                                f"- `baca artikel PHK`\n\n"
                                f"Atau ketik `menu` untuk konsultasi hukum.")
                    
                    st.session_state.messages.append({"role": "assistant", "content": "Silakan tentukan topik artikel yang ingin dibaca."})
            
            # PROSES KONSULTASI NORMAL
            else:
                # Add user message
                with st.chat_message("user"):
                    st.write(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Process response
                if prompt.lower() in ["reset", "mulai ulang", "baru"]:
                    st.session_state.fsm.reset()
                    response = st.session_state.fsm._menu_utama("✨ Sesi direset. Mulai konsultasi baru:")
                else:
                    response = st.session_state.fsm.transition(prompt)
                
                # Format and add bot response
                if response["type"] == "menu":
                    msg_text = f"**{response['title']}**\n\n{response['text']}\n\n"
                    for opt in response["options"]:
                        msg_text += f"`{opt['key']}` {opt['label']}\n"
                    
                    msg_data = {"role": "assistant", "content": msg_text}
                    with st.chat_message("assistant", avatar="⚖️"):
                        st.write(msg_text)
                        st.markdown("---")
                        st.caption("💡 *Ketik 'baca artikel [topik]' untuk membaca artikel. Contoh: baca artikel pelecehan*")
                    st.session_state.messages.append(msg_data)
                    
                elif response["type"] == "result":
                    msg_text = f"""
**📋 HASIL KONSULTASI**

**{response['title']}** ({response['pasal']})

{response['text']}

**📄 Dokumen yang diperlukan:**
"""
                    for d in response['dokumen']:
                        msg_text += f"• {d}\n"
                    
                    msg_text += f"""
**👨‍⚖️ Rekomendasi:** {response['advokat']}

---
Ketik `reset` untuk konsultasi baru.
"""
                    # Tambahkan link artikel jika ada
                    msg_data = {"role": "assistant", "content": msg_text}
                    if "artikel" in response and response["artikel"]:
                        msg_data["artikel_link"] = response["artikel"]["id"]
                        msg_text += f"\n\n📖 **Baca artikel selengkapnya dengan klik tombol di bawah ini!**"
                        msg_data["content"] = msg_text
                    
                    with st.chat_message("assistant", avatar="⚖️"):
                        st.write(msg_text)
                        if "artikel" in response and response["artikel"]:
                            artikel_info = response["artikel"]
                            for artikel in db["artikel"]:
                                if artikel["id"] == artikel_info["id"]:
                                    if st.button(f"📖 Baca Artikel: {artikel['judul']}", key=f"btn_artikel_{artikel['id']}_{len(st.session_state.messages)}"):
                                        st.session_state.chatbot_selected_article = artikel
                                        st.rerun()
                                    break
                        st.markdown("---")
                        st.caption("💡 *Ketik 'baca artikel [topik]' untuk membaca artikel lain. Contoh: baca artikel KDRT*")
                    
                    st.session_state.messages.append(msg_data)
                    
                else:
                    with st.chat_message("assistant", avatar="⚖️"):
                        st.write(response.get("text", "Maaf, saya tidak mengerti. Silakan coba lagi."))
                        st.markdown("---")
                        st.caption("💡 *Ketik 'baca artikel [topik]' untuk membaca artikel. Contoh: baca artikel pelecehan*")
                    st.session_state.messages.append({"role": "assistant", "content": response.get("text", "Maaf, saya tidak mengerti.")})

# ============================================================
# ADVOKAT PAGE
# ============================================================
elif selected == "Advokat":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem;">
        <h1 style="margin: 0;">👨‍⚖️ Informasi Advokat</h1>
        <p style="margin: 0.5rem 0 0 0;">Temukan advokat berpengalaman dan berlisensi sesuai kebutuhan hukum Anda</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter
    spesialisasi_list = ["Semua"] + sorted(list(set([a["spesialisasi"] for a in db["advokat"]])))
    selected_spesialisasi = st.selectbox("Filter Spesialisasi", spesialisasi_list)
    
    filtered_advokat = db["advokat"] if selected_spesialisasi == "Semua" else [a for a in db["advokat"] if a["spesialisasi"] == selected_spesialisasi]
    
    st.markdown(f"<p style='color: #6b7280; margin-bottom: 1rem;'>Menampilkan {len(filtered_advokat)} advokat</p>", unsafe_allow_html=True)
    
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
                <div style="border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 1rem; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <h3 style="margin: 0;">{adv['nama']}</h3>
                        <span class="badge {badge_class}">{adv['spesialisasi']}</span>
                    </div>
                    <div style="display: flex; gap: 1rem; margin: 0.5rem 0; color: #6b7280; font-size: 0.875rem; flex-wrap: wrap;">
                        <span>📍 {adv['kota']}</span>
                        <span>⏱ {adv['pengalaman']}</span>
                        <span>⭐ {adv['rating']}</span>
                        <span>📁 {adv['kasus']} kasus</span>
                    </div>
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                        <code>📞 {adv['telepon']}</code>
                        <code>✉️ {adv['email']}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# ARTIKEL PAGE
# ============================================================
elif selected == "Artikel":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem;">
        <h1 style="margin: 0;">📚 Artikel Hukum</h1>
        <p style="margin: 0.5rem 0 0 0;">Perluas pengetahuan hukum Anda melalui artikel informatif dari para ahli</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.selected_article is None:
        # Filter
        kategori_list = ["Semua"] + sorted(list(set([a["kategori"] for a in db["artikel"]])))
        selected_kategori = st.selectbox("Filter Kategori", kategori_list)
        
        filtered_artikel = db["artikel"] if selected_kategori == "Semua" else [a for a in db["artikel"] if a["kategori"] == selected_kategori]
        
        st.markdown(f"<p style='color: #6b7280; margin-bottom: 1rem;'>Menampilkan {len(filtered_artikel)} artikel</p>", unsafe_allow_html=True)
        
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
    else:
        # Show article detail
        artikel = st.session_state.selected_article
        
        if st.button("← Kembali ke Daftar Artikel"):
            st.session_state.selected_article = None
            st.rerun()
        
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

# ============================================================
# FAQ PAGE
# ============================================================
elif selected == "FAQ":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem;">
        <h1 style="margin: 0;">❓ Pertanyaan Umum (FAQ)</h1>
        <p style="margin: 0.5rem 0 0 0;">Temukan jawaban dari pertanyaan yang paling sering ditanyakan</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Category filter
    kategori_list = ["Semua"] + sorted(list(set([f["kategori"] for f in db["faq"]])))
    cols = st.columns(len(kategori_list))
    for idx, kat in enumerate(kategori_list):
        with cols[idx]:
            if st.button(kat, key=f"faq_cat_{kat}", use_container_width=True):
                st.session_state.selected_faq_category = kat
                st.rerun()
    
    filtered_faq = db["faq"] if st.session_state.selected_faq_category == "Semua" else [f for f in db["faq"] if f["kategori"] == st.session_state.selected_faq_category]
    
    st.markdown(f"<p style='color: #6b7280; margin-bottom: 1rem;'>Menampilkan {len(filtered_faq)} pertanyaan</p>", unsafe_allow_html=True)
    
    for faq in filtered_faq:
        with st.expander(f"📌 {faq['pertanyaan']}"):
            st.markdown(f"<p>{faq['jawaban']}</p>", unsafe_allow_html=True)
            st.caption(f"Kategori: {faq['kategori']}")

# ============================================================
# KONTAK PAGE
# ============================================================
elif selected == "Kontak":
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
elif selected == "Admin":
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
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if username == db["admin"]["username"] and password == db["admin"]["password"]:
                    st.session_state.admin_logged_in = True
                    st.success("Login berhasil!")
                    st.rerun()
                else:
                    st.error("Username atau password salah.")
    else:
        st.success("Selamat datang, Admin!")
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("Logout", use_container_width=True):
                st.session_state.admin_logged_in = False
                st.rerun()
        
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👨‍⚖️ Advokat", "📚 Artikel", "❓ FAQ"])
        
        with tab1:
            st.markdown("### Statistik")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Konsultasi", db["stats"]["konsultasi"])
            with col2:
                st.metric("Total Advokat", len(db["advokat"]))
            with col3:
                st.metric("Total Artikel", len(db["artikel"]))
            with col4:
                st.metric("Total Pengguna", db["stats"]["pengguna"])
            
            st.markdown("### Pesan Masuk")
            pesan_list = db["pesan"][::-1]
            if pesan_list:
                for p in pesan_list:
                    with st.expander(f"📧 {p['subjek']} - {p['nama']} ({p['tanggal']})"):
                        st.write(f"**Email:** {p['email']}")
                        st.write(f"**Pesan:** {p['pesan']}")
                        st.caption(f"Status: {p['status']}")
            else:
                st.info("Belum ada pesan masuk.")
        
        with tab2:
            st.markdown("### Daftar Advokat")
            for adv in db["advokat"]:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{adv['nama']}** - {adv['spesialisasi']} - {adv['kota']}")
                with col2:
                    if st.button("Hapus", key=f"del_adv_{adv['id']}"):
                        db["advokat"] = [a for a in db["advokat"] if a["id"] != adv["id"]]
                        st.rerun()
            
            st.markdown("---")
            st.markdown("### Tambah Advokat")
            with st.form("tambah_advokat"):
                col1, col2 = st.columns(2)
                with col1:
                    nama = st.text_input("Nama")
                    spesialisasi = st.selectbox("Spesialisasi", ["Pidana", "Perdata", "Keluarga", "Ketenagakerjaan"])
                    pengalaman = st.text_input("Pengalaman (contoh: 10 Tahun)")
                with col2:
                    kota = st.text_input("Kota")
                    telepon = st.text_input("Telepon")
                    email = st.text_input("Email")
                
                if st.form_submit_button("Tambah Advokat", use_container_width=True):
                    if nama and telepon and email:
                        baru = {
                            "id": len(db["advokat"]) + 1,
                            "nama": nama,
                            "spesialisasi": spesialisasi,
                            "pengalaman": pengalaman or "Baru",
                            "kota": kota or "Jakarta",
                            "telepon": telepon,
                            "email": email,
                            "rating": 5.0,
                            "kasus": 0
                        }
                        db["advokat"].append(baru)
                        st.success("Advokat berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("Nama, Telepon, dan Email wajib diisi.")
        
        with tab3:
            st.markdown("### Daftar Artikel")
            for art in db["artikel"]:
                with st.expander(f"📄 {art['judul']} - {art['kategori']}"):
                    st.write(f"**Penulis:** {art['penulis']}")
                    st.write(f"**Tanggal:** {art['tanggal']}")
                    st.write(f"**Isi:** {art['isi'][:200]}...")
                    if st.button("Hapus", key=f"del_art_{art['id']}"):
                        db["artikel"] = [a for a in db["artikel"] if a["id"] != art["id"]]
                        st.rerun()
            
            st.markdown("---")
            st.markdown("### Tambah Artikel")
            with st.form("tambah_artikel"):
                judul = st.text_input("Judul")
                kategori = st.selectbox("Kategori", ["Pidana", "Perdata", "Keluarga", "Ketenagakerjaan"])
                isi = st.text_area("Isi Artikel", height=200)
                
                if st.form_submit_button("Tambah Artikel", use_container_width=True):
                    if judul and isi:
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
                    else:
                        st.error("Judul dan Isi Artikel wajib diisi.")
        
        with tab4:
            st.markdown("### Daftar FAQ")
            for faq in db["faq"]:
                with st.expander(f"❓ {faq['pertanyaan']}"):
                    st.write(f"**Jawaban:** {faq['jawaban']}")
                    st.write(f"**Kategori:** {faq['kategori']}")
                    if st.button("Hapus", key=f"del_faq_{faq['id']}"):
                        db["faq"] = [f for f in db["faq"] if f["id"] != faq["id"]]
                        st.rerun()
            
            st.markdown("---")
            st.markdown("### Tambah FAQ")
            with st.form("tambah_faq"):
                pertanyaan = st.text_input("Pertanyaan")
                jawaban = st.text_area("Jawaban", height=100)
                kategori = st.text_input("Kategori", value="Umum")
                
                if st.form_submit_button("Tambah FAQ", use_container_width=True):
                    if pertanyaan and jawaban:
                        baru = {
                            "id": len(db["faq"]) + 1,
                            "pertanyaan": pertanyaan,
                            "jawaban": jawaban,
                            "kategori": kategori
                        }
                        db["faq"].append(baru)
                        st.success("FAQ berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("Pertanyaan dan Jawaban wajib diisi.")

