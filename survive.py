# Imports
import random
import time
from time import *

import math
import pygame
import sys
from pygame import image, mixer
from pygame.locals import *

# Initializing
pygame.init()

# Frames per Second festlegen
FPS = 60
clock = pygame.time.Clock()
mixer.set_num_channels(100)

# Farbwerte vordefinieren
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

START = 1
NORMAL_RUN = 2
BOSS_RUN = 3
LEVEL_ENDE = 4
SPIEL_ENDE = 5

Kanonen_x = [
    [59, 42, 36, 36, 72, 313, 304, 299, 275, 267, 260, 431, 204, 202, 444, 442, 114, 262, 408, 358, 358, 40,
     278, 35,
     263], [], [], []]
Kanonen_y = [
    [2127, 2369, 2451, 2545, 2683, 3782, 3925, 4064, 4677, 4825, 4958, 6240, 6273, 6337, 6396, 6464, 6629,
     6641, 6929,
     6977, 7043, 7331, 7343, 7558, 7571], [], [], [], []]
Background_Mapping = [3, 1, 2, 4]
Background_Count = [23, 23, 30, 56]
# Weitere Konstanten
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 809
SPEED = 5
SCORE = 0
LASERSPEED = 30
SCROLLSPEED = 2

Level = 1
Gegnergetroffen = 0

# Fonts festlegen
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Fenster erstellen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BLACK)
pygame.display.set_caption("Survive")
pygame.mouse.set_visible(False)
laserImages = [image.load('Laser/beam2.png'), image.load('Laser/beaml.png'), image.load('Laser/beamr.png'),
               image.load('Laser/beamdl.png'), image.load('Laser/beamdr.png')]
gegnerlaserImages = [image.load('Gegnerfeuer/1.png'), image.load('Gegnerfeuer/2.png'), image.load('Gegnerfeuer/3.png'),
                     image.load('Gegnerfeuer/4.png'), image.load('Gegnerfeuer/5.png'), image.load('Gegnerfeuer/20.png'),
                     image.load('Gegnerfeuer/boss1.png'), image.load('Gegnerfeuer/boss2.png'),
                     image.load('Gegnerfeuer/boss3.png'),
                     image.load('Gegnerfeuer/boss4.png'), ]
bonusImages = [image.load('Bonus/1.png'), image.load('Bonus/2.png'), image.load('Bonus/3.png'),
               image.load('Bonus/4.png'), image.load('Bonus/5.png'), image.load('Bonus/6.png'),
               image.load('Bonus/7.png'), image.load('Bonus/8.png'), image.load('Bonus/9.png'),
               image.load('Bonus/10.png'), image.load('Bonus/11.png')]
laserSounds = [mixer.Sound('Sounds/Laser0.wav'), mixer.Sound('Sounds/Laser1.wav'), mixer.Sound('Sounds/Laser1.wav'),
               mixer.Sound('Sounds/Laser4.wav'), mixer.Sound('Sounds/Laser4.wav'), ]
explosionSounds = [mixer.Sound('Explosionssounds/exp1.wav'), mixer.Sound('Explosionssounds/exp2.wav'),
                   mixer.Sound('Explosionssounds/exp3.wav'), mixer.Sound('Explosionssounds/exp4.wav'),
                   mixer.Sound('Explosionssounds/exp5.wav'), mixer.Sound('Explosionssounds/exp6.wav'),
                   mixer.Sound('Explosionssounds/exp7.wav'), mixer.Sound('Explosionssounds/exp8.wav'),
                   mixer.Sound('Explosionssounds/exp9.wav')]
bonusSounds = [mixer.Sound('Bonussounds/1.mp3'), mixer.Sound('Bonussounds/2.wav'), mixer.Sound('Bonussounds/3.mp3'),
               mixer.Sound('Bonussounds/4.wav'), mixer.Sound('Bonussounds/5.wav'), mixer.Sound('Bonussounds/6.mp3'),
               mixer.Sound('Bonussounds/7.wav'), mixer.Sound('Bonussounds/8.wav'), mixer.Sound('Bonussounds/9.mp3'),
               mixer.Sound('Bonussounds/10.wav'), mixer.Sound('Bonussounds/11.wav'),
               mixer.Sound('Bonussounds/Plopp.wav'), ]


