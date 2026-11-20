# LEMBAR JAWABAN UTS PEMROGRAMAN DASAR (TK091)

**Universitas Amikom Yogyakarta – S1 Teknik Komputer – Semester Ganjil TA 2026/2027**
Dosen Pengampu: Muhammad Koprawi, S.Kom., M.Eng
Nama: William Putra Pamungkas  
NIM: 25.83.1193  
Kelas: TK01  
Link Repository: https://github.com/Ugokazaru/UTS_Pemrograman_Dasar.git

---

## Soal 1 – Analisis Masalah dan Rancangan Aplikasi

**Masalah.** Dosen dan staf prodi sering merekap nilai mahasiswa secara manual di spreadsheet. Hal ini rawan salah hitung, NIM ganda, nilai kosong yang terhitung 0, dan sulit membuat rekap per kelas dengan cepat.

**Tujuan.** Membangun aplikasi CLI Python untuk menyimpan, memvalidasi, mencari, dan merekap nilai mahasiswa secara konsisten, serta menghasilkan file keluaran JSON/CSV.

**Target pengguna.** Dosen pengampu, asisten dosen, dan staf administrasi prodi yang nyaman menggunakan terminal.

**Format input.** File `data_input.json` berisi list objek dengan field `nim`, `nama`, `kelas`, `tugas`, `uts`, `uas` (nilai boleh `null`). Selain itu ada input interaktif dari keyboard melalui menu.

**Format output.** (1) Tabel teks dan rekap di terminal; (2) `data_output.json` berisi `rekap` dan `mahasiswa` lengkap dengan `nilai_akhir` dan `grade`; (3) `data_output.csv`.

**Fitur utama.**
1. **Tambah & hapus data** – validasi NIM/nama/kelas/nilai, cegah NIM ganda, konfirmasi sebelum hapus.
2. **Pencarian & filtering** – cari nama, filter kelas, filter nilai akhir minimal, ranking.
3. **Rekapitulasi statistik** – rata-rata, median, tertinggi/terendah, persentase lulus, distribusi grade, rata-rata per kelas.
4. **Hapus data duplikat** dan **simpan hasil** ke JSON & CSV.

---

## Soal 2 – Struktur Data

| Struktur | Dipakai untuk | Alasan pemilihan |
|---|---|---|
| `list` | Kumpulan seluruh mahasiswa (list of dict); daftar hasil filter; ranking | Menjaga urutan data, mudah diiterasi, di-*sort*, dan di-*slice*; cocok untuk koleksi yang bertambah/berkurang |
| `dict` | Satu record mahasiswa; bobot nilai; distribusi grade; pengelompokan nilai per kelas; indeks `{nim: record}` | Data bernama (key-value) lebih terbaca dari indeks angka, langsung sesuai format JSON, dan lookup cepat |
| `set` | Himpunan NIM terdaftar; deteksi duplikat; daftar kelas unik | Anggota otomatis unik dan pengecekan keanggotaan O(1) sehingga efisien untuk validasi duplikat |

**Fitur pemrosesan yang diimplementasikan:** pencarian (`cari_nama`), filtering (`filter_kelas`, `filter_nilai_minimal`), pengelompokan (rata-rata per kelas), rekapitulasi (`rekap_statistik`), dan penghapusan data duplikat (`hapus_duplikat`).

---

## Soal 3 – Control Flow dan Pythonic Programming

- **Percabangan:** `if/elif/else` pada menu utama (`cli.jalankan_menu`), penentuan grade, dan validasi.
- **Perulangan:** `while True` pada loop menu dan `minta_input`; `for` pada `hapus_duplikat`, `rekap_statistik`, dan `format_tabel`.
- **Comprehension:**
  - list comprehension: `hapus_mahasiswa`, `cari_nama`, `lengkapi_hasil`
  - set comprehension: `nim_terdaftar`, `daftar_kelas`
  - dict comprehension: `rata_per_kelas` pada `rekap_statistik`, `distribusi_grade`
- **Edge case yang ditangani:**
  1. Nilai kosong (`null`/Enter) → nilai akhir `None`, grade `-`, tidak dihitung dalam statistik (tidak dianggap 0).
  2. Data kosong → `rekap_statistik` tidak crash dan menampilkan pesan.
  3. Nilai negatif / >100 / bukan angka → ditolak dan diminta ulang.
  4. NIM ganda → ditolak saat tambah, dibuang saat hapus duplikat.

**Contoh hasil (data normal, `python main.py --batch`):**
12 record valid, 1 ditolak (UTS = 150), 1 duplikat dibuang; rata-rata 72.68, median 73.05, tertinggi 98, terendah 40.5, lulus 8 (80%), distribusi grade A=3, B=2, C=3, D=1, E=1. _(sertakan screenshot terminal)_

