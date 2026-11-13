"""Valider un paquet ou ZIP 0.3.1 sans extraction. SPDX-License-Identifier: MIT"""
import argparse
import csv
import hashlib
import io
import json
import re
import stat
import sys
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator

try:
    from tools.profile_v031 import CATEGORIES, HEADERS, VERSION, ROOT
    from tools.validate import Invalid, require, pairs, safe_path, portable
except ModuleNotFoundError:
    from profile_v031 import CATEGORIES, HEADERS, VERSION, ROOT
    from validate import Invalid, require, pairs, safe_path, portable


class Package:
    """Lecture seule, chemins contrôlés ; les ZIP ne sont jamais extraits."""
    def __init__(self, source):
        self.source = Path(source)
        self.files, self.dirs, self.members = set(), set(), {}
        self.zip = None
        if self.source.is_file():
            self.zip = zipfile.ZipFile(self.source)
            try:
                entries = self.zip.infolist()
                require(sum(e.file_size for e in entries) <= 512 * 1024 * 1024, "Paquet trop volumineux (512 Mio maximum)")
                roots = [e.filename[:-len("Index/individus.csv")] for e in entries if e.filename.endswith("Index/individus.csv")]
                require(len(roots) == 1, "Un seul paquet avec Index/individus.csv est requis")
                prefix = roots[0]
                seen = set()
                for entry in entries:
                    raw = entry.filename.rstrip("/")
                    portable(raw)
                    key = unicodedata.normalize("NFC", raw).casefold()
                    require(key not in seen, "ZIP : entrée dupliquée ou collision de noms")
                    seen.add(key)
                    require(not stat.S_ISLNK(entry.external_attr >> 16), "ZIP : lien symbolique interdit")
                    require(entry.file_size <= 32 * 1024 * 1024, "ZIP : fichier trop volumineux (32 Mio maximum)")
                    if entry.filename == prefix:
                        continue
                    require(entry.filename.startswith(prefix), "ZIP : entrée hors du paquet")
                    relative = entry.filename[len(prefix):].rstrip("/")
                    if not relative:
                        continue
                    self._register(relative, entry.is_dir())
                    if not entry.is_dir():
                        self.members[relative] = entry
            except Exception:
                self.zip.close()
                raise
        else:
            require(self.source.is_dir() and not self.source.is_symlink()
                    and not getattr(self.source, "is_junction", lambda: False)(), "Racine de paquet invalide")
            pending = [self.source]
            while pending:
                for p in pending.pop().iterdir():
                    relative = p.relative_to(self.source).as_posix()
                    safe_path(self.source, relative)
                    self._register(relative, p.is_dir())
                    if p.is_dir():
                        pending.append(p)
        keys = {}
        for path in self.files | self.dirs:
            key = unicodedata.normalize("NFC", path).casefold()
            require(key not in keys, "Collision de chemins après normalisation")
            keys[key] = path
        require(not self.files & self.dirs, "Collision fichier/répertoire")

    def _register(self, relative, directory):
        portable(relative)
        (self.dirs if directory else self.files).add(relative)
        self.dirs.update(str(p) for p in PurePosixPath(relative).parents if str(p) != ".")

    def close(self):
        if self.zip:
            self.zip.close()

    def read(self, path):
        portable(path)
        require(path in self.files, "Fichier obligatoire ou référencé absent")
        return self.zip.read(self.members[path]) if self.zip else safe_path(self.source, path).read_bytes()

    def text(self, path):
        return self.read(path).decode("utf-8-sig")


SCHEMAS = {}


def check(data, name, schema_version="0.3.1"):
    key = (schema_version, name)
    if key not in SCHEMAS:
        schema = json.loads((ROOT / f"schemas/{schema_version}/{name}.schema.json").read_text(encoding="utf-8"))
        SCHEMAS[key] = Draft202012Validator(schema)
    error = next(SCHEMAS[key].iter_errors(data), None)
    require(error is None, f"Schéma {name} non conforme (valeurs privées masquées)")


def table(package, path, name, schema_version="0.3.1"):
    reader = csv.DictReader(io.StringIO(package.text(path), newline=""))
    require(reader.fieldnames == HEADERS[name], f"En-tête CSV incorrect : {name}")
    result = list(reader)
    for row in result:
        check(row, name + "-ligne", schema_version)
    return result


