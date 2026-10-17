# S03 — Parcours enseignant : architecture et compression de l’histoire

Document distinct du [cours NSI](SEANCE_03.md). Préparation : lire S02 et examiner les fonctions du [TP03 corrigé](python/s03_tp.py). Production attendue : formalisation, démonstration, lecture critique et proposition de transposition. Le temps de lecture approfondie est préparatoire ; pendant 95–110 min, substituer la discussion scientifique au guidage élève. Le TP reste dans les 120 minutes, pas dans une séance allongée implicitement.

## 1. Politique à historique et réalisation avec état interne

Notons Ω les observations, A les commandes, S les états du monde et M les états de mémoire. À l’instant t, l’histoire disponible est `h_t=(o_0,a_0,…,a_(t−1),o_t)`. Une politique déterministe à historique est une application des histoires admissibles vers A. Elle peut être conceptuellement définie sans que toute l’histoire soit effectivement stockée.

Dans notre convention, `m_t` désigne le souvenir **avant** de traiter `o_t`. La mise à jour `u : M×Ω → M` produit `m_(t+1)=u(m_t,o_t)` ; la décision du TP est `a_t=d(o_t,m_(t+1))`. Ainsi `F(o,m)=(d(o,u(m,o)),u(m,o))` réalise le contrat Python. On pourrait définir une autre fonction de commande prenant la mémoire avant actualisation : il faudrait composer les fonctions correctement, sans changer tacitement l’ordre.

Un contrôleur général peut aussi intégrer la commande et le résultat de transition à sa mise à jour. Le TP ne le fait pas : le chemin déterministe, la position observée et l’indice initial suffisent pour la tâche. La mémoire n’est pas l’état réel, et le résultat de `u` n’est pas une preuve de vérité.

Dans le TP, `M={inconnu, bleu, orange}` : c’est une mémoire finie. L’alphabet d’observations pertinentes est également fini. Une table de transitions de mémoire suffit : depuis n’importe quel souvenir, un indice bleu conduit à bleu ; orange conduit à orange ; une absence conserve le souvenir. L’entrée invalide n’appartient pas à cet alphabet et doit être signalée. L’ensemble fini des mémoires n’implique ni apprentissage ni planification.

L’implémentation Python utilise trois valeurs plutôt qu’un encodage binaire. Sur un matériel à bits, deux bits suffiraient pour les trois états ; après un indice fiable, distinguer les deux couleurs exige au moins deux états de mémoire. Cette borne porte sur ce contrôleur, sous les canaux d’information autorisés, pas sur la taille physique d’un objet Python.

## 2. Démonstration expliquée et conditions de validité

**Nécessité d’une distinction conservée à la bifurcation.** Les deux histoires commencent par des couleurs différentes puis donnent les mêmes observations de position. Avec une commande restante et les sorties imposées, leurs actions de réussite sont disjointes. Si un contrôleur déterministe associe la même mémoire à ces deux histoires, ses entrées `(observation,mémoire)` seront identiques au dernier pas ; il retournera donc la même commande et échouera dans au moins un monde. La mémoire doit distinguer ces histoires, ou un autre canal d’information doit être autorisé.

**Suffisance pour notre tâche.** Initialiser le souvenir à inconnu. Au départ, l’indice fiable actualise le souvenir à la couleur c. Aux deux pas suivants, l’indice est absent ; la règle conserve c. Les deux premières règles mènent à la bifurcation, et la troisième choisit la sortie autorisée par c. Les trois commandes respectent le budget. La preuve combine invariant de mémoire et trace de positions, et ne se réduit pas à la réussite d’un test.

Hypothèses : couleur stable, observation initiale exacte, chemin et carte fixes, mémoire non corrompue après actualisation, transitions sans glissement, trois commandes disponibles, pas de lecture de la variable cachée par le contrôleur. L’appel ne transmet que l’observation et la mémoire ; le conducteur, lui, connaît la cible pour évaluer le résultat. Les fonctions élèves doivent respecter cette frontière : accéder à des variables globales du conducteur changerait le problème.

**Contre-exemples.** Si aucun indice n’est reçu et que les deux mondes commencent avec la même mémoire, l’argument d’indiscernabilité reste valable, même avec une mémoire arbitrairement volumineuse construite à partir des mêmes données. Si l’indice ment ou change après le départ sans nouvelle observation, conserver la couleur ne garantit plus la réussite. Si l’on autorise un capteur supplémentaire ou un autre budget, il faut refaire l’analyse. Une mémoire utile ne remplace pas une vérification des hypothèses.

## 3. Architectures : dimensions combinables

Les repères classiques de Russell et Norvig distinguent règles réflexes simples, état interne, buts et utilités. Ils servent ici à comparer des choix de conception, sans catalogue exhaustif ni classement linéaire du moins au plus intelligent. Un système peut combiner plusieurs mécanismes.

| Repère | Ce qui intervient dans le choix | Limite à examiner | Cas original pour discuter |
|---|---|---|---|
| Réflexe simple | Observation présente, règles | Confusion entre situations perceptuellement identiques | Toujours gauche à la bifurcation. |
| Réflexe avec état | Souvenir actualisé, règles | Données périmées ou mise à jour erronée | Couleur retenue, sans recherche prospective. |
| Orienté objectif | But explicite et modèle des effets, éventuellement recherche | Modèle incomplet, coût du calcul | Comparer deux plans fournis qui atteignent une sortie. |
| Orienté utilité | Préférences numériques entre issues, modèle d’incertitude si nécessaire | Mauvais critère, estimations fragiles | Préférer coût 2 à coût 5 sous U=−coût. |

