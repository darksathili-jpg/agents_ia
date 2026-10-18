"""Ancien point d’entrée : construit uniquement U01.1."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('construire-u01.py')), run_name='__main__')
