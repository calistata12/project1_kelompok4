from datetime import datetime, timedelta

from alat import Alat
from kategori_alat import KategoriAlat
from mahasiswa import Mahasiswa
from transaksi import (
    MAKS_HARI_PINJAM,
    MAKS_TRANSAKSI_AKTIF,
    TransaksiPeminjaman,
)

DAFTAR_MAHASISWA = {}
DAFTAR_KATEGORI = {}
DAFTAR_ALAT = {}
DAFTAR_TRANSAKSI = []

KONDISI_PILIHAN = ("Baik", "Rusak Ringan", "Rusak Berat")
_id_transaksi = [0]


def id_transaksi_baru():
    """Membuat ID transaksi unik: TRX-001, TRX-002, ..."""
    _id_transaksi[0] += 1
    return f"TRX-{_id_transaksi[0]:03d}"


LOG_AKTIVITAS = []


def catat_aktivitas(pesan, waktu=None):
    """Mencatat satu baris log aktivitas program.

    Format tampilan layaknya contoh soal:
      [2026-08-10 10:15] Mahasiswa 2410512001 ditambahkan
    """
    LOG_AKTIVITAS.append({"waktu": waktu or datetime.now(), "pesan": pesan})


def _jumlah_unit(jumlah):
    """Mengubah angka jumlah jadi kata, contoh: 2 -> 'Dua' (seperti soal)."""
    kamus = {1: "Satu", 2: "Dua", 3: "Tiga", 4: "Empat", 5: "Lima",
             6: "Enam", 7: "Tujuh", 8: "Delapan", 9: "Sembilan",
             10: "Sepuluh"}
    return kamus.get(jumlah, str(jumlah))


def catat_pembuatan_transaksi(trx):
    """Log pembuatan transaksi beserta setiap alat yang ikut dipinjam."""
    catat_aktivitas(
        f"Transaksi {trx.id_transaksi} dibuat "
        f"(peminjam {trx.mahasiswa.get_nim()} - {trx.mahasiswa.get_nama()})",
        trx.tanggal_pinjam)
    for detail in trx.daftar_detail:
        catat_aktivitas(f"{_jumlah_unit(detail.jumlah)} unit "
                        f"{detail.alat.nama_alat} dipinjam "
                        f"(trx {trx.id_transaksi})", trx.tanggal_pinjam)


def catat_pengembalian(trx, detail):
    """Log pengembalian satu alat pada sebuah transaksi."""
    catat_aktivitas(
        f"{_jumlah_unit(detail.jumlah)} unit {detail.alat.nama_alat} "
        f"dikembalikan (kondisi {detail.kondisi_kembali}) "
        f"(trx {trx.id_transaksi})", detail.tanggal_kembali)


def siapkan_data():
    """Mengisi data awal mahasiswa, kategori, alat, dan contoh transaksi."""
    waktu_data = datetime.now() - timedelta(days=16)
    for nama_kategori in ("Perangkat Komputasi", "Perangkat Jaringan",
                          "Perangkat Multimedia"):
        DAFTAR_KATEGORI[nama_kategori] = KategoriAlat(nama_kategori)
        catat_aktivitas(f"Kategori '{nama_kategori}' ditambahkan", waktu_data)

    for nim, nama, nohp in [
        ("2410512001", "Andi Wijaya", "081234567890"),
        ("2410512002", "Siti Rahmawati", "081298765432"),
        ("2410512003", "Budi Santoso", "081377766655"),
        ("2410512004", "Rina Amelia", "081355544433"),
    ]:
        DAFTAR_MAHASISWA[nim] = Mahasiswa(nim, nama, nohp)
        catat_aktivitas(f"Mahasiswa {nim} ({nama}) ditambahkan", waktu_data)

    for kode, nama, nama_kategori, kondisi in [
        ("AL001", "Laptop ASUS Core i5", "Perangkat Komputasi", "Baik"),
        ("AL002", "PC Desktop Lab", "Perangkat Komputasi", "Baik"),
        ("AL003", "Arduino Uno Kit", "Perangkat Komputasi", "Baik"),
        ("AL004", "Raspberry Pi 4 Kit", "Perangkat Komputasi", "Baik"),
        ("AL005", "Kabel LAN (UTP) + Crimping", "Perangkat Jaringan", "Baik"),
        ("AL006", "Switch Hub 8 Port", "Perangkat Jaringan", "Baik"),
        ("AL007", "Router Mikrotik hEX", "Perangkat Jaringan", "Baik"),
        ("AL008", "Kamera Digital Canon", "Perangkat Multimedia", "Baik"),
        ("AL009", "Tripod Kamera", "Perangkat Multimedia", "Baik"),
        ("AL010", "Proyektor Mini", "Perangkat Multimedia", "Rusak Berat"),
    ]:
        alat = Alat(kode, nama, DAFTAR_KATEGORI[nama_kategori])
        if kondisi != "Baik":
            alat.set_kondisi(kondisi)
        DAFTAR_ALAT[kode] = alat
        catat_aktivitas(f"Alat {kode} - {nama} ({nama_kategori}, "
                        f"kondisi {kondisi}) ditambahkan", waktu_data)

    _buat_contoh_transaksi()


