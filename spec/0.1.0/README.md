# SGAN — Spécification Draft 0.1.0

**Statut : brouillon expérimental non officiel, publié le 13 novembre 2026.**
Les règles ci-dessous définissent uniquement ce profil SGAN. Elles ne sont pas
des obligations émanant d’un organisme de normalisation.

## Portée et vocabulaire

Une **collection** est la racine `Classement/` contenant un manifeste, les dossiers
individuels et éventuellement des espaces auxiliaires préfixés `_`.
Un **individu** est une notice ; son identifiant est permanent dans cette collection.
Une **source** décrit l’origine d’une information ; un **document** est un fichier
numérique local ; une **assertion** exprime une proposition accompagnée de son analyse.
Une **relation** est un lien typé entre notices. Une source n’est pas une preuve
automatique et une relation déclarée n’est pas une conclusion historique garantie.

**DOIT**, **NE DOIT PAS**, **DEVRAIT** et **PEUT** signifient respectivement
exigence, interdiction, recommandation justifiable et possibilité.
Les exemples sont informatifs ; les exigences du présent répertoire sont normatives
uniquement à l’intérieur de ce brouillon. Le schéma formalise les types et champs.
Un désaccord texte/schéma est un défaut à signaler, pas une permission de choisir
silencieusement l’interprétation la plus commode.

## Socle de conformité 0.1.0

| Règle | Exigence |
|---|---|
| SGAN-001 | Un manifeste `collection.json` ou `collection.yaml`, exactement un, conforme au schéma collection. |
| SGAN-002 | Un dossier par individu déclaré, directement sous la racine, nommé par son code principal suivi d’un espace et d’un libellé. |
| SGAN-003 | Chaque dossier contient exactement une fiche `fiche_individu.json` ou `.yaml`, un `inventaire.csv` et un `LISEZ-MOI.md` non vide. |
| SGAN-004 | Identifiants et codes principaux/alias uniques dans la collection ; aucune référence pendante. |
| SGAN-005 | Les relations pointent vers deux personnes distinctes ; les filiations ne forment pas de cycle. |
| SGAN-006 | Chaque document déclaré existe dans la collection et son SHA-256 correspond au fichier. |
| SGAN-007 | L’inventaire de chaque individu contient exactement les documents qui lui sont associés. |
| SGAN-008 | Les chemins sont relatifs, portables, sans lien symbolique, remontée, lecteur ni sortie de collection. |
| SGAN-009 | Les assertions `etayee` ou `contestee` ont au moins une citation et une analyse non vide. |
| SGAN-010 | Les fichiers de données suivent les types JSON ; clés dupliquées, types YAML spécifiques et ancres sont refusés. |

Les contrôles associés sont décrits dans [Conformité](../../docs/conformite.md).
L’évaluation humaine des sources, des droits et de la confidentialité reste nécessaire.
Le profil `socle` est le seul niveau revendicable et validé dans cette édition.
Les appellations « documenté » et « archivistique » sont des objectifs futurs,
pas des certifications ni des niveaux implémentés. L’exemple nommé `documente`
illustre le socle enrichi de documents et d’assertions.

## Modèle d’échange

Le manifeste contient `standard: SGAN`, `version: "0.1.0"`, `statut: Draft`,
`profil: socle`, un UUID de collection, une désignation, une déclaration
`donnees_synthetiques`, la personne de référence (ou `null`), l’index des personnes,
et quatre listes : sources, documents, relations, assertions.
Les listes peuvent être vides. Une collection contient au moins un individu.

Chaque objet utilise un identifiant typé : `P000001`, `S000001`, `D000001`,
`R000001` ou `A000001`, six chiffres exactement, sauf `000000` réservé.
Les références externes utilisent le couple UUID de collection + identifiant local.
`null` signifie inconnu ; une liste vide signifie aucune entrée consignée.
Ne jamais inventer de nom, de date ou de parent pour satisfaire un schéma.
Une notice anonyme utilise un nom d’affichage explicite tel que « Personne inconnue ».

Lire les chapitres [numérotation](numerotation.md), [répertoires](repertoires.md)
et [archives, relations et preuves](archives-relations-preuves.md).
