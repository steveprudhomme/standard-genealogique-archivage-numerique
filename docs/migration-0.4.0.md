# Passer à SGAN Draft 0.4.0

Le changement porte sur le nommage et l’inventaire des images ; la structure à dix
catégories reste celle de 0.3.1. Les archives privées ne sont jamais modifiées par
les validateurs. Le projet ne livre pas de renommage automatique fondé sur une
reconnaissance de personnes ou une date supposée.

1. Travailler sur une copie privée sauvegardée du paquet.
2. Recenser les images dans les dossiers 06 et les images communes référencées.
3. Vérifier les document_id existants : conserver les IDs compatibles et uniques.
   Si un ID doit changer pour respecter les six chiffres, enregistrer explicitement
   la correspondance et mettre à jour toutes ses références avant de le retirer.
4. Relever le nom d’origine, choisir la précision de date justifiée, une description
   courte et une variante lorsque nécessaire. Employer `sans-date` en cas d’inconnu.
5. Renommer chaque fichier une seule fois, puis mettre à jour tous les inventaires
   qui pointent vers lui. Conserver la table ancien chemin/nouveau chemin.
6. Donner un ID distinct à chaque dérivé et consigner `derive_de=Dxxxxxx` dans ses
   notes. Conserver l’image source et les empreintes des fichiers.
7. Après contrôle, passer les fiches à `0.4.0-draft`, actualiser la documentation
   du paquet et lancer `python tools/validate_v040.py CHEMIN_DU_PAQUET`.
8. Créer un ZIP avec `tools/package_v040.py` pour conserver les catégories vides.

Les paquets anciens peuvent continuer à être validés par leurs outils versionnés.
Le lecteur 0.4.0 refuse une fiche déclarant une version antérieure ; changer
uniquement le numéro de version ne suffit pas à garantir la conformité.
Pour les particularités du prototype à dix dossiers encore étiqueté 0.3.0,
voir d’abord [l’alignement 0.3.1](alignement-0.3.1.md).
