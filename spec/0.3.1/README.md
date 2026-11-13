# SGAN Draft 0.3.1 — Profil à dix dossiers

**Projet de spécification expérimental non officiel.** Cette édition décrit le
classement atteint dans le prototype 0.3.1 : trois fichiers de base et dix catégories
documentaires fixes par individu. Elle remplace 0.1.0 comme référence de travail.
Les anciennes éditions restent consultables ; aucune homologation n’est revendiquée.

## Paquet et arborescence

```text
Paquet/
├── LISEZ-MOI.md
├── Classement/
│   ├── 1 Exemple_Aline/
│   │   ├── fiche_individu.yaml
│   │   ├── inventaire.csv
│   │   ├── LISEZ-MOI.md
│   │   ├── 01_Etat_civil/
│   │   ├── 02_Famille_et_relations/
│   │   ├── 03_Residences_et_recensements/
│   │   ├── 04_Etudes_et_professions/
│   │   ├── 05_Service_militaire/
│   │   ├── 06_Photographies/
│   │   ├── 07_Correspondance/
│   │   ├── 08_Biens_et_patrimoine/
│   │   ├── 09_Recherches_genealogiques/
│   │   └── 10_Autres_documents/
│   └── 11 Exemple_Basile/
├── Index/
│   ├── individus.csv
│   ├── familles.csv
│   ├── relations.csv
│   └── chemins_ascendants_alternatifs.csv
├── Documentation/
│   ├── specification_provisoire.md
│   └── categories_documentaires.md
└── Sources/
    └── exemple-fictif.ged
```

Le nom externe du paquet est libre et ne détermine pas sa version. Tous les
individus sont directement dans `Classement/` ; les index sont au niveau du paquet.
Le manifeste `collection.json` proposé dans 0.1.0 n’est pas requis dans ce profil.

## Exigences du profil

**DOIT** exprime une obligation du présent profil ; **DEVRAIT** une recommandation.
Ces termes n’impliquent aucune obligation légale ou institutionnelle.

| Règle | Exigence |
|---|---|
| SGAN031-01 | Un paquet comporte les quatre index CSV, les deux documents et le LISEZ-MOI racine indiqués ci-dessus. |
| SGAN031-02 | Une personne indexée possède un seul dossier plat `<code> <libelle>` et réciproquement. |
| SGAN031-03 | Chaque dossier comporte une fiche, un inventaire et un résumé non vide. |
| SGAN031-04 | Les dix catégories 01 à 10 sont présentes, même vides ; aucun onzième dossier immédiat `00_Identification`. |
| SGAN031-05 | Fiches et lignes CSV respectent les schémas 0.3.1, y compris l’ordre des colonnes. |
| SGAN031-06 | Codes principaux et identifiants d’export sont uniques ; les références et chemins alternatifs sont résolus. |
| SGAN031-07 | Identité, dates source, relations et appartenances familiales concordent entre fiches et index. |
| SGAN031-08 | Les liens parents/enfants sont réciproques ; les partenaires sont représentés dans les deux sens. |
| SGAN031-09 | Le GEDCOM nommé dans la traçabilité existe sous `Sources/`. Les références restent propres à cet export. |
| SGAN031-10 | Tout fichier local inventorié existe ; son SHA-256 correspond ; les descriptions d’un document partagé concordent. |
| SGAN031-11 | Les chemins sont relatifs au paquet, portables et confinés ; liens symboliques et collisions de casse/Unicode sont refusés. |

Des sous-répertoires peuvent organiser les pièces **à l’intérieur** des dix
catégories. D’autres espaces au niveau du paquet peuvent conserver un fonds ou
des documents communs sans imposer de duplication des pièces.

## Lire les chapitres

- [Numérotation et identifiants provisoires](numerotation.md)
- [Fiches, index et inventaires](donnees.md)
- [Catégories, archives et preuves](archives.md)
- [Migration et écarts du prototype](../../docs/alignement-0.3.1.md)
- [Conformité et limites](../../docs/conformite.md)

Le validateur contrôle la structure et les concordances, pas la vérité généalogique.
Les relations importées ne sont pas qualifiées automatiquement de biologiques.
La stabilisation des identifiants et les profils de preuve avancés restent ouverts.