def _buat_contoh_transaksi():
    """Beberapa data transaksi contoh agar riwayat dan status tidak kosong."""
    sekarang = datetime.now()

    trx1 = TransaksiPeminjaman(
        id_transaksi_baru(), DAFTAR_MAHASISWA["2410512001"],
        tanggal_pinjam=sekarang - timedelta(days=10), lama_hari=7)
    trx1.tambah_alat(DAFTAR_ALAT["AL003"])
    trx1.tambah_alat(DAFTAR_ALAT["AL004"])
    trx1.kembalikan_alat("AL003", "baik",
                         tanggal=sekarang - timedelta(days=8))
    DAFTAR_TRANSAKSI.append(trx1)
    catat_pembuatan_transaksi(trx1)
    catat_pengembalian(trx1, trx1.cari_detail("AL003"))

    trx2 = TransaksiPeminjaman(
        id_transaksi_baru(), DAFTAR_MAHASISWA["2410512002"],
        tanggal_pinjam=sekarang - timedelta(days=15), lama_hari=7)
    trx2.tambah_alat(DAFTAR_ALAT["AL001"])
    trx2.tambah_alat(DAFTAR_ALAT["AL002"])
    trx2.kembalikan_alat("AL001", "baik",
                         tanggal=sekarang - timedelta(days=13))
    trx2.kembalikan_alat("AL002", "rusak ringan",
                         tanggal=sekarang - timedelta(days=13))
    DAFTAR_TRANSAKSI.append(trx2)
    catat_pembuatan_transaksi(trx2)
    catat_pengembalian(trx2, trx2.cari_detail("AL001"))
    catat_pengembalian(trx2, trx2.cari_detail("AL002"))

    trx3 = TransaksiPeminjaman(
        id_transaksi_baru(), DAFTAR_MAHASISWA["2410512003"],
        tanggal_pinjam=sekarang - timedelta(days=1), lama_hari=7)
    trx3.tambah_alat(DAFTAR_ALAT["AL005"])
    DAFTAR_TRANSAKSI.append(trx3)
    catat_pembuatan_transaksi(trx3)

    LOG_AKTIVITAS.sort(key=lambda catatan: catatan["waktu"])

    for mhs in DAFTAR_MAHASISWA.values():
        mhs.set_status_aktif(_punya_transaksi_aktif(mhs.get_nim()))


def judul(teks):
    print("\n" + "=" * 62)
    print(teks.center(62))
    print("=" * 62)


def garis():
    print("-" * 62)


def jeda():
    input("\nTekan ENTER untuk kembali ke menu...")


def baca_int(pesan, minimum=None, maksimum=None, wajib=True):
    """Membaca input angka; mengembalikan None bila tidak wajib & kosong."""
    while True:
        teks = input(pesan).strip()
        if not teks:
            if not wajib:
                return None
            print("  Input tidak boleh kosong.")
            continue
        try:
            nilai = int(teks)
        except ValueError:
            print("  Input harus berupa angka.")
            continue
        if minimum is not None and nilai < minimum:
            print(f"  Input minimal {minimum}.")
            continue
        if maksimum is not None and nilai > maksimum:
            print(f"  Input maksimal {maksimum}.")
            continue
        return nilai


def transaksi_mahasiswa(nim, hanya_aktif=False):
    hasil = [t for t in DAFTAR_TRANSAKSI if t.milik(nim)]
    if hanya_aktif:
        hasil = [t for t in hasil if t.aktif]
    return hasil


