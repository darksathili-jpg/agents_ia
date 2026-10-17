# S03 — Feuille élève

Nom : __________ Classe : __________ Binôme : __________ Date : __________

Référence : [cours et consignes](SEANCE_03.md). Code initial : [script à copier entièrement](python/s03_depart.py). Cette feuille est distribuable sans corrigé. Décrire les résultats en mots ; aucune distinction ne repose uniquement sur une couleur d’affichage.

## 0–10 min — Retrouver la question

A. Observation à la bifurcation : __________

Sortie requise si bleu : __________ ; si orange : __________

Pourquoi une même observation ne suffit-elle pas ? __________

## 10–25 min — Prédire avant de lancer

| Contrôleur | Monde bleu, prédiction | Monde orange, prédiction | Observation après exécution |
|---|---|---|---|
| Oublie, choisit gauche | __________ | __________ | __________ |
| Écrase par l’indice courant | __________ | __________ | __________ |
| Mon contrôleur | __________ | __________ | __________ |

B. Un succès unique valide-t-il ma règle ? Pourquoi ? __________

C. À quel pas l’écrasement détruit-il la couleur ? __________

## 25–40 min — Spécifier

D. Compléter : si l’indice vaut `None`, je __________ ; sinon je __________.

Entrées de la fonction : __________ ; deux valeurs retournées : __________.

Une variable du monde que la fonction ne reçoit pas : __________.

## 40–80 min — TP03

Mode : console, une exécution complète, sans mouvement de la grille. Compléter `a_completer`. Dans le bloc de démonstration, essayer cette fonction sur les deux mondes. Ne pas changer la carte ou le budget pour rendre le test plus facile.

Hypothèse : __________ ; variable modifiée : __________ ; paramètres fixes : __________.

Code proposé sur feuille ou fichier :

________________________________________________________________

________________________________________________________________

| Monde | Pas | Observation reçue | Mémoire avant | Action | Mémoire après | Position après |
|---|---|---|---|---|---|---|
| bleu | 0 | __________ | __________ | __________ | __________ | __________ |
| bleu | 1 | __________ | __________ | __________ | __________ | __________ |
| bleu | 2 | __________ | __________ | __________ | __________ | __________ |
| orange | 0 | __________ | __________ | __________ | __________ | __________ |
| orange | 1 | __________ | __________ | __________ | __________ | __________ |
| orange | 2 | __________ | __________ | __________ | __________ | __________ |

Résultats prédits puis obtenus : __________. Erreur rencontrée et correction justifiée : __________.

## 80–95 min — Tester la limite

E. Appel `episode(a_completer, "bleu", visible=False)` : prédiction __________ ; résultat __________ ; explication __________.

F. Appel `episode(a_completer, "orange", visible=False, initiale="bleu")` : prédiction __________ ; résultat __________.

Puis indice visible : qu’est-ce qui change et pourquoi ? __________.

Terminale : invariant proposé __________ ; initialisation __________ ; conservation __________ ; hypothèse nécessaire __________.

## 95–110 min — Comparer sans confondre

G. Deux plans réussissent, coûts 2 et 5 : que dit le test de but ? __________ ; que préfère `U=-coût` ? __________.

Le TP choisit-il un plan en simulant les conséquences ou suit-il des règles ? Preuve : __________.

Dans S02, ce qui varie est __________ ; dans `choix_stochastique`, ce qui varie est __________.

Exemple d’hybridation et priorité d’une règle de sécurité : __________.

## 110–120 min — Bilan individuel

B1. Mise à jour et retour en Python : __________.

B2. Indice invisible, mémoire orange, position `(1,1)` : action __________ ; mémoire retournée __________.

B3. Pourquoi écraser par `None` est-il erroné ? __________.

B4. Politique et transition stochastiques : un exemple de chaque __________.

B5. Une limite avec condition précise : __________.

Maîtrise formative proposée : quatre réponses satisfaisantes sur cinq, B1 et B2 indispensables. La mémorisation d’une formule sans trace cohérente ne suffit pas. Si B1/B2 manquent, reprendre deux appels manuels ; si B4 manque, fixer une commande puis distinguer choix et effet. Ce seuil sera à éprouver en classe.
