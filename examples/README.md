# Exemples entièrement synthétiques

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