---

## Soal 4 – Function, Module, dan Package

Program dipecah menjadi package buatan sendiri `sistem_nilai` dengan prinsip **single responsibility**: satu fungsi mengerjakan satu tugas, dan setiap modul menangani satu area. Setiap fungsi memiliki docstring (Args/Returns/Raises) di kode sumber.

**a. `validator.py` – validasi dan normalisasi input**

| Fungsi | Parameter | Return | Tanggung jawab |
|---|---|---|---|
| `validasi_nim` | `nim` | `str` | Memastikan format NIM `YY.JJ.NNNN`; `ValueError` jika salah |
| `validasi_nama` | `nama` | `str` | Memastikan nama tidak kosong dan tanpa angka; merapikan huruf kapital |
| `validasi_kelas` | `kelas` | `str` | Memastikan format kelas (mis. `TK01`) dan mengubahnya ke huruf besar |
| `validasi_nilai` | `nilai`, `label="Nilai"` | `float` atau `None` | Memastikan nilai 0-100; kosong menjadi `None` (edge case) |
| `validasi_record` | `record` | `dict` | Memvalidasi satu mahasiswa lengkap dan mengembalikan dict bersih |

**b. `operations.py` – manipulasi data (tidak mengubah list asli)**

| Fungsi | Parameter | Return | Tanggung jawab |
|---|---|---|---|
| `nim_terdaftar` | `daftar` | `set[str]` | Himpunan NIM yang sudah ada |
| `buat_indeks` | `daftar` | `dict` | Indeks `{nim: record}` untuk lookup cepat |
| `daftar_kelas` | `daftar` | `list[str]` | Daftar kelas unik terurut |
| `tambah_mahasiswa` | `daftar`, `mahasiswa` | `list` | Menambah data; `ValueError` jika NIM ganda |
| `hapus_mahasiswa` | `daftar`, `nim` | `tuple(list, bool)` | Menghapus berdasarkan NIM; bool menandai ada tidaknya data terhapus |
| `cari_nama` | `daftar`, `kata_kunci` | `list` | Pencarian nama (tidak peka huruf besar/kecil) |
| `filter_kelas` | `daftar`, `kelas` | `list` | Memfilter mahasiswa pada satu kelas |
| `filter_nilai_minimal` | `daftar_hasil`, `batas` | `list` | Memfilter berdasarkan nilai akhir minimal |
| `hapus_duplikat` | `daftar` | `tuple(list, int)` | Membuang NIM ganda; int = jumlah yang dibuang |

**c. `analytics.py` – perhitungan murni**

| Fungsi | Parameter | Return | Tanggung jawab |
|---|---|---|---|
| `hitung_nilai_akhir` | `tugas`, `uts`, `uas` | `float` atau `None` | Nilai akhir berbobot 30/30/40; `None` jika ada komponen kosong |
| `tentukan_grade` | `nilai_akhir` | `str` | Konversi nilai ke grade A-E (`-` jika `None`) |
| `lengkapi_hasil` | `daftar` | `list` | Menambahkan `nilai_akhir` dan `grade` ke tiap mahasiswa |
| `ranking` | `daftar_hasil`, `n=5` | `list` | `n` nilai tertinggi; `ValueError` jika `n` tidak valid |
| `rekap_statistik` | `daftar_hasil` | `dict` | Rata-rata, median, min/max, persen lulus, distribusi grade, rata-rata per kelas |

**d. `io_handler.py` – akses file**

| Fungsi | Parameter | Return | Tanggung jawab |
|---|---|---|---|
| `baca_json` | `path` | `list` | Membaca JSON mentah; galat dibungkus `DataFileError` |
| `muat_mahasiswa` | `path` | `tuple(list, list[str])` | Membaca + memvalidasi; record rusak dilewati dan dilaporkan |
| `simpan_json` | `path`, `daftar_hasil`, `rekap` | `None` | Menyimpan data dan rekap ke JSON |
| `simpan_csv` | `path`, `daftar_hasil` | `None` | Menyimpan data ke CSV |

**e. `tampilan.py` dan `cli.py` / `main.py` – antarmuka**

| Fungsi | Parameter | Return | Tanggung jawab |
|---|---|---|---|
| `format_tabel` | `daftar_hasil` | `str` | Membentuk tabel teks |
| `format_rekap` | `rekap` | `str` | Membentuk teks rekap statistik |
| `minta_input` | `pesan`, `validator`, `**kwargs` | hasil validator | Meminta input berulang sampai valid |
| `aksi_tambah` / `aksi_hapus` / `aksi_duplikat` | `data` | `list` | Menjalankan satu menu dan mengembalikan data terbaru |
| `aksi_simpan` | `data`, `path_json`, `path_csv` | `None` | Menyimpan hasil ke JSON dan CSV |
| `muat_awal` | `path_input` | `list` | Memuat data awal; gagal menjadi data kosong + peringatan |
| `jalankan_menu` | `path_input`, `path_json`, `path_csv` | `None` | Loop menu interaktif |
| `jalankan_batch` | `path_input`, `path_json`, `path_csv` | `int` | Mode otomatis; 0 sukses, 1 gagal |
| `baca_argumen` (main.py) | `argv=None` | `Namespace` | Membaca argumen command line |
| `main` (main.py) | `argv=None` | `int` | Titik masuk; mengembalikan exit code |

