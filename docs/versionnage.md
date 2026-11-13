# Versions et publication

Les numéros suivent `MAJEUR.MINEUR.CORRECTIF`. Pendant `0.x`, un changement
incompatible nécessite une nouvelle version mineure et des instructions de migration.
Un correctif est éditorial ou corrige un outil sans modifier le contrat accepté.
Une modification des règles qui invalide une collection existante n’est pas éditoriale.
À partir de 1.0, une rupture exige une version majeure.

Le statut documentaire (`Draft`, puis éventuellement `Candidate` et `Stable`) est
distinct du numéro. « Stable » signifie stable dans le projet, jamais homologué.
Cette édition porte `0.1.0`, `Draft`, et le tag Git `v0.1.0-draft`.
Les données déclarent exactement la version des schémas qu’elles utilisent.

Pour publier : clore les décisions nécessaires, mettre à jour VERSION et CHANGELOG,
vérifier les schémas et tests, relire les exemples pour la confidentialité,
committer, attendre la réussite CI, créer un tag annoté et une préversion GitHub.
Une édition publiée ne doit pas être réécrite sous le même tag ; publier un correctif.
Les schémas sont versionnés dans `schemas/<version>/`, la spécification dans
`spec/<version>/`. Les outils courants n’acceptent que 0.1.0 ; pas de migration implicite.
