from cx_Freeze import setup, Executable


def get_ver():
    from dpt.game import Game
    return Game.VERSION


# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=[], excludes=[])

import sys

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [Executable('dpt/main.py', base=base)]

setup(name="Don't Play Together", version='ALPHA-0.3.4', description='Jeu anti-collaboratif', options=dict(build_exe=buildOptions), executables=executables)
