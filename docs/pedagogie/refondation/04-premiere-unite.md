# Proposition détaillée U01 — Commander n’est pas déplacer

**Document de conception, pas leçon rédigée.** Durée cible : 20 minutes, avec une marge maximale à tester jusqu’à 25 minutes. Aucun support apprenant, dialogue, énoncé final, corrigé distribuable ou nouvelle activité applicative n’est généré ici. La réalisation et l’essai attendent l’accord du commanditaire.

## Problème à résoudre et résultat attendu

Comprendre qu’un système peut produire la même commande à deux instants et obtenir deux résultats différents parce que le déplacement est possible depuis une position et bloqué depuis l’autre. La carte reste fixe. L’unité ne cherche pas encore à définir tous les agents, expliquer les LLM, classer des architectures ou programmer une politique complète.

Capacité centrale : sur une courte trace, distinguer la commande choisie et la position obtenue, puis expliquer un refus sans l’attribuer à un changement de décision. Une seconde production sur un cas inédit devra montrer que l’apprenant n’a pas seulement mémorisé « deux commandes, un déplacement ».

## Périmètre scientifique et convention locale

Utiliser le cas déterministe connu du laboratoire : première commande droite acceptée, seconde commande droite refusée devant le mur. Le moteur vérifie le déplacement ; la règle garde le même choix de direction. Pour éviter une surcharge, employer au départ commande, position avant, position après et refus. Les termes politique et transition pourront être nommés après compréhension, sans être exigés au billet de sortie.

Le matériel à concevoir devra distinguer ce qui est observé dans le journal de ce qui est établi par lecture de la règle. Voir le même mot deux fois ne suffit pas à prouver que la règle choisit toujours droite. On ne conclut ni à une perception physique du robot, ni à une intelligence générale. La carte et la cible sont des données du modèle.

## Prérequis réellement nécessaires

Savoir repérer une case puis sa voisine à droite, comparer deux positions et lire une ligne courte. Python, tuples, dictionnaires, assertions, mémoire et notation mathématique ne sont pas requis. Le contrôle initial doit distinguer difficulté de lecture de coordonnées et difficulté de raisonnement ; une réponse en mots ou par désignation de cases sera recevable.

Prévoir un bref soutien sur le repérage avant l’essai si nécessaire. Ne pas transformer un diagnostic de trois minutes en épreuve d’entrée à Python. La préparation technique (navigateur et serveur ouverts) se fait avant les vingt minutes et son coût est relevé séparément.

## Déroulement proposé, non encore produit

| Temps | Intention et activité à concevoir après accord | Trace de compréhension à recueillir | Aide et limite |
|---|---|---|---|
| 0–3 min | Installer le repère spatial et la différence entre demander un mouvement et le constater ; vérifier la lecture d’une ligne | Une désignation de la case avant/après, sans jargon requis | Aide de lecture possible ; aucun résultat de l’expérience donné à l’avance. |
| 3–5 min | Faire prédire le premier mouvement, puis justifier ce qui pourrait empêcher la commande d’aboutir | Prédiction individuelle courte, fixée avant le lancement | Le professeur reformule la consigne, pas le mécanisme attendu. |
| 5–8 min | Exécuter un premier pas dans le laboratoire existant et rapprocher commande et position | Première ligne de trace avec trois éléments distingués | Une ligne complétée collectivement sert d’exemple guidé. |
| 8–11 min | Prédire puis exécuter le deuxième pas, sans changer la règle ; comparer aux attentes | Seconde ligne renseignée par l’élève et explication initiale du refus | Ne pas fournir immédiatement la phrase de synthèse. |
| 11–14 min | Mettre en relation les deux tentatives et examiner deux explications concurrentes | Identification de la commande conservée et de la vérification qui empêche le mouvement | Relance sur une donnée du journal ; noter si l’explication n’est obtenue qu’avec aide. |
| 14–18 min | Proposer une courte situation de transfert différente, sans rejouer le cas appris | Prédiction et justification individuelles d’un déplacement accepté ou refusé | Situation sur table à concevoir ; aucune nouvelle carte graphique n’est promise. |
| 18–20 min | Recueillir un bilan individuel puis une mise en mots du mécanisme | Explication personnelle du refus, sans nouveau vocabulaire imposé | Ne pas valider sur récitation de la synthèse finale ; critères dans le document de validation. |

Cette proposition inclut le temps de réponse et de discussion ; elle n’ajoute pas une fiche complète en devoir. Si les réponses nécessitent plus de 25 minutes, revoir le dispositif au lieu de comprimer la phase d’explication ou de supprimer le transfert.

## Usage envisagé de l’application existante

Pour un premier essai accompagné, l’enseignant peut préparer le laboratoire indépendant sur la politique gloutonne et réinitialiser avant l’arrivée de l’apprenant. Seuls le pas à pas, la position et le journal sont nécessaires. Le fonctionnement automatique, BFS, la console Python et le score du bilan existant ne servent pas à valider cette unité. Aucun contrôle n’est supprimé ou modifié dans cette mission.

Cette possibilité n’est pas annoncée comme une unité déjà intégrée. Si les contrôles non utilisés distraient les apprenants ou rendent le premier essai impraticable, il faudra décider explicitement d’un support adapté ; aucune modification d’interface n’est présumée autorisée. Un essai accompagné ne validera pas à lui seul un parcours autonome.

## Approfondissement enseignant associé

Après le même phénomène, travail de préparation distinct : expliquer les responsabilités de la règle et de l’environnement ; construire un cas où une commande identique n’a pas le même effet ; distinguer ce que la trace suffit à établir de ce qui requiert le code ; proposer une relance pour un élève qui attribue le refus au choix du robot.

Production attendue pour juger cet approfondissement : modèle verbal ou tableau, hypothèses du cas, analyse d’une explication erronée et justification de la relance. La formalisation par fonction de transition n’est pas un prérequis de l’unité commune ; elle pourra être introduite après ces productions, si utile au niveau du groupe. Ce travail ne s’ajoute pas silencieusement aux vingt minutes élève.

## Erreurs à surveiller et remédiation à préparer

| Erreur possible | Indice observable | Remédiation envisagée après accord | Nouvelle preuve nécessaire |
|---|---|---|---|
| Commande confondue avec mouvement | Compte deux déplacements parce que deux commandes sont présentes | Comparer uniquement les cases avant et après chaque ligne | Cas nouveau où une commande est refusée. |
| Refus attribué à un changement de choix | Explique que le robot « a décidé de rester » malgré la commande droite | Localiser séparément le mot commandé et le résultat vérifié | Reformulation sur un autre refus, sans vocabulaire imposé. |
| Explication par intention ou surprise | Répond « il a compris » sans citer une donnée | Revenir à une prédiction susceptible d’être démentie | Prédiction justifiée sur le transfert. |
| Difficulté de coordonnées | Raisonnement cohérent en désignant les cases, erreurs de tuples | Autoriser désignation et mots, puis reprise du repérage dans une étape distincte | Ne pas confondre cette difficulté avec la compréhension commande/effet. |

## Arbitrages soumis à accord

Valider ou amender : objectif unique ; départ par l’expérience sans programmation ; place de l’exemple guidé ; nature du transfert ; distinction pilote accompagné/parcours autonome ; preuve attendue pour les enseignants ; critères d’arrêt et de remédiation. Cette proposition ne vaut accord ni sur sa rédaction ni sur son intégration.
