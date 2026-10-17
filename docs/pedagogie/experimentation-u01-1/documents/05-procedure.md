# Préparer et exploiter un premier essai accompagné U01.1

Statut : **préparation uniquement**. Aucun essai auprès d’élèves ou d’enseignants n’a été réalisé dans ce dossier. Version scientifique de référence : `fcbdb8b1c73c0760e60fb4d53506d6c5d85e4fc6`. Les fichiers U01.1 restent inchangés ; les adaptations portent sur la mise en page et les instruments d’observation.

## 1. Préparer les documents et la séance

L’organisateur fixe un petit groupe compatible avec une observation attentive, comprenant des élèves de Première et de Terminale NSI et des enseignants découvrant la théorie des agents. Relever séparément ces publics ; ne pas présumer des acquis à partir de la classe ou de la fonction. Si une seule personne anime et observe, commencer par un essai individuel accompagné ou prévoir des pauses de prise de notes ; déclarer ce choix au lieu de promettre un suivi individuel impossible dans un grand groupe.

Préparer les cinq documents du dossier : support élève essentiel, guide enseignant, grille d’observation, retour enseignant et présente procédure. Le support élève réunit les deux sources nécessaires, sans les exercices facultatifs A2/B1 ni leurs corrigés. Le guide conserve les approfondissements, l’exemple Python complet, les exercices enseignants et les corrigés expliqués ; ses pages sont réservées à l’enseignant.

Utiliser les PDF joints pour une impression à pagination stable, ou les DOCX après vérification dans la version locale de Word. Imprimer en A4, taille réelle 100 %, noir et blanc ; ne pas activer « plusieurs pages par feuille ». Le support élève est prévu en recto simple pour pouvoir remettre les feuilles successivement et laisser la place à l’écriture. La grille d’observation est en paysage ; les autres documents sont en portrait. Ne pas distribuer le guide enseignant par erreur.

Attribuer un code de participant non nominatif, par exemple un code aléatoire sans correspondance conservée avec un nom. Sur les formulaires, ne noter ni nom, ni adresse, ni établissement. Indiquer seulement Première, Terminale ou enseignant selon le besoin d’analyse. Ne pas recopier de détail permettant d’identifier quelqu’un dans les commentaires ou citations ; masquer un nom que le participant aurait ajouté à sa copie. Ne pas constituer de liste code/identité. Ces précautions portent sur les documents recueillis ; la présence de l’observateur auprès de personnes connues ne devient pas une observation humaine « anonyme » par magie.

Fixer un code de séance, la version du dossier et la modalité : individuel accompagné ou groupe. Garder un exemplaire vierge de chaque document. Les cases de temps observé et de résultats doivent rester vides avant l’essai ; les durées cibles préimprimées sont des hypothèses, jamais des valeurs à recopier comme mesures.

## 2. Ouvrir et vérifier le laboratoire existant

Depuis le dossier du dépôt, double-cliquer sur `Ouvrir-Agent-Academy.cmd` ; Python doit être installé. Laisser sa fenêtre ouverte. Dans Edge ou Chrome, ouvrir `http://127.0.0.1:8765/laboratoire.html`, et non l’ancienne leçon S01 HTML. Si le port est déjà occupé, lancer `python scripts/ouvrir-academy.py --port 8766`, puis utiliser `http://127.0.0.1:8766/laboratoire.html`. Ctrl+C dans la fenêtre du serveur l’arrête après utilisation.

Choisir « Gloutonne (axe horizontal prioritaire) » dans Politique ; cliquer Réinitialiser. Vérifier Position actuelle = 0,2 et Décisions prises = 0. Faire un essai préparatoire sans participant : premier pas vers 1,2 ; second pas refusé devant le mur, position conservée à 1,2. Réinitialiser ensuite pour revenir à 0,2 et au compteur 0. Ne pas laisser le résultat préparatoire affiché à l’arrivée de l’apprenant.

Ne pas changer de politique, ne pas lancer l’automatique, BFS ou Python pendant le parcours élève. Le code Python du guide sert à la formation de l’enseignant ; il ne pilote pas cette expérience. Ni la porte de Nora ni le curseur ne sont des fonctionnalités du laboratoire : ces deux situations se traitent sur papier.

En cas d’indisponibilité technique, utiliser les deux relevés du guide, remis l’un après l’autre après chaque prédiction. Inscrire « relevés fournis » dans la grille, conserver le temps perdu et l’incident. Ne pas présenter cette modalité comme une manipulation réalisée par l’élève. Séparer ses observations de celles d’un essai avec grille réelle.

## 3. Mener le parcours sans fabriquer la réponse

Avant de commencer, expliquer qu’il ne s’agit pas d’une note ni d’une évaluation de la personne : on examine la clarté du support et le raisonnement rendu possible. Demander de conserver les premières réponses et de signaler les changements, sans effacer la prédiction initiale. Ne pas annoncer à l’avance « deux commandes, un déplacement ».

Remettre les pages du support élève par étapes : page 1 pour le contexte ; pages 2–3 pour prédictions et observation ; page 4 seulement après les deux tentatives et les réponses E2/E3, pour l’explication et A1 ; page 5 pour Nora ; page 6 pour le curseur. L’explication scientifique conservée page 4 reprend normalement l’exemple observé : ce n’est pas un corrigé du transfert. Cette distribution évite de livrer la conclusion avant l’observation. Aucun corrigé d’activité n’est inclus dans le support élève.