class BgTile():
    def __init__(self, num, level):
        self.name = 'Backgrounds/' + str(Background_Mapping[level - 1]) + '-' + str(num) + '.png'
        # print(self.name)
        self.image = image.load(self.name)
        self.num = num
        self.level = level


class ScrollingBackground():
    def __init__(self):
        # Alle Images laden
        self.bgField = []
        for i in range(Background_Count[Level - 1]):
            self.bgField.append(BgTile(i, Level))

        self.bottomTile = 0
        self.topTile = -720
        self.movingDownSpeed = SCROLLSPEED
        self.bCounter = 0

    def update(self):
        global scroll_yPos, game_console
        self.bottomTile += self.movingDownSpeed
        self.topTile += self.movingDownSpeed
        scroll_yPos += self.movingDownSpeed
        game_console.updateProgress(scroll_yPos, Background_Count[Level - 1] * 720)

        if self.bottomTile >= 720:
            self.bottomTile = 0
            self.topTile = -720
            self.bCounter += 1

    def zeichnen(self):
        if self.bCounter + 1 < Background_Count[Level - 1]:
            screen.blit(self.bgField[self.bCounter + 1].image, (0, self.topTile + 38))
        else:
            screen.fill(BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.bCounter < Background_Count[Level - 1]:
            screen.blit(self.bgField[self.bCounter].image, (0, self.bottomTile + 38))


class Hero():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.mode = 0
        self.image = []
        self.leftCannon = 0
        self.rightCannon = 0
        self.doubleCannon = 0
        self.megabombrotatedImage = image.load("Bonus/8.png")
        self.megabombImage = pygame.transform.rotate(self.megabombrotatedImage, 180)
        self.rotatedImage = [image.load("Hero/Hero0.png"), image.load("Hero/Hero1.png"),
                             image.load("Hero/Hero2.png"), image.load("Hero/Hero3.png"),
                             image.load("Hero/Hero4.png"), image.load("Hero/Hero5.png"),
                             image.load("Hero/Hero6.png"), image.load("Hero/Hero7.png")]
        for i in range(8):
            self.image.append(pygame.transform.rotate(self.rotatedImage[i], 90))
            self.image[i] = pygame.transform.scale(self.image[i], (105, 90))
        self.height = self.image[0].get_height()
        self.width = self.image[0].get_width()
        self.firepower = 1
        self.shields = 1
        self.shieldspowered = 0
        self.megabomb = False
        self.lives = 4
        self.hidden = False
        self.hiddentime = 0
        self.unverwundbar = False
        self.unverwundbartime = 0

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        if self.y > 710:
            self.y = 710
        self.mode = self.leftCannon + self.rightCannon * 2 + self.doubleCannon * 4

    def zeichnen(self):
        if not self.hidden:
            if self.megabomb:
                screen.blit(self.megabombImage, (
                    self.x - int(self.megabombImage.get_width() / 2) + 2,
                    self.y - int(self.megabombImage.get_height() / 2) - 30))
            screen.blit(self.image[self.mode], (self.x - int(self.width / 2), self.y - int(self.height / 2)))
        else:
            self.hiddentime -= 1
            if self.hiddentime == 0:
                self.hidden = False
        if self.unverwundbartime > 0:
            self.unverwundbartime -=1
            if not (self.unverwundbartime/2) == int(self.unverwundbartime/2):
                self.hidden = True
            else:
                self.hidden = False
        else:
            self.unverwundbar = False

    def upgradefirepower(self):
        if self.firepower < 10:
            self.firepower += 1

    def installcannon(self, cannon):
        if cannon[0]:
            self.leftCannon = 1
        if cannon[1]:
            self.doubleCannon = 1
        if cannon[2]:
            self.rightCannon = 1

    def installmegabomb(self):
        self.megabomb = True

    def addlive(self):
        self.lives += 1

    def restoreshield(self):
        if self.shieldspowered < self.shields:
            self.shieldspowered += 1

    def upgradeshields(self):
        if self.shields < 4:
            self.shields += 1
        self.restoreshield()

    def treffer(self):
        global game_console
        if not self.unverwundbar:
            if self.shieldspowered > 0:
                self.shieldspowered -= 1
                game_console.update()
            else:
                self.zerstoeren()

    def zerstoeren(self):
        global explosionsAktiv
        explosionsAktiv.append(Explosion(self.x, self.y, 100, 8, 0))
        self.hidden = True
        self.unverwundbar = True
        self.unverwundbartime = 90
        self.hiddentime = 30
        self.lives -= 1
        if self.lives > 0:
            if self.firepower > 1:
                self.firepower += 1
        else:
            print('Game over')


class Laser():
    def __init__(self, typ, x, y, dx, dy, richtung):
        self.typ = typ
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.richtung = richtung
        self.rotatedImage = laserImages[typ]
        self.image = pygame.transform.rotate(laserImages[self.typ], self.richtung)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 0.8, self.image.get_height() * 0.8))
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.lasersound = laserSounds[self.typ]
        self.lasersound.set_volume(0.07)
        self.lasersound.play()

    def bewegen(self):
        self.x += self.dx
        self.y -= self.dy

    def zeichnen(self):
        screen.blit(self.image, (self.x - int(self.width / 2), self.y - int(self.height / 2)))


