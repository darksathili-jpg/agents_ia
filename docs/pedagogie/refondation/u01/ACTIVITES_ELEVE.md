# U01 — Activités élève

À utiliser avec [le cours U01](COURS_ELEVE.md). Les règles nécessaires à chaque activité sont indiquées ci-dessous. Les activités sur papier ne modifient pas la grille du laboratoire.

## A. Entraînement — 12 à 15 minutes

On reprend la piste du cours : les cases se suivent dans l’ordre A, B, C, D, E, F, G ; C contient un mur, toutes les autres cases sont libres. La commande **droite** demande la case immédiatement à droite. Le moteur déplace le robot seulement si cette case est libre ; sinon il le laisse où il est.

Les deux essais suivants sont **indépendants** : on place le robot dans la case de départ indiquée pour chaque ligne, puis on applique une seule commande droite. Il n’y a pas de déplacement entre les deux essais. On raisonne sur papier, sans chercher à changer le départ du laboratoire.

**A1.** Complétez les cases du tableau. Dans la dernière colonne, citez la case demandée et indiquez si elle est libre ou contient un mur.

| Essai | Case avant | Commande déjà choisie | Case demandée | Case après | Justification |
|---|---|---|---|---|---|
| 1 | D | droite | __________ | __________ | ____________________ |
| 2 | B | droite | __________ | __________ | ____________________ |

**A2.** À propos de l’essai 2, Maya affirme : « Puisque le robot est resté en B, sa règle n’a pas choisi droite. » Cette affirmation est-elle compatible avec les données ? Justifiez en distinguant la commande choisie et le résultat du moteur : ____________________.

## T. Transfert individuel — 15 à 18 minutes

Dans un jeu, le personnage **Nora** peut se trouver dans deux pièces : le **hall** ou le **bureau**. Une porte sépare les deux pièces.

```text
HALL  —  PORTE  —  BUREAU
```

La porte a exactement deux états possibles : **ouverte** ou **fermée**. Son état est fixé avant chaque essai et ne change pas pendant cet essai. Elle ne s’ouvre pas automatiquement lorsqu’une commande est reçue.

La seule commande étudiée est **AVANCER**. Depuis le hall, elle demande de rejoindre le bureau en franchissant la porte. Le moteur du jeu applique les règles suivantes :

- Si Nora est dans le hall et si la porte est ouverte, elle rejoint le bureau.
- Si Nora est dans le hall et si la porte est fermée, elle reste dans le hall.
- Si Nora est déjà dans le bureau, elle y reste : ce modèle ne prévoit pas de déplacement plus loin.

Dans ce jeu simplifié, il n’y a ni clé, ni autre obstacle, ni délai de déplacement. Un mouvement autorisé est entièrement réalisé lorsqu’on lit la position après la commande.

Les essais du tableau sont **indépendants** : Nora est replacée dans le hall avant chacun d’eux. Dans les deux essais, la commande AVANCER a déjà été choisie. Vous n’avez pas à déterminer comment elle a été choisie.

**T1.** Complétez le tableau sans faire fonctionner le laboratoire : il s’agit d’une autre situation, décrite entièrement ici.

| Essai | Position avant | État de la porte pendant l’essai | Commande choisie | Position après | Déplacement réalisé ? |
|---|---|---|---|---|---|
| 1 | hall | fermée | AVANCER | __________ | oui / non : ____ |
| 2 | hall | ouverte | AVANCER | __________ | oui / non : ____ |

**T2.** La commande choisie est-elle différente dans les deux essais ? Expliquez pourquoi les positions obtenues peuvent être différentes. Appuyez-vous sur une règle de fonctionnement de la porte, sans supposer que Nora change de décision : ____________________.

## B. Bilan individuel — 18 à 20 minutes

**B1.** Un camarade lit uniquement le mot AVANCER dans le journal de l’essai 1 du transfert. Il conclut que Nora a nécessairement changé de pièce. Expliquez pourquoi cette conclusion n’est pas justifiée. Indiquez la position avant, la position après et ce qui a empêché le déplacement : ____________________.

Avant de rendre votre travail, vérifiez que vous avez écrit au moins une explication du mécanisme, pas seulement « oui » ou « non ». Les réponses du transfert et du bilan sont relues par l’enseignant ; cocher une case ne suffit pas à établir la compréhension.