def _punya_transaksi_aktif(nim):
    return any(t.milik(nim) and t.aktif for t in DAFTAR_TRANSAKSI)


def sinkron_status_mahasiswa(mhs):
    """Menyesuaikan field status aktif mahasiswa dengan data transaksi."""
    mhs.set_status_aktif(_punya_transaksi_aktif(mhs.get_nim()))
    return mhs


def teks_status_peminjaman(mhs):
    return "MEMINJAM alat" if mhs.get_status_aktif() else "tidak meminjam"


def pilih_mahasiswa():
    """Menampilkan daftar mahasiswa lalu meminta NIM. None bila batal."""
    if not DAFTAR_MAHASISWA:
        print("  Belum ada data mahasiswa.")
        return None
    print("\nDaftar mahasiswa:")
    for mhs in DAFTAR_MAHASISWA.values():
        sinkron_status_mahasiswa(mhs)
        print(f"  [{mhs.get_nim()}] {mhs.get_nama():<20} - "
              f"{teks_status_peminjaman(mhs)}")
    nim = input("\nMasukkan NIM (kosong = batal): ").strip()
    if not nim:
        return None
    mhs = DAFTAR_MAHASISWA.get(nim)
    if mhs is None:
        print(f"  [!] NIM {nim} tidak ditemukan.")
        return None
    return mhs


def cetak_transaksi(trx, rinci=True):
    """Menampilkan satu transaksi lengkap dengan peringatan keterlambatan."""
    print(f"  ID transaksi   : {trx.id_transaksi}")
    print(f"  Peminjam       : {trx.mahasiswa.get_nim()} - "
          f"{trx.mahasiswa.get_nama()}")
    print(f"  Tanggal pinjam : {trx.tanggal_pinjam:%Y-%m-%d %H:%M}")
    print(f"  Batas kembali  : {trx.batas_kembali:%Y-%m-%d}")
    print(f"  Status         : {trx.status}")
    if trx.terlambat():
        print(f"  Peringatan     : TERLAMBAT {trx.hari_terlambat()} hari!")
    if rinci:
        print("  Alat           :")
        for detail in trx.daftar_detail:
            print(f"    - {detail}")


def menu_status_mahasiswa():
    judul("STATUS MAHASISWA")
    mhs = pilih_mahasiswa()
    if mhs is None:
        return

    nim = mhs.get_nim()
    semua = transaksi_mahasiswa(nim)
    sinkron_status_mahasiswa(mhs)
    aktif = [t for t in semua if t.aktif]

    print("\n--- Data Mahasiswa ---")
    print(f"  NIM              : {nim}")
    print(f"  Nama             : {mhs.get_nama()}")
    print(f"  No. HP           : {mhs.get_no_hp()}")
    print(f"  Status peminjaman: {teks_status_peminjaman(mhs)}")
    print(f"  Total transaksi  : {len(semua)} ({len(aktif)} aktif)")

    if not aktif:
        print("\n  Mahasiswa tidak memiliki peminjaman aktif.")
        return

    print("\n--- Peminjaman Aktif ---")
    for trx in aktif:
        garis()
        cetak_transaksi(trx)


def tampilkan_kondisi_alat():
    print("\n--- Kondisi Alat ---")
    for alat in DAFTAR_ALAT.values():
        print(f"  [{alat.kode_alat}] {alat.nama_alat:<28} "
              f"({alat.kategori.nama_kategori}) | Kondisi: {alat.kondisi}")


def tampilkan_ketersediaan_alat():
    print("\n--- Ketersediaan Alat ---")
    for alat in DAFTAR_ALAT.values():
        print(f"  {alat.get_info()}")
    jumlah = sum(1 for a in DAFTAR_ALAT.values() if a.tersedia)
    print(f"\n  Total: {jumlah} tersedia dari {len(DAFTAR_ALAT)} alat.")


