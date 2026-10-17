# S02 — Parcours enseignant : information, transition et indiscernabilité

Parcours scientifique distinct du support élève. Dans les mêmes 120 min, remplacer une partie du guidage de programmation par la formalisation et la lecture critique ; fournir les auxiliaires déjà maîtrisés. Les développements optionnels ne doivent pas réduire le TP ni le bilan. Ce document ne constitue pas une séance 03 anticipée sur la construction des architectures à mémoire.

## 1. Modéliser le système avant de lui attribuer une propriété

On distingue le monde de son contrôleur. Le premier exemple utilise une carte `W` et une destination `g` connues et fixes. Pour prévoir un déplacement, la position `p=(x,y)` suffit comme état variable. Dans un modèle complet d’épisode, état terminal et budget restant peuvent aussi être nécessaires. On ne doit pas appeler « état complet » un tuple qui omet une variable gouvernant les effets futurs.

Notations de ce cours : `S` ensemble des états, `Ω` ensemble des observations et `A` ensemble des commandes. `s ∈ S` est un état réel du modèle, `o ∈ Ω` une observation transmise, `a ∈ A` une commande. L’alphabet comprend droite, gauche, haut, bas et arrêt ; il ne comprend pas un mot arbitraire comme voler. Admissibilité du mot et possibilité physique d’un déplacement sont deux validations distinctes.

### Transition déterministe et résultat de commande

`T : S × A → S` associe un état suivant à un état et une commande. Dans la carte fixe, la candidate est obtenue par le déplacement associé ; elle remplace la position seulement si elle est libre. Le refus donne une position inchangée. On peut écrire séparément un résultat `r(s,a)` indiquant accepté, refusé ou arrêt. Le fait que deux commandes différentes puissent donner la même position n’invalide pas le déterminisme.

La fonction Python retourne `(position_apres, resultat)`. Elle n’implémente pas seule une politique et son champ `resultat` n’est pas un score de réussite. Le conducteur du labo arrête l’épisode après un refus ; le TP appelle les transitions isolément. La comparaison doit donc porter sur les étapes annoncées, sans supposer un droit universel de réessai.

### Observation et information accessible

`O : S → Ω` produit l’observation. Une observation complète pour la tâche peut permettre de récupérer les aspects pertinents de l’état ; une observation partielle peut réunir des états nécessitant des comportements différents. La propriété s’apprécie relativement à la tâche et au modèle, pas à la richesse visuelle du dessin.

Dans la grille graphique, le code reçoit carte et cible. Dans le script masqué, l’état retient `(p,c,n)` : position `p`, couleur d’autorisation `c ∈ {bleu, orange}`, nombre de commandes déjà effectuées `n ∈ {0,1,2,3}`. `O` transmet la position et la couleur au départ ; ensuite elle transmet position et indice non visible. Le budget de trois commandes appartient à la tâche et les deux cas sont comparés au même `n=2`. Le script ne possède pas de mécanisme graphique de masquage.

## 2. Déterminisme, hasard et modèle d’information

Une transition déterministe donne une issue unique pour `(s,a)` fixé. Ignorer un mur n’introduit pas du hasard dans cette transition ; c’est une limite de l’information ou de son exploitation. Une distribution de transitions peut se noter `K(s'|s,a)`, où `s'` est un état suivant possible. Chaque valeur est non négative et la somme sur les états suivants vaut 1. Cela décrit l’incertitude du modèle choisi ; la notation n’est pas une explication physique de son origine.

**Instanciation originale du TP** : pour une commande droite vers une case libre, le modèle de glissement affecte une chance sur deux à avancer et une chance sur deux à rester. Devant un mur, les deux tirages donnent le même refus. Le contrôleur choisit toujours droite. `appliquer_avec_glissement(..., tirage)` rend explicite la source du hasard pour vérifier toutes les branches ; `essais_glissement` fournit ensuite des tirages pseudo-aléatoires reproductibles.

Inclure l’état du générateur dans un programme informatique peut rendre sa trajectoire entièrement reproductible. Cela ne contredit pas l’usage d’un modèle stochastique au niveau de description retenu, où cet état n’est pas une donnée du contrôleur. Ne pas confondre cet exercice avec une politique stochastique : celle-ci distribuerait les commandes, alors que l’expérience fixe la commande et varie son effet. Aucun de ces choix ne requiert un LLM.

## 3. Indiscernabilité et contre-exemple réactif

Définissons, pour **une observation instantanée**, `s ~ s'` lorsque `O(s)=O(s')`. C’est une relation d’équivalence induite par la fonction d’observation. Elle ne dit pas que les deux mondes auront les mêmes effets pour toutes les actions futures, ni qu’ils ont le même historique. Elle n’est pas une preuve de bisimulation.

