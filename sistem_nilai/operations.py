from __future__ import annotations

from .validator import validasi_kelas, validasi_nilai


def nim_terdaftar(daftar: list[dict]) -> set[str]:
    return {m["nim"] for m in daftar}


def buat_indeks(daftar: list[dict]) -> dict[str, dict]:
    return {m["nim"]: m for m in daftar}


def daftar_kelas(daftar: list[dict]) -> list[str]:
    return sorted({m["kelas"] for m in daftar})


def tambah_mahasiswa(daftar: list[dict], mahasiswa: dict) -> list[dict]:
    if mahasiswa["nim"] in nim_terdaftar(daftar):
        raise ValueError(f"NIM {mahasiswa['nim']} sudah terdaftar.")
    return daftar + [mahasiswa]


def hapus_mahasiswa(daftar: list[dict], nim: str) -> tuple[list[dict], bool]:
    baru = [m for m in daftar if m["nim"] != nim.strip()]  # list comprehension
    return baru, len(baru) != len(daftar)


def cari_nama(daftar: list[dict], kata_kunci: str) -> list[dict]:
    kata = kata_kunci.strip().lower()
    if not kata:
        raise ValueError("Kata kunci pencarian tidak boleh kosong.")
    return [m for m in daftar if kata in m["nama"].lower()]


def filter_kelas(daftar: list[dict], kelas: str) -> list[dict]:
    kode = validasi_kelas(kelas)
    return [m for m in daftar if m["kelas"] == kode]


def filter_nilai_minimal(daftar_hasil: list[dict], batas) -> list[dict]:
    ambang = validasi_nilai(batas, "Batas nilai")
    if ambang is None:
        raise ValueError("Batas nilai tidak boleh kosong.")
    return [
        m for m in daftar_hasil
        if m["nilai_akhir"] is not None and m["nilai_akhir"] >= ambang
    ]


def hapus_duplikat(daftar: list[dict]) -> tuple[list[dict], int]:
    terlihat: set[str] = set()  # set: cek "sudah pernah muncul?" dalam O(1)
    unik: list[dict] = []
    for m in daftar:
        if m["nim"] not in terlihat:
            terlihat.add(m["nim"])
            unik.append(m)
    return unik, len(daftar) - len(unik)
