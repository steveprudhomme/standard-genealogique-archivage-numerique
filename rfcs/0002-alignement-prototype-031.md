# RFC 0002 — Aligner la référence de travail sur le prototype à dix dossiers

- Statut : Discussion (implémentation expérimentale disponible)
- Édition de travail : 0.3.1-draft
- Origine : demande explicite du propriétaire de refléter le prototype courant

## Besoin

La première publication avait ajouté un manifeste et une syntaxe de codes qui
ne correspondaient pas au paquet déjà produit. Le nouveau paquet fixe dix catégories
par personne, avec des index globaux et des fiches riches.

## Proposition mise à l’essai

Décrire fidèlement cette organisation, conserver les références provisoires,
ajouter un lecteur de ZIP sans extraction et produire des exemples fictifs.
Ne pas réécrire 0.1.0 ni publier les données privées de référence.

## Arbitrages explicités

La version des fiches nouvelles est harmonisée en 0.3.1-draft ; un mode de lecture
explicite tolère l’ancienne métadonnée. Les dossiers vides sont obligatoires.
Les `~` historiques restent opaques. Les chemins documentaires sont relatifs au
paquet ; ce choix formalise un point que les inventaires vides ne résolvaient pas.

## Compatibilité et discussion

L’implémentation accompagne la demande d’alignement comme édition de travail.
Elle ne constitue pas une décision consensuelle après consultation. Les 14 jours
prévus par la gouvernance restent applicables à son examen communautaire.
Les identifiants durables, règles de génération de codes et preuves structurées
doivent faire l’objet de propositions ultérieures avec migrations explicites.
