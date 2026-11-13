# Schémas SGAN Draft 0.4.0

Les schémas de fiches et de lignes CSV reprennent 0.3.1, avec la déclaration de
version `0.4.0-draft` dans la fiche. Le schéma `nom-photographie` décrit un **nom
de fichier**, pas un chemin, selon la syntaxe photographique de cette édition.
Ses fichiers JSON et YAML représentent le même JSON Schema 2020-12.

La syntaxe seule n’écarte pas une date impossible : `tools/photographies.py`
contrôle le calendrier, l’intervalle d’années, la correspondance des IDs et
les liens entre dérivés et sources. `tools/validate_v040.py` applique ces
contrôles aux dossiers ou ZIP après validation de la structure et des inventaires.

Générer avec `python tools/profile_v040.py` ; vérifier avec `--check`.
Les schémas publiés précédemment ne sont pas réécrits.
