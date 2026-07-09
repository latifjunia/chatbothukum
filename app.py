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

# ============================================================
# Custom CSS -- "Buku Hukum" (law-ledger) design system, v2 layout
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap');

    :root {
        --ink: #0F1B33;
        --ink-soft: #2C3A63;
        --paper: #F7F8FC;
        --surface: #FFFFFF;
        --border: #DDE3F0;
        --brass: #C89A3C;
        --brass-light: #E3BE6B;
        --brass-dark: #9C7526;
        --forest: #0F8B6C;
        --muted: #5B6478;
        --danger: #C6402E;
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--ink); }

    h1, h2, h3, h4 {
        font-family: 'Fraunces', serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em;
        color: var(--ink);
    }

    code, .mono { font-family: 'IBM Plex Mono', monospace !important; }

    .block-container { padding-top: 2rem; max-width: 1200px; }

    .stApp {
        background:
            repeating-linear-gradient(to bottom, transparent 0px, transparent 39px, rgba(200,154,60,0.05) 40px),
            var(--paper);
    }

    section[data-testid="stSidebar"] { background: var(--surface); border-right: 1px solid var(--border); }
    section[data-testid="stSidebar"] hr { border-color: var(--border); }

    /* ============================================================
       HERO (Beranda) -- two column grid
       ============================================================ */
    .hero-wrap {
        position: relative;
        background: linear-gradient(155deg, var(--ink) 0%, #16264A 60%, #1B2E56 100%);
        border-radius: 20px;
        padding: 3rem 3rem;
        color: var(--paper);
        overflow: hidden;
        box-shadow: 0 20px 45px -20px rgba(15,27,51,0.45);
        margin-bottom: 1.75rem;
    }
    .hero-wrap::before {
        content: "\\00A7";
        position: absolute;
        right: -0.5rem; top: -3.5rem;
        font-family: 'Fraunces', serif;
        font-size: 13rem; font-weight: 700;
        color: rgba(247,248,252,0.05);
        line-height: 1; pointer-events: none;
    }
    .hero-grid {
        display: grid;
        grid-template-columns: 1.15fr 0.85fr;
        gap: 2.5rem;
        align-items: center;
        position: relative;
    }
    .hero-eyebrow {
        display: inline-flex; align-items: center; gap: 0.5rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem; font-weight: 600; letter-spacing: 0.14em;
        text-transform: uppercase; color: var(--brass-light);
        background: rgba(227,190,107,0.12);
        border: 1px solid rgba(227,190,107,0.3);
        padding: 0.3rem 0.75rem; border-radius: 999px;
        margin-bottom: 1rem;
    }
    .hero-wrap h1 { color: var(--paper) !important; font-size: 2.6rem; line-height: 1.15; margin: 0 0 0.9rem 0; }
    .hero-wrap p.hero-sub { font-size: 1.08rem; opacity: 0.78; margin: 0 0 1.5rem 0; max-width: 480px; }
    .hero-stat-row { display: flex; gap: 0.75rem; flex-wrap: wrap; }
    .stat-pill {
        display: flex; flex-direction: column; gap: 0.15rem;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 12px; padding: 0.65rem 1rem; min-width: 108px;
    }
    .stat-pill .num { font-family: 'Fraunces', serif; font-size: 1.35rem; font-weight: 700; color: var(--brass-light); }
    .stat-pill .lbl { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; letter-spacing: 0.06em; text-transform: uppercase; opacity: 0.75; }

    .hero-panel {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 16px;
        padding: 1.5rem 1.5rem 1.25rem;
        backdrop-filter: blur(2px);
    }
    .hero-panel .hp-title { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.65; margin-bottom: 0.9rem; }
    .hero-cat-row { display: flex; align-items: center; gap: 0.75rem; padding: 0.55rem 0; border-bottom: 1px solid rgba(255,255,255,0.08); }
    .hero-cat-row:last-child { border-bottom: none; }
    .hero-cat-icon { width: 34px; height: 34px; border-radius: 9px; background: rgba(227,190,107,0.15); display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
    .hero-cat-text b { font-size: 0.87rem; }
    .hero-cat-text span { display: block; font-size: 0.74rem; opacity: 0.65; }

    /* ============================================================
       PAGE HEADER -- icon badge + title (used on all sub-pages)
       ============================================================ */
    .page-header {
        position: relative;
        background: linear-gradient(155deg, var(--ink) 0%, #16264A 100%);
        border-radius: 16px;
        padding: 1.85rem 2rem;
        color: var(--paper);
        margin-bottom: 1.75rem;
        overflow: hidden;
        box-shadow: 0 14px 32px -16px rgba(15,27,51,0.4);
    }
    .page-header::before {
        content: "\\00A7";
        position: absolute; right: 0.5rem; top: -2.5rem;
        font-family: 'Fraunces', serif; font-size: 9rem; font-weight: 700;
        color: rgba(247,248,252,0.05); line-height: 1; pointer-events: none;
    }
    .ph-row { display: flex; align-items: center; gap: 1.1rem; position: relative; }
    .header-icon-badge {
        width: 54px; height: 54px; border-radius: 14px; flex-shrink: 0;
        background: rgba(227,190,107,0.14); border: 1px solid rgba(227,190,107,0.32);
        display: flex; align-items: center; justify-content: center; font-size: 1.55rem;
    }
    .page-header h1 { color: var(--paper) !important; font-size: 1.55rem; margin: 0; }
    .page-header p { color: var(--paper); opacity: 0.72; margin: 0.3rem 0 0 0; font-size: 0.95rem; }

    /* ============================================================
       Section labels
       ============================================================ */
    .eyebrow {
        display: flex; align-items: center; gap: 0.6rem;
        font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; font-weight: 600;
        letter-spacing: 0.14em; text-transform: uppercase; color: var(--brass-dark);
        margin: 0 0 0.35rem 0;
    }
    .eyebrow::before { content: ""; width: 22px; height: 2px; background: var(--brass); display: inline-block; }
    .section-heading { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem; }
    .section-heading h2 { margin: 0; font-size: 1.5rem; }
    .section-heading .sh-note { color: var(--muted); font-size: 0.88rem; }

    /* ============================================================
       Service cards -- horizontal icon-left layout
       ============================================================ */
    .service-h-card {
        display: flex; gap: 1rem; align-items: flex-start;
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 14px; padding: 1.25rem 1.3rem;
        height: 100%; transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
        box-shadow: 0 2px 10px -6px rgba(15,27,51,0.1);
    }
    .service-h-card:hover { transform: translateY(-3px); box-shadow: 0 16px 28px -14px rgba(15,27,51,0.22); border-color: var(--brass-light); }
    .service-icon {
        width: 46px; height: 46px; border-radius: 12px; flex-shrink: 0;
        background: linear-gradient(135deg, var(--brass-light), var(--brass));
        display: flex; align-items: center; justify-content: center; font-size: 1.3rem;
        box-shadow: 0 6px 14px -6px rgba(200,154,60,0.55);
    }
    .service-h-card h4 { margin: 0 0 0.25rem 0; font-size: 1.02rem; }
    .service-h-card p { margin: 0; color: var(--muted); font-size: 0.85rem; line-height: 1.5; }

    /* ============================================================
       Featured / list article rows
       ============================================================ */
    .featured-card {
        background: var(--surface); border: 1px solid var(--border); border-radius: 16px;
        padding: 1.75rem; height: 100%;
        border-top: 4px solid var(--brass);
        box-shadow: 0 4px 16px -8px rgba(15,27,51,0.12);
    }
    .featured-card h3 { font-size: 1.3rem; margin: 0.7rem 0 0.5rem 0; }
    .article-row-item {
        display: flex; gap: 0.9rem; align-items: flex-start;
        background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
        padding: 0.95rem 1.05rem; margin-bottom: 0.7rem;
        border-left: 4px solid var(--brass-light);
    }
    .article-row-item .ari-num { font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.4rem; color: var(--border); flex-shrink: 0; width: 28px; }
    .article-row-item h5 { margin: 0 0 0.2rem 0; font-size: 0.98rem; }
    .article-row-item p { margin: 0; color: var(--muted); font-size: 0.82rem; }

    /* ============================================================
       Generic cards / badges
       ============================================================ */
    .card, .article-card {
        position: relative; background: var(--surface); padding: 1.5rem 1.4rem;
        border-radius: 14px; border: 1px solid var(--border);
        transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
        overflow: hidden; margin-bottom: 1rem; height: 100%;
        box-shadow: 0 2px 10px -6px rgba(15,27,51,0.1);
    }
    .card:hover, .article-card:hover { transform: translateY(-3px); box-shadow: 0 16px 28px -14px rgba(15,27,51,0.2); border-color: var(--brass-light); }
    .card h3, .card h4, .article-card h4 { margin-top: 0.6rem; font-size: 1.08rem; }

    .badge {
        display: inline-block; font-family: 'IBM Plex Mono', monospace;
        padding: 0.22rem 0.7rem; border-radius: 999px; border: none;
        font-size: 0.66rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;
    }
    .badge-pidana { background: #FDEAE7; color: #C6402E; }
    .badge-perdata { background: #E7EEFE; color: #1D4ED8; }
    .badge-keluarga { background: #F3EBFE; color: #7C3AED; }
    .badge-ketenagakerjaan { background: #FEF3D6; color: #B45309; }

    /* ============================================================
       Stat cards (used in Admin)
       ============================================================ */
    .stat-card {
        text-align: center; padding: 1.1rem 0.5rem 0.9rem; border-radius: 14px;
        background: var(--surface); border: 1px solid var(--border); border-top: 3px solid var(--brass);
    }
    .stat-number { font-family: 'Fraunces', serif; font-size: 2rem; font-weight: 700; color: var(--ink); line-height: 1.1; }
    .stat-label { font-family: 'IBM Plex Mono', monospace; color: var(--muted); font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.35rem; }

    /* ============================================================
       Buttons / inputs
       ============================================================ */
    .stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
        background: var(--ink); color: var(--paper) !important; border: 1px solid var(--ink);
        border-radius: 8px; padding: 0.5rem 1.1rem; font-weight: 600; font-size: 0.86rem;
        letter-spacing: 0.01em; transition: all .18s ease; box-shadow: none;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
        background: var(--brass); border-color: var(--brass); color: var(--ink) !important;
        transform: translateY(-1px); box-shadow: 0 8px 16px -6px rgba(200,154,60,0.45);
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 8px !important; border-color: var(--border) !important;
    }

    /* Chip-style filter buttons (category / topic pills) */
    div[data-testid="stHorizontalBlock"] .chip-row .stButton > button {
        border-radius: 999px !important;
        background: var(--surface); color: var(--ink) !important; border: 1px solid var(--border);
        font-size: 0.78rem; padding: 0.35rem 0.5rem;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [aria-selected="true"] { color: var(--brass-dark) !important; }

    div[data-testid="stMetric"] {
        background: var(--surface); border: 1px solid var(--border); border-top: 3px solid var(--brass);
        border-radius: 12px; padding: 0.9rem 1rem;
    }

    hr { border-color: var(--border) !important; }

    /* ============================================================
       CTA banner
       ============================================================ */
    .cta-banner {
        background: linear-gradient(155deg, var(--ink) 0%, #16264A 100%);
        border-radius: 20px; padding: 2.75rem; position: relative; overflow: hidden;
        display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; flex-wrap: wrap;
    }
    .cta-banner::before {
        content: "\\00A7"; position: absolute; right: 0.5rem; top: -2.75rem;
        font-family: 'Fraunces', serif; font-size: 10rem; font-weight: 700;
        color: rgba(247,248,252,0.05); line-height: 1;
    }
    .cta-text h2 { color: var(--paper) !important; font-size: 1.7rem; margin: 0 0 0.4rem 0; position: relative; }
    .cta-text p { color: var(--paper); opacity: 0.72; margin: 0; font-size: 0.98rem; position: relative; max-width: 420px; }

    /* ============================================================
       Chatbot layout helpers
       ============================================================ */
    .chat-side-card {
        background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
        padding: 1.1rem 1.2rem; margin-bottom: 0.9rem;
    }
    .chat-side-card h5 { margin: 0 0 0.6rem 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--brass-dark); font-family: 'IBM Plex Mono', monospace; }
    [data-testid="stChatMessage"] { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 0.4rem 0.6rem; margin-bottom: 0.6rem; }

    /* ============================================================
       Article detail panel
       ============================================================ */
    .article-detail {
        background: var(--surface); border-radius: 16px; padding: 2rem; border: 1px solid var(--border);
        margin-top: 0.5rem; box-shadow: 0 4px 20px -12px rgba(15,27,51,0.15);
    }
    .article-detail-meta { display: flex; gap: 1rem; flex-wrap: wrap; margin: 0.9rem 0 1.4rem 0; color: var(--muted); font-size: 0.85rem; }
    .article-detail-body { border-top: 1px solid var(--border); padding-top: 1.4rem; line-height: 1.85; }

    /* ============================================================
       Advokat grid card
       ============================================================ */
    .advokat-grid-card {
        background: var(--surface); border: 1px solid var(--border); border-radius: 16px;
        padding: 1.4rem; text-align: center; height: 100%;
        box-shadow: 0 2px 10px -6px rgba(15,27,51,0.1);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .advokat-grid-card:hover { transform: translateY(-3px); box-shadow: 0 16px 28px -14px rgba(15,27,51,0.2); }
    .advokat-avatar {
        width: 62px; height: 62px; border-radius: 50%; margin: 0 auto 0.75rem;
        display: flex; align-items: center; justify-content: center; color: var(--paper);
        font-family: 'Fraunces', serif; font-size: 1.4rem; font-weight: 700;
        background: linear-gradient(135deg, var(--ink), var(--ink-soft)); border: 2px solid var(--brass);
    }
    .advokat-grid-card h4 { margin: 0.2rem 0 0.35rem 0; font-size: 1.05rem; }
    .advokat-meta-grid { display: flex; flex-direction: column; gap: 0.3rem; color: var(--muted); font-size: 0.82rem; margin: 0.7rem 0; }
    .advokat-contact-grid { display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.78rem; }

    /* ============================================================
       Footer
       ============================================================ */
    .app-footer {
        margin-top: 3.5rem; padding-top: 2.25rem; border-top: 1px solid var(--border);
    }
    .app-footer .af-grid { display: grid; grid-template-columns: 1.4fr 1fr 1fr; gap: 2rem; }
    .app-footer h4 { font-size: 1.05rem; margin: 0 0 0.5rem 0; }
    .app-footer p, .app-footer li { color: var(--muted); font-size: 0.85rem; line-height: 1.7; }
    .app-footer ul { list-style: none; padding: 0; margin: 0; }
    .app-footer .af-bottom { text-align: center; color: var(--muted); font-size: 0.78rem; margin-top: 1.75rem; padding-top: 1.25rem; border-top: 1px solid var(--border); }

    /* ============================================================
       Sidebar nav polish
       ============================================================ */
    .sidebar-brand { display: flex; align-items: center; gap: 0.6rem; padding: 0.25rem 0 0.9rem; }
    .sidebar-brand .sb-badge { width: 38px; height: 38px; border-radius: 10px; background: var(--ink); color: var(--brass-light); display: flex; align-items: center; justify-content: center; font-size: 1.1rem; }
    .sidebar-brand .sb-text b { display: block; font-family: 'Fraunces', serif; font-size: 1.05rem; line-height: 1.1; }
    .sidebar-brand .sb-text span { font-size: 0.68rem; color: var(--muted); letter-spacing: 0.04em; }

    section[data-testid="stSidebar"] .nav-link { border-radius: 8px !important; font-family: 'Inter', sans-serif !important; margin: 0.15rem 0 !important; }
    section[data-testid="stSidebar"] .nav-link:hover { background-color: #EAF0FF !important; }
    section[data-testid="stSidebar"] .nav-link-selected { border-radius: 8px !important; box-shadow: inset 3px 0 0 var(--brass); }
    section[data-testid="stSidebar"] .menu-title { font-family: 'Fraunces', serif !important; }

    a:focus-visible, button:focus-visible, .stButton > button:focus-visible {
        outline: 2px solid var(--brass) !important; outline-offset: 2px;
    }

    @media (prefers-reduced-motion: no-preference) {
        .hero-wrap, .page-header, .card, .article-card, .stat-card, .service-h-card, .featured-card, .advokat-grid-card {
            animation: legalassist-fade-up 0.4s ease both;
        }
    }
    @keyframes legalassist-fade-up { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

    /* ============================================================
       RESPONSIVE
       ============================================================ */
    @media (max-width: 992px) {
        .hero-grid { grid-template-columns: 1fr; }
        .hero-panel { margin-top: 0.5rem; }
        .hero-wrap { padding: 2.25rem 1.75rem; }
        .hero-wrap h1 { font-size: 2rem; }
        .app-footer .af-grid { grid-template-columns: 1fr 1fr; }
    }

    @media (max-width: 640px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .hero-wrap { padding: 1.75rem 1.25rem; border-radius: 14px; }
        .hero-wrap h1 { font-size: 1.55rem; }
        .hero-wrap::before, .page-header::before, .cta-banner::before { display: none; }
        .hero-panel { padding: 1.1rem; }
        .page-header { padding: 1.4rem 1.15rem; border-radius: 12px; }
        .header-icon-badge { width: 42px; height: 42px; font-size: 1.2rem; border-radius: 10px; }
        .page-header h1 { font-size: 1.2rem; }
        .page-header p { font-size: 0.82rem; }

        div[data-testid="stHorizontalBlock"] { flex-direction: column !important; }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            width: 100% !important; flex: 1 1 100% !important; min-width: 100% !important;
        }

        .card, .article-card, .service-h-card, .featured-card, .advokat-grid-card { padding: 1.15rem; }
        .stat-number { font-size: 1.6rem; }
        .cta-banner { padding: 1.75rem 1.35rem; flex-direction: column; text-align: center; }
        .app-footer .af-grid { grid-template-columns: 1fr; gap: 1.4rem; text-align: left; }

        h1 { font-size: 1.4rem !important; }
        h2 { font-size: 1.2rem !important; }
        h3 { font-size: 1.05rem !important; }
    }

    @media (min-width: 641px) and (max-width: 900px) {
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] { min-width: 45% !important; flex: 1 1 45% !important; }
    }
</style>
""", unsafe_allow_html=True)


# ---------------- Layout helper components ----------------
def render_page_header(icon, title, subtitle):
    st.markdown(f"""
    <div class="page-header">
        <div class="ph-row">
            <div class="header-icon-badge">{icon}</div>
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="app-footer">
        <div class="af-grid">
            <div>
                <h4>⚖️ LegalAssist</h4>
                <p>Platform konsultasi hukum digital yang menghubungkan masyarakat dengan informasi hukum yang jelas dan advokat terpercaya, kapan saja Anda butuhkan.</p>
            </div>
            <div>
                <h4 style="font-size:0.95rem;">Layanan</h4>
                <ul>
                    <li>Chatbot Konsultasi</li>
                    <li>Direktori Advokat</li>
                    <li>Artikel Hukum</li>
                    <li>FAQ Hukum</li>
                </ul>
            </div>
            <div>
                <h4 style="font-size:0.95rem;">Kontak</h4>
                <ul>
                    <li>📞 (021) 5678-9012</li>
                    <li>✉️ info@legalassist.id</li>
                    <li>📍 Jl. Hukum No. 1, Jakarta Pusat</li>
                </ul>
            </div>
        </div>
        <div class="af-bottom">© 2026 LegalAssist — Solusi Hukum Digital Terpercaya</div>
    </div>
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
if "artikel_filter_kategori" not in st.session_state:
    st.session_state.artikel_filter_kategori = "Semua"
if "advokat_filter_spesialisasi" not in st.session_state:
    st.session_state.advokat_filter_spesialisasi = "Semua"

MENU_OPTIONS = ["Beranda", "Chatbot", "Advokat", "Artikel", "FAQ", "Kontak", "Admin"]

# Allow other parts of the app (e.g. the homepage CTA) to programmatically jump tabs
_manual_select = None
if "force_nav" in st.session_state:
    _target = st.session_state.pop("force_nav")
    if _target in MENU_OPTIONS:
        _manual_select = MENU_OPTIONS.index(_target)

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sb-badge">⚖️</div>
        <div class="sb-text">
            <b>LegalAssist</b>
            <span>KONSULTASI HUKUM DIGITAL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    selected = option_menu(
        menu_title=None,
        options=MENU_OPTIONS,
        icons=[
            "house-door-fill",
            "chat-dots-fill",
            "person-badge-fill",
            "journal-bookmark-fill",
            "patch-question-fill",
            "envelope-paper-fill",
            "shield-lock-fill",
        ],
        default_index=0,
        manual_select=_manual_select,
        key="main_menu",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#C89A3C", "font-size": "1.05rem"},
            "nav-link": {"font-size": "0.9rem", "text-align": "left", "margin": "0.2rem 0", "border-radius": "8px"},
            "nav-link-selected": {"background-color": "#0F1B33", "border-radius": "8px"},
        }
    )

    st.markdown("---")
    st.caption("© 2026 LegalAssist")
    st.caption("Solusi Hukum Digital Terpercaya")

# ============================================================
# BERANDA PAGE
# ============================================================
if selected == "Beranda":
    # ---------- Hero (two-column grid) ----------
    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-grid">
            <div>
                <div class="hero-eyebrow">⚖️ Platform Hukum Digital</div>
                <h1>Solusi Hukum <span style="color:#E3BE6B;">Ada&nbsp;di&nbsp;Sini</span></h1>
                <p class="hero-sub">Konsultasi masalah hukum Anda dengan cepat, mudah, dan terpercaya — ditemani chatbot cerdas dan jaringan advokat berpengalaman.</p>
                <div class="hero-stat-row">
                    <div class="stat-pill"><span class="num">{db['stats']['konsultasi']}</span><span class="lbl">Konsultasi</span></div>
                    <div class="stat-pill"><span class="num">{db['stats']['advokat']}</span><span class="lbl">Advokat</span></div>
                    <div class="stat-pill"><span class="num">{db['stats']['artikel']}</span><span class="lbl">Artikel</span></div>
                    <div class="stat-pill"><span class="num">{db['stats']['pengguna']}</span><span class="lbl">Kasus</span></div>
                </div>
            </div>
            <div class="hero-panel">
                <div class="hp-title">Kategori Populer</div>
                <div class="hero-cat-row">
                    <div class="hero-cat-icon">⚖️</div>
                    <div class="hero-cat-text"><b>Pidana</b><span>Penipuan, pencurian, kekerasan</span></div>
                </div>
                <div class="hero-cat-row">
                    <div class="hero-cat-icon">📋</div>
                    <div class="hero-cat-text"><b>Perdata</b><span>Hutang, wanprestasi, sengketa</span></div>
                </div>
                <div class="hero-cat-row">
                    <div class="hero-cat-icon">👨‍👩‍👧</div>
                    <div class="hero-cat-text"><b>Keluarga</b><span>Perceraian, hak asuh anak</span></div>
                </div>
                <div class="hero-cat-row">
                    <div class="hero-cat-icon">💼</div>
                    <div class="hero-cat-text"><b>Ketenagakerjaan</b><span>PHK, pesangon, perselisihan</span></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # ---------- Layanan (horizontal icon cards, 2x2) ----------
    st.markdown("""
    <div class="section-heading">
        <div><div class="eyebrow">Layanan</div><h2>Apa yang Bisa Kami Bantu?</h2></div>
        <div class="sh-note">4 layanan utama untuk masalah hukum Anda</div>
    </div>
    """, unsafe_allow_html=True)

    layanan = [
        ("💬", "Chatbot Konsultasi", "Konsultasi 24/7 dengan chatbot cerdas yang memandu setiap kasus."),
        ("🧑‍⚖️", "Direktori Advokat", "Temukan advokat berpengalaman sesuai spesialisasi & kota Anda."),
        ("📚", "Artikel Hukum", "Perluas pengetahuan hukum lewat artikel yang mudah dipahami."),
        ("❓", "FAQ Hukum", "Jawaban cepat untuk pertanyaan-pertanyaan yang paling sering muncul."),
    ]
    r1 = st.columns(2)
    r2 = st.columns(2)
    for i, (icon, title, desc) in enumerate(layanan):
        target = r1[i] if i < 2 else r2[i - 2]
        with target:
            st.markdown(f"""
            <div class="service-h-card">
                <div class="service-icon">{icon}</div>
                <div><h4>{title}</h4><p>{desc}</p></div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # ---------- Artikel Terbaru (featured + list) ----------
    st.markdown("""
    <div class="section-heading">
        <div><div class="eyebrow">Bacaan</div><h2>Artikel Hukum Terbaru</h2></div>
        <div class="sh-note">Diperbarui secara berkala oleh tim redaksi</div>
    </div>
    """, unsafe_allow_html=True)

    latest = db['artikel'][:3]
    if latest:
        col_feat, col_list = st.columns([1.2, 1])
        featured = latest[0]
        with col_feat:
            badge_class = f"badge-{featured['kategori'].lower()}"
            st.markdown(f"""
            <div class="featured-card">
                <span class="badge {badge_class}">{featured['kategori']}</span>
                <h3>{featured['judul']}</h3>
                <p style="color:var(--muted); line-height:1.7;">{featured['ringkasan'][:220]}...</p>
                <p style="color:#8891A6; font-size:0.78rem; margin-top:1rem;">✍ {featured['penulis']} · 📅 {featured['tanggal']} · 👁 {featured['baca']} dibaca</p>
            </div>
            """, unsafe_allow_html=True)
        with col_list:
            for idx, artikel in enumerate(latest[1:], start=2):
                st.markdown(f"""
                <div class="article-row-item">
                    <div class="ari-num">{idx:02d}</div>
                    <div>
                        <h5>{artikel['judul']}</h5>
                        <p>{artikel['ringkasan'][:80]}...</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.write("")

    # ---------- CTA ----------
    st.markdown("""
    <div class="cta-banner">
        <div class="cta-text">
            <h2>Siap Konsultasi Sekarang?</h2>
            <p>Chatbot kami siap membantu Anda 24/7, gratis, dan tanpa perlu mendaftar.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    col_cta = st.columns([2, 1, 2])
    with col_cta[1]:
        if st.button("💬 Mulai Konsultasi", use_container_width=True, key="home_cta_btn"):
            st.session_state.force_nav = "Chatbot"
            st.rerun()

    render_footer()

# ============================================================
# CHATBOT PAGE
# ============================================================
elif selected == "Chatbot":
    render_page_header("💬", "Konsultasi Hukum", "Chatbot untuk membantu Anda memahami masalah hukum")

    # Cek apakah sedang menampilkan artikel dari chatbot
    if st.session_state.get("chatbot_selected_article"):
        artikel = st.session_state.chatbot_selected_article

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

        badge_class = f"badge-{artikel['kategori'].lower()}"
        st.markdown(f"""
        <div class="article-detail">
            <span class="badge {badge_class}">{artikel['kategori']}</span>
            <h1 style="margin: 1rem 0 0.5rem 0;">{artikel['judul']}</h1>
            <div class="article-detail-meta">
                <span>✍ {artikel['penulis']}</span>
                <span>📅 {artikel['tanggal']}</span>
                <span>👁 {artikel['baca']} dibaca</span>
            </div>
            <div class="article-detail-body">{artikel['isi']}</div>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.get("show_article_list"):
        st.markdown('<div class="eyebrow">Perpustakaan</div>', unsafe_allow_html=True)
        st.markdown("## 📚 Daftar Artikel Hukum")
        st.caption("Pilih artikel yang ingin Anda baca")

        if st.button("← Kembali ke Chatbot", key="back_from_list"):
            st.session_state.show_article_list = False
            st.rerun()

        st.write("")

        kategori_list = ["Semua"] + sorted(list(set([a["kategori"] for a in db["artikel"]])))
        chip_cols = st.columns(len(kategori_list))
        for i, kat in enumerate(kategori_list):
            with chip_cols[i]:
                if st.button(kat, key=f"chatbot_chip_{kat}", use_container_width=True):
                    st.session_state.artikel_filter_kategori = kat

        selected_kategori = st.session_state.artikel_filter_kategori
        filtered_artikel = db["artikel"] if selected_kategori == "Semua" else [a for a in db["artikel"] if a["kategori"] == selected_kategori]
        st.markdown(f"<p style='color: var(--muted); margin: 1rem 0;'>Menampilkan {len(filtered_artikel)} artikel</p>", unsafe_allow_html=True)

        grid_cols = st.columns(2)
        for idx, artikel in enumerate(filtered_artikel):
            badge_class = f"badge-{artikel['kategori'].lower()}"
            with grid_cols[idx % 2]:
                st.markdown(f"""
                <div class="card">
                    <span class="badge {badge_class}">{artikel['kategori']}</span>
                    <h4>{artikel['judul']}</h4>
                    <p style="color: var(--muted); font-size: 0.85rem;">{artikel['ringkasan']}</p>
                    <p style="color: #8891A6; font-size: 0.75rem;">✍ {artikel['penulis']} · 📅 {artikel['tanggal']} · 👁 {artikel['baca']} dibaca</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("📖 Baca Selengkapnya", key=f"read_artikel_{artikel['id']}_{idx}", use_container_width=True):
                    st.session_state.chatbot_selected_article = artikel
                    st.session_state.show_article_list = False
                    st.rerun()

        st.markdown("---")
        if st.button("← Kembali ke Chatbot", key="back_from_list_bottom", use_container_width=True):
            st.session_state.show_article_list = False
            st.rerun()

    else:
        # ---------- Two column layout: chat history (left) + quick-access panel (right) ----------
        col_chat, col_side = st.columns([2, 1])

        with col_side:
            st.markdown("""
            <div class="chat-side-card">
                <h5>Kategori Tersedia</h5>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            - ⚖️ **Pidana** — Penipuan, Pencurian
            - 📋 **Perdata** — Hutang, Wanprestasi
            - 👨‍👩‍👧 **Keluarga** — Perceraian, Hak Asuh
            - 💼 **Ketenagakerjaan** — PHK, Perselisihan
            """)

            st.markdown("""
            <div class="chat-side-card" style="margin-top:0.9rem;">
                <h5>Baca Artikel</h5>
            </div>
            """, unsafe_allow_html=True)
            st.caption("Ketik `baca artikel [topik]`, contoh: `baca artikel PHK`")
            if st.button("📖 Buka Daftar Artikel", use_container_width=True, key="sidebar_article_btn"):
                st.session_state.show_article_list = True
                st.rerun()

            st.markdown("""
            <div class="chat-side-card" style="margin-top:0.9rem;">
                <h5>Cara Penggunaan</h5>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            1. Ceritakan masalah hukum Anda
            2. Jawab pertanyaan chatbot
            3. Terima hasil & rekomendasi
            """)

            if st.button("🔄 Mulai Ulang Konsultasi", use_container_width=True):
                st.session_state.fsm.reset()
                st.session_state.messages = []
                st.rerun()

        with col_chat:
            if not st.session_state.messages:
                st.info("👋 Halo! Ceritakan masalah hukum Anda, atau ketik **baca artikel [topik]** untuk membaca artikel.")

            for idx, msg in enumerate(st.session_state.messages):
                if msg["role"] == "user":
                    with st.chat_message("user"):
                        st.write(msg["content"])
                else:
                    with st.chat_message("assistant", avatar="⚖️"):
                        st.write(msg["content"])
                        if "artikel_link" in msg and msg["artikel_link"]:
                            if msg["artikel_link"] in ARTIKEL_LINK:
                                artikel_info = ARTIKEL_LINK[msg["artikel_link"]]
                                for artikel in db["artikel"]:
                                    if artikel["id"] == artikel_info["id"]:
                                        if st.button(f"📖 Baca Artikel: {artikel['judul']}", key=f"btn_artikel_{artikel['id']}_{idx}"):
                                            st.session_state.chatbot_selected_article = artikel
                                            st.rerun()
                                        break

        # Chat input stays outside the columns so it pins correctly at the bottom
        prompt = st.chat_input("Ceritakan masalah hukum anda... Atau ketik 'baca artikel [topik]' untuk membaca artikel")

        if prompt:
            if prompt.lower().startswith("baca artikel") or prompt.lower().startswith("artikel"):
                kata_kunci = prompt.lower().replace("baca artikel", "").replace("artikel", "").strip()

                if kata_kunci:
                    artikel_ditemukan = cari_artikel_by_keyword(kata_kunci)

                    if artikel_ditemukan:
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        st.session_state.chatbot_selected_article = artikel_ditemukan
                        st.rerun()
                    else:
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": (
                                f"Maaf, saya tidak menemukan artikel tentang '{kata_kunci}'. Berikut topik artikel yang tersedia:\n\n"
                                f"- pelecehan / kekerasan seksual\n- KDRT / kekerasan rumah tangga\n- penipuan online\n"
                                f"- PHK / pesangon\n- tipu lowongan kerja\n- pencemaran nama baik / ITE\n"
                                f"- sengketa tanah / warisan\n- pinjol ilegal\n- pencurian\n- perceraian\n\n"
                                f"Ketik `baca artikel [topik]` dengan topik yang sesuai."
                            )
                        })
                        st.rerun()
                else:
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": (
                            "Silakan tentukan topik artikel yang ingin Anda baca. Contoh:\n\n"
                            "- `baca artikel pelecehan`\n- `baca artikel KDRT`\n- `baca artikel penipuan online`\n- `baca artikel PHK`\n\n"
                            "Atau ketik `menu` untuk konsultasi hukum."
                        )
                    })
                    st.rerun()
            else:
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
                    st.session_state.messages.append({"role": "assistant", "content": msg_text})

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
**🧑‍⚖️ Rekomendasi:** {response['advokat']}

---
Ketik `reset` untuk konsultasi baru.
"""
                    msg_data = {"role": "assistant", "content": msg_text}
                    if "artikel" in response and response["artikel"]:
                        msg_data["artikel_link"] = response["artikel"]["id"]
                        msg_text += "\n\n📖 **Baca artikel selengkapnya dengan klik tombol di bawah ini!**"
                        msg_data["content"] = msg_text

                    st.session_state.messages.append(msg_data)

                else:
                    st.session_state.messages.append({"role": "assistant", "content": response.get("text", "Maaf, saya tidak mengerti.")})

                st.rerun()

# ============================================================
# ADVOKAT PAGE
# ============================================================
elif selected == "Advokat":
    render_page_header("🧑‍⚖️", "Informasi Advokat", "Temukan advokat berpengalaman dan berlisensi sesuai kebutuhan hukum Anda")

    spesialisasi_list = ["Semua"] + sorted(list(set([a["spesialisasi"] for a in db["advokat"]])))
    chip_cols = st.columns(len(spesialisasi_list))
    for i, sp in enumerate(spesialisasi_list):
        with chip_cols[i]:
            if st.button(sp, key=f"adv_chip_{sp}", use_container_width=True):
                st.session_state.advokat_filter_spesialisasi = sp

    selected_spesialisasi = st.session_state.advokat_filter_spesialisasi
    filtered_advokat = db["advokat"] if selected_spesialisasi == "Semua" else [a for a in db["advokat"] if a["spesialisasi"] == selected_spesialisasi]

    st.markdown(f"<p style='color: var(--muted); margin: 1rem 0;'>Menampilkan {len(filtered_advokat)} advokat</p>", unsafe_allow_html=True)

    grid_cols = st.columns(2)
    for idx, adv in enumerate(filtered_advokat):
        badge_class = f"badge-{adv['spesialisasi'].lower()}"
        with grid_cols[idx % 2]:
            st.markdown(f"""
            <div class="advokat-grid-card">
                <div class="advokat-avatar">{adv['nama'][0]}</div>
                <h4>{adv['nama']}</h4>
                <span class="badge {badge_class}">{adv['spesialisasi']}</span>
                <div class="advokat-meta-grid">
                    <span>📍 {adv['kota']} &nbsp;·&nbsp; ⏱ {adv['pengalaman']}</span>
                    <span>⭐ {adv['rating']} &nbsp;·&nbsp; 📁 {adv['kasus']} kasus</span>
                </div>
                <div class="advokat-contact-grid">
                    <code>📞 {adv['telepon']}</code>
                    <code>✉️ {adv['email']}</code>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")

    render_footer()

# ============================================================
# ARTIKEL PAGE
# ============================================================
elif selected == "Artikel":
    render_page_header("📚", "Artikel Hukum", "Perluas pengetahuan hukum Anda melalui artikel informatif dari para ahli")

    if st.session_state.selected_article is None:
        kategori_list = ["Semua"] + sorted(list(set([a["kategori"] for a in db["artikel"]])))
        chip_cols = st.columns(len(kategori_list))
        for i, kat in enumerate(kategori_list):
            with chip_cols[i]:
                if st.button(kat, key=f"art_chip_{kat}", use_container_width=True):
                    st.session_state.artikel_filter_kategori = kat

        selected_kategori = st.session_state.artikel_filter_kategori
        filtered_artikel = db["artikel"] if selected_kategori == "Semua" else [a for a in db["artikel"] if a["kategori"] == selected_kategori]

        st.markdown(f"<p style='color: var(--muted); margin: 1rem 0;'>Menampilkan {len(filtered_artikel)} artikel</p>", unsafe_allow_html=True)

        grid_cols = st.columns(3)
        for idx, artikel in enumerate(filtered_artikel):
            badge_class = f"badge-{artikel['kategori'].lower()}"
            with grid_cols[idx % 3]:
                st.markdown(f"""
                <div class="card">
                    <span class="badge {badge_class}">{artikel['kategori']}</span>
                    <h4>{artikel['judul']}</h4>
                    <p style="color: var(--muted); font-size: 0.85rem;">{artikel['ringkasan'][:110]}...</p>
                    <p style="color: #8891A6; font-size: 0.75rem;">✍ {artikel['penulis']} · 📅 {artikel['tanggal']} · 👁 {artikel['baca']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Baca Selengkapnya →", key=f"art_read_{artikel['id']}_{idx}", use_container_width=True):
                    st.session_state.selected_article = artikel
                    st.rerun()
                st.write("")
    else:
        artikel = st.session_state.selected_article

        if st.button("← Kembali ke Daftar Artikel"):
            st.session_state.selected_article = None
            st.rerun()

        badge_class = f"badge-{artikel['kategori'].lower()}"
        st.markdown(f"""
        <div class="article-detail">
            <span class="badge {badge_class}">{artikel['kategori']}</span>
            <h1 style="margin: 1rem 0 0.5rem 0;">{artikel['judul']}</h1>
            <div class="article-detail-meta">
                <span>✍ {artikel['penulis']}</span>
                <span>📅 {artikel['tanggal']}</span>
                <span>👁 {artikel['baca']} dibaca</span>
            </div>
            <div class="article-detail-body">{artikel['isi']}</div>
        </div>
        """, unsafe_allow_html=True)

    render_footer()

# ============================================================
# FAQ PAGE
# ============================================================
elif selected == "FAQ":
    render_page_header("❓", "Pertanyaan Umum (FAQ)", "Temukan jawaban dari pertanyaan yang paling sering ditanyakan")

    kategori_list = ["Semua"] + sorted(list(set([f["kategori"] for f in db["faq"]])))
    cols = st.columns(len(kategori_list))
    for idx, kat in enumerate(kategori_list):
        with cols[idx]:
            if st.button(kat, key=f"faq_cat_{kat}", use_container_width=True):
                st.session_state.selected_faq_category = kat
                st.rerun()

    filtered_faq = db["faq"] if st.session_state.selected_faq_category == "Semua" else [f for f in db["faq"] if f["kategori"] == st.session_state.selected_faq_category]

    st.markdown(f"<p style='color: var(--muted); margin: 1rem 0;'>Menampilkan {len(filtered_faq)} pertanyaan</p>", unsafe_allow_html=True)

    # Two-column FAQ grid
    faq_cols = st.columns(2)
    for idx, faq in enumerate(filtered_faq):
        with faq_cols[idx % 2]:
            with st.expander(f"📌 {faq['pertanyaan']}"):
                st.markdown(f"<p>{faq['jawaban']}</p>", unsafe_allow_html=True)
                st.caption(f"Kategori: {faq['kategori']}")

    render_footer()

# ============================================================
# KONTAK PAGE
# ============================================================
elif selected == "Kontak":
    render_page_header("📞", "Hubungi Kami", "Ada pertanyaan atau masukan? Kami siap membantu Anda")

    col1, col2 = st.columns([0.9, 1.1])

    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="margin-top:0;">Informasi Kontak</h3>
            <div class="chat-side-card" style="border:none; padding:0.6rem 0;">
                <p style="margin:0.4rem 0;">📞 &nbsp;<strong>(021) 5678-9012</strong></p>
                <p style="margin:0.4rem 0;">✉️ &nbsp;<strong>info@legalassist.id</strong></p>
                <p style="margin:0.4rem 0;">📍 &nbsp;Jl. Hukum No. 1, Jakarta Pusat</p>
                <p style="margin:0.4rem 0;">🕒 &nbsp;Senin–Jumat, 08:00–17:00</p>
            </div>
            <hr>
            <p style="color: var(--muted); font-size: 0.88rem;">💬 <strong>Chatbot</strong> tersedia 24/7 untuk konsultasi dasar, tanpa perlu menunggu jam kerja.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        with st.form("kontak_form"):
            st.markdown("<h3 style='margin-top:0;'>Kirim Pesan</h3>", unsafe_allow_html=True)
            nama = st.text_input("Nama Lengkap")
            email = st.text_input("Email")
            subjek = st.text_input("Subjek")
            pesan = st.text_area("Pesan", height=140)
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

    render_footer()

# ============================================================
# ADMIN PAGE
# ============================================================
elif selected == "Admin":
    render_page_header("🔒", "Panel Admin", "Kelola advokat, artikel, FAQ, dan pesan")

    if not st.session_state.admin_logged_in:
        col_l, col_m, col_r = st.columns([1, 1, 1])
        with col_m:
            with st.form("login_form"):
                st.markdown("<h3 style='margin-top:0;'>Login Admin</h3>", unsafe_allow_html=True)
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
        col_welcome, col_logout = st.columns([4, 1])
        with col_welcome:
            st.success("Selamat datang, Admin!")
        with col_logout:
            if st.button("Logout", use_container_width=True):
                st.session_state.admin_logged_in = False
                st.rerun()

        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "⚖️ Advokat", "📚 Artikel", "❓ FAQ"])

        with tab1:
            stat_cols = st.columns(4)
            stat_defs = [
                ("Total Konsultasi", db["stats"]["konsultasi"]),
                ("Total Advokat", len(db["advokat"])),
                ("Total Artikel", len(db["artikel"])),
                ("Total Pengguna", db["stats"]["pengguna"]),
            ]
            for c, (label, val) in zip(stat_cols, stat_defs):
                with c:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{val}</div>
                        <div class="stat-label">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.write("")
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