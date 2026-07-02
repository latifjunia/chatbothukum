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

# Custom CSS - Enhanced Professional Design
st.markdown("""
<style>
    /* Reset and base styles */
    .main {
        padding: 0rem 1rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Enhanced Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 50%, #1e293b 100%);
        padding: 3.5rem 2.5rem;
        border-radius: 1.5rem;
        color: white;
        margin-bottom: 2.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
        transform: rotate(45deg);
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        margin-bottom: 0.75rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
        font-weight: 300;
    }
    
    .main-header .highlight {
        color: #818cf8;
        font-weight: 600;
    }
    
    /* Enhanced Card styling */
    .card {
        background: white;
        padding: 1.75rem;
        border-radius: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(226, 232, 240, 0.8);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #a78bfa);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
        border-color: #c7d2fe;
    }
    
    .card:hover::before {
        opacity: 1;
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        display: inline-block;
    }
    
    .card h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0.5rem 0;
    }
    
    .card p {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Enhanced Stat card */
    .stat-card {
        background: white;
        padding: 1.75rem 1.5rem;
        border-radius: 1.25rem;
        text-align: center;
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        border-color: #c7d2fe;
    }
    
    .stat-card:hover::after {
        opacity: 1;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }
    
    /* Enhanced Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.6rem 1.25rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.2);
        letter-spacing: 0.025em;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Enhanced Badge */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.025em;
        text-transform: uppercase;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .badge-pidana { 
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        color: #dc2626; 
    }
    
    .badge-perdata { 
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        color: #2563eb; 
    }
    
    .badge-keluarga { 
        background: linear-gradient(135deg, #faf5ff, #f3e8ff);
        color: #7c3aed; 
    }
    
    .badge-ketenagakerjaan { 
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
        color: #d97706; 
    }
    
    /* Enhanced Chat message styling */
    .chat-message-user {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        padding: 0.75rem 1.25rem;
        border-radius: 1.25rem 1.25rem 0.25rem 1.25rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.2);
        max-width: 80%;
        margin-left: auto;
    }
    
    .chat-message-bot {
        background: white;
        color: #1e293b;
        padding: 0.75rem 1.25rem;
        border-radius: 0.25rem 1.25rem 1.25rem 1.25rem;
        margin: 0.5rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        max-width: 80%;
    }
    
    /* Enhanced Article card */
    .article-card {
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        background: white;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    
    .article-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
        border-color: #c7d2fe;
    }
    
    /* Enhanced Footer */
    .footer {
        text-align: center;
        padding: 2.5rem;
        margin-top: 4rem;
        border-top: 1px solid #e2e8f0;
        color: #94a3b8;
        background: white;
        border-radius: 1rem;
    }
    
    /* Enhanced Sidebar */
    .css-1d391kg {
        background: white;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Container styling */
    .section-title {
        font-size: 1.875rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5rem;
        letter-spacing: -0.025em;
    }
    
    .section-subtitle {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* CTA Box */
    .cta-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 50%, #1e293b 100%);
        padding: 3.5rem;
        border-radius: 1.5rem;
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.2);
    }
    
    .cta-box::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
        transform: rotate(45deg);
    }
    
    .cta-box h2 {
        font-size: 2.25rem;
        margin-bottom: 0.75rem;
        position: relative;
        z-index: 1;
    }
    
    .cta-box p {
        font-size: 1.1rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 2.5rem 0;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 0.75rem !important;
        border: 1px solid #e2e8f0;
        font-weight: 500;
        color: #1e293b;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #c7d2fe;
        background: #f8fafc;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.75rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        background: transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f1f5f9;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white !important;
    }
    
    /* Info box styling */
    .info-box {
        background: #f8fafc;
        border-left: 4px solid #6366f1;
        padding: 1.25rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .stat-number {
            font-size: 2rem;
        }
        
        .card {
            padding: 1.25rem;
        }
        
        .cta-box {
            padding: 2rem 1.5rem;
        }
        
        .cta-box h2 {
            font-size: 1.75rem;
        }
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

# Sidebar Navigation - Enhanced
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
        <div style="font-size: 2.5rem;">⚖️</div>
        <h2 style="color: #1e293b; margin: 0; font-weight: 700;">LegalAssist</h2>
        <p style="color: #64748b; font-size: 0.8rem; margin: 0;">Solusi Hukum Digital</p>
    </div>
    <hr style="border-color: #e2e8f0; margin: 1rem 0;">
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Beranda", "Chatbot", "Advokat", "Artikel", "FAQ", "Kontak", "Admin"],
        icons=["house-fill", "chat-dots-fill", "people-fill", "book-fill", "question-circle-fill", "envelope-fill", "shield-lock-fill"],
        menu_icon=None,
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#6366f1", "font-size": "1.1rem", "margin-right": "0.75rem"},
            "nav-link": {
                "font-size": "0.95rem", 
                "text-align": "left", 
                "margin": "0.25rem 0",
                "padding": "0.6rem 1rem",
                "border-radius": "0.75rem",
                "color": "#475569",
                "font-weight": "500",
                "transition": "all 0.2s ease"
            },
            "nav-link-hover": {
                "background-color": "#f1f5f9",
                "color": "#1e293b"
            },
            "nav-link-selected": {
                "background-color": "linear-gradient(135deg, #6366f1, #8b5cf6)",
                "color": "white",
                "font-weight": "600"
            },
        }
    )
    
    st.markdown("---")
    st.caption("📌 © 2026 LegalAssist")
    st.caption("💡 Solusi Hukum Digital")

# ============================================================
# BERANDA PAGE
# ============================================================
if selected == "Beranda":
    # Hero Section - Enhanced
    st.markdown("""
    <div class="main-header">
        <h1>Solusi Hukum <span class="highlight">Ada di Sini</span></h1>
        <p>Konsultasi masalah hukum Anda dengan cepat, mudah, dan terpercaya</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats - Enhanced
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
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Layanan - Enhanced
    st.markdown('<h2 class="section-title">🎯 Layanan Kami</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Apa yang bisa kami bantu?</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div class="card-icon">💬</div>
            <h3>Chatbot Konsultasi</h3>
            <p>Konsultasi 24/7 dengan chatbot cerdas</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div class="card-icon">👨‍⚖️</div>
            <h3>Direktori Advokat</h3>
            <p>Temukan advokat berpengalaman</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div class="card-icon">📚</div>
            <h3>Artikel Hukum</h3>
            <p>Perluas pengetahuan hukum Anda</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div class="card-icon">❓</div>
            <h3>FAQ Hukum</h3>
            <p>Jawaban pertanyaan umum</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Artikel Terbaru - Enhanced
    st.markdown('<h2 class="section-title">📰 Artikel Hukum Terbaru</h2>', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, artikel in enumerate(db['artikel'][:3]):
        with cols[idx]:
            badge_class = f"badge-{artikel['kategori'].lower()}"
            st.markdown(f"""
            <div class="card">
                <span class="badge {badge_class}">{artikel['kategori']}</span>
                <h4 style="margin: 0.75rem 0 0.5rem 0; color: #1e293b;">{artikel['judul']}</h4>
                <p style="color: #64748b; font-size: 0.9rem; line-height: 1.6;">{artikel['ringkasan'][:100]}...</p>
                <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 0.75rem;">
                    ✍ {artikel['penulis']} · 📅 {artikel['tanggal']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # CTA - Enhanced
    st.markdown("""
    <div class="cta-box">
        <h2>Siap Konsultasi Sekarang?</h2>
        <p>Chatbot kami siap membantu Anda 24/7, gratis, dan tanpa perlu mendaftar.</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# CHATBOT PAGE
# ============================================================
elif selected == "Chatbot":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 50%, #1e293b 100%); 
                padding: 2.5rem; border-radius: 1.5rem; color: white; margin-bottom: 2.5rem;
                position: relative; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);">
        <div style="position: absolute; top: -50%; right: -50%; width: 100%; height: 100%; 
                    background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%); 
                    transform: rotate(45deg);"></div>
        <h1 style="margin: 0; font-weight: 700; position: relative; z-index: 1;">💬 Konsultasi Hukum</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; position: relative; z-index: 1;">
            Chatbot untuk membantu Anda memahami masalah hukum
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cek apakah sedang menampilkan artikel dari chatbot
    if st.session_state.get("chatbot_selected_article"):
        artikel = st.session_state.chatbot_selected_article
        
        # Tombol kembali
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Kembali ke Chatbot", key="back_from_article", use_container_width=True):
                st.session_state.chatbot_selected_article = None
                st.rerun()
        with col2:
            if st.button("📚 Daftar Artikel", key="list_from_article", use_container_width=True):
                st.session_state.chatbot_selected_article = None
                st.session_state.show_article_list = True
                st.rerun()
        
        # Tampilkan artikel lengkap
        badge_class = f"badge-{artikel['kategori'].lower()}"
        st.markdown(f"""
        <div style="background: white; border-radius: 1.25rem; padding: 2.5rem; 
                    border: 1px solid #e2e8f0; margin-top: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
            <span class="badge {badge_class}">{artikel['kategori']}</span>
            <h1 style="margin: 1rem 0 0.5rem 0; color: #1e293b;">{artikel['judul']}</h1>
            <div style="display: flex; gap: 1.5rem; margin-bottom: 1.5rem; color: #64748b; font-size: 0.9rem;">
                <span>✍ {artikel['penulis']}</span>
                <span>📅 {artikel['tanggal']}</span>
                <span>👁 {artikel['baca']} dibaca</span>
            </div>
            <div style="border-top: 1px solid #e2e8f0; padding-top: 1.5rem; line-height: 1.8; color: #334155;">
                {artikel['isi']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif st.session_state.get("show_article_list"):
        # Tampilkan daftar artikel yang bisa dibaca
        st.markdown('<h2 class="section-title">📚 Daftar Artikel Hukum</h2>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Pilih artikel yang ingin Anda baca:</p>', unsafe_allow_html=True)
        
        # Tombol kembali ke chatbot
        if st.button("← Kembali ke Chatbot", key="back_from_list", use_container_width=True):
            st.session_state.show_article_list = False
            st.rerun()
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        # Filter kategori artikel
        kategori_list = ["Semua"] + sorted(list(set([a["kategori"] for a in db["artikel"]])))
        selected_kategori = st.selectbox("Filter Kategori", kategori_list, key="chatbot_article_filter")
        
        filtered_artikel = db["artikel"] if selected_kategori == "Semua" else [a for a in db["artikel"] if a["kategori"] == selected_kategori]
        
        st.markdown(f"<p style='color: #64748b; margin-bottom: 1.5rem;'>Menampilkan {len(filtered_artikel)} artikel</p>", unsafe_allow_html=True)
        
        # Tampilkan artikel dalam bentuk list
        for idx, artikel in enumerate(filtered_artikel):
            badge_class = f"badge-{artikel['kategori'].lower()}"
            with st.container():
                st.markdown(f"""
                <div class="article-card">
                    <span class="badge {badge_class}">{artikel['kategori']}</span>
                    <h4 style="margin: 0.5rem 0; color: #1e293b;">{artikel['judul']}</h4>
                    <p style="color: #64748b; font-size: 0.9rem; margin: 0.5rem 0; line-height: 1.6;">{artikel['ringkasan']}</p>
                    <p style="color: #94a3b8; font-size: 0.8rem;">✍ {artikel['penulis']} · 📅 {artikel['tanggal']} · 👁 {artikel['baca']} dibaca</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"📖 Baca Selengkapnya", key=f"read_artikel_{artikel['id']}_{idx}", use_container_width=True):
                    st.session_state.chatbot_selected_article = artikel
                    st.session_state.show_article_list = False
                    st.rerun()
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        if st.button("← Kembali ke Chatbot", key="back_from_list_bottom", use_container_width=True):
            st.session_state.show_article_list = False
            st.rerun()
    
    else:
        # Sidebar info untuk chatbot - Enhanced
        with st.sidebar:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f8fafc, #f1f5f9); 
                        padding: 1.25rem; border-radius: 1rem; border: 1px solid #e2e8f0;">
                <h4 style="color: #1e293b; margin: 0 0 0.5rem 0;">📋 Kategori Tersedia</h4>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="padding: 0.25rem 0;">
                <span style="color: #475569;">• ⚖️ Pidana (Penipuan, Pencurian)</span><br>
                <span style="color: #475569;">• 📋 Perdata (Hutang, Wanprestasi)</span><br>
                <span style="color: #475569;">• 👨‍👩‍👧 Keluarga (Perceraian, Hak Asuh)</span><br>
                <span style="color: #475569;">• 💼 Ketenagakerjaan (PHK, Perselisihan)</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f8fafc, #f1f5f9); 
                        padding: 1.25rem; border-radius: 1rem; border: 1px solid #e2e8f0;">
                <h4 style="color: #1e293b; margin: 0 0 0.5rem 0;">📚 Baca Artikel</h4>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="padding: 0.25rem 0;">
                <span style="color: #475569; font-size: 0.9rem;">Contoh perintah:</span><br>
                <code style="font-size: 0.8rem; background: #f1f5f9; padding: 0.2rem 0.5rem; border-radius: 0.25rem;">baca artikel pelecehan</code><br>
                <code style="font-size: 0.8rem; background: #f1f5f9; padding: 0.2rem 0.5rem; border-radius: 0.25rem;">artikel KDRT</code><br>
                <code style="font-size: 0.8rem; background: #f1f5f9; padding: 0.2rem 0.5rem; border-radius: 0.25rem;">baca artikel penipuan online</code>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📖 Baca Artikel Hukum", use_container_width=True, key="sidebar_article_btn"):
                st.session_state.show_article_list = True
                st.rerun()
            
            st.markdown("---")
            
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f8fafc, #f1f5f9); 
                        padding: 1.25rem; border-radius: 1rem; border: 1px solid #e2e8f0;">
                <h4 style="color: #1e293b; margin: 0 0 0.5rem 0;">📌 Cara Penggunaan</h4>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="padding: 0.25rem 0; color: #475569; font-size: 0.9rem;">
                1. Ceritakan masalah hukum Anda<br>
                2. Jawab pertanyaan chatbot<br>
                3. Terima hasil & rekomendasi
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            if st.button("🔄 Mulai Ulang Konsultasi", use_container_width=True):
                st.session_state.fsm.reset()
                st.session_state.messages = []
                st.rerun()
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
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
                                    if st.button(f"📖 Baca Artikel: {artikel['judul']}", key=f"btn_artikel_{artikel['id']}_{idx}", use_container_width=True):
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
                                    if st.button(f"📖 Baca Artikel: {artikel['judul']}", key=f"btn_artikel_{artikel['id']}_{len(st.session_state.messages)}", use_container_width=True):
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
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 50%, #1e293b 100%);
                padding: 2.5rem; border-radius: 1.5rem; color: white; margin-bottom: 2.5rem;
                position: relative; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);">
        <div style="position: absolute; top: -50%; right: -50%; width: 100%; height: 100%; 
                    background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%); 
                    transform: rotate(45deg);"></div>
        <h1 style="margin: 0; font-weight: 700; position: relative; z-index: 1;">👨‍⚖️ Informasi Advokat</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; position: relative; z-index: 1;">
            Temukan advokat berpengalaman dan berlisensi sesuai kebutuhan hukum Anda
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter
    spesialisasi_list = ["Semua"] + sorted(list(set([a["spesialisasi"] for a in db["advokat"]])))
    selected_spesialisasi = st.selectbox("Filter Spesialisasi", spesialisasi_list)
    
    filtered_advokat = db["advokat"] if selected_spesialisasi == "Semua" else [a for a in db["advokat"] if a["spesialisasi"] == selected_spesialisasi]
    
    st.markdown(f"<p style='color: #64748b; margin-bottom: 1.5rem;'>Menampilkan {len(filtered_advokat)} advokat</p>", unsafe_allow_html=True)
    
    for adv in filtered_advokat:
        badge_class = f"badge-{adv['spesialisasi'].lower()}"
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"""
                <div style="width: 72px; height: 72px; background: linear-gradient(135deg, #6366f1, #8b5cf6); 
                            border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                            color: white; font-size: 1.5rem; font-weight: 700;
                            box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);">
                    {adv['nama'][0]}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="border: 1px solid #e2e8f0; border-radius: 1rem; padding: 1.25rem; margin-bottom: 1rem;
                            background: white; transition: all 0.3s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <h3 style="margin: 0; color: #1e293b;">{adv['nama']}</h3>
                        <span class="badge {badge_class}">{adv['spesialisasi']}</span>
                    </div>
                    <div style="display: flex; gap: 1.25rem; margin: 0.5rem 0; color: #64748b; font-size: 0.9rem; flex-wrap: wrap;">
                        <span>📍 {adv['kota']}</span>
                        <span>⏱ {adv['pengalaman']}</span>
                        <span>⭐ {adv['rating']}</span>
                        <span>📁 {adv['kasus']} kasus</span>
                    </div>
                    <div style="display: flex; gap: 1.25rem; flex-wrap: wrap; margin-top: 0.25rem;">
                        <code style="background: #f1f5f9; padding: 0.2rem 0.75rem; border-radius: 0.5rem; color: #1e293b;">📞 {adv['telepon']}</code>
                        <code style="background: #f1f5f9; padding: 0.2rem 0.75rem; border-radius: 0.5rem; color: #1e293b;">✉️ {adv['email']}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# ARTIKEL PAGE
# ============================================================
elif selected == "Artikel":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 50%, #1e293b 100%);
                padding: 2.5rem; border-radius: 1.5rem; color: white; margin-bottom: 2.5rem;
                position: relative; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);">
        <div style="position: absolute; top: -50%; right: -50%; width: 100%; height: 100%; 
                    background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%); 
                    transform: rotate(45deg);"></div>
        <h1 style="margin: 0; font-weight: 700; position: relative; z-index: 1;">📚 Artikel Hukum</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; position: relative; z-index: 1;">
            Perluas pengetahuan hukum Anda melalui artikel informatif dari para ahli
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.selected_article is None:
        # Filter
        kategori_list = ["Semua"] + sorted(list(set([a["kategori"] for a in db["artikel"]])))
        selected_kategori = st.selectbox("Filter Kategori", kategori_list)
        
        filtered_artikel = db["artikel"] if selected_kategori == "Semua" else [a for a in db["artikel"] if a["kategori"] == selected_kategori]
        
        st.markdown(f"<p style='color: #64748b; margin-bottom: 1.5rem;'>Menampilkan {len(filtered_artikel)} artikel</p>", unsafe_allow_html=True)
        
        for artikel in filtered_artikel:
            badge_class = f"badge-{artikel['kategori'].lower()}"
            with st.expander(f"📄 {artikel['judul']}"):
                st.markdown(f"""
                <div>
                    <span class="badge {badge_class}">{artikel['kategori']}</span>
                    <p style="color: #64748b; margin: 0.5rem 0;">✍ {artikel['penulis']} · 📅 {artikel['tanggal']} · 👁 {artikel['baca']} dibaca</p>
                    <div style="line-height: 1.8; color: #334155;">{artikel['isi']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Show article detail
        artikel = st.session_state.selected_article
        
        if st.button("← Kembali ke Daftar Artikel", use_container_width=True):
            st.session_state.selected_article = None
            st.rerun()
        
        badge_class = f"badge-{artikel['kategori'].lower()}"
        st.markdown(f"""
        <div style="background: white; border-radius: 1.25rem; padding: 2.5rem; 
                    border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
            <span class="badge {badge_class}">{artikel['kategori']}</span>
            <h1 style="margin: 1rem 0 0.5rem 0; color: #1e293b;">{artikel['judul']}</h1>
            <div style="display: flex; gap: 1.5rem; margin-bottom: 1.5rem; color: #64748b; font-size: 0.9rem;">
                <span>✍ {artikel['penulis']}</span>
                <span>📅 {artikel['tanggal']}</span>
                <span>👁 {artikel['baca']} dibaca</span>
            </div>
            <div style="border-top: 1px solid #e2e8f0; padding-top: 1.5rem; line-height: 1.8; color: #334155;">
                {artikel['isi']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# FAQ PAGE
# ============================================================
elif selected == "FAQ":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 50%, #1e293b 100%);
                padding: 2.5rem; border-radius: 1.5rem; color: white; margin-bottom: 2.5rem;
                position: relative; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);">
        <div style="position: absolute; top: -50%; right: -50%; width: 100%; height: 100%; 
                    background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%); 
                    transform: rotate(45deg);"></div>
        <h1 style="margin: 0; font-weight: 700; position: relative; z-index: 1;">❓ Pertanyaan Umum (FAQ)</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; position: relative; z-index: 1;">
            Temukan jawaban dari pertanyaan yang paling sering ditanyakan
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Category filter
    kategori_list = ["Semua"] + sorted(list(set([f["kategori"] for f in db["faq"]])))
    cols = st.columns(min(len(kategori_list), 4))
    for idx, kat in enumerate(kategori_list):
        with cols[idx % 4]:
            if st.button(kat, key=f"faq_cat_{kat}", use_container_width=True):
                st.session_state.selected_faq_category = kat
                st.rerun()
    
    filtered_faq = db["faq"] if st.session_state.selected_faq_category == "Semua" else [f for f in db["faq"] if f["kategori"] == st.session_state.selected_faq_category]
    
    st.markdown(f"<p style='color: #64748b; margin-bottom: 1.5rem;'>Menampilkan {len(filtered_faq)} pertanyaan</p>", unsafe_allow_html=True)
    
    for faq in filtered_faq:
        with st.expander(f"📌 {faq['pertanyaan']}"):
            st.markdown(f"<div style='color: #334155; line-height: 1.8;'>{faq['jawaban']}</div>", unsafe_allow_html=True)
            st.caption(f"Kategori: {faq['kategori']}")

# ============================================================
# KONTAK PAGE
# ============================================================
elif selected == "Kontak":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 50%, #1e293b 100%);
                padding: 2.5rem; border-radius: 1.5rem; color: white; margin-bottom: 2.5rem;
                position: relative; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);">
        <div style="position: absolute; top: -50%; right: -50%; width: 100%; height: 100%; 
                    background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%); 
                    transform: rotate(45deg);"></div>
        <h1 style="margin: 0; font-weight: 700; position: relative; z-index: 1;">📞 Hubungi Kami</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; position: relative; z-index: 1;">
            Ada pertanyaan atau masukan? Kami siap membantu Anda
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.75rem; border-radius: 1.25rem; border: 1px solid #e2e8f0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.06); height: 100%;">
            <h3 style="color: #1e293b; margin-bottom: 1.25rem;">Informasi Kontak</h3>
            <div style="space-y: 0.5rem;">
                <p style="color: #475569; margin: 0.5rem 0;"><strong style="color: #1e293b;">📞 Telepon:</strong> (021) 5678-9012</p>
                <p style="color: #475569; margin: 0.5rem 0;"><strong style="color: #1e293b;">✉️ Email:</strong> info@legalassist.id</p>
                <p style="color: #475569; margin: 0.5rem 0;"><strong style="color: #1e293b;">📍 Alamat:</strong> Jl. Hukum No. 1, Jakarta Pusat</p>
                <p style="color: #475569; margin: 0.5rem 0;"><strong style="color: #1e293b;">🕒 Jam Layanan:</strong> Senin–Jumat, 08:00–17:00</p>
            </div>
            <hr style="border-color: #e2e8f0; margin: 1.25rem 0;">
            <div style="background: #f8fafc; padding: 1rem; border-radius: 0.75rem; border-left: 3px solid #6366f1;">
                <p style="margin: 0; color: #475569;"><strong>💬 Chatbot</strong> tersedia 24/7 untuk konsultasi dasar.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("kontak_form"):
            st.markdown("<h3 style='color: #1e293b; margin-bottom: 1rem;'>Kirim Pesan</h3>", unsafe_allow_html=True)
            nama = st.text_input("Nama Lengkap", placeholder="Masukkan nama lengkap Anda")
            email = st.text_input("Email", placeholder="Masukkan alamat email Anda")
            subjek = st.text_input("Subjek", placeholder="Masukkan subjek pesan")
            pesan = st.text_area("Pesan", height=150, placeholder="Tuliskan pesan Anda di sini...")
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
                    st.error("⚠️ Semua field harus diisi.")

# ============================================================
# ADMIN PAGE
# ============================================================
elif selected == "Admin":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 50%, #1e293b 100%);
                padding: 2.5rem; border-radius: 1.5rem; color: white; margin-bottom: 2.5rem;
                position: relative; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);">
        <div style="position: absolute; top: -50%; right: -50%; width: 100%; height: 100%; 
                    background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%); 
                    transform: rotate(45deg);"></div>
        <h1 style="margin: 0; font-weight: 700; position: relative; z-index: 1;">🔒 Panel Admin</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; position: relative; z-index: 1;">
            Kelola advokat, artikel, FAQ, dan pesan
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.admin_logged_in:
        with st.form("login_form"):
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 1rem; border: 1px solid #e2e8f0;">
            """, unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            if submitted:
                if username == db["admin"]["username"] and password == db["admin"]["password"]:
                    st.session_state.admin_logged_in = True
                    st.success("✅ Login berhasil!")
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah.")
    else:
        st.success("👋 Selamat datang, Admin!")
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.admin_logged_in = False
                st.rerun()
        
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👨‍⚖️ Advokat", "📚 Artikel", "❓ FAQ"])
        
        with tab1:
            st.markdown("<h3 style='color: #1e293b;'>Statistik</h3>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Konsultasi", db["stats"]["konsultasi"])
            with col2:
                st.metric("Total Advokat", len(db["advokat"]))
            with col3:
                st.metric("Total Artikel", len(db["artikel"]))
            with col4:
                st.metric("Total Pengguna", db["stats"]["pengguna"])
            
            st.markdown("<h3 style='color: #1e293b; margin-top: 2rem;'>Pesan Masuk</h3>", unsafe_allow_html=True)
            pesan_list = db["pesan"][::-1]
            if pesan_list:
                for p in pesan_list:
                    with st.expander(f"📧 {p['subjek']} - {p['nama']} ({p['tanggal']})"):
                        st.write(f"**Email:** {p['email']}")
                        st.write(f"**Pesan:** {p['pesan']}")
                        st.caption(f"Status: {p['status']}")
            else:
                st.info("📭 Belum ada pesan masuk.")
        
        with tab2:
            st.markdown("<h3 style='color: #1e293b;'>Daftar Advokat</h3>", unsafe_allow_html=True)
            for adv in db["advokat"]:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{adv['nama']}** - {adv['spesialisasi']} - {adv['kota']}")
                with col2:
                    if st.button("🗑️ Hapus", key=f"del_adv_{adv['id']}", use_container_width=True):
                        db["advokat"] = [a for a in db["advokat"] if a["id"] != adv["id"]]
                        st.rerun()
            
            st.markdown("<hr style='border-color: #e2e8f0; margin: 2rem 0;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #1e293b;'>Tambah Advokat</h3>", unsafe_allow_html=True)
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
                
                if st.form_submit_button("➕ Tambah Advokat", use_container_width=True):
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
                        st.success("✅ Advokat berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("⚠️ Nama, Telepon, dan Email wajib diisi.")
        
        with tab3:
            st.markdown("<h3 style='color: #1e293b;'>Daftar Artikel</h3>", unsafe_allow_html=True)
            for art in db["artikel"]:
                with st.expander(f"📄 {art['judul']} - {art['kategori']}"):
                    st.write(f"**Penulis:** {art['penulis']}")
                    st.write(f"**Tanggal:** {art['tanggal']}")
                    st.write(f"**Isi:** {art['isi'][:200]}...")
                    if st.button("🗑️ Hapus", key=f"del_art_{art['id']}"):
                        db["artikel"] = [a for a in db["artikel"] if a["id"] != art["id"]]
                        st.rerun()
            
            st.markdown("<hr style='border-color: #e2e8f0; margin: 2rem 0;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #1e293b;'>Tambah Artikel</h3>", unsafe_allow_html=True)
            with st.form("tambah_artikel"):
                judul = st.text_input("Judul")
                kategori = st.selectbox("Kategori", ["Pidana", "Perdata", "Keluarga", "Ketenagakerjaan"])
                isi = st.text_area("Isi Artikel", height=200)
                
                if st.form_submit_button("➕ Tambah Artikel", use_container_width=True):
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
                        st.success("✅ Artikel berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("⚠️ Judul dan Isi Artikel wajib diisi.")
        
        with tab4:
            st.markdown("<h3 style='color: #1e293b;'>Daftar FAQ</h3>", unsafe_allow_html=True)
            for faq in db["faq"]:
                with st.expander(f"❓ {faq['pertanyaan']}"):
                    st.write(f"**Jawaban:** {faq['jawaban']}")
                    st.write(f"**Kategori:** {faq['kategori']}")
                    if st.button("🗑️ Hapus", key=f"del_faq_{faq['id']}"):
                        db["faq"] = [f for f in db["faq"] if f["id"] != faq["id"]]
                        st.rerun()
            
            st.markdown("<hr style='border-color: #e2e8f0; margin: 2rem 0;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #1e293b;'>Tambah FAQ</h3>", unsafe_allow_html=True)
            with st.form("tambah_faq"):
                pertanyaan = st.text_input("Pertanyaan")
                jawaban = st.text_area("Jawaban", height=100)
                kategori = st.text_input("Kategori", value="Umum")
                
                if st.form_submit_button("➕ Tambah FAQ", use_container_width=True):
                    if pertanyaan and jawaban:
                        baru = {
                            "id": len(db["faq"]) + 1,
                            "pertanyaan": pertanyaan,
                            "jawaban": jawaban,
                            "kategori": kategori
                        }
                        db["faq"].append(baru)
                        st.success("✅ FAQ berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("⚠️ Pertanyaan dan Jawaban wajib diisi.")