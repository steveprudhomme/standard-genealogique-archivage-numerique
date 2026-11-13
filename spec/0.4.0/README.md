# SGAN Draft 0.4.0 — Nommage des photographies

**Spécification expérimentale non officielle.** Cette édition ajoute la convention
photographique acceptée par le responsable du projet au profil à dix catégories.

## Base normative et changement de version

Les exigences SGAN031-01 à SGAN031-11 et les chapitres
[organisation](../0.3.1/README.md), [numérotation](../0.3.1/numerotation.md),
[données](../0.3.1/donnees.md) et [archives](../0.3.1/archives.md) de 0.3.1 sont
repris dans cette édition, avec deux différences explicites :

1. Les fiches déclarent `version: "0.4.0-draft"` ; les schémas 0.4.0 font référence.
2. Les photographies suivent les exigences PHOTO-01 à PHOTO-05 du
   [chapitre de nommage](photographies.md), qui précisent les règles documentaires.

Les trois fichiers individuels, dix catégories fixes et quatre index CSV sont
conservés. Les IDs GEDCOM restent provisoires ; les identifiants documentaires
des images sont indépendants de ces IDs et des codes généalogiques.

L’ajout d’une contrainte de nommage peut invalider des noms acceptés précédemment :
il justifie une version mineure 0.4.0. Les éditions et outils historiques restent
disponibles. Aucune migration ni renumérotation implicite n’est effectuée.

## Utilisation

```sh
python tools/validate_v040.py examples/v0.4.0/Paquet
python tools/package_v040.py examples/v0.4.0/Paquet exemple-photos.zip
python tools/validate_v040.py exemple-photos.zip
```

Le lecteur vérifie un dossier ou ZIP sans modification. Les exemples contiennent
des mires PNG techniques et des notices fictives, sans photographies réelles.

Lire aussi [la migration](../../docs/migration-0.4.0.md),
les [schémas](../../schemas/0.4.0/README.md) et la
[RFC 0003](../../rfcs/0003-nommage-photographies.md).
