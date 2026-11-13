# Versions et publication

La référence courante est **Draft 0.4.0**, tag `v0.4.0-draft`. Les fiches déclarent
`version: "0.4.0-draft"` et `statut: "prototype_non_officiel"`. Le fichier VERSION
du projet contient `0.4.0` ; le statut reste indiqué dans le tag et la documentation.

La contrainte de nommage photographique justifie une nouvelle édition mineure :
certains noms acceptés en 0.3.1 deviennent non conformes. Les tags précédents
restent inchangés ; voir la [migration 0.4.0](migration-0.4.0.md).

La version 0.1.0 reste publiée sans modification de son tag. Le saut à 0.3.1
reprend le nom du prototype de classement pour faciliter le rapprochement ;
aucune publication GitHub 0.2.0 ou 0.3.0 n’est prétendue. Le passage du prototype
0.3.0 au profil à dix dossiers change les contraintes : le chiffre de correctif
est ici hérité du prototype, sans garantie de compatibilité sémantique.

Pour les évolutions futures, suivre MAJEUR.MINEUR.CORRECTIF : pendant 0.x,
une modification incompatible exige une nouvelle version mineure et une migration.
Un correctif corrige les outils ou le texte sans modifier le contrat accepté.
Après 1.0, une rupture exige une version majeure. Une erreur de règle qui invalide
des collections existantes n’est pas une simple correction éditoriale.

Le statut documentaire (Draft, éventuellement Candidate et Stable) ne vaut
jamais homologation. Une publication reste une édition de travail tant que sa
consultation n’est pas achevée ; voir la gouvernance et les RFC.

Pour publier : actualiser VERSION et CHANGELOG, vérifier schémas, exemples et
confidentialité, exécuter la CI, créer un tag annoté et une préversion GitHub.
Ne pas déplacer un tag publié. Les textes et schémas vivent dans leurs répertoires
versionnés. Les migrations doivent préserver les données et expliquer les pertes.
Un nom de fichier ZIP ou de dossier externe ne suffit jamais à déterminer un format.
