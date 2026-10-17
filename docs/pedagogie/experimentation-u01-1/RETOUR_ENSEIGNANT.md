# Retour enseignant — compréhension et réemploi

Code non nominatif : ____________________  Code de séance : ____________________

Ce protocole concerne un enseignant compétent en informatique qui peut découvrir la théorie des agents. Il se traite après lecture de la préparation scientifique, dans un temps séparé de l’activité élève. Il ne donne pas une note à la personne. Conserver les règles et le code du guide accessibles ; ne consulter les corrigés de l’exercice enseignant qu’après sa résolution. Indiquer toute aide reçue.

## 1. Expliquer ce qui a été compris

**R1.** Avec vos propres mots, distinguez le choix d’une commande et son application. Utilisez une ligne de l’expérience Microduck pour étayer cette distinction. Indiquez ce que le journal permet d’observer et ce qui exige de connaître la règle.

Réponse :

**R2.** Repérez un passage du guide que vous n’avez pas compris ou dont vous ne sauriez pas expliquer l’intérêt. Indiquez la page et quelques mots permettant de le retrouver, la difficulté précise et l’explication supplémentaire dont vous auriez besoin. Si aucun passage n’est identifié, choisissez la distinction qui vous a demandé le plus d’attention et expliquez pourquoi.

Réponse :

## 2. Modèle de transition et Python

Les questions suivantes utilisent exclusivement la porte de Nora et le code `appliquer_porte` du guide : position hall/bureau, porte fermée/ouverte, commande AVANCER. Les règles sont celles du sujet, pas celles d’une porte réelle. Le guide contient la table complète et les définitions ; aucune connaissance antérieure de la théorie des agents n’est requise.

**R3.** Pourquoi deux commandes AVANCER depuis le hall peuvent-elles donner des positions après différentes dans les deux essais du sujet ? Précisez ce qui diffère dans les données avant et expliquez pourquoi cela ne contredit pas le résultat unique associé à un état complet et une commande dans ce modèle. Une réponse en mots est suffisante, sans formule obligatoire.

Réponse :

**R4.** Sans exécuter le code dans un premier temps, expliquez le rôle de chacun des trois paramètres et la signification des deux éléments du couple renvoyé. Suivez ensuite l’appel pour hall/ouverte/AVANCER puis bureau/fermée/AVANCER : quelle branche s’applique et quelle valeur est renvoyée ? Pourquoi les appels de la liste `cas` ne forment-ils pas un trajet continu ?

Réponse :

**R5.** Si vous choisissez d’exécuter ensuite le bloc Python du guide, relevez séparément votre prévision, la sortie réelle et ce que vous corrigez dans votre explication. N’écrivez pas « vérifié par exécution » si vous avez seulement lu les sorties attendues. Si vous n’exécutez pas, indiquez « non exécuté » ; ce choix n’empêche pas l’analyse du raisonnement.

Prévision / exécution éventuelle / interprétation :

## 3. Réutiliser et transposer

**R6.** Proposez un nouveau cas où une commande de déplacement est choisie sans déplacement obtenu. Définissez le contexte, les positions possibles, les données avant, la commande, la règle d’application et le résultat après. Évitez une information indispensable laissée implicite. Expliquez ensuite une modification d’une seule donnée avant qui autoriserait le mouvement, avec les mêmes règles et la même commande. Votre exemple n’est pas une nouvelle unité de cours : il sert à rendre votre raisonnement vérifiable.

Réponse :

**R7.** Pour un élève qui déduit « aucune commande n’a été choisie » d’un non-déplacement, proposez une question de relance et expliquez ce qu’elle vous permettrait d’observer sans lui dicter la conclusion. Quelle production nouvelle vous ferait distinguer compréhension et répétition du corrigé ?

Réponse :

## 4. Trace pour l’observateur — ne pas remplir à la place de l’enseignant

Pour R1–R7, relever les données mobilisées, les passages cités et les aides, en conservant les formulations utiles sans identité. R1 : séparation des responsabilités ; R2 : difficulté localisée ; R3 : état complet ; R4 : paramètres, branche et retour ; R5 : lecture ou exécution réellement distinguées ; R6 : exemple entièrement défini et cohérent ; R7 : relance et preuve de réemploi. Une réponse longue, un code exécuté ou une satisfaction déclarée ne suffisent pas à valider ces dimensions.

Ce qui reste à clarifier avant réutilisation en classe :
