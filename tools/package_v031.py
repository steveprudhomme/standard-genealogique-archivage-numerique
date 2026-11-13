"""Créer un ZIP en conservant les dossiers vides. SPDX-License-Identifier: MIT"""
import argparse
import zipfile
from pathlib import Path

try:
    from tools.validate_v031 import validate
except ModuleNotFoundError:
    from validate_v031 import validate


def package(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output.is_relative_to(source):
        raise ValueError("Le ZIP doit être créé hors du paquet source")
    validate(source)
    # Mode x : un fichier existant n’est jamais écrasé.
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            relative = path.relative_to(source).as_posix()
            if path.is_dir():
                archive.writestr(relative + "/", b"")
            elif path.name != ".gitkeep":
                archive.write(path, relative)
    return validate(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Créer un ZIP SGAN 0.3.1 avec ses dix dossiers vides")
    parser.add_argument("paquet", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(package(args.paquet, args.destination))
