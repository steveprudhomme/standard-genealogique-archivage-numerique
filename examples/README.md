# Exemples entièrement synthétiques

La référence courante est [v0.4.0/Paquet](v0.4.0/Paquet) : deux personnes inventées,
huit mires PNG techniques, vingt catégories et une image commune référencée dans
deux inventaires. Les vignettes unies testent les noms et les empreintes ; aucune
photographie de personne réelle n’est incluse. Les suffixes de transformation
décrivent uniquement des scénarios de test.
Génération avec `tools/generate_example_v040.py`, validation avec
`tools/validate_v040.py`, création ZIP avec `tools/package_v040.py`.

## Exemple historique 0.3.1

Le [paquet v0.3.1](v0.3.1/Paquet) conserve dix personnes inventées,
six familles, quatre index, un document partagé et dix catégories par personne.
Les `.gitkeep` conservent les catégories vides dans Git. Le programme
`tools/package_v031.py` crée un ZIP contenant les répertoires sans ces marqueurs.
Le générateur `tools/generate_example_v031.py` reproduit seulement cet exemple.

## Exemples historiques 0.1.0

Ces jeux sont inventés pour le projet, sans reprise d’un arbre ou d’une personne
réelle. Les prénoms usuels ne désignent personne. Aucun GEDCOM privé n’est inclus.

- `minimal/Classement` : une notice sans document, manifeste YAML et fiche JSON.
- `documente/Classement` : neuf notices YAML et manifeste JSON, demi-fratrie,
  unions multiples, adoption, ascendant commun représenté par un alias, individu
  non rattaché, document partagé, source sans fichier et assertion contestée.

Dans la simulation, Basile et Camille ont un ascendant commun : Hortense a les
positions `111` et `121` mais une seule identité. Ce cas artificiel sert à tester
l’implexe. Le code `11-U1-E1` est un alias d’Aline, qui conserve le dossier `1`.

Les deux jeux satisfont le même profil `socle`. Le nom « documente » n’est pas
une certification de niveau supérieur. Les jeux peuvent être régénérés avec
`python tools/generate_examples.py` (cela remplace leurs fichiers de référence).
