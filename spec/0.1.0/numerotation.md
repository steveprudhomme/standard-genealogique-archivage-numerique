# Identifiants et numérotation — Draft 0.1.0

## Identité permanente

L’identifiant `P000001` est attribué une seule fois dans la collection, sans
signification familiale. Il NE DOIT PAS être réutilisé pour une autre personne.
Changer de nom ou de personne de référence ne change pas cet identifiant.
Lors d’une fusion future de notices, garder une table de redirection et l’historique ;
le format d’échange de cette table est une question ouverte et n’est pas implémenté.
Le numéro interne RootsMagic et le pointeur GEDCOM ne sont pas cet identifiant.

## Code généalogique principal et alias

Le brouillon retient la **notation longue explicite** comme syntaxe d’échange :

```text
ancetre  = "1" suivi de zéro ou plusieurs caractères "1" ou "2"
isole    = "X" suivi de six chiffres (000001 à 999999)
rang     = entier décimal strictement positif, sans zéro initial
code     = (ancetre | isole) suivi de zéro ou plusieurs segments
segment  = "-D" rang | "-U" rang "-E" rang | "-U" rang "-C" rang
```

| Exemple | Lecture dans la convention proposée |
|---|---|
| `1` | Personne de référence |
| `11`, `12` | Premier et second emplacement parental de l’ascendance sélectionnée |
| `111` | Premier parent de `11` |
| `1-D1`, `1-D1-D1` | Enfant puis petit-enfant selon le registre d’attribution |
| `11-U2-E1` | Enfant associé à la deuxième unité parentale enregistrée de `11` |
| `11-U2-C1` | Premier autre partenaire enregistré dans cette unité |
| `X000001` | Individu non rattaché au sujet par les chemins retenus |

La convention historique « 1 = père, 2 = mère » peut être utilisée pour une
ascendance choisie, mais les emplacements ne codent pas nécessairement le sexe
ni la nature biologique du lien. Ces informations appartiennent aux relations.
La sélection des parents en cas d’adoption ou de filiations concurrentes doit
être expliquée dans le résumé de la collection ; tous les liens restent conservés.
Une modification de parenté exige une révision explicite du code et de ses alias.

Les rangs reflètent **l’ordre d’attribution**, jamais une naissance présumée.
On conserve les rangs existants quand un enfant plus âgé est découvert. Une unité
parentale peut être une relation sans mariage. `U` n’est pas une preuve d’union.
Le code d’une unité seule (`11-U2`) ne désigne pas une personne et n’est pas admis
comme code principal. Les segments `C` et `E` désignent des personnes.

La notation compacte `111.U1.1` et les rangs à zéro initial du prototype
(`-U01-E01`) sont des propositions antérieures ; ils ne passent pas le schéma
0.1.0. Leur adoption éventuelle exige une RFC et une migration documentée.

## Une personne, plusieurs chemins

Une personne apparaissant dans plusieurs branches conserve une seule fiche.
Son code principal reste stable ; les autres chemins se placent dans `alias_codes`.
Tous les codes, principaux comme alias, doivent être uniques dans la collection.
Les relations utilisent exclusivement les identifiants `P`, jamais les codes.
Pour un implexe, un alias peut représenter une seconde position d’ascendance.

Une fratrie ou demi-fratrie est déterminée par les parents effectivement déclarés
et le type de filiation, pas par la ressemblance des codes. Les unions multiples
se décrivent par des relations séparées et les assertions associées.

L’algorithme de choix automatique d’un chemin principal, la gestion structurée des
unités `U` et la preuve que chaque code correspond au graphe sont **ouverts**.
Le validateur vérifie syntaxe et unicité ; il ne déduit pas une parenté du code.
