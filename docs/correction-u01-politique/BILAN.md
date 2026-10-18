# Correction ciblée : expliquer la règle de déplacement

Branche conservée : `feature/u01-1-integration-interactive`. État avant correction : commit `88242a60eb14c2ef6bf5116243837714f2152604`. Le corpus approuvé U01.1 au commit `fcbdb8b1c73c0760e60fb4d53506d6c5d85e4fc6` et ses exercices restent inchangés.

## Constat et audit du code réel

Dans `laboratoire-moteur.js`, `naive(p)` reçoit la position courante et lit l’arrivée `goal`. L’ordre des tests est exactement :

1. Abscisse du robot inférieure à celle de l’arrivée : retourne `droite`.
2. Abscisse supérieure : retourne `gauche`.
3. À abscisses égales, ordonnée inférieure : retourne `bas`.
4. À abscisses égales, ordonnée supérieure : retourne `haut`.
5. Position égale à l’arrivée : retourne `null`, aucune commande de déplacement.

Les ordonnées augmentent vers le bas dans cette grille. La fonction ne consulte ni `walls`, ni `valid`, ni une recherche de chemin. Les deux premiers tests donnent la priorité gauche/droite ; aucune autre direction n’est comparée si l’un de ces tests réussit. Avec l’arrivée actuelle en dernière colonne, le cas « arrivée à gauche » n’est pas rencontré depuis une position autorisée de cette expérience ; il existe néanmoins dans la fonction générale.

Le moteur `step()` prend la commande choisie, calcule la case voisine puis appelle `valid(next)`. Cette fonction accepte seulement une case dans les limites `0 ≤ x < 7`, `0 ≤ y < 5` et absente de `walls`. Un mur ou une sortie de grille entraîne refus, position conservée et état `blocked`. L’expérience s’arrête alors ; elle ne repart pas automatiquement avec une autre commande. Le code gère également arrêt demandé, absence de commande et commande inconnue, sans rechercher un détour à la place de la règle. Ces cas ne sont pas les deux tentatives étudiées dans U01.1.

| Tentative réellement exécutée | Comparaison utilisée par la règle | Commande | Vérification | Résultat |
|---|---|---|---|---|
| 1, départ A `(0,2)` | `0 < 6` : G est à droite de A | droite, demande B `(1,2)` | B est dans la grille et libre | A → B, un déplacement |
| 2, départ B `(1,2)` | `1 < 6` : G est encore à droite de B | droite, demande C `(2,2)` | C appartient aux murs | B → B, aucun déplacement ; arrêt |

La présence d’un autre chemin sur la carte n’est pas incohérente avec ce comportement : ce programme ne le calcule pas. Une recherche de chemin est un mécanisme différent, qui n’a pas été ajouté ici. Aucune correction du moteur n’est justifiée par ce constat.

## Correction pédagogique et affichage

Le complément [regle-deplacement-v1.md](../../contenus/u01/regle-deplacement-v1.md) définit « politique », explique les comparaisons, la priorité horizontale, l’absence de consultation des murs lors du choix et le contrôle ultérieur du moteur. Il annonce explicitement que le détour visible n’est pas comparé au trajet direct. Les termes du nom de la règle sont expliqués après son fonctionnement ; son comportement n’est pas attribué à toute stratégie dite gloutonne.

Ce complément versionné est distinct des sources approuvées, conservées à l’identique. Il est ajouté avant P1 et la manipulation dans la leçon, et avant les boutons dans le laboratoire ouvert seul. Dans le cadre intégré, il n’est pas répété : il reste visible dans la leçon qui contient le cadre. Le générateur le lit depuis cette seule source ; sa provenance et son empreinte sont ajoutées à `u01-sources.json` et contrôlées par `verifier-u01.py`.

Après chaque tentative, quatre zones distinctes affichent :

- la commande effectivement journalisée et la case demandée ;
- la raison, vérifiée contre l’appel de la fonction réelle `naive` pour la position avant ;
- la vérification de la case par les limites et les murs réels du moteur ;
- la comparaison entre position avant et position effectivement affichée après.

L’adaptateur lit la trace et les données du moteur ; il ne commande pas de mouvement supplémentaire et ne remplace pas la politique. Une divergence entre calcul explicatif et effet observé serait signalée. Au départ et après réinitialisation, aucune réponse d’étape n’est affichée à l’avance. Le dernier détail concerne une tentative à la fois ; le journal existant conserve les deux lignes.

## Contrôles effectués

- `python scripts/construire-u01.py` : génération depuis le corpus approuvé et le complément identifié.
- `python scripts/verifier-u01.py` : paragraphes et liens, complément présent, archives, comparaison du moteur extrait à l’original et Worker inchangé ; Python enseignant exécuté sous CPython.
- `node --check u01-laboratoire.js` : syntaxe correcte.
- `npx playwright test --workers=2 --reporter=dot` : **33 tests réussis**, aucun échec au dernier passage, dont six nouveaux scénarios ciblés. Le résumé est conservé dans [tests.txt](tests.txt).
- Contrôles directs des fonctions réelles : les deux retours droite, les cas verticaux à colonne égale, l’absence de commande à l’arrivée, case libre, mur et quatre limites de grille.
- Dans chaque mode clair, sombre et vidéoprojecteur : les quatre messages de la tentative 1, puis ceux de la tentative 2 ; compteur et arrêt ; réinitialisation sans détail périmé. Boutons actionnés au clavier, erreurs JavaScript absentes.
- Contrôle du cadre intégré à 390 px, absence de débordement du document et du cadre, focus clavier ; texte agrandi du mode vidéoprojecteur.
- Suite U01.1/V2 complète maintenue, avec les transferts inchangés et le Python réel sous Pyodide, interruption et reprise comprises.

Les captures « avant » ont été prises dans Chromium **avant les modifications**, dans les trois modes, après la deuxième tentative. Les captures « après » proviennent du navigateur réel : avant manipulation, après chacune des deux étapes et sur mobile. Elles ont été relues visuellement : distinction des quatre rubriques, cohérence avec la grille et la trace, contraste et lisibilité générale. [Galerie avant/après](index.html).

## Limites et arrêt

Cette correction ajoute de la lecture : son coût en temps doit être mesuré, et non absorbé artificiellement dans les vingt minutes annoncées comme hypothèse. La compréhension effective du choix, la capacité à distinguer règle et moteur et l’utilité des quatre rubriques restent à examiner avec des personnes. Aucun essai humain ni efficacité démontrée ne sont revendiqués.

Le lecteur d’écran et le vidéoprojecteur physique n’ont pas été testés. Le nom de la règle est conservé et expliqué ; son adéquation au public reste soumise à relecture. Aucune nouvelle activité, aucune autre stratégie, aucune modification du moteur ou de Pyodide. Ni fusion, ni publication de branche, ni déploiement. Arrêt pour validation humaine avant toute suite.
