# SGAN — Standard généalogique d’archivage numérique

**Draft 0.4.0 · Projet communautaire non officiel · Dix dossiers et nommage des photographies.**

SGAN propose un classement durable des dossiers généalogiques, une identification
explicite des personnes et une traçabilité des archives, relations et preuves.
Ce texte est une proposition ouverte : il ne constitue pas une norme homologuée
et n’est approuvé ni par FamilySearch, ni par RootsMagic, ni par un organisme de normalisation.

Les dossiers individuels sont tous placés directement sous `Classement/`.
Le code généalogique aide à naviguer ; l’identifiant permanent relie les données.
Un document commun conserve une seule copie maîtresse, référencée par plusieurs personnes.
Cette édition reflète le prototype à **trois fichiers et dix catégories fixes par
individu, même vides**, avec des index CSV à l’extérieur de `Classement/`.
Les références `GEDCOM:Ix` restent provisoires et propres à chaque export.

Les photographies suivent désormais la forme
`<date>_<description>_<document_id>[_<variante>].<extension>`, par exemple
`1948-env_portrait-exemple-aline_D000125.tif`. Voir la
[convention complète](spec/0.4.0/photographies.md) pour les dates inconnues,
photos communes, copies restaurées et références à l’image source.

```text
Paquet/
├── Classement/
│   ├── 1 Exemple_Aline/
│   │   ├── fiche_individu.yaml
│   │   ├── inventaire.csv
│   │   ├── LISEZ-MOI.md
│   │   └── 01_Etat_civil/ … 10_Autres_documents/
│   └── 11 Exemple_Basile/
├── Index/
│   ├── individus.csv
│   ├── familles.csv
│   ├── relations.csv
│   └── chemins_ascendants_alternatifs.csv
├── Documentation/
├── Sources/
└── LISEZ-MOI.md
```

## Commencer

1. Lire la [spécification courante](spec/0.4.0/README.md) et le [nommage photographique](spec/0.4.0/photographies.md).
2. Examiner le [paquet fictif 0.4.0](examples/v0.4.0/Paquet), avec deux personnes et huit mires PNG de démonstration.
3. Constituer votre paquet dans un espace privé en conservant la concordance des fiches, index et export GEDCOM.
4. Valider avec Python 3.11 ou supérieur :

```sh
python -m venv .venv
# Windows PowerShell : .venv/Scripts/Activate.ps1
# Linux/macOS : source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/validate_v040.py examples/v0.4.0/Paquet
python tools/package_v040.py examples/v0.4.0/Paquet exemple-sgan.zip
python tools/validate_v040.py exemple-sgan.zip
python -m unittest discover -s tests -v
```

Le validateur lit un dossier de paquet ou un ZIP sans l’extraire. Il vérifie les
schémas, les dix catégories, références, index, inventaires, empreintes et noms
photographiques. Les dates historiques et l’identité des personnes restent à vérifier.
Il ne prouve ni l’exactitude historique, ni les droits de diffusion, ni l’anonymat.
Tous les exemples de ce dépôt sont **entièrement synthétiques**, sans extraction
d’un arbre réel ni reprise du GEDCOM privé à l’origine des réflexions.

Les anciens paquets à dix dossiers dont les fiches indiquent encore `0.3.0-draft`
peuvent être examinés par `tools/validate_v031.py` avec `--accepter-prototype-03`.
Le lecteur historique signale cette version héritée et ne réécrit pas l’archive.
Le profil courant exige `0.4.0-draft` : voir la [migration 0.4.0](docs/migration-0.4.0.md)
et [l’alignement initial](docs/alignement-0.3.1.md).
Le générateur livré crée seulement l’exemple fictif ; il ne convertit pas un GEDCOM réel.

## Parcourir le projet

| Contenu | Point d’entrée |
|---|---|
| Exigences et conformité | [Spécification Draft 0.4.0](spec/0.4.0/README.md) |
| Noms des photographies | [Dates, descriptions, identifiants et variantes](spec/0.4.0/photographies.md) |
| Identifiants et codes | [Numérotation](spec/0.3.1/numerotation.md) |
| Fiches, index et inventaires | [Données](spec/0.3.1/donnees.md) |
| Dix catégories, archives et preuves | [Archives](spec/0.3.1/archives.md) |
| Échanges avec les logiciels | [GEDCOM et RootsMagic](docs/interop.md) |
| Schémas JSON et représentation YAML | [Schémas](schemas/0.4.0/README.md) |
| Limites des contrôles automatiques | [Conformité](docs/conformite.md) |
| Évolution | [Feuille de route](ROADMAP.md), [questions ouvertes](docs/questions-ouvertes.md), [versions](docs/versionnage.md) |
| Participation | [Contribution](CONTRIBUTING.md), [gouvernance](GOVERNANCE.md), [RFC](rfcs/README.md) |
| Protection des personnes | [Sécurité](SECURITY.md), [code de conduite](CODE_OF_CONDUCT.md) |

## Licences

La spécification et la documentation sont sous **CC BY 4.0**. Le code,
les schémas, les exemples et la configuration sont sous **MIT**.
Voir [LICENSE](LICENSE) pour la répartition précise et les textes complets.
Ces licences ne s’appliquent pas aux archives privées que vous classez avec SGAN.

## Éditions et statut

La [première édition 0.1.0](spec/0.1.0/README.md) est conservée avec ses schémas,
exemples et validateur `tools/validate.py`. Elle proposait une organisation
différente, désormais historique. L’édition 0.3.1 aligne la référence de travail
sur le prototype courant, sans réécrire l’historique ni annoncer une consultation
communautaire achevée. Voir la [RFC 0002](rfcs/0002-alignement-prototype-031.md).
La version 0.4.0 y ajoute le nommage photographique, avec une migration explicite
et la [RFC 0003](rfcs/0003-nommage-photographies.md) ouverte à la discussion.
Aucune compatibilité automatique ou sans perte avec RootsMagic n’est revendiquée.
