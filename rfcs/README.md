# Processus RFC

Une RFC est une demande de commentaires sur un changement durable.
Copier [0000-modele.md](0000-modele.md), proposer un numéro libre sur quatre chiffres
et ouvrir une PR liée à une issue de discussion.

Cycle : **Proposee → Discussion → Acceptee / Rejetee / Reportee → Implementee**.
Une proposition retirée prend le statut **Retiree**. Ne pas effacer les décisions.
La discussion dure au moins 14 jours pour un changement normatif. Le mainteneur
consigne les objections, la décision, sa date et les liens de PR. Une acceptation
n’implique pas une implémentation ni une publication immédiate.

Toute RFC indique le besoin, les règles proposées, les cas limites, les effets sur
les données existantes, les alternatives, les tests et les points de confidentialité.
Une modification acceptée est intégrée dans une version annoncée avec migration.
Les décisions sont régies par [GOVERNANCE.md](../GOVERNANCE.md).
