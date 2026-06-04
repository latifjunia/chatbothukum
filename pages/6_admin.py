import streamlit as st
from data import db
from datetime import datetime

st.set_page_config(
    page_title="Admin Panel - LegalAssist",
    page_icon="🔒",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .admin-header {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
    }
    .admin-header h1 {
        margin: 0;
        font-size: 2rem;
    }
    .admin-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 0.75rem;
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    .stat-number {
        font-size: 1.75rem;
        font-weight: bold;
        color: #4f46e5;
    }
    .admin-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize login state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# Header
st.markdown("""
<div class="admin-header">
    <h1>🔒 Panel Administrator</h1>
    <p>Kelola advokat, artikel, FAQ, dan pesan masuk</p>
</div>
""", unsafe_allow_html=True)

# Login form
if not st.session_state.admin_logged_in:
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="admin-card">', unsafe_allow_html=True)
            st.markdown("### 🔐 Login Administrator")
            
            with st.form("admin_login"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", use_container_width=True)
                
                if submitted:
                    if username == db["admin"]["username"] and password == db["admin"]["password"]:
                        st.session_state.admin_logged_in = True
                        st.session_state.admin_name = "Administrator"
                        st.success("Login berhasil!")
                        st.rerun()
                    else:
                        st.error("Username atau password salah.")
            
            st.markdown("</div>", unsafe_allow_html=True)
else:
    # Logout button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()
    
    st.success(f"Selamat datang, {st.session_state.admin_name}!")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "👨‍⚖️ Advokat", "📚 Artikel", "❓ FAQ", "📧 Pesan"])
    
    # ==================== TAB 1: DASHBOARD ====================
    with tab1:
        st.markdown("### Statistik Website")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{db['stats']['konsultasi']}</div>
                <div>Total Konsultasi</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(db['advokat'])}</div>
                <div>Total Advokat</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(db['artikel'])}</div>
                <div>Total Artikel</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            pesan_baru = len([p for p in db["pesan"] if p["status"] == "Belum dibaca"])
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{pesan_baru}</div>
                <div>Pesan Baru</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📊 Statistik Spesialisasi Advokat")
        
        # Count by spesialisasi
        spesialisasi_count = {}
        for adv in db["advokat"]:
            spesialisasi_count[adv["spesialisasi"]] = spesialisasi_count.get(adv["spesialisasi"], 0) + 1
        
        for spec, count in spesialisasi_count.items():
            st.progress(count / len(db["advokat"]), text=f"{spec}: {count} advokat")
        
        st.markdown("---")
        st.markdown("### 📈 Statistik Kategori Artikel")
        
        kategori_count = {}
        for art in db["artikel"]:
            kategori_count[art["kategori"]] = kategori_count.get(art["kategori"], 0) + 1
        
        for kat, count in kategori_count.items():
            st.progress(count / len(db["artikel"]), text=f"{kat}: {count} artikel")
    
    # ==================== TAB 2: ADVOKAT CRUD ====================
    with tab2:
        st.markdown("### 👨‍⚖️ Kelola Advokat")
        
        # Display existing advokat
        st.markdown("#### Daftar Advokat Saat Ini")
        
        for adv in db["advokat"]:
            with st.expander(f"📌 {adv['nama']} - {adv['spesialisasi']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**ID:** {adv['id']}")
                    st.write(f"**Nama:** {adv['nama']}")
                    st.write(f"**Spesialisasi:** {adv['spesialisasi']}")
                    st.write(f"**Pengalaman:** {adv['pengalaman']}")
                    st.write(f"**Kota:** {adv['kota']}")
                    st.write(f"**Telepon:** {adv['telepon']}")
                    st.write(f"**Email:** {adv['email']}")
                    st.write(f"**Rating:** {adv['rating']} ⭐")
                    st.write(f"**Kasus:** {adv['kasus']}")
                with col2:
                    if st.button("🗑️ Hapus", key=f"del_adv_{adv['id']}"):
                        db["advokat"] = [a for a in db["advokat"] if a["id"] != adv["id"]]
                        st.success(f"Advokat {adv['nama']} berhasil dihapus!")
                        st.rerun()
        
        st.markdown("---")
        st.markdown("#### Tambah Advokat Baru")
        
        with st.form("tambah_advokat"):
            col1, col2 = st.columns(2)
            with col1:
                nama_baru = st.text_input("Nama Lengkap")
                spesialisasi_baru = st.selectbox("Spesialisasi", ["Pidana", "Perdata", "Keluarga", "Ketenagakerjaan"])
                pengalaman_baru = st.text_input("Pengalaman (contoh: 10 Tahun)")
                kota_baru = st.text_input("Kota")
            with col2:
                telepon_baru = st.text_input("Telepon")
                email_baru = st.text_input("Email")
                rating_baru = st.slider("Rating (1-5)", 1.0, 5.0, 5.0, 0.1)
                kasus_baru = st.number_input("Jumlah Kasus Ditangani", min_value=0, value=0)
            
            submitted = st.form_submit_button("Tambah Advokat", use_container_width=True)
            
            if submitted:
                if nama_baru and telepon_baru and email_baru:
                    baru = {
                        "id": len(db["advokat"]) + 1,
                        "nama": nama_baru,
                        "spesialisasi": spesialisasi_baru,
                        "pengalaman": pengalaman_baru or "Baru",
                        "kota": kota_baru or "Jakarta",
                        "telepon": telepon_baru,
                        "email": email_baru,
                        "rating": rating_baru,
                        "kasus": kasus_baru
                    }
                    db["advokat"].append(baru)
                    st.success(f"✅ Advokat {nama_baru} berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error("Nama, Telepon, dan Email wajib diisi.")
    
    # ==================== TAB 3: ARTIKEL CRUD ====================
    with tab3:
        st.markdown("### 📚 Kelola Artikel")
        
        # Display existing articles
        st.markdown("#### Daftar Artikel Saat Ini")
        
        for art in db["artikel"]:
            with st.expander(f"📄 {art['judul']} - {art['kategori']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**ID:** {art['id']}")
                    st.write(f"**Judul:** {art['judul']}")
                    st.write(f"**Kategori:** {art['kategori']}")
                    st.write(f"**Penulis:** {art['penulis']}")
                    st.write(f"**Tanggal:** {art['tanggal']}")
                    st.write(f"**Dibaca:** {art['baca']} kali")
                    st.write(f"**Isi:** {art['isi'][:200]}...")
                with col2:
                    if st.button("🗑️ Hapus", key=f"del_art_{art['id']}"):
                        db["artikel"] = [a for a in db["artikel"] if a["id"] != art["id"]]
                        st.success(f"Artikel {art['judul']} berhasil dihapus!")
                        st.rerun()
        
        st.markdown("---")
        st.markdown("#### Tambah Artikel Baru")
        
        with st.form("tambah_artikel"):
            judul_baru = st.text_input("Judul Artikel")
            kategori_baru = st.selectbox("Kategori", ["Pidana", "Perdata", "Keluarga", "Ketenagakerjaan"])
            isi_baru = st.text_area("Isi Artikel", height=200, help="Tulis konten artikel lengkap di sini")
            penulis_baru = st.text_input("Penulis", value="Admin")
            
            submitted = st.form_submit_button("Tambah Artikel", use_container_width=True)
            
            if submitted:
                if judul_baru and isi_baru:
                    baru = {
                        "id": len(db["artikel"]) + 1,
                        "judul": judul_baru,
                        "kategori": kategori_baru,
                        "isi": isi_baru,
                        "ringkasan": isi_baru[:150] + "..." if len(isi_baru) > 150 else isi_baru,
                        "tanggal": datetime.now().strftime("%d %b %Y"),
                        "penulis": penulis_baru,
                        "baca": 0
                    }
                    db["artikel"].append(baru)
                    st.success(f"✅ Artikel {judul_baru} berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error("Judul dan Isi Artikel wajib diisi.")
    
    # ==================== TAB 4: FAQ CRUD ====================
    with tab4:
        st.markdown("### ❓ Kelola FAQ")
        
        # Display existing FAQs
        st.markdown("#### Daftar FAQ Saat Ini")
        
        for faq in db["faq"]:
            with st.expander(f"📌 {faq['pertanyaan']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**ID:** {faq['id']}")
                    st.write(f"**Pertanyaan:** {faq['pertanyaan']}")
                    st.write(f"**Jawaban:** {faq['jawaban']}")
                    st.write(f"**Kategori:** {faq['kategori']}")
                with col2:
                    if st.button("🗑️ Hapus", key=f"del_faq_{faq['id']}"):
                        db["faq"] = [f for f in db["faq"] if f["id"] != faq["id"]]
                        st.success(f"FAQ berhasil dihapus!")
                        st.rerun()
        
        st.markdown("---")
        st.markdown("#### Tambah FAQ Baru")
        
        with st.form("tambah_faq"):
            pertanyaan_baru = st.text_input("Pertanyaan")
            jawaban_baru = st.text_area("Jawaban", height=100)
            kategori_baru = st.text_input("Kategori", value="Umum")
            
            submitted = st.form_submit_button("Tambah FAQ", use_container_width=True)
            
            if submitted:
                if pertanyaan_baru and jawaban_baru:
                    baru = {
                        "id": len(db["faq"]) + 1,
                        "pertanyaan": pertanyaan_baru,
                        "jawaban": jawaban_baru,
                        "kategori": kategori_baru
                    }
                    db["faq"].append(baru)
                    st.success(f"✅ FAQ berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error("Pertanyaan dan Jawaban wajib diisi.")
    
    # ==================== TAB 5: PESAN ====================
    with tab5:
        st.markdown("### 📧 Pesan Masuk")
        
        if not db["pesan"]:
            st.info("Belum ada pesan masuk.")
        else:
            for pesan in db["pesan"][::-1]:
                with st.expander(f"📧 {pesan['subjek']} - {pesan['nama']} ({pesan['tanggal']})"):
                    st.write(f"**Nama:** {pesan['nama']}")
                    st.write(f"**Email:** {pesan['email']}")
                    st.write(f"**Subjek:** {pesan['subjek']}")
                    st.write(f"**Tanggal:** {pesan['tanggal']}")
                    st.write(f"**Status:** {pesan['status']}")
                    st.write("---")
                    st.write(f"**Pesan:**")
                    st.write(pesan['pesan'])
                    
                    if pesan['status'] == "Belum dibaca":
                        pesan['status'] = "Sudah dibaca"
                        st.rerun()