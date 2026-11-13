"""Paquet fictif avec vignettes techniques PNG, sans personne réelle. SPDX-License-Identifier: MIT"""
import hashlib
import json
import struct
import zlib

try:
    from tools.profile_v031 import CATEGORIES, HEADERS, ROOT
    from tools.generate_example_v031 import csv_write, write
except ModuleNotFoundError:
    from profile_v031 import CATEGORIES, HEADERS, ROOT
    from generate_example_v031 import csv_write, write

EXAMPLE = ROOT / "examples/v0.4.0/Paquet"
PHOTO_NAMES = [
    "1948-06-12_portrait-exemple-aline_D000123.png",
    "1948_portrait-exemple-aline_D000124.png",
    "1948-env_portrait-exemple-aline_D000125.png",
    "1962-08_reunion-famille-exemple_D000126.png",
    "1975_vacances-famille-exemple-quebec_D000127.png",
    "sans-date_portrait-femme-non-identifiee_D000128.png",
    "1948-env_portrait-exemple-aline_D000129_restauree-v01.png",
    "1948-env_portrait-exemple-aline_D000130_colorisee-v01.png",
]


def png(color):
    """Une mire unie de 8 × 8 pixels, pas une photographie historique."""
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    scanlines = (b"\0" + bytes(color) * 8) * 8
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 8, 8, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(scanlines, level=9)) + chunk(b"IEND", b""))


def generate(root=EXAMPLE):
    people = [("I1", "1", "Aline", "reference"), ("I2", "11", "Basile", "ascendance")]
    indices, edges = [], []
    for gid, code, name, method in people:
        folder = code + " Exemple_" + name
        base = root / "Classement" / folder
        for category in CATEGORIES:
            write(base / category / ".gitkeep", "")
        kind = "parents" if gid == "I1" else "enfants"
        other = {"code": "11", "gedcom_id": "I2", "nom": "Exemple Basile"} if gid == "I1" else {"code": "1", "gedcom_id": "I1", "nom": "Exemple Aline"}
        relations = {"parents": [], "partenaires": [], "enfants": []}
        relations[kind].append(other)
        fiche = {"standard": "SGAN", "version": "0.4.0-draft", "statut": "prototype_non_officiel",
                 "code_genealogique": code, "identifiant_permanent_provisoire": "GEDCOM:" + gid,
                 "identite": {"nom_complet": "Exemple " + name, "nom": "Exemple", "prenoms": name, "sexe_gedcom": None},
                 "evenements": {"naissance": None, "deces": None}, "relations": relations,
                 "familles_gedcom": {"enfant_de": ["F1"] if gid == "I1" else [], "partenaire_dans": ["F1"] if gid == "I2" else []},
                 "tracabilite": {"fichier_source": "exemple-fictif.ged", "identifiant_gedcom": gid,
                                 "methode_numerotation": method, "note": "Personne et relations entièrement inventées pour les tests."}}
        write(base / "fiche_individu.yaml", json.dumps(fiche, ensure_ascii=False, indent=2) + "\n")
        write(base / "LISEZ-MOI.md", f"# Exemple {name} — personne fictive\n\nLes fichiers PNG de ce paquet sont des mires techniques de couleur unie. Leurs noms et dates servent à tester les conventions ; aucune photographie historique ni identité réelle n’est représentée.\n")
        indices.append(dict(zip(HEADERS["individus"], [code, gid, "Exemple " + name, folder, method, "", "", "I2" if gid == "I1" else "", "", "I1" if gid == "I2" else ""])))
        edges.append(dict(zip(HEADERS["relations"], [gid, code, kind, other["gedcom_id"], other["code"]])))
    rows = []
    for i, name in enumerate(PHOTO_NAMES):
        relative = ("Archives/Photos/" if i == 3 else "Classement/1 Exemple_Aline/06_Photographies/") + name
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        data = png((32 + i * 20, 64, 160 - i * 10))
        path.write_bytes(data)
        did = f"D{123+i:06}"
        notes = f"nom_original=MIRE_{i+1:02}.png; Mire technique fictive."
        if i in (6, 7):
            notes += " derive_de=D000125; Transformation simulée pour les tests."
        rows.append(dict(zip(HEADERS["inventaire"], [did, "06_Photographies", "Mire fictive : " + name.split("_")[1],
                       name.split("_")[0], relative, "Création technique SGAN sous MIT", "", "", "pièce fictive associée à la notice", hashlib.sha256(data).hexdigest(), notes])))
    csv_write(root / "Classement/1 Exemple_Aline/inventaire.csv", "inventaire", rows)
    csv_write(root / "Classement/11 Exemple_Basile/inventaire.csv", "inventaire", [rows[3]])
    csv_write(root / "Index/individus.csv", "individus", indices)
    csv_write(root / "Index/relations.csv", "relations", edges)
    csv_write(root / "Index/familles.csv", "familles", [dict(zip(HEADERS["familles"], ["F1", "I2", "", "I1", ""]))])
    csv_write(root / "Index/chemins_ascendants_alternatifs.csv", "chemins_ascendants_alternatifs", [])
    write(root / "Sources/exemple-fictif.ged", "0 HEAD\n1 SOUR SGAN_SYNTHETIQUE\n1 GEDC\n2 VERS 5.5.1\n2 FORM LINEAGE-LINKED\n1 CHAR UTF-8\n1 SUBM @SUB1@\n0 @SUB1@ SUBM\n1 NAME Exemple fictif SGAN\n0 @I1@ INDI\n1 NAME Aline /Exemple/\n1 FAMC @F1@\n0 @I2@ INDI\n1 NAME Basile /Exemple/\n1 FAMS @F1@\n0 @F1@ FAM\n1 HUSB @I2@\n1 CHIL @I1@\n0 TRLR\n")
    write(root / "LISEZ-MOI.md", "# SGAN Draft 0.4.0 — exemple technique fictif\n\nDeux notices inventées, vingt catégories, huit mires PNG. Les fichiers sont des carrés de couleur, pas des portraits. Ils démontrent les dates, le partage d’une image unique et les liens de dérivation. Les noms originale/restaurée/colorisée sont des scénarios de validation et ne décrivent aucune archive réelle.\n")
    write(root / "Documentation/specification_provisoire.md", "# SGAN Draft 0.4.0 — non officiel\n\nBase à dix catégories par personne, trois fichiers descriptifs et quatre index. Les photographies se nomment date_description_document-id[_variante].extension. Chaque fichier dérivé reçoit un nouvel ID et note sa référence avec derive_de=Dxxxxxx.\n")
    write(root / "Documentation/categories_documentaires.md", "# Dix catégories obligatoires, même vides\n\n" + "\n".join("- `" + c + "`" for c in CATEGORIES) + "\n")


if __name__ == "__main__":
    generate()
    print("Exemple 0.4.0 entièrement fictif généré.")