class Schuesse():
    global game_hero, laserAktiv

    def __init__(self):
        print(' Schüsse initialisiert')

    def feuer(self):

        laserAktiv.append(Laser(0, game_hero.x, game_hero.y - 56, 0, LASERSPEED * 0.5, 90))
        if game_hero.leftCannon:
            laserAktiv.append(Laser(1, game_hero.x - 43, game_hero.y - 14, LASERSPEED * -0.22, LASERSPEED * 0.42, 115))
        if game_hero.rightCannon:
            laserAktiv.append(Laser(2, game_hero.x + 43, game_hero.y - 14, LASERSPEED * 0.22, LASERSPEED * 0.42, 65))
        if game_hero.doubleCannon:
            laserAktiv.append(Laser(3, game_hero.x - 50, game_hero.y + 36, 0, LASERSPEED * 1.2, 90))
            laserAktiv.append(Laser(4, game_hero.x + 50, game_hero.y + 36, 0, LASERSPEED * 1.2, 90))


class Enemyfire():
    def __init__(self, typ, x, y, angle, speed):
        self.x = x
        self.y = y
        self.typ = typ
        self.angle = angle
        self.speed = speed
        self.image = gegnerlaserImages[self.typ - 1]
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.dx = math.cos(self.angle * math.pi / 180) * self.speed
        self.dy = -1 * math.sin(self.angle * math.pi / 180) * self.speed
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x += 2 * self.dx
        self.y += 2 * self.dy

    def update(self):
        self.x += self.dx
        self.y += self.dy + SCROLLSPEED

    def zeichnen(self):
        screen.blit(self.image, (self.x - int(self.width / 2), self.y - int(self.height / 2)))