Deux états du script à la bifurcation sont `s_b=((1,1),bleu,2)` et `s_o=((1,1),orange,2)`. Ils sont indiscernables à cet instant : la position est la même et la couleur n’est plus transmise. La tâche autorise respectivement la sortie gauche et la sortie droite. Avec une seule commande restante, les ensembles d’actions permettant la réussite sont disjoints : `{gauche}` et `{droite}`.

Pour une politique déterministe de l’observation seule, `a=π(o)`, l’entrée commune impose la même sortie dans les deux cas. Aucune sortie unique n’appartient aux deux ensembles ; cette politique ne garantit donc pas les deux réussites immédiates. C’est une preuve sur un contre-exemple construit. Elle ne démontre ni l’échec de toutes les politiques réactives sur tous les environnements partiels, ni la suffisance générale de la mémoire.

Historique : `h_t=(o_0,a_0,…,a_(t−1),o_t)`, contenant observations reçues jusqu’à `t` et commandes antérieures. Dans notre parcours imposé, les premières observations distinguent les couleurs, bien que les dernières coïncident. Une politique à historique pourrait utiliser cette information passée. Une mémoire qui conserve la couleur serait suffisante pour ce cas. Sa mise en œuvre est réservée à S03 ; stocker l’histoire ne produit pas à lui seul un modèle exact de l’environnement.

Si l’on supprime le budget, autorise une action d’interrogation ou change le contenu de `O`, il faut refaire l’analyse. Une politique qui relit directement `c` dans l’état caché ne résout pas le problème annoncé : elle change l’information autorisée. Une observation partielle ne doit pas être simulée par un simple cache sur le dessin tandis que le code conserve la carte entière.

## 4. Production enseignant et lecture critique, dans la séance

Production à remettre : (a) définition des états/observations/commandes pour un cas ; (b) trace d’un refus ; (c) paire indiscernable et argument en trois lignes ; (d) une modification des hypothèses qui exige de réexaminer la conclusion.

Lecture courte, 10 min prises sur formalisation/transfert : [Russell–Norvig, extrait de chapitre 2, propriétés des environnements](https://aima.cs.berkeley.edu/4th-ed/pdfs/newchap02.pdf), et [Poole–Mackworth, §2.1, contrôleurs et état de croyance](https://artint.info/3e/html/ArtInt3e.Ch2.S1.html). R1 et R3 du dossier sont reconsultés pour ce jalon ; le PDF Russell–Norvig reste non daté, sans attribution de pagination à la 4e édition. On ne prétend pas avoir lu les ouvrages entiers.

Question critique : « Une observation courante identique signifie-t-elle que l’agent dispose de la même information ? » Réponse : uniquement si on exclut les observations antérieures, la mémoire et les autres canaux d’information. Poole–Mackworth distingue le percept courant de ce qui est conservé par le contrôleur ; la trace du TP permet de mettre cette distinction à l’épreuve. L’extrait Russell–Norvig aide à séparer caractère observable et déterministe : ces axes ne se réduisent pas l’un à l’autre. Ces apports de lecture sont des synthèses ciblées, non des définitions nouvelles attribuées aux auteurs.

Prolongement facultatif : distinguer perte de données, capteur bruité et modèle de transition incorrect. Ne pas charger le parcours NSI d’un calcul de probabilités conditionnelles ; une extension de modèle d’observation stochastique se réservera à une formation ultérieure autorisée.

## 5. Transposition didactique spécifique

| Difficulté | Première | Terminale préparée | Indicateur de compréhension |
|---|---|---|---|
| État = ce qui est affiché | Deux fiches de monde, puis colonnes de données reçues | Fonction d’observation explicite, entrées autorisées | Cite une variable réelle absente de l’observation. |
| Retour = déplacement | Tableau candidat/commande/effet ; fonction auxiliaire fournie | Contrat, exception, tests de bords | Conserve position lors du refus et l’explique. |
| Refus = hasard | Rejouer le même cas | Comparer T et modèle K, sans exiger la notation des élèves | Situe quel composant varie. |
| Masquer = supprimer | Fiche couverte et valeur `None` expliquée | Champs de dictionnaire et deux histoires | Ne conclut pas à l’absence de sortie. |
| Mémoire = accès au monde caché | Conserver sur papier la couleur antérieure | Démonstration d’indiscernabilité instantanée | N’utilise pas l’indice caché dans la décision finale. |
| Réussir = valider la théorie | Demander un autre cas et une limite | Refaire l’analyse si budget/capteur change | Distingue garantie dans le modèle et succès d’un essai. |

Les appuis P1/P2 sont programmation, tests, représentations et modélisation ; les agents, le noyau de transition stochastique et l’indiscernabilité restent des approfondissements du module, pas des rubriques réglementaires ajoutées. S02 ne requiert pas les graphes pour les élèves. La profondeur enseignant réside dans les frontières, les hypothèses et l’argument, pas dans le seul emploi des symboles.
