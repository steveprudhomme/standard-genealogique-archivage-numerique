# RFC 0003 — Noms photographiques lisibles et stables

- Statut : Discussion ; implémentation expérimentale demandée par le responsable
- Édition : Draft 0.4.0
- Décision de travail : convention validée par le propriétaire du projet

## Besoin et proposition

Les noms de photos doivent indiquer date de prise de vue, description et identifiant
documentaire, avec une variante facultative. Le nom reste compréhensible hors du
dossier individuel, tandis que l’inventaire conserve les informations détaillées.

Le [chapitre photographique](../spec/0.4.0/photographies.md) définit dates partielles,
approximatives et inconnues, fichiers dérivés, photos communes et traçabilité.
Les IDs des images sont distincts des références GEDCOM provisoires.

## Compatibilité et tests

La règle rend certains noms anciens non conformes : édition mineure 0.4.0,
schémas distincts et migration documentée, sans renommage automatique.
Les tests couvrent syntaxe, calendrier, inventaire, partage et dérivations.
Les fichiers de référence sont des mires techniques fictives, pas des photos privées.

## Consultation et points ouverts

La demande d’implémentation autorise cette édition de travail ; elle ne constitue
pas une consultation communautaire de 14 jours déjà achevée. L’examen prévu par
la gouvernance reste ouvert. Les montages multisources, les formats complémentaires
et un registre structuré de dérivation pourront faire l’objet de versions ultérieures.