def tampilkan_alat_dipinjam():
    print("\n--- Alat yang Sedang Dipinjam ---")
    ditemukan = False
    for trx in DAFTAR_TRANSAKSI:
        belum = trx.alat_belum_kembali()
        if not trx.aktif or not belum:
            continue
        ditemukan = True
        catatan = " [TERLAMBAT]" if trx.terlambat() else ""
        print(f"  {trx.id_transaksi} | {trx.mahasiswa.get_nim()} - "
              f"{trx.mahasiswa.get_nama()} | batas "
              f"{trx.batas_kembali:%Y-%m-%d}{catatan}")
        for detail in belum:
            print(f"    - {detail}")
    if not ditemukan:
        print("  Belum ada alat yang sedang dipinjam.")


def menu_tambah_kategori():
    """Menambah kategori alat baru tanpa mengubah struktur program."""
    judul("TAMBAH KATEGORI ALAT")
    tampilkan_daftar_kategori()
    nama = input("\nNama kategori baru (kosong = batal): ").strip()
    if not nama:
        print("  Pembatalan, kategori tidak ditambahkan.")
        return
    for kategori in DAFTAR_KATEGORI.values():
        if kategori.nama_kategori.lower() == nama.lower():
            print(f"  [!] Kategori '{nama}' sudah ada.")
            return
    DAFTAR_KATEGORI[nama] = KategoriAlat(nama)
    catat_aktivitas(f"Kategori '{nama}' ditambahkan")
    print(f"  [OK] Kategori '{nama}' berhasil ditambahkan.")


def tampilkan_daftar_kategori():
    print("\n--- Daftar Kategori Alat ---")
    for kategori in DAFTAR_KATEGORI.values():
        jumlah = sum(1 for a in DAFTAR_ALAT.values()
                     if a.kategori.nama_kategori == kategori.nama_kategori)
        print(f"  - {kategori.nama_kategori} ({jumlah} alat)")


def menu_tambah_alat():
    """Menambah alat baru; kategori dipilih dari daftar kategori dinamis."""
    judul("TAMBAH ALAT BARU")
    if not DAFTAR_KATEGORI:
        print("  [!] Belum ada kategori. Tambah kategori terlebih dahulu.")
        return

    daftar_kategori = list(DAFTAR_KATEGORI.values())
    tampilkan_daftar_kategori()
    pilihan = baca_int("\nPilihan kategori: ", minimum=1,
                       maksimum=len(daftar_kategori))
    kategori = daftar_kategori[pilihan - 1]

    while True:
        kode = input("\nKode alat (kosong = batal): ").strip().upper()
        if not kode:
            print("  Pembatalan, alat tidak ditambahkan.")
            return
        if kode in DAFTAR_ALAT:
            print(f"  [!] Kode {kode} sudah dipakai alat lain.")
            continue
        break

    nama = input("Nama alat: ").strip()
    if not nama:
        print("  Pembatalan, nama alat tidak boleh kosong.")
        return

    alat = Alat(kode, nama, kategori, kondisi="Baik")
    DAFTAR_ALAT[kode] = alat
    catat_aktivitas(f"Alat {kode} - {nama} ({kategori.nama_kategori}, "
                    f"kondisi Baik) ditambahkan")
    print(f"\n  [OK] Alat {kode} - {nama} ({kategori.nama_kategori}) "
          f"berhasil ditambahkan dengan kondisi Baik.")


def menu_alat():
    while True:
        judul("DATA ALAT")
        print("1. Kondisi alat")
        print("2. Ketersediaan alat")
        print("3. Alat yang sedang dipinjam")
        print("4. Tambah kategori baru")
        print("5. Tambah alat baru")
        print("0. Kembali ke menu utama")
        pilihan = baca_int("\nPilihan: ", minimum=0, maksimum=5, wajib=False)

        if pilihan in (None, 0):
            return
        elif pilihan == 1:
            tampilkan_kondisi_alat()
        elif pilihan == 2:
            tampilkan_ketersediaan_alat()
        elif pilihan == 3:
            tampilkan_alat_dipinjam()
        elif pilihan == 4:
            menu_tambah_kategori()
        elif pilihan == 5:
            menu_tambah_alat()
        jeda()


