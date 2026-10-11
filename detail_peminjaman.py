from datetime import datetime

KONDISI_VALID = ("baik", "rusak ringan", "rusak berat")


class DetailPeminjaman:
    def __init__(self, alat, jumlah=1):
        if jumlah < 1:
            raise ValueError("Jumlah harus minimal 1.")
        self.alat = alat
        self.jumlah = jumlah
        self.kondisi_kembali = None
        self.tanggal_kembali = None
        self.hari_terlambat = 0

    @property
    def sudah_dikembalikan(self):
        return self.tanggal_kembali is not None

    def kembalikan(self, kondisi, tanggal=None, hari_terlambat=0):
        kondisi = kondisi.strip().lower()
        if kondisi not in KONDISI_VALID:
            raise ValueError(f"Kondisi harus salah satu dari: {', '.join(KONDISI_VALID)}")
        if self.sudah_dikembalikan:
            raise ValueError(f"Alat {self.alat.kode_alat} sudah dikembalikan.")
        self.kondisi_kembali = kondisi.title()
        self.tanggal_kembali = tanggal or datetime.now()
        self.hari_terlambat = hari_terlambat
        self.alat.set_kondisi(self.kondisi_kembali)
        self.alat.set_tersedia(kondisi == "baik")

    def to_dict(self):
        return {
            "kode_alat": self.alat.kode_alat,
            "nama_alat": self.alat.nama_alat,
            "jumlah": self.jumlah,
            "kondisi_kembali": self.kondisi_kembali,
            "tanggal_kembali": (
                self.tanggal_kembali.strftime("%Y-%m-%d %H:%M")
                if self.tanggal_kembali else None
            ),
            "hari_terlambat": self.hari_terlambat,
        }

    def __str__(self):
        if self.sudah_dikembalikan:
            info = (f"dikembalikan {self.tanggal_kembali:%Y-%m-%d} "
                    f"({self.kondisi_kembali})")
            if self.hari_terlambat:
                info += f", terlambat {self.hari_terlambat} hari"
        else:
            info = "masih dipinjam"
        return f"{self.alat.kode_alat} - {self.alat.nama_alat} x{self.jumlah} [{info}]"