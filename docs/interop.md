# GEDCOM et RootsMagic

**Draft 0.1.0 — conception d’interopérabilité, pas un convertisseur livré.**
Le validateur SGAN ne valide pas le contenu d’un GEDCOM. Aucun aller-retour
RootsMagic n’a été exécuté pour cette édition.

## Correspondances envisagées

| SGAN | GEDCOM | Limite |
|---|---|---|
| Personne `P` et nom | `INDI`, `NAME` | Conserver variantes et texte source |
| Identité durable | `UID`, `EXID` ou `REFN` selon profil | Un `P` seul n’est pas global ; préserver l’UUID de collection |
| Filiation et partenariat | `FAM`, `FAMC`, `FAMS` et qualification appropriée | La conversion des types de filiation exige une règle explicite |
| Source et citation | `SOUR`, citation et localisation | Une analyse SGAN ne se réduit pas à un score de qualité |
| Fichier documentaire | `OBJE`, `FILE` | Vérifier les fichiers associés, pas seulement les chemins |
| Assertion de naissance/décès | `BIRT`, `DEAT`, `DATE`, `PLAC`, citations | Les prédicats libres et incertitudes doivent être conservés |

Les pointeurs tels que `@I1@` servent à l’intérieur d’un fichier GEDCOM et ne sont
pas garantis stables après réexport. Conserver une table de correspondance par
export, avec son empreinte, la version déclarée dans `HEAD/GEDC/VERS`, les
identifiants sources et les `P` attribués. Ne jamais rapprocher automatiquement
deux personnes seulement par leur nom ou leur numéro interne.
La [FAQ officielle GEDCOM](https://gedcom.io/techfaqs/) distingue ces pointeurs
des identifiants durables ; la [spécification GEDCOM 7](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)
décrit les structures disponibles. Ce tableau est une proposition SGAN.

GEDCOM 5.5.1 et GEDCOM 7 doivent être traités comme des profils distincts.
Lire la version effectivement exportée. Ne pas supposer qu’un fichier produit
par RootsMagic est un GEDCOM 7. Les extensions spécifiques non interprétées
doivent être conservées dans une copie d’origine privée et signalées dans le rapport.
SGAN n’impose actuellement aucun tag personnalisé `_SGAN`.

## Protocole manuel RootsMagic à exécuter

La [documentation officielle d’export RootsMagic 11](https://help.rootsmagic.com/RM11/exporting-data.html)
décrit l’export GEDCOM, la sélection des personnes, des sources, notes, liens de
médias et options de confidentialité. Ces réglages influencent ce qui est transmis.

1. Créer une nouvelle base exclusivement synthétique ; noter version exacte et système.
2. Inclure adoption, unions multiples, implexe, nom accentué, date approximative,
   source contradictoire, note et média partagé.
3. Exporter via Files / Export Data / GEDCOM File ; consigner toutes les options.
4. Relever la version GEDCOM réellement écrite et vérifier les médias sur disque.
5. Établir la table de correspondance ; convertir seulement les éléments compris.
6. Réimporter dans une base de test distincte, puis réexporter.
7. Comparer personnes, relations, dates, sources, citations, notes, chemins et identifiants.
8. Publier uniquement les résultats synthétiques et la liste précise des pertes.

| Matrice de vérification | État à la publication |
|---|---|
| Documentation GEDCOM 7 consultée | Oui, 2026-11-13 |
| Options d’export RootsMagic 11 consultées | Oui, 2026-11-13 |
| Importateur/exportateur SGAN | Non implémenté |
| Essai pratique RootsMagic | Non exécuté |
| Garantie d’aller-retour sans perte | Aucune |