def menu_pinjam_alat():
    judul("PINJAM ALAT")
    mhs = pilih_mahasiswa()
    if mhs is None:
        return

    nim = mhs.get_nim()
    aktif = transaksi_mahasiswa(nim, hanya_aktif=True)
    if len(aktif) >= MAKS_TRANSAKSI_AKTIF:
        print(f"\n  [!] Mahasiswa sudah memiliki {len(aktif)} transaksi aktif "
              f"(maksimal {MAKS_TRANSAKSI_AKTIF}).")
        print("      Silakan kembalikan alat terlebih dahulu.")
        return

    tersedia = [a for a in DAFTAR_ALAT.values() if a.tersedia]
    if not tersedia:
        print("\n  [!] Semua alat sedang tidak tersedia.")
        return

    print("\n--- Alat yang Tersedia ---")
    for alat in tersedia:
        print(f"  [{alat.kode_alat}] {alat.nama_alat:<28} "
              f"({alat.kategori.nama_kategori}) | Kondisi: {alat.kondisi}")

    pilihan = []
    while True:
        kode = input("\nKode alat yang dipinjam (kosong = selesai): ").strip()
        if not kode:
            break
        kode = kode.upper()
        if kode in pilihan:
            print("  Alat sudah dipilih sebelumnya.")
            continue
        alat = DAFTAR_ALAT.get(kode)
        if alat is None:
            print("  [!] Kode alat tidak ditemukan.")
            continue
        if not alat.tersedia:
            print(f"  [!] {kode} - {alat.nama_alat} tidak tersedia.")
            continue
        pilihan.append(kode)
        print(f"  + {alat.nama_alat} dipilih.")

    if not pilihan:
        print("\n  Tidak ada alat dipilih, transaksi dibatalkan.")
        return

    print(f"\nLama peminjaman 1-{MAKS_HARI_PINJAM} hari "
          f"(ENTER = {MAKS_HARI_PINJAM} hari).")
    lama = baca_int("Lama peminjaman: ", minimum=1,
                    maksimum=MAKS_HARI_PINJAM, wajib=False)
    if lama is None:
        lama = MAKS_HARI_PINJAM

    trx = None
    try:
        trx = TransaksiPeminjaman(id_transaksi_baru(), mhs, lama_hari=lama)
        for kode in pilihan:
            trx.tambah_alat(DAFTAR_ALAT[kode])
    except ValueError as pesan:
        if trx is not None:
            for detail in trx.daftar_detail:
                detail.alat.set_tersedia(True)
        print(f"\n  [!] Gagal membuat transaksi: {pesan}")
        return

    DAFTAR_TRANSAKSI.append(trx)
    mhs.set_status_aktif(True)
    catat_pembuatan_transaksi(trx)
    print("\n  [OK] Peminjaman berhasil dicatat.")
    garis()
    cetak_transaksi(trx)


def menu_pengembalian_alat():
    judul("PENGEMBALIAN ALAT")
    mhs = pilih_mahasiswa()
    if mhs is None:
        return

    nim = mhs.get_nim()
    aktif = transaksi_mahasiswa(nim, hanya_aktif=True)
    if not aktif:
        print("\n  Mahasiswa tidak memiliki transaksi aktif.")
        return

    if len(aktif) == 1:
        trx = aktif[0]
    else:
        print("\n--- Transaksi Aktif Mahasiswa ---")
        for t in aktif:
            print(f"  {t.id_transaksi} | batas {t.batas_kembali:%Y-%m-%d} "
                  f"| {t.status}")
        id_trx = input("\nMasukkan ID transaksi: ").strip().upper()
        trx = next((t for t in aktif
                    if t.id_transaksi.upper() == id_trx), None)
        if trx is None:
            print("  [!] ID transaksi tidak ditemukan.")
            return

    belum = trx.alat_belum_kembali()
    print(f"\n--- Alat yang belum dikembalikan ({trx.id_transaksi}) ---")
    for detail in belum:
        print(f"    - {detail}")
    if not belum:
        print("  Semua alat pada transaksi ini sudah dikembalikan.")
        return

    kode = input("\nKode alat yang dikembalikan: ").strip().upper()
    if kode not in {d.alat.kode_alat for d in belum}:
        print("  [!] Alat tidak ada dalam transaksi ini.")
        return

    print("\nKondisi alat saat dikembalikan:")
    for i, kondisi in enumerate(KONDISI_PILIHAN, start=1):
        print(f"  {i}. {kondisi}")
    pilihan = baca_int("Pilihan kondisi: ", minimum=1,
                       maksimum=len(KONDISI_PILIHAN))
    kondisi = KONDISI_PILIHAN[pilihan - 1]

    try:
        detail = trx.kembalikan_alat(kode, kondisi)
    except ValueError as pesan:
        print(f"  [!] Gagal: {pesan}")
        return

    catat_pengembalian(trx, detail)
    print(f"\n  [OK] {kode} berhasil dikembalikan dengan kondisi "
          f"'{kondisi.title()}'.")
    if not trx.aktif:
        print(f"  Transaksi {trx.id_transaksi} SELESAI - semua alat kembali.")
        sinkron_status_mahasiswa(mhs)
        if not mhs.get_status_aktif():
            print("  Status peminjaman mahasiswa menjadi: tidak meminjam.")
    else:
        print("  Transaksi masih berjalan, ada alat yang belum kembali.")
    garis()
    cetak_transaksi(trx)


