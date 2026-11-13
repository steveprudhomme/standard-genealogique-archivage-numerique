"""Exemple inventé indépendamment des archives privées. SPDX-License-Identifier: MIT"""
import csv
import hashlib
import io
import json
from pathlib import Path

try:
    from tools.profile_v031 import CATEGORIES, HEADERS, VERSION, ROOT
except ModuleNotFoundError:
    from profile_v031 import CATEGORIES, HEADERS, VERSION, ROOT

EXAMPLE = ROOT / "examples/v0.3.1/Paquet"


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def csv_write(path, name, rows):
    text = io.StringIO(newline="")
    writer = csv.DictWriter(text, fieldnames=HEADERS[name], lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    write(path, text.getvalue())


def generate(root=EXAMPLE):
    people = [
        ("I1", "1", "Aline", "reference"), ("I2", "11", "Basile", "ascendance"),
        ("I3", "12", "Camille", "ascendance"), ("I4", "11-C02", "Dominique", "partenaire"),
        ("I5", "11-U02-E01", "Emile", "branche_familiale"), ("I6", "1-D01", "Florence", "descendance"),
        ("I7", "1-C01", "Gael", "partenaire"), ("I8", "X000001", "Indigo", "non_rattache"),
        ("I9", "1-C01-P1", "Hector", "parent_hors_ascendance"), ("I10", "112~2", "Iris", "ascendance")]
    families = [("F1", "I2", "I3", ["I1"]), ("F2", "I2", "I4", ["I5"]),
                ("F3", "I1", "I7", ["I6"]), ("F4", "I9", "", ["I7"]),
                ("F5", "", "I10", ["I2"]), ("F6", "", "I10", ["I3"])]
    info = {gid: {"code": code, "nom": "Exemple " + name, "dossier": code + " Exemple_" + name, "methode": method} for gid, code, name, method in people}
    links = {gid: {k: set() for k in ["parents", "partenaires", "enfants"]} for gid in info}
    memberships = {gid: {"enfant_de": [], "partenaire_dans": []} for gid in info}
    family_rows = []
    for fid, father, mother, children in families:
        parents = [x for x in [father, mother] if x]
        for parent in parents:
            memberships[parent]["partenaire_dans"].append(fid)
            links[parent]["partenaires"].update(set(parents) - {parent})
            links[parent]["enfants"].update(children)
        for child in children:
            memberships[child]["enfant_de"].append(fid)
            links[child]["parents"].update(parents)
        family_rows.append(dict(zip(HEADERS["familles"], [fid, father, mother, ";".join(children), ""])))
    document = "DOCUMENT FICTIF — sans valeur historique.\nExemple de document commun concernant Aline et Basile Exemple.\n"
    write(root / "Archives/document-fictif.txt", document)
    digest = hashlib.sha256(document.encode("utf-8")).hexdigest()
    individual_rows, relation_rows = [], []
    for gid, data in info.items():
        base = root / "Classement" / data["dossier"]
        for category in CATEGORIES:
            # Git ne conserve pas les répertoires vides. L’outil ZIP omet ces marqueurs.
            write(base / category / ".gitkeep", "")
        relations = {k: [{"code": info[other]["code"], "gedcom_id": other, "nom": info[other]["nom"]} for other in sorted(v)] for k, v in links[gid].items()}
        date = "ABT 1900" if gid == "I1" else ""
        fiche = {"standard": "SGAN", "version": VERSION, "statut": "prototype_non_officiel",
                 "code_genealogique": data["code"], "identifiant_permanent_provisoire": "GEDCOM:" + gid,
                 "identite": {"nom_complet": data["nom"], "nom": "Exemple", "prenoms": data["nom"].split()[1], "sexe_gedcom": None},
                 "evenements": {"naissance": {"date": date, "place": None, "value": None} if date else None, "deces": None},
                 "relations": relations, "familles_gedcom": memberships[gid],
                 "tracabilite": {"fichier_source": "exemple-fictif.ged", "identifiant_gedcom": gid,
                                 "methode_numerotation": data["methode"], "note": "Jeu entièrement synthétique. Codes provisoires, non déduits de données privées."}}
        write(base / "fiche_individu.yaml", json.dumps(fiche, ensure_ascii=False, indent=2) + "\n")
        write(base / "LISEZ-MOI.md", f"# {data['nom']} — personnage fictif\n\nRéférence locale : `{gid}` ; code : `{data['code']}`.\n\nLes relations sont décrites dans la fiche et les index. La date éventuelle est une valeur inventée, dont l’incertitude est conservée. Aucune information de ce jeu ne représente une famille réelle.\n")
        inv = []
        if gid in ["I1", "I2"]:
            inv.append(dict(zip(HEADERS["inventaire"], ["D0001", "02_Famille_et_relations", "Document fictif partagé", "", "Archives/document-fictif.txt", "Création synthétique SGAN sous MIT", "", "", "personne citée", digest, "Illustration sans valeur probante."])))
        csv_write(base / "inventaire.csv", "inventaire", inv)
        individual_rows.append(dict(zip(HEADERS["individus"], [data["code"], gid, data["nom"], data["dossier"], data["methode"], date, "", *[";".join(sorted(links[gid][k])) for k in ["parents", "partenaires", "enfants"]]])))
        for kind, entries in relations.items():
            for other in entries:
                relation_rows.append(dict(zip(HEADERS["relations"], [gid, data["code"], kind, other["gedcom_id"], other["code"]])))
    csv_write(root / "Index/individus.csv", "individus", individual_rows)
    csv_write(root / "Index/relations.csv", "relations", relation_rows)
    csv_write(root / "Index/familles.csv", "familles", family_rows)
    csv_write(root / "Index/chemins_ascendants_alternatifs.csv", "chemins_ascendants_alternatifs", [{"personne_gedcom": "I10", "code_alternatif": "122~2", "code_principal": "112~2"}])
    ged = ["0 HEAD", "1 SOUR SGAN_SYNTHETIQUE", "1 GEDC", "2 VERS 5.5.1", "2 FORM LINEAGE-LINKED", "1 CHAR UTF-8", "1 SUBM @SUB1@", "0 @SUB1@ SUBM", "1 NAME Exemple fictif SGAN"]
    for gid, data in info.items():
        ged.extend([f"0 @{gid}@ INDI", f"1 NAME {data['nom'].split()[1]} /Exemple/"])
        if gid == "I1":
            ged.extend(["1 BIRT", "2 DATE ABT 1900"])
        ged.extend(f"1 FAMC @{fid}@" for fid in memberships[gid]["enfant_de"])
        ged.extend(f"1 FAMS @{fid}@" for fid in memberships[gid]["partenaire_dans"])
    for fid, father, mother, children in families:
        ged.append(f"0 @{fid}@ FAM")
        if father:
            ged.append(f"1 HUSB @{father}@")
        if mother:
            ged.append(f"1 WIFE @{mother}@")
        ged.extend(f"1 CHIL @{child}@" for child in children)
    write(root / "Sources/exemple-fictif.ged", "\n".join(ged + ["0 TRLR", ""]))
    write(root / "LISEZ-MOI.md", "# SGAN Draft 0.3.1 — jeu entièrement synthétique\n\nDix personnes inventées, six familles fictives, trois fichiers et dix catégories par individu. Identités provisoires liées à cet export uniquement. Les marqueurs .gitkeep préservent les dossiers dans Git ; ils sont omis du ZIP généré.\n\nL’ascendant commun Iris illustre un chemin alternatif et un code historique contenant ~, dont la sémantique de génération reste ouverte. Les champs de familles GEDCOM sont des rôles exportés, sans garantie biologique.\n")
    write(root / "Documentation/specification_provisoire.md", "# SGAN Draft 0.3.1 — non officiel\n\nDossiers individuels à plat, trois fichiers descriptifs et dix catégories fixes, même vides. Fiches JSON dans des fichiers .yaml. Index et Sources au niveau du paquet. Aucun manifeste collection.json exigé. Références GEDCOM provisoires et dates source conservées.\n")
    write(root / "Documentation/categories_documentaires.md", "# Dix catégories obligatoires\n\nCréer ces dix dossiers, même vides. Aucun 00_Identification.\n\n" + "\n".join("- `" + c + "/`" for c in CATEGORIES) + "\n")


if __name__ == "__main__":
    generate()
    print("Exemple public 0.3.1 entièrement synthétique généré.")
