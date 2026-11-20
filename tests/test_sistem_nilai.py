import json
import os
import tempfile
import unittest

from sistem_nilai import analytics, operations, validator
from sistem_nilai.io_handler import DataFileError, baca_json, muat_mahasiswa


def mhs(nim, kelas="TK-01", tugas=80, uts=80, uas=80, nama="Budi"):
    return validator.validasi_record(
        {"nim": nim, "nama": nama, "kelas": kelas, "tugas": tugas, "uts": uts, "uas": uas}
    )


class TestValidator(unittest.TestCase):
    def test_nilai_valid_dan_koma(self):
        self.assertEqual(validator.validasi_nilai("85,5"), 85.5)

    def test_nilai_kosong_menjadi_none(self):
        self.assertIsNone(validator.validasi_nilai("  "))
        self.assertIsNone(validator.validasi_nilai(None))

    def test_nilai_negatif_dan_terlalu_besar(self):
        for buruk in (-1, 101, "abc", "nan", True):
            with self.assertRaises(ValueError):
                validator.validasi_nilai(buruk)

    def test_nim_dan_nama_tidak_valid(self):
        with self.assertRaises(ValueError):
            validator.validasi_nim("12345")
        with self.assertRaises(ValueError):
            validator.validasi_nama("Budi123")


class TestAnalytics(unittest.TestCase):
    def test_nilai_akhir_berbobot(self):
        self.assertEqual(analytics.hitung_nilai_akhir(100, 100, 100), 100.0)
        self.assertEqual(analytics.hitung_nilai_akhir(80, 70, 90), 81.0)

    def test_edge_case_nilai_kosong(self):
        self.assertIsNone(analytics.hitung_nilai_akhir(80, None, 90))
        self.assertEqual(analytics.tentukan_grade(None), "-")

    def test_grade(self):
        self.assertEqual(analytics.tentukan_grade(85), "A")
        self.assertEqual(analytics.tentukan_grade(84.99), "B")
        self.assertEqual(analytics.tentukan_grade(10), "E")

    def test_rekap_data_kosong_tidak_error(self):
        rekap = analytics.rekap_statistik([])
        self.assertEqual(rekap["total_mahasiswa"], 0)
        self.assertIsNone(rekap["rata_rata"])

    def test_rekap_normal(self):
        hasil = analytics.lengkapi_hasil([mhs("23.11.0001", uas=100), mhs("23.11.0002", uas=60)])
        rekap = analytics.rekap_statistik(hasil)
        self.assertEqual(rekap["sudah_dinilai"], 2)
        self.assertEqual(rekap["jumlah_lulus"], 2)


class TestOperations(unittest.TestCase):
    def test_tambah_nim_ganda_ditolak(self):
        data = [mhs("23.11.0001")]
        with self.assertRaises(ValueError):
            operations.tambah_mahasiswa(data, mhs("23.11.0001"))

    def test_hapus_dan_duplikat(self):
        data = [mhs("23.11.0001"), mhs("23.11.0001"), mhs("23.11.0002")]
        unik, jumlah = operations.hapus_duplikat(data)
        self.assertEqual((len(unik), jumlah), (2, 1))
        baru, ok = operations.hapus_mahasiswa(unik, "23.11.0002")
        self.assertTrue(ok)
        self.assertEqual(len(baru), 1)

    def test_cari_kosong_ditolak(self):
        with self.assertRaises(ValueError):
            operations.cari_nama([mhs("23.11.0001")], "   ")


class TestIO(unittest.TestCase):
    def test_file_tidak_ada(self):
        with self.assertRaises(DataFileError):
            baca_json("tidak_ada.json")

    def test_json_rusak_dan_record_buruk(self):
        with tempfile.TemporaryDirectory() as d:
            rusak = os.path.join(d, "rusak.json")
            with open(rusak, "w", encoding="utf-8") as f:
                f.write("[{")
            with self.assertRaises(DataFileError):
                baca_json(rusak)

            campur = os.path.join(d, "campur.json")
            with open(campur, "w", encoding="utf-8") as f:
                json.dump([{"nim": "23.11.0001", "nama": "Ani", "kelas": "TK-01"},
                           {"nim": "salah", "nama": "X", "kelas": "TK-01"}], f)
            valid, galat = muat_mahasiswa(campur)
            self.assertEqual((len(valid), len(galat)), (1, 1))


if __name__ == "__main__":
    unittest.main()