**Alur dependensi antar-module:**
```
main.py → cli → io_handler → validator → konfigurasi
               → operations → validator
               → analytics  → konfigurasi
               → tampilan
               → validator
```
Alur pemanggilan mode batch: `main.main()` → `cli.jalankan_batch()` → `io_handler.muat_mahasiswa()` → `operations.hapus_duplikat()` → `analytics.lengkapi_hasil()` → `analytics.rekap_statistik()` → `io_handler.simpan_json()` / `simpan_csv()`.
Dependensi searah (tanpa siklus): lapisan atas (`cli`) memanggil lapisan bawah, dan modul bawah tidak mengetahui modul di atasnya.

---

## Soal 5 – Pemrosesan File CSV/JSON

- **Baca:** `io_handler.baca_json` membaca `data/data_input.json` (UTF-8); format list langsung atau objek `{"mahasiswa": [...]}`.
- **Transformasi/analisis:** validasi → normalisasi (nama jadi huruf kapital awal kata, kelas huruf besar, koma desimal diterima) → hapus duplikat → hitung nilai akhir & grade → rekap statistik.
- **Simpan:** `data/data_output.json` (rekap + data) dan `data/data_output.csv`.
- **Contoh file uji:** `data_input.json` (sengaja memuat 1 duplikat, 2 nilai tidak lengkap, 1 record tidak valid), `data_output.json`, `data_output.csv`, `data_rusak.json`, `data_kosong.json`.

---

## Soal 6 – Exception Handling, Debugging, dan Dokumentasi

**Exception handling & defensive programming**

| Kondisi | Penanganan |
|---|---|
| File tidak ditemukan | `FileNotFoundError` → `DataFileError("File tidak ditemukan: ...")`; batch exit code 1; menu mulai dengan data kosong |
| JSON rusak | `json.JSONDecodeError` → pesan berisi baris & kolom |
| Encoding / izin file | `UnicodeDecodeError`, `OSError` ditangkap |
| Record tidak valid | Dilewati, dilaporkan per nomor record, record lain tetap diproses |
| Input CLI salah (NIM, nama, nilai) | `ValueError` ditangkap di `minta_input`, pengguna diminta mengulang |
| Menu tidak dikenal / ranking non-angka | Pesan peringatan, program tetap berjalan |
| `Ctrl+C` / EOF | Keluar dengan rapi |
| Gagal menulis output | `OSError` → `DataFileError`, ditampilkan tanpa crash |

**Skenario debugging: rekap pada data kosong**
1. *Gejala:* menjalankan `python main.py --input data/data_kosong.json --batch` ketika pengecekan `if not nilai:` belum ada pada `rekap_statistik` menghasilkan traceback `statistics.StatisticsError: mean requires at least one data point`.
2. *Pelacakan:* membaca traceback dari baris paling bawah ke atas → error muncul di `statistics.mean(nilai)` pada `analytics.rekap_statistik`; dicetak `print(len(nilai))` → hasilnya `0`, sehingga list kosong menjadi penyebab.
3. *Perbaikan:* menambahkan *guard clause* `if not nilai: return rekap` dan nilai statistik default `None`; `tampilan.format_rekap` menampilkan pesan yang informatif.
4. *Verifikasi:* unit test `test_rekap_data_kosong_tidak_error` dan menjalankan ulang perintah di atas (exit code 0).

**Dokumentasi:** `README.md` memuat struktur program, cara menjalankan, serta package dan dependency (hanya standard library).

---

## Catatan Referensi, Library, dan Penggunaan AI

**Library (semua standard library Python 3.9+):** `json`, `csv`, `re`, `math`, `statistics`, `argparse`, `os`, `pathlib`, `datetime`, `unittest`, `tempfile`. Tidak ada library pihak ketiga.

**Referensi:**
- Dokumentasi resmi Python: https://docs.python.org/3/ (modul `json`, `csv`, `statistics`, `argparse`, `unittest`)
- PEP 8 – Style Guide for Python Code, PEP 257 – Docstring Conventions

**Penggunaan AI:** Penggunaan AI: Dengan bantuan Claude saya membuat file README, mengecek apakah struktur package sudah benar & rapi atau belum, dan menguji edge case.