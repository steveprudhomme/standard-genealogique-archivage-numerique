# Schémas SGAN Draft 0.3.1

Le schéma `individu` décrit l’objet JSON stocké dans `fiche_individu.yaml`.
Les schémas `*-ligne` décrivent les objets obtenus après lecture des CSV avec
leurs en-têtes : individus, familles, relations, chemins alternatifs et inventaire.
Les représentations `.json` et `.yaml` sont équivalentes (JSON Schema 2020-12).

Génération : `python tools/profile_v031.py` ; synchronisation : même commande
avec `--check`. Le validateur utilise les schémas JSON versionnés sur disque,
sans résolution distante. Les contrôles de concordance, de dossiers et de fichiers
complètent les schémas dans `tools/validate_v031.py`.

La version contractuelle est `0.3.1-draft`. Le mode de lecture du prototype
0.3.0 est une option explicite du validateur, pas un assouplissement du schéma.
