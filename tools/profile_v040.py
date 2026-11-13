"""Schémas SGAN 0.4.0, extension du profil à dix dossiers. SPDX-License-Identifier: MIT"""
import argparse
import copy
import json

import yaml

try:
    from tools.profile_v031 import ROOT, schemas as baseline, SchemaDumper
    from tools.photographies import SCHEMA_PATTERN
except ModuleNotFoundError:
    from profile_v031 import ROOT, schemas as baseline, SchemaDumper
    from photographies import SCHEMA_PATTERN

VERSION = "0.4.0-draft"


def schemas():
    result = copy.deepcopy(baseline())
    result["individu"]["properties"]["version"] = {"const": VERSION}
    result["nom-photographie"] = {"type": "string", "pattern": SCHEMA_PATTERN,
                                   "description": "Date de prise de vue, description, identifiant et variante facultative. Les dates et liens d’inventaire sont contrôlés par le validateur."}
    for name, schema in result.items():
        schema.update({"$schema": "https://json-schema.org/draft/2020-12/schema",
                       "$id": f"https://raw.githubusercontent.com/steveprudhomme/standard-genealogique-archivage-numerique/v0.4.0-draft/schemas/0.4.0/{name}.schema.json",
                       "title": f"SGAN Draft 0.4.0 — {name}", "$comment": "SPDX-License-Identifier: MIT"})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    folder = ROOT / "schemas/0.4.0"
    folder.mkdir(parents=True, exist_ok=True)
    for name, schema in schemas().items():
        for ext, text in [("json", json.dumps(schema, ensure_ascii=False, indent=2) + "\n"),
                          ("yaml", yaml.dump(schema, Dumper=SchemaDumper, allow_unicode=True, sort_keys=False))]:
            path = folder / f"{name}.schema.{ext}"
            if args.check:
                if not path.exists() or path.read_text(encoding="utf-8") != text:
                    raise SystemExit(f"Schéma à régénérer : {name}.{ext}")
            else:
                path.write_text(text, encoding="utf-8", newline="\n")
    print("Schémas 0.4.0 synchronisés.")


if __name__ == "__main__":
    main()
