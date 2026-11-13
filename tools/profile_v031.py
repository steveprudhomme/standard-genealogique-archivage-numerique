"""Contrat du paquet SGAN 0.3.1. SPDX-License-Identifier: MIT"""
import argparse
import json
from pathlib import Path

import yaml

try:
    from tools.generate_schemas import SchemaDumper, obj, array
except ModuleNotFoundError:
    from generate_schemas import SchemaDumper, obj, array

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.3.1-draft"
CATEGORIES = ["01_Etat_civil", "02_Famille_et_relations", "03_Residences_et_recensements",
              "04_Etudes_et_professions", "05_Service_militaire", "06_Photographies",
              "07_Correspondance", "08_Biens_et_patrimoine", "09_Recherches_genealogiques",
              "10_Autres_documents"]
HEADERS = {
    "individus": ["code_genealogique", "id_gedcom", "nom", "dossier", "methode", "naissance_date_source", "deces_date_source", "parents_gedcom", "partenaires_gedcom", "enfants_gedcom"],
    "relations": ["personne_gedcom", "code_personne", "type_relation", "autre_personne_gedcom", "code_autre_personne"],
    "familles": ["famille_gedcom", "pere_gedcom", "mere_gedcom", "enfants_gedcom", "date_mariage_source"],
    "chemins_ascendants_alternatifs": ["personne_gedcom", "code_alternatif", "code_principal"],
    "inventaire": ["document_id", "categorie", "titre", "date", "chemin_relatif", "provenance", "cote", "url_source", "relation", "sha256", "notes"],
}
# Rang sur au moins deux chiffres ; suffixes ~ conservés comme jetons opaques.
RANK = r"(?:0[1-9]|[1-9][0-9]+)"
CODE = rf"^(?:1[12]*|X(?!000000)[0-9]{{6}})(?:-U{RANK}-E{RANK}|-[DC]{RANK}|-P[12]|~[1-9][0-9]*)*$(?![\s\S])"
METHODS = ["reference", "ascendance", "branche_familiale", "descendance", "partenaire", "parent_hors_ascendance", "non_rattache"]
TEXT = {"type": "string"}
NONEMPTY = {"type": "string", "minLength": 1}
NULLTEXT = {"type": ["string", "null"]}
PERSON = {"type": "string", "pattern": r"^I[0-9]+$"}
FAMILY = {"type": "string", "pattern": r"^F[0-9]+$"}
CODE_SCHEMA = {"type": "string", "pattern": CODE}


def schemas():
    event = {"anyOf": [{"type": "null"}, obj({"date": NULLTEXT, "place": NULLTEXT, "value": NULLTEXT})]}
    relative = obj({"code": CODE_SCHEMA, "gedcom_id": PERSON, "nom": TEXT})
    person = obj({
        "standard": {"const": "SGAN"}, "version": {"const": VERSION},
        "statut": {"const": "prototype_non_officiel"}, "code_genealogique": CODE_SCHEMA,
        "identifiant_permanent_provisoire": {"type": "string", "pattern": r"^GEDCOM:I[0-9]+$"},
        "identite": obj({"nom_complet": TEXT, "nom": NULLTEXT, "prenoms": NULLTEXT, "sexe_gedcom": NULLTEXT}),
        "evenements": obj({"naissance": event, "deces": event}),
        "relations": obj({k: array(relative) for k in ("parents", "partenaires", "enfants")}),
        "familles_gedcom": obj({"enfant_de": array(FAMILY), "partenaire_dans": array(FAMILY)}),
        "tracabilite": obj({"fichier_source": NONEMPTY, "identifiant_gedcom": PERSON,
                            "methode_numerotation": {"enum": METHODS}, "note": TEXT}),
    })
    result = {"individu": person}
    for name, headers in HEADERS.items():
        result[name + "-ligne"] = obj({k: TEXT for k in headers})
    for key in ["code_genealogique"]:
        result["individus-ligne"]["properties"][key] = CODE_SCHEMA
    result["individus-ligne"]["properties"]["id_gedcom"] = PERSON
    result["individus-ligne"]["properties"]["methode"] = {"enum": METHODS}
    rel = result["relations-ligne"]["properties"]
    for k in ["personne_gedcom", "autre_personne_gedcom"]:
        rel[k] = PERSON
    for k in ["code_personne", "code_autre_personne"]:
        rel[k] = CODE_SCHEMA
    rel["type_relation"] = {"enum": ["parents", "partenaires", "enfants"]}
    result["familles-ligne"]["properties"]["famille_gedcom"] = FAMILY
    alt = result["chemins_ascendants_alternatifs-ligne"]["properties"]
    alt.update({"personne_gedcom": PERSON, "code_alternatif": CODE_SCHEMA, "code_principal": CODE_SCHEMA})
    inv = result["inventaire-ligne"]["properties"]
    for k in ["document_id", "titre", "provenance", "relation"]:
        inv[k] = {"type": "string", "pattern": r"\S"}
    inv["categorie"] = {"enum": CATEGORIES}
    inv["sha256"] = {"type": "string", "pattern": "^([a-f0-9]{64})?$"}
    for name, schema in result.items():
        schema.update({"$schema": "https://json-schema.org/draft/2020-12/schema",
                       "$id": f"https://raw.githubusercontent.com/steveprudhomme/standard-genealogique-archivage-numerique/v0.3.1-draft/schemas/0.3.1/{name}.schema.json",
                       "title": f"SGAN Draft 0.3.1 — {name}", "$comment": "SPDX-License-Identifier: MIT"})
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    folder = ROOT / "schemas/0.3.1"
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
    print("Schémas 0.3.1 synchronisés.")


if __name__ == "__main__":
    main()
