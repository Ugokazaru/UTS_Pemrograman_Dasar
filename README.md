# Sistem Pengelolaan Data Nilai Mahasiswa (CLI)

Proyek UTS **TK091 – Pemrograman Dasar** (S1 Teknik Komputer, Universitas Amikom Yogyakarta, TA 2026/2027).
Aplikasi command line berbasis Python yang mengelola data nilai mahasiswa: membaca JSON, mengolah, dan menyimpan ke JSON/CSV.

- **Nama**: William Putra Pamungkas
- **NIM**: 25.83.1193
- **Kelas**: TK01
- **Link repository**: https://github.com/Ugokazaru/UTS_Pemrograman_Dasar.git

## Persyaratan
- Python **3.9+**
- **Hanya standard library** (`json`, `csv`, `re`, `statistics`, `argparse`, `unittest`, dll). Tidak ada `pip install`.

## Cara Menjalankan

```bash
# 1. masuk ke folder proyek
cd uts_nilai_mahasiswa

# 2. menu interaktif
python main.py            

# 3. mode batch: baca -> hapus duplikat -> analisis -> simpan output
python main.py --batch

# 4. pakai file lain
python main.py --input data/data_input.json --output hasil/out.json --csv hasil/out.csv --batch

# 5. jalankan unit test
python -m unittest discover -v
```

Skenario uji error:
```bash
python main.py --input tidak_ada.json --batch        # file tidak ditemukan
python main.py --input data/data_rusak.json --batch  # JSON rusak
python main.py --input data/data_kosong.json --batch # edge case: data kosong
```

## Struktur Proyek

```
uts_nilai_mahasiswa/
├── main.py                  # titik masuk + parsing argumen CLI
├── README.md
├── LAPORAN.md               # draf laporan (export ke PDF)
├── data/
│   ├── data_input.json      # contoh input (termasuk duplikat, nilai kosong, data tidak valid)
│   ├── data_output.json     # hasil run: data + nilai akhir + grade + rekap
│   ├── data_output.csv      # hasil run dalam CSV
│   ├── data_rusak.json      # contoh file JSON rusak (uji error)
│   └── data_kosong.json     # contoh data kosong (uji edge case)
├── sistem_nilai/            # package buatan sendiri
│   ├── __init__.py
│   ├── konfigurasi.py       # konstanta: bobot, batas grade, batas lulus
│   ├── validator.py         # validasi & normalisasi input
│   ├── operations.py        # tambah, hapus, cari, filter, hapus duplikat
│   ├── analytics.py         # nilai akhir, grade, ranking, rekap statistik
│   ├── io_handler.py        # baca/tulis JSON & CSV + exception
│   ├── tampilan.py          # format tabel/rekap (tanpa I/O)
│   └── cli.py               # menu interaktif & mode batch
└── tests/
    └── test_sistem_nilai.py # 14 unit test
```

## Format Data

**Input** (`data_input.json`) – list objek:
```json
{"nim": "23.11.5001", "nama": "Andi Pratama", "kelas": "TK-01", "tugas": 88, "uts": 82, "uas": 90}
```
`tugas`, `uts`, `uas` boleh `null`/dihilangkan (nilai belum ada). Nilai akhir = **30% tugas + 30% UTS + 40% UAS**.

**Output** (`data_output.json`): objek `{dibuat_pada, rekap, mahasiswa[]}`; `mahasiswa[]` memuat `nilai_akhir` & `grade`. File output ini juga bisa dipakai lagi sebagai input.
**Output CSV**: `nim,nama,kelas,tugas,uts,uas,nilai_akhir,grade`.

Grade: A ≥ 85, B ≥ 70, C ≥ 60, D ≥ 50, selain itu E. Lulus jika nilai akhir ≥ 60.

## Menu Aplikasi
1 Tampilkan data · 2 Tambah · 3 Hapus (konfirmasi) · 4 Cari nama · 5 Filter (kelas / nilai minimal) · 6 Rekap statistik · 7 Ranking · 8 Hapus duplikat · 9 Simpan JSON & CSV · 0 Keluar

## Penjelasan Modul & Dependensi

```
main.py ──> cli ──> io_handler ──> validator ──> konfigurasi
              ├───> operations ───> validator
              ├───> analytics ────> konfigurasi
              ├───> tampilan
              └───> validator
```
Tidak ada dependensi melingkar; `konfigurasi` dan `tampilan` tidak mengimpor modul lain di package.

| Modul | Tanggung jawab |
|---|---|
| `validator` | Memeriksa NIM, nama, kelas, nilai; melempar `ValueError` berpesan jelas |
| `operations` | Manipulasi list data (tidak mengubah list asli) |
| `analytics` | Perhitungan murni: nilai akhir, grade, ranking, statistik |
| `io_handler` | Semua akses file; mengubah galat OS/JSON menjadi `DataFileError` |
| `tampilan` | Mengubah data jadi teks tabel |
| `cli` | Interaksi pengguna, loop menu, penanganan input salah |

## Penanganan Error
File tidak ada / JSON rusak / izin ditolak → `DataFileError` (pesan ramah, exit code 1 di mode batch, atau mulai dengan data kosong di mode menu) · record tak valid dilewati dan dilaporkan · input CLI salah diminta ulang · `Ctrl+C`/EOF keluar dengan rapi · data kosong tidak menyebabkan crash.

## Referensi, Library, dan Bantuan AI
Lihat bagian terakhir `LAPORAN.md`.
