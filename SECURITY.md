# Sécurité et confidentialité

La branche `main`, le profil courant Draft 0.3.1 et le lecteur historique 0.1.0 sont suivis à ce stade,
sans engagement de délai. SGAN décrit des archives potentiellement sensibles.

## Signaler un problème

Pour une faille exploitable, utiliser « Report a vulnerability » dans l’onglet
Security **si cette fonction est disponible**, ou un canal privé affiché sur le
[profil du responsable](https://github.com/steveprudhomme).
Sans canal privé, une issue peut seulement demander un moyen de contact, sans
publier la faille, les données ni les étapes d’exploitation.

Fournir version, système, impact et reproduction synthétique. Ne transmettre aucun
arbre réel. Le mainteneur convient avec le rapporteur d’une correction et d’une
publication coordonnée. Aucun programme de récompenses n’est prévu.

## Utiliser le projet

Le validateur lit les fichiers locaux et ne transmet rien sur le réseau. Il refuse
les chemins absolus, les remontées `..`, les références hors collection et les liens
symboliques détectés. Il n’est pas conçu comme un service d’analyse de fichiers
hostiles : appliquer des limites de ressources et une isolation pour cet usage.
Ne pas exécuter de scripts contenus dans des archives reçues.

Une empreinte SHA-256 détecte une modification ; elle ne prouve ni l’auteur,
ni l’authenticité historique. Sauvegarder séparément et tester la restauration.
La conformité n’autorise pas la publication : vérifier droits, consentement,
personnes vivantes, métadonnées et conditions des institutions détentrices.

En cas de donnée privée commise par erreur, retirer le contenu accessible et
demander au responsable une purge de l’historique et des artefacts concernés.
Changer tout secret divulgué ; un commit de suppression seul ne l’efface pas.
