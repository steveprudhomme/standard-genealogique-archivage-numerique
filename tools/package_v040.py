"""Créer un ZIP validé SGAN 0.4.0. SPDX-License-Identifier: MIT"""
import argparse
from pathlib import Path

try:
    from tools.package_v031 import package as build
    from tools.validate_v040 import validate
except ModuleNotFoundError:
    from package_v031 import package as build
    from validate_v040 import validate


def package(source, output):
    return build(source, output, validator=validate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Créer un ZIP SGAN 0.4.0 sans écraser de fichier existant")
    parser.add_argument("paquet", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(package(args.paquet, args.destination))
