from __future__ import annotations

import math
import re

from .konfigurasi import NILAI_MAX, NILAI_MIN

# Format NIM Amikom, contoh: 23.11.5001
POLA_NIM = re.compile(r"^\d{2}\.\d{2}\.\d{4}$")
POLA_KELAS = re.compile(r"^[A-Z0-9-]{2,10}$")


def validasi_nim(nim) -> str:
    if not isinstance(nim, str) or not POLA_NIM.match(nim.strip()):
        raise ValueError(f"NIM tidak valid: {nim!r} (format yang benar: 23.11.5001)")
    return nim.strip()


def validasi_nama(nama) -> str:
    if not isinstance(nama, str):
        raise ValueError(f"Nama harus berupa teks, diterima: {nama!r}")
    bersih = " ".join(nama.split())
    if not bersih:
        raise ValueError("Nama tidak boleh kosong.")
    if not all(c.isalpha() or c in " .'-" for c in bersih):
        raise ValueError(f"Nama mengandung karakter tidak valid: {nama!r}")
    return bersih.title()


def validasi_kelas(kelas) -> str:
    if not isinstance(kelas, str):
        raise ValueError(f"Kelas harus berupa teks, diterima: {kelas!r}")
    bersih = kelas.strip().upper()
    if not POLA_KELAS.match(bersih):
        raise ValueError(f"Kelas tidak valid: {kelas!r} (contoh: TK-01)")
    return bersih


def validasi_nilai(nilai, label: str = "Nilai"):
    if nilai is None:
        return None
    if isinstance(nilai, bool):
        raise ValueError(f"{label} harus berupa angka, diterima: {nilai!r}")
    if isinstance(nilai, str):
        teks = nilai.strip().replace(",", ".")
        if teks == "":
            return None
        try:
            angka = float(teks)
        except ValueError:
            raise ValueError(f"{label} harus berupa angka, diterima: {nilai!r}") from None
    elif isinstance(nilai, (int, float)):
        angka = float(nilai)
    else:
        raise ValueError(f"{label} harus berupa angka, diterima: {nilai!r}")

    if not math.isfinite(angka):
        raise ValueError(f"{label} tidak valid: {nilai!r}")
    if angka < NILAI_MIN or angka > NILAI_MAX:
        raise ValueError(f"{label} harus di antara {NILAI_MIN:g}-{NILAI_MAX:g}, diterima: {angka:g}")
    return angka


def validasi_record(record) -> dict:
    if not isinstance(record, dict):
        raise ValueError("Record harus berupa objek/dictionary.")
    kunci_hilang = [k for k in ("nim", "nama", "kelas") if k not in record]
    if kunci_hilang:
        raise ValueError(f"Kunci wajib hilang: {', '.join(kunci_hilang)}")
    return {
        "nim": validasi_nim(record["nim"]),
        "nama": validasi_nama(record["nama"]),
        "kelas": validasi_kelas(record["kelas"]),
        "tugas": validasi_nilai(record.get("tugas"), "Nilai tugas"),
        "uts": validasi_nilai(record.get("uts"), "Nilai UTS"),
        "uas": validasi_nilai(record.get("uas"), "Nilai UAS"),
    }
