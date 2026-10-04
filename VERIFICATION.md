# Vérification du socle

Contrôles exécutés le 4 octobre 2026 sur la copie destinée au portfolio.

```sh
python3 -m unittest discover -s tests -v
python3 -m examples.demo
```

Les six tests passent : validation d’une demande invalide, retour antérieur au départ,
mapping d’un payload local, ordre des couches et arrêt au succès, absence de répétition
d’une couche, et arrêt en cas d’intervention humaine.

La démo utilise une fixture JSON locale avec un client injecté. Elle n’exécute aucune
requête réseau. Le mapping fait confiance au client officiel injecté et vérifie la présence
d’une identité tarifaire et d’une URL ; il ne vérifie pas lui-même l’origine de cette preuve.

Aucun site aérien, prix, condition tarifaire actuelle, connecteur MCP ou parcours de
réservation n’a été validé. Aucun compte ni secret n’est nécessaire pour ces tests.
Les notes de recherche de voyage personnelles du dossier initial sont exclues de cette copie.
