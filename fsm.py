import re

# =====================================================================
# ARTIKEL REDIRECT - mapping kasus ke artikel yang relevan
# =====================================================================
ARTIKEL_LINK = {
    "penipuan_online": {"id": 2, "judul": "Modus Penipuan Belanja Online: Kenali dan Laporkan!"},
    "penipuan":        {"id": 2, "judul": "Modus Penipuan Belanja Online: Kenali dan Laporkan!"},
    "tipu_loker":      {"id": 6, "judul": "Modus Tipu Lowongan Kerja: Jangan Tertipu!"},
    "kdrt":            {"id": 3, "judul": "KDRT: Jangan Diam! Ini Langkah Hukum yang Bisa Anda Lakukan"},
    "pelecehan":       {"id": 5, "judul": "UU TPKS: Perlindungan Baru untuk Korban Pelecehan Seksual"},
    "phk":             {"id": 4, "judul": "Di-PHK Sepihak? Ini Hak Pesangon yang Wajib Perusahaan Bayar"},
    "ite":             {"id": 7, "judul": "Dihina di Medsos? Kenali UU ITE dan Cara Melaporkannya"},
    "pencemaran":      {"id": 7, "judul": "Dihina di Medsos? Kenali UU ITE dan Cara Melaporkannya"},
    "tanah":           {"id": 8, "judul": "Sengketa Tanah Warisan: Panduan Hukum dan Penyelesaien"},
    "pinjol":          {"id": 1, "judul": "Waspada Pinjaman Online Ilegal: Ciri-Ciri dan Cara Melaporkan"},
    "kekerasan":       {"id": 5, "judul": "UU TPKS: Perlindungan Baru untuk Korban Pelecehan Seksual"},
    "pencurian":       {"id": 9, "judul": "Hak Korban Pencurian dan Cara Melaporkannya ke Polisi"},
    "penganiayaan":    {"id": 9, "judul": "Hak Korban Pencurian dan Cara Melaporkannya ke Polisi"},
    "upah":            {"id": 4, "judul": "Di-PHK Sepihak? Ini Hak Pesangon yang Wajib Perusahaan Bayar"},
    "hutang":          {"id": 8, "judul": "Sengketa Tanah Warisan: Panduan Hukum dan Penyelesaien"},
    "cerai":           {"id": 10, "judul": "Panduan Perceraian: Prosedur, Hak, dan Kewajiban"},
}

# =====================================================================
# HOTLINE DARURAT
# =====================================================================
HOTLINE_TEXT = (
    "\n📞 **Nomor Darurat (24 jam):**\n"
    "• **SAPA 129** (kekerasan perempuan & anak) — WA 08111-129-129\n"
    "• **Komnas Perempuan** — (021) 390-3963 / 0811-171-7177\n"
    "• **KPAI** (perlindungan anak) — (021) 319-01555\n"
    "• **LBH APIK** (bantuan hukum perempuan) — (021) 877-9829\n"
    "• **Polisi** — 110\n"
    "• **OJK** (pinjol ilegal) — 157 / WA 0811-5715-7157\n"
)


