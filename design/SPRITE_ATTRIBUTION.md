# Sprite Microduck — intégration ORCHESTRA

- **Source :** planche PNG 768×1024 fournie par l’utilisateur dans la conversation.
- **Découpage :** 3 colonnes × 4 lignes, cellules exactement 256×256, RGBA.
- **Correspondance :** lignes 1 = face/sud ; 2 = profil gauche/ouest ; 3 = profil droit/est ; 4 = dos/nord.
- **Colonnes :** pas A, neutre, pas B. Les trois frames gardent la même origine et le même ancrage au sol.
- **Usages :** héro de Première (sud), héros de Terminale (est), visualisation Première, plateau Terminale, visualiseur BFS.
- **Vérité des données :** seuls les tracés moteurs contrôlent le déplacement du robot dans les grilles ; l’animation des héros est décorative.
- **Accessibilité :** mouvement décoratif désactivé par défaut si `prefers-reduced-motion`, bouton pause/reprise conservé.
- **Limite :** trois poses par direction ne représentent pas une marche cinématique complète (pas de saut/victoire/scan spécifique).
- **Publication :** les ressources PNG/WebP et le JS graphique sont autorisés par liste blanche ; le fichier Markdown reste privé.
