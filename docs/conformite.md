# Vérifier un paquet SGAN

## Profil courant 0.3.1

```sh
python tools/profile_v031.py --check
python tools/validate_v031.py examples/v0.3.1/Paquet
python tools/validate_v031.py paquet-prive.zip --accepter-prototype-03
python -m unittest discover -s tests -v
```

La racine attendue contient Classement, Index, Documentation et Sources. Un ZIP
peut ajouter un répertoire englobant de nom libre. Le ZIP est lu sans extraction,
réécriture ni envoi sur le réseau. Aucun chemin privé n’est codé dans les outils
ou la CI. Limites ZIP : 512 Mio décompressés au total, 32 Mio par fichier.
Ce lecteur n’est pas un service d’analyse de contenus hostiles.

| Exigence | Contrôle |
|---|---|
| SGAN031-01 à 03 | Fichiers requis, index complet, une fiche par dossier plat, résumés non vides |
| SGAN031-04 | Exactement les dix catégories immédiates, y compris dans les ZIP |
| SGAN031-05 | Schémas des fiches et des cinq types de lignes CSV ; colonnes exactes |
| SGAN031-06 à 08 | IDs/codes uniques ; identité, dates, relations réciproques et familles concordantes |
| SGAN031-09 | GEDCOM déclaré présent ; identité provisoire liée à sa référence d’export |
| SGAN031-10 | Pièces locales présentes, SHA-256 exact, descriptions partagées concordantes |
| SGAN031-11 | Chemins confinés, noms portables, absence de liens symboliques et de collisions |

Le programme retourne 0 si les contrôles passent et 1 en cas d’erreur. Le rapport
affiche des nombres et avertissements ; les diagnostics de schéma masquent les valeurs.
`--accepter-prototype-03` tolère uniquement la métadonnée de fiche `0.3.0-draft`
avec avertissement. La validation stricte exige `0.3.1-draft`.
Les codes historiques `~` sont acceptés avec avertissement dans les deux modes.

La CI répète les validations des éditions 0.1.0 et 0.3.1 et leurs tests sur
Windows/Ubuntu avec Python 3.11/3.13. Les tests créent uniquement des copies
temporaires fictives : catégorie absente, onzième catégorie, version héritée,
date modifiée, référence manquante, index divergent, fichier altéré, ZIP sans
dossiers vides et tentative de chemin sortant. Les marqueurs `.gitkeep` servent
uniquement à Git et sont retirés par l’outil de création ZIP.
Un test de lien symbolique peut être ignoré si le système interdit sa création.

## Contrôles humains

La concordance entre fichiers ne prouve pas leur exactitude par rapport au GEDCOM
source : le validateur ne parse pas ce dernier. Il ne vérifie pas non plus
l’algorithme d’attribution des codes, la vérité historique, la validité d’une
parenté, les droits de diffusion, les sauvegardes ou l’anonymat.
Les cycles généalogiques et types de filiation doivent être examinés séparément :
le profil 0.3.1 conserve les relations d’export sans leur attribuer de type biologique.
Une source, une citation et une conclusion restent des notions distinctes.

## Édition historique 0.1.0

`python tools/validate.py examples/minimal/Classement` et la variante `documente`
restent disponibles pour l’ancien modèle à manifeste. Ce validateur contrôle
notamment les assertions structurées et les cycles, selon les règles propres
à 0.1.0. Ne pas le lancer sur un paquet 0.3.1 en supposant les formats identiques.
