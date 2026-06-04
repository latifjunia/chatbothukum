class LegalFSM:
    def __init__(self):
        self.state = "START"
        self.conversation_history = []

    def reset(self):
        self.state = "START"
        self.conversation_history = []

    def add_to_history(self, role, content):
        self.conversation_history.append({"role": role, "content": content})
        if len(self.conversation_history) > 20:
            self.conversation_history.pop(0)

    def transition(self, user_input):
        ui = user_input.strip().lower()
        self.add_to_history("user", user_input)

        if self.state == "START":
            if ui == "1":
                self.state = "PIDANA"
                return self._menu("Hukum Pidana", "pidana", "Pilih jenis kasus pidana yang Anda hadapi:", [("1", "Penipuan"), ("2", "Pencurian"), ("0", "← Kembali")])
            elif ui == "2":
                self.state = "PERDATA"
                return self._menu("Hukum Perdata", "perdata", "Pilih jenis kasus perdata:", [("1", "Hutang Piutang"), ("2", "Wanprestasi"), ("0", "← Kembali")])
            elif ui == "3":
                self.state = "KELUARGA"
                return self._menu("Hukum Keluarga", "keluarga", "Pilih jenis kasus keluarga:", [("1", "Perceraian"), ("2", "Hak Asuh Anak"), ("0", "← Kembali")])
            elif ui == "4":
                self.state = "KETENAGAKERJAAN"
                return self._menu("Hukum Ketenagakerjaan", "ketenagakerjaan", "Pilih jenis kasus ketenagakerjaan:", [("1", "PHK"), ("2", "Perselisihan Kerja"), ("0", "← Kembali")])
            return self._menu_utama()

        elif self.state == "PIDANA":
            if ui == "0":
                self.state = "START"
                return self._menu_utama()
            elif ui == "1":
                self.state = "PENIPUAN"
                return self._menu("Penipuan - Bukti", "pertanyaan", "Apakah Anda memiliki bukti transaksi (transfer, kwitansi, screenshot)?", [("1", "Ya, saya memiliki bukti"), ("2", "Tidak ada bukti"), ("0", "← Kembali")])
            elif ui == "2":
                self.state = "SELESAI"
                return self._hasil("Tindak Pidana Pencurian", "Pasal 362 KUHP", "pidana", "Kasus Anda termasuk tindak pidana pencurian. Pelaku dapat diancam pidana penjara paling lama 5 tahun.", ["KTP / Identitas diri", "Bukti kepemilikan barang", "Laporan kehilangan (jika ada)", "Keterangan saksi"], "Advokat Pidana")
            return {"type": "error", "text": "Masukkan angka 1, 2, atau 0."}

        elif self.state == "PENIPUAN":
            if ui == "0":
                self.state = "PIDANA"
                return self._menu("Hukum Pidana", "pidana", "Pilih jenis kasus pidana:", [("1", "Penipuan"), ("2", "Pencurian"), ("0", "← Kembali")])
            elif ui in ("1", "2"):
                self.state = "SELESAI"
                catatan = "Bukti transaksi Anda akan memperkuat posisi hukum." if ui == "1" else "Meski tanpa bukti transaksi, keterangan saksi dan data digital tetap bisa digunakan."
                return self._hasil("Tindak Pidana Penipuan", "Pasal 378 KUHP", "pidana", f"Kasus Anda termasuk tindak pidana penipuan. {catatan}", ["KTP / Identitas diri", "Bukti transfer atau kwitansi", "Screenshot percakapan", "Bukti promosi dari pelaku", "Data rekening pelaku"], "Advokat Pidana")
            return {"type": "error", "text": "Masukkan angka 1, 2, atau 0."}

        elif self.state == "PERDATA":
            if ui == "0":
                self.state = "START"
                return self._menu_utama()
            elif ui == "1":
                self.state = "SELESAI"
                return self._hasil("Hutang Piutang", "Pasal 1754–1769 KUHPerdata", "perdata", "Kasus hutang piutang dapat diselesaikan melalui gugatan perdata atau mediasi di pengadilan.", ["KTP kedua pihak", "Perjanjian hutang", "Bukti pembayaran / transfer", "Surat tagihan", "Bukti komunikasi"], "Advokat Perdata")
            elif ui == "2":
                self.state = "SELESAI"
                return self._hasil("Wanprestasi", "Pasal 1243 KUHPerdata", "perdata", "Wanprestasi terjadi ketika pihak lain tidak memenuhi kewajiban kontrak. Anda berhak atas ganti rugi.", ["KTP / Identitas diri", "Salinan kontrak / perjanjian", "Bukti ingkar janji", "Bukti kerugian", "Surat somasi"], "Advokat Perdata")
            return {"type": "error", "text": "Masukkan angka 1, 2, atau 0."}

        elif self.state == "KELUARGA":
            if ui == "0":
                self.state = "START"
                return self._menu_utama()
            elif ui == "1":
                self.state = "SELESAI"
                return self._hasil("Perceraian", "UU No. 1/1974 jo. KHI", "keluarga", "Perceraian diajukan ke Pengadilan Agama (Muslim) atau Pengadilan Negeri (non-Muslim) dengan alasan yang sah secara hukum.", ["KTP suami dan istri", "Kartu Keluarga (KK)", "Buku Nikah / Akta Perkawinan", "Akta Kelahiran Anak", "Pernyataan alasan perceraian"], "Advokat Hukum Keluarga")
            elif ui == "2":
                self.state = "SELESAI"
                return self._hasil("Hak Asuh Anak", "Pasal 41 UU No. 1/1974", "keluarga", "Hak asuh ditentukan berdasarkan kepentingan terbaik anak. Pengadilan mempertimbangkan kemampuan finansial dan psikologis orang tua.", ["KTP orang tua", "Akta Kelahiran anak", "Akta Perceraian", "Bukti kemampuan finansial", "Bukti kelayakan tempat tinggal"], "Advokat Hukum Keluarga")
            return {"type": "error", "text": "Masukkan angka 1, 2, atau 0."}

        elif self.state == "KETENAGAKERJAAN":
            if ui == "0":
                self.state = "START"
                return self._menu_utama()
            elif ui == "1":
                self.state = "SELESAI"
                return self._hasil("Pemutusan Hubungan Kerja", "UU Cipta Kerja No. 11/2020", "ketenagakerjaan", "PHK harus melalui prosedur yang benar. Anda berhak atas pesangon, uang penghargaan masa kerja, dan uang penggantian hak.", ["KTP", "Perjanjian Kerja / Kontrak", "Surat PHK dari perusahaan", "Slip gaji 3 bulan terakhir", "Bukti masa kerja"], "Advokat Ketenagakerjaan")
            elif ui == "2":
                self.state = "SELESAI"
                return self._hasil("Perselisihan Hubungan Industrial", "UU No. 2/2004 (PPHI)", "ketenagakerjaan", "Perselisihan dapat diselesaikan melalui bipartit, mediasi Disnaker, atau Pengadilan Hubungan Industrial (PHI).", ["KTP", "Perjanjian Kerja / PKB", "Bukti perselisihan", "Risalah perundingan bipartit", "Surat dari Dinas Tenaga Kerja"], "Advokat Ketenagakerjaan")
            return {"type": "error", "text": "Masukkan angka 1, 2, atau 0."}

        elif self.state == "SELESAI":
            self.state = "START"
            return self._menu_utama("✨ Konsultasi selesai. Pilih kategori baru:")

        self.state = "START"
        return self._menu_utama()

    def _menu(self, title, icon, text, opts):
        return {"type": "menu", "title": title, "icon": icon, "text": text, "options": [{"key": k, "label": l} for k, l in opts]}

    def _hasil(self, title, pasal, kategori, text, dokumen, advokat):
        return {"type": "result", "title": title, "pasal": pasal, "kategori": kategori, "text": text, "dokumen": dokumen, "advokat": advokat}

    def _menu_utama(self, intro=None):
        return {"type": "menu", "title": "Menu Utama", "icon": "home", "text": intro or "⚖️ Selamat datang di LegalAssist! Pilih kategori hukum yang sesuai:", "options": [{"key": "1", "label": "⚖️ Pidana"}, {"key": "2", "label": "📋 Perdata"}, {"key": "3", "label": "👨‍👩‍👧 Keluarga"}, {"key": "4", "label": "💼 Ketenagakerjaan"}]}