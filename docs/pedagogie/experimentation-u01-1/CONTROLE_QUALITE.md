# Contrôle documentaire — 17 octobre 2026

## Contrôles effectués

- Cinq DOCX ouverts dans Microsoft Word 16.0 en lecture seule, repaginés et exportés en PDF. Pagination finale : élève 6 pages ; enseignant 9 ; observation 3 en paysage ; retour enseignant 3 ; procédure 3. Les compteurs de page sont des champs Word.
- Contrôle des 78 lignes de tableaux dans Word : aucune ligne répartie sur deux pages. Les en-têtes sont répétés si nécessaire. Les petites tables enseignantes sont conservées d’un seul tenant.
- Extraction du texte des cinq PDF et contrôle des coordonnées des mots : aucun texte hors page, aucune page vide hors pied de page. Ce contrôle géométrique ne remplace pas la lecture visuelle.
- Planches de toutes les pages relues visuellement : hiérarchie noire, absence d’aplats, tableaux bordés, espaces de réponse, séparation des publics et sauts de page. Vues agrandies des situations Nora/curseur et du code enseignant disponibles dans `controle/`.
- Le support élève contient les seules activités essentielles. Les cellules de réponse sont vierges ; A2/B1 et les corrigés ne figurent pas dans ce support. L’explication de Microduck reste en page 4, distribuée après E2/E3 ; aucune conclusion de cette page n’apparaît dans les pages de prédiction.
- Le texte scientifique et les corrigés enseignants sont repris des sources, contrôlés par extraction textuelle avec tolérance pour la typographie et les retours de ligne. Les définitions des paramètres, hypothèses, quatre états, limites, erreurs anticipées et références sont conservées.
- Le bloc Python extrait du DOCX est comparé à la source puis exécuté sous CPython : quatre états conformes à la table ; trois entrées invalides refusées par `ValueError`. Le code n’est pas exécuté dans l’application et ne modifie aucun personnage.
- Vérification des chemins du lanceur et de l’option `--port` dans le script existant. La procédure indique explicitement l’URL du laboratoire, le lanceur ouvrant initialement la page du module. Le contrôle préparatoire des deux pas à effectuer sur chaque poste est décrit ; aucune nouvelle validation de l’application ou de Pyodide n’est revendiquée ici.
- Empreintes des sept sources U01.1 conservées ; comparaison Git avec le commit de référence sans modification de ces sources. Les seuls ajouts sont dans ce nouveau dossier documentaire.

Les résultats détaillés de pagination et de contrôle sont conservés dans `controle-word.json` et `controle/verification.json`. Les captures sont des rendus documentaires, pas des productions d’apprenants.

## Points corrigés pendant la fabrication

Un bloc Python initialement coupé a été regroupé. Une page vide de la grille causée par un saut de page a été supprimée. Les largeurs des tableaux, les bordures et les lignes d’écriture ont été ajustées. Les références et la préparation technique enseignante ont été regroupées pour éviter un dernier paragraphe isolé. Ces corrections portent sur ce dossier de fabrication, sans réécriture des sources validées pour l’essai.

## Limites à conserver explicitement

Ce contrôle porte sur les fichiers et leur rendu dans l’environnement disponible. Aucun essai élève ou enseignant, aucune impression physique, aucun contrôle avec lecteur d’écran n’a été effectué. Les DOCX comportent des titres structurés et des en-têtes de tableaux, mais cela ne constitue pas un audit complet d’accessibilité bureautique.

Les vingt minutes, la suffisance des espaces d’écriture, la compréhension des consignes, la neutralité effective des relances, la qualité des transferts et le temps de préparation enseignante restent à mesurer. La préparation et le retour enseignant n’ont pas de durée validée. Une autre version de Word ou un remplacement des polices peut modifier la pagination ; employer les PDF joints pour le tirage de référence.

La bibliographie de la version scientifique est conservée sans nouvelle interprétation ; ce travail de mise en forme ne constitue pas une nouvelle revue scientifique indépendante. Aucun résultat favorable n’est prérempli dans les instruments. Le dossier attend la relecture et l’accord du commanditaire avant toute expérimentation présentée comme réalisée.
