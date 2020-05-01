.. DPT-Client documentation master file, created by
sphinx-quickstart on Fri May  1 15:21:13 2020.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive.

Ressources
==========

Principe
++++++++

Les `ressources` sont la deuxième partie importante du jeu avec le package ``dpt``. En effet, elles représentent tous les objets modifiables du jeu (textures, blocks, entitées...) ainsi que tous les différents niveaux.

Certaines `ressources` sont particulières car uniques et non réplicables :
   - `user/settings.json`
   - `user/profile.json`

.. important::
        Si les `ressources` sont modifiables et extensibles, elle font tout de même partie de la base du jeu et une modification érronée peut rendre le jeu inutilisable.

.. danger::
        De plus, il n'y a aucune sécurité lors de l'execution de `ressources`, ainsi n'installez pas de `ressources` sans être sûr de la source de celle-ci. (Les `ressources` peuvent executer toutes les fonctions inclues dans les packages figée lors du build du jeu, et donc peuvent être très dangeureuses). Nous ne pouvons pas garantir que les `ressources` distribuées par des tiers soient de confiance.
        
Notre gestionnaire de ressources :py:mod:`dpt.engine.loader` se base sur des `entrées` pour charger les ressources. Cette clé correspond à son chemin d'accès depuis le dossier :file:`%Dossier D'installation%/dpt/ressources`. Ce système permet de rajouter très simplement des ressources vu que dès qu'un nouveau fichier compatible est placé dans les sous dossiers de :file:`%Dossier D'installation%/dpt/ressources`, il est automatiquement repertorié.

Ensuite, il suffit d'ajouter la ressource à la liste de ressources à chargé (avec ``RessourceLoader.add_pending()``) et elle sera chargée lorsque que la fonction ``RessourceLoader.load()`` sera executée.

.. note::
        Si vous créez un addon, vous n'avez pas besoin d'executer ``RessourceLoader.load()`` car cela est directement géré lors du chargement du niveau (pour les blocs et entitées **uniquement**)

Création d'addons
+++++++++++++++++

.. note::
        La création d'addons requière d'avoir des connaissances de base dans la création de jeux avec Pygame. Cette documentation va simplement vous expliquer comment vous pouvez integrer vos addons au jeu.

..  _structure_ressources:

Structure des ressources
************************

