# U01 — Commander n’est pas déplacer

**Cours élève — version expérimentale U01.1.** Le parcours essentiel est prévu pour vingt minutes : c’est une hypothèse à mesurer, pas une durée déjà observée. Pour travailler, vous devez disposer de ce cours et des [activités élève](ACTIVITES_ELEVE.md), sur papier ou à l’écran. Aucun ancien cours n’est nécessaire. Les corrigés sont remis après votre recherche.

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

**C0 — Repérage.** Quelle case est immédiatement à droite de A ? La case C est-elle libre ou occupée par un mur ? Répondez avant de continuer : ____________________.

## 2. Prévoir, essayer et relever — 3 à 10 minutes

Le laboratoire doit être ouvert par l’enseignant. Dans la liste **Politique**, sélectionnez **Gloutonne (axe horizontal prioritaire)** : c’est le nom de la règle utilisée ici. Cliquez sur **Réinitialiser**. Vérifiez que **Position actuelle** indique `0,2`, donc A, et que **Décisions prises** indique 0. Ne lancez pas l’exécution automatique et ne changez plus de règle.

**P1 — Prédiction individuelle.** Avant de cliquer sur une étape, écrivez la commande que vous prévoyez et la case où Microduck se trouvera après cette première tentative. Justifiez avec les données de la piste.

Commande : __________ Case après : __________ Raison : ____________________.

**E1 — Première tentative guidée.** Cliquez une fois sur **Exécuter une étape**. Dans le journal intitulé **Trace pédagogique**, le mot après la première flèche est la commande choisie. Relevez ensuite **Position actuelle**. Complétez la première ligne du tableau. L’enseignant vous aide à lire cette ligne, pas à changer la règle.

| Tentative | Case avant | Commande relevée dans le journal | Case après, d’après la position affichée |
|---|---|---|---|
| 1 | A | __________ | __________ |
| 2 | À compléter après la première tentative : ____ | __________ | __________ |

**P2 — Nouvelle prédiction individuelle.** Sans réinitialiser, utilisez la position obtenue à la première tentative. Prévoyez la commande et la position après la deuxième tentative, puis justifiez : ____________________.

**E2 — Deuxième tentative.** Cliquez une seconde fois sur **Exécuter une étape**, puis complétez la deuxième ligne. Lisez aussi le résultat écrit dans le journal : ____________________. Si le robot est bloqué, ne lancez pas d’autre étape : l’expérience est terminée.

**E3 — Comparaison.** Combien de commandes ont été choisies pendant les deux tentatives ? Combien de déplacements d’une case ont réellement eu lieu ? Votre seconde prédiction correspond-elle à la position relevée ? Expliquez un éventuel écart : ____________________.

Si le laboratoire n’est pas accessible, l’enseignant vous remet les deux relevés de remplacement prévus dans son dossier, **après** chacune de vos prédictions. Vous les analysez de la même façon ; il s’agit alors d’une étude de relevés, pas d’une manipulation du robot par vous-même.

## 3. Comprendre ce qui s’est passé — 10 à 12 minutes

À lire après les deux tentatives.

La commande est ce que la règle demande : ici, aller à droite. Un autre composant du programme, appelé **moteur de déplacement**, vérifie la case demandée. Si cette case est libre, il y place le robot. Si elle contient un mur, il refuse le mouvement et conserve la position précédente.

Lors de la première tentative, la commande droite demande B, qui est libre : Microduck passe de A à B. Lors de la deuxième, la même commande demande C, qui contient un mur : Microduck reste en B. Le mur n’a pas changé ; le robot n’est plus au même endroit avant la deuxième tentative.

Il y a donc deux commandes, mais un seul déplacement. Lors du refus, la commande n’est pas remplacée par « rester sur place » : elle reste droite. **Choisir une commande et appliquer cette commande sont deux opérations distinctes.** Pour connaître le résultat, on compare la position avant et la position après ; le mot commandé ne suffit pas.

## 4. S’entraîner, transférer, faire le bilan — 12 à 20 minutes

Passez aux [activités élève](ACTIVITES_ELEVE.md) : entraînement A1, situation de la porte T1–T2, puis vérification I1–I2 dans une troisième situation. Le transfert et la vérification finale sont individuels. Vous pouvez justifier en phrases courtes ; aucune formule ni définition générale n’est demandée.

A2 et B1 sont des prolongements facultatifs, hors des vingt minutes. Ils ne remplacent ni les prédictions, ni l’explication, ni le transfert, ni la vérification finale. Si le parcours essentiel prend plus de temps, l’enseignant en relève la durée et adapte la suite sans supprimer ces phases.
