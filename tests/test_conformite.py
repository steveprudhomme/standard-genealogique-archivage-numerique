"""Tests de conformité positifs et mutations invalides. SPDX-License-Identifier: MIT"""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import generate_schemas
from tools.validate import Invalid, load, safe_path, validate


class Conformite(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "Classement"
        shutil.copytree(ROOT / "examples/documente/Classement", self.root)
        self.path = self.root / "collection.json"
        self.manifest = load(self.path)
        self.person = self.root / self.manifest["individus"][0]["dossier"] / "fiche_individu.yaml"

    def save(self):
        self.path.write_text(json.dumps(self.manifest, ensure_ascii=False), encoding="utf-8")

    def bad(self, message):
        self.save()
        with self.assertRaisesRegex(Invalid, message):
            validate(self.root)

    def test_examples(self):
        self.assertEqual(validate(self.root)["individus"], 9)
        self.assertEqual(validate(ROOT / "examples/minimal/Classement")["documents"], 0)

    def test_schema_equivalence_and_validity(self):
        for name, expected in generate_schemas.schemas().items():
            folder = ROOT / "schemas/0.1.0"
            schema = load(folder / f"{name}.schema.json")
            self.assertEqual(schema, expected)
            self.assertEqual(schema, load(folder / f"{name}.schema.yaml"))
            Draft202012Validator.check_schema(schema)

    def test_duplicate_identifier(self):
        item = copy.deepcopy(self.manifest["sources"][0])
        item["titre"] = "Autre titre"
        self.manifest["sources"].append(item)
        self.bad("identifiant dupliqué")

    def test_missing_reference_person(self):
        self.manifest["personne_reference"] = "P999999"
        self.bad("personne de référence absente")

    def test_unknown_version(self):
        self.manifest["version"] = "0.2.0"
        self.bad("Schéma collection")

    def test_unknown_field(self):
        self.manifest["soruces"] = []
        self.bad("Schéma collection")

    def test_nested_folder(self):
        self.manifest["individus"][0]["dossier"] = "parent/enfant"
        self.bad("à plat")

    def test_missing_summary(self):
        (self.person.parent / "LISEZ-MOI.md").unlink()
        self.bad("résumé absent")

    def test_both_person_serializations(self):
        self.person.with_suffix(".json").write_text(json.dumps(load(self.person)), encoding="utf-8")
        self.bad("exactement un")

    def test_both_manifest_serializations(self):
        (self.root / "collection.yaml").write_text(yaml.safe_dump(self.manifest), encoding="utf-8")
        self.bad("exactement un")

    def test_fiche_id_mismatch(self):
        data = load(self.person)
        data["id"] = "P999999"
        self.person.write_text(yaml.safe_dump(data), encoding="utf-8")
        self.bad("fiche/index différent")

    def test_invalid_revision_date(self):
        data = load(self.person)
        data["revision"] = "2026-02-30"
        self.person.write_text(yaml.safe_dump(data), encoding="utf-8")
        self.bad("Schéma individu")

    def test_alias_collision(self):
        data = load(self.person)
        data["alias_codes"] = ["11"]
        self.person.write_text(yaml.safe_dump(data), encoding="utf-8")
        self.bad("code dupliqué")

    def test_invalid_code(self):
        data = load(self.person)
        data["alias_codes"] = ["111.U1.1"]
        self.person.write_text(yaml.safe_dump(data), encoding="utf-8")
        self.bad("Schéma individu")

    def test_missing_source(self):
        self.manifest["documents"][0]["source_id"] = "S999999"
        self.bad("source du document absente")

    def test_missing_person_in_document(self):
        self.manifest["documents"][0]["personnes"].append("P999999")
        self.bad("personne du document absente")

    def test_missing_file(self):
        self.manifest["documents"][0]["chemin"] = "_archives/absent.txt"
        self.bad("document absent")

    def test_modified_bytes(self):
        with (self.root / "_archives/acte-fictif.txt").open("ab") as stream:
            stream.write(b"alteration")
        self.bad("empreinte incorrecte")

    def test_traversal(self):
        self.manifest["documents"][0]["chemin"] = "../secret.txt"
        self.bad("SGAN-008")

    def test_unsafe_paths(self):
        for path in ["/tmp/a", "C:/a", "a\\b", "a/../b", "a//b", "a/./b", "CON.txt", "a.", "a ", "a:b", "a/COM1"]:
            with self.subTest(path=path), self.assertRaises(Invalid):
                safe_path(self.root, path)

    def test_inventory_mismatch(self):
        (self.person.parent / "inventaire.csv").write_text("document_id,role\n", encoding="utf-8")
        self.bad("inventaire divergent")

    def test_inventory_duplicate(self):
        with (self.person.parent / "inventaire.csv").open("a", encoding="utf-8") as stream:
            stream.write("D000001,autre role\n")
        self.bad("document répété")

    def test_missing_relation_endpoint(self):
        self.manifest["relations"][0]["de"] = "P999999"
        self.bad("extrémité de relation absente")

    def test_self_relation(self):
        self.manifest["relations"][0]["de"] = "P000001"
        self.bad("autorelation")

    def test_parent_cycle(self):
        self.manifest["relations"].append({"id": "R999999", "de": "P000001", "vers": "P000002", "type": "parent_biologique", "assertions": []})
        self.bad("cycle de filiation")

    def test_symmetric_partner_duplicate(self):
        self.manifest["relations"].append({"id": "R999999", "de": "P000003", "vers": "P000002", "type": "partenaire", "assertions": []})
        self.bad("relation dupliquée")

    def test_missing_assertion(self):
        self.manifest["relations"][0]["assertions"] = ["A999999"]
        self.bad("assertion de relation absente")

    def test_unrelated_assertion(self):
        self.manifest["relations"][0]["assertions"] = ["A000002"]
        self.bad("sans les deux sujets")

    def test_missing_citation_source(self):
        self.manifest["assertions"][0]["citations"][0]["source_id"] = "S999999"
        self.bad("source de citation absente")

    def test_unsupported_evidence(self):
        self.manifest["assertions"][0]["citations"] = []
        self.bad("Schéma collection")

    def test_whitespace_analysis(self):
        self.manifest["assertions"][0]["analyse"] = "  "
        self.bad("Schéma collection")

    def test_json_duplicate_keys(self):
        self.path.write_text('{"standard":"SGAN","standard":"autre"}', encoding="utf-8")
        with self.assertRaisesRegex(Invalid, "clé dupliquée"):
            validate(self.root)

    def test_yaml_duplicate_keys(self):
        self.person.write_text("id: P000001\nid: P000002\n", encoding="utf-8")
        self.bad("clé dupliquée")

    def test_yaml_outside_json_subset(self):
        path = Path(self.temp.name) / "test.yaml"
        for text in ["date: 2026-11-13", "ok: yes", "x: &a [1]\ny: *a", "x: !!str 1", "x: .inf", "x: 01", "x: {1: a}"]:
            with self.subTest(text=text):
                path.write_text(text, encoding="utf-8")
                with self.assertRaises((Invalid, yaml.YAMLError)):
                    load(path)

    def test_orphan_folder(self):
        (self.root / "999 Orphelin").mkdir()
        self.bad("non déclaré")

    def test_hidden_nested_fiche(self):
        folder = self.root / "_archives/cache"
        folder.mkdir()
        shutil.copyfile(self.person, folder / "fiche_individu.yaml")
        self.bad("imbriquée ou cachée")

    def test_symlink_escape(self):
        link = self.root / "_archives/lien.txt"
        try:
            link.symlink_to(self.path)
        except OSError:
            self.skipTest("Création de liens symboliques non autorisée sur ce système")
        self.bad("lien symbolique")

    def test_cli_exit_status(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/validate.py"), str(self.root)], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.manifest["version"] = "invalid"
        self.save()
        result = subprocess.run([sys.executable, str(ROOT / "tools/validate.py"), str(self.root)], capture_output=True)
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