def ids(value):
    values = value.split(";") if value else []
    require(all(values) and len(values) == len(set(values)) if values else True, "Liste de références vide ou dupliquée")
    return set(values)


def validate(source, accept_legacy=False):
    package = Package(source)
    try:
        return validate_package(package, accept_legacy)
    finally:
        package.close()


def validate_package(p, accept_legacy, schema_version="0.3.1"):
    warnings = []
    required = ["LISEZ-MOI.md", "Documentation/specification_provisoire.md", "Documentation/categories_documentaires.md"]
    for path in required:
        require(p.text(path).strip(), "Documentation obligatoire vide")
    documentation = "\n".join(p.text(path) for path in required)
    if "Aucun sous-dossier documentaire vide n'est créé" in documentation:
        warnings.append("Documentation héritée contradictoire sur les dossiers vides ; appliquer les dix catégories obligatoires.")
    indexes = {name: table(p, f"Index/{name}.csv", name, schema_version) for name in HEADERS if name != "inventaire"}
    people, codes, folders, fiches = {}, {}, set(), {}
    edges, inventory_docs = set(), {}
    legacy_count = 0
    for row in indexes["individus"]:
        gid, code, folder = row["id_gedcom"], row["code_genealogique"], row["dossier"]
        require(gid not in people and code not in codes and folder not in folders, "Individu, code ou dossier dupliqué")
        require("/" not in folder and folder.startswith(code + " ") and folder[len(code)+1:].strip(), "Dossier individuel non plat ou préfixe incorrect")
        portable(folder)
        people[gid], codes[code] = row, gid
        folders.add(folder)
        base = "Classement/" + folder
        immediate = {d[len(base)+1:] for d in p.dirs if d.startswith(base + "/") and "/" not in d[len(base)+1:]}
        require(immediate == set(CATEGORIES), "Chaque individu doit posséder exactement les dix catégories 01 à 10")
        require(p.text(base + "/LISEZ-MOI.md").strip(), "Résumé individuel vide")
        # Le prototype utilise un objet JSON dans un fichier .yaml (sous-ensemble YAML 1.2).
        fiche = json.loads(p.text(base + "/fiche_individu.yaml"), object_pairs_hook=pairs)
        if fiche.get("version") == "0.3.0-draft" and accept_legacy and schema_version == "0.3.1":
            fiche = dict(fiche, version=VERSION)
            legacy_count += 1
        check(fiche, "individu", schema_version)
        fiches[gid] = fiche
        trace = fiche["tracabilite"]
        require(trace["identifiant_gedcom"] == gid and fiche["identifiant_permanent_provisoire"] == "GEDCOM:" + gid, "Référence GEDCOM incohérente")
        require(fiche["code_genealogique"] == code and fiche["identite"]["nom_complet"] == row["nom"]
                and trace["methode_numerotation"] == row["methode"], "Fiche et index individuel divergents")
        for event, field in [("naissance", "naissance_date_source"), ("deces", "deces_date_source")]:
            require(((fiche["evenements"][event] or {}).get("date") or "") == row[field], "Date source divergente entre fiche et index")
        source = trace["fichier_source"]
        require("/" not in source and source.lower().endswith(".ged"), "Nom du GEDCOM source invalide")
        require("Sources/" + source in p.files, "GEDCOM source absent")
        for kind in ("parents", "partenaires", "enfants"):
            relatives = fiche["relations"][kind]
            relation_ids = {r["gedcom_id"] for r in relatives}
            require(len(relation_ids) == len(relatives) and relation_ids == ids(row[kind + "_gedcom"]), "Relations fiche/index divergentes ou dupliquées")
            edges.update((gid, kind, other) for other in relation_ids)
        inv = table(p, base + "/inventaire.csv", "inventaire", schema_version)
        inv_ids = set()
        for doc in inv:
            did = doc["document_id"]
            require(did not in inv_ids, "Document répété dans un inventaire")
            inv_ids.add(did)
            require(doc["chemin_relatif"] or doc["cote"] or doc["url_source"], "Document sans localisation")
            if doc["chemin_relatif"]:
                digest = hashlib.sha256(p.read(doc["chemin_relatif"])).hexdigest()
                require(doc["sha256"] == digest, "Empreinte de document absente ou incorrecte")
            else:
                require(not doc["sha256"], "Empreinte sans fichier local")
            common = tuple(doc[k] for k in ["titre", "date", "chemin_relatif", "provenance", "cote", "url_source", "sha256"])
            require(did not in inventory_docs or inventory_docs[did] == common, "Document partagé décrit de manière contradictoire")
            inventory_docs[did] = common
    require(bool(people) and "1" in codes, "Une personne de référence de code 1 est requise")
    actual = {d.split("/")[1] for d in p.dirs if d.startswith("Classement/") and len(d.split("/")) == 2}
    require(actual == folders, "Dossier individuel absent ou non indexé")
    expected_fiches = {"Classement/" + f + "/fiche_individu.yaml" for f in folders}
    require({f for f in p.files if PurePosixPath(f).name.startswith("fiche_individu.")} == expected_fiches, "Fiche supplémentaire ou imbriquée")
    for gid, f in fiches.items():
        for kind, relatives in f["relations"].items():
            for other in relatives:
                ref = other["gedcom_id"]
                require(ref in people and ref != gid, "Relation pendante ou autorelation")
                require(other["code"] == people[ref]["code_genealogique"] and other["nom"] == people[ref]["nom"], "Référence de relation incohérente")
                reverse = {"parents": "enfants", "enfants": "parents", "partenaires": "partenaires"}[kind]
                require((ref, reverse, gid) in edges, "Relation réciproque absente")
    index_edges = set()
    for row in indexes["relations"]:
        left, right, kind = row["personne_gedcom"], row["autre_personne_gedcom"], row["type_relation"]
        require(left in people and right in people, "Index de relations : personne absente")
        require(row["code_personne"] == people[left]["code_genealogique"] and row["code_autre_personne"] == people[right]["code_genealogique"], "Index de relations : code divergent")
        key = (left, kind, right)
        require(key not in index_edges, "Relation indexée deux fois")
        index_edges.add(key)
    require(index_edges == edges, "Index des relations différent des fiches")
    family_ids, family_edges = set(), set()
    child_in, partner_in = {gid: set() for gid in people}, {gid: set() for gid in people}
    for row in indexes["familles"]:
        fid = row["famille_gedcom"]
        require(fid not in family_ids, "Famille dupliquée")
        family_ids.add(fid)
        parents = {x for x in [row["pere_gedcom"], row["mere_gedcom"]] if x}
        children = ids(row["enfants_gedcom"])
        require(parents | children <= people.keys(), "Membre de famille absent")
        require(not parents & children, "Une personne est parent et enfant dans la même famille")
        for child in children:
            child_in[child].add(fid)
        for parent in parents:
            partner_in[parent].add(fid)
            family_edges.update((parent, "partenaires", other) for other in parents if other != parent)
            for child in children:
                family_edges.update([(parent, "enfants", child), (child, "parents", parent)])
    require(family_edges == edges, "Familles et relations divergentes")
    for gid, f in fiches.items():
        require(set(f["familles_gedcom"]["enfant_de"]) == child_in[gid]
                and set(f["familles_gedcom"]["partenaire_dans"]) == partner_in[gid], "Appartenance familiale incohérente")
    alternate = set()
    for row in indexes["chemins_ascendants_alternatifs"]:
        gid, code = row["personne_gedcom"], row["code_alternatif"]
        require(gid in people and row["code_principal"] == people[gid]["code_genealogique"], "Chemin alternatif sans personne principale")
        require(code not in codes and code not in alternate, "Chemin alternatif ambigu ou dupliqué")
        alternate.add(code)
    if legacy_count:
        warnings.append(f"{legacy_count} fiches portent encore 0.3.0-draft ; compatibilité de lecture explicite, aucune réécriture.")
    if any("~" in c for c in set(codes) | alternate):
        warnings.append("Codes historiques avec ~ conservés ; leur sémantique reste à stabiliser.")
    return {"profil": schema_version + "-draft", "individus": len(people), "familles": len(family_ids),
            "relations": len(edges), "categories": 10 * len(people), "documents": len(inventory_docs),
            "avertissements": warnings}


def main():
    parser = argparse.ArgumentParser(description="Valider un paquet ou ZIP SGAN avec dix catégories par individu")
    parser.add_argument("paquet", type=Path)
    parser.add_argument("--accepter-prototype-03", action="store_true", help="Tolérer les fiches héritées 0.3.0-draft avec avertissement")
    args = parser.parse_args()
    try:
        result = validate(args.paquet, args.accepter_prototype_03)
    except (Invalid, OSError, ValueError, csv.Error, zipfile.BadZipFile) as exc:
        print(f"NON CONFORME : {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
