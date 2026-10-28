#!/usr/bin/env python3
"""Crée une publication GitHub Pages à liste blanche, jamais le dépôt brut.

Usage local sans binaires : python scripts/build_site.py --allow-cdn
Publication hors-ligne : python scripts/build_site.py --require-local-pyodide
"""
from __future__ import annotations
import argparse
import hashlib
import os
import subprocess
from datetime import datetime, timezone
import json
import re
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '_site'
STATIC = (
    'index.html', 'site.css', 'shared/editor-indent.js', 'shared/microduck-sprite.js',
    'premiere/index.html', 'premiere/styles.css', 'premiere/app.js',
    'premiere/engine.py', 'premiere/python-worker.js', 'premiere/hero-motion.js',
    'terminale/index.html', 'terminale/styles.css', 'terminale/app.js',
    'terminale/python-worker.js', 'terminale/runner.py', 'terminale/monde.py',
    'terminale/cases.js', 'terminale/demo-bfs.js', 'terminale/bfs-visualizer.js',
    'terminale/hero-motion.js', 'terminale/eleve_a_completer.py',
)
ASSET_DIRS = ('assets', 'premiere/assets', 'terminale/assets')
ASSET_SUFFIXES = {'.png', '.jpg', '.jpeg', '.webp', '.avif', '.svg'}
VENDOR = ('prism-core.min.js', 'prism-clike.min.js', 'prism-python.min.js', 'PRISM-LICENSE.txt')
PYODIDE_FILES = ('pyodide.js', 'pyodide.asm.js', 'pyodide.asm.wasm', 'python_stdlib.zip', 'pyodide-lock.json')


def copy_file(relative: str) -> None:
    source = ROOT / relative
    if not source.is_file():
        raise RuntimeError(f'Fichier nécessaire absent : {relative}')
    destination = OUTPUT / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_pyodide(required: bool) -> bool:
    folder = ROOT / 'pyodide'
    existing = [name for name in PYODIDE_FILES if (folder / name).is_file()]
    if not existing:
        if required:
            raise RuntimeError('Pyodide local absent : installer la version 0.27.7 et son MANIFEST_INSTALLATION.json avant toute publication hors ligne.')
        return False
    if len(existing) != len(PYODIDE_FILES):
        raise RuntimeError('Distribution Pyodide incomplète : ' + ', '.join(set(PYODIDE_FILES) - set(existing)))
    manifest_path = folder / 'MANIFEST_INSTALLATION.json'
    if not manifest_path.is_file():
        raise RuntimeError('Empreintes Pyodide manquantes : MANIFEST_INSTALLATION.json requis pour éviter de publier des fichiers non vérifiés.')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('version') != '0.27.7':
        raise RuntimeError('Version Pyodide inattendue (0.27.7 requise).')
    for name in PYODIDE_FILES:
        record = manifest.get('files', {}).get(name, {})
        expected = record.get('sha256')
        if not isinstance(expected, str) or len(expected) != 64:
            raise RuntimeError(f'Empreinte SHA-256 absente pour {name}')
        current = hashlib.sha256((folder / name).read_bytes()).hexdigest()
        if current != expected:
            raise RuntimeError(f'Empreinte SHA-256 incompatible : {name}')
        copy_file('pyodide/' + name)
    return True


def validate_publication() -> None:
    paths = [x.relative_to(OUTPUT).as_posix() for x in OUTPUT.rglob('*') if x.is_file()]
    blocked_names = {'GUIDE_ENSEIGNANT.md', 'README.md', 'RECETTE_EDGE.md', 'LANCER_ORCHESTRA.cmd',
                     'INSTALLER_PYODIDE.cmd', 'REFERENCE_SOLUTION.py', 'reference_solution.py'}
    if any(x.split('/')[-1] in blocked_names or x.startswith(('tests/', '.github/', 'scripts/'))
           or '/tests/' in x or x.startswith('outils/') or x.endswith(('.md', '.cmd', '.pyc'))
           for x in paths):
        raise RuntimeError('Un fichier non autorisé figure dans la distribution publique.')
    for rel in ('index.html', 'premiere/index.html', 'terminale/index.html'):
        text = (OUTPUT / rel).read_text(encoding='utf-8')
        if 'fonts.googleapis.com' in text or 'fonts.gstatic.com' in text:
            raise RuntimeError('Police externe interdite dans le site élève : ' + rel)
    for rel in ('premiere/app.js', 'premiere/engine.py'):
        text = (OUTPUT / rel).read_text(encoding='utf-8')
        if 'REFERENCE_SOLUTION' in text or 'const SOLUTION =' in text:
            raise RuntimeError('Corrigé présent dans le site élève : ' + rel)
    # Defense-in-depth: don't publish hidden file or supplementary docs.
    if any('/.' in '/' + p or p.startswith('.') for p in paths):
        raise RuntimeError('Fichier masqué dans le site public')


