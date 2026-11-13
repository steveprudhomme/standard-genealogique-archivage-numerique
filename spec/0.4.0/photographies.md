# Nommage des fichiers photographiques — Draft 0.4.0

La convention vise des noms lisibles hors de leur dossier, associés à un inventaire
et indépendants des codes généalogiques provisoires. Elle est propre à SGAN ;
aucun organisme externe n’impose cette syntaxe.

## PHOTO-01 — Forme du nom

```text
<date>_<description>_<document_id>[_<variante>].<extension>
```

Trois parties sont obligatoires ; la variante est facultative. Utiliser `_` entre
les parties, `-` entre les mots de la description, et un seul point avant l’extension.
La description contient uniquement lettres latines minuscules sans accent,
chiffres et traits d’union simples entre mots. Pas d’espace, apostrophe, souligné
interne à la description, ni ponctuation supplémentaire.
Les noms propres correctement orthographiés restent dans l’inventaire.

| Situation fictive | Exemple |
|---|---|
| Jour connu | `1948-06-12_portrait-exemple-aline_D000123.jpg` |
| Année connue | `1948_portrait-exemple-aline_D000124.tif` |
| Année approximative | `1948-env_portrait-exemple-aline_D000125.tif` |
| Groupe familial | `1962-08_reunion-famille-exemple_D000126.jpg` |
| Lieu utile | `1975_vacances-famille-exemple-quebec_D000127.jpg` |
| Personne et date inconnues | `sans-date_portrait-femme-non-identifiee_D000128.tif` |

Choisir une description courte : type de photographie, personne principale,
événement et, si utile, lieu. Les listes de personnes, leur position dans l’image,
les incertitudes d’identification et les sources restent dans l’inventaire.
Un code de personne ou de dossier ne remplace pas la description ni le document_id.
La longueur totale doit rester compatible avec les logiciels utilisés ; aucun
nombre de caractères universel n’est garanti.

## PHOTO-02 — Date de prise de vue

La date du nom désigne la prise de vue, jamais la numérisation ou la restauration.

| Forme | Sens |
|---|---|
| `AAAA-MM-JJ` | Date connue au jour près |
| `AAAA-MM` | Mois connu |
| `AAAA` | Année connue |
| `AAAA-env` | Année approximative (« vers ») |
| `AAAA-AAAA` | Intervalle d’années, borne initiale strictement antérieure à la finale |
| `sans-date` | Date inconnue |

Chaque année est comprise entre 0001 et 9999. Mois et jours ont deux chiffres.
Les dates complètes doivent être possibles dans le calendrier grégorien utilisé
pour cette notation. Ne pas inventer un 1er janvier, un jour 00 ou une année précise.
Pour une date exprimée dans un autre calendrier, conserver l’expression source
dans les notes et documenter toute conversion ; sinon employer `sans-date`.
Les formes `-env` et les intervalles sont des conventions SGAN, pas des dates ISO.

Le champ `date` de l’inventaire peut conserver une expression plus riche, par
exemple « vers 1948, estimation d’après l’album ». Sa cohérence avec le nom relève
de la relecture humaine ; le validateur contrôle la forme et les dates impossibles.
La date de numérisation se place dans les métadonnées ou les notes.
Le tri alphabétique facilite la lecture, sans garantir un ordre chronologique
strict entre dates incomplètes, approximatives et inconnues.

## PHOTO-03 — Identifiant stable et inventaire

L’identifiant du fichier est `D` suivi de six chiffres, de `D000001` à `D999999`.
Il correspond exactement au `document_id` de l’inventaire, est unique pour un
fichier dans tout le paquet et n’est jamais réattribué. Ne pas recommencer la
numérotation dans chaque dossier individuel. Les IDs des autres types de documents
conservent le contrat du profil de base ; ne pas réutiliser un de leurs IDs.

L’identifiant demeure inchangé si une recherche corrige la date ou l’identité
représentée. Le nom lisible et les chemins d’inventaire peuvent alors être mis
à jour ensemble, en conservant la correspondance ancien/nouveau nom.

