# Fiches et index — Draft 0.3.1

## Fiche individuelle

`fiche_individu.yaml` contient **un objet JSON en UTF-8**, compatible avec le
sous-ensemble JSON de YAML 1.2, comme dans le prototype. Cette édition n’étend
pas cette forme à toutes les syntaxes YAML. Clés dupliquées et champs inconnus
sont refusés. Une absence d’information reste `null`, une liste vide `[]`.

| Champ | Contenu |
|---|---|
| `standard`, `version`, `statut` | `SGAN`, `0.3.1-draft`, `prototype_non_officiel` |
| `code_genealogique` | Code principal du dossier |
| `identifiant_permanent_provisoire` | `GEDCOM:` suivi de l’ID de personne de cet export |
| `identite` | `nom_complet`, `nom`, `prenoms`, `sexe_gedcom` ; conserver les valeurs source |
| `evenements` | `naissance` et `deces`, chacun null ou objet `date`, `place`, `value` |
| `relations` | Listes `parents`, `partenaires`, `enfants` ; chaque référence contient `code`, `gedcom_id`, `nom` |
| `familles_gedcom` | Listes `enfant_de` et `partenaire_dans` d’IDs de famille |
| `tracabilite` | `fichier_source` (nom simple sous Sources), `identifiant_gedcom`, `methode_numerotation`, `note` |

Les méthodes reconnues sont `reference`, `ascendance`, `branche_familiale`,
`descendance`, `partenaire`, `parent_hors_ascendance`, `non_rattache`.
Le schéma courant reprend les IDs numériques `I…` et `F…` du profil observé ;
il ne prétend pas couvrir toutes les formes de pointeurs permises par GEDCOM.

Les dates GEDCOM incertaines (`ABT`, `BEF`, `AFT`, intervalles…) restent des chaînes
exportées, sans conversion en fausse date exacte. Le champ `value` conserve la
valeur de l’événement (par exemple `Y`) et ne doit pas être perdu.
Un événement absent n’établit pas qu’une personne est vivante.

## Index CSV

Encodage UTF-8, BOM toléré ; séparateur virgule, guillemets CSV pour les champs qui
l’exigent. Les listes de références au sein d’une cellule sont séparées par `;`.
Une liste inconnue ou non renseignée donne une cellule vide. Pas de référence dupliquée.
Les en-têtes suivants et leur ordre sont contractuels :

```csv
code_genealogique,id_gedcom,nom,dossier,methode,naissance_date_source,deces_date_source,parents_gedcom,partenaires_gedcom,enfants_gedcom
```

`Index/individus.csv` : `dossier` est uniquement le nom du dossier sous Classement.

```csv
famille_gedcom,pere_gedcom,mere_gedcom,enfants_gedcom,date_mariage_source
```

`Index/familles.csv` : les parents peuvent être inconnus. Ces colonnes décrivent
les rôles de l’export, pas une conclusion biologique ou une obligation de mariage.

```csv
personne_gedcom,code_personne,type_relation,autre_personne_gedcom,code_autre_personne
```

`Index/relations.csv` : `type_relation` vaut `parents`, `partenaires` ou `enfants`.
`parents` va de la personne vers son parent ; `enfants` va du parent vers son enfant.
Ces deux lignes réciproques sont attendues. Chaque partenariat a deux directions.

```csv
personne_gedcom,code_alternatif,code_principal
```

`Index/chemins_ascendants_alternatifs.csv` peut ne contenir que son en-tête.

## Inventaire individuel

```csv
document_id,categorie,titre,date,chemin_relatif,provenance,cote,url_source,relation,sha256,notes
```

L’inventaire sans pièce contient seulement cet en-tête. Pour chaque ligne :
identifiant, catégorie, titre, provenance et relation à la personne sont renseignés.
Une localisation est nécessaire (chemin, cote ou URL). Les inconnues restent vides.
`categorie` reprend exactement l’un des dix noms de dossiers.

Dans cette formalisation, `chemin_relatif` part de la **racine du paquet**, et non
du dossier de la personne. Cette convention explicite l’origine auparavant non
précisée ; elle n’a pu être inférée des inventaires du prototype, qui étaient vides.
Elle permet de référencer une seule pièce dans plusieurs inventaires sans `..`.
Un fichier local exige une empreinte SHA-256 minuscule de 64 caractères.
Une source sans fichier local peut garder `chemin_relatif` et `sha256` vides.

Le même `document_id` désigne la même pièce dans tout le paquet. Titre, date,
chemin, provenance, cote, URL et empreinte doivent concorder dans les inventaires.
`relation`, `notes` et catégorie peuvent varier selon la personne.
Ces règles de lignes documentaires sont une formalisation à éprouver : leur
fonctionnement est testé sur des pièces synthétiques, pas sur les inventaires vides
du prototype de référence.