def _source_revision() -> str:
    """Révision de la source construite, sans dépendance réseau."""
    candidate = os.environ.get("GITHUB_SHA", "")
    if re.fullmatch(r"[0-9a-f]{40}", candidate):
        return candidate
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5, check=True,
        )
        if re.fullmatch(r"[0-9a-f]{40}", result.stdout.strip()):
            return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass
    return "inconnue"


def guard_legacy_deployments() -> None:
    """Refuse une release si un autre workflow GitHub peut publier le dépôt entier.

    Cela ne désactive PAS un workflow existant : il faut le retirer dans GitHub.
    """
    folder = ROOT / '.github' / 'workflows'
    if not folder.exists():
        return
    for path in sorted((*folder.glob('*.yml'), *folder.glob('*.yaml'))):
        if path.name == 'pages.yml':
            continue
        content = path.read_text(encoding='utf-8')
        if ('deploy-pages@' in content or 'upload-pages-artifact@' in content
                or re.search(r"(?m)^\s*path\s*:\s*['\"]?\.['\"]?\s*$", content)):
            raise RuntimeError(f'Ancien workflow de déploiement à supprimer ou désactiver : {path.relative_to(ROOT)}')


def build(require_local: bool) -> dict:
    guard_legacy_deployments()
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    try:
        for item in STATIC:
            copy_file(item)
        for folder in ASSET_DIRS:
            for asset in sorted((ROOT / folder).iterdir()):
                if asset.is_file() and asset.suffix.lower() in ASSET_SUFFIXES:
                    copy_file(asset.relative_to(ROOT).as_posix())
        for folder in ('premiere/vendor', 'terminale/vendor'):
            for name in VENDOR:
                copy_file(folder + '/' + name)
        local = copy_pyodide(required=require_local)
        # En publication stricte, aucun secours vers le CDN : fonctionnement
        # exclusivement avec les binaires locaux vérifiés pendant le build.
        if require_local:
            for relative in ('premiere/python-worker.js','terminale/python-worker.js'):
                target = OUTPUT / relative
                js = target.read_text(encoding='utf-8')
                old = 'const ALLOW_CDN_FALLBACK = true;'
                if js.count(old) != 1:
                    raise RuntimeError('Garde de secours réseau introuvable : ' + relative)
                target.write_text(js.replace(old,'const ALLOW_CDN_FALLBACK = false;'),encoding='utf-8')
        validate_publication()
        # Cette métadonnée est publique et ne contient aucune information élève.
        # Elle permet de comparer directement le site publié à la branche Git.
        provenance = {
            'source_commit': _source_revision(),
            'built_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'mode': 'pyodide-local-verifie' if require_local else 'developpement-cdn-autorise',
            'index_sha256': hashlib.sha256((OUTPUT / 'index.html').read_bytes()).hexdigest(),
        }
        (OUTPUT / 'orchestra-build.json').write_text(
            json.dumps(provenance, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
        files = [x for x in OUTPUT.rglob('*') if x.is_file()]
        return {'destination': str(OUTPUT), 'files': len(files),
                'pyodide_local_verified': local, 'source_commit': provenance['source_commit'],
                'size_bytes': sum(x.stat().st_size for x in files)}
    except BaseException:
        shutil.rmtree(OUTPUT, ignore_errors=True)
        raise


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--require-local-pyodide', action='store_true')
    mode.add_argument('--allow-cdn', action='store_true')
    args = p.parse_args()
    try:
        print(json.dumps(build(require_local=args.require_local_pyodide), ensure_ascii=False, indent=2))
    except (RuntimeError, OSError, ValueError) as exc:
        print(f'ERREUR DE PUBLICATION : {exc}', file=sys.stderr)
        sys.exit(1)
