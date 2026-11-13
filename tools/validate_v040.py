"""Valider SGAN 0.4.0 et ses photographies, en lecture seule. SPDX-License-Identifier: MIT"""
import argparse
import csv
import json
import sys
import zipfile
from pathlib import Path

try:
    from tools.validate_v031 import Package, validate_package, table
    from tools.photographies import validate_photos
    from tools.validate import Invalid
except ModuleNotFoundError:
    from validate_v031 import Package, validate_package, table
    from photographies import validate_photos
    from validate import Invalid


def validate(source):
    p = Package(source)
    try:
        result = validate_package(p, False, "0.4.0")
        rows = []
        for person in table(p, "Index/individus.csv", "individus", "0.4.0"):
            rows.extend(table(p, f"Classement/{person['dossier']}/inventaire.csv", "inventaire", "0.4.0"))
        result["photographies"] = validate_photos(p, rows)
        return result
    finally:
        p.close()


def main():
    parser = argparse.ArgumentParser(description="Valider SGAN 0.4.0 et le nommage photographique")
    parser.add_argument("paquet", type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.paquet)
    except (Invalid, OSError, ValueError, csv.Error, zipfile.BadZipFile) as exc:
        print(f"NON CONFORME : {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