class Enemy():
    def __init__(self, enemytyp, formation, fireTyp, drehbar, x, y, shield, speed):
        self.enemyTyp = enemytyp
        self.formation = formation
        self.fireTyp = fireTyp
        self.drehbar = drehbar
        self.speed = speed
        self.x = x
        self.y = y
        self.scalefaktor = [0, 40, 25, 40, 40, 40, 40, 40, 40, 40]
        if shield:
            self.shield = 's'
        else:
            self.shield = 'n'
        self.originalImage = pygame.image.load('Enemys/' + str(enemytyp) + self.shield + '.png')
        # self.originalImage = pygame.transform.rotate(self.originalImage, -90)
        self.image = self.originalImage
        self.remove = False

        self.originalImage = pygame.transform.scale(self.originalImage,
                                                    (self.scalefaktor[enemytyp] / 100 * self.originalImage.get_width(),
                                                     self.scalefaktor[
                                                         enemytyp] / 100 * self.originalImage.get_height()))
        self.image = self.originalImage
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.origin_x = 0
        self.origin_y = 0
        self.angle = -90
        self.feuerabstand = int(random.uniform(2000, 4000)) - Level / 2 * 800
        self.feuerzuletzt = 0

    def update(self):
        global game_hero, enemyfireAktiv

        if self.drehbar:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
            self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            self.image = pygame.transform.rotate(self.originalImage, int(self.angle))
            # self.rect = self.image.get_rect(center=(480, 400))
        else:
            self.image = pygame.transform.rotate(self.originalImage, self.angle)
        self.y += self.speed
        if self.formation == 1:
            self.x -= 6
        elif self.formation == 2:
            self.x += 6
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.origin_x = self.x - self.width / 2
        self.origin_y = self.y - self.height / 2
        if time() * 1000 - self.feuerzuletzt > self.feuerabstand:
            self.feuerzuletzt = time() * 1000
            enemyfireAktiv.append(Enemyfire(self.fireTyp, self.x, self.y, self.angle, int(random.uniform(10, 15))))

    def zeichnen(self):
        screen.blit(self.image, (self.origin_x, self.origin_y))
        image_rect = (self.x - self.width / 2, self.y - self.height / 2, self.width,
                      self.height)  # self.image.get_rect(center=(280, 300))


class Explosion():
    def __init__(self, x_pos, y_pos, size, exp_type, exp_downspeed):
        self.x = x_pos
        self.y = y_pos
        self.size = size
        self.exp_type = exp_type
        self.exp_downspeed = exp_downspeed
        self.image = []
        self.expImageCount = [0, 7, 19, 7, 17, 12, 16, 20, 11, 10, 7]
        self.expScale = [0, 0.7, 0.7, 0.7, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5]
        for i in range(self.expImageCount[exp_type]):
            tempimage = pygame.image.load('Explosions/' + str(self.exp_type) + '-' + str(i + 1) + '.png')
            tempimage = pygame.transform.scale(tempimage, (
                tempimage.get_width() * self.expScale[exp_type], tempimage.get_height() * self.expScale[exp_type]))
            self.image.append(tempimage)
        self.height = self.image[0].get_height()
        self.width = self.image[0].get_width()
        self.image_number = 0
        self.fertig = False
        self.expsound = explosionSounds[self.exp_type - 1]
        self.expsound.set_volume(0.25)
        self.expsound.play()
        self.frames = 0

    def bewegen(self):
        self.y += self.exp_downspeed

    def explode(self):
        self.frames += 1
        if self.frames > 1:
            self.frames = 0
            self.image_number += 1
        if self.image_number < self.expImageCount[self.exp_type]:
            self.height = self.image[self.image_number].get_height()
            self.width = self.image[self.image_number].get_width()
            screen.blit(self.image[self.image_number], (self.x - int(self.width / 2), self.y - int(self.height / 2)))
        else:
            self.fertig = True


