class Mahasiswa:
    def __init__(self, nim: str, nama: str, no_hp: str):
        self.__nim = nim
        self.__nama = nama
        self.__no_hp = no_hp
        self.__status_aktif = False

    def get_nim(self) -> str:
        """Mengembalikan value NIM"""
        return self.__nim

    def get_nama(self) -> str:
        """Mengembalikan value Nama"""
        return self.__nama

    def get_no_hp(self) -> str:
        """Mengembalikan value Nomor HP"""
        return self.__no_hp

    def get_status_aktif(self) -> bool:
        """Mengembalikan status aktif peminjaman mahasiswa"""
        return self.__status_aktif

    def set_status_aktif(self, status: bool):
        """Mengubah status aktif peminjaman mahasiswa"""
        self.__status_aktif = status
