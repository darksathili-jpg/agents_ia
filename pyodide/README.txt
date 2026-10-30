ORCHESTRA NSI — Pyodide 0.27.7 (exécution Python dans le navigateur)

L'archive v1.4 de départ contenait seulement ce fichier README. Le dépôt
GitHub utilisé au lycée peut être différent et posséder déjà les binaires.

Pour installer localement : lancer INSTALLER_PYODIDE.cmd depuis la racine
sur un poste avec Internet. Vérifier ensuite que sont présents :
  pyodide.js, pyodide.asm.js, pyodide.asm.wasm,
  python_stdlib.zip, pyodide-lock.json, MANIFEST_INSTALLATION.json

Le manifeste contient taille et SHA-256 ; il détecte une altération par rapport
aux fichiers enregistrés lors de l'installation, mais ne remplace pas une
vérification indépendante de l'origine des téléchargements.

Le script scripts/build_site.py --require-local-pyodide REFUSE une publication
lorsqu'un fichier manque ou si son empreinte diffère. Dans ce mode, le site
public désactive aussi la connexion de secours au CDN.

Pour un test local de l'interface sans distribution, utiliser le serveur Python
et, si Internet est autorisé, le secours CDN (pas adapté à un déploiement
hors ligne garanti).
