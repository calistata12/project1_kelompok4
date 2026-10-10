from kategori_alat import KategoriAlat

class Alat:

  def __init__(self, kode_alat, nama_alat, kategori, kondisi="Baik"):
    self.kode_alat = kode_alat
    self.nama_alat = nama_alat
    self.kategori = kategori
    self.kondisi = kondisi
    self.tersedia = True

  def set_kondisi(self, kondisi_baru):
    self.kondisi = kondisi_baru
    if kondisi_baru.lower() == "rusak berat":
      self.tersedia = False

  def set_tersedia(self, status):
    self.tersedia = status

  def get_info(self):
    status_str = "Tersedia" if self.tersedia else "Tidak Tersedia"
    return (
        f"[{self.kode_alat}] {self.nama_alat}"
        f" ({self.kategori.nama_kategori}) | Kondisi: {self.kondisi} | Status:"
        f" {status_str}"
    )