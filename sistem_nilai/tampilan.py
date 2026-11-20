from __future__ import annotations


def _fmt(angka) -> str:
    return "-" if angka is None else f"{angka:g}"


def format_tabel(daftar_hasil: list[dict]) -> str:
    if not daftar_hasil:
        return "(Tidak ada data untuk ditampilkan)"
    garis = "-" * 86
    baris = [
        garis,
        f"{'NIM':<11}{'Nama':<28}{'Kelas':<8}{'Tugas':>6}{'UTS':>6}{'UAS':>6}{'Akhir':>8}{'Grade':>7}",
        garis,
    ]
    for m in daftar_hasil:
        baris.append(
            f"{m['nim']:<11}{m['nama'][:27]:<28}{m['kelas']:<8}"
            f"{_fmt(m['tugas']):>6}{_fmt(m['uts']):>6}{_fmt(m['uas']):>6}"
            f"{_fmt(m['nilai_akhir']):>8}{m['grade']:>7}"
        )
    baris.append(garis)
    baris.append(f"Total: {len(daftar_hasil)} mahasiswa")
    return "\n".join(baris)


def format_rekap(rekap: dict) -> str:
    """Bentuk teks rekapitulasi statistik dari dict hasil rekap_statistik()."""
    if rekap["sudah_dinilai"] == 0:
        return (
            f"Total mahasiswa : {rekap['total_mahasiswa']}\n"
            "Belum ada mahasiswa dengan nilai lengkap, statistik tidak dapat dihitung."
        )
    grade = ", ".join(f"{g}={j}" for g, j in rekap["distribusi_grade"].items())
    kelas = "\n".join(f"  - {k}: {v:g}" for k, v in rekap["rata_per_kelas"].items())
    return (
        f"Total mahasiswa   : {rekap['total_mahasiswa']}\n"
        f"Nilai lengkap     : {rekap['sudah_dinilai']} (belum lengkap: {rekap['belum_lengkap']})\n"
        f"Rata-rata         : {rekap['rata_rata']:g}\n"
        f"Median            : {rekap['median']:g}\n"
        f"Tertinggi/Terendah: {rekap['tertinggi']:g} / {rekap['terendah']:g}\n"
        f"Lulus             : {rekap['jumlah_lulus']} ({rekap['persen_lulus']:g}%)\n"
        f"Distribusi grade  : {grade}\n"
        f"Rata-rata per kelas:\n{kelas}"
    )
