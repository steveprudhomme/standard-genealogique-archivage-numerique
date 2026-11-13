# Contribuer à SGAN

**Draft 0.3.1 — projet non officiel.** Les contributions en français sont privilégiées.

Ouvrir une issue pour un défaut ou une question. Pour un changement d’exigence,
de code généalogique ou de schéma, suivre le [processus RFC](rfcs/README.md).
Une correction de langue ou de lien peut être proposée directement par pull request.

1. Créer une branche depuis `main`.
2. Décrire le problème, la proposition, son effet sur les collections existantes
   et les alternatives envisagées.
3. Modifier ensemble texte, schéma, exemples et tests lorsque la règle évolue.
4. Installer `requirements.txt`, exécuter `python tools/generate_schemas.py --check`,
   `python tools/profile_v031.py --check`
   et `python -m unittest discover -s tests -v`.
5. Ajouter une entrée sous « À venir » dans CHANGELOG.md et remplir le modèle de PR.

Les exemples soumis doivent être entièrement inventés. Ne joindre ni GEDCOM réel,
ni document familial, ni coordonnées privées, ni captures contenant des personnes réelles.
Une modification de noms ne suffit pas à anonymiser un arbre.

Conserver les dix catégories des exemples 0.3.1 avec leurs marqueurs `.gitkeep`.
Ne pas modifier les schémas des éditions publiées pour faire passer un nouveau profil.

En proposant une contribution, vous confirmez disposer des droits nécessaires et
la publier sous la licence du fichier concerné, selon [LICENSE](LICENSE).
Il n’y a ni cession de droits, ni accord distinct de contribution imposé.
Une référence externe doit être citée sans copier de contenu non autorisé.

Les mainteneurs examinent la cohérence, la simplicité d’usage, la conservation des
données et la couverture des cas limites. Les commentaires doivent viser les idées.
Voir le [code de conduite](CODE_OF_CONDUCT.md).
