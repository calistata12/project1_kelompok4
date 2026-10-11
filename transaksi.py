"""TransaksiPeminjaman: induk transaksi, berisi list DetailPeminjaman.

Memakai class milik kelompok:
    Mahasiswa: get_nim(), get_nama()
    Alat:      kode_alat, nama_alat, tersedia, set_tersedia(), set_kondisi()
"""
from datetime import datetime, timedelta

from detail_peminjaman import DetailPeminjaman

STATUS_DIPINJAM = "Dipinjam"
STATUS_SEBAGIAN = "Sebagian Dikembalikan"
STATUS_SELESAI = "Selesai"

MAKS_HARI_PINJAM = 7
MAKS_TRANSAKSI_AKTIF = 2   


class TransaksiPeminjaman:
    def __init__(self, id_transaksi, mahasiswa, tanggal_pinjam=None,
                 lama_hari=MAKS_HARI_PINJAM):
        if not 1 <= lama_hari <= MAKS_HARI_PINJAM:
            raise ValueError(f"Lama peminjaman harus 1-{MAKS_HARI_PINJAM} hari.")
        self.id_transaksi = id_transaksi
        self.mahasiswa = mahasiswa
        self.daftar_detail = []                      # list[DetailPeminjaman]
        self.tanggal_pinjam = tanggal_pinjam or datetime.now()
        self.batas_kembali = self.tanggal_pinjam + timedelta(days=lama_hari)
        self.status = STATUS_DIPINJAM

    # ---------- isi transaksi ----------
    def tambah_alat(self, alat, jumlah=1):
        """Tambah alat ke transaksi (Aturan 1 & 3)."""
        if not alat.tersedia:
            raise ValueError(f"Alat {alat.kode_alat} - {alat.nama_alat} tidak tersedia.")
        if self.cari_detail(alat.kode_alat):
            raise ValueError(f"Alat {alat.kode_alat} sudah ada di transaksi ini.")
        alat.set_tersedia(False)           # alat sedang dipinjam
        detail = DetailPeminjaman(alat, jumlah)
        self.daftar_detail.append(detail)
        return detail

    def cari_detail(self, kode_alat):
        for d in self.daftar_detail:
            if d.alat.kode_alat == kode_alat:
                return d
        return None

    # ---------- pengembalian ----------
    def kembalikan_alat(self, kode_alat, kondisi, tanggal=None):
        """Kembalikan satu alat (Aturan 4 & 5), lalu perbarui status transaksi."""
        detail = self.cari_detail(kode_alat)
        if detail is None:
            raise ValueError(f"Alat {kode_alat} tidak ada di transaksi {self.id_transaksi}.")
        detail.kembalikan(kondisi, tanggal)
        self._perbarui_status()
        return detail

    def _perbarui_status(self):
        sudah = sum(1 for d in self.daftar_detail if d.sudah_dikembalikan)
        if sudah == 0:
            self.status = STATUS_DIPINJAM
        elif sudah < len(self.daftar_detail):
            self.status = STATUS_SEBAGIAN
        else:
            self.status = STATUS_SELESAI

    # ---------- query ----------
    @property
    def aktif(self):
        """Aturan 4: transaksi aktif sampai SEMUA alat dikembalikan."""
        return self.status != STATUS_SELESAI

    def milik(self, nim):
        """True jika transaksi ini milik mahasiswa ber-NIM tersebut."""
        return self.mahasiswa.get_nim() == nim

    def alat_belum_kembali(self):
        return [d for d in self.daftar_detail if not d.sudah_dikembalikan]

    def memuat_alat(self, kode_alat):
        """Aturan 6: apakah alat masih tercatat di transaksi aktif ini."""
        d = self.cari_detail(kode_alat)
        return self.aktif and d is not None and not d.sudah_dikembalikan

    def terlambat(self, sekarang=None):
        return self.aktif and (sekarang or datetime.now()) > self.batas_kembali

    def hari_terlambat(self, sekarang=None):
        if not self.terlambat(sekarang):
            return 0
        return ((sekarang or datetime.now()) - self.batas_kembali).days

    def to_dict(self):
        return {
            "id_transaksi": self.id_transaksi,
            "nim": self.mahasiswa.get_nim(),
            "nama_mahasiswa": self.mahasiswa.get_nama(),
            "tanggal_pinjam": self.tanggal_pinjam.strftime("%Y-%m-%d %H:%M"),
            "batas_kembali": self.batas_kembali.strftime("%Y-%m-%d"),
            "status": self.status,
            "detail": [d.to_dict() for d in self.daftar_detail],
        }

    def __str__(self):
        baris = [
            f"Transaksi : {self.id_transaksi}",
            f"Peminjam  : {self.mahasiswa.get_nim()} - {self.mahasiswa.get_nama()}",
            f"Tgl pinjam: {self.tanggal_pinjam:%Y-%m-%d}",
            f"Batas     : {self.batas_kembali:%Y-%m-%d}",
            f"Status    : {self.status}",
            "Alat      :",
        ]
        baris += [f"  - {d}" for d in self.daftar_detail]
        return "\n".join(baris)