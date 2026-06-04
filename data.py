# Database untuk seluruh aplikasi

db = {
    "stats": {
        "konsultasi": 1248,
        "advokat": 45,
        "artikel": 87,
        "pengguna": 3200
    },
    "advokat": [
        {"id": 1, "nama": "Dr. Budi Santoso, S.H., M.H.", "spesialisasi": "Pidana", "pengalaman": "15 Tahun", "kota": "Jakarta", "telepon": "0812-3456-7890", "email": "budi.santoso@legalassist.id", "rating": 4.9, "kasus": 320},
        {"id": 2, "nama": "Siti Rahayu, S.H.", "spesialisasi": "Perdata", "pengalaman": "10 Tahun", "kota": "Bandung", "telepon": "0821-1234-5678", "email": "siti.rahayu@legalassist.id", "rating": 4.8, "kasus": 215},
        {"id": 3, "nama": "Ahmad Fauzi, S.H., M.Kn.", "spesialisasi": "Keluarga", "pengalaman": "12 Tahun", "kota": "Surabaya", "telepon": "0831-9876-5432", "email": "ahmad.fauzi@legalassist.id", "rating": 4.7, "kasus": 180},
        {"id": 4, "nama": "Dewi Lestari, S.H.", "spesialisasi": "Ketenagakerjaan", "pengalaman": "8 Tahun", "kota": "Semarang", "telepon": "0856-1122-3344", "email": "dewi.lestari@legalassist.id", "rating": 4.9, "kasus": 145},
        {"id": 5, "nama": "Ricky Prasetyo, S.H., M.H.", "spesialisasi": "Pidana", "pengalaman": "20 Tahun", "kota": "Medan", "telepon": "0878-5566-7788", "email": "ricky.p@legalassist.id", "rating": 5.0, "kasus": 410},
        {"id": 6, "nama": "Nadia Kusuma, S.H.", "spesialisasi": "Perdata", "pengalaman": "6 Tahun", "kota": "Yogyakarta", "telepon": "0895-4433-2211", "email": "nadia.k@legalassist.id", "rating": 4.6, "kasus": 98},
    ],
    "artikel": [
        {"id": 1, "judul": "Memahami Hak-Hak Anda Saat Ditangkap Polisi", "kategori": "Pidana", "ringkasan": "Ketika seseorang ditangkap oleh aparat penegak hukum, ada hak-hak dasar yang wajib dipenuhi.", "isi": "Saat ditangkap polisi, Anda memiliki beberapa hak penting yang dijamin oleh hukum Indonesia. Pertama, hak untuk mengetahui alasan penangkapan. Kedua, hak untuk mendapatkan pengacara. Ketiga, hak untuk diam dan tidak memberatkan diri sendiri. Keempat, hak untuk diberitahu kepada keluarga. Hak-hak ini diatur dalam KUHAP dan wajib dihormati oleh setiap aparat penegak hukum.", "tanggal": "12 Jan 2025", "penulis": "Dr. Budi Santoso", "baca": 1240},
        {"id": 2, "judul": "Prosedur Mengajukan Gugatan Perdata di Pengadilan", "kategori": "Perdata", "ringkasan": "Gugatan perdata adalah upaya hukum seseorang untuk memperoleh haknya melalui pengadilan.", "isi": "Mengajukan gugatan perdata memerlukan beberapa langkah penting. Pertama, siapkan surat gugatan yang memuat identitas para pihak, posita (uraian fakta), dan petitum (tuntutan). Kedua, daftarkan gugatan ke Pengadilan Negeri yang berwenang. Ketiga, bayar biaya perkara. Keempat, tunggu panggilan sidang.", "tanggal": "15 Jan 2025", "penulis": "Siti Rahayu", "baca": 890},
        {"id": 3, "judul": "Panduan Hukum Perceraian: Hak dan Kewajiban", "kategori": "Keluarga", "ringkasan": "Perceraian adalah proses hukum yang kompleks. Ketahui hak dan kewajiban Anda.", "isi": "Perceraian di Indonesia dapat dilakukan melalui dua cara: cerai talak (bagi suami Muslim) dan cerai gugat (bagi istri). Prosesnya melibatkan Pengadilan Agama untuk pasangan Muslim dan Pengadilan Negeri untuk non-Muslim.", "tanggal": "18 Jan 2025", "penulis": "Ahmad Fauzi", "baca": 2100},
        {"id": 4, "judul": "PHK Sepihak: Apa Yang Harus Anda Lakukan?", "kategori": "Ketenagakerjaan", "ringkasan": "Di-PHK secara tiba-tiba? Ada langkah-langkah hukum yang bisa Anda tempuh.", "isi": "Jika Anda mengalami PHK sepihak, langkah pertama adalah meminta surat PHK secara tertulis dari perusahaan. Selanjutnya, hitung hak Anda berdasarkan masa kerja sesuai UU Cipta Kerja.", "tanggal": "20 Jan 2025", "penulis": "Dewi Lestari", "baca": 3400},
        {"id": 5, "judul": "Mengenal Jenis-Jenis Tindak Pidana Siber", "kategori": "Pidana", "ringkasan": "Di era digital, kejahatan siber semakin marak. Kenali jenis-jenisnya.", "isi": "Tindak pidana siber di Indonesia diatur dalam UU ITE. Beberapa jenis kejahatan siber antara lain: penipuan online, pencemaran nama baik digital, akses ilegal ke sistem komputer.", "tanggal": "22 Jan 2025", "penulis": "Ricky Prasetyo", "baca": 1875},
        {"id": 6, "judul": "Hak Pekerja dalam Perjanjian Kerja Waktu Tertentu", "kategori": "Ketenagakerjaan", "ringkasan": "PKWT atau kontrak kerja memiliki aturan tersendiri.", "isi": "Perjanjian Kerja Waktu Tertentu (PKWT) diatur dalam UU Cipta Kerja. Pekerja PKWT berhak mendapatkan kompensasi saat kontrak berakhir.", "tanggal": "25 Jan 2025", "penulis": "Dewi Lestari", "baca": 1200},
    ],
    "faq": [
        {"id": 1, "pertanyaan": "Apakah konsultasi di LegalAssist gratis?", "jawaban": "Ya, layanan chatbot konsultasi dasar di LegalAssist sepenuhnya gratis.", "kategori": "Umum"},
        {"id": 2, "pertanyaan": "Bagaimana cara menggunakan chatbot konsultasi?", "jawaban": "Klik menu 'Chatbot Konsultasi', kemudian ikuti panduan yang diberikan.", "kategori": "Chatbot"},
        {"id": 3, "pertanyaan": "Apakah informasi yang saya berikan terjaga kerahasiaannya?", "jawaban": "Kami menjaga privasi pengguna sesuai kebijakan privasi kami.", "kategori": "Privasi"},
        {"id": 4, "pertanyaan": "Bagaimana cara menghubungi advokat yang terdaftar?", "jawaban": "Kunjungi halaman 'Informasi Advokat', temukan advokat sesuai spesialisasi.", "kategori": "Advokat"},
        {"id": 5, "pertanyaan": "Apakah LegalAssist memberikan nasihat hukum resmi?", "jawaban": "LegalAssist memberikan informasi hukum edukatif, bukan nasihat hukum resmi.", "kategori": "Umum"},
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