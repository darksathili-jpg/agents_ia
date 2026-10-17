# U01 — Commander n’est pas déplacer

Code non nominatif : ____________________

**Cours élève — version expérimentale U01.1.** Le parcours essentiel est prévu pour vingt minutes : c’est une hypothèse à mesurer, pas une durée déjà observée. Pour travailler, vous devez disposer de ce document réunissant cours et activités. Aucun ancien cours n’est nécessaire.

Vous avez seulement besoin de savoir repérer une case à droite d’une autre et comparer deux positions. Vous n’avez pas de programme à écrire.

À la fin, vous devrez pouvoir distinguer **la commande choisie** et **le déplacement obtenu**, expliquer un refus, puis utiliser cette distinction dans une autre situation.

## 1. Microduck et sa piste — 0 à 3 minutes

Dans cette expérience, Microduck est le robot représenté sur une grille à l’écran. Il doit rejoindre une case d’arrivée. Nous étudions seulement ses deux premières tentatives de déplacement sur la rangée suivante, lue de gauche à droite.

| Case | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| Contenu au départ | Robot, case libre | Libre | Mur | Libre | Libre | Libre | Arrivée, case libre |
| Repère affiché dans le laboratoire | 0,2 | 1,2 | 2,2 | 3,2 | 4,2 | 5,2 | 6,2 |

Les lettres A à G sont les noms utilisés dans cette fiche. Les écritures « 0,2 », « 1,2 », etc. sont les repères des mêmes cases dans le laboratoire : utilisez la dernière ligne du tableau pour les lire, sans calcul. Les autres rangées de la grille ne sont pas utilisées dans ces deux tentatives.

Microduck commence en A ; l’arrivée est G. Sa règle choisit la commande **droite** lorsque l’arrivée est à sa droite. Pour les deux tentatives étudiées, l’arrivée reste à sa droite. La commande droite demande d’aller sur la case immédiatement à droite, pas directement à l’arrivée. Un mur ne peut pas être traversé ; la carte et l’arrivée ne changent pas pendant l’expérience.

**C0 — Repérage.** Quelle case est immédiatement à droite de A ? La case C est-elle libre ou occupée par un mur ? Répondez avant de continuer :



```{=openxml}
<w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p>
```



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 2. Prévoir, essayer et relever — 3 à 10 minutes

Le laboratoire doit être ouvert par l’enseignant. Dans la liste **Politique**, sélectionnez **Gloutonne (axe horizontal prioritaire)** : c’est le nom de la règle utilisée ici. Cliquez sur **Réinitialiser**. Vérifiez que **Position actuelle** indique `0,2`, donc A, et que **Décisions prises** indique 0. Ne lancez pas l’exécution automatique et ne changez plus de règle.

**P1 — Prédiction individuelle.** Avant de cliquer sur une étape, écrivez la commande que vous prévoyez et la case où Microduck se trouvera après cette première tentative. Justifiez avec les données de la piste.

Commande : __________ Case après : __________

```{=openxml}
<w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p>
```



**E1 — Première tentative guidée.** Cliquez une fois sur **Exécuter une étape**. Dans le journal intitulé **Trace pédagogique**, le mot après la première flèche est la commande choisie. Relevez ensuite **Position actuelle**. Complétez la première ligne du tableau. L’enseignant vous aide à lire cette ligne, pas à changer la règle.

| Tentative | Case avant | Commande relevée dans le journal | Case après, d’après la position affichée |
|---|---|---|---|
| 1 | A | __________ | __________ |
| 2 | À compléter après la première tentative : ____ | __________ | __________ |

**P2 — Nouvelle prédiction individuelle.** Sans réinitialiser, utilisez la position obtenue à la première tentative. Prévoyez la commande et la position après la deuxième tentative, puis justifiez :

```{=openxml}
<w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p>
```





