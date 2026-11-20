import argparse
import sys
from pathlib import Path

from sistem_nilai import cli

BASE = Path(__file__).resolve().parent


def baca_argumen(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Sistem Pengelolaan Data Nilai Mahasiswa")
    p.add_argument("--input", default=str(BASE / "data" / "data_input.json"), help="file JSON input")
    p.add_argument("--output", default=str(BASE / "data" / "data_output.json"), help="file JSON output")
    p.add_argument("--csv", default=str(BASE / "data" / "data_output.csv"), help="file CSV output")
    p.add_argument("--batch", action="store_true", help="proses otomatis tanpa menu")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = baca_argumen(argv)
    if args.batch:
        return cli.jalankan_batch(args.input, args.output, args.csv)
    cli.jalankan_menu(args.input, args.output, args.csv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