def menu_status_transaksi():
    judul("STATUS TRANSAKSI")
    nim = input("Filter NIM (kosong = semua transaksi): ").strip()
    daftar = [t for t in DAFTAR_TRANSAKSI if not nim or t.milik(nim)]

    if not daftar:
        pesan = (f"Tidak ada transaksi untuk NIM {nim}."
                 if nim else "Belum ada transaksi.")
        print(f"\n  {pesan}")
        return

    print(f"\n--- Daftar Transaksi ({len(daftar)}) ---")
    for trx in daftar:
        garis()
        cetak_transaksi(trx)
    garis()


def menu_transaksi():
    while True:
        judul("TRANSAKSI")
        print("1. Pinjam alat")
        print("2. Pengembalian alat")
        print("3. Status transaksi")
        print("0. Kembali ke menu utama")
        pilihan = baca_int("\nPilihan: ", minimum=0, maksimum=3, wajib=False)

        if pilihan in (None, 0):
            return
        elif pilihan == 1:
            menu_pinjam_alat()
        elif pilihan == 2:
            menu_pengembalian_alat()
        elif pilihan == 3:
            menu_status_transaksi()
        jeda()


def menu_riwayat_pinjaman():
    judul("RIWAYAT PINJAMAN")
    mhs = pilih_mahasiswa()
    if mhs is None:
        return

    nim = mhs.get_nim()
    daftar = sorted(transaksi_mahasiswa(nim),
                    key=lambda t: t.tanggal_pinjam, reverse=True)
    if not daftar:
        print("\n  Belum ada riwayat peminjaman untuk mahasiswa ini.")
        return

    print(f"\n  Riwayat peminjaman {nim} - {mhs.get_nama()} "
          f"({len(daftar)} transaksi)")
    total_alat = 0
    masih_dipinjam = 0
    for trx in daftar:
        garis()
        print(f"  {trx.id_transaksi} | pinjam "
              f"{trx.tanggal_pinjam:%Y-%m-%d} | batas "
              f"{trx.batas_kembali:%Y-%m-%d} | {trx.status}")
        for detail in trx.daftar_detail:
            total_alat += 1
            if detail.sudah_dikembalikan:
                info = (f"kembali {detail.tanggal_kembali:%Y-%m-%d} | "
                        f"kondisi {detail.kondisi_kembali}")
            else:
                info = "masih dipinjam"
                masih_dipinjam += 1
            print(f"     - {detail.alat.kode_alat} {detail.alat.nama_alat} "
                  f"x{detail.jumlah} | {info}")
    garis()
    print(f"  Total alat dipinjam : {total_alat}")
    print(f"  Masih dipinjam      : {masih_dipinjam}")
    print(f"  Sudah dikembalikan  : {total_alat - masih_dipinjam}")


def menu_hapus_mahasiswa():
    """Mahasiswa hanya boleh dihapus jika tidak punya transaksi aktif."""
    judul("HAPUS DATA MAHASISWA")
    mhs = pilih_mahasiswa()
    if mhs is None:
        return

    nim = mhs.get_nim()
    aktif = transaksi_mahasiswa(nim, hanya_aktif=True)
    if aktif:
        print(f"\n  [!] NIM {nim} tidak boleh dihapus (Aturan 6).")
        print(f"      Masih memiliki {len(aktif)} transaksi peminjaman aktif:")
        for trx in aktif:
            print(f"        - {trx.id_transaksi} | batas "
                  f"{trx.batas_kembali:%Y-%m-%d} | {trx.status}")
        print("      Selesaikan peminjaman alat terlebih dahulu.")
        return

    konfirmasi = input(f"\nHapus {nim} - {mhs.get_nama()}? (y/t): ").strip()
    if konfirmasi.lower() not in ("y", "ya"):
        print("  Penghapusan dibatalkan.")
        return

    del DAFTAR_MAHASISWA[nim]
    catat_aktivitas(f"Mahasiswa {nim} ({mhs.get_nama()}) dihapus")
    print(f"  [OK] Data mahasiswa {nim} berhasil dihapus.")
    print("       Riwayat peminjaman lama tetap tersimpan pada daftar transaksi.")


