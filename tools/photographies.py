"""Convention de nommage SGAN 0.4.0. SPDX-License-Identifier: MIT"""
import datetime
import re
from pathlib import PurePosixPath

try:
    from tools.validate import require
except ModuleNotFoundError:
    from validate import require

EXTENSIONS = ("jpg", "jpeg", "tif", "tiff", "png", "heic", "heif", "dng", "cr2", "cr3",
              "nef", "arw", "raf", "orf", "rw2", "pef", "srw", "raw", "avif", "webp",
              "jxl", "gif", "bmp")
DATE = r"(?:sans-date|[0-9]{4}(?:-env|-[0-9]{4}|-[0-9]{2}(?:-[0-9]{2})?)?)"
DESCRIPTION = r"[a-z0-9]+(?:-[a-z0-9]+)*"
ID = r"D(?!000000)[0-9]{6}"
RANK = r"(?:0[1-9]|[1-9][0-9]+)"
DERIVED = rf"(?:restauree|colorisee|recadree)-v{RANK}"
VARIANT = rf"(?:original|recto|verso|consultation|{DERIVED})"
PATTERN = rf"^(?P<date>{DATE})_(?P<description>{DESCRIPTION})_(?P<id>{ID})(?:_(?P<variante>{VARIANT}))?\.(?P<extension>{'|'.join(EXTENSIONS)})$(?![\s\S])"
# JSON Schema utilise des groupes ordinaires (la syntaxe des groupes nommés Python
# ne fait pas partie de l’expression portable publiée).
SCHEMA_PATTERN = re.sub(r"\(\?P<[^>]+>", "(", PATTERN)


def parse_name(name):
    match = re.fullmatch(PATTERN, name)
    require(match is not None, "PHOTO-01 : nom photographique non conforme")
    data = match.groupdict()
    token = data["date"]
    if token != "sans-date":
        try:
            if token.endswith("-env"):
                datetime.date(int(token[:4]), 1, 1)
            elif re.fullmatch(r"[0-9]{4}-[0-9]{4}", token):
                start, end = map(int, token.split("-"))
                datetime.date(start, 1, 1)
                datetime.date(end, 1, 1)
                require(start < end, "PHOTO-02 : intervalle chronologique invalide")
            else:
                values = [int(part) for part in token.split("-")]
                datetime.date(*(values + [1] * (3 - len(values))))
        except ValueError as exc:
            raise ValueError("PHOTO-02 : date photographique impossible") from exc
    return data


def is_image(path):
    return PurePosixPath(path).suffix.lower().lstrip(".") in EXTENSIONS


def validate_photos(package, inventories):
    """Contrôler les noms, IDs et liens vers les originaux sans lire les images."""
    by_path, by_id = {}, {}
    for row in inventories:
        by_id.setdefault(row["document_id"], []).append(row)
        if row["chemin_relatif"]:
            by_path.setdefault(row["chemin_relatif"], []).append(row)
    paths = {path for path in package.files if "06_Photographies" in PurePosixPath(path).parts and is_image(path)}
    paths.update(row["chemin_relatif"] for row in inventories
                 if row["categorie"] == "06_Photographies" and row["chemin_relatif"] and is_image(row["chemin_relatif"]))
    identities, parent_edges = {}, {}
    for path in sorted(paths):
        data = parse_name(PurePosixPath(path).name)
        rows = by_path.get(path, [])
        require(rows and any(r["categorie"] == "06_Photographies" for r in rows), "PHOTO-03 : image sans inventaire photographique")
        did = data["id"]
        require(all(row["document_id"] == did for row in rows), "PHOTO-03 : identifiant du nom différent de l’inventaire")
        require(did not in identities or identities[did] == path, "PHOTO-03 : identifiant attribué à plusieurs fichiers")
        identities[did] = path
        parents = set()
        for row in rows:
            # Déclaration lisible dans la colonne notes, sans ajouter de colonne CSV.
            if "derive_de=" in row["notes"]:
                tokens = re.findall(r"(?<![a-z0-9_])derive_de=([^;\s]+)", row["notes"])
                require(tokens and all(re.fullmatch(ID, token) for token in tokens), "PHOTO-04 : référence de dérivation invalide")
                parents.update(tokens)
        derived = data["variante"] == "consultation" or bool(re.fullmatch(DERIVED, data["variante"] or ""))
        require(not derived or len(parents) == 1, "PHOTO-04 : indiquer derive_de=Dxxxxxx pour la copie dérivée")
        require(len(parents) <= 1, "PHOTO-04 : plusieurs sources immédiates de dérivation")
        if parents:
            parent = next(iter(parents))
            require(parent != did and parent in by_id, "PHOTO-04 : original absent ou référence vers soi-même")
            originals = by_id[parent]
            require(all(r["chemin_relatif"] in package.files and is_image(r["chemin_relatif"]) for r in originals),
                    "PHOTO-04 : image de référence locale absente")
            parent_edges[did] = parent
    for start in parent_edges:
        seen, node = set(), start
        while node in parent_edges:
            require(node not in seen, "PHOTO-04 : cycle entre fichiers dérivés")
            seen.add(node)
            node = parent_edges[node]
    return len(paths)
