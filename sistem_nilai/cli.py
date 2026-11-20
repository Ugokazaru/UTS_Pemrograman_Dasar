from __future__ import annotations

from . import analytics, operations, tampilan
from .konfigurasi import PEMBUAT
from .io_handler import DataFileError, muat_mahasiswa, simpan_csv, simpan_json
from .validator import validasi_kelas, validasi_nama, validasi_nilai, validasi_nim, validasi_record

MENU = """
=== SISTEM PENGELOLAAN NILAI MAHASISWA ===
 1. Tampilkan semua data
 2. Tambah mahasiswa
 3. Hapus mahasiswa (berdasarkan NIM)
 4. Cari mahasiswa (nama)
 5. Filter (kelas / nilai minimal)
 6. Rekapitulasi statistik
 7. Ranking nilai tertinggi
 8. Hapus data duplikat
 9. Simpan hasil (JSON & CSV)
 0. Keluar
"""



def minta_input(pesan: str, validator, **kwargs):
     while True:
        try:
            return validator(input(pesan), **kwargs)
        except ValueError as e:
            print(f"  [!] {e} Silakan coba lagi.")


def aksi_tampilkan(data: list[dict]) -> None:
    print(tampilan.format_tabel(analytics.lengkapi_hasil(data)))


def aksi_tambah(data: list[dict]) -> list[dict]:
    print("Tambah mahasiswa (nilai boleh dikosongkan dengan menekan Enter).")
    mahasiswa = validasi_record({
        "nim": minta_input("NIM (contoh 23.11.5001): ", validasi_nim),
        "nama": minta_input("Nama: ", validasi_nama),
        "kelas": minta_input("Kelas (contoh TK-01): ", validasi_kelas),
        "tugas": minta_input("Nilai tugas (0-100): ", validasi_nilai, label="Nilai tugas"),
        "uts": minta_input("Nilai UTS (0-100): ", validasi_nilai, label="Nilai UTS"),
        "uas": minta_input("Nilai UAS (0-100): ", validasi_nilai, label="Nilai UAS"),
    })
    try:
        data = operations.tambah_mahasiswa(data, mahasiswa)
        print(f"Berhasil menambahkan {mahasiswa['nama']}.")
    except ValueError as e:
        print(f"  [!] {e}")
    return data


def aksi_hapus(data: list[dict]) -> list[dict]:
    nim = minta_input("NIM yang dihapus: ", validasi_nim)
    if input(f"Yakin hapus {nim}? (y/n): ").strip().lower() != "y":
        print("Dibatalkan.")
        return data
    data, terhapus = operations.hapus_mahasiswa(data, nim)
    print("Data dihapus." if terhapus else f"NIM {nim} tidak ditemukan.")
    return data


def aksi_cari(data: list[dict]) -> None:
    try:
        hasil = operations.cari_nama(data, input("Kata kunci nama: "))
    except ValueError as e:
        print(f"  [!] {e}")
        return
    print(tampilan.format_tabel(analytics.lengkapi_hasil(hasil)))


def aksi_filter(data: list[dict]) -> None:
    pilihan = input("Filter berdasarkan [1] Kelas  [2] Nilai minimal: ").strip()
    try:
        if pilihan == "1":
            print(f"Kelas tersedia: {', '.join(operations.daftar_kelas(data)) or '-'}")
            hasil = operations.filter_kelas(data, input("Kode kelas: "))
            print(tampilan.format_tabel(analytics.lengkapi_hasil(hasil)))
        elif pilihan == "2":
            hasil = operations.filter_nilai_minimal(
                analytics.lengkapi_hasil(data), input("Nilai akhir minimal: ")
            )
            print(tampilan.format_tabel(hasil))
        else:
            print("  [!] Pilihan filter tidak dikenal.")
    except ValueError as e:
        print(f"  [!] {e}")


def aksi_rekap(data: list[dict]) -> None:
    print(tampilan.format_rekap(analytics.rekap_statistik(analytics.lengkapi_hasil(data))))


def aksi_ranking(data: list[dict]) -> None:
    teks = input("Tampilkan berapa teratas? [5]: ").strip() or "5"
    try:
        hasil = analytics.ranking(analytics.lengkapi_hasil(data), int(teks))
    except ValueError:
        print("  [!] Masukkan bilangan bulat positif.")
        return
    print(tampilan.format_tabel(hasil))


def aksi_duplikat(data: list[dict]) -> list[dict]:
    data, jumlah = operations.hapus_duplikat(data)
    print(f"{jumlah} data duplikat dihapus." if jumlah else "Tidak ada data duplikat.")
    return data


def aksi_simpan(data: list[dict], path_json: str, path_csv: str) -> None:
    hasil = analytics.lengkapi_hasil(data)
    try:
        simpan_json(path_json, hasil, analytics.rekap_statistik(hasil))
        simpan_csv(path_csv, hasil)
        print(f"Tersimpan: {path_json} dan {path_csv}")
    except DataFileError as e:
        print(f"  [!] {e}")


def muat_awal(path_input: str) -> list[dict]:
    try:
        data, galat = muat_mahasiswa(path_input)
    except DataFileError as e:
        print(f"[PERINGATAN] {e}\nAplikasi dimulai dengan data kosong.")
        return []
    for pesan in galat:
        print(f"[PERINGATAN] {pesan}")
    print(f"{len(data)} record berhasil dimuat dari {path_input}.")
    return data


def jalankan_menu(path_input: str, path_json: str, path_csv: str) -> None:
    data = muat_awal(path_input)
    while True:
        print(MENU)
        print(f"Dibuat oleh: {PEMBUAT}")
        try:
            pilihan = input("Pilih menu [0-9]: ").strip()
            if pilihan == "1":
                aksi_tampilkan(data)
            elif pilihan == "2":
                data = aksi_tambah(data)
            elif pilihan == "3":
                data = aksi_hapus(data)
            elif pilihan == "4":
                aksi_cari(data)
            elif pilihan == "5":
                aksi_filter(data)
            elif pilihan == "6":
                aksi_rekap(data)
            elif pilihan == "7":
                aksi_ranking(data)
            elif pilihan == "8":
                data = aksi_duplikat(data)
            elif pilihan == "9":
                aksi_simpan(data, path_json, path_csv)
            elif pilihan == "0":
                print("Terima kasih. Sampai jumpa!")
                break
            else:
                print("  [!] Menu tidak dikenal, pilih angka 0-9.")
        except (EOFError, KeyboardInterrupt):
            print("\nInput dihentikan. Keluar dari aplikasi.")
            break


def jalankan_batch(path_input: str, path_json: str, path_csv: str) -> int:
    try:
        data, galat = muat_mahasiswa(path_input)
        for pesan in galat:
            print(f"[PERINGATAN] {pesan}")
        data, duplikat = operations.hapus_duplikat(data)
        hasil = analytics.lengkapi_hasil(data)
        rekap = analytics.rekap_statistik(hasil)
        simpan_json(path_json, hasil, rekap)
        simpan_csv(path_csv, hasil)
    except DataFileError as e:
        print(f"[GALAT] {e}")
        return 1
    print(f"Record valid: {len(data)} | ditolak: {len(galat)} | duplikat dibuang: {duplikat}")
    print(tampilan.format_rekap(rekap))
    print(f"Output disimpan ke {path_json} dan {path_csv}")
    return 0