```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Observer la deuxième tentative et comparer

**E2 — Deuxième tentative.** Cliquez une seconde fois sur **Exécuter une étape**, puis complétez la deuxième ligne. Lisez aussi le résultat écrit dans le journal :

```{=openxml}
<w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p>
```

 Si le robot est bloqué, ne lancez pas d’autre étape : l’expérience est terminée.

**E3 — Comparaison.** Combien de commandes ont été choisies pendant les deux tentatives ? Combien de déplacements d’une case ont réellement eu lieu ? Votre seconde prédiction correspond-elle à la position relevée ? Expliquez un éventuel écart :

```{=openxml}
<w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p>
```



Si le laboratoire n’est pas accessible, l’enseignant vous remet les deux relevés de remplacement prévus dans son dossier, **après** chacune de vos prédictions. Vous les analysez de la même façon ; il s’agit alors d’une étude de relevés, pas d’une manipulation du robot par vous-même.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 3. Comprendre ce qui s’est passé — 10 à 12 minutes

À lire après les deux tentatives.

La commande est ce que la règle demande : ici, aller à droite. Un autre composant du programme, appelé **moteur de déplacement**, vérifie la case demandée. Si cette case est libre, il y place le robot. Si elle contient un mur, il refuse le mouvement et conserve la position précédente.

Lors de la première tentative, la commande droite demande B, qui est libre : Microduck passe de A à B. Lors de la deuxième, la même commande demande C, qui contient un mur : Microduck reste en B. Le mur n’a pas changé ; le robot n’est plus au même endroit avant la deuxième tentative.

Il y a donc deux commandes, mais un seul déplacement. Lors du refus, la commande n’est pas remplacée par « rester sur place » : elle reste droite. **Choisir une commande et appliquer cette commande sont deux opérations distinctes.** Pour connaître le résultat, on compare la position avant et la position après ; le mot commandé ne suffit pas.



## A. Entraînement — 12 à 14 minutes

On reprend la piste du cours : les cases se suivent dans l’ordre A, B, C, D, E, F, G ; C contient un mur, toutes les autres cases sont libres. La commande **droite** demande la case immédiatement à droite. Le moteur déplace le robot seulement si cette case est libre ; sinon il le laisse où il est.

Les deux essais suivants sont **indépendants** : on place le robot dans la case de départ indiquée pour chaque ligne, puis on applique une seule commande droite. Il n’y a pas de déplacement entre les deux essais. On raisonne sur papier, sans chercher à changer le départ du laboratoire.

**A1.** Complétez les cases du tableau. Dans la dernière colonne, citez la case demandée et indiquez si elle est libre ou contient un mur.

| Essai | Case avant | Commande déjà choisie | Case demandée | Case après | Justification |
|---|---|---|---|---|---|
| 1 | D | droite | __________ | __________ | ____________________ |
| 2 | B | droite | __________ | __________ | ____________________ |



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## T. Transfert individuel — 14 à 17 minutes

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

**T2.** La commande choisie est-elle différente dans les deux essais ? Expliquez pourquoi les positions obtenues peuvent être différentes. Appuyez-vous sur une règle de fonctionnement de la porte, sans supposer que Nora change de décision :

```{=openxml}
<w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p>
```





```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## I. Vérification individuelle : un curseur — 17 à 20 minutes

Travaillez seul, sans corrigé ni indice sur la réponse. Toutes les règles nécessaires sont données ici : ce n’est ni le robot de la piste ni le personnage de la porte.

Un éditeur de texte simplifié contient un seul caractère, la lettre **X**. Un **curseur** est le trait vertical qui repère une position dans ce texte. Il peut occuper exactement deux positions, nommées **début** et **fin** :

```text
début : |X       fin : X|
```

La seule commande étudiée est **DROITE**. Elle demande de déplacer le curseur vers la position suivante à droite. Le programme applique ces règles :

- Depuis début, DROITE place le curseur à fin.
- Depuis fin, DROITE laisse le curseur à fin : aucune position plus à droite n’est autorisée.

Le texte ne change pas, le curseur ne revient pas automatiquement au début et aucune autre commande n’intervient. Le résultat indiqué est celui obtenu après application complète de l’unique commande. Les deux essais suivants sont **indépendants** : le curseur est placé dans la position avant indiquée pour chaque ligne. La commande DROITE a déjà été choisie dans les deux essais.

**I1.** Complétez le tableau. Dans la dernière colonne, citez la règle qui explique le résultat.

| Essai | Position avant | Commande choisie | Position après | Le curseur s’est-il déplacé ? | Justification |
|---|---|---|---|---|---|
| 1 | fin | DROITE | __________ | oui / non : ____ | ____________________ |
| 2 | début | DROITE | __________ | oui / non : ____ | ____________________ |

**I2.** Un camarade affirme : « Dans l’essai 1, puisque le curseur n’a pas changé de position, la commande DROITE n’a pas été choisie. » Cette affirmation est-elle compatible avec les données ? Justifiez en indiquant la commande choisie, les positions avant et après, et la règle appliquée :

```{=openxml}
<w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p><w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p>
```




Avant de rendre votre travail, vérifiez que vous avez écrit une explication, pas seulement « oui » ou « non ».