Tout d'abord, vous devez créer un dossier qui sera la racine de votre addon. Il devra être placer dans le dossier des ressources (:file:`%Dossier D'installation%/dpt/ressources`). Il doit porter un nom ne contenant pas d'espaces et indiquant le nom d'une organisation/personne (dans ce cas, créer un sous dossier specifique à votre addon dans ce dossier) ou simplement le nom de votre addon.

Exemple :
   - :file:`addon1`
   - :file:`dwStd/addon1`

Ensuite, l'organisation interne au dossier est libre, vous pouvez l'organiser comme vous le souhaitez tant que vous respectez le sytème de nommage des fichiers (permet à notre gestionnaire de ressources de reconnaitre les ressources, voir :py:mod:`dpt.engine.loader`) :

.. important::
        Si vous ne respectez pas la structure necessaire, notre gestionnaire de ressources ne sera pas capable de reconnaitre et charger vos ressources. Ainsi, prêtez attention à cette partie.

+----------------+--------------------------+------------------+
| Type d'objet   | Type de fichier          | Nom nécessaire   |
+================+==========================+==================+
| Texture        | Image (*.png)                               |
+----------------+---------------------------------------------+
| Son (Effets)   | Son (*.ogg)                                 |
+----------------+--------------------------+------------------+
| Son (Musique)  | Son (*.ogg)              | *.music.ogg      |
+----------------+--------------------------+------------------+
| Niveau         | Document JSON (*.json)   | *.level.json     |
+----------------+--------------------------+------------------+
| Block          | Script Python (*.py)     | *.block.py       |
+----------------+--------------------------+------------------+
| Entitée        | Script Python (*.py)     | *.entity.py      |
+----------------+--------------------------+------------------+
| Police         | Fichier OpenType (*.otf) | *.otf            |
+----------------+--------------------------+------------------+

Création d'objets
*****************

Blocs
-----

.. tip::
        Pensez à aller regarder la :ref:`liste_ressources` et notre page GitHub (https://github.com/Deleranax/DPT-Client/tree/master/dpt/ressources/dpt) pour vous inspirer de notre travail, et donc pouvoir respecter la structure du programme (notment pour des collisions).

Tout d'abord, vous devez créer un fichier qui portera le même nom de que la classe de votre bloc (sans l'extension). Le nom du fichier Ce nom doit respecter la structure des noms (voir :ref:`structure_ressources`).

Cette classe devra comporter les éléments suivants :

.. code-block:: python

   class Block(pygame.sprite.Sprite):
      texture = "your.ressource.entry" # La clé d'entrée de la ressource de la texture
      textures = "your.ressource.entry" # La clé d'entrée des ressources des textures (pour les animations, optionnel)
      sounds = "your.ressource.entry" # La clé d'entrée des ressources des sons (à vous de définir l'utilisation)
      width = height = 0 # The width and 
      offset_x = 0
      offset_y = 0

      def __init__(self, x, y):
         """Créer un sprite du type Block

         :param x: Abscisse
         :type x: int
         :param y: Ordonnée
         :type y: int

         :rtype: pygame.sprite.Sprite
         """
         # Importatons locales
         from dpt.engine.tileManager import TileManager
         from dpt.engine.loader import RessourceLoader
         from dpt.game import Game
         
         pygame.sprite.Sprite.__init__(self, TileManager.environment_group) # Appelle du constructeur pygame, ici on doit specifier les groupes (voir Groupes de Sprite)
         self.image = RessourceLoader.get(self.texture) # Récupération de la texture (une fois chargée)
         self.image = pygame.transform.smoothscale(self.image, (self.width, self.height)) # Redimensionnage de la texture
         
         # Redimensionnage des textures (en cas d'utilisation de plusieurs textures pour une annimation par exemple, optionnel)
         self.images = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in RessourceLoader.get_multiple(self.textures)] 
         
         self.rect = self.image.get_rect() # Création du rectange
         self.rect.x = x + self.offset_x # Application de l'Offset
         self.rect.y = y + self.offset_y # Application de l'Offset
         
         # Ajout du bruit de placement (éditeur, optionnel)
         if not TileManager.loadlevel:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()
         
         self.mask = pygame.mask.from_surface(self.image) # Création du mask
		

.. warning::
        Si vous utilisez une annimation, vous devez vous même ajouter la gestion de cette annimation en définissant la fonction ``update(self)``

      
.. tip::
        Lorsque vous importez un module propre au jeu, pensez à faire une importation locale pour éviter les boucles d'importation. (Notament lorsque vous devez importer :py:mod:`dpt.loader.tileManager`)


Entitées
--------

.. tip::
        Pensez à aller regarder la :ref:`liste_ressources` et notre page GitHub (https://github.com/Deleranax/DPT-Client/tree/master/dpt/ressources/dpt) pour vous inspirer de notre travail, et donc pouvoir respecter la structure du programme (notment pour des collisions).

Tout d'abord, vous devez créer un fichier qui portera le même nom de que la classe de votre entitée (sans l'extension). Le nom du fichier doit respecter la structure des noms (voir :ref:`structure_ressources`).

Cette classe devra comporter les éléments suivants :

.. code-block:: python

   class Entity(pygame.sprite.Sprite):
      texture = "your.ressource.entry" # La clé d'entrée de la ressource de la texture
      textures = "your.ressource.entry" # La clé d'entrée des ressources des textures (pour les animations, optionnel)
      sounds = "your.ressource.entry" # La clé d'entrée des ressources des sons (à vous de définir l'utilisation)
      width = height = 0 # The width and 
      offset_x = 0
      offset_y = 0
      customPlacement = False # Définie si on peut placer l'entitée en dehors de la grille de placement (éditeur)

      def __init__(self, x, y):
         """Créer un sprite du type Entitée

         :param x: Abscisse
         :type x: int
         :param y: Ordonnée
         :type y: int

         :rtype: pygame.sprite.Sprite
         """
         # Importatons locales
         from dpt.engine.tileManager import TileManager
         from dpt.engine.loader import RessourceLoader
         from dpt.game import Game
         
         pygame.sprite.Sprite.__init__(self, TileManager.entity) # Appelle du constructeur pygame, ici on doit specifier les groupes (voir Groupes de Sprite)
         self.image = RessourceLoader.get(self.texture) # Récupération de la texture (une fois chargée)
         self.image = pygame.transform.smoothscale(self.image, (self.width, self.height)) # Redimensionnage de la texture
         
         # Redimensionnage des textures (en cas d'utilisation de plusieurs textures pour une annimation par exemple, optionnel)
         self.images = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in RessourceLoader.get_multiple(self.textures)] 
         
         self.rect = self.image.get_rect() # Création du rectange
         self.rect.x = x + self.offset_x # Application de l'Offset
         self.rect.y = y + self.offset_y # Application de l'Offset
         
         # Ajout du bruit de placement (éditeur, optionnel)
         if not TileManager.loadlevel:
            self.sound = RessourceLoader.get(self.sounds)
            self.sound.set_volume(Game.settings["sound_volume"] * Game.settings["general_volume"])
            self.sound.play()
         
         self.mask = pygame.mask.from_surface(self.image) # Création du mask
         
    def update(self, *args, **kwargs):
        """Actualise les sprites

        :param args: Arguments spécifique
        :param kwargs: Arguments spécifique
        """
		

.. warning::
        Si vous utilisez une annimation, vous devez vous même ajouter la gestion de cette annimation en définissant la fonction ``update(self)``. De plus, contrairement au blocs, vous devez gérer les collision vous même dans cette même fonction.

      
.. tip::
        Lorsque vous importez un module propre au jeu, pensez à faire une importation locale pour éviter les boucles d'importation. (Notament lorsque vous devez importer :py:mod:`dpt.loader.tileManager`)
        

.. _liste_ressources:

Liste des ressources
++++++++++++++++++++

.. toctree::
   :maxdepth: 1
   :glob:
   
   autoapi/*/block/*
   autoapi/*/entity/*