class LegalFSM:
    def __init__(self):
        self.state = "START"
        self.conversation_history = []
        self.context = {}

    def reset(self):
        self.state = "START"
        self.conversation_history = []
        self.context = {}

    def add_to_history(self, role, content):
        self.conversation_history.append({"role": role, "content": content})
        if len(self.conversation_history) > 30:
            self.conversation_history.pop(0)

    def _match(self, text, *keywords):
        t = text.lower()
        return any(kw.lower() in t for kw in keywords)

    def _tanya(self, text):
        return {"type": "question", "text": text}

    def _info(self, text):
        return {"type": "info", "text": text}

    def _hasil(self, title, pasal, kategori, text, dokumen, advokat, artikel_key=None):
        r = {
            "type": "result",
            "title": title,
            "pasal": pasal,
            "kategori": kategori,
            "text": text,
            "dokumen": dokumen,
            "advokat": advokat,
        }
        if artikel_key and artikel_key in ARTIKEL_LINK:
            r["artikel"] = ARTIKEL_LINK[artikel_key]
            r["artikel_link"] = artikel_key
        return r

    def _menu_utama(self, intro=None):
        return {
            "type": "menu",
            "title": "Menu Utama",
            "icon": "home",
            "text": intro or (
                "⚖️ **Halo! Saya LegalBot.**\n\n"
                "Ceritakan masalah hukum yang sedang kamu alami.\n\n"
                "📌 Contoh:\n\n"
                "- Aku ditipu beli HP online\n"
                "- Suamiku suka mukul aku\n"
                "- Gajiku 3 bulan nggak dibayar\n"
                "- Aku dilecehkan di kantor\n"
                "- Kena tipu lowongan kerja\n\n"
                "Silakan pilih kategori di bawah."
            ),
            "options": [
                {"key": "1", "label": "⚖️ Hukum Pidana"},
                {"key": "2", "label": "📋 Perdata & Ketenagakerjaan"},
                {"key": "3", "label": "👨‍👩‍👧 Keluarga & Perempuan"},
                {"key": "4", "label": "🆘 Bantuan Hukum"},
            ],
        }

    def _menu_pidana(self):
        return {"type": "menu", "title": "Hukum Pidana", "icon": "pidana", "text": "⚖️ **Pilih kasus pidana:**", "options": [{"key": "a", "label": "Penipuan"}, {"key": "b", "label": "Penipuan Online"}, {"key": "c", "label": "Pencurian"}, {"key": "d", "label": "Penganiayaan"}, {"key": "e", "label": "Pencemaran Nama Baik / ITE"}, {"key": "0", "label": "← Kembali"}]}

    def _menu_perdata(self):
        return {"type": "menu", "title": "Hukum Perdata", "icon": "perdata", "text": "📋 **Pilih kasus:**", "options": [{"key": "a", "label": "Sengketa Tanah"}, {"key": "b", "label": "Hutang Piutang"}, {"key": "c", "label": "Tipu Loker"}, {"key": "d", "label": "Gaji Tidak Dibayar"}, {"key": "e", "label": "PHK"}, {"key": "f", "label": "Perselisihan Kerja"}, {"key": "g", "label": "Pinjol Ilegal"}, {"key": "0", "label": "← Kembali"}]}

    def _menu_keluarga(self):
        return {"type": "menu", "title": "Perlindungan Keluarga", "icon": "keluarga", "text": "👨‍👩‍👧 **Pilih kasus:**", "options": [{"key": "a", "label": "Perceraian"}, {"key": "b", "label": "Hak Asuh Anak"}, {"key": "c", "label": "KDRT"}, {"key": "d", "label": "Kekerasan Perempuan"}, {"key": "e", "label": "Kekerasan Anak"}, {"key": "f", "label": "Pelecehan Seksual"}, {"key": "0", "label": "← Kembali"}]}

    def _kontak_bantuan(self):
        return {
            "type": "result",
            "title": "Kontak Bantuan Hukum & Darurat",
            "pasal": "-",
            "kategori": "bantuan",
            "text": "📞 **HOTLINE NASIONAL (24 JAM):**\n\n"
                    "1. 🆘 **SAPA 129** — kekerasan perempuan & anak\n"
                    "   Telepon: 129 | WA: 08111-129-129\n\n"
                    "2. 👮 **POLRI** — 110 | https://polri.go.id/\n\n"
                    "3. ♀️ **KOMNAS PEREMPUAN** — (021) 390-3963 / 0811-129-129\n\n"
                    "4. 👶 **KPAI** — (024)31901556\n\n"
                    "5. ⚖️ **LBH APIK** — (024) 3510499\n\n"
                    "6. 💰 **OJK** — 157 / WA 0811-5715-7157 (pinjol ilegal)\n\n"
                    "💡 Semua layanan ini RAHASIA dan GRATIS!",
            "dokumen": [],
            "advokat": "Hubungi hotline sesuai kasus",
        }

    def _handle_advokat(self, ui_low):
        kota_list = ["jakarta", "surabaya", "bandung", "medan", "semarang", "makassar", "yogyakarta", "malang", "denpasar", "palembang"]
        for kota in kota_list:
            if kota in ui_low:
                return self._rekomendasi_advokat_by_city(kota)
        self.state = "TANYA_DOMISILI"
        return self._tanya("📍 Kamu lagi di kota mana? Biar aku kasih rekomendasi advokat terdekat. Contoh: Jakarta, Surabaya, Bandung, Semarang")

    def _state_tanya_domisili(self, ui, ui_low):
        self.state = "START"
        return self._rekomendasi_advokat_by_city(ui.title())

    def _rekomendasi_advokat_by_city(self, kota):
        kota_lower = kota.lower()
        data = {
            "jakarta": [
                {"nama": "Dr. Otto Hasibuan, S.H., M.H.", "spesialisasi": "Pidana & HAM", "telepon": "0811-888-1234", "alamat": "Jl. MH Thamrin No. 10, Jakarta Pusat"},
                {"nama": "Prof. Dr. Todung Mulya Lubis, S.H., LL.M.", "spesialisasi": "Perdata & HAM", "telepon": "0812-888-5678", "alamat": "Jl. Diponegoro No. 25, Jakarta Selatan"},
            ],
            "surabaya": [
                {"nama": "H. M. Iksan, S.H.", "spesialisasi": "Pidana", "telepon": "0812-3456-7890", "alamat": "Jl. Pemuda No. 15, Surabaya"},
            ],
            "bandung": [
                {"nama": "Ahmad Fauzi, S.H.", "spesialisasi": "Pidana", "telepon": "0821-1234-5678", "alamat": "Jl. Asia Afrika No. 20, Bandung"},
            ],
            "semarang": [
                {"nama": "Bambang Sutopo, S.H.", "spesialisasi": "Ketenagakerjaan", "telepon": "0822-333-4444", "alamat": "Jl. Pandanaran No. 12, Semarang"},
                {"nama": "Sri Mulyani, S.H.", "spesialisasi": "Keluarga", "telepon": "0857-8888-9999", "alamat": "Jl. Pahlawan No. 20, Semarang"},
                {"nama": "Agus Wibowo, S.H.", "spesialisasi": "Perdata", "telepon": "0824-5555-6666", "alamat": "Jl. Simpang Lima No. 5, Semarang"},
                {"nama": "H. Zaenal Arifin, S.H.", "spesialisasi": "Pidana", "telepon": "0812-7777-8888", "alamat": "Jl. MT Haryono No. 50, Semarang"},
                {"nama": "Dr. H. Nur Kholis, S.H., M.H.", "spesialisasi": "Perdata Pertanahan", "telepon": "0813-2222-3333", "alamat": "Jl. Gajah Mada No. 25, Semarang"},
            ],
            "medan": [
                {"nama": "M. Yamin, S.H., M.H.", "spesialisasi": "Pidana & Perdata", "telepon": "0812-999-1111", "alamat": "Jl. Sudirman No. 30, Medan"},
            ],
            "yogyakarta": [
                {"nama": "Sri Wahyuni, S.H.", "spesialisasi": "Keluarga & Perdata", "telepon": "0858-111-2222", "alamat": "Jl. Malioboro No. 5, Yogyakarta"},
            ],
            "malang": [
                {"nama": "Drs. H. Imam Suharto, S.H.", "spesialisasi": "Pidana", "telepon": "0821-9999-1111", "alamat": "Jl. Ijen No. 8, Malang"},
            ],
            "denpasar": [
                {"nama": "I Wayan Sudarsana, S.H.", "spesialisasi": "Pidana", "telepon": "0812-4444-5555", "alamat": "Jl. Teuku Umar No. 10, Denpasar"},
            ],
            "makassar": [
                {"nama": "Andi Zainal, S.H.", "spesialisasi": "Pidana", "telepon": "0811-222-3333", "alamat": "Jl. Urip Sumoharjo No. 8, Makassar"},
            ],
            "palembang": [
                {"nama": "H. Zainal Abidin, S.H.", "spesialisasi": "Pidana", "telepon": "0811-2222-3333", "alamat": "Jl. Jend. Sudirman No. 15, Palembang"},
            ],
        }
        for city_key, advokats in data.items():
            if city_key in kota_lower or kota_lower in city_key:
                text = f"📍 **Rekomendasi Advokat di {kota.title()}:**\n\n"
                for adv in advokats:
                    text += f"👨‍⚖️ **{adv['nama']}**\n"
                    text += f"   📌 Spesialisasi: {adv['spesialisasi']}\n"
                    text += f"   📞 Telepon: {adv['telepon']}\n"
                    text += f"   🏢 Alamat: {adv['alamat']}\n\n"
                text += "💡 **Tips:** Hubungi dulu untuk konsultasi awal. Tanyakan biaya jasa.\n"
                text += "💰 Jika tidak mampu, minta **bantuan hukum gratis (pro bono)** ke LBH terdekat.\n\n"
                text += "Ketik **menu** untuk kembali."
                return {"type": "result", "title": f"Advokat di {kota.title()}", "pasal": "-", "kategori": "bantuan", "text": text, "dokumen": ["KTP", "Dokumen kasus"], "advokat": "Sesuai spesialisasi"}
        return self._info(f"📌 Maaf, belum ada data advokat untuk {kota.title()}.\n\nKamu bisa cari di peradi.or.id atau hubungi Posbakum di pengadilan terdekat.\n\nKetik **menu** untuk kembali.")

    def _hasil_kekerasan_anak(self):
        return self._hasil(
            "Kekerasan Terhadap Anak",
            "UU Perlindungan Anak No. 35/2014",
            "keluarga",
            "⚠️ **Kekerasan terhadap anak wajib dilaporin!**\n\n"
            "Pelaku bisa dipenjara sampe 15 tahun.\n\n"
            "**Langkah:**\n"
            "1. Bawa anak ke dokter/psikolog\n"
            "2. Jauhkan anak dari pelaku\n"
            "3. Lapor ke polisi (Unit PPA) atau Dinas Sosial\n"
            "4. Hubungi P2TP2A di daerahmu"
            + HOTLINE_TEXT,
            ["KTP orang tua", "Akta kelahiran anak", "Visum", "Bukti kekerasan", "Saksi"],
            "Advokat Hukum Anak / KPAI",
            "kekerasan"
        )

    def transition(self, user_input):
        ui = user_input.strip()
        ui_low = ui.lower()
        self.add_to_history("user", ui)

        # ----- GLOBAL HANDLERS -----
        if self._match(ui_low, "menu", "reset", "mulai ulang", "kembali ke menu"):
            self.reset()
            return self._menu_utama("✨ Oke, mulai dari awal yuk. Ceritain masalah kamu:")

        if self._match(ui_low, "terima kasih", "makasih", "thanks", "thank you", "trims"):
            return self._info(
                "😊 Sama-sama! Seneng bisa bantu. Kalo masih ada yang mau ditanyain, "
                "ketik **menu** ya buat konsultasi baru. Semoga cepet selesai masalahnya! 🙏"
            )

        if self._match(ui_low, "hotline", "nomor darurat", "kontak darurat", "sapa 129", "komnas"):
            return self._kontak_bantuan()

        if self._match(ui_low, "advokat", "pengacara", "rekomendasi pengacara", "cari pengacara", "butuh pengacara"):
            return self._handle_advokat(ui_low)

        # ----- ROUTING BERDASARKAN STATE -----
        handler = getattr(self, f"_state_{self.state.lower()}", None)
        if handler:
            return handler(ui, ui_low)

        self.state = "START"
        return self._state_start(ui, ui_low)

    def _state_start(self, ui, ui_low):
        # ----- PILIH KATEGORI PAKAI ANGKA -----
        if ui_low.strip() == "1":
            self.state = "MENU_PIDANA"
            return self._menu_pidana()
        if ui_low.strip() == "2":
            self.state = "MENU_PERDATA"
            return self._menu_perdata()
        if ui_low.strip() == "3":
            self.state = "MENU_KELUARGA"
            return self._menu_keluarga()
        if ui_low.strip() == "4":
            return self._kontak_bantuan()

        # ----- HUKUM PIDANA -----
        if self._match(ui_low, "penipuan online", "tipu online", "beli online", "marketplace",
                       "shopee", "tokopedia", "lazada", "barang ga datang", "seller kabur", "ditipu"):
            self.state = "PENIPUAN_ONLINE_Q1"
            self.context["kategori"] = "penipuan_online"
            return self._tanya(
                "Aduh, maaf banget ya kamu ngalamin ini 😔\n\n"
                "Biar aku bisa bantu, **kerugiannya berupa apa?**\n"
                "Misal: barang nggak dateng, dapet barang palsu, atau uang udah transfer tapi penjualnya ilang?"
            )

        if self._match(ui_low, "penipuan", "ditipu", "tipu", "dibohongi"):
            self.state = "PENIPUAN_Q1"
            self.context["kategori"] = "penipuan"
            return self._tanya(
                "Wah, nyesek ya kena tipu 😔 Tenang, aku bantu.\n\n"
                "**Penipuannya kayak gimana?** Misalnya:\n"
                "• Jual beli barang\n"
                "• Investasi bodong\n"
                "• Pinjaman uang\n"
                "• Lowongan kerja palsu\n\n"
                "Ceritain aja ya."
            )

        if self._match(ui_low, "curi", "dicuri", "maling", "kemalingan", "hp hilang", "motor hilang"):
            self.state = "PENCURIAN_Q1"
            self.context["kategori"] = "pencurian"
            return self._tanya(
                "Duh, kasian banget 😢 Aku bantu ya.\n\n"
                "**Barang apa yang ilang / dicuri?** Terus kira-kira kapan kejadiannya?"
            )

        if self._match(ui_low, "dipukul", "dianiaya", "pukul", "tendang", "penganiayaan", "luka"):
            self.state = "ANIAYA_Q1"
            self.context["kategori"] = "penganiayaan"
            return self._tanya(
                "Duh, sakit pasti ya 😔 Kamu kuat!\n\n"
                "Pertama-tanya — **udah ke dokter atau puskesmas belum?** "
                "Ini penting buat jadi bukti."
            )

        if self._match(ui_low, "fitnah", "dihina", "pencemaran", "dibully", "hoaks", "ite", "medsos"):
            self.state = "ITE_Q1"
            self.context["kategori"] = "ite"
            return self._tanya(
                "Itu nggak boleh dibiarin, kamu berhak lapor! 💪\n\n"
                "**Kejadiannya di mana?** Instagram, TikTok, Facebook, WhatsApp, atau di tempat lain?"
            )

        # ----- HUKUM PERDATA & KETENAGAKERJAAN -----
        if self._match(ui_low, "loker palsu", "tipu loker", "lowongan palsu", "kena tipu loker", "lowongan kerja bodong"):
            self.state = "TIPU_LOKER_Q1"
            self.context["kategori"] = "tipu_loker"
            return self._tanya(
                "Itu penipuan yang banyak banget korbannya 😤 Kamu nggak sendirian!\n\n"
                "**Apa yang diminta sama si 'perekrut'?**\n"
                "Bayar biaya admin? Pelatihan? Atau diminta data KTP/rekening?"
            )

        if self._match(ui_low, "hutang", "piutang", "utang", "pinjam uang", "nggak mau bayar"):
            self.state = "HUTANG_Q1"
            self.context["kategori"] = "hutang"
            return self._tanya(
                "Oke, aku bantu ya 🤝\n\n"
                "**Ada nggak perjanjian tertulis atau bukti transaksi** (transfer, kuitansi, chat) "
                "antara kamu sama yang berhutang?"
            )

        if self._match(ui_low, "pinjol", "pinjaman online", "teror pinjol", "dc pinjol"):
            self.state = "PINJOL_Q1"
            self.context["kategori"] = "pinjol"
            return self._tanya(
                "Wah, pinjol ilegal itu bahaya banget 😤\n\n"
                "**Kamu udah terlanjur pinjam atau lagi diteror DC-nya?**"
            )

        if self._match(ui_low, "tanah", "sengketa tanah", "rebut tanah", "sertifikat tanah", "tanah warisan"):
            self.state = "TANAH_Q1"
            self.context["kategori"] = "tanah"
            return self._tanya(
                "Sengketa tanah emang ribet, tapi ada jalan keluarnya kok 💪\n\n"
                "**Sengketanya sama siapa?** Saudara? Tetangga? Perusahaan?"
            )

        if self._match(ui_low, "upah", "gaji", "gaji nggak dibayar", "upah tidak dibayar", "nunggak gaji"):
            self.state = "UPAH_Q1"
            self.context["kategori"] = "upah"
            return self._tanya(
                "Hak kamu wajib dibayar! Aku bantu ya 💪\n\n"
                "**Udah berapa bulan gajimu belum dibayar?**"
            )

        if self._match(ui_low, "phk", "dipecat", "dirumahkan", "pesangon", "diberhentikan"):
            self.state = "PHK_Q1"
            self.context["kategori"] = "phk"
            return self._tanya(
                "PHK tanpa prosedur yang bener itu nggak boleh! Kamu punya hak 💪\n\n"
                "**Udah berapa lama kamu kerja di sana?** Terus **ada surat PHK resmi nggak?**"
            )

        if self._match(ui_low, "perselisihan kerja", "konflik kerja", "masalah sama kantor"):
            self.state = "AKTIF"
            return self._hasil(
                "Perselisihan Hubungan Industrial",
                "UU No. 2/2004 (PPHI)",
                "ketenagakerjaan",
                "Tenang, ada jalur resmi yang bisa kamu tempuh:\n\n"
                "1. **Bipartit** — ngobrol langsung sama perusahaan\n"
                "2. **Mediasi** ke Dinas Tenaga Kerja setempat\n"
                "3. **Konsiliasi / Arbitrase**\n"
                "4. **Pengadilan Hubungan Industrial (PHI)**\n\n"
                "📌 Yang penting, semua perundingan didokumentasikan ya!",
                ["KTP", "Perjanjian Kerja", "Bukti perselisihan", "Risalah bipartit"],
                "Advokat Ketenagakerjaan",
                "phk"
            )

        # ----- KELUARGA & PERLINDUNGAN PEREMPUAN -----
        if self._match(ui_low, "kdrt", "kekerasan rumah tangga", "dipukul suami", "dipukul istri"):
            self.state = "KDRT_Q1"
            self.context["kategori"] = "kdrt"
            return self._tanya(
                "Aku turut prihatin banget 😔 Kamu nggak sendirian, dan **kamu berhak dilindungi**.\n\n"
                "Pertama dan paling penting — **kamu lagi dalam kondisi aman nggak sekarang?**"
            )

        if self._match(ui_low, "pelecehan seksual", "dilecehkan", "pelecehan", "leceh", "perkosaan", "kekerasan seksual"):
            self.state = "PELECEHAN_Q1"
            self.context["kategori"] = "pelecehan"
            return self._tanya(
                "Aku sangat menyesal kamu ngalamin ini 😔 Kamu hebat banget mau cerita.\n\n"
                "**Kejadiannya di mana?** Di kantor? Tempat umum? Sekolah? Atau online?"
            )

        if self._match(ui_low, "kekerasan perempuan", "korban kekerasan", "kekerasan gender"):
            self.state = "KEKERASAN_PEREMPUAN_Q1"
            self.context["kategori"] = "kekerasan"
            return self._tanya(
                "Kamu sangat berani mau cerita 💪 Aku siap bantu.\n\n"
                "**Jenis kekerasannya kayak gimana?** Fisik? Seksual? Psikis (diancam/dihina)?"
            )

        if self._match(ui_low, "kekerasan anak", "anak dipukul", "anak dianiaya", "anak ditelantarkan"):
            self.state = "AKTIF"
            return self._hasil_kekerasan_anak()

        if self._match(ui_low, "cerai", "perceraian", "pisah", "gugat cerai", "ingin cerai"):
            self.state = "CERAI_Q1"
            self.context["kategori"] = "cerai"
            return self._tanya(
                "Keputusan besar ini pasti nggak gampang. Aku bantu infonya ya 🤝\n\n"
                "**Kamu/pasangan beragama Islam?** (Ini ngaruh ke pengadilan mana yang berwenang)"
            )

        if self._match(ui_low, "hak asuh", "asuh anak", "anak ikut siapa", "rebut hak asuh"):
            self.state = "AKTIF"
            return self._hasil(
                "Hak Asuh Anak",
                "Pasal 41 UU No. 1/1974",
                "keluarga",
                "Hak asuh ditentuin berdasarkan **kepentingan terbaik anak**.\n\n"
                "Yang dilihat pengadilan:\n"
                "• Anak < 12 tahun: biasanya ikut ibu\n"
                "• Anak ≥ 12 tahun: bisa milih sendiri\n"
                "• Kemampuan finansial dan psikologis orang tua\n"
                "• Lingkungan tempat tinggal\n\n"
                "Apapun hasilnya, kedua orang tua tetap wajib nafkahin anak.",
                ["KTP orang tua", "Akta kelahiran anak", "Akta cerai", "Bukti penghasilan"],
                "Advokat Hukum Keluarga"
            )

        return self._menu_utama()

   
    def _state_penipuan_online_q1(self, ui, ui_low):
        self.context["jenis_penipuan_online"] = ui
        self.state = "PENIPUAN_ONLINE_Q2"
        return self._tanya(f"Oke, kasus **{ui}**.\n\n**Total kerugiannya kira-kira berapa?**")

    def _state_penipuan_online_q2(self, ui, ui_low):
        self.context["kerugian"] = ui
        self.state = "PENIPUAN_ONLINE_Q3"
        return self._tanya(
            "Oke dicatat. Sekarang soal bukti:\n\n"
            "**Kamu punya bukti transaksi atau percakapan sama pelaku nggak?**\n"
            "Misal: screenshot chat, bukti transfer, link toko, rekening tujuan."
        )

    def _state_penipuan_online_q3(self, ui, ui_low):
        punya_bukti = self._match(ui_low, "ya", "ada", "punya", "iya", "screenshot", "foto", "transfer")
        self.context["punya_bukti"] = punya_bukti
        self.state = "PENIPUAN_ONLINE_Q4"
        if punya_bukti:
            return self._tanya(
                "Bagus banget! Bukti itu penting banget 💪\n\n"
                "**Kamu tau identitas pelakunya nggak?** Nama, nomor HP, rekening, atau akun medsos?"
            )
        else:
            return self._tanya(
                "Tenang, meskipun nggak ada bukti transfer masih bisa lapor kok! 💪\n\n"
                "**Kamu masih inget atau punya data pelaku nggak?** "
                "Nama toko, nomor HP, akun medsos, atau nomor rekening?"
            )

    def _state_penipuan_online_q4(self, ui, ui_low):
        punya_identitas = self._match(ui_low, "ya", "ada", "punya", "tau", "tahu", "nomor", "rekening", "akun")
        self.context["punya_identitas"] = punya_identitas
        self.state = "AKTIF"

        punya_bukti = self.context.get("punya_bukti", False)
        if punya_bukti and punya_identitas:
            catatan = "Kamu punya bukti dan data pelaku — posisi kamu sangat kuat buat lapor! 💪"
        elif punya_bukti:
            catatan = "Kamu punya bukti transaksi — itu udah cukup kuat buat mulai lapor."
        elif punya_identitas:
            catatan = "Meskipun bukti terbatas, data pelaku bisa dipake. Coba hubungi platform marketplace buat minta data."
        else:
            catatan = "Tenang, laporan tanpa bukti tetap SAH. Polisi bakal bantu penyelidikan."

        return self._hasil(
            "Penipuan Online",
            "Pasal 378 KUHP & Pasal 28 UU ITE",
            "pidana",
            f"{catatan}\n\n"
            "📌 **Langkah yang bisa kamu lakuin:**\n"
            "1. Backup semua bukti digital\n"
            "2. Catat kerugian secara rinci\n"
            "3. Lapor ke polisi via patrolisiber.id atau polsek terdekat\n"
            "4. Lapor ke marketplace biar akun penipu diblokir\n"
            "5. Hubungi bank buat blokir rekening pelaku",
            ["KTP", "Screenshot chat", "Bukti transfer", "Link toko pelaku", "Nomor rekening pelaku"],
            "Advokat Cyber Crime",
            "penipuan_online"
        )

    # ==================================================================
    # STATE PENCURIAN
    # ==================================================================
    def _state_pencurian_q1(self, ui, ui_low):
        self.context["barang_dicuri"] = ui
        self.state = "PENCURIAN_Q2"
        return self._tanya(f"Dicuri **{ui}**, nyesek banget ya 😤\n\n**Ada saksi yang liat nggak?** Atau rekaman CCTV?")

    def _state_pencurian_q2(self, ui, ui_low):
        self.state = "AKTIF"
        ada_saksi = self._match(ui_low, "ya", "ada", "iya", "cctv", "saksi")
        catatan = "Bagus! Saksi/CCTV bakal bantu banget." if ada_saksi else "Coba cek CCTV sekitar lokasi. Kalo nggak ada, laporan tetep bisa diproses."
        return self._hasil(
            "Pencurian",
            "Pasal 362 KUHP",
            "pidana",
            f"{catatan}\n\nPelaku bisa dipenjara paling lama **5 tahun**. Segera lapor ke polisi ya!",
            ["KTP", "Bukti kepemilikan barang (nota, STNK)", "Rekaman CCTV", "Keterangan saksi"],
            "Advokat Pidana"
        )

    # ==================================================================
    # STATE KDRT
    # ==================================================================
    def _state_kdrt_q1(self, ui, ui_low):
        aman = self._match(ui_low, "aman", "sudah aman")
        self.state = "KDRT_Q2"
        if not aman:
            return self._tanya(
                "⚠️ **Keselamatanmu nomor satu!**\n\n"
                "Segera hubungi:\n📞 SAPA 129 (WA 08111-129-129)\n📞 Komnas Perempuan 0811-171-7177\n📞 Polisi 110\n\n"
                "Kalo bisa, pergi ke tempat aman dulu. **Ada anak yang ikut kamu?**"
            )
        return self._tanya("Syukurlah kamu aman 🙏 **Ini udah terjadi lebih dari sekali atau baru pertama?**")

    def _state_kdrt_q2(self, ui, ui_low):
        self.context["ada_anak"] = self._match(ui_low, "ya", "ada", "anak")
        self.state = "KDRT_Q3"
        return self._tanya("**Jenis kekerasannya kayak gimana?** Fisik (dipukul), psikis (diancam), seksual, atau ditelantarkan?")

    def _state_kdrt_q3(self, ui, ui_low):
        self.context["jenis_kdrt"] = ui
        self.state = "KDRT_Q4"
        return self._tanya("**Ada bukti atau saksi nggak?** Foto luka, rekaman, tetangga yang tau, atau chat ancaman?")

    def _state_kdrt_q4(self, ui, ui_low):
        self.state = "AKTIF"
        ada_bukti = self._match(ui_low, "ya", "ada", "foto", "saksi", "chat")
        catatan = "Bagus, buktinya bakal bantu banget!" if ada_bukti else "Meski tanpa bukti, laporan tetep bisa diproses."
        ada_anak = self.context.get("ada_anak", False)
        catatan_anak = "\n\n👶 Kalo ada anak, pastikan keselamatannya juga dijaga." if ada_anak else ""
        return self._hasil(
            "KDRT",
            "UU PKDRT No. 23/2004",
            "keluarga",
            f"{catatan}{catatan_anak}\n\nPelaku bisa dipenjara 5-15 tahun. Kamu juga bisa minta Surat Perlindungan.\n{HOTLINE_TEXT}",
            ["KTP", "Kartu Keluarga", "Buku Nikah", "Foto luka", "Hasil visum", "Saksi"],
            "Advokat KDRT / LBH APIK",
            "kdrt"
        )

    # ==================================================================
    # STATE AKTIF (untuk pertanyaan lanjutan)
    # ==================================================================
    def _state_aktif(self, ui, ui_low):
        # ----- RESPON BAHASA SEHARI-HARI -----
        if self._match(ui_low, "masa iya", "masa", "serius", "beneran", "yakin", "masa sih"):
            return self._info(
                "😊 **Serius, aku nggak bercanda!**\n\n"
                "Polisi punya kewajiban buat terima laporan, apapun buktinya.\n\n"
                "Kamu udah hebat banget mau nanya-nanya dulu. Jangan nyerah ya! 💪"
            )
        
        # ----- TANYA BUKTI LUKA -----
        if self._match(ui_low, "gaada bukti luka", "gak ada bukti luka", "tidak ada bukti luka", "foto luka ga ada"):
            return self._info(
                "📌 **Tenang, meskipun gaada foto luka, kamu tetap bisa lapor!**\n\n"
                "Yang bisa kamu lakuin:\n\n"
                "✅ **Tetap lapor polisi** — ceritakan secara detail kronologi kejadian\n"
                "✅ **Minta visum** — ke puskesmas/RS, dokter bisa mendeteksi luka meski udah agak lama\n"
                "✅ **Cari saksi** — siapa tau ada yang melihat kejadian\n\n"
                "💡 **Visum itu penting banget!** Jangan ragu buat minta visum ya!"
            )
        
        # ----- TANYA BUKTI TRANSFER -----
        if self._match(ui_low, "gaada bukti transfer", "gak ada bukti transfer", "tidak ada bukti transfer", "transfer ga ada bukti"):
            return self._info(
                "📌 **Tenang, meskipun gaada bukti transfer, kamu tetap bisa lapor!**\n\n"
                "Yang bisa kamu lakuin:\n\n"
                "✅ **Tetap lapor polisi** — ceritakan kronologi kejadian\n"
                "✅ **Cek rekening koran** — minta ke bank, pasti ada jejak transaksi!\n"
                "✅ **Kumpulkan chat percakapan** — screenshot chat dengan pelaku\n"
                "✅ **Cari saksi** — siapa tau ada yang tau atau lihat\n\n"
                "💡 **Bank bisa bantu!** Kamu bisa minta cetak mutasi rekening ke bank!"
            )
        
        # ----- TANYA BUKTI UMUM -----
        if self._match(ui_low, "gak ada bukti", "nggak ada bukti", "tidak ada bukti", "tanpa bukti"):
            return self._info(
                "✨ **Tenang aja, santai.**\n\n"
                "Kamu nggak sendirian kok yang ngalamin gini. Banyak kasus yang awalnya "
                "nggak punya bukti, tapi tetep bisa diproses.\n\n"
                "🟢 **Yang bisa kamu lakuin sekarang:**\n"
                "• 📝 Catat semua detail kejadian (kapan, di mana, sama siapa)\n"
                "• 📱 Cek lagi HP-mu, siapa tau ada chat lama yang tersimpan\n"
                "• 🏦 Hubungi bank minta cetak mutasi rekening\n"
                "• 👥 Cari saksi (temen, keluarga, tetangga) yang tau kejadiannya\n\n"
                "💡 Percaya deh, polisi tetep wajib terima laporan kamu meskipun tanpa bukti!"
            )
        
        # ----- TANYA TEMPAT LAPOR -----
        if self._match(ui_low, "lapor ke mana", "kemana lapor", "lapor kemana", "cara lapor"):
            return self._info(
                "📍 **Bisa lapor di sini:**\n\n"
                "🏠 **Dateng langsung:** Polsek atau Polres terdekat dari rumah kamu.\n"
                "💻 **Online:** https://spion.polri.go.id\n"
                "🌐 **Khusus online:** Direktorat Siber Bareskrim\n"
                "📞 **Telepon:** 110 (gratis, 24 jam)\n\n"
                "💡 Tips: Bawa KTP dan semua bukti yang ada. Kalo nggak ada bukti juga gapapa!"
            )
        
        # ----- TANYA BIAYA -----
        if self._match(ui_low, "biaya", "gratis", "mahal", "bayar", "perlu bayar"):
            return self._info(
                "💰 **Tenang, ini GRATIS!**\n\n"
                "• Lapor ke polisi: GRATIS 100%\n"
                "• Pengadilan: ada biaya, tapi bisa minta keringanan (prodeo)\n"
                "• Pake pengacara: ada yang bayar, ada yang pro bono (gratis)\n\n"
                "💡 Kalo kamu nggak mampu bayar, bisa minta bantuan gratis ke LBH terdekat!"
            )
        
        # ----- TANYA PROSES -----
        if self._match(ui_low, "berapa lama", "lama nggak", "prosesnya lama", "kapan selesai"):
            return self._info(
                "⏰ **Sabar ya, ini estimasinya:**\n\n"
                "• Laporan diterima: 1-3 hari\n"
                "• Penyelidikan: 14-30 hari\n"
                "• Penyidikan: 30-90 hari\n"
                "• Ke kejaksaan: 14 hari\n"
                "• Sidang: 2-6 bulan\n\n"
                "💡 Kasus sederhana bisa selesai 1-3 bulan. Yang penting kamu udah lapor dulu!"
            )
        
        # ----- TANYA RASA MALU -----
        if self._match(ui_low, "malu", "takut", "nggak berani", "ragu", "khawatir"):
            return self._info(
                "🤗 **Wajar kok kamu ngerasa gitu.**\n\n"
                "Banyak orang yang juga ngerasa takut atau malu sebelum melapor.\n\n"
                "🟢 **Coba ini dulu:**\n"
                "• Ajak teman atau keluarga yang kamu percaya buat nemenin\n"
                "• Lapor online dulu lewat spion.polri.go.id\n"
                "• Identitas kamu dilindungi kok\n"
                "• Hubungi SAPA 129 buat konseling gratis dulu\n\n"
                "💪 Kamu sudah berani banget dengan mau cerita ke aku!"
            )
        
        # ----- TANYA HAK KORBAN -----
        if self._match(ui_low, "hak saya apa", "apa hak saya", "hak korban"):
            return self._info(
                "📜 **Hak-hak kamu sebagai korban:**\n\n"
                "✅ Hak bikin laporan polisi (nggak bisa ditolak)\n"
                "✅ Hak tau perkembangan kasus\n"
                "✅ Hak didampingi pengacara (gratis kalo nggak mampu)\n"
                "✅ Hak dilindungi identitasnya\n"
                "✅ Hak dapet ganti rugi (restitusi)\n"
                "✅ Hak dapet bantuan psikolog\n\n"
                "💡 Jangan ragu buat nuntut hak-hakmu!"
            )
        
        # ----- TANYA UANG BISA BALIK -----
        if self._match(ui_low, "uang bisa balik", "duit kembali", "kerugian bisa diganti"):
            return self._info(
                "💰 **Soal uang, ini tergantung:**\n\n"
                "✅ **Kabar baik:** kalo pelaku ketemu dan terbukti, kamu berhak minta ganti rugi.\n\n"
                "⚠️ **Tapi:** prosesnya nggak instan, bisa makan waktu berbulan-bulan.\n\n"
                "🟢 **Yang bisa kamu lakuin sekarang:**\n"
                "• Lapor ke bank buat blokir rekening pelaku\n"
                "• Simpan semua bukti transaksi\n"
                "• Ikuti proses hukum sampai tuntas\n\n"
                "💡 Fokus dulu ke laporan polisi! Urusan uang belakangan."
            )
        
        # ----- TANYA PELAKU TIDAK DIKENAL -----
        if self._match(ui_low, "pelaku gak dikenal", "nggak kenal pelaku", "gak tau pelakunya"):
            return self._info(
                "🕵️ **Nggak kenal pelaku? Nggak masalah!**\n\n"
                "Banyak kasus yang pelakunya nggak dikenal korban.\n\n"
                "Polisi bakal nyari pelaku pake data yang ada (CCTV, nomor HP, rekening bank).\n"
                "Kamu cukup kasih ciri-ciri atau info yang kamu inget.\n\n"
                "💡 Yang penting jangan nyerah!"
            )
        
        # ----- TANYA SAKSI TIDAK ADA -----
        if self._match(ui_low, "saksi gak ada", "nggak ada saksi", "gak ada yang liat"):
            return self._info(
                "👀 **Nggak ada saksi? Tenang, masih bisa kok!**\n\n"
                "Yang bisa jadi 'saksi' selain orang:\n"
                "• Chat WhatsApp/Telegram\n"
                "• Email\n"
                "• CCTV di sekitar lokasi\n"
                "• Mutasi rekening bank\n\n"
                "💡 Kalo bener-bener kosong, catat detail kejadian sejelas-jelasnya!"
            )
        
        # ----- TANYA PASAL -----
        if self._match(ui_low, "pasal", "cari pasal", "pasal berapa"):
            if "378" in ui_low:
                return self._info(
                    "📖 **Pasal 378 KUHP** (Penipuan)\n\n"
                    "Ancaman pidana penjara paling lama 4 tahun."
                )
            elif "362" in ui_low:
                return self._info(
                    "📖 **Pasal 362 KUHP** (Pencurian)\n\n"
                    "Ancaman pidana penjara paling lama 5 tahun."
                )
            else:
                return self._info(
                    "📖 **Cari Pasal**\n\n"
                    "Ketik: 'pasal 378' (penipuan), 'pasal 362' (pencurian)"
                )
        
        # ----- DEFAULT -----
        return self._info(
            f"Hmm, aku denger kamu bilang: *\"{ui[:80]}\"*\n\n"
            "🗣️ **Pertanyaan yang sering ditanyakan:**\n\n"
            "• *'Gak ada bukti, gimana dong?'*\n"
            "• *'Lapor ke mana ya?'*\n"
            "• *'Bayar nggak?'* → GRATIS!\n"
            "• *'Prosesnya lama?'* → sekitar 1-6 bulan\n"
            "• *'Aku malu/takut lapor'* → wajar kok!\n"
            "• *'Hak saya apa aja?'*\n"
            "• *'Uang bisa balik nggak?'*\n"
            "• *'Pelaku nggak dikenal gimana?'*\n\n"
            "📌 **Atau ketik 'menu'** buat konsultasi baru.\n\n"
            "Ada yang mau ditanyain lagi? Aku dengerin kok 👂"
        )

    # ==================================================================
    # STATE PENIPUAN (shortcut)
    # ==================================================================
    def _state_penipuan_q1(self, ui, ui_low):
        self.state = "PENIPUAN_Q2"
        return self._tanya("**Apakah ada bukti transfer dan chat dengan pelaku?**")

    def _state_penipuan_q2(self, ui, ui_low):
        self.state = "PENIPUAN_Q3"
        return self._tanya("**Berapa nominal kerugiannya?**")

    def _state_penipuan_q3(self, ui, ui_low):
        self.state = "AKTIF"
        return self._hasil(
            "Penipuan",
            "Pasal 378 KUHP",
            "pidana",
            "Penipuan adalah tindak pidana!\n\n"
            "Langkah yang harus dilakukan:\n"
            "1. Kumpulkan semua bukti (chat, transfer)\n"
            "2. Laporkan ke bank untuk blokir rekening\n"
            "3. Laporkan ke polisi\n\n"
            "Ancaman hukuman: maksimal 4 tahun penjara.",
            ["KTP", "Bukti transfer", "Screenshot chat", "Nomor rekening pelaku"],
            "Advokat Pidana",
            "penipuan"
        )

    # ==================================================================
    # STATE ITE
    # ==================================================================
    def _state_ite_q1(self, ui, ui_low):
        self.state = "ITE_Q2"
        return self._tanya(f"Kejadian di {ui} ya.\n\n**Apakah kamu punya screenshot atau bukti lainnya?**")

    def _state_ite_q2(self, ui, ui_low):
        self.state = "ITE_Q3"
        punya_bukti = self._match(ui_low, "ya", "ada", "punya", "screenshot")
        if punya_bukti:
            return self._tanya("Bagus! **Apakah kamu tahu identitas pelakunya?**")
        else:
            return self._tanya("Segera screenshot sebelum dihapus! **Apakah kamu tahu identitas pelakunya?**")

    def _state_ite_q3(self, ui, ui_low):
        self.state = "AKTIF"
        return self._hasil(
            "Pencemaran Nama Baik (ITE)",
            "Pasal 27 ayat (3) UU ITE",
            "pidana",
            "Langkah-langkah yang bisa kamu lakukan:\n\n"
            "1. Kumpulkan semua bukti screenshot\n"
            "2. Laporkan ke platform media sosial\n"
            "3. Laporkan ke polisi (Direktorat Siber)\n"
            "4. Jangan hapus bukti asli\n\n"
            "Ancaman pidana: maksimal 4 tahun penjara.",
            ["Screenshot konten", "URL link", "Username pelaku"],
            "Advokat Cyber Crime",
            "ite"
        )

    # ==================================================================
    # STATE TIPU LOKER
    # ==================================================================
    def _state_tipu_loker_q1(self, ui, ui_low):
        self.state = "TIPU_LOKER_Q2"
        return self._tanya("**Berapa nominal yang diminta?** Dan sudah ditransfer belum?")

    def _state_tipu_loker_q2(self, ui, ui_low):
        self.state = "TIPU_LOKER_Q3"
        return self._tanya("**Apakah kamu punya bukti chat dan bukti transfer?**")

    def _state_tipu_loker_q3(self, ui, ui_low):
        self.state = "AKTIF"
        return self._hasil(
            "Penipuan Lowongan Kerja",
            "Pasal 378 KUHP",
            "ketenagakerjaan",
            "⚠️ LOWONGAN KERJA YANG MEMUNGUT BIAYA ADALAH PENIPUAN!\n\n"
            "Langkah yang harus dilakukan:\n"
            "1. Kumpulkan semua bukti (chat, transfer, iklan)\n"
            "2. Laporkan ke polisi\n"
            "3. Laporkan ke platform loker\n"
            "4. Blokir nomor penipu\n\n"
            "Ingat: Rekrutmen resmi TIDAK PERNAH memungut biaya apapun!",
            ["Screenshot chat", "Bukti transfer", "Iklan lowongan"],
            "Advokat Pidana",
            "tipu_loker"
        )

    # ==================================================================
    # STATE HUTANG
    # ==================================================================
    def _state_hutang_q1(self, ui, ui_low):
        self.state = "HUTANG_Q2"
        return self._tanya("**Apakah ada perjanjian tertulis atau bukti pinjaman?**")

    def _state_hutang_q2(self, ui, ui_low):
        self.state = "AKTIF"
        return self._hasil(
            "Hutang Piutang",
            "Pasal 1754 KUHPerdata",
            "perdata",
            "Langkah penagihan hutang:\n\n"
            "1. Kirim somasi (surat peringatan) 3x\n"
            "2. Ajukan gugatan perdata ke Pengadilan Negeri\n"
            "3. Upaya paksa melalui juru sita\n\n"
            "Tips: Simpan semua bukti transaksi dan komunikasi!",
            ["Perjanjian hutang", "Bukti transfer", "Chat/somasi"],
            "Advokat Perdata"
        )

    # ==================================================================
    # STATE TANAH
    # ==================================================================
    def _state_tanah_q1(self, ui, ui_low):
        self.state = "TANAH_Q2"
        return self._tanya("**Apakah kamu memiliki sertifikat atau bukti kepemilikan tanah?**")

    def _state_tanah_q2(self, ui, ui_low):
        self.state = "TANAH_Q3"
        return self._tanya("**Apakah sengketa ini sudah pernah dilaporkan ke kantor pertanahan?**")

    def _state_tanah_q3(self, ui, ui_low):
        self.state = "AKTIF"
        return self._hasil(
            "Sengketa Tanah",
            "UUPA No. 5/1960",
            "perdata",
            "Penyelesaian sengketa tanah:\n\n"
            "1. Mediasi di Kantor Pertanahan (ATR/BPN)\n"
            "2. Gugatan ke Pengadilan Tata Usaha Negara\n"
            "3. Gugatan perdata ke Pengadilan Negeri\n\n"
            "💡 Saran: Selesaikan secara kekeluargaan terlebih dahulu!",
            ["Sertifikat tanah", "KTP", "KK"],
            "Advokat Perdata Pertanahan",
            "tanah"
        )

    # ==================================================================
    # STATE PHK
    # ==================================================================
    def _state_phk_q1(self, ui, ui_low):
        self.state = "PHK_Q2"
        return self._tanya("**Sudah berapa lama Anda bekerja di perusahaan tersebut?**")

    def _state_phk_q2(self, ui, ui_low):
        self.context["masa_kerja"] = ui
        self.state = "PHK_Q3"
        return self._tanya("**Apakah ada surat PHK resmi?** Jika ada, apa alasan PHK yang tercantum?")

    def _state_phk_q3(self, ui, ui_low):
        self.state = "AKTIF"
        return self._hasil(
            "PHK Sepihak",
            "UU Cipta Kerja No. 11/2020",
            "ketenagakerjaan",
            f"Hak pesangon berdasarkan masa kerja {self.context.get('masa_kerja', 'belum diketahui')}:\n\n"
            "Hak yang wajib dibayar perusahaan:\n"
            "• Uang Pesangon (UP)\n"
            "• Uang Penghargaan Masa Kerja (UPMK)\n"
            "• Uang Penggantian Hak (cuti, dll)\n\n"
            "Jika PHK sepihak (tanpa prosedur):\n"
            "1. Kirim somasi ke perusahaan\n"
            "2. Lapor ke Dinas Tenaga Kerja\n"
            "3. Gugat ke PHI\n\n"
            "⚠️ Jangan menandatangani surat pengunduran diri jika dipaksa!",
            ["Kontrak kerja", "Surat PHK", "Slip gaji"],
            "Advokat Ketenagakerjaan",
            "phk"
        )

    # ==================================================================
    # STATE CERAI
    # ==================================================================
    def _state_cerai_q1(self, ui, ui_low):
        if self._match(ui_low, "islam", "muslim"):
            self.context["agama"] = "islam"
        else:
            self.context["agama"] = "non_islam"
        self.state = "CERAI_Q2"
        return self._tanya("**Apakah sudah ada kesepakatan mengenai harta gono-gini dan hak asuh anak?**")

    def _state_cerai_q2(self, ui, ui_low):
        self.state = "CERAI_Q3"
        return self._tanya("**Sudah berapa lama menikah dan apakah sudah pisah rumah?**")

    def _state_cerai_q3(self, ui, ui_low):
        self.state = "AKTIF"
        if self.context.get("agama") == "islam":
            return self._hasil(
                "Perceraian (Islam)",
                "UU No. 1/1974 & Kompilasi Hukum Islam",
                "keluarga",
                "Prosedur cerai untuk pasangan Muslim:\n\n"
                "1. Ajukan gugatan ke Pengadilan Agama\n"
                "2. Jalani mediasi (wajib)\n"
                "3. Persidangan dengan 2 orang saksi\n"
                "4. Putusan cerai talak\n\n"
                "📌 Yang perlu disiapkan:\n"
                "• Buku nikah asli\n"
                "• Alasan cerai yang kuat\n"
                "• Daftar harta gono-gini\n\n"
                "⏱ Proses: 3-6 bulan",
                ["Buku nikah", "KTP", "KK"],
                "Advokat Hukum Keluarga / Pengadilan Agama"
            )
        else:
            return self._hasil(
                "Perceraian (Non-Islam)",
                "UU No. 1/1974 & KUHPerdata",
                "keluarga",
                "Prosedur cerai untuk pasangan non-Muslim:\n\n"
                "1. Ajukan gugatan ke Pengadilan Negeri\n"
                "2. Jalani mediasi (wajib)\n"
                "3. Persidangan\n"
                "4. Putusan cerai\n\n"
                "📌 Yang perlu disiapkan:\n"
                "• Akta nikah\n"
                "• Alasan cerai yang sah\n"
                "• Daftar harta bersama\n\n"
                "⏱ Proses: 4-8 bulan",
                ["Akta nikah", "KTP", "KK"],
                "Advokat Hukum Keluarga"
            )

    # ==================================================================
    # STATE UPAH
    # ==================================================================
    def _state_upah_q1(self, ui, ui_low):
        self.state = "UPAH_Q2"
        return self._tanya("**Sudah berapa bulan gaji tidak dibayar?**")

    def _state_upah_q2(self, ui, ui_low):
        self.state = "UPAH_Q3"
        return self._tanya("**Apakah kamu memiliki kontrak kerja dan slip gaji?**")

    def _state_upah_q3(self, ui, ui_low):
        self.state = "AKTIF"
        return self._hasil(
            "Gaji Tidak Dibayar",
            "UU Ketenagakerjaan No. 13/2003",
            "ketenagakerjaan",
            "Hak kamu dilindungi hukum!\n\n"
            "Langkah yang bisa dilakukan:\n"
            "1. Kirim surat somasi ke perusahaan\n"
            "2. Laporkan ke Dinas Tenaga Kerja setempat\n"
            "3. Ajukan gugatan ke Pengadilan Hubungan Industrial (PHI)\n\n"
            "💰 Perusahaan bisa dikenakan denda dan wajib membayar gaji + kompensasi!",
            ["Kontrak kerja", "Slip gaji", "Absensi"],
            "Advokat Ketenagakerjaan",
            "upah"
        )

    # ==================================================================
    # STATE PINJOL
    # ==================================================================
    def _state_pinjol_q1(self, ui, ui_low):
        if self._match(ui_low, "teror", "dc", "penagih", "diteror"):
            self.state = "PINJOL_Q2"
            return self._tanya("Wah, teror pinjol ilegal itu sangat mengganggu 😤\n\n**Apa saja yang mereka lakukan?**")
        else:
            self.state = "PINJOL_Q2"
            return self._tanya("**Apakah pinjol tersebut sudah terdaftar di OJK?** Cek di https://kontak157.ojk.go.id")

    def _state_pinjol_q2(self, ui, ui_low):
        self.state = "AKTIF"
        return self._hasil(
            "Pinjaman Online Ilegal",
            "POJK No. 77/2016 & UU ITE",
            "perdata",
            "⚠️ PINJOL ILEGAL WAJIB DILAPORKAN!\n\n"
            "Langkah yang harus dilakukan:\n"
            "1. Jangan bayar! Pinjol ilegal tidak memiliki kekuatan hukum\n"
            "2. Blokir semua nomor penagih\n"
            "3. Laporkan ke OJK via 157 atau WhatsApp 0811-5715-7157\n"
            "4. Laporkan ke polisi jika ada ancaman/teror\n"
            "5. Ganti nomor HP jika perlu\n\n"
            "🔐 Data pribadi kamu dilindungi hukum!",
            ["Screenshot teror", "Bukti transfer", "Nomor penagih"],
            "Advokat Perdata / LBH",
            "pinjol"
        )

    # ==================================================================
    # STATE KEKERASAN PEREMPUAN
    # ==================================================================
    def _state_kekerasan_perempuan_q1(self, ui, ui_low):
        self.state = "KEKERASAN_PEREMPUAN_Q2"
        return self._tanya("**Sudah minta visum atau ke dokter?** Ini penting sebagai bukti.")

    def _state_kekerasan_perempuan_q2(self, ui, ui_low):
        self.state = "AKTIF"
        return self._hasil(
            "Kekerasan Terhadap Perempuan",
            "UU PKDRT No. 23/2004 & UU TPKS No. 12/2022",
            "keluarga",
            f"📢 KAMU TIDAK SENDIRIAN! Banyak yang siap bantu.\n\n"
            "Langkah yang harus dilakukan:\n"
            "1. Pergi ke tempat aman\n"
            "2. Minta visum di puskesmas/RS\n"
            "3. Kumpulkan bukti (foto, chat, saksi)\n"
            "4. Lapor polisi (Unit PPA)\n"
            "5. Hubungi hotline bantuan\n\n"
            f"{HOTLINE_TEXT}\n\n"
            "Hak kamu sebagai korban:\n"
            "• Perlindungan dari pendamping\n"
            "• Bantuan hukum gratis\n"
            "• Rehabilitasi psikologis\n"
            "• Restitusi (ganti rugi)",
            ["KTP", "KK", "Foto luka", "Visum", "Saksi"],
            "LBH APIK / Komnas Perempuan",
            "kekerasan"
        )

    # ==================================================================
    # STATE PELECEHAN
    # ==================================================================
    def _state_pelecehan_q1(self, ui, ui_low):
        self.context["lokasi_pelecehan"] = ui
        self.state = "PELECEHAN_Q2"
        return self._tanya("**Apakah kamu punya bukti?** (chat, rekaman, saksi, atau pesan ancaman)")

    def _state_pelecehan_q2(self, ui, ui_low):
        self.state = "PELECEHAN_Q3"
        punya_bukti = self._match(ui_low, "ya", "ada", "punya", "chat", "screenshot")
        if punya_bukti:
            return self._tanya("Bagus! **Apakah pelecehan terjadi berulang atau hanya sekali?**")
        else:
            return self._tanya("**Apakah ada saksi yang melihat atau mendengar kejadian tersebut?**")

    def _state_pelecehan_q3(self, ui, ui_low):
        self.state = "PELECEHAN_Q4"
        return self._tanya("**Apakah kamu mengenali pelakunya?** (rekan kerja, atasan, teman, atau orang tidak dikenal)")

    def _state_pelecehan_q4(self, ui, ui_low):
        self.state = "AKTIF"
        return self._hasil(
            "Pelecehan Seksual",
            "UU TPKS No. 12/2022",
            "keluarga",
            f"⚠️ PELECEHAN SEKSUAL ADALAH TINDAK PIDANA!\n\n"
            "Hak kamu:\n"
            "1. Berhak melapor tanpa takut\n"
            "2. Berhak didampingi pendamping khusus\n"
            "3. Berhak atas kerahasiaan identitas\n"
            "4. Berhak mendapatkan restitusi\n\n"
            "Langkah yang bisa dilakukan:\n"
            "• Kumpulkan bukti (jangan dihapus!)\n"
            "• Minta visum (jika ada kontak fisik)\n"
            "• Lapor polisi (Unit PPA)\n"
            "• Hubungi hotline pendampingan\n\n"
            f"{HOTLINE_TEXT}\n\n"
            "💪 Kamu BERANI melapor = melindungi calon korban lainnya!",
            ["KTP", "Bukti chat/foto/rekaman", "Saksi", "Visum"],
            "LBH APIK / Komnas Perempuan",
            "pelecehan"
        )

    # ==================================================================
    # STATE PENGANIAYAAN
    # ==================================================================
    def _state_aniaya_q1(self, ui, ui_low):
        self.state = "ANIAYA_Q2"
        return self._tanya("**Sudah minta visum ke puskesmas atau rumah sakit?**")

    def _state_aniaya_q2(self, ui, ui_low):
        self.state = "ANIAYA_Q3"
        return self._tanya("**Apakah ada saksi yang melihat kejadian atau rekaman CCTV?**")

    def _state_aniaya_q3(self, ui, ui_low):
        self.state = "AKTIF"
        return self._hasil(
            "Penganiayaan",
            "Pasal 351 KUHP",
            "pidana",
            "Penganiayaan adalah tindak pidana!\n\n"
            "Ancaman hukuman:\n"
            "• Penganiayaan biasa: maksimal 2,5 tahun penjara\n"
            "• Penganiayaan berat: maksimal 7 tahun penjara\n\n"
            "Langkah yang harus dilakukan:\n"
            "1. Minta visum (bukti medis)\n"
            "2. Foto luka-luka\n"
            "3. Cari saksi atau CCTV\n"
            "4. Lapor polisi (yang paling cepat!)\n\n"
            "⚠️ Jangan membalas kekerasan dengan kekerasan!",
            ["KTP", "Visum", "Foto luka", "Saksi/CCTV"],
            "Advokat Pidana"
        )

    # ==================================================================
    # MENU STATE HANDLERS
    # ==================================================================
    def _state_menu_pidana(self, ui, ui_low):
        if ui_low == "0":
            self.state = "START"
            return self._menu_utama()
        mapping = {"a": ("PENIPUAN_Q1", "aku ditipu"), "b": ("PENIPUAN_ONLINE_Q1", "aku kena tipu online"), "c": ("PENCURIAN_Q1", "barangku dicuri"), "d": ("ANIAYA_Q1", "aku dipukul"), "e": ("ITE_Q1", "aku difitnah di medsos")}
        if ui_low in mapping:
            self.state, trigger = mapping[ui_low]
            return self.transition(trigger)
        return self._menu_pidana()

    def _state_menu_perdata(self, ui, ui_low):
        if ui_low == "0":
            self.state = "START"
            return self._menu_utama()
        mapping = {"a": ("TANAH_Q1", "sengketa tanah"), "b": ("HUTANG_Q1", "hutang piutang"), "c": ("TIPU_LOKER_Q1", "tipu loker"), "d": ("UPAH_Q1", "gaji nggak dibayar"), "e": ("PHK_Q1", "aku dipecat"), "f": ("START", "perselisihan kerja"), "g": ("PINJOL_Q1", "pinjol ilegal")}
        if ui_low in mapping:
            self.state, trigger = mapping[ui_low]
            return self.transition(trigger)
        return self._menu_perdata()

    def _state_menu_keluarga(self, ui, ui_low):
        if ui_low == "0":
            self.state = "START"
            return self._menu_utama()
        mapping = {"a": ("CERAI_Q1", "aku mau cerai"), "b": ("START", "hak asuh anak"), "c": ("KDRT_Q1", "kdrt"), "d": ("KEKERASAN_PEREMPUAN_Q1", "kekerasan perempuan"), "e": ("START", "kekerasan anak"), "f": ("PELECEHAN_Q1", "pelecehan seksual")}
        if ui_low in mapping:
            self.state, trigger = mapping[ui_low]
            return self.transition(trigger)
        return self._menu_keluarga()