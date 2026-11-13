# Alignement sur le prototype 0.3.1

Cette édition prend pour référence l’état fonctionnel décrit dans la conversation
de conception et le paquet 0.3.1 à dix dossiers. L’archive privée a servi à vérifier
la structure ; elle n’est ni versionnée, ni jointe aux publications, ni utilisée en CI.
Les exemples publics sont construits séparément à partir de personnages inventés.

## Écarts corrigés par rapport à 0.1.0

| Sujet | Première publication 0.1.0 | Référence courante 0.3.1 |
|---|---|---|
| Organisation globale | `collection.json` dans Classement | Index CSV, Documentation et Sources au niveau du paquet |
| Fiche individuelle | Identité courte, relations centralisées | Identité, événements, relations, familles et traçabilité dans la fiche |
| Inventaire | Deux colonnes | Onze colonnes documentaires |
| Catégories | Onze catégories facultatives | Dix catégories obligatoires, même vides, sans 00_Identification |
| Rangs des codes | `-D1`, `-U1-E1` | `-D01`, `-U01-E01` ; au moins deux chiffres |
| Partenaires et parents indirects | Proposition différente | Segments `-Cxx`, `-P1`, `-P2` conservés |
| Identifiants | `P000001` présenté comme permanent | `GEDCOM:Ix` explicitement provisoire dans cet export |
| Preuves | Registre d’assertions obligatoire au manifeste | Sources, notes et inventaires ; modèle structuré à discuter |

## Particularités du ZIP de référence

Le paquet nommé 0.3.1 conserve un nom de répertoire externe mentionnant 0.3,
et ses fiches portent encore `0.3.0-draft`. Le nom externe est libre ; les nouvelles
fiches publiées avec ce profil portent `0.3.1-draft`.
La documentation contient aussi une ancienne phrase interdisant les dossiers
vides, en contradiction avec la section ajoutée sur les dix catégories fixes.
L’édition présente retient les dix catégories, cohérentes avec l’arborescence réelle.

Le lecteur fournit `--accepter-prototype-03` pour examiner ces anciennes fiches
en signalant leur version. Cette option ne modifie aucun octet et ne rend pas
automatiquement tout paquet 0.3.0 conforme : les dix dossiers et tous les autres
contrôles restent exigés. Sans cette option, les versions de fiche sont strictes.
Les codes contenant `~` sont préservés avec avertissement, sans sémantique inventée.

## Passer d’un paquet réel à une édition cohérente

1. Conserver intact le ZIP d’origine et travailler sur une copie privée.
2. Vérifier les dix catégories par individu et la concordance des quatre index.
3. Mettre les versions de fiche à `0.3.1-draft` après contrôle, puis corriger les
   phrases documentaires héritées. Ne pas renuméroter ni renommer les personnes.
4. Conserver dates, événements, références GEDCOM et index alternatifs sans perte.
5. Valider en mode strict puis fabriquer un ZIP conservant les répertoires vides.

Un paquet 0.1.0 ne se convertit pas par simple changement de version : les
identifiants, fiches et index diffèrent. Un convertisseur explicite reste à concevoir.
La présente mise à jour ne réécrit pas le ZIP privé de l’utilisateur.

## Portée des vérifications

Le prototype a permis de vérifier l’arborescence, les fiches et la concordance
des relations et familles. Ses inventaires étaient vides : les règles détaillées
de pièces sont testées sur l’exemple synthétique. Aucun import ou réexport
RootsMagic n’a été exécuté. Le projet ne revendique pas un générateur GEDCOM →
paquet reproductible tant que le code du générateur initial n’a pas été établi.
