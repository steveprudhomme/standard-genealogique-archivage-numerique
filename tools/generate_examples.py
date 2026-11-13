"""Écrire uniquement les jeux synthétiques de référence. SPDX-License-Identifier: MIT"""
import csv
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "examples"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def generate(kind, people, relations, documented=False):
    root = ROOT / kind / "Classement"
    manifest = {
        "standard": "SGAN", "version": "0.1.0", "statut": "Draft", "profil": "socle",
        "collection_id": "c70ddc0b-cfd4-44f0-9c7e-" + ("000000000001" if documented else "000000000002"),
        "titre": "Collection entièrement fictive — " + kind,
        "resume": "Jeu synthétique de démonstration ; aucune personne ni archive réelle. Les emplacements 11 et 12 désignent les parents choisis pour l’ascendance.",
        "donnees_synthetiques": True, "personne_reference": "P000001",
        "individus": [], "sources": [], "documents": [], "relations": relations, "assertions": []}
    for number, code, label, aliases in people:
        pid = f"P{number:06}"
        folder = root / f"{code} {label}"
        manifest["individus"].append({"id": pid, "dossier": folder.name})
        person = {"standard": "SGAN", "version": "0.1.0", "id": pid, "code": code,
                  "alias_codes": aliases, "nom_affichage": label.replace("_", " "),
                  "autres_noms": [], "statut_vital": "inconnu",
                  "notes": "Personnage entièrement fictif, créé pour les tests SGAN.", "revision": "2026-11-13"}
        suffix = "yaml" if documented else "json"
        content = yaml.safe_dump(person, allow_unicode=True, sort_keys=False) if documented else json.dumps(person, ensure_ascii=False, indent=2) + "\n"
        write(folder / f"fiche_individu.{suffix}", content)
        write(folder / "LISEZ-MOI.md", f"# {label.replace('_', ' ')}\n\nPersonnage entièrement fictif ({pid}).\n\nDates et statut vital inconnus. Voir le manifeste de collection pour les relations et assertions ; inventaire.csv pour les documents.\n")
        with (folder / "inventaire.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(["document_id", "role"])
            if documented and number in (1, 2, 3):
                writer.writerow(["D000001", "personne citée dans la simulation"])
    if documented:
        write(root / "_archives/acte-fictif.txt", "DOCUMENT SYNTHÉTIQUE — sans valeur historique.\nSimulation : Aline Exemple est enfant de Basile Exemple et Camille Exemple.\nDate simulée : vers 1900 ; une seconde source fictive propose 1901.\n")
        manifest["sources"] = [
            {"id": "S000001", "titre": "Registre simulé A", "depot": "Dépôt fictif SGAN", "cote": "SIM-A-1", "provenance": "Texte inventé pour cet exemple."},
            {"id": "S000002", "titre": "Note simulée B", "depot": None, "cote": None, "provenance": "Source fictive contradictoire, sans fichier associé."}]
        manifest["documents"] = [{"id": "D000001", "titre": "Simulation de notice familiale", "chemin": "_archives/acte-fictif.txt",
                                  "sha256": hashlib.sha256((root / "_archives/acte-fictif.txt").read_bytes()).hexdigest(),
                                  "source_id": "S000001", "personnes": ["P000001", "P000002", "P000003"],
                                  "provenance": "Création synthétique pour le dépôt SGAN.", "droits": "MIT — contributeurs SGAN", "acces": "public"}]
        manifest["assertions"] = [
            {"id": "A000001", "sujets": ["P000001", "P000002"], "predicat": "filiation", "valeur": "Basile est parent d’Aline dans la simulation.",
             "statut": "etayee", "analyse": "Le registre fictif énonce ce lien ; cet exemple illustre la citation, sans preuve réelle.",
             "citations": [{"source_id": "S000001", "localisation": "ligne 2", "apport": "soutient"}]},
            {"id": "A000002", "sujets": ["P000001"], "predicat": "naissance", "valeur": "vers 1900",
             "statut": "contestee", "analyse": "Les deux sources fictives divergent ; la date n’est pas résolue.",
             "citations": [{"source_id": "S000001", "localisation": "ligne 3", "apport": "soutient"},
                           {"source_id": "S000002", "localisation": "note unique : 1901", "apport": "contredit"}]}]
    if documented:
        write(root / "collection.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    else:
        write(root / "collection.yaml", yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False))


def main():
    generate("minimal", [(1, "1", "Personne_inconnue", [])], [])
    people = [(1, "1", "Exemple_Aline", ["11-U1-E1"]), (2, "11", "Exemple_Basile", []),
              (3, "12", "Exemple_Camille", []), (4, "11-U2-C1", "Exemple_Dominique", []),
              (5, "11-U2-E1", "Exemple_Emile", []), (6, "1-D1", "Exemple_Florence", []),
              (7, "1-U1-C1", "Exemple_Gael", []), (8, "111", "Exemple_Hortense", ["121"]),
              (9, "X000001", "Exemple_Indigo", [])]
    edges = [(2, 1, "parent_biologique"), (3, 1, "parent_biologique"),
             (2, 3, "partenaire"), (2, 4, "partenaire"), (2, 5, "parent_biologique"),
             (4, 5, "parent_biologique"), (1, 6, "parent_adoptif"), (7, 6, "parent_adoptif"),
             (1, 7, "partenaire"), (8, 2, "parent_biologique"), (8, 3, "parent_biologique")]
    relations = [{"id": f"R{i:06}", "de": f"P{a:06}", "vers": f"P{b:06}", "type": kind,
                  "assertions": ["A000001"] if i == 1 else []}
                 for i, (a, b, kind) in enumerate(edges, 1)]
    generate("documente", people, relations, documented=True)
    print("Exemples synthétiques générés.")


if __name__ == "__main__":
    main()