Toute image locale dans `06_Photographies`, y compris ses sous-répertoires, doit
être inventoriée avec cette catégorie. Les images conservées ailleurs et
référencées dans une ligne de catégorie `06_Photographies` suivent également
la convention. Plusieurs inventaires peuvent référencer **le même chemin et le
même identifiant** pour une photo de groupe : une seule copie de référence.
Ils ne doivent pas attribuer plusieurs identifiants au même fichier photographique.

## PHOTO-04 — Originaux et fichiers dérivés

Le fichier de référence peut ne porter aucun suffixe, ou porter `_original`.
Le mot « original » désigne ici le fichier numérique de référence conservé ;
il ne prouve pas l’authenticité historique du support photographique.

Les variantes suivantes sont définies :

| Variante | Usage |
|---|---|
| `original` | Fichier numérique de référence |
| `recto`, `verso` | Numérisations distinctes des faces d’un support |
| `consultation` | Copie destinée à la consultation |
| `restauree-v01` | Restauration, version 01 |
| `colorisee-v01` | Colorisation, version 01 |
| `recadree-v01` | Recadrage, version 01 |

Les indices de version ont au moins deux chiffres : 01 à 09, puis 10…100.
Chaque fichier dérivé, nouvelle version, autre face ou autre format reçoit un
document_id distinct. Ne pas écraser le fichier de référence.

```text
1948-env_portrait-exemple-aline_D000125.tif
1948-env_portrait-exemple-aline_D000129_restauree-v01.jpg
1948-env_portrait-exemple-aline_D000130_colorisee-v01.jpg
```

Pour `consultation`, `restauree`, `colorisee` ou `recadree`, la colonne `notes`
doit contenir `derive_de=Dxxxxxx`, désignant le fichier image source immédiat,
conservé localement et présent dans les inventaires. Cette déclaration compacte
permet le contrôle sans ajouter de colonne CSV. Un seul parent immédiat est prévu
dans ce profil ; les montages à plusieurs sources restent à définir.
Pas de référence vers soi-même ni de cycle entre dérivés.

Exemple de note : `derive_de=D000125; restauration du contraste, sans autre modification.`
Conserver une description des opérations et, si connue, leur date.
Pour recto/verso, attribuer deux IDs et expliquer dans les notes qu’ils appartiennent
au même support ; aucune relation de dérivation n’est déduite entre les deux faces.

## PHOTO-05 — Formats et traçabilité

L’extension correspond au format réel et s’écrit en minuscules. Un simple
renommage d’extension n’effectue aucune conversion. Les contrôles automatiques
couvrent : jpg, jpeg, tif, tiff, png, heic, heif, dng, cr2, cr3, nef, arw, raf,
orf, rw2, pef, srw, raw, avif, webp, jxl, gif et bmp. Cette liste n’est ni une
recommandation de format de conservation ni une garantie de décodage.

Les fichiers annexes (XMP, notes, index, `.gitkeep`) ne sont pas des photographies
et ne reçoivent pas automatiquement un ID d’image. Les formats non couverts
nécessitent un examen manuel et éventuellement une extension du profil.
Le validateur ne décode pas les images et ne prouve pas l’accord extension/contenu.

Le nom reçu d’origine DEVRAIT être conservé dans les notes, par exemple
`nom_original=IMG_4827.JPG`, ou dans des métadonnées documentées. S’il est inconnu,
l’indiquer sans inventer une valeur. Garder également la provenance et le SHA-256
du fichier conformément au profil de base. Renommer un fichier ne change pas son
empreinte ; retoucher ses pixels ou métadonnées intégrées peut la changer.

## Fondement et limites

Les recommandations de noms descriptifs, cohérents et uniques sont exposées par
les [Archives nationales américaines](https://www.archives.gov/files/preservation/formats/pdf/naming-and-organizing-files.pdf).
La [Library of Congress](https://digitalpreservation.gov/personalarchiving/photos.html)
recommande aussi de décrire et inventorier les photographies personnelles.
L’ordre des champs, les dates incertaines et les IDs ci-dessus sont des décisions
SGAN. Une validation réussie n’atteste ni la date historique, ni l’identité des
personnes, ni les droits de diffusion.
