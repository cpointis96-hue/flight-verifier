# Flight verification fallback core

Prototype Python d’orchestration de vérification de vols. Il définit des contrats de données,
une chaîne de repli et un adaptateur de compagnie testé sur des fixtures locales.
Il ne recherche pas encore de vols en direct et ne permet pas de réserver.

Le projet explore la séparation entre découverte d’un vol, preuve provenant d’une compagnie,
gestion des erreurs et intervention humaine. Les couches Playwright, Chrome/Patchright,
Camoufox et Computer Use sont une architecture prévue, pas des intégrations déjà livrées.

## Architecture

Le flux prévu est :

1. un `DiscoveryProvider` — Google Flights MCP — produit des `FlightCandidate` ;
2. `FallbackOrchestrator` essaie les couches injectées dans l’ordre : données structurées,
   réseau ciblé, Playwright déterministe, Chrome/Patchright, Camoufox, explorateur léger,
   puis Computer Use ;
3. un adaptateur officiel transforme la réponse de la compagnie en `VerificationResult` ;
4. une erreur bornée passe à la couche suivante ; une demande d’intervention humaine arrête
   immédiatement le parcours.

Chaque couche est appelée une seule fois par défaut. Les erreurs sont conservées dans
`VerificationResult.attempts`, ce qui évite les boucles silencieuses et permet de distinguer
une absence de preuve d’un billet non remboursable.

## Adaptateurs

`flight_verifier.adapters.SriLankanAdapter` illustre la frontière compagnie. Il reçoit un
`OfficialSiteClient` injecté : le client réel pourra utiliser une requête structurée ou un
navigateur déterministe, tandis que les tests utilisent uniquement un fixture local.
Une nouvelle compagnie doit suivre ce même contrat et sauvegarder ses sélecteurs, règles et
preuves dans son adaptateur.

Le projet ne contient volontairement pas encore de client réseau vivant : les URLs, les
sélecteurs et les conditions tarifaires doivent être observés sur le site officiel de chaque
compagnie avant d’être codés. Un CAPTCHA ou une étape obligatoire d’identité est un arrêt
propre, pas un signal pour contourner le contrôle.

## Installation et exécution

Python 3.10 ou plus récent suffit ; le code courant utilise uniquement la bibliothèque standard.
Télécharger les sources avec **Code → Download ZIP**, extraire l’archive et se placer à sa racine.

```sh
python3 -m examples.demo
```

L’exemple imprime un résultat JSON provenant du fichier de test. `demo_only: true` et
`live_site_checked: false` signalent qu’aucun site aérien n’a été interrogé. Le champ
`result.verified` décrit l’acceptation du payload par l’adaptateur : il ne prouve pas qu’un
tarif existe aujourd’hui. Les conditions et montants de la fixture ne sont pas des offres
actuelles à utiliser pour acheter un billet.

## Validation

Depuis la racine du projet :

```bash
python3 -m unittest discover -s tests -v
```

Cette commande valide les contrats et le mapping fixture-backed. Elle ne prouve pas le
fonctionnement d’un site aérien en direct ; cette validation devra être menée séparément avec
un client officiel réel, des locators ciblés, des timeouts bornés et une trace de source.

Les six tests locaux passent dans la copie préparée pour le portfolio. Voir
[VERIFICATION.md](VERIFICATION.md) pour leur portée exacte.

## Organisation

- `flight_verifier/models.py` : demandes, candidats, preuves et résultats.
- `flight_verifier/discovery.py` : contrat du fournisseur de découverte.
- `flight_verifier/orchestrator.py` : ordre des couches et arrêt de la chaîne.
- `flight_verifier/adapters/` : contrat du client officiel et mapping SriLankan.
- `tests/` : validation des modèles, du mapping et du repli.
- `examples/demo.py` : essai entièrement local sur la fixture.
- `docs/superpowers/plans/` : plan d’architecture initial.

Un skill tiers de recherche Google Flights est conservé dans `.agents/skills/google-flights/`,
avec sa licence MIT et son attribution à [skillhq/flight-search](https://github.com/skillhq/flight-search).
Il s’agit d’instructions pour un agent, pas du client réseau de cette bibliothèque et pas
d’un composant écrit pour ce projet. Il n’a pas été exécuté lors de la validation locale.

## État et prochaine étape

Statut : socle de bibliothèque testé, intégration externe inachevée. Il n’y a ni interface
graphique, ni serveur MCP, ni client Google Flights, ni navigateur automatisé dans le code
livré. Une capture d’interface web ne serait donc pas représentative de ce dépôt.

Pour poursuivre, implémenter un client `OfficialSiteClient` pour une seule compagnie à partir
de son parcours observé, conserver la preuve et sa date, puis tester ce client séparément
des fixtures. Raccorder ensuite un `DiscoveryProvider` réel et des couches de repli utiles.
Ne pas interpréter une absence de preuve comme une règle tarifaire défavorable. Ajouter
des tests couvrant les réponses incomplètes, les changements de schéma et les demandes
d’intervention humaine avant d’étendre à plusieurs compagnies.
