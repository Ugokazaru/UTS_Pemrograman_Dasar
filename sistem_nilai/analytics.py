"""Perhitungan nilai akhir, penentuan grade, ranking, dan rekapitulasi statistik."""
from __future__ import annotations

import statistics

from .konfigurasi import BATAS_GRADE, BATAS_LULUS, BOBOT, GRADE_TERENDAH, GRADE_URUT


def hitung_nilai_akhir(tugas, uts, uas):
    if tugas is None or uts is None or uas is None:
        return None
    total = tugas * BOBOT["tugas"] + uts * BOBOT["uts"] + uas * BOBOT["uas"]
    return round(total, 2)


def tentukan_grade(nilai_akhir) -> str:
    if nilai_akhir is None:
        return "-"
    for batas, grade in BATAS_GRADE:
        if nilai_akhir >= batas:
            return grade
    return GRADE_TERENDAH


def _dengan_hasil(mahasiswa: dict) -> dict:
    akhir = hitung_nilai_akhir(mahasiswa["tugas"], mahasiswa["uts"], mahasiswa["uas"])
    return {**mahasiswa, "nilai_akhir": akhir, "grade": tentukan_grade(akhir)}


def lengkapi_hasil(daftar: list[dict]) -> list[dict]:
    return [_dengan_hasil(m) for m in daftar]


def ranking(daftar_hasil: list[dict], n: int = 5) -> list[dict]:
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Jumlah ranking harus bilangan bulat positif.")
    dinilai = [m for m in daftar_hasil if m["nilai_akhir"] is not None]
    return sorted(dinilai, key=lambda m: m["nilai_akhir"], reverse=True)[:n]


def rekap_statistik(daftar_hasil: list[dict]) -> dict:
    nilai = [m["nilai_akhir"] for m in daftar_hasil if m["nilai_akhir"] is not None]
    rekap = {
        "total_mahasiswa": len(daftar_hasil),
        "sudah_dinilai": len(nilai),
        "belum_lengkap": len(daftar_hasil) - len(nilai),
        "rata_rata": None,
        "median": None,
        "tertinggi": None,
        "terendah": None,
        "jumlah_lulus": 0,
        "persen_lulus": None,
        "distribusi_grade": {g: 0 for g in GRADE_URUT},
        "rata_per_kelas": {},
    }
    if not nilai:
        return rekap

    for m in daftar_hasil:
        if m["grade"] in rekap["distribusi_grade"]:
            rekap["distribusi_grade"][m["grade"]] += 1

    per_kelas: dict[str, list[float]] = {}  # dict: kelompokkan nilai berdasarkan kelas
    for m in daftar_hasil:
        if m["nilai_akhir"] is not None:
            per_kelas.setdefault(m["kelas"], []).append(m["nilai_akhir"])

    lulus = sum(1 for n in nilai if n >= BATAS_LULUS)
    rekap.update(
        rata_rata=round(statistics.mean(nilai), 2),
        median=round(statistics.median(nilai), 2),
        tertinggi=max(nilai),
        terendah=min(nilai),
        jumlah_lulus=lulus,
        persen_lulus=round(lulus / len(nilai) * 100, 1),
        rata_per_kelas={k: round(statistics.mean(v), 2) for k, v in sorted(per_kelas.items())},  # dict comprehension
    )
    return rekap
