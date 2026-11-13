# SGAN — Standard généalogique d’archivage numérique

**Draft 0.1.0 · 13 novembre 2026 · Projet communautaire non officiel.**

SGAN propose un classement durable des dossiers généalogiques, une identification
stable des personnes et une traçabilité des archives, relations et preuves.
Ce texte est une proposition ouverte : il ne constitue pas une norme homologuée
et n’est approuvé ni par FamilySearch, ni par RootsMagic, ni par un organisme de normalisation.

Les dossiers individuels sont tous placés directement sous `Classement/`.
Le code généalogique aide à naviguer ; l’identifiant permanent relie les données.
Un document commun conserve une seule copie maîtresse, référencée par plusieurs personnes.

```text
Classement/
├── collection.json
├── 1 Exemple_Aline/
│   ├── fiche_individu.yaml
│   ├── inventaire.csv
│   └── LISEZ-MOI.md
├── 11 Exemple_Basile/
├── 12 Exemple_Camille/
└── _archives/
    └── acte-fictif.txt
```

## Commencer

1. Lire la [spécification](spec/0.1.0/README.md) et les [règles de numérotation](spec/0.1.0/numerotation.md).
2. Copier l’[exemple minimal](examples/minimal/Classement) ou l’[exemple documenté](examples/documente/Classement).
3. Remplacer les données fictives dans votre espace privé et conserver les identifiants attribués.
4. Valider avec Python 3.11 ou supérieur :

```sh
python -m venv .venv
# Windows PowerShell : .venv/Scripts/Activate.ps1
# Linux/macOS : source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/validate.py examples/minimal/Classement
python tools/validate.py examples/documente/Classement
python -m unittest discover -s tests -v
```

Le validateur vérifie les schémas, dossiers, références, inventaires et empreintes.
Il ne prouve ni l’exactitude historique, ni les droits de diffusion, ni l’anonymat.
Tous les exemples de ce dépôt sont **entièrement synthétiques**, sans extraction
d’un arbre réel ni reprise du GEDCOM privé à l’origine des réflexions.

## Parcourir le projet

| Contenu | Point d’entrée |
|---|---|
| Exigences et conformité | [Spécification Draft 0.1.0](spec/0.1.0/README.md) |
| Identifiants et codes | [Numérotation](spec/0.1.0/numerotation.md) |
| Dossiers et contenu minimal | [Répertoires](spec/0.1.0/repertoires.md) |
| Archives, relations, raisonnement | [Archives et preuves](spec/0.1.0/archives-relations-preuves.md) |
| Échanges avec les logiciels | [GEDCOM et RootsMagic](docs/interop.md) |
| Schémas JSON et représentation YAML | [Schémas](schemas/0.1.0/README.md) |
| Limites des contrôles automatiques | [Conformité](docs/conformite.md) |
| Évolution | [Feuille de route](ROADMAP.md), [questions ouvertes](docs/questions-ouvertes.md), [versions](docs/versionnage.md) |
| Participation | [Contribution](CONTRIBUTING.md), [gouvernance](GOVERNANCE.md), [RFC](rfcs/README.md) |
| Protection des personnes | [Sécurité](SECURITY.md), [code de conduite](CODE_OF_CONDUCT.md) |

## Licences

La spécification et la documentation sont sous **CC BY 4.0**. Le code,
les schémas, les exemples et la configuration sont sous **MIT**.
Voir [LICENSE](LICENSE) pour la répartition précise et les textes complets.
Ces licences ne s’appliquent pas aux archives privées que vous classez avec SGAN.

## Statut de la première version

`0.1.0` est la première édition publiée du projet. Les mentions `0.2` et `0.3`
des échanges exploratoires antérieurs désignaient des prototypes non publiés ;
elles ne constituent pas des versions officielles de ce dépôt.
Les décisions retenues ici restent révisables par RFC. Aucune compatibilité
automatique ou sans perte avec RootsMagic n’est revendiquée.
