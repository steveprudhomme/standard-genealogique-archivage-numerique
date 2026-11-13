# Archives, relations et preuves — Draft 0.1.0

## Sources et documents

Une source `S` contient un titre, un dépôt ou détenteur (`null` si inconnu), une
cote (`null` si inconnue) et une provenance explicite. Une source peut décrire un
document non numérisé ou une publication ; elle n’exige pas de fichier local.
Ne pas inventer une cote ni attribuer une archive fictive à une institution réelle.

Un document `D` contient un titre, un chemin local, un SHA-256 hexadécimal minuscule,
une référence de source, une liste non vide de personnes concernées, une provenance,
un énoncé de droits et un accès (`public`, `restreint`, `prive`). Ces champs sont
obligatoires lorsqu’un document est présent. `droits` peut explicitement indiquer
« inconnus — diffusion non autorisée ». Le champ d’accès exprime une intention ;
il ne chiffre pas le fichier et ne change pas les permissions du système.

Conserver les originaux numérisés et enregistrer l’origine d’une transcription.
Ne pas écraser une copie maîtresse lors d’une retouche. Vérifier les empreintes
après copie ; enregistrer les contrôles dans l’historique local de conservation.
Préserver le contexte d’un fonds et les cotes d’origine, même lorsque l’accès se
fait depuis les dossiers individuels. SGAN ne remplace pas une description de fonds.

## Relations

Chaque relation `R` comporte `de`, `vers`, `type` et une liste `assertions`.
`parent_biologique`, `parent_adoptif`, `parent_social` et `parent_indetermine`
vont du parent vers l’enfant ; `partenaire` est un lien symétrique, stocké une seule fois.
Plusieurs types entre deux personnes peuvent coexister si l’analyse les justifie.
Pas d’autorelation. Les filiations, tous types confondus dans ce profil simple,
doivent former un graphe sans cycle. Les restrictions de ce choix restent discutables.
Une relation sans assertion est autorisée au socle mais reste non étayée.
Une relation ne doit citer que des assertions dont les sujets comprennent ses deux extrémités.

## Assertions et citations

Une assertion `A` contient : sujets (`P`), prédicat libre, valeur textuelle,
statut (`hypothese`, `etayee`, `contestee`, `refutee`), analyse et citations.
Une citation indique `source_id`, `localisation` précise dans la source et
`apport` (`soutient`, `contredit`, `contexte`). Une date incertaine se transcrit
dans la valeur (« vers 1900 », « entre 1900 et 1902 ») sans précision inventée.
La normalisation des calendriers et dates est reportée à une RFC.

`etayee` et `contestee` exigent au moins une citation et une analyse non vide.
Le statut est une appréciation motivée, pas une note mathématique de certitude.
Des assertions contradictoires restent séparées, avec leurs sources respectives.
Une absence de résultat doit préciser ce qui a été recherché et dans quel périmètre ;
elle ne démontre pas à elle seule l’absence d’événement.

Le validateur contrôle la présence et la cohérence structurelle de ces champs.
L’évaluation critique des sources, la résolution des contradictions et les
conclusions généalogiques relèvent d’une personne compétente.
