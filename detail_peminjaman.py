"""DetailPeminjaman: rincian satu item alat dalam sebuah transaksi.

Memakai class Alat milik kelompok (atribut: kode_alat, nama_alat, kondisi,
tersedia; method: set_kondisi(), set_tersedia()).
"""
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
    @property
    def sudah_dikembalikan(self):
        return self.tanggal_kembali is not None

    def kembalikan(self, kondisi, tanggal=None):
        """Catat pengembalian item ini dan perbarui kondisi + ketersediaan alat.

        Aturan 5: hanya kondisi "baik" yang membuat alat tersedia lagi.
        Rusak ringan / rusak berat -> tidak tersedia.
        """
        kondisi = kondisi.strip().lower()
        if kondisi not in KONDISI_VALID:
            raise ValueError(f"Kondisi harus salah satu dari: {', '.join(KONDISI_VALID)}")
        if self.sudah_dikembalikan:
            raise ValueError(f"Alat {self.alat.kode_alat} sudah dikembalikan.")
        self.kondisi_kembali = kondisi
        self.tanggal_kembali = tanggal or datetime.now()
        self.alat.set_kondisi(kondisi.title())            
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
        }

    def __str__(self):
        if self.sudah_dikembalikan:
            info = (f"dikembalikan {self.tanggal_kembali:%Y-%m-%d} "
                    f"({self.kondisi_kembali})")
        else:
            info = "masih dipinjam"
        return f"{self.alat.kode_alat} - {self.alat.nama_alat} x{self.jumlah} [{info}]"