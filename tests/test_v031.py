"""Régressions du profil à dix dossiers, données fictives. SPDX-License-Identifier: MIT"""
import csv
import io
import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.generate_example_v031 import EXAMPLE, generate
from tools.package_v031 import package
from tools.profile_v031 import CATEGORIES, ROOT, VERSION, schemas
from tools.validate import Invalid, load
from tools.validate_v031 import validate
from jsonschema import Draft202012Validator


class Profile031(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "Paquet"
        shutil.copytree(EXAMPLE, self.root)
        self.person = self.root / "Classement/1 Exemple_Aline"

    def fiche(self, change):
        path = self.person / "fiche_individu.yaml"
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def mutate_csv(self, name, change):
        path = self.root / ("Index/" + name + ".csv")
        reader = csv.DictReader(io.StringIO(path.read_text(encoding="utf-8")))
        fields, rows = reader.fieldnames, list(reader)
        change(rows)
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fields)
            writer.writeheader()
            writer.writerows(rows)

    def test_reference(self):
        result = validate(self.root)
        self.assertEqual((result["individus"], result["categories"], result["documents"]), (10, 100, 1))

    def test_schemas(self):
        for name, expected in schemas().items():
            folder = ROOT / "schemas/0.3.1"
            self.assertEqual(load(folder / f"{name}.schema.json"), expected)
            self.assertEqual(load(folder / f"{name}.schema.yaml"), expected)
            Draft202012Validator.check_schema(expected)

    def test_missing_empty_category(self):
        path = self.person / CATEGORIES[0]
        (path / ".gitkeep").unlink()
        path.rmdir()
        with self.assertRaisesRegex(Invalid, "dix catégories"):
            validate(self.root)

    def test_identification_not_eleventh(self):
        (self.person / "00_Identification").mkdir()
        with self.assertRaisesRegex(Invalid, "dix catégories"):
            validate(self.root)

    def test_legacy_version_requires_explicit_mode(self):
        self.fiche(lambda f: f.update(version="0.3.0-draft"))
        with self.assertRaises(Invalid):
            validate(self.root)
        self.assertTrue(any("1 fiches" in w for w in validate(self.root, True)["avertissements"]))

    def test_future_version_not_accepted(self):
        self.fiche(lambda f: f.update(version="0.4.0-draft"))
        with self.assertRaises(Invalid):
            validate(self.root, True)

    def test_missing_source(self):
        (self.root / "Sources/exemple-fictif.ged").unlink()
        with self.assertRaisesRegex(Invalid, "GEDCOM source absent"):
            validate(self.root)

    def test_date_preserved(self):
        self.fiche(lambda f: f["evenements"]["naissance"].update(date="1900"))
        with self.assertRaisesRegex(Invalid, "Date source divergente"):
            validate(self.root)

    def test_provisional_identity(self):
        self.fiche(lambda f: f.update(identifiant_permanent_provisoire="GEDCOM:I99"))
        with self.assertRaisesRegex(Invalid, "GEDCOM incohérente"):
            validate(self.root)

    def test_relation_index(self):
        self.mutate_csv("relations", lambda rows: rows.pop())
        with self.assertRaisesRegex(Invalid, "différent des fiches"):
            validate(self.root)

    def test_family_membership(self):
        self.fiche(lambda f: f["familles_gedcom"].update(enfant_de=[]))
        with self.assertRaisesRegex(Invalid, "Appartenance familiale"):
            validate(self.root)

    def test_unknown_alternate_person(self):
        self.mutate_csv("chemins_ascendants_alternatifs", lambda rows: rows[0].update(personne_gedcom="I99"))
        with self.assertRaisesRegex(Invalid, "Chemin alternatif"):
            validate(self.root)

    def test_document_integrity(self):
        (self.root / "Archives/document-fictif.txt").write_text("altération", encoding="utf-8")
        with self.assertRaisesRegex(Invalid, "Empreinte"):
            validate(self.root)

    def test_zip_preserves_empty_folders(self):
        output = Path(self.temp.name) / "example.zip"
        result = package(self.root, output)
        self.assertEqual(result["categories"], 100)
        with zipfile.ZipFile(output) as z:
            self.assertTrue(all(not n.endswith(".gitkeep") for n in z.namelist()))
            self.assertIn("Classement/1 Exemple_Aline/01_Etat_civil/", z.namelist())

    def test_missing_empty_folder_in_zip(self):
        output = Path(self.temp.name) / "incomplete.zip"
        with zipfile.ZipFile(output, "w") as z:
            for p in self.root.rglob("*"):
                if p.is_file() and p.name != ".gitkeep":
                    z.write(p, p.relative_to(self.root).as_posix())
        with self.assertRaisesRegex(Invalid, "dix catégories"):
            validate(output)

    def test_zip_traversal(self):
        output = Path(self.temp.name) / "unsafe.zip"
        package(self.root, output)
        with zipfile.ZipFile(output, "a") as z:
            z.writestr("../escape.txt", "x")
        with self.assertRaisesRegex(Invalid, "SGAN-008"):
            validate(output)

    def test_zip_case_collision(self):
        output = Path(self.temp.name) / "collision.zip"
        package(self.root, output)
        with zipfile.ZipFile(output, "a") as z:
            z.writestr("sources/EXEMPLE-FICTIF.GED", "x")
        with self.assertRaisesRegex(Invalid, "collision"):
            validate(output)

    def test_package_never_overwrites(self):
        output = Path(self.temp.name) / "existing.zip"
        output.write_bytes(b"preserve")
        with self.assertRaises(FileExistsError):
            package(self.root, output)
        self.assertEqual(output.read_bytes(), b"preserve")

    def test_generator_reproducible(self):
        second = Path(self.temp.name) / "generated"
        generate(second)
        expected = {p.relative_to(EXAMPLE).as_posix(): p.read_bytes() for p in EXAMPLE.rglob("*") if p.is_file()}
        actual = {p.relative_to(second).as_posix(): p.read_bytes() for p in second.rglob("*") if p.is_file()}
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
