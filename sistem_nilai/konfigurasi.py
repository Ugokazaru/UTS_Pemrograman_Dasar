# Rentang nilai yang sah
NILAI_MIN = 0.0
NILAI_MAX = 100.0

# Bobot komponen nilai akhir (total harus 1.0)
BOBOT = {"tugas": 0.3, "uts": 0.3, "uas": 0.4}

# Batas nilai minimal tiap grade, diurutkan dari tertinggi ke terendah.
# List of tuple dipilih karena URUTAN penting saat dicek satu per satu.
BATAS_GRADE = [(85.0, "A"), (70.0, "B"), (60.0, "C"), (50.0, "D")]
GRADE_TERENDAH = "E"
GRADE_URUT = ["A", "B", "C", "D", "E"]

# Mahasiswa dinyatakan lulus jika nilai akhir >= batas ini
BATAS_LULUS = 60.0

# Identitas pembuat (ditampilkan pada menu)
PEMBUAT = "William Putra Pamungkas (25.83.1193) - TK01"