La présence d’une destination dans le code ne suffit pas à caractériser une architecture qui raisonne sur des buts. Inversement, un programme à règles peut avoir été conçu pour satisfaire un objectif. Distinguer intention du concepteur, critère d’évaluation et mécanisme effectivement exécuté.

Une fonction d’utilité représente un ordre de préférence dans un modèle. Comparer une somme `Σ P(issue|a,information) U(issue)` suppose des issues, des probabilités et une utilité suffisamment définies pour la décision considérée. Les élèves ne calculent pas cette somme ; ils comparent les deux coûts déterministes. Un chiffre de performance, une récompense immédiate et une utilité sur les trajectoires ne sont pas systématiquement interchangeables.

**Hybridation discutée, non implémentée** : estimation par mémoire, planification sur cette estimation, puis filtre réflexe qui refuse une action dangereuse. Il faut spécifier ce qui se passe si le filtre bloque le plan et quelle règle prime. L’architecture supplémentaire ne corrige pas automatiquement un modèle erroné. Il n’y a ici ni implémentation de recherche S04 ni contrôleur LLM.

## 4. Politique stochastique et transition stochastique

Une politique stochastique peut être décrite par `π(a|o,m)` ; une transition par `K(s'|s,a)`. Dans le TP, à la bifurcation sans couleur, le tirage sélectionne gauche ou droite tandis que le déplacement associé reste fixe. Dans S02, la commande droite restait fixe tandis que son effet pouvait être avancer ou patiner. Ces deux sources peuvent coexister dans d’autres modèles.

Le code sépare les deux issues par un paramètre `tirage`, puis les échantillonne avec un générateur à graine. La reproductibilité du programme ne transforme pas le mécanisme de décision modélisé en une preuve expérimentale de probabilité.

Si une politique sans information de couleur choisit gauche avec probabilité p, sa probabilité de réussite vaut p en bleu et 1−p en orange. Elle ne peut donner une garantie de 1 aux deux mondes. Son pire cas vaut au plus 1/2, atteint à p=1/2 sous ce critère. Cela ne suppose pas une répartition équiprobable des mondes ; une réussite moyenne exigerait de spécifier cette répartition. Le TP force les deux branches mais ne prétend pas estimer p sur huit observations.

## 5. Lecture scientifique critique

Sources contrôlées pour ce jalon : [Poole et Mackworth, 2023, §2.1.1–2.1.3](https://artint.info/3e/html/ArtInt3e.Ch2.S1.html), manuel scientifique en accès auteur ; [Russell et Norvig, extrait public du chapitre 2, §2.4](https://aima.cs.berkeley.edu/4th-ed/pdfs/newchap02.pdf), manuel, extrait non daté. Conserver la réserve du dossier : le chemin du PDF ne suffit pas à établir sa correspondance exacte avec la pagination de la quatrième édition. Ce sont des ouvrages de synthèse, pas des résultats expérimentaux nouveaux évalués ici ; aucune prépublication ni guide industriel ne fonde la preuve du TP.

Travail court : relever le rôle attribué à l’information conservée, puis identifier une différence de convention de notation avec notre contrat. Demander ensuite : « le terme belief state signifie-t-il nécessairement une distribution de probabilités ? » Réponse attendue : le sens général de mémoire employé dans cette lecture est plus large. Notre couleur stockée est un cas particulier très simple ; elle ne constitue pas un filtre probabiliste.

Deuxième question : « notre règle de couleur est-elle automatiquement une architecture orientée objectif parce qu’elle atteint la bonne sortie ? » Non : examiner le code, qui applique des règles sans comparer des futurs simulés. Les exemples et la preuve de ce dossier sont originaux ; ne pas les attribuer aux auteurs des ouvrages. Les termes doivent être rapprochés des mécanismes, pas utilisés comme des labels d’autorité.

## 6. Transposition didactique et évaluation enseignante

Production en quinze minutes : choisir un exemple de clé visible une seule fois ; préciser observation autorisée, trois états de mémoire, mise à jour, règle d’action et un cas d’erreur ; justifier le niveau choisi. Correction-type : inconnu/clé rouge/clé verte ; observation non reçue conserve l’état ; la clé doit rester valide ; une serrure changée à l’insu de l’agent invalide la garantie. Ne pas confondre ce changement du monde avec un effacement de mémoire.

Première : donner le conducteur, nommer chaque champ, remplir deux lignes à la main avant saisie, limiter la modification à quatre lignes et faire reformuler `return`. Terminale : demander la table de mémoire, l’invariant, le nombre minimal d’états distincts et la preuve par deux histoires. Les deux parcours ont la même question scientifique, pas le même volume de formalisme.

Évaluer l’enseignant sur : contrat cohérent (ordre temporel explicité), preuve avec hypothèses, distinction modèle/mémoire, contre-exemple valide, transposition avec critères observables. Une notation riche sans définition des variables n’est pas un approfondissement réussi. Les appuis NSI sont fonctions, structures de données, spécification, boucles et tests ; les taxonomies d’architectures ne sont pas présentées comme un nouveau contenu réglementaire obligatoire.
