"""Générer les schémas JSON et YAML identiques. SPDX-License-Identifier: MIT"""
import argparse
import json
from pathlib import Path

import yaml


class SchemaDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://raw.githubusercontent.com/steveprudhomme/standard-genealogique-archivage-numerique/v0.1.0-draft/schemas/0.1.0/"
CODE = r"^(1[12]*|X(?!000000)[0-9]{6})(-D[1-9][0-9]*|-U[1-9][0-9]*-[EC][1-9][0-9]*)*$"


def obj(properties, required=None):
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required,
            "additionalProperties": False}


def array(items, minimum=0):
    return {"type": "array", "items": items, "minItems": minimum, "uniqueItems": True}


def ident(prefix):
    return {"type": "string", "pattern": f"^{prefix}(?!000000)[0-9]{{6}}$"}


TEXT = {"type": "string", "minLength": 1, "pattern": r"\S"}
NULLTEXT = {"anyOf": [TEXT, {"type": "null"}]}


def schemas():
    citation = obj({"source_id": ident("S"), "localisation": TEXT,
                    "apport": {"enum": ["soutient", "contredit", "contexte"]}})
    assertion = obj({"id": ident("A"), "sujets": array(ident("P"), 1),
                     "predicat": TEXT, "valeur": TEXT,
                     "statut": {"enum": ["hypothese", "etayee", "contestee", "refutee"]},
                     "analyse": {"type": "string"}, "citations": array(citation)})
    assertion["allOf"] = [{"if": {"properties": {"statut": {"enum": ["etayee", "contestee"]}}},
                           "then": {"properties": {"analyse": TEXT, "citations": {"minItems": 1}}}}]
    person = obj({"standard": {"const": "SGAN"}, "version": {"const": "0.1.0"},
                  "id": ident("P"), "code": {"type": "string", "pattern": CODE},
                  "alias_codes": array({"type": "string", "pattern": CODE}),
                  "nom_affichage": TEXT, "autres_noms": array(TEXT),
                  "statut_vital": {"enum": ["vivant", "decede", "inconnu"]},
                  "notes": {"type": "string"}, "revision": {"type": "string", "format": "date"}})
    source = obj({"id": ident("S"), "titre": TEXT, "depot": NULLTEXT,
                  "cote": NULLTEXT, "provenance": TEXT})
    document = obj({"id": ident("D"), "titre": TEXT, "chemin": TEXT,
                    "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
                    "source_id": ident("S"), "personnes": array(ident("P"), 1),
                    "provenance": TEXT, "droits": TEXT,
                    "acces": {"enum": ["public", "restreint", "prive"]}})
    relation = obj({"id": ident("R"), "de": ident("P"), "vers": ident("P"),
                    "type": {"enum": ["parent_biologique", "parent_adoptif", "parent_social",
                                      "parent_indetermine", "partenaire"]},
                    "assertions": array(ident("A"))})
    collection = obj({"standard": {"const": "SGAN"}, "version": {"const": "0.1.0"},
                      "statut": {"const": "Draft"}, "profil": {"const": "socle"},
                      "collection_id": {"type": "string", "format": "uuid"},
                      "titre": TEXT, "resume": TEXT, "donnees_synthetiques": {"type": "boolean"},
                      "personne_reference": {"anyOf": [ident("P"), {"type": "null"}]},
                      "individus": array(obj({"id": ident("P"), "dossier": TEXT}), 1),
                      "sources": array(source), "documents": array(document),
                      "relations": array(relation), "assertions": array(assertion)})
    result = {"individu": person, "collection": collection}
    for name, schema in result.items():
        schema.update({"$schema": "https://json-schema.org/draft/2020-12/schema",
                       "$id": BASE + name + ".schema.json",
                       "title": f"SGAN {name} — Draft 0.1.0 non officiel",
                       "$comment": "SPDX-License-Identifier: MIT"})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "schemas/0.1.0"
    target.mkdir(parents=True, exist_ok=True)
    stale = []
    for name, schema in schemas().items():
        for suffix, text in [("json", json.dumps(schema, ensure_ascii=False, indent=2) + "\n"),
                             ("yaml", yaml.dump(schema, Dumper=SchemaDumper, allow_unicode=True, sort_keys=False))]:
            path = target / f"{name}.schema.{suffix}"
            if args.check:
                if not path.exists() or path.read_text(encoding="utf-8") != text:
                    stale.append(str(path.relative_to(ROOT)))
            else:
                path.write_text(text, encoding="utf-8", newline="\n")
    if stale:
        raise SystemExit("Schémas à régénérer : " + ", ".join(stale))
    print("Schémas synchronisés.")


if __name__ == "__main__":
    main()
