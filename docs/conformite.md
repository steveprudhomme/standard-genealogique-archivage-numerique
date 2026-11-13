# Vérifier une collection

La commande `python tools/validate.py CHEMIN/Classement` retourne 0 lorsque les
contrôles du socle Draft 0.1.0 passent et 1 sinon. Le premier défaut structurel
détecté est expliqué ; corriger puis relancer. Les cinq premiers défauts de schéma
peuvent être affichés ensemble. Le validateur utilise uniquement les schémas locaux.

| Exigence | Vérification automatique |
|---|---|
| SGAN-001 | Un manifeste, version et profil connus, types et champs obligatoires |
| SGAN-002 | Dossiers à plat, index complet, noms préfixés, absence de fiche imbriquée |
| SGAN-003 | Fiche unique, résumé non vide, inventaire présent |
| SGAN-004 | Identifiants et alias uniques, concordance fiche/index, références résolues |
| SGAN-005 | Pas d’autorelation, doublon de relation ou cycle parental |
| SGAN-006 | Fichiers présents, un chemin par document, SHA-256 exact |
| SGAN-007 | En-tête CSV, rôles, absence de doublons, concordance des associations |
| SGAN-008 | Chemins portables, confinement, liens, collisions de casse/Unicode |
| SGAN-009 | Citations et analyse des assertions étayées ou contestées |
| SGAN-010 | Types JSON, rejet de clés dupliquées et constructions YAML ambiguës |

`python -m unittest discover -s tests -v` accepte les deux collections de référence
et crée des copies temporaires pour tester les erreurs. Aucun exemple invalide
n’est confondu avec un exemple de référence. Les tests couvrent notamment fichier
altéré, référence absente, filiation cyclique et divergence d’inventaire.
La CI répète les contrôles sur Windows et Ubuntu avec Python 3.11 et 3.13.
Un test de lien symbolique peut être ignoré si le système interdit sa création.

## Contrôles humains obligatoires avant diffusion

Vérifier la pertinence des codes par rapport aux relations, les conclusions
historiques, la fidélité des citations, la provenance et les droits de diffusion.
La déclaration `donnees_synthetiques` est une déclaration de l’auteur, pas un
anonymiseur. Le validateur accepte aussi des collections privées non synthétiques,
mais seuls des jeux entièrement fictifs peuvent être contribués au dépôt public.

Les octets des fichiers déclarés sont vérifiés ; la qualité d’un scan, la lisibilité
d’un format, les sauvegardes et la restauration ne sont pas évaluées automatiquement.
Les fichiers non déclarés peuvent exister (notes ou dérivés de travail) ; une revue
manuelle doit décider s’ils doivent être inventoriés et s’ils peuvent être partagés.