class Kanone():
    def __init__(self, number):
        self.number = number
        self.typ = int(random.uniform(1, 5))
        self.drehbar = (int(random.uniform(1, 5)) == 1)
        self.kapazitaet = int(random.uniform(0, 4))
        self.feuerabstand = int(random.uniform(4000, 6000)) - Level / 2 * 1000
        self.feuerzuletzt = time() * 1000
        self.x = Kanonen_x[0][self.number] * 2  # erstes Feld später für Level
        self.y = scroll_yPos - Kanonen_y[0][self.number] * 2 + 38
        self.angle = int(random.uniform(-80, 10))
        if self.x > 240:
            self.angle = int(random.uniform(179, 260))
        self.origin_x = 0
        self.origin_y = 0
        self.width = 0
        self.height = 0
        self.originalImage = [pygame.image.load('Cannons/' + str(self.typ) + '1.png'),
                              pygame.image.load('Cannons/' + str(self.typ) + '2.png'),
                              pygame.image.load('Cannons/' + str(self.typ) + '3.png'),
                              pygame.image.load('Cannons/' + str(self.typ) + '4.png')]
        # self.originalImage = pygame.transform.rotate(self.originalImage, -90)
        self.remove = False

        for i in range(4):
            self.originalImage[i] = pygame.transform.scale(self.originalImage[i],
                                                           (0.4 * self.originalImage[i].get_width(),
                                                            0.4 * self.originalImage[i].get_height()))
            # if not self.drehbar:
            #     self.originalImage[i] = pygame.transform.rotate(self.originalImage[i], self.angle)
        self.image = self.originalImage[0]
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()

    def bewegen(self):
        global game_hero

        if self.drehbar:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
            self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            self.image = pygame.transform.rotate(self.originalImage[self.kapazitaet], int(self.angle))
        else:
            self.image = pygame.transform.rotate(self.originalImage[self.kapazitaet], self.angle)
        self.y += SCROLLSPEED
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.origin_x = self.x - self.width / 2
        self.origin_y = self.y - self.height / 2
        if time() * 1000 - self.feuerzuletzt > self.feuerabstand:
            self.feuerzuletzt = time() * 1000
            enemyfireAktiv.append(Enemyfire(6, self.x, self.y, self.angle, int(random.uniform(10, 15))))

    def zeichnen(self):
        screen.blit(self.image, (self.origin_x, self.origin_y))
        image_rect = (self.x - self.width / 2, self.y - self.height / 2, self.width,
                      self.height)  # self.image.get_rect(center=(280, 300))


class Bonus():
    def __init__(self):
        self.x = int(random.uniform(60, SCREEN_WIDTH - 60))
        self.y = -100
        self.typ = int(random.uniform(1, 9))
        self.bonussound = bonusSounds[self.typ - 1]
        self.bonussound.set_volume(1.0)
        self.bonusimage = bonusImages[self.typ - 1]
        self.width = self.bonusimage.get_width()
        self.height = self.bonusimage.get_height()

    def bewegen(self):
        self.y += SCROLLSPEED + 1
        self.rect = (self.x - self.width / 2, self.y - self.height / 2, self.width,
                     self.height)

    def zeichnen(self):
        screen.blit(self.bonusimage, (self.x, self.y))


class GameConsole():
    def __init__(self):
        self.x = 0
        self.y_fortschritt = 0
        self.y_rahmen = 758
        self.x_schilde = 395
        self.y_schilde = 777
        self.infoimage = image.load("Sonstiges/Rahmen.png")
        self.fortschrittimage = image.load("Sonstiges/fortschritt.png")
        self.shieldimage = image.load("Sonstiges/1-0.png")
        self.progressimage = image.load("Sonstiges/Progress.png")
        self.progress_x = 0

    def update(self):
        global game_hero
        self.shieldimage = image.load(
            "Sonstiges/" + str(game_hero.shields) + "-" + str(game_hero.shieldspowered) + ".png")

    def zeichnen(self):
        screen.blit(self.fortschrittimage, (self.x, self.y_fortschritt))
        screen.blit(self.progressimage, (self.progress_x, self.y_fortschritt + 4))
        screen.blit(self.infoimage, (self.x, self.y_rahmen))
        screen.blit(self.shieldimage, (self.x_schilde, self.y_schilde))

    def updateProgress(self, scrollPos, scrollMax):
        self.progress_x = 10 + (scrollPos / scrollMax) * 940


def bonusHandler():
    global game_hero, game_console, bonusAktiv, Gegnergetroffen

    heroRechteck = pygame.Rect(int(game_hero.x - game_hero.width / 2), int(game_hero.y - game_hero.height / 2) + 10,
                               game_hero.width, game_hero.height - 12)
    if Gegnergetroffen > 6 - Level:
        Gegnergetroffen = 0
        bonusAktiv.append(Bonus())

    for bonus in bonusAktiv:
        bonus.bewegen()
        bonus.zeichnen()
        bonusRechteck = pygame.Rect(int(bonus.x - bonus.width / 2) + 2, int(bonus.y - bonus.height / 2) + 2,
                                    bonus.width - 4,
                                    bonus.height - 4)
        if bonusRechteck.colliderect(heroRechteck):
            bonus.bonussound.play()
            if bonus.typ == 1:
                game_hero.upgradeshields()
                game_console.update()
            if bonus.typ == 2:
                game_hero.restoreshield()
                game_console.update()
            if bonus.typ == 3:
                game_hero.addlive()
                game_console.update()
            if bonus.typ == 4:
                game_hero.upgradefirepower()
            if bonus.typ == 5:
                game_hero.installcannon([1, 0, 0])
            if bonus.typ == 6:
                game_hero.installcannon([0, 0, 1])
            if bonus.typ == 7:
                game_hero.installcannon([0, 1, 0])
            if bonus.typ == 8:
                game_hero.installmegabomb()
            bonusAktiv.remove(bonus)


