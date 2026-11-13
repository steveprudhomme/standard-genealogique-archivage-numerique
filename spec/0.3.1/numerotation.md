# Numérotation et identifiants — Draft 0.3.1

Les codes décrivent les chemins de navigation du prototype. Ils ne sont ni des
identifiants permanents ni la numérotation Sosa classique.

| Forme | Sens dans le prototype |
|---|---|
| `1` | Personne de référence, unique dans le paquet |
| `11`, `12`, `111`… | Ajouter 1 pour le père, 2 pour la mère dans l’ascendance exportée |
| `111-U01-E02` | Deuxième enfant de la première unité parentale rattachée au chemin choisi |
| `1-D01` | Descendant rattaché au chemin de l’individu |
| `1-C01` | Partenaire auquel aucun code principal n’avait encore été attribué |
| `1-C01-P1`, `1-C01-P2` | Parent rencontré hors de l’ascendance directe |
| `X000001` | Personne non rattachée par les chemins exploités lors de la génération |

Les segments peuvent se poursuivre : `111-U01-E02-D01`, `1-C01-P1-P2`.
Les rangs des segments U/E/D/C ont **au moins deux chiffres**, avec un zéro initial
de 01 à 09, puis 10, 11… 100. Zéro n’est pas un rang. Les rangs suivent l’ordre
de parcours des familles et enfants du GEDCOM ; ils ne garantissent pas l’ordre
des naissances. Les chiffres de P sont uniquement 1 ou 2.
Les rôles père/mère reflètent l’export ; ils ne démontrent pas une filiation biologique.

## Chemins alternatifs et marqueur historique `~`

Une personne conserve un seul dossier principal. Les chemins ascendants alternatifs
sont consignés dans `Index/chemins_ascendants_alternatifs.csv` avec son ID GEDCOM,
le code alternatif et le code principal. Le même code ne peut désigner deux personnes.

Le prototype contient également des codes avec `~` suivi de chiffres, parfois
avant d’autres segments. Le lecteur les préserve et les accepte comme des **codes
historiques opaques**. La signification exacte de leurs chiffres, leur génération
et leur propagation ne sont pas établies par la documentation disponible.
Ils ne doivent être ni supprimés ni interprétés comme une parenté supplémentaire.
Le validateur émet un avertissement lorsqu’il les rencontre. Une RFC doit définir
leur éventuel remplacement et une table de correspondance explicite.

## Identité provisoire et stabilisation

Le champ observé `identifiant_permanent_provisoire` vaut `GEDCOM:I…`. Malgré son
nom, il n’est **pas permanent** : il est lié au fichier exporté. La traçabilité
consigne le nom du fichier et son ID de personne sans les délimiteurs `@`.
Le profil reprend ces clés pour lire les paquets existants sans perte.

L’attribution d’UUID indépendants de l’export et la table de correspondance
durable sont des travaux futurs. Ne pas remplacer automatiquement un `GEDCOM:I…`
par un `P…` sans registre de migration. Conserver ensemble le GEDCOM, les index
et les fiches d’une génération ; figer les chemins avant d’ajouter des documents.
Un réexport peut changer les IDs et l’ordre de parcours. Aucun rapprochement par
nom seul, ni renumérotation automatique des dossiers existants, n’est autorisé par
ce profil. Sauvegarder et examiner les changements avant toute reconstruction.