def menu_hapus_alat():
    """Alat hanya boleh dihapus jika tidak tercatat di transaksi aktif."""
    judul("HAPUS DATA ALAT")
    if not DAFTAR_ALAT:
        print("  Belum ada data alat.")
        return
    tampilkan_kondisi_alat()

    kode = input("\nKode alat yang dihapus (kosong = batal): ").strip().upper()
    if not kode:
        print("  Penghapusan dibatalkan.")
        return
    alat = DAFTAR_ALAT.get(kode)
    if alat is None:
        print(f"  [!] Kode alat {kode} tidak ditemukan.")
        return

    for trx in DAFTAR_TRANSAKSI:
        if trx.aktif and trx.cari_detail(kode) is not None:
            print(f"\n  [!] Alat {kode} - {alat.nama_alat} tidak boleh "
                  f"dihapus (Aturan 6).")
            print(f"      Masih tercatat pada transaksi aktif {trx.id_transaksi} "
                  f"milik {trx.mahasiswa.get_nim()}.")
            print("      Kembalikan alat tersebut terlebih dahulu.")
            return

    konfirmasi = input(f"\nHapus {kode} - {alat.nama_alat}? (y/t): ").strip()
    if konfirmasi.lower() not in ("y", "ya"):
        print("  Penghapusan dibatalkan.")
        return

    del DAFTAR_ALAT[kode]
    catat_aktivitas(f"Alat {kode} - {alat.nama_alat} dihapus")
    print(f"  [OK] Alat {kode} - {alat.nama_alat} berhasil dihapus.")


def menu_hapus_data():
    while True:
        judul("HAPUS DATA")
        print("1. Hapus data mahasiswa")
        print("2. Hapus data alat")
        print("0. Kembali ke menu utama")
        pilihan = baca_int("\nPilihan: ", minimum=0, maksimum=2, wajib=False)

        if pilihan in (None, 0):
            return
        elif pilihan == 1:
            menu_hapus_mahasiswa()
        elif pilihan == 2:
            menu_hapus_alat()
        jeda()


def tampilkan_log_aktivitas():
    if not LOG_AKTIVITAS:
        print("\n  Belum ada aktivitas yang tercatat.")
        return
    print(f"\n--- Log Aktivitas ({len(LOG_AKTIVITAS)} catatan, terbaru dulu) ---")
    for catatan in sorted(LOG_AKTIVITAS, key=lambda c: c["waktu"],
                          reverse=True):
        print(f"  [{catatan['waktu']:%Y-%m-%d %H:%M}] {catatan['pesan']}")


def menu_log_aktivitas():
    judul("LOG AKTIVITAS")
    tampilkan_log_aktivitas()


def menu_log_aktivitas_mahasiswa():
    """Log aktivitas milik satu mahasiswa (NIM + semua ID transaksinya)."""
    judul("LOG AKTIVITAS MAHASISWA")
    if not LOG_AKTIVITAS:
        print("\n  Belum ada aktivitas yang tercatat.")
        return
    mhs = pilih_mahasiswa()
    if mhs is None:
        return

    nim = mhs.get_nim()
    kunci = {nim}
    kunci.update(t.id_transaksi for t in transaksi_mahasiswa(nim))

    hasil = [c for c in LOG_AKTIVITAS
             if any(word in c["pesan"] for word in kunci)]
    if not hasil:
        print(f"\n  Tidak ada aktivitas untuk NIM {nim}.")
        return
    print(f"\n--- Log Aktivitas {nim} - {mhs.get_nama()} "
          f"({len(hasil)} catatan) ---")
    for catatan in sorted(hasil, key=lambda c: c["waktu"], reverse=True):
        print(f"  [{catatan['waktu']:%Y-%m-%d %H:%M}] {catatan['pesan']}")


