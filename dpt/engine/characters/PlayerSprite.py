import pygame
import math
import time
from dpt.game import Game
from dpt.engine.loader import RessourceLoader
from dpt.engine.tileManager import TileManager
from dpt.engine.gui.ui.Heart import Heart
from dpt.engine.effectsManagement import EffectsManagement


class PlayerSprite(pygame.sprite.Sprite):
    """Gère le fonctionnement du joueur et sa physique plus particulièrement"""
    char = "dpt.images.characters.player.standing"
    walk_right_textures = "dpt.images.characters.player.R-*"
    walk_left_textures = "dpt.images.characters.player.L-*"
    jump_right_texture = "dpt.images.characters.player.RJump"
    jump_left_texture = "dpt.images.characters.player.LJump"
    mask = "dpt.images.characters.player.mask"

    accessories = {
        "HappyLeft": "dpt.images.characters.player.accessories.Eye_L_Happy",
        "HappyRight": "dpt.images.characters.player.accessories.Eye_R_Happy",
        "MadLeft": "dpt.images.characters.player.accessories.Eye_L_Mad",
        "MadRight": "dpt.images.characters.player.accessories.Eye_R_Mad",
        "OpenLeft": "dpt.images.characters.player.accessories.Eye_L_Open",
        "OpenRight": "dpt.images.characters.player.accessories.Eye_R_Open",
        "SquintLeft": "dpt.images.characters.player.accessories.Eye_L_Squint",
        "SquintRight": "dpt.images.characters.player.accessories.Eye_R_Squint",
        "HatLeft": "dpt.images.characters.player.accessories.Hat_L",
        "HatRight": "dpt.images.characters.player.accessories.Hat_R",
    }

    available_expressions = [
        "Open",
        "Squint",
        "Mad",
        "Happy"
    ]

    def __init__(self, x, y):
        """Crée un joueur

        :param x: Abscisse
        :type x: int
        :param y: Ordonnée
        :type y: int

        :rtype: PlayerSprite
        """
        pygame.sprite.Sprite.__init__(self, Game.player_group)  # Sprite's constructor called
        self.width = math.floor(156 * Game.DISPLAY_RATIO)
        self.height = math.floor(156 * Game.DISPLAY_RATIO)
        self.CONSTWIDTH = self.width
        self.CONSTHEIGT = self.height
        self.image = pygame.transform.scale(RessourceLoader.get(self.char), (self.width, self.height))
        self.walkLeft = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in
                         RessourceLoader.get_multiple(self.walk_left_textures)]
        self.jumpLeft = pygame.transform.smoothscale(RessourceLoader.get(self.jump_left_texture), (self.width, self.height))

        self.walkRight = [pygame.transform.smoothscale(i, (self.width, self.height)) for i in
                          RessourceLoader.get_multiple(self.walk_right_textures)]
        self.jumpRight = pygame.transform.smoothscale(RessourceLoader.get(self.jump_right_texture), (self.width, self.height))

        self.accessories_images = {k: pygame.transform.smoothscale(RessourceLoader.get(v), (self.width, self.height)) for k, v in PlayerSprite.accessories.items()}
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xvel = 0
        self.yvel = 0
        self.left = True
        self.right = False
        self.standing = False
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 23
        self.CONSTJUMPCOUNT = self.jumpCount
        self.onPlatform = False
        self.allowJump = True
        self.mask = pygame.mask.from_surface(pygame.transform.scale(RessourceLoader.get(PlayerSprite.mask),
                                                                    (self.width, self.height)))
        self.gravityCount = 0
        self.gravity = 0
        self.imunityTime = 180
        self.alive = True
        self.damaged = False
        self.frameCount = 0
        self.gravityModifier = 0
        self.maxvelocity = 4
        self.jumpModifier = 0
        self.isReallyInJump = False
        self.fallCount = 0

        self.blink = False

        self.hat = True
        self.current_eye = "Open"
        self.blink_eye = 0

        self.eye_count = 0

        Heart()

    def update(self):
        """Actualise les effets, les déplacements, les collisions, sa santé"""
        if self.alive:

            if EffectsManagement.dico_current_effects["Fast"]:
                self.maxvelocity = 6
            else:
                self.maxvelocity = 4

            if EffectsManagement.dico_current_effects["lowGravity"]:
                self.gravityModifier = 0.04
            else:
                self.gravityModifier = 0

            if EffectsManagement.dico_current_effects["Slow"]:
                if self.isJump:
                    self.isReallyInJump = True
                if not self.isReallyInJump:
                    self.frameCount = 0
                    self.fallCount += 1
                    self.isJump = False
                else:
                    self.frameCount += 1
                    if self.jumpCount > 0:
                        self.fallCount = 0
                    else:
                        self.fallCount += 1

            if EffectsManagement.dico_current_effects["jumpBoost"]:
                self.jumpModifier = 0.07
            else:
                self.jumpModifier = 0

            keys = pygame.key.get_pressed()
            mur = -TileManager.camera.last_x

            Game.add_debug_info("Player.damaged = " + str(self.damaged))
            Game.add_debug_info("Player.xvel = " + str(self.xvel))
            Game.add_debug_info("Player.yvel = " + str(self.yvel))
            Game.add_debug_info("Player.jumpCount = " + str(self.jumpCount))
            Game.add_debug_info("Player.isJump = " + str(self.isJump))
            Game.add_debug_info("Player.fallCount = " + str(self.fallCount))

            if EffectsManagement.dico_current_effects["inversion"]:
                left = pygame.K_RIGHT
                right = pygame.K_LEFT
                up = pygame.K_DOWN
                leftLetter = pygame.K_d
                rightLetter = pygame.K_q
                upLetter = pygame.K_s
            else:
                left = pygame.K_LEFT
                right = pygame.K_RIGHT
                up = pygame.K_UP
                leftLetter = pygame.K_q
                rightLetter = pygame.K_d
                upLetter = pygame.K_z

            if (keys[left] or keys[leftLetter]) and self.rect.x - self.xvel - 1 > mur:
                if self.xvel > 0 and not EffectsManagement.dico_current_effects["Ice"]:
                    self.xvel = 0
                if -self.maxvelocity * Game.DISPLAY_RATIO > self.xvel > -self.maxvelocity * 2 * Game.DISPLAY_RATIO and self.onPlatform:
                    self.xvel += self.xvel * 0.01
                if self.xvel >= -self.maxvelocity * Game.DISPLAY_RATIO:
                    self.xvel -= 0.25 * Game.DISPLAY_RATIO
                self.left = True
                self.right = False
                self.standing = False
            elif keys[right] or keys[rightLetter]:
                if self.xvel < 0 and not EffectsManagement.dico_current_effects["Ice"]:
                    self.xvel = 0
                if self.maxvelocity * Game.DISPLAY_RATIO < self.xvel < self.maxvelocity * 2 * Game.DISPLAY_RATIO and self.onPlatform:
                    self.xvel += self.xvel * 0.01
                if self.xvel <= self.maxvelocity * Game.DISPLAY_RATIO:
                    self.xvel += 0.25 * Game.DISPLAY_RATIO
                self.left = False
                self.right = True
                self.standing = False
            else:
                if not EffectsManagement.dico_current_effects["Ice"]:
                    self.xvel = 0
                else:
                    if self.xvel > 0.05 * Game.DISPLAY_RATIO:
                        self.xvel -= 0.05 * Game.DISPLAY_RATIO
                    elif self.xvel < -0.05 * Game.DISPLAY_RATIO:
                        if self.rect.x - self.xvel - 1 > mur:
                            self.xvel += 0.05 * Game.DISPLAY_RATIO
                        else:
                            self.xvel = 0
                    else:
                        self.xvel = 0
                self.standing = True
                self.walkCount = 0
            if self.allowJump:
                if not self.isJump:
                    if keys[up] or keys[upLetter]:
                        self.isJump = True
                        self.walkCount = 0
                        self.onPlatform = False
                else:
                    if not self.onPlatform:
                        if (self.jumpCount >= 0 and not EffectsManagement.dico_current_effects["Slow"]) or (EffectsManagement.dico_current_effects["Slow"] and self.frameCount % 3 == 0):
                            self.yvel = math.floor((self.jumpCount ** 2) * (0.05 + self.gravityModifier + self.jumpModifier) * Game.DISPLAY_RATIO)
                            self.jumpCount -= 1
                        elif self.jumpCount < 0:
                            if self.isReallyInJump:
                                self.isJump = True
                            else:
                                self.isJump = False
                        else:
                            self.yvel = 0

            if not self.isJump or self.jumpCount < 0:
                if (EffectsManagement.dico_current_effects["Slow"] and self.fallCount % 3 == 0) or not EffectsManagement.dico_current_effects["Slow"]:
                    Game.add_debug_info("GRAVITY")
                    self.allowJump = False
                    self.gravityCount += 1
                    self.gravity = math.floor((self.gravityCount ** 2) * (0.05 - self.gravityModifier) * Game.DISPLAY_RATIO) * -1
                    self.yvel = self.gravity
                else:
                    self.yvel = 0

            self.collide()

            self.rect.left += math.floor(self.xvel)
            self.rect.top -= math.floor(self.yvel)

            self.animation()
            self.enemies_collision(self.yvel, TileManager.enemy_group)
            if not EffectsManagement.dico_current_effects["star"]:
                self.deadly_object_collision()
            if self.damaged:
                self.imunityTime -= 1
                Game.life = 2
            else:
                self.imunityTime = 180
                Game.life = 1

            if self.imunityTime % 7 == 0 and self.imunityTime > 0 and self.damaged:
                self.blink = not self.blink
            elif self.imunityTime < 0:
                self.blink = False

            if self.blink:
                self.image = pygame.Surface((self.rect.width, self.rect.height)).convert_alpha()
                self.image.fill((0, 0, 0, 0))
        else:
            self.die()
        self.death_fall()

    def animation(self):
        """Change l'image du joueur pour donner l'illusion de déplacement"""
        add = abs(math.floor(self.xvel / (self.maxvelocity // 4)))
        if self.walkCount + add >= 180:
            self.walkCount = 0

        if self.onPlatform:
            if self.current_eye == "Happy":
                self.current_eye = "Open"
            if not self.standing:
                if self.left:
                    self.image = self.walkLeft[self.walkCount // 12 + 1]
                    self.walkCount += add
                elif self.right:
                    self.image = self.walkRight[self.walkCount // 12 + 1]
                    self.walkCount += add
            else:
                if self.right:
                    self.image = self.walkRight[0]
                else:
                    self.image = self.walkLeft[0]
        else:
            self.current_eye = "Happy"
            if self.right:
                self.image = self.jumpRight
            else:
                self.image = self.jumpLeft

        self.image = self.image.copy()

        if self.hat:
            if self.right:
                self.image.blit(self.accessories_images["HatRight"], (0, 0))
            else:
                self.image.blit(self.accessories_images["HatLeft"], (0, 0))

        direction = "Left"
        if self.right:
            direction = "Right"

        if self.blink_eye < 0:
            self.image.blit(self.accessories_images[self.current_eye + direction], (0, 0))
        elif self.blink_eye > 8:
            self.image.blit(self.accessories_images["Squint" + direction], (0, 0))
        elif self.blink_eye < 2:
            self.image.blit(self.accessories_images["Squint" + direction], (0, 0))

        if self.blink_eye < -180:
            self.blink_eye = 10

        Game.add_debug_info(str(self.blink_eye))
        self.blink_eye -= 1

    def collide(self):
        """Gère toute la partie physique du joueur, l'empêche de traverser les blocs"""
        for i in TileManager.environment_group:
            if i.rect.colliderect(Game.display_rect):
                rx = i.rect.x - (self.rect.x + math.floor(self.xvel))
                ry = i.rect.y - (self.rect.y - math.floor(self.yvel))

                if self.mask.overlap(i.mask, (rx, ry)):
                    dx = 0
                    dy = 0

                    if math.floor(self.yvel) == 0:
                        mask = self.mask.overlap_mask(i.mask, (rx, ry))
                        b_rects = mask.get_bounding_rects()
                        for rect in b_rects:
                            if -8 * Game.DISPLAY_RATIO <= rect.height <= 8 * Game.DISPLAY_RATIO:
                                dy = rect.height
                                self.yvel = 0
                                self.onPlatform = True
                                self.gravityCount = 0
                                self.isJump = False
                                self.allowJump = True
                                self.isReallyInJump = False
                                self.jumpCount = self.CONSTJUMPCOUNT
                                self.frameCount = 0
                            break

                    crx = i.rect.x - self.rect.x
                    mask = self.mask.overlap_mask(i.mask, (crx, ry))
                    b_rects = mask.get_bounding_rects()
                    for rect in b_rects:
                        if self.rect.centery < i.rect.y:
                            dy = rect.height + math.floor(self.yvel)
                            self.yvel = 0
                            self.onPlatform = True
                            self.gravityCount = 0
                            self.isJump = False
                            self.isReallyInJump = False
                            self.allowJump = True
                            self.jumpCount = self.CONSTJUMPCOUNT
                            self.frameCount = 0
                        elif self.rect.centery > i.rect.y:
                            dy = - rect.height + math.floor(self.yvel)
                            self.yvel = 0
                            self.isJump = False
                            self.isReallyInJump = False
                            self.allowJump = False
                            self.jumpCount = self.CONSTJUMPCOUNT
                        break

                    self.rect.y -= dy

                    cry = (i.rect.y - self.rect.y)
                    mask = self.mask.overlap_mask(i.mask, (rx, cry))
                    b_rects = mask.get_bounding_rects()
                    for rect in b_rects:
                        Game.add_debug_info("dx = " + str(dx))
                        if self.rect.x > i.rect.x:
                            dx = rect.width + math.floor(self.xvel)
                            self.xvel = 0
                        elif self.rect.x < i.rect.x:
                            dx = - rect.width + math.floor(self.xvel)
                            self.xvel = 0
                        break

                    self.rect.x += dx

    def deadly_object_collision(self):
        """Gère les collisions avec des objets physiques mortels"""
        for i in TileManager.deadly_object_group:
            if pygame.sprite.collide_mask(self, i):
                if self.damaged:
                    if self.imunityTime < 0:
                        self.alive = False
                        self.yvel = 0
                        Game.freeze_game = True
                        self.xvel = 0
                        time.sleep(0.5)
                        self.die()
                        self.jumpCount = self.CONSTJUMPCOUNT
                else:
                    self.isJump = True
                    self.walkCount = 0
                    self.onPlatform = False
                    self.damaged = True
                    self.allowJump = True
                    self.gravityCount = 0

    def enemies_collision(self, yVelDelta, enemies):
        """Gère les collisions avec des ennemis, permet de les tuer"""
        for i in enemies:
            if pygame.sprite.collide_mask(self, i):
                if yVelDelta < 0 and not EffectsManagement.dico_current_effects["monsterimmortal"]:
                    if self.damaged and self.imunityTime < 120:
                        i.kill()
                    elif not self.damaged:
                        i.kill()
                else:
                    if self.damaged and not EffectsManagement.dico_current_effects["star"]:
                        if self.imunityTime < 0:
                            self.alive = False
                            self.yvel = 0
                            Game.freeze_game = True
                            self.xvel = 0
                            time.sleep(0.5)
                            self.die()
                            self.jumpCount = self.CONSTJUMPCOUNT
                    elif EffectsManagement.dico_current_effects["star"]:
                        i.kill()
                    else:
                        self.isJump = True
                        self.walkCount = 0
                        self.onPlatform = False
                        self.damaged = True
                        self.allowJump = True
                        self.gravityCount = 0

    def die(self):
        """Animation de mort"""
        Game.life = 3
        self.alive = False
        if self.jumpCount > 0:
            neg = 1
        else:
            neg = -1
        self.yvel = math.floor((self.jumpCount ** 2) * 0.05 * Game.DISPLAY_RATIO) * neg
        self.jumpCount -= 1
        self.rect.top -= self.yvel

    def death_fall(self):
        """Tue le joueur s'il sort de l'écran"""
        if self.rect.top >= Game.WINDOW_HEIGHT:
            Game.get_logger("Player").info("Player sprite killed")
            Game.freeze_game = True

            from dpt.engine.scenes import Scenes
            Scenes.game_over()

            Game.player_sprite.kill()
            del self

    def kill(self):
        pygame.event.post(pygame.event.Event(Game.PLAYER_DEATH_EVENT, {}))
        pygame.sprite.Sprite.kill(self)