def explosionHandler():
    global explosionsAktiv
    for explosion in explosionsAktiv:
        if not explosion.fertig:
            explosion.explode()
            explosion.bewegen()
        else:
            explosionsAktiv.remove(explosion)


def enemyfireHandler():
    global enemyfireAktiv
    for enemyfire in enemyfireAktiv:
        if (enemyfire.y > 40) and (enemyfire.y < SCREEN_HEIGHT - 20) and (
                enemyfire.x > -20) and (enemyfire.x < SCREEN_WIDTH + 20):
            enemyfire.update()
            enemyfire.zeichnen()
        else:
            enemyfireAktiv.remove(enemyfire)


def enemyHandler():
    global enemyAktiv, lastWavePos
    waveDistance = int(random.uniform(160, 260)) + Level * 60
    if (scroll_yPos - lastWavePos) >= waveDistance:  # neue Gegenerwelle erzeugen
        lastWavePos = scroll_yPos
        typ = int(random.uniform(1, 10))
        fire_typ = int(random.uniform(1, 6))
        drehbar = (int(random.uniform(1, 4)) == 1)
        formation = int(random.uniform(1, 6))
        enemy_count = int(random.uniform(1, 4))
        dx = int(random.uniform(-20, 20))
        verschiebung = int(random.uniform(1, 100))
        x_start = 0
        y_start = 0

        for i in range(enemy_count):
            if formation == 1:
                # 1. Formation von rechts oben hintereinander schräg versetzt
                x_start = SCREEN_WIDTH + 80 * i - verschiebung
                y_start = 0 - 100 * i
            if formation == 2:
                x_start = -80 * i + verschiebung
                y_start = 0 - 100 * i
            if formation == 3:
                x_start = SCREEN_WIDTH / 2 + (dx + (90 - (90 * i)))
                y_start = 0 - (20 * ((i - (enemy_count - 1) / 2) * (i - ((enemy_count - 1) / 2))))
            if formation >= 4:
                x_start = int(random.uniform(80, SCREEN_WIDTH - 80))
                y_start = 0 - 100 * i
            enemyAktiv.append(
                Enemy(typ, formation, fire_typ, drehbar, x_start, y_start, False, int(random.uniform(4, 7))))

    for enemy in enemyAktiv:
        if enemy.y < SCREEN_HEIGHT - 20:
            enemy.update()
            enemy.zeichnen()
        else:
            enemyAktiv.remove(enemy)


