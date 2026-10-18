"""Ancien point d’entrée : vérifie uniquement le parcours U01.1 courant."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('verifier-u01.py')), run_name='__main__')
