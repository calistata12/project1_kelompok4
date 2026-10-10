class KategoriAlat:

  def __init__(self, nama_kategori):
    self.nama_kategori = nama_kategori

  def get_info(self):
    return f"Kategori: {self.nama_kategori}"