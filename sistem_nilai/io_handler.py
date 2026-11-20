"""Pembacaan dan penyimpanan file JSON/CSV dengan exception handling."""
from __future__ import annotations

import csv
import json
import os
from datetime import datetime

from .validator import validasi_record


class DataFileError(Exception):
    """Galat terkait file data (tidak ada, rusak, tak bisa ditulis, dsb.)."""


def baca_json(path: str) -> list:
    """Baca file JSON dan kembalikan list record mentah.

    File boleh berupa list langsung, atau objek dengan kunci 'mahasiswa'
    (format file output aplikasi ini), sehingga output bisa dipakai lagi sebagai input.

    Raises:
        DataFileError: file tidak ada, tidak bisa dibaca, JSON rusak, atau struktur salah.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            isi = json.load(f)
    except FileNotFoundError:
        raise DataFileError(f"File tidak ditemukan: {path}") from None
    except json.JSONDecodeError as e:
        raise DataFileError(
            f"Format JSON rusak di {path} (baris {e.lineno}, kolom {e.colno}): {e.msg}"
        ) from e
    except UnicodeDecodeError:
        raise DataFileError(f"Encoding file bukan UTF-8: {path}") from None
    except OSError as e:
        raise DataFileError(f"Tidak dapat membaca {path}: {e.strerror}") from e

    if isinstance(isi, dict) and "mahasiswa" in isi:
        isi = isi["mahasiswa"]
    if not isinstance(isi, list):
        raise DataFileError("Struktur JSON harus berupa list data mahasiswa.")
    return isi


def muat_mahasiswa(path: str) -> tuple[list[dict], list[str]]:
    """Baca file lalu validasi tiap record; record rusak dilewati, tidak menggagalkan semua.

    Returns:
        tuple: (list record valid, list pesan galat per record yang ditolak).
    Raises:
        DataFileError: jika file itu sendiri tidak dapat dibaca.
    """
    valid: list[dict] = []
    galat: list[str] = []
    for nomor, record in enumerate(baca_json(path), start=1):
        try:
            valid.append(validasi_record(record))
        except ValueError as e:
            galat.append(f"Record #{nomor} ditolak: {e}")
    return valid, galat


def _siapkan_folder(path: str) -> None:
    """Buat folder tujuan bila belum ada."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)


def simpan_json(path: str, daftar_hasil: list[dict], rekap: dict) -> None:
    """Simpan data + rekap ke JSON.

    Raises:
        DataFileError: jika file tidak dapat ditulis.
    """
    isi = {
        "dibuat_pada": datetime.now().isoformat(timespec="seconds"),
        "rekap": rekap,
        "mahasiswa": daftar_hasil,
    }
    try:
        _siapkan_folder(path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(isi, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise DataFileError(f"Gagal menyimpan {path}: {e.strerror}") from e


def simpan_csv(path: str, daftar_hasil: list[dict]) -> None:
    """Simpan data hasil ke CSV (kolom berurutan, nilai kosong jadi sel kosong).

    Raises:
        DataFileError: jika file tidak dapat ditulis.
    """
    kolom = ["nim", "nama", "kelas", "tugas", "uts", "uas", "nilai_akhir", "grade"]
    try:
        _siapkan_folder(path)
        with open(path, "w", encoding="utf-8", newline="") as f:
            penulis = csv.DictWriter(f, fieldnames=kolom, extrasaction="ignore")
            penulis.writeheader()
            for m in daftar_hasil:
                penulis.writerow({k: ("" if m.get(k) is None else m[k]) for k in kolom})
    except OSError as e:
        raise DataFileError(f"Gagal menyimpan {path}: {e.strerror}") from e