Pour chaque phase, noter début, fin, pauses et difficulté rencontrée. Ne pas arrêter la réponse pour faire respecter le chiffre prévu. Les vingt minutes sont un budget à éprouver ; installation, préparation enseignante et remédiation supplémentaire sont notées séparément. Ne retirer ni prédiction, ni explication, ni transfert, ni vérification finale en cas de retard.

Pendant l’exemple guidé E1, l’aide de lecture du journal est prévue : la noter comme aide d’accès. Pour T1–T2 et I1–I2, laisser les règles imprimées accessibles mais ni corrigé ni indication de résultat. Une relance « quelle donnée du sujet utilises-tu ? » n’a pas le même effet qu’un rappel de la règle qui empêche le mouvement : transcrire la relance et coder son effet plutôt que supposer sa neutralité.

Si une difficulté empêche de poursuivre, recueillir d’abord la réponse ou l’absence de réponse, puis aider sans laisser l’élève bloqué indéfiniment. Marquer la réponse obtenue après indice conceptuel comme « avec relance ». Une réponse juste après lecture du corrigé ne devient pas une réponse autonome. Ne pas corriger Nora avant d’avoir recueilli le curseur si l’objectif est d’observer le réemploi sans nouvelle explication entre les deux.

## 4. Recueillir et coder les observations

Utiliser une grille par participant pour les productions et les aides, avec le même code sur sa copie. En groupe, distinguer durée collective de phase et temps individuel réellement observé ; laisser « non observé » si l’on ne dispose pas de mesure individuelle. Ne pas convertir une durée collective en durée individuelle supposée.

La grille sépare trois objets : les temps ; les productions Nora/curseur et les critères V1–V3 ; les difficultés et interventions. Relever un indice précis : réponse citée sans identité, position avant/après, commande indiquée, règle invoquée, demande de lecture, incident technique. Ne pas résumer par « compris » ou « pas motivé ».

Coder chaque critère avec les mots du guide : autonome, avec relance, non établi ou non observable. Une question non traitée faute de temps n’est pas automatiquement une preuve d’incompréhension. Une difficulté de coordonnées n’est pas automatiquement une confusion commande/effet. Noter si une réponse a été revue après une aide, et conserver la première version lisible.

Pour les enseignants, prévoir une préparation séparée avec le guide, puis le protocole de retour. Recueillir leurs explications et leur résolution avant les corrigés de l’exercice enseignant. La formalisation est facultative, le raisonnement verbal recevable. La préparation scientifique n’est pas ajoutée artificiellement aux vingt minutes élèves. La fiche de retour demande des productions et des passages précis, pas seulement un avis de satisfaction.

## 5. Analyser et décider des corrections

Après l’essai autorisé, rassembler copies, grilles et retours par code et modalité. Séparer Première, Terminale et enseignants, ainsi que manipulation réelle et relevés fournis. Comparer pour chaque phase durées cibles et observées en indiquant pauses, données manquantes et aides. Pour un petit groupe, présenter les cas et les étendues observées ; ne pas annoncer un effet représentatif de toutes les classes.

Pour V1, vérifier que la commande n’est pas remplacée par l’effet ; pour V2, que le non-déplacement est expliqué par la règle du cas ; pour V3, que Nora et le curseur sont tous deux traités à partir de leurs données. L’exactitude des positions sans justification ne suffit pas à établir le mécanisme. Examiner les incohérences entre tableau et phrase plutôt que choisir seulement la partie favorable. La grille ne se réduit pas à une note globale.

Faire relire les productions ambiguës par une seconde personne si possible. Consigner le désaccord de codage et les indices utilisés ; ne pas le dissimuler dans une moyenne. Distinguer difficulté rédactionnelle, difficulté de lecture, erreur de mécanisme, intervention suggestive et incident technique. Une réponse fausse ne désigne pas à elle seule sa cause.

Ouvrir ensuite un registre de décisions : constat daté et anonymisé, tâche touchée, exemple de production, hypothèse explicative, correction envisagée, autre explication possible, preuve attendue après révision. Ne pas modifier silencieusement les sources de référence. Une ambiguïté de règle ou une contradiction scientifique bloque la validation de la version ; une difficulté récurrente de lecture conduit à une proposition rédactionnelle ciblée ; un dépassement récurrent conduit à revoir le budget, pas à supprimer les phases essentielles.

Les corrections proposées doivent être soumises au commanditaire avec les productions qui les motivent. Un résultat favorable sur quelques personnes permet au plus de proposer une suite d’essais ; il ne prouve ni efficacité générale, ni exploitation autonome, ni rétention différée. Un essai accompagné ne valide pas un usage sans enseignant. Aucun seuil de satisfaction ou pourcentage de réussite ne déclenche automatiquement une nouvelle unité.

## 6. Point d’arrêt de cette préparation

Le présent dossier fournit des instruments vierges et une procédure. Il ne contacte personne, ne déclare aucun essai réalisé et ne préremplit aucun résultat. Attendre la validation du dossier et les modalités convenues avant d’annoncer une expérimentation. Aucune intégration applicative, fusion ou mise en ligne n’est effectuée.
