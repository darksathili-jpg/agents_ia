# Comprendre la règle avant de manipuler

Dans la liste « Politique », ce mot désigne la règle qui choisit une commande. Ici, cette règle regarde d’abord si l’arrivée est à droite ou à gauche du robot. Elle demande alors un pas dans cette direction. Elle ne consulte pas les murs pour faire ce choix.

Seulement lorsque le robot et l’arrivée sont dans la même colonne, c’est-à-dire l’un au-dessus de l’autre, elle regarde si l’arrivée est plus haut ou plus bas. Elle demande alors un pas vers le haut ou vers le bas. Si le robot est déjà à l’arrivée, elle ne demande plus de déplacement.

Cette règle ne recherche pas de chemin et ne calcule pas de détour. Même si vous voyez un autre passage sur la grille, elle ne le compare pas au passage direct. À chaque tentative, elle refait la même comparaison à partir de la position courante.

Le **moteur de déplacement** est la partie du programme qui applique la commande choisie. Il vérifie que la case demandée est dans la grille et ne contient pas de mur. Sinon, il refuse le mouvement et le robot reste à sa position précédente. Dans ce laboratoire, ce refus termine l’expérience : il ne déclenche pas une recherche de détour.

**Que signifie le nom affiché ?** « Axe horizontal prioritaire » signifie que la règle examine gauche/droite avant haut/bas. « Gloutonne » désigne ici un choix immédiat dirigé vers l’arrivée, sans préparer la suite du trajet. C’est la règle précise de ce laboratoire : le mot « gloutonne » ne signifie pas que toutes les règles portant ce nom ignorent les obstacles ou choisissent de la même manière.