def menu_log():
    while True:
        judul("LOG AKTIVITAS")
        print("1. Semua log aktivitas")
        print("2. Log aktivitas per mahasiswa")
        print("0. Kembali ke menu utama")
        pilihan = baca_int("\nPilihan: ", minimum=0, maksimum=2, wajib=False)

        if pilihan in (None, 0):
            return
        elif pilihan == 1:
            menu_log_aktivitas()
        elif pilihan == 2:
            menu_log_aktivitas_mahasiswa()
        jeda()


def _statistik_alat():
    """Menghitung frequency setiap alat dipinjam (per unit)."""
    hitung = {}
    for trx in DAFTAR_TRANSAKSI:
        for detail in trx.daftar_detail:
            kunci = detail.alat.nama_alat
            hitung[kunci] = hitung.get(kunci, 0) + detail.jumlah
    return hitung


def _statistik_mahasiswa():
    """Menghitung frequency setiap mahasiswa membuat transaksi."""
    hitung = {}
    for trx in DAFTAR_TRANSAKSI:
        nim = trx.mahasiswa.get_nim()
        nama = trx.mahasiswa.get_nama()
        jumlah = hitung.get(nim, (nama, 0))[1]
        hitung[nim] = (nama, jumlah + 1)
    return hitung


def menu_statistik():
    judul("STATISTIK PEMINJAMAN")
    if not DAFTAR_TRANSAKSI:
        print("\n  Belum ada transaksi, statistik belum tersedia.")
        return

    stat_alat = _statistik_alat()
    urut_alat = sorted(stat_alat.items(), key=lambda kv: (-kv[1], kv[0]))
    print("\n--- Alat Paling Sering Dipinjam ---")
    for nama, jumlah in urut_alat[:5]:
        print(f"  {jumlah:>3} unit  - {nama}")
    if urut_alat:
        print(f"  -> Paling sering: {urut_alat[0][0]} "
              f"({urut_alat[0][1]} unit)")

    stat_mhs = _statistik_mahasiswa()
    urut_mhs = sorted(stat_mhs.items(),
                      key=lambda kv: (-kv[1][1], kv[0]))
    print("\n--- Mahasiswa Paling Sering Meminjam ---")
    for nim, (nama, jumlah) in urut_mhs[:5]:
        print(f"  {jumlah:>3} transaksi - {nim} {nama}")
    if urut_mhs:
        nim_top, (nama_top, jml_top) = urut_mhs[0]
        print(f"  -> Paling sering: {nama_top} ({nim_top}, {jml_top} "
              f"transaksi)")

    selesai = sum(1 for t in DAFTAR_TRANSAKSI if not t.aktif)
    aktif = len(DAFTAR_TRANSAKSI) - selesai
    print("\n--- Ringkasan Transaksi ---")
    print(f"  Jumlah transaksi selesai : {selesai}")
    print(f"  Jumlah transaksi aktif   : {aktif}")
    print(f"  Total transaksi          : {len(DAFTAR_TRANSAKSI)}")


def tampilkan_menu_utama():
    judul("SISTEM PEMINJAMAN ALAT LABORATORIUM")
    print("1. Status Mahasiswa")
    print("2. Data Alat")
    print("3. Transaksi")
    print("4. Riwayat Pinjaman")
    print("5. Hapus Data")
    print("6. Log Aktivitas")
    print("7. Statistik Peminjaman")
    print("0. Keluar Program")


def main():
    siapkan_data()
    while True:
        tampilkan_menu_utama()
        pilihan = baca_int("\nPilih menu: ", minimum=0, maksimum=7,
                           wajib=False)

        if pilihan in (None, 0):
            print("\nTerima kasih. Program selesai. Sampai jumpa!")
            break
        elif pilihan == 1:
            menu_status_mahasiswa()
            jeda()
        elif pilihan == 2:
            menu_alat()
        elif pilihan == 3:
            menu_transaksi()
        elif pilihan == 4:
            menu_riwayat_pinjaman()
            jeda()
        elif pilihan == 5:
            menu_hapus_data()
        elif pilihan == 6:
            menu_log()
        elif pilihan == 7:
            menu_statistik()
            jeda()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram dihentikan. Terima kasih!")
