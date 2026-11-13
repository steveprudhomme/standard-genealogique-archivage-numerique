"""Valider une collection SGAN sans accès réseau. SPDX-License-Identifier: MIT"""
import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

SCHEMAS = Path(__file__).resolve().parents[1] / "schemas/0.1.0"


class Invalid(ValueError):
    """Erreur de conformité avec un diagnostic lisible."""


def require(condition, message):
    if not condition:
        raise Invalid(message)


def pairs(items):
    result = {}
    for key, value in items:
        require(isinstance(key, str), "SGAN-010 : clé non textuelle")
        require(key not in result, f"SGAN-010 : clé dupliquée {key}")
        result[key] = value
    return result


class StrictLoader(yaml.SafeLoader):
    pass


def mapping(loader, node):
    return pairs([(loader.construct_object(k), loader.construct_object(v)) for k, v in node.value])


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def load(path):
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix == ".json":
        def bad_constant(value):
            raise Invalid(f"SGAN-010 : constante JSON interdite {value}")
        return json.loads(text, object_pairs_hook=pairs, parse_constant=bad_constant)
    for token in yaml.scan(text):
        require(not isinstance(token, (yaml.tokens.AnchorToken, yaml.tokens.AliasToken, yaml.tokens.TagToken)),
                "SGAN-010 : ancres, alias et tags YAML interdits")
        if isinstance(token, yaml.tokens.ScalarToken) and token.plain:
            # Refuser les booléens non JSON et les nombres interprétés différemment.
            if token.value.lower() in {"yes", "no", "on", "off", "true", "false", "null", "~"}:
                require(token.value in {"true", "false", "null"}, "SGAN-010 : scalaire YAML hors sous-ensemble JSON")
            if re.match(r"^[+-]?[0-9]", token.value) and not isinstance(yaml.safe_load(token.value), str):
                try:
                    json.loads(token.value)
                except ValueError:
                    raise Invalid("SGAN-010 : citer les dates et scalaires ambigus YAML")
    data = yaml.load(text, Loader=StrictLoader)
    # Les dates, ensembles et flottants non finis ne font pas partie des types JSON.
    try:
        json.dumps(data, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise Invalid("SGAN-010 : type YAML non compatible JSON") from exc
    return data


def schema_check(data, name):
    schema = json.loads((SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(data), key=lambda e: str(list(e.path)))
    require(not errors, f"Schéma {name} : " + "; ".join(f"{list(e.path)} {e.message}" for e in errors[:5]))


def portable(relative):
    require(isinstance(relative, str) and relative, "SGAN-008 : chemin vide")
    for part in relative.split("/"):
        require(part not in {"", ".", ".."} and not re.search(r'[<>:"\\|?*\x00-\x1f]', part)
                and part[-1:] not in {" ", "."}, f"SGAN-008 : chemin non portable {relative}")
        require(not re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)", part, re.I),
                f"SGAN-008 : nom réservé {relative}")


def safe_path(root, relative):
    portable(relative)
    path = root / relative
    require(path.resolve().is_relative_to(root.resolve()), f"SGAN-008 : chemin hors collection {relative}")
    for component in [path, *path.parents]:
        if component == root:
            break
        require(not component.is_symlink(), f"SGAN-008 : lien symbolique {relative}")
        require(not getattr(component, "is_junction", lambda: False)(), f"SGAN-008 : jonction {relative}")
    return path


def one_file(folder, stem):
    paths = [folder / (stem + ext) for ext in (".json", ".yaml")]
    found = [p for p in paths if p.is_file()]
    require(len(found) == 1, f"SGAN-001/003 : exactement un {stem}.json ou .yaml dans {folder.name}")
    return found[0]


def index(items, label):
    result = {}
    for item in items:
        require(item["id"] not in result, f"SGAN-004 : identifiant dupliqué {item['id']} ({label})")
        result[item["id"]] = item
    return result


def validate(root):
    root = Path(root).absolute()
    require(root.is_dir() and not root.is_symlink()
            and not getattr(root, "is_junction", lambda: False)(), "Collection absente ou lien symbolique/jonction")
    # Parcours sans suivre les liens ; contrôle de tous les composants, y compris non déclarés.
    seen_paths = set()
    pending = [root]
    while pending:
        for path in pending.pop().iterdir():
            relative = path.relative_to(root).as_posix()
            safe_path(root, relative)
            key = unicodedata.normalize("NFC", relative).casefold()
            require(key not in seen_paths, f"SGAN-008 : collision de chemins {relative}")
            seen_paths.add(key)
            if path.is_dir():
                pending.append(path)
    manifest = load(one_file(root, "collection"))
    schema_check(manifest, "collection")
    people = index(manifest["individus"], "personnes")
    sources = index(manifest["sources"], "sources")
    documents = index(manifest["documents"], "documents")
    relations = index(manifest["relations"], "relations")
    assertions = index(manifest["assertions"], "assertions")
    require(manifest["personne_reference"] is None or manifest["personne_reference"] in people,
            "SGAN-004 : personne de référence absente")
    declared_dirs, codes, inventories = set(), set(), {}
    for pid, entry in people.items():
        folder_name = entry["dossier"]
        require("/" not in folder_name and not folder_name.startswith("_"), "SGAN-002 : dossier individuel à plat requis")
        require(folder_name not in declared_dirs, "SGAN-002 : dossier partagé entre individus")
        declared_dirs.add(folder_name)
        folder = safe_path(root, folder_name)
        require(folder.is_dir(), f"SGAN-003 : dossier absent {folder_name}")
        person = load(one_file(folder, "fiche_individu"))
        schema_check(person, "individu")
        require(person["id"] == pid, "SGAN-004 : identifiant fiche/index différent")
        require(folder_name.startswith(person["code"] + " ") and folder_name[len(person["code"]) + 1:].strip(),
                "SGAN-002 : préfixe du dossier différent du code")
        for code in [person["code"], *person["alias_codes"]]:
            require(code not in codes, f"SGAN-004 : code dupliqué {code}")
            codes.add(code)
        summary = folder / "LISEZ-MOI.md"
        require(summary.is_file() and summary.read_text(encoding="utf-8-sig").strip(), "SGAN-003 : résumé absent ou vide")
        inventory = folder / "inventaire.csv"
        require(inventory.is_file(), "SGAN-003 : inventaire absent")
        with inventory.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            require(reader.fieldnames == ["document_id", "role"], "SGAN-007 : en-tête CSV incorrect")
            ids = []
            for row in reader:
                require(None not in row and row.get("role") and row["role"].strip(), "SGAN-007 : ligne CSV invalide")
                ids.append(row["document_id"])
            require(len(ids) == len(set(ids)), "SGAN-007 : document répété dans l’inventaire")
            inventories[pid] = set(ids)
    actual_dirs = {p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith("_")}
    require(actual_dirs == declared_dirs, "SGAN-002 : dossier individuel non déclaré")
    expected_fiches = {root / d for d in declared_dirs}
    for pattern in ("fiche_individu.json", "fiche_individu.yaml"):
        require(all(p.parent in expected_fiches for p in root.rglob(pattern)), "SGAN-002 : fiche individuelle imbriquée ou cachée")
    doc_paths = set()
    for doc in documents.values():
        require(doc["source_id"] in sources, "SGAN-004 : source du document absente")
        require(set(doc["personnes"]) <= people.keys(), "SGAN-004 : personne du document absente")
        path = safe_path(root, doc["chemin"])
        require(doc["chemin"] not in doc_paths, "SGAN-006 : plusieurs notices pour le même fichier maître")
        doc_paths.add(doc["chemin"])
        require(path.is_file(), f"SGAN-006 : document absent {doc['chemin']}")
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        require(digest == doc["sha256"], f"SGAN-006 : empreinte incorrecte {doc['id']}")
    for pid, ids in inventories.items():
        expected = {d["id"] for d in documents.values() if pid in d["personnes"]}
        require(ids == expected, f"SGAN-007 : inventaire divergent pour {pid}")
    for assertion in assertions.values():
        require(set(assertion["sujets"]) <= people.keys(), "SGAN-004 : sujet d’assertion absent")
        require(all(c["source_id"] in sources for c in assertion["citations"]), "SGAN-004 : source de citation absente")
    graph = {pid: set() for pid in people}
    edge_keys = set()
    for rel in relations.values():
        left, right = rel["de"], rel["vers"]
        require(left in people and right in people, "SGAN-004 : extrémité de relation absente")
        require(left != right, "SGAN-005 : autorelation")
        require(set(rel["assertions"]) <= assertions.keys(), "SGAN-004 : assertion de relation absente")
        require(all({left, right} <= set(assertions[a]["sujets"]) for a in rel["assertions"]),
                "SGAN-004 : assertion sans les deux sujets de la relation")
        endpoints = tuple(sorted((left, right))) if rel["type"] == "partenaire" else (left, right)
        key = (rel["type"], *endpoints)
        require(key not in edge_keys, "SGAN-005 : relation dupliquée")
        edge_keys.add(key)
        if rel["type"].startswith("parent_"):
            graph[left].add(right)
    # Tri topologique itératif : adapté aux longues ascendances.
    indegree = dict.fromkeys(graph, 0)
    for children in graph.values():
        for child in children:
            indegree[child] += 1
    queue = [p for p, n in indegree.items() if n == 0]
    visited = 0
    while queue:
        node = queue.pop()
        visited += 1
        for child in graph[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    require(visited == len(graph), "SGAN-005 : cycle de filiation")
    return {"individus": len(people), "documents": len(documents), "relations": len(relations)}


def main():
    parser = argparse.ArgumentParser(description="Valider le socle SGAN Draft 0.1.0")
    parser.add_argument("collection", type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.collection)
    except (Invalid, OSError, ValueError, yaml.YAMLError, csv.Error) as exc:
        print(f"NON CONFORME : {exc}", file=sys.stderr)
        return 1
    print("CONFORME au socle structurel Draft 0.1.0 : " + json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
