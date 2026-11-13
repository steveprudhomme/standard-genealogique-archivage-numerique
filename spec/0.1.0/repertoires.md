# Dossiers individuels à plat — Draft 0.1.0

Chaque dossier individuel DOIT être enfant direct de la collection. Ne pas créer
de dossier d’ancêtre à l’intérieur de celui d’un descendant. L’index du manifeste
associe chaque `P` à son dossier ; les dossiers auxiliaires commencent par `_`.
Le nom d’un dossier est `<code principal> <libelle>`, par exemple
`11 Exemple_Basile`. Le libellé peut conserver les accents ; le nom complet
canonique reste dans la fiche, indépendamment des adaptations du nom de fichier.

## Minimum obligatoire

- `fiche_individu.yaml` **ou** `fiche_individu.json`, jamais les deux : version,
  identifiant, code, alias, nom d’affichage, variantes, statut vital, notes et
  date de révision. Les liens sont centralisés dans le manifeste.
- `inventaire.csv` : UTF-8, séparateur virgule, guillemets CSV usuels, en-tête exact
  `document_id,role`. Un inventaire sans document contient seulement cet en-tête.
  Le rôle libre non vide décrit le lien (par exemple « personne citée »).
  Les autres métadonnées restent dans le manifeste pour éviter les divergences.
- `LISEZ-MOI.md` : résumé humain non vide, avec les inconnues, l’état de recherche
  et les renvois utiles. Ce texte ne remplace pas les données structurées.

## Catégories facultatives

Créer seulement les catégories qui contiennent des fichiers :

| Répertoire conseillé | Contenu |
|---|---|
| `00_Identification` | Variantes de noms, signatures |
| `01_Etat_civil` | Naissance, baptême, mariage, décès |
| `02_Famille_et_relations` | Filiation, adoption, contrats familiaux |
| `03_Residences_et_recensements` | Recensements, déplacements |
| `04_Etudes_et_professions` | Études, métiers, associations |
| `05_Service_militaire` | Service et décorations |
| `06_Photographies` | Portraits, albums |
| `07_Correspondance` | Lettres, cartes, courriels historiques |
| `08_Biens_et_patrimoine` | Actes notariés, successions |
| `09_Recherches_genealogiques` | Transcriptions, notes de recherche |
| `10_Autres_documents` | Autres pièces décrites |

Un document partagé peut être conservé dans `_archives/`, en respectant son fonds
et sa provenance, puis référencé par plusieurs inventaires. Pas de copie maîtresse
multiple ni de lien symbolique nécessaire. Une copie de consultation éventuelle
reçoit une nouvelle notice documentaire ; la relation de dérivation est décrite
dans sa provenance en attendant un modèle structuré.

## Portabilité

Utiliser `/` dans les chemins du manifeste. Interdire les chemins absolus,
`..`, `.`, composants vides, `:`, `\\`, caractères de contrôle et `< > " | ? *`.
Interdire les noms Windows réservés (`CON`, `PRN`, `AUX`, `NUL`, `COM1` à `COM9`,
`LPT1` à `LPT9`, même avec extension), les points/espaces finaux et les liens symboliques.
Deux chemins ne doivent pas entrer en collision après normalisation Unicode NFC
et comparaison sans casse. Le validateur contrôle ces collisions pour toute
l’arborescence. Réduire la longueur totale des chemins selon les outils utilisés ;
aucune limite universelle n’est garantie par le brouillon.

Une fiche JSON et son équivalent YAML ne doivent pas cohabiter dans un dossier.
Les dates doivent être des chaînes entre guillemets en YAML. Le sous-ensemble
accepté est celui des types JSON ; pas de tags personnalisés, ancres, clés dupliquées
ou valeurs implicites propres à YAML telles que `yes` et dates non citées.
