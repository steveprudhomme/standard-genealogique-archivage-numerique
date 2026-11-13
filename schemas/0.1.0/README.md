# Schémas SGAN Draft 0.1.0

`collection.schema.json` et `individu.schema.json` utilisent JSON Schema 2020-12.
Les fichiers `.schema.yaml` représentent exactement les mêmes objets et ne sont
pas un langage de schéma différent. Le validateur charge les JSON locaux, sans réseau.

`tools/generate_schemas.py` est la source de construction. Régénérer avec
`python tools/generate_schemas.py`, puis vérifier avec `--check` et les tests.
Les champs sont fermés (`additionalProperties: false`) pour détecter les fautes.
Toute extension nécessite une version ou un profil explicitement défini par RFC.

Les contraintes entre fichiers (identifiants uniques, références, graphe,
chemins et empreintes) sont vérifiées par `tools/validate.py`, en complément
du schéma. Le format `date` est vérifié avec un FormatChecker.
