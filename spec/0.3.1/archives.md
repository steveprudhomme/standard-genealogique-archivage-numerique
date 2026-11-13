# Dix catégories, archives et preuves — Draft 0.3.1

Chaque personne DOIT avoir les dix répertoires suivants **même vides**.
`00_Identification` est supprimé : l’identité est dans la fiche et le résumé.

| Catégorie | Usage |
|---|---|
| `01_Etat_civil` | Naissance, baptême, mariage, divorce, décès, sépulture |
| `02_Famille_et_relations` | Filiation, adoption, contrats familiaux |
| `03_Residences_et_recensements` | Recensements, domiciles, immigration |
| `04_Etudes_et_professions` | Études, diplômes, emplois |
| `05_Service_militaire` | Service, états militaires, décorations |
| `06_Photographies` | Portraits, albums et reproductions |
| `07_Correspondance` | Lettres, cartes, échanges |
| `08_Biens_et_patrimoine` | Biens, contrats, testaments, successions |
| `09_Recherches_genealogiques` | Hypothèses, transcriptions, recherches |
| `10_Autres_documents` | Autres pièces, avec leur description |

## Préserver les dossiers vides

Les ZIP conformes conservent explicitement les entrées de répertoire vide.
Git ne les versionne pas : les exemples du dépôt utilisent des fichiers `.gitkeep`
sans contenu. Ce sont des marqueurs techniques, pas des pièces à inventorier.
`tools/package_v031.py` les omet du ZIP et y conserve les entrées de répertoire.

## Archives communes et fonds

Conserver une seule copie maîtresse d’une pièce commune et la référencer dans
les inventaires de toutes les personnes concernées. Une pièce peut rester dans
un fonds organisé au niveau du paquet ; ne pas démanteler ce fonds pour satisfaire
un classement par personne. Conserver provenance, cote et institution détentrice.
Une copie de consultation ou transcription ne remplace pas l’original numérique.
Expliquer la dérivation dans les notes et attribuer des notices distinctes.

Les médias externes ne sont pas incorporés automatiquement par la présence d’un
GEDCOM. Les fichiers effectivement collectés doivent être copiés et contrôlés
séparément, dans le respect des droits et conditions de consultation.

## Information, hypothèse, preuve

Les relations issues du GEDCOM sont des données importées, pas une preuve.
Pour une conclusion, consigner les sources, leur localisation, ce qu’elles
soutiennent ou contredisent et le raisonnement. Distinguer absence de source et
source contradictoire. Conserver les recherches non résolues dans les notes et
`09_Recherches_genealogiques` ; citer les pièces dans les inventaires.

Le prototype ne possède pas de registre structuré d’assertions ou de niveaux
de preuve. Le modèle proposé en 0.1.0 peut nourrir une RFC future ; il n’est pas
imposé à ce paquet et aucun niveau « archivistique certifié » n’est annoncé.
SHA-256 contrôle les octets, pas l’authenticité historique d’un acte.

## Confidentialité

Un paquet réel avec son GEDCOM est privé par défaut, même s’il suit un standard
ouvert. Vérifier les personnes vivantes, les notes et les métadonnées avant tout
partage. Le validateur ne détermine ni les droits de diffusion ni l’anonymat.
Les seuls exemples publiés par le projet sont intégralement inventés.
