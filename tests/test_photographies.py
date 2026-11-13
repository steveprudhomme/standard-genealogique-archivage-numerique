"""Conformité du nommage photo et intégration inventaire/ZIP. SPDX-License-Identifier: MIT"""
import csv
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from tools.generate_example_v040 import EXAMPLE, PHOTO_NAMES, generate
from tools.package_v040 import package
from tools.photographies import parse_name, validate_photos
from tools.profile_v040 import ROOT, schemas
from tools.validate import Invalid, load
from tools.validate_v031 import Package
from tools.validate_v040 import validate


class Names(unittest.TestCase):
    def test_accepted_dates(self):
        for date in ["1948-06-12", "1948-06", "1948", "1948-env", "1948-1952", "sans-date", "2000-02-29"]:
            with self.subTest(date=date):
                self.assertEqual(parse_name(date + "_portrait-exemple-aline_D000123.tif")["date"], date)

    def test_invalid_names(self):
        for name in ["1948_portrait_D000000.jpg", "1948_portrait_D123.jpg", "1948_Portrait_D000123.jpg", "1948_portrét_D000123.jpg",
                     "1948_portrait_aline_D000123.jpg", "1948_portrait_D000123.JPG", "1948_portrait_D000123_restauree-v00.jpg",
                     "1948_portrait_D000123_restauree-v1.jpg", "1948_portrait_D000123.jpg\n", "1948_11-aline_GEDCOM-I1.jpg"]:
            with self.subTest(name=name), self.assertRaises(Invalid):
                parse_name(name)

    def test_impossible_dates(self):
        for date in ["0000", "0000-env", "1948-00", "1948-13", "1948-02-30", "1900-02-29", "1952-1948", "1948-1948", "0000-1948"]:
            with self.subTest(date=date), self.assertRaises(ValueError):
                parse_name(date + "_portrait_D000123.png")

    def test_variants(self):
        for variant in ["original", "recto", "verso", "consultation", "restauree-v01", "colorisee-v02", "recadree-v100"]:
            self.assertEqual(parse_name(f"1948_portrait_D000123_{variant}.png")["variante"], variant)


class Photographies(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "Paquet"
        shutil.copytree(EXAMPLE, self.root)
        self.inv = self.root / "Classement/1 Exemple_Aline/inventaire.csv"
        reader = csv.DictReader(io.StringIO(self.inv.read_text(encoding="utf-8")))
        self.fields, self.rows = reader.fieldnames, list(reader)

    def save(self):
        with self.inv.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, self.fields)
            writer.writeheader()
            writer.writerows(self.rows)

    def test_reference_and_shared_image(self):
        result = validate(self.root)
        self.assertEqual((result["profil"], result["photographies"], result["documents"]), ("0.4.0-draft", 8, 8))

    def test_name_id_mismatch(self):
        self.rows[0]["document_id"] = "D999999"
        self.save()
        with self.assertRaisesRegex(Invalid, "PHOTO-03"):
            validate(self.root)

    def test_unlisted_image(self):
        self.rows.pop(0)
        self.save()
        with self.assertRaisesRegex(Invalid, "image sans inventaire"):
            validate(self.root)

    def test_derived_without_reference(self):
        self.rows[-1]["notes"] = "Copie colorisée"
        self.save()
        with self.assertRaisesRegex(Invalid, "indiquer derive_de"):
            validate(self.root)

    def test_missing_original(self):
        self.rows[-1]["notes"] = "derive_de=D999999"
        self.save()
        with self.assertRaisesRegex(Invalid, "original absent"):
            validate(self.root)

    def test_derivation_cycle(self):
        self.rows[-1]["notes"] = "derive_de=D000129"
        self.rows[-2]["notes"] = "derive_de=D000130"
        self.save()
        with self.assertRaisesRegex(Invalid, "cycle"):
            validate(self.root)

    def test_wrong_derivation_id_syntax(self):
        self.rows[-1]["notes"] = "derive_de=GEDCOM:I1"
        self.save()
        with self.assertRaisesRegex(Invalid, "référence de dérivation"):
            validate(self.root)

    def test_shared_photo_outside_category_is_checked(self):
        old = self.root / self.rows[3]["chemin_relatif"]
        new = old.with_name("IMG_4827.png")
        old.rename(new)
        for inv in self.root.glob("Classement/*/inventaire.csv"):
            inv.write_text(inv.read_text(encoding="utf-8").replace(PHOTO_NAMES[3], new.name), encoding="utf-8")
        with self.assertRaisesRegex(Invalid, "PHOTO-01"):
            validate(self.root)

    def test_sidecar_not_treated_as_an_image(self):
        (self.root / self.rows[0]["chemin_relatif"]).with_suffix(".xmp").write_text("metadata", encoding="utf-8")
        self.assertEqual(validate(self.root)["photographies"], 8)

    def test_old_version_not_silently_upgraded(self):
        path = self.root / "Classement/1 Exemple_Aline/fiche_individu.yaml"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = "0.3.1-draft"
        path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(Invalid, "Schéma individu"):
            validate(self.root)

    def test_photo_id_cannot_point_to_two_files(self):
        first = self.rows[0]
        relative = first["chemin_relatif"].replace("portrait-exemple-aline", "autre-portrait")
        (self.root / relative).write_bytes((self.root / first["chemin_relatif"]).read_bytes())
        rows = [*self.rows, dict(first, chemin_relatif=relative)]
        p = Package(self.root)
        try:
            with self.assertRaisesRegex(Invalid, "plusieurs fichiers"):
                validate_photos(p, rows)
        finally:
            p.close()

    def test_schemas_and_example_names(self):
        for name, schema in schemas().items():
            folder = ROOT / "schemas/0.4.0"
            self.assertEqual(load(folder / f"{name}.schema.json"), schema)
            self.assertEqual(load(folder / f"{name}.schema.yaml"), schema)
            Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schemas()["nom-photographie"])
        for name in PHOTO_NAMES:
            validator.validate(name)

    def test_zip(self):
        self.assertEqual(package(self.root, Path(self.temp.name) / "photos.zip")["photographies"], 8)

    def test_generation(self):
        other = Path(self.temp.name) / "generated"
        generate(other)
        expected = {p.relative_to(EXAMPLE).as_posix(): p.read_bytes() for p in EXAMPLE.rglob("*") if p.is_file()}
        actual = {p.relative_to(other).as_posix(): p.read_bytes() for p in other.rglob("*") if p.is_file()}
        self.assertEqual(expected, actual)

    def test_cli(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/validate_v040.py"), str(self.root)], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.rows[0]["document_id"] = "D999999"
        self.save()
        result = subprocess.run([sys.executable, str(ROOT / "tools/validate_v040.py"), str(self.root)], capture_output=True)
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
