#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

# !/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3

"""
Icone sous Windows: il faut:
=> un xxx.ico pour integration dans le exe, avec "icon=xxx.ico"
=> un xxx.png pour integration avec PyQt4 + demander la recopie avec includefiles.
"""

import os
import sys

from cx_Freeze import setup, Executable

#############################################################################
# preparation des options

# chemins de recherche des modules
# ajouter d'autres chemins (absolus) si necessaire: sys.path + ["chemin1", "chemin2"]
path = sys.path + [os.path.abspath(".")]

# options d'inclusion/exclusion des modules
includes = ["pygame", "json", "requests", "tkinter", "psutil", "math", "tkinter.simpledialog", "tkinter.filedialog"]  # nommer les modules non trouves par cx_freeze
excludes = ["dpt"]
packages = []  # nommer les packages utilises

# copier les fichiers non-Python et/ou repertoires et leur contenu:
includefiles = ["dpt/"]


# detection de la version
def get_ver():
    sys.path.insert(0, os.path.pardir)
    from dpt.game import Game
    return Game.VERSION


if sys.platform == "win32":
    pass  # includefiles += [...] : ajouter les recopies specifiques à Windows
elif sys.platform == "linux2":
    pass  # includefiles += [...] : ajouter les recopies specifiques à Linux
else:
    pass  # includefiles += [...] : cas du Mac OSX non traite ici

# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]

# niveau d'optimisation pour la compilation en bytecodes
optimize = 0

# si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = False

# construction du dictionnaire des options
options = {
    "path": path,
    "includes": includes,
    "excludes": excludes,
    "packages": packages,
    "include_files": includefiles,
    "bin_path_includes": binpathincludes,
    "optimize": optimize,
    "silent": silent}

# pour inclure sous Windows les dll system de Windows necessaires
if sys.platform == "win32":
    options["include_msvcr"] = True

#############################################################################
# préparation des cibles
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # pour application graphique sous Windows  # base = "Console" # pour application en console
    # sous Windows

icone = None
if sys.platform == "win32":
    icone = "icone.ico"

cible_1 = Executable(script="main.py", base=base, icon=icone)

#############################################################################
# creation du setup
setup(name="Don't Play Together", version=get_ver(),
      description="Jeu vidéo anti-collaboratif",
      author="GamerMine, WhiteRed, Deleranax",
      options={
          "build_exe": options}, executables=[cible_1])