def collisionHandler():
    global enemyAktiv, laserAktiv, explosionsAktiv, Gegnergetroffen

    heroRechteck = pygame.Rect(int(game_hero.x - game_hero.width / 2), int(game_hero.y - game_hero.height / 2) + 10,
                               game_hero.width, game_hero.height - 12)

    for enemyfire in enemyfireAktiv:
        enemyfireRechteck = pygame.Rect(int(enemyfire.x - enemyfire.width / 2) + 4,
                                        int(enemyfire.y - enemyfire.height / 2) + 4,
                                        enemyfire.width - 8,
                                        enemyfire.height - 8)
        if enemyfireRechteck.colliderect(heroRechteck):
            enemyfireAktiv.remove(enemyfire)
            game_hero.treffer()

    for enemy in enemyAktiv:
        enemyRechteck = pygame.Rect(int(enemy.x - enemy.width / 2) + 8, int(enemy.y - enemy.height / 2) + 8,
                                    enemy.width - 16,
                                    enemy.height - 16)
        for laser in laserAktiv:
            laserRechteck = pygame.Rect(int(laser.x - laser.width / 2) + 4, int(laser.y - laser.height / 2) + 4,
                                        laser.width - 8,
                                        laser.height - 8)

            if enemyRechteck.colliderect(laserRechteck):
                laserAktiv.remove(laser)
                enemy.remove = True
        if enemyRechteck.colliderect(heroRechteck):
            enemy.remove = True
            game_hero.treffer()

        if enemy.remove:
            explosionsAktiv.append(Explosion(enemy.x, enemy.y, 100, int(random.uniform(1, 8)), enemy.speed))
            enemyAktiv.remove(enemy)
            Gegnergetroffen += 1

    for kanone in kanonenAktiv:
        kanoneRechteck = pygame.Rect(int(kanone.x - kanone.width / 2) + 8, int(kanone.y - kanone.height / 2) + 8,
                                     kanone.width - 16,
                                     kanone.height - 16)

        for laser in laserAktiv:
            laserRechteck = pygame.Rect(int(laser.x - laser.width / 2) + 4, int(laser.y - laser.height / 2) + 4,
                                        laser.width - 8,
                                        laser.height - 8)

            if kanoneRechteck.colliderect(laserRechteck):
                laserAktiv.remove(laser)
                kanone.kapazitaet -= 1
        if kanoneRechteck.colliderect(heroRechteck):
            kanone.kapazitaet = -1
            game_hero.treffer()
        if kanone.kapazitaet < 0:
            kanone.remove = True
        if kanone.remove:
            explosionsAktiv.append(Explosion(kanone.x, kanone.y, 100, int(random.uniform(1, 8)), SCROLLSPEED))
            kanonenAktiv.remove(kanone)

    # Prüfe Kollision von Gegner mit Hero
    # pygame.draw.rect(screen, WHITE, heroRechteck,2)


def laserHandler():
    global laserAktiv
    for laser in laserAktiv:
        if laser.y > 0 and (laser.x > 0 and laser.x < 960):
            laser.bewegen()
        else:
            laserAktiv.remove(laser)


def backgroundHandler():
    global back_ground
    if back_ground.bCounter < len(back_ground.bgField):
        back_ground.update()
        back_ground.zeichnen()


def kanonenHandler():
    global kanonenAktiv, kanonenListcounter

    # Neue Kanone in Sichtweite?
    if len(Kanonen_y[0]) > kanonenListcounter:
        if Kanonen_y[0][kanonenListcounter] * 2 - scroll_yPos < 200:
            # nächste Kanone erzeugen
            kanonenAktiv.append(Kanone(kanonenListcounter))
            kanonenListcounter += 1
        for kan in kanonenAktiv:
            kan.bewegen()
            kan.zeichnen()
            if kan.y > SCREEN_HEIGHT - 20:
                kanonenAktiv.remove(kan)


back_ground = ScrollingBackground()
game_console = GameConsole()
game_hero = Hero()
game_schuesse = Schuesse()

game_Mode = NORMAL_RUN

laserAktiv = []
enemyAktiv = []
enemyfireAktiv = []
explosionsAktiv = []
kanonenAktiv = []
bonusAktiv = []

kanonenListcounter = 0

last_time = time() * 1000
scroll_yPos = 0
lastWavePos = 0

# Game Loop
while True:
    act_time = time() * 1000
    # Cycles through all occurring events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.mouse.set_visible(True)
            pygame.quit()
            sys.exit()
    if game_Mode == NORMAL_RUN:
        mouseButton = pygame.mouse.get_pressed()
        if mouseButton[0]:
            if (act_time - last_time) > 1000 / game_hero.firepower:
                game_schuesse.feuer()
                last_time = time() * 1000
        backgroundHandler()
        kanonenHandler()
        enemyHandler()
        enemyfireHandler()
        laserHandler()
        bonusHandler()
        game_hero.update()
        game_hero.zeichnen()

        collisionHandler()
        explosionHandler()

        for l in laserAktiv:
            l.zeichnen()
        # Gegner bewegen
        game_console.zeichnen()

    pygame.display.update()
    clock.tick(FPS)
