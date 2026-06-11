# Database untuk seluruh aplikasi

db = {
    "stats": {
        "konsultasi": 1248,
        "advokat": 48,
        "artikel": 10,
        "pengguna": 3200
    },
    "advokat": [
        # ==================== PULAU JAWA ====================
        # JAKARTA (10 advokat)
        {"id": 1, "nama": "Dr. Otto Hasibuan, S.H., M.H.", "spesialisasi": "Pidana", "pengalaman": "25 Tahun", "kota": "Jakarta", "telepon": "0811-888-1234", "email": "otto.hasibuan@lawyer.com", "rating": 4.9, "kasus": 500},
        {"id": 2, "nama": "Prof. Dr. Todung Mulya Lubis, S.H., LL.M.", "spesialisasi": "Perdata", "pengalaman": "30 Tahun", "kota": "Jakarta", "telepon": "0812-888-5678", "email": "todung@lawyer.com", "rating": 4.8, "kasus": 450},
        {"id": 3, "nama": "Hotman Paris Hutapea, S.H.", "spesialisasi": "Pidana", "pengalaman": "28 Tahun", "kota": "Jakarta", "telepon": "0811-111-3333", "email": "hotman@lawyer.com", "rating": 4.9, "kasus": 600},
        {"id": 4, "nama": "Rieke Diah Pitaloka, S.H.", "spesialisasi": "Keluarga", "pengalaman": "15 Tahun", "kota": "Jakarta", "telepon": "0812-999-7777", "email": "rieke@lawyer.com", "rating": 4.7, "kasus": 200},
        {"id": 5, "nama": "Fifi Lety Indra, S.H.", "spesialisasi": "Ketenagakerjaan", "pengalaman": "12 Tahun", "kota": "Jakarta", "telepon": "0813-888-5555", "email": "fifi@lawyer.com", "rating": 4.8, "kasus": 180},
        {"id": 6, "nama": "Petrus Bala Pattyona, S.H., M.H.", "spesialisasi": "Pidana", "pengalaman": "18 Tahun", "kota": "Jakarta", "telepon": "0812-222-3333", "email": "petrus@lawyer.com", "rating": 4.6, "kasus": 320},
        {"id": 7, "nama": "Maria Fransiska, S.H.", "spesialisasi": "Keluarga", "pengalaman": "10 Tahun", "kota": "Jakarta", "telepon": "0856-1111-2222", "email": "maria@lawyer.com", "rating": 4.7, "kasus": 150},
        {"id": 8, "nama": "Dr. Juniver Girsang, S.H., M.H.", "spesialisasi": "Perdata", "pengalaman": "20 Tahun", "kota": "Jakarta", "telepon": "0812-4444-5555", "email": "juniver@lawyer.com", "rating": 4.8, "kasus": 380},
        {"id": 9, "nama": "Luhut MP Pangaribuan, S.H.", "spesialisasi": "Pidana", "pengalaman": "22 Tahun", "kota": "Jakarta", "telepon": "0813-7777-8888", "email": "luhut@lawyer.com", "rating": 4.8, "kasus": 410},
        {"id": 10, "nama": "Indah Sari, S.H.", "spesialisasi": "Ketenagakerjaan", "pengalaman": "8 Tahun", "kota": "Jakarta", "telepon": "0857-2222-3333", "email": "indah@lawyer.com", "rating": 4.6, "kasus": 95},
        
        # BANDUNG (6 advokat)
        {"id": 11, "nama": "Ahmad Fauzi, S.H.", "spesialisasi": "Pidana", "pengalaman": "15 Tahun", "kota": "Bandung", "telepon": "0821-1234-5678", "email": "ahmad.fauzi@lawyer.com", "rating": 4.8, "kasus": 215},
        {"id": 12, "nama": "Dewi Sartika, S.H.", "spesialisasi": "Keluarga", "pengalaman": "10 Tahun", "kota": "Bandung", "telepon": "0856-7890-1234", "email": "dewi.sartika@lawyer.com", "rating": 4.9, "kasus": 178},
        {"id": 13, "nama": "Dr. H. Umar Said, S.H., M.H.", "spesialisasi": "Perdata", "pengalaman": "20 Tahun", "kota": "Bandung", "telepon": "0822-4444-5555", "email": "umar.said@lawyer.com", "rating": 4.7, "kasus": 290},
        {"id": 14, "nama": "Nina Herlina, S.H.", "spesialisasi": "Ketenagakerjaan", "pengalaman": "8 Tahun", "kota": "Bandung", "telepon": "0852-1111-2222", "email": "nina@lawyer.com", "rating": 4.6, "kasus": 112},
        {"id": 15, "nama": "Rudi Hermawan, S.H.", "spesialisasi": "Pidana", "pengalaman": "12 Tahun", "kota": "Bandung", "telepon": "0812-5555-6666", "email": "rudi@lawyer.com", "rating": 4.7, "kasus": 165},
        {"id": 16, "nama": "Tuti Alawiyah, S.H.", "spesialisasi": "Keluarga", "pengalaman": "9 Tahun", "kota": "Bandung", "telepon": "0857-3333-4444", "email": "tuti@lawyer.com", "rating": 4.8, "kasus": 145},
        
        # SURABAYA (6 advokat)
        {"id": 17, "nama": "H. M. Iksan, S.H.", "spesialisasi": "Pidana", "pengalaman": "20 Tahun", "kota": "Surabaya", "telepon": "0812-3456-7890", "email": "iksan@lawyer.com", "rating": 4.8, "kasus": 320},
        {"id": 18, "nama": "Susanti, S.H., M.Kn.", "spesialisasi": "Keluarga", "pengalaman": "12 Tahun", "kota": "Surabaya", "telepon": "0813-5678-1234", "email": "susanti@lawyer.com", "rating": 4.7, "kasus": 180},
        {"id": 19, "nama": "Dr. M. Syafi'i, S.H., M.H.", "spesialisasi": "Pidana", "pengalaman": "22 Tahun", "kota": "Surabaya", "telepon": "0823-1111-2222", "email": "syafii@lawyer.com", "rating": 4.9, "kasus": 410},
        {"id": 20, "nama": "Linda Kusuma, S.H.", "spesialisasi": "Ketenagakerjaan", "pengalaman": "9 Tahun", "kota": "Surabaya", "telepon": "0856-4444-5555", "email": "linda@lawyer.com", "rating": 4.6, "kasus": 132},
        {"id": 21, "nama": "Bambang Widodo, S.H.", "spesialisasi": "Perdata", "pengalaman": "15 Tahun", "kota": "Surabaya", "telepon": "0811-2222-3333", "email": "bambang@lawyer.com", "rating": 4.7, "kasus": 210},
        {"id": 22, "nama": "Siti Aisyah, S.H.", "spesialisasi": "Keluarga", "pengalaman": "10 Tahun", "kota": "Surabaya", "telepon": "0852-6666-7777", "email": "aisyah@lawyer.com", "rating": 4.8, "kasus": 156},
        
        # SEMARANG (5 advokat)
        {"id": 23, "nama": "Bambang Sutopo, S.H.", "spesialisasi": "Ketenagakerjaan", "pengalaman": "14 Tahun", "kota": "Semarang", "telepon": "0822-333-4444", "email": "bambang.sutopo@lawyer.com", "rating": 4.7, "kasus": 145},
        {"id": 24, "nama": "Sri Mulyani, S.H.", "spesialisasi": "Keluarga", "pengalaman": "11 Tahun", "kota": "Semarang", "telepon": "0857-8888-9999", "email": "sri.mulyani@lawyer.com", "rating": 4.8, "kasus": 178},
        {"id": 25, "nama": "Agus Wibowo, S.H.", "spesialisasi": "Perdata", "pengalaman": "16 Tahun", "kota": "Semarang", "telepon": "0824-5555-6666", "email": "agus@lawyer.com", "rating": 4.6, "kasus": 190},
        {"id": 26, "nama": "H. Zaenal Arifin, S.H.", "spesialisasi": "Pidana", "pengalaman": "18 Tahun", "kota": "Semarang", "telepon": "0812-7777-8888", "email": "zaenal@lawyer.com", "rating": 4.7, "kasus": 210},
        {"id": 27, "nama": "Dr. H. Nur Kholis, S.H., M.H.", "spesialisasi": "Perdata", "pengalaman": "20 Tahun", "kota": "Semarang", "telepon": "0813-2222-3333", "email": "nur.kholis@lawyer.com", "rating": 4.8, "kasus": 250},
        
        # YOGYAKARTA (4 advokat)
        {"id": 28, "nama": "Sri Wahyuni, S.H.", "spesialisasi": "Keluarga", "pengalaman": "13 Tahun", "kota": "Yogyakarta", "telepon": "0858-111-2222", "email": "sri.wahyuni@lawyer.com", "rating": 4.9, "kasus": 198},
        {"id": 29, "nama": "Dr. Muhammad Arif, S.H.", "spesialisasi": "Pidana", "pengalaman": "18 Tahun", "kota": "Yogyakarta", "telepon": "0812-7777-8888", "email": "arif@lawyer.com", "rating": 4.7, "kasus": 267},
        {"id": 30, "nama": "Ani Susilowati, S.H.", "spesialisasi": "Ketenagakerjaan", "pengalaman": "7 Tahun", "kota": "Yogyakarta", "telepon": "0857-3333-4444", "email": "ani@lawyer.com", "rating": 4.6, "kasus": 98},
        {"id": 31, "nama": "Budi Santoso, S.H.", "spesialisasi": "Perdata", "pengalaman": "10 Tahun", "kota": "Yogyakarta", "telepon": "0813-9999-1111", "email": "budi.s@lawyer.com", "rating": 4.7, "kasus": 145},
        
        # MALANG (3 advokat)
        {"id": 32, "nama": "Drs. H. Imam Suharto, S.H.", "spesialisasi": "Pidana", "pengalaman": "17 Tahun", "kota": "Malang", "telepon": "0821-9999-1111", "email": "imam@lawyer.com", "rating": 4.7, "kasus": 210},
        {"id": 33, "nama": "Nurul Hasanah, S.H.", "spesialisasi": "Keluarga", "pengalaman": "9 Tahun", "kota": "Malang", "telepon": "0856-2222-3333", "email": "nurul@lawyer.com", "rating": 4.8, "kasus": 132},
        {"id": 34, "nama": "H. Abdul Majid, S.H.", "spesialisasi": "Perdata", "pengalaman": "14 Tahun", "kota": "Malang", "telepon": "0812-4444-5555", "email": "majid@lawyer.com", "rating": 4.6, "kasus": 167},
        
        # DENPASAR (4 advokat)
        {"id": 35, "nama": "I Wayan Sudarsana, S.H.", "spesialisasi": "Pidana", "pengalaman": "17 Tahun", "kota": "Denpasar", "telepon": "0812-4444-5555", "email": "wayan.s@lawyer.com", "rating": 4.8, "kasus": 267},
        {"id": 36, "nama": "Ni Luh Putu Sukarniti, S.H.", "spesialisasi": "Keluarga", "pengalaman": "14 Tahun", "kota": "Denpasar", "telepon": "0823-8888-9999", "email": "sukarniti@lawyer.com", "rating": 4.9, "kasus": 198},
        {"id": 37, "nama": "Made Adi Putra, S.H.", "spesialisasi": "Perdata", "pengalaman": "11 Tahun", "kota": "Denpasar", "telepon": "0857-1111-2222", "email": "m.adi@lawyer.com", "rating": 4.7, "kasus": 156},
        {"id": 38, "nama": "Gede Purnama, S.H.", "spesialisasi": "Ketenagakerjaan", "pengalaman": "9 Tahun", "kota": "Denpasar", "telepon": "0813-5555-6666", "email": "gede@lawyer.com", "rating": 4.6, "kasus": 112},
        
        # MAKASSAR (4 advokat)
        {"id": 39, "nama": "Andi Zainal, S.H.", "spesialisasi": "Pidana", "pengalaman": "18 Tahun", "kota": "Makassar", "telepon": "0811-222-3333", "email": "zainal@lawyer.com", "rating": 4.8, "kasus": 310},
        {"id": 40, "nama": "Dr. Hj. Rasmina, S.H., M.H.", "spesialisasi": "Keluarga", "pengalaman": "16 Tahun", "kota": "Makassar", "telepon": "0823-5555-6666", "email": "rasmina@lawyer.com", "rating": 4.7, "kasus": 245},
        {"id": 41, "nama": "Muhammad Rusli, S.H.", "spesialisasi": "Perdata", "pengalaman": "14 Tahun", "kota": "Makassar", "telepon": "0852-7777-8888", "email": "rusli@lawyer.com", "rating": 4.6, "kasus": 189},
        {"id": 42, "nama": "St. Aisyah, S.H.", "spesialisasi": "Ketenagakerjaan", "pengalaman": "8 Tahun", "kota": "Makassar", "telepon": "0853-2222-3333", "email": "aisyah.m@lawyer.com", "rating": 4.6, "kasus": 98},
        
        # MEDAN (4 advokat)
        {"id": 43, "nama": "M. Yamin, S.H., M.H.", "spesialisasi": "Pidana", "pengalaman": "20 Tahun", "kota": "Medan", "telepon": "0812-999-1111", "email": "yamin@lawyer.com", "rating": 4.8, "kasus": 410},
        {"id": 44, "nama": "Hj. Fatimah, S.H.", "spesialisasi": "Keluarga", "pengalaman": "15 Tahun", "kota": "Medan", "telepon": "0821-5555-6666", "email": "fatimah@lawyer.com", "rating": 4.7, "kasus": 210},
        {"id": 45, "nama": "Rudi Hartono, S.H.", "spesialisasi": "Ketenagakerjaan", "pengalaman": "10 Tahun", "kota": "Medan", "telepon": "0853-7777-8888", "email": "rudi.h@lawyer.com", "rating": 4.6, "kasus": 145},
        {"id": 46, "nama": "Eka Prasetya, S.H.", "spesialisasi": "Perdata", "pengalaman": "12 Tahun", "kota": "Medan", "telepon": "0811-3333-4444", "email": "eka@lawyer.com", "rating": 4.6, "kasus": 167},
        
        # PALEMBANG (2 advokat)
        {"id": 47, "nama": "H. Zainal Abidin, S.H.", "spesialisasi": "Pidana", "pengalaman": "16 Tahun", "kota": "Palembang", "telepon": "0811-2222-3333", "email": "zainal@lawyer.com", "rating": 4.7, "kasus": 198},
        {"id": 48, "nama": "Rina Marlina, S.H.", "spesialisasi": "Perdata", "pengalaman": "10 Tahun", "kota": "Palembang", "telepon": "0823-4444-5555", "email": "rina.m@lawyer.com", "rating": 4.6, "kasus": 134},
    ],
    "artikel": [
        {
            "id": 1, 
            "judul": "Waspada Pinjaman Online Ilegal: Ciri-Ciri dan Cara Melaporkan", 
            "kategori": "Perdata", 
            "ringkasan": "Pinjol ilegal marak dengan bunga tinggi dan teror. Kenali ciri-cirinya dan laporkan ke OJK.", 
            "isi": "Pinjaman online ilegal menjadi momok bagi masyarakat. Ciri-cirinya: tidak terdaftar di OJK, bunga di atas 0.8% per hari, tenor pendek (7-14 hari), akses kontak pribadi, dan ancaman teror. Jika terjerat: jangan panik, blokir nomor penagih, laporkan ke OJK via 157 atau WhatsApp 0811-5715-7157, dan lapor polisi jika ada ancaman. Dasar hukum: POJK No.77/2016 dan Pasal 378 KUHP.", 
            "tanggal": "15 Mar 2026", 
            "penulis": "Tim LegalAssist", 
            "baca": 15420
        },
        {
            "id": 2, 
            "judul": "Modus Penipuan Belanja Online Terbaru 2026", 
            "kategori": "Pidana", 
            "ringkasan": "Penipuan belanja online makin canggih. Kenali modus terbaru dan cara melaporkannya.", 
            "isi": "Modus penipuan online yang marak: tautan palsu (phishing), penjual fiktif meminta transfer di luar aplikasi, barang palsu/tidak sesuai, dan COD palsu. Pencegahan: transaksi di marketplace resmi, jangan klik tautan mencurigakan, screenshot semua bukti. Jika menjadi korban: kumpulkan bukti, laporkan ke polisi via SPION online, blokir rekening penipu ke bank. Dasar hukum: Pasal 378 KUHP dan Pasal 28 UU ITE. Ingat: Semakin cepat melapor, semakin besar peluang uang kembali!", 
            "tanggal": "10 Mar 2026", 
            "penulis": "Tim LegalAssist", 
            "baca": 12890
        },
        {
            "id": 3, 
            "judul": "KDRT: Jangan Diam! Ini Langkah Hukum yang Bisa Anda Lakukan", 
            "kategori": "Keluarga", 
            "ringkasan": "Kekerasan dalam rumah tangga bukan aib. Kenali hak Anda dan langkah melaporkan.", 
            "isi": "KDRT meliputi kekerasan fisik (pukul, tendang), psikis (ancaman, hinaan), seksual, dan penelantaran. Langkah yang harus dilakukan: hubungi SAPA 129 (24 jam) nebo WA 08111-129-129, pergi ke rumah aman, minta visum ke puskesmas/RS, dokumentasikan luka (foto/video), kumpulkan saksi, lapor polisi ke Unit PPA. Nomor penting: Komnas Perempuan (021)390-3963/0811-171-7177, LBH APIK (021)877-9829. Dasar hukum: UU No.23/2004 tentang PKDRT.", 
            "tanggal": "5 Mar 2026", 
            "penulis": "Tim LegalAssist", 
            "baca": 9870
        },
        {
            "id": 4, 
            "judul": "Di-PHK Sepihak? Ini Hak Pesangon yang Wajib Perusahaan Bayar", 
            "kategori": "Ketenagakerjaan", 
            "ringkasan": "PHK sepihak sering terjadi. Ketahui hak pesangon Anda berdasarkan UU Cipta Kerja.", 
            "isi": "Hak pesangon jika di-PHK: Uang Pesangon (UP) berdasarkan masa kerja (1-9 bulan upah), Uang Penghargaan Masa Kerja (UPMK) untuk masa kerja 3-24 tahun (2-10 bulan upah), dan Uang Penggantian Hak (cuti tahunan, biaya pulang, dll). Dokumen yang perlu disiapkan: kontrak kerja, slip gaji 3 bulan terakhir, surat PHK. Jika perusahaan tidak membayar: laporkan ke Dinas Tenaga Kerja setempat nebo gugat ke PHI. Dasar hukum: UU Cipta Kerja No.11/2020 dan PP No.35/2021.", 
            "tanggal": "28 Feb 2026", 
            "penulis": "Tim LegalAssist", 
            "baca": 7650
        },
        {
            "id": 5, 
            "judul": "UU TPKS: Perlindungan Baru untuk Korban Pelecehan Seksual", 
            "kategori": "Keluarga", 
            "ringkasan": "UU Tindak Pidana Kekerasan Seksual (TPKS) hadir untuk melindungi korban.", 
            "isi": "UU TPKS No.12/2022 mengatur 9 jenis kekerasan seksual: pelecehan seksual, eksibisionisme, pemaksaan kontrasepsi/sterilisasi, pemaksaan perkawinan, perbudakan seksual, eksploitasi seksual, pemaksaan aborsi, pemerkosaan, dan tindakan seksual dengan anak. Hak korban: pendampingan psikologis, pendampingan hukum (advokat gratis), restitusi (ganti rugi), kerahasiaan identitas. Langkah: kumpulkan bukti, minta visum, hubungi SAPA 129 nebo Komnas Perempuan 0811-171-7177, lapor polisi. Dasar hukum: UU TPKS No.12/2022.", 
            "tanggal": "20 Feb 2026", 
            "penulis": "Tim LegalAssist", 
            "baca": 5430
        },
        {
            "id": 6, 
            "judul": "Modus Tipu Loker: Jangan Tertipu Lowongan Kerja Palsu!", 
            "kategori": "Ketenagakerjaan", 
            "ringkasan": "Penipuan lowongan kerja marak. Kenali ciri-cirinya dan laporkan ke polisi.", 
            "isi": "Ciri lowongan kerja palsu: memungut biaya pendaftaran (Rp50.000-Rp500.000), tidak ada wawancara langsung, janji gaji besar tanpa syarat, rekrutmen via WhatsApp/Telegram saja, mengatasnamakan perusahaan ternama. Modus yang sering terjadi: biaya administrasi, pelatihan berbayar, tugas pekerjaan gratis untuk 'tes'. Jika menjadi korban: screenshot semua bukti, catat identitas pelaku (nama, no HP, rekening), lapor ke polisi via SPION online, laporkan ke Dinas Tenaga Kerja setempat. Dasar hukum: Pasal 378 KUHP dan Pasal 28 UU ITE. Ingat: Rekrutmen resmi TIDAK PERNAH memungut biaya!", 
            "tanggal": "12 Feb 2026", 
            "penulis": "Tim LegalAssist", 
            "baca": 11230
        },
        {
            "id": 7, 
            "judul": "Dihina di Medsos? Kenali UU ITE dan Cara Melaporkannya", 
            "kategori": "Pidana", 
            "ringkasan": "Pencemaran nama baik di media sosial bisa dipidana. Simak panduan lengkapnya.", 
            "isi": "Pencemaran nama baik di media sosial diatur UU ITE. Pasal 27 ayat (3): pencemaran nama baik ancaman 4 tahun penjara. Pasal 28 ayat (2): menyebarkan berita bohong/hoax ancaman 6 tahun penjara. Pasal 45 ayat (1): konten asusila ancaman 6 tahun penjara. Langkah jika menjadi korban: screenshot semua bukti (jangan hapus!), simpan URL link, catat profil pelaku (username, nama), lapor ke polisi cyber (Direktorat Siber Bareskrim), lapor juga ke admin platform medsos (Instagram, TikTok, Facebook, X). Cara melapor: offline ke Polres terdekat nebo online via SPION https://spion.polri.go.id. Dasar hukum: UU No.19/2016 tentang ITE.", 
            "tanggal": "5 Feb 2026", 
            "penulis": "Tim LegalAssist", 
            "baca": 8760
        },
        {
            "id": 8, 
            "judul": "Sengketa Tanah Warisan: Panduan Hukum dan Penyelesaian", 
            "kategori": "Perdata", 
            "ringkasan": "Sengketa tanah warisan sering terjadi. Kenali cara penyelesaiannya secara hukum.", 
            "isi": "Penyebab sengketa tanah warisan: tidak ada surat wasiat yang jelas, ahli waris tidak setuju pembagian, tanah dikuasai oleh salah satu ahli waris, sertifikat tanah bermasalah (ganda/tumpang tindih), pewaris meninggal tanpa dokumen lengkap. Langkah penyelesaian: musyawarah keluarga (paling dianjurkan), mediasi dengan bantuan RT/RW nebo desa, gugatan ke Pengadilan Agama (jika pewaris Muslim), gugatan ke Pengadilan Negeri (jika non-Muslim). Dokumen yang diperlukan: sertifikat tanah/bukti kepemilikan, surat kematian pewaris, Kartu Keluarga dan KTP ahli waris, surat keterangan ahli waris dari kelurahan, akta kelahiran (untuk ahli waris). Dasar hukum: KUHPerdata Pasal 830-1130, Kompilasi Hukum Islam (KHI) untuk Muslim. Saran: selesaikan secara kekeluargaan dulu, pengadilan adalah jalan terakhir.", 
            "tanggal": "25 Jan 2026", 
            "penulis": "Tim LegalAssist", 
            "baca": 6540
        }
    ],
    "faq": [
        {"id": 1, "pertanyaan": "Apakah konsultasi di LegalAssist gratis?", "jawaban": "Ya, layanan chatbot konsultasi dasar di LegalAssist sepenuhnya gratis.", "kategori": "Umum"},
        {"id": 2, "pertanyaan": "Bagaimana cara menggunakan chatbot konsultasi?", "jawaban": "Klik menu 'Chatbot Konsultasi', kemudian ikuti panduan yang diberikan.", "kategori": "Chatbot"},
        {"id": 3, "pertanyaan": "Apakah informasi yang saya berikan terjaga kerahasiaannya?", "jawaban": "Kami menjaga privasi pengguna sesuai kebijakan privasi kami.", "kategori": "Privasi"},
        {"id": 4, "pertanyaan": "Bagaimana cara menghubungi advokat yang terdaftar?", "jawaban": "Kunjungi halaman 'Informasi Advokat', temukan advokat sesuai spesialisasi.", "kategori": "Advokat"},
        {"id": 5, "pertanyaan": "Apakah LegalAssist memberikan nasihat hukum resmi?", "jawaban": "LegalAssist memberikan informasi hukum edukatif, bukan nasihat hukum resmi.", "kategori": "Umum"},
        {"id": 6, "pertanyaan": "Apa yang harus dilakukan jika menjadi korban pinjol ilegal?", "jawaban": "Laporkan ke OJK via 157, blokir nomor penagih, dan lapor polisi jika ada ancaman.", "kategori": "Perdata"},
        {"id": 7, "pertanyaan": "Bagaimana cara melapor jika mengalami KDRT?", "jawaban": "Hubungi SAPA 129, minta visum ke puskesmas, kumpulkan bukti, lalu lapor polisi.", "kategori": "Keluarga"},
        {"id": 8, "pertanyaan": "Apakah hak saya jika di-PHK?", "jawaban": "Anda berhak atas pesangon, uang penghargaan masa kerja, dan uang penggantian hak.", "kategori": "Ketenagakerjaan"},
        {"id": 9, "pertanyaan": "Bagaimana cara melapor penipuan online?", "jawaban": "Kumpulkan bukti screenshot dan transfer, lalu lapor ke polisi via SPION online.", "kategori": "Pidana"},
        {"id": 10, "pertanyaan": "Nomor darurat apa yang bisa dihubungi untuk kasus kekerasan?", "jawaban": "SAPA 129, Komnas Perempuan 0811-171-7177, atau polisi 110.", "kategori": "Keluarga"},
        {"id": 11, "pertanyaan": "Apa itu Pasal 378 KUHP?", "jawaban": "Pasal 378 KUHP adalah pasal tentang penipuan. Ancaman pidana maksimal 4 tahun penjara.", "kategori": "Pidana"},
        {"id": 12, "pertanyaan": "Berapa biaya lapor ke polisi?", "jawaban": "Lapor ke polisi GRATIS 100%! Tidak dipungut biaya apapun.", "kategori": "Umum"}
    ],
    "pesan": [
        {"id": 1, "nama": "Andi Wijaya", "email": "andi@email.com", "subjek": "Pertanyaan tentang kasus PHK", "pesan": "Saya ingin berkonsultasi lebih lanjut mengenai kasus PHK.", "tanggal": "10 Jan 2025", "status": "Sudah dibaca"},
        {"id": 2, "nama": "Rina Sari", "email": "rina@email.com", "subjek": "Bantuan kasus penipuan online", "pesan": "Saya menjadi korban penipuan belanja online.", "tanggal": "12 Jan 2025", "status": "Belum dibaca"},
    ],
    "admin": {
        "username": "admin",
        "password": "admin123",
        "logged_in": False
    }
}