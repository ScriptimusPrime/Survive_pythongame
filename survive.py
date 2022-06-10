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
clock = pygame.time.Clock()
mixer.set_num_channels(100)

import sys

from Konstanten import *
from Images import *
from Sounds import *



BUTTON_UP_PRESSED = USEREVENT + 1
BUTTON_DOWN_PRESSED = USEREVENT + 2
BUTTON_START_PRESSED = USEREVENT + 3
LEVEL_ENDE_EVENT = USEREVENT + 4
SPIEL_ENDE_EVENT = USEREVENT + 5

# Fonts festlegen
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Fenster erstellen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BLACK)
pygame.display.set_caption("Survive")
screen.blit(pygame.transform.scale(image.load('Sonstiges/Titel.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

pygame.display.update()
pygame.mouse.set_visible(False)



laserAktiv = []
enemyAktiv = []
enemyfireAktiv = []
explosionsAktiv = []
kanonenAktiv = []
bonusAktiv = []
minesAktiv = []
meteorsAktiv = []
bosskanonenAktiv = []


class Game():
    def __init__(self):
        self.kanonenListcounter = None
        self.timeOfLastEnemyWave = None
        self.timeTillNewWave = None
        self.timeOfLastMine = None
        self.timeTillNewMine = None
        self.timeOfLastMeteor = None
        self.timeTillNewMeteor = None
        self.timeLastShot = None
        self.Mode = START
        self.showLevel = None
        self.Level = 1
        self.Gegnergetroffen = None
        self.smallbonusavailable = None
        self.mediumbonusavailable = None
        self.largebonusavailable = None

    def levelinit(self):
        self.kanonenListcounter = 0
        self.timeOfLastEnemyWave = now() + int(random.uniform(2000,3000))
        self.timeTillNewWave = int(random.uniform(1500, 2500))+self.Level*300
        self.timeOfLastMine = now() + int(random.uniform(10000,15000))
        self.timeTillNewMine = int(random.uniform(20000, 25000)) - self.Level * 2000
        self.timeOfLastMeteor = now() + int(random.uniform(10000,15000))
        self.timeTillNewMeteor = int(random.uniform(10000, 14000)) - self.Level * 500
        self.timeLastShot = now()
        self.showLevel = True
        self.Gegnergetroffen = 0
        self.smallbonusavailable = True
        self.mediumbonusavailable = True
        self.largebonusavailable = True

    def setzeMode(self,mode):
        self.Mode = mode

    def erhoeheLevel(self):
        self.Level += 1

    def erhoeheklc(self):
        self.kanonenListcounter += 1

    def resetGegnergetroffen(self):
        self.Gegnergetroffen = 0

    def erhoeheGegnergetroffen(self):
        self.Gegnergetroffen += 1

    def setzemeteortime(self):
        self.timeOfLastMeteor = now()
        self.timeTillNewMeteor = int(random.uniform(10000, 20000))

    def setzeminetime(self):
        self.timeOfLastMine = now()
        self.timeTillNewMine = int(random.uniform(10000, 15000))

    def setzewavetime(self):
        self.timeOfLastEnemyWave = now()  # aktuelle Zeit als neuen Bezugspunkt festlegen
        self.timeTillNewWave = int(random.uniform(4000, 6000) - self.Level * 700)  # Zufallszeitspanne bis zu nächster Welle festlegen


class BgTile():
    def __init__(self, num, level):
        self.name = 'Backgrounds/' + str(Background_Mapping[level - 1]) + '-' + str(num) + '.png'
        self.image = image.load(self.name)
        self.num = num
        self.level = level


def playBackgroundSongs(level):
        mixer.music.load(ingamemusicSounds[level - 1])
        mixer.music.set_volume(0.2)
        mixer.music.play(-1,0,0)

def stopBackgroundSongs():
        mixer.music.stop()


class ScrollingBackground():
    def __init__(self):
        # Alle Images laden
        self.bgField = []
        self.bottomTile = 0
        self.topTile = -720
        self.movingDownSpeed = SCROLLSPEED
        self.bCounter = 0
        self.scroll_yPos = None

    def loadlevel(self, level):
        self.scroll_yPos = 0
        self.bCounter = 0
        self.bottomTile = 0
        self.topTile = -720
        del self.bgField[:]
        for i in range(Background_Count[level - 1]):
            self.bgField.append(BgTile(i, level))

    def update(self):
        if self.bCounter < Background_Count[game.Level - 1]:
            self.bottomTile += self.movingDownSpeed
            self.topTile += self.movingDownSpeed
            self.scroll_yPos += self.movingDownSpeed
            game_console.updateProgress(self.scroll_yPos, Background_Count[game.Level - 1] * 720)

            if self.bottomTile >= 720:
                self.bottomTile = 0
                self.topTile = -720
                self.bCounter += 1

    def zeichnen(self):
        if self.bCounter < Background_Count[game.Level - 1] - 1:
            screen.blit(self.bgField[self.bCounter + 1].image, (0, self.topTile + 38))
            screen.blit(self.bgField[self.bCounter].image, (0, self.bottomTile + 38))
        else:
            screen.fill(BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            if game.Mode == NORMAL_RUN:
                game.setzeMode(BOSS_ENTER)


class Hero():
    def __init__(self):
        self.aktiv = True
        self.x = 0
        self.y = 0
        self.mode = 0
        self.image = []
        self.leftCannon = 0
        self.rightCannon = 0
        self.doubleCannon = 0
        self.megabombrotatedImage = image.load("Bonus/8.png")
        self.megabombImage = pygame.transform.rotate(self.megabombrotatedImage, 180)
        self.rotatedImage = (image.load("Hero/Hero0.png"), image.load("Hero/Hero1.png"),
                             image.load("Hero/Hero2.png"), image.load("Hero/Hero3.png"),
                             image.load("Hero/Hero4.png"), image.load("Hero/Hero5.png"),
                             image.load("Hero/Hero6.png"), image.load("Hero/Hero7.png"))
        for i in range(8):
            self.image.append(pygame.transform.rotate(self.rotatedImage[i], 90))
            self.image[i] = pygame.transform.scale(self.image[i], (105, 90))
        self.height = self.image[0].get_height()
        self.width = self.image[0].get_width()
        self.firepower = 1
        self.shields = 1
        self.shieldspowered = 1
        self.megabomb = False
        self.lives = 4
        self.points = 0
        self.hidden = False
        self.timehidden = 0
        self.unverwundbar = False
        self.timeunverwundbar = 0
        self.blink = 0
        self.shieldOriginalImage = schutzschildImages[0]
        self.shieldImage = self.shieldOriginalImage
        self.shieldwidth = 0
        self.shieldheight = 0
        self.shieldrotate = 0
        self.lasersound = laserSounds[0]
        self.sidelasersound = laserSounds[1]
        self.doublelasersound = laserSounds[2]
        self.rot_rect = 0
        self.orig_rect = 0

    def upgrade(self, typ):
        self.shields = 4
        self.shieldspowered = 4
        if typ == SMALL:
            self.leftCannon = 1
            if self.firepower < 3:
                self.firepower = 3
        elif typ == MEDIUM:
            self.leftCannon = 1
            self.rightCannon = 1
            if self.firepower < 4:
                self.firepower = 4
        elif typ == LARGE:
            self.leftCannon = 1
            self.rightCannon = 1
            self.doubleCannon = 1
            if self.firepower < 6:
                self.firepower = 6

    def moveout(self):
        self.y -= 15

    def setzepos(self, pos):
        self.x = pos[0]
        self.y = pos[1]


    def update(self, ingame):
        if ingame:
            self.x, self.y = pygame.mouse.get_pos()
            if self.y > 710:
                self.y = 710
        self.mode = self.leftCannon + self.rightCannon * 2 + self.doubleCannon * 4
        # Drehe Schutzschild weiter
        self.shieldOriginalImage = schutzschildImages[self.shieldspowered]  # Ausgangspunkt immer vom Originalimage nehmen
        self.shieldrotate += 2
        self.shieldImage = pygame.transform.rotate(self.shieldOriginalImage, self.shieldrotate)
        # neue Breite und Höhe des gedrehten Images bestimmen
        self.shieldwidth = self.shieldImage.get_width()
        self.shieldheight = self.shieldImage.get_height()

    def zeichnen(self):
        if not self.hidden:
            # Raumschiff zeichnen
            if self.megabomb:  # ggf.mit Megabombe darunter zeichnen
                screen.blit(self.megabombImage, (
                    self.x - int(self.megabombImage.get_width() / 2) + 2,
                    self.y - 110))
            screen.blit(self.image[self.mode], (self.x - int(self.width / 2), self.y - int(self.height / 2)))
            screen.blit(self.shieldImage, (self.x + 3 - int(self.shieldwidth / 2), self.y + 5 - int(self.shieldheight / 2)))

        if self.timehidden > 0:
            self.aktiv = False
            self.timehidden -= 1
            if self.timehidden == 0:
                self.aktiv = True
                self.unverwundbar = True
                self.timeunverwundbar = 120
                self.hidden = False
        if self.unverwundbar:
            self.timeunverwundbar -= 1
            self.blink -= 1
            if self.blink < 1:
                self.blink = 4
                self.hidden = not self.hidden
            if self.timeunverwundbar == 0:
                self.unverwundbar = False
                self.hidden = False

    def upgradefirepower(self):
        if self.firepower < 6:
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

    def looselive(self):
        self.lives -= 1
        if self.lives == 0:
            game.setzeMode(GAME_OVER)

    def upgradeshields(self):
        if self.shields < 4:
            self.shields += 1
        self.restoreshield()

    def restoreshield(self):
        if self.shieldspowered < self.shields:
            self.shieldspowered += 1
        self.updateshield()

    def updateshield(self):
        self.shieldOriginalImage = schutzschildImages[self.shieldspowered]

    def treffer(self):
        if self.megabomb:
            self.zuendeMegabombe()
        elif not self.hidden or not self.unverwundbar:
            if self.shieldspowered > 0:
                self.shieldspowered -= 1
                self.updateshield()
                game_console.update()
            else:
                self.zerstoeren()

    def zerstoeren(self):
        explosionsAktiv.append(Explosion(self.x, self.y, 1, 8, 0))
        self.hidden = True
        self.aktiv = False
        self.timehidden = 45
        self.looselive()
        if self.lives > 0:
            if self.firepower > 1:
                self.firepower -= 1
        else:
            print('Game over')

    def has_megabomb(self):
        return self.megabomb

    def zuendeMegabombe(self):
        self.megabomb = False
        explosionsAktiv.append(Explosion(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100, 2.5, 9, 0))
        for enemy in enemyAktiv:
            enemy.zerstoeren(POINTS_YES)
        for enemyfire in enemyfireAktiv:
            enemyfire.aufloesen()
        for kanone in kanonenAktiv:
            kanone.zerstoeren()
        for mine in minesAktiv:
            mine.zerstoeren(POINTS_YES)
        for meteor in meteorsAktiv:
            meteor.zerstoeren()

    def addPoints(self, p):
        self.points += p


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
        self.remove = False

    def bewegen(self):
        self.x += self.dx
        self.y -= self.dy

    def zeichnen(self):
        screen.blit(self.image, (self.x - int(self.width / 2), self.y - int(self.height / 2)))

    def zerstoeren(self):
        explosionsAktiv.append(Explosion(self.x, self.y, 0.3, 1, 0))
        self.aufloesen()

    def aufloesen(self):
        self.remove = True


class Enemyfire():
    def __init__(self, typ, x, y, angle, speed, downspeed):
        self.x = x
        self.y = y
        self.typ = typ
        self.angle = angle
        self.speed = speed
        self.downspeed = downspeed
        self.image = gegnerlaserImages[self.typ - 1]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 0.75, self.image.get_height() * 0.75))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.dx = math.cos(self.angle * math.pi / 180) * self.speed
        self.dy = -1 * math.sin(self.angle * math.pi / 180) * self.speed
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x += 2 * self.dx
        self.y += 2 * self.dy
        self.remove = False
        self.sound = gegnerlaserSounds[0]
        self.sound.set_volume(0.08)
        self.sound.play()

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.y += self.downspeed
        if (SCREEN_BOTTOM + 20 < self.y < SCREEN_TOP - 20) or (SCREEN_LEFT - 20 > self.x > SCREEN_RIGHT + 20):
            self.aufloesen()

    def zeichnen(self):
        screen.blit(self.image, (self.x - int(self.width / 2), self.y - int(self.height / 2)))

    def aufloesen(self):
        self.remove = True

    def zerstoeren(self):
        explosionsAktiv.append(Explosion(self.x, self.y, 0.3, 1, 0))
        self.aufloesen()


class Meteor():
    def __init__(self):
        self.scalefaktor = random.uniform(0.2, 0.5)
        self.rotatespeed = random.uniform(-4, 5)
        self.dy = random.uniform(1, 8)
        self.originalImage = meteorImage  # immer als Referenz für alle Drehungen
        self.originalwidth = self.originalImage.get_width()
        self.originalheight = self.originalImage.get_height()
        self.originalImage = pygame.transform.scale(self.originalImage, (self.originalwidth * self.scalefaktor, self.originalheight * self.scalefaktor))
        self.originalwidth = self.originalImage.get_width()
        self.originalheight = self.originalImage.get_height()
        self.image = self.originalImage  # Bild für Drehung und Darstellung
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = int(random.uniform(0 - self.width * 2, SCREEN_WIDTH + self.width * 2))
        self.y = SCREEN_TOP - self.height / 2
        if self.x < 300:
            self.dx = 4
        elif self.x > SCREEN_WIDTH - 300:
            self.dx = -4
        else:
            self.dx = int(random.uniform(-1, 2)) * 5

        self.rotate = 0
        self.remove = False

    def bewegen(self):
        if (self.y < SCREEN_BOTTOM + 30) and (SCREEN_LEFT - 100 < self.x < SCREEN_RIGHT + 100):
            self.x += self.dx
            self.y += self.dy
            self.rotate += self.rotatespeed
            self.image = pygame.transform.rotate(self.originalImage, self.rotate)
            # neue Breite und Höhe des gedrehten Images bestimmen
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        else:
            self.aufloesen()

    def aufloesen(self):
        self.remove = True

    def zeichnen(self):
        screen.blit(self.image, (self.x - int(self.width / 2), self.y - int(self.height / 2)))

    def zerstoeren(self):
        explosionsAktiv.append(Explosion(self.x, self.y, 1, 4, SCROLLSPEED))
        self.aufloesen()
        raumschiff.addPoints(20000)


class Enemy():
    def __init__(self, enemytyp, formation, fireTyp, drehbar, x, y, speed):
        self.enemyTyp = enemytyp
        self.formation = formation
        self.fireTyp = fireTyp
        self.drehbar = drehbar
        self.speed = speed
        self.x = x
        self.y = y
        if game.Level == 1:
            self.hasshield = 0
        elif game.Level == 2:
            self.hasshield = int(random.uniform(0, 2))
        else:
            self.hasshield = 1
        self.scalefaktor = [40, 25, 40, 40, 40, 40, 40, 40, 40]
        self.shieldon = 0
        self.shieldduration = int(random.uniform(3000, 8000) / (game.Level * 2))
        self.shieldtimer = 0
        if self.hasshield == 1:
            self.shieldon = int(random.uniform(0, 2))
        self.originalImage = gegnerImages[9 * self.hasshield + self.enemyTyp]
        self.image = self.originalImage
        self.ladeGegnerImage()
        self.remove = False

        self.height = 0
        self.width = 0
        self.rect = 0
        self.origin_x = 0
        self.origin_y = 0
        self.angle = -90
        self.feuerabstand = int(random.uniform(2000, 4000)) - game.Level / 4 * 800
        self.feuerzuletzt = 0

    def ladeGegnerImage(self):
        self.originalImage = gegnerImages[9 * self.shieldon + self.enemyTyp]
        self.originalImage = pygame.transform.scale(self.originalImage,
                                                    (self.scalefaktor[self.enemyTyp] / 100 * self.originalImage.get_width(),
                                                     self.scalefaktor[self.enemyTyp] / 100 * self.originalImage.get_height()))
        self.image = self.originalImage
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.origin_x = 0
        self.origin_y = 0
        self.angle = -90

    def update(self):
        if self.hasshield:
            if now() - self.shieldtimer > self.shieldduration:
                self.wechselSchutzschild()
                self.shieldtimer = now()
                self.ladeGegnerImage()
        self.y += self.speed
        if self.y < SCREEN_BOTTOM + 20:
            if self.drehbar:
                self.angle = pygame.math.Vector2(self.x - raumschiff.x, self.y - raumschiff.y).angle_to((-1, 0))
                self.image = pygame.transform.rotate(self.originalImage, int(self.angle))
            else:
                self.image = pygame.transform.rotate(self.originalImage, self.angle)
            if self.formation == 1:
                self.x -= 6
            elif self.formation == 2:
                self.x += 6
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.origin_x = self.x - self.width / 2
            self.origin_y = self.y - self.height / 2
            if now() - self.feuerzuletzt > self.feuerabstand:
                if self.y > SCREEN_TOP + 100:
                    self.feuerzuletzt = now()
                    enemyfireAktiv.append(Enemyfire(self.fireTyp, self.x, self.y, self.angle, int(random.uniform(7, 11))+game.Level, SCROLLSPEED))
        else:
            self.aufloesen()

    def wechselSchutzschild(self):
        if self.shieldon == 0:
            self.shieldon = 1
        else:
            self.shieldon = 0

    def zeichnen(self):
        screen.blit(self.image, (self.origin_x, self.origin_y))
        # image_rect = (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)  # self.image.get_rect(center=(280, 300))

    def aufloesen(self):
        self.remove = True

    def zerstoeren(self, getPoints):
        explosionsAktiv.append(Explosion(self.x, self.y, 0, int(random.uniform(1, 8)), self.speed))
        self.aufloesen()
        if getPoints:
            game.erhoeheGegnergetroffen()
            raumschiff.addPoints(500)


class Mine():
    def __init__(self):
        self.x = int(random.uniform(20, 50))
        self.y = SCREEN_TOP - 30
        self.dx = random.uniform(0.5, 2) * 3
        self.dy = random.uniform(-1, 1)
        self.side = int(random.uniform(0, 2))
        if self.side == 1:
            self.x = SCREEN_RIGHT - self.x
            self.dx *= -1

        self.kapazitaet = int(random.uniform(0, 4))
        self.originalImage = mineImages[self.kapazitaet]
        self.image = self.originalImage
        self.startkapazitaet = self.kapazitaet + 1

        self.originalwidth = self.originalImage.get_width()
        self.originalheight = self.originalImage.get_height()
        self.rotatespeed = 5
        self.rotate = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.remove = False

    def bewegen(self):
        if (self.y < SCREEN_BOTTOM + 30) and (SCREEN_LEFT - 30 < self.x < SCREEN_RIGHT + 30):
            self.x += self.dx
            self.y += SCROLLSPEED + self.dy
            self.rotate += self.rotatespeed
            self.originalImage = mineImages[self.kapazitaet]
            self.image = pygame.transform.rotate(self.originalImage, self.rotate)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        else:
            self.aufloesen()

    def zeichnen(self):
        screen.blit(self.image, (self.x - int(self.width / 2), self.y - int(self.height / 2)))

    def treffer(self):
        self.kapazitaet -= 1
        if self.kapazitaet < 0:
            self.zerstoeren(POINTS_YES)

    def aufloesen(self):
        self.remove = True

    def zerstoeren(self, getPoints):
        explosionsAktiv.append(Explosion(self.x, self.y, 0, 1, SCROLLSPEED))
        self.aufloesen()
        if getPoints:
            game.erhoeheGegnergetroffen()
            raumschiff.addPoints(200 * self.startkapazitaet)


class Explosion():
    def __init__(self, x_pos, y_pos, size, exp_type, exp_downspeed):
        self.x = x_pos
        self.y = y_pos
        self.size = size
        self.exp_type = exp_type
        self.exp_downspeed = exp_downspeed
        self.image = []
        self.expImageCount = [0, 7, 19, 7, 17, 12, 16, 20, 11, 10, 7]
        self.expScale = [0, 0.7, 0.7, 0.7, 0.3, 0.5, 0.5, 0.5, 1, 0.5, 0.5]
        if self.size > 0:
            self.scale = self.size
        else:
            self.scale = self.expScale[exp_type]
        for i in range(self.expImageCount[exp_type]):
            tempimage = pygame.image.load('Explosions/' + str(self.exp_type) + '-' + str(i + 1) + '.png')
            tempimage = pygame.transform.scale(tempimage, (tempimage.get_width() * self.scale, tempimage.get_height() * self.scale))
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
    def __init__(self, level, number):
        self.liste = level - 1
        self.number = number
        self.typ = int(random.uniform(1, 5))
        self.drehbar = (int(random.uniform(0, 5)) <= level)
        self.kapazitaet = int(random.uniform(0, level + 1))
        self.startkapazitaet = self.kapazitaet + 1
        if self.kapazitaet > 3: self.kapazitaet = 3
        self.feuerabstand = int(random.uniform(3000, 5000)) - level / 2 * 1000
        self.feuerzuletzt = now()
        self.x = Kanonen_x[self.liste][self.number] * 2  # erstes Feld später für Level
        self.y = background.scroll_yPos - Kanonen_y[self.liste][self.number] * 2 + Kanonen_Versatz[self.liste]
        self.angle = int(random.uniform(-80, 10))
        if self.x > 360:
            self.angle = int(random.uniform(179, 260))
        self.width = 0
        self.height = 0
        self.originalImage = [pygame.image.load('Cannons/' + str(self.typ) + '1.png'),
                              pygame.image.load('Cannons/' + str(self.typ) + '2.png'),
                              pygame.image.load('Cannons/' + str(self.typ) + '3.png'),
                              pygame.image.load('Cannons/' + str(self.typ) + '4.png')]
        self.remove = False

        for i in range(4):
            self.originalImage[i] = pygame.transform.scale(self.originalImage[i],
                                                           (0.4 * self.originalImage[i].get_width(),
                                                            0.4 * self.originalImage[i].get_height()))
        self.image = self.image = pygame.transform.rotate(self.originalImage[self.kapazitaet], self.angle)
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()

    def bewegen(self):
        if self.y < SCREEN_BOTTOM + 30:
            if self.drehbar:
                self.angle = self.angle = pygame.math.Vector2(self.x - raumschiff.x, self.y - raumschiff.y).angle_to((-1, 0))

                self.image = pygame.transform.rotate(self.originalImage[self.kapazitaet], int(self.angle))
            # else:
            #    self.image = pygame.transform.rotate(self.originalImage[self.kapazitaet], self.angle)
            self.y += SCROLLSPEED
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            if now() - self.feuerzuletzt > self.feuerabstand:
                self.feuerzuletzt = now()
                enemyfireAktiv.append(Enemyfire(6, self.x, self.y, self.angle, int(random.uniform(7, 11))+game.Level, SCROLLSPEED))

        else:
            self.aufloesen()

    def zeichnen(self):
        screen.blit(self.image, (self.x - int(self.width / 2), self.y - int(self.height / 2)))
        image_rect = (self.x - self.width / 2, self.y - self.height / 2, self.width,
                      self.height)

    def treffer(self):
        self.kapazitaet -= 1
        if self.kapazitaet < 0:
            self.zerstoeren()

    def aufloesen(self):
        self.remove = True

    def zerstoeren(self):
        explosionsAktiv.append(Explosion(self.x, self.y, 0, int(random.uniform(1, 8)), SCROLLSPEED))
        self.aufloesen()
        game.erhoeheGegnergetroffen()
        raumschiff.addPoints(self.startkapazitaet * 500)


class Bonus():
    def __init__(self, typ):
        self.x = int(random.uniform(60, SCREEN_WIDTH - 60))
        self.y = -100
        self.typ = typ
        if self.typ == 0:
            map_element = int(random.uniform(0, len(Bonus_Map)))
            self.typ = Bonus_Map[map_element]
        self.bonussound = bonusSounds[self.typ - 1]
        self.bonussound.set_volume(1.0)
        self.bonusimage = bonusImages[self.typ - 1]
        self.image = self.bonusimage
        self.width = 0
        self.height = 0
        self.rotate = 0
        self.remove = False

    def bewegen(self):
        if self.y < SCREEN_BOTTOM + 30:
            self.y += SCROLLSPEED + 1
            self.rotate += 5
            self.image = pygame.transform.rotate(self.bonusimage, self.rotate)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        else:
            self.loeschen()

    def zeichnen(self):
        screen.blit(self.image, (self.x - int(self.width / 2), self.y - int(self.height / 2)))

    def sammeln(self):
        self.bonussound.play()
        if self.typ == 1:
            raumschiff.upgradeshields()
            game_console.update()
        if self.typ == 2:
            raumschiff.restoreshield()
            game_console.update()
        if self.typ == 3:
            raumschiff.addlive()
            game_console.update()
        if self.typ == 4:
            raumschiff.upgradefirepower()
        if self.typ == 5:
            raumschiff.installcannon([1, 0, 0])
        if self.typ == 6:
            raumschiff.installcannon([0, 0, 1])
        if self.typ == 7:
            raumschiff.installcannon([0, 1, 0])
        if self.typ == 8:
            raumschiff.installmegabomb()
        if self.typ == 9:
            raumschiff.upgrade(SMALL)
            game_console.update()
        if self.typ == 10:
            raumschiff.upgrade(MEDIUM)
            game_console.update()
        if self.typ == 11:
            raumschiff.upgrade(LARGE)
            game_console.update()
        raumschiff.addPoints(1000)
        self.loeschen()

    def loeschen(self):
        self.remove = True


class GameConsole():
    def __init__(self):
        self.x = 0
        self.fortschrittimage = image.load("Sonstiges/fortschritt.png")
        self.y_fortschritt = 0
        self.infoimage = image.load("Sonstiges/Rahmen.png")
        self.y_rahmen = 758
        self.x_schilde = 395
        self.y_schilde = 777
        self.shieldimage = [['' for i in range(5)] for j in range(5)]
        for i in range(4):
            for j in range(5):
                try:
                    filename = 'Sonstiges/' + str(i + 1) + '-' + str(j) + '.png'
                    self.shieldimage[i + 1][j] = image.load(filename)
                except FileNotFoundError:
                    print('')
        self.actualshieldimage = self.shieldimage[1][0]

        self.progressimage = image.load("Sonstiges/Progress.png")
        self.progress_x = 0

    def update(self):
        self.actualshieldimage = self.shieldimage[raumschiff.shields][raumschiff.shieldspowered]

    def zeichnen(self):
        screen.blit(self.fortschrittimage, (self.x, self.y_fortschritt))
        screen.blit(self.progressimage, (self.progress_x, self.y_fortschritt + 4))
        screen.blit(self.infoimage, (self.x, self.y_rahmen))
        screen.blit(self.actualshieldimage, (self.x_schilde, self.y_schilde))
        livesstring = str(raumschiff.lives)
        for i in range(len(livesstring)):
            ziffer = int(livesstring[i])
            screen.blit(zahlImages[ziffer], (self.x + 115 + i * 35, self.y_rahmen + 10))
        pointsstring = str(raumschiff.points)
        for i in range(len(pointsstring)):
            ziffer = int(pointsstring[i])
            screen.blit(zahlImages[ziffer], (self.x + 745 + i * 32, self.y_rahmen + 10))

    def updateProgress(self, scrollPos, scrollMax):
        self.progress_x = 10 + (scrollPos / scrollMax) * 940


class Button():
    def __init__(self, typ, scale, x, y, pressable, eventtyp):
        self.typ = typ
        self.x = x
        self.y = y
        self.eventtyp = eventtyp
        self.scale = scale
        self.pressable = pressable
        self.originalImage = buttonImages[self.typ]
        self.originalwidth = self.originalImage.get_width()
        self.originalheight = self.originalImage.get_height()
        self.originalImage = pygame.transform.scale(self.originalImage, (self.originalwidth * self.scale, self.originalheight * self.scale))
        self.image = pygame.transform.scale(self.originalImage, (self.originalwidth * self.scale, self.originalheight * self.scale))
        self.button_width = self.image.get_width()
        self.button_height = self.image.get_height()
        self.my_event = 0
        self.x_min = self.x
        self.y_min = self.y
        self.x_max = self.x_min + self.button_width
        self.y_max = self.y_min + self.button_height

    def checkselection(self):
        if self.pressable:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (mouse_x > self.x_min) and (mouse_y > self.y_min) and (mouse_x < self.x_max) and (mouse_y < self.y_max):
                pygame.event.post(pygame.event.Event(self.eventtyp, message='Button pressed'))

    def zeichnen(self):
        self.image = pygame.transform.scale(self.originalImage, (self.originalwidth * self.scale, self.originalheight * self.scale))
        screen.blit(self.image, (self.x, self.y))

    def setalpha(self, wert):
        self.originalImage.set_alpha(wert)


class Titel():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.buttons_x = 740
        self.buttons_y = 20
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.image = image.load('Sonstiges/Titel.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.sound = mixer.Sound('Sounds/Clearside - Assimilator.wav')
        self.sound.play(-1)

        self.buttonup = Button(BUTTON_UP, 0.75, self.buttons_x, self.buttons_y, True, BUTTON_UP_PRESSED)
        self.buttonLevel = Button(LEVELWAHL[0], 1.1, self.buttons_x - 28, self.buttons_y + 42, False, 0)
        self.buttondown = Button(BUTTON_DOWN, 0.75, self.buttons_x, self.buttons_y + 119, True, BUTTON_DOWN_PRESSED)
        self.buttonstart = Button(BUTTON_START, 1.1, self.buttons_x - 28, self.buttons_y + 175, True, BUTTON_START_PRESSED)

    def update(self):
        self.buttonLevel.originalImage = buttonImages[LEVELWAHL[game.Level - 1]]

    def zeichnen(self):
        screen.blit(self.image, (self.x, self.y), )
        self.buttonup.zeichnen()
        self.buttonLevel.zeichnen()
        self.buttondown.zeichnen()
        self.buttonstart.zeichnen()

    def checkselection(self):
        self.buttonup.checkselection()
        self.buttondown.checkselection()
        self.buttonstart.checkselection()

    def ausblenden(self):
        for i in range(255, 0, -5):
            self.image.set_alpha(i)
            pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
            self.buttonup.setalpha(i)
            self.buttonLevel.setalpha(i)
            self.buttondown.setalpha(i)
            self.buttonstart.setalpha(i)
            self.zeichnen()
            pygame.display.update()
            self.sound.set_volume(256 / (256 - i) * 0.2)
        self.sound.stop()


class Bosskanone():
    def __init__(self, level, num):
        self.num = num
        self.level = level
        self.typ = Boss_Kanone_typ[level][num]
        self.dx = Boss_Kanone_x[level][num]
        self.dy = Boss_Kanone_y[level][num]
        self.kapazitaet = Boss_Kanone_hits[level][num]
        self.startkapazitaet = self.kapazitaet
        self.originalImage = Boss_Kanone_Image[self.typ - 1][self.kapazitaet - 1]
        self.drehbar = (self.typ == 1 or self.typ == 4)
        self.angle = -90
        self.image = pygame.transform.rotate(self.originalImage, self.angle)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.feuerzuletzt = now() + random.uniform(2000, 4000)
        self.feuerabstand = random.uniform(1000, 3000)
        self.remove = False
        self.x = 0
        self.y = 0

    def treffer(self):
        self.kapazitaet -= 1
        if self.kapazitaet == 0:
            self.zerstoeren()
        else:
            self.updateImage()

    def zerstoeren(self):
        explosionsAktiv.append(Explosion(self.x, self.y, 0, int(random.uniform(1, 8)), SCROLLSPEED))
        self.remove = True
        boss.kanonezerstoert()
        game.erhoeheGegnergetroffen()

        raumschiff.addPoints(self.startkapazitaet * 500)

    def update(self):
        self.angle = pygame.math.Vector2(self.x - raumschiff.x, self.y - raumschiff.y).angle_to((-1, 0))

        self.image = pygame.transform.rotate(self.originalImage, int(self.angle))
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def updateImage(self):
        self.originalImage = Boss_Kanone_Image[self.typ - 1][self.kapazitaet - 1]

    def bewegen(self):
        self.x = boss.x + 2 * self.dx
        self.y = boss.y - 2 * self.dy + Boss_Kanone_dy[self.level]

        if self.drehbar:
            self.update()

        if now() - self.feuerzuletzt > self.feuerabstand:
            self.feuerzuletzt = now()
            enemyfireAktiv.append(Enemyfire(self.typ + 5, self.x, self.y, self.angle, int(random.uniform(5, 9)), SCROLLSPEED))

    def zeichnen(self):
        screen.blit(self.image, (int(self.x - self.width / 2), int(self.y - self.height / 2)))


class Boss():
    def __init__(self):
        print('init Level-Boss')
        self.counter = 0
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_TOP - 100
        self.num = game.Level - 1
        self.originalImage = bossImages[self.num]
        self.originalImage = pygame.transform.rotate(self.originalImage, -90)
        self.image = self.originalImage
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.bosskanonencount = 1
        self.remove = False
        self.zerstoert = False
        self.lastexplosion = 0
        self.explosioncount = 12

    def initLevel(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_TOP - 100
        self.bossnum = game.Level - 1
        self.originalImage = bossImages[self.bossnum]
        self.originalImage = pygame.transform.rotate(self.originalImage, -90)
        self.image = self.originalImage
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.remove = False
        self.zerstoert = False
        self.explosioncount = 12

        # erzeuge Bosskanonen
        del bosskanonenAktiv[:]
        for i in range(len(Boss_Kanone_x[self.bossnum])):
            bosskanonenAktiv.append(Bosskanone(self.bossnum, i))
        self.bosskanonencount = len(bosskanonenAktiv)

    def bewegen(self):
        self.x += Boss_Bahn_x[self.counter]
        self.y += Boss_Bahn_y[self.counter]

        self.counter += 1
        if self.counter >= len(Boss_Bahn_x):
            self.counter = 0

    def enter(self):
        self.y += 3
        if self.y > SCREEN_TOP + 40 + int(self.height / 2):
            game.setzeMode(BOSS_RUN)
            print('GameMode = BOSS-RUN')

    def kanonezerstoert(self):
        self.bosskanonencount -= 1
        if self.bosskanonencount == 0:
            self.remove = True
            self.zerstoert = False

    def zerstoeren(self):
        if self.explosioncount > 0:
            if now() - self.lastexplosion > 150:
                self.lastexplosion = now()
                self.explosioncount -= 1
                x = random.uniform(self.x - self.width / 2, self.x + self.width / 2)
                y = random.uniform(self.y - self.height / 2, self.y + self.height / 2)
                size = random.uniform(0.8, 1.1)
                explosionsAktiv.append(Explosion(x, y, size, 1, 0))
        else:
            explosionsAktiv.append(Explosion(self.x, self.y, 2.3, 4, 0))
            self.zerstoert = True

    def zeichnen(self):
        screen.blit(self.image, (int(self.x - self.width / 2), int(self.y - self.height / 2)))


def createLasers():
    laserAktiv.append(Laser(0, raumschiff.x, raumschiff.y - 56, 0, LASERSPEED * 0.5, 90))
    if raumschiff.leftCannon:
        laserAktiv.append(Laser(1, raumschiff.x - 43, raumschiff.y - 14, LASERSPEED * -0.22, LASERSPEED * 0.42, 115))
    if raumschiff.rightCannon:
        laserAktiv.append(Laser(2, raumschiff.x + 43, raumschiff.y - 14, LASERSPEED * 0.22, LASERSPEED * 0.42, 65))
    if raumschiff.doubleCannon:
        laserAktiv.append(Laser(3, raumschiff.x - 50, raumschiff.y + 36, 0, LASERSPEED * 1.2, 90))
        laserAktiv.append(Laser(4, raumschiff.x + 50, raumschiff.y + 36, 0, LASERSPEED * 1.2, 90))
    # Wähle abzuspielden Sound aus
    if raumschiff.doubleCannon:
        raumschiff.doublelasersound.set_volume(0.1)
        raumschiff.doublelasersound.play()
    elif raumschiff.leftCannon or raumschiff.rightCannon:
        raumschiff.sidelasersound.set_volume(0.09)
        raumschiff.sidelasersound.play()
    else:
        raumschiff.lasersound.set_volume(0.09)
        raumschiff.lasersound.play()


def createEnemys():
    typ = int(random.uniform(0, 9))
    fire_typ = int(random.uniform(1, 6))
    drehbar = (int(random.uniform(1, 4)) == 1)
    formation = int(random.uniform(1, 6))
    enemy_count = int(random.uniform(2, 4) + game.Level / 3)
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
            Enemy(typ, formation, fire_typ, drehbar, x_start, y_start, int(random.uniform(SCROLLSPEED+2, SCROLLSPEED+5))))


def collisionHandler():
    if raumschiff.hidden or raumschiff.unverwundbar:
        heroRechteck1 = heroRechteck2 = pygame.Rect(0, 0, 0, 0, )
    else:
        heroRechteck1 = pygame.Rect(raumschiff.x - 50, raumschiff.y, 102, 36)
        heroRechteck2 = pygame.Rect(raumschiff.x - 9, raumschiff.y - 35, 20, 80)
        if SHOWRECTS:
            pygame.draw.rect(screen, RED, heroRechteck1, 2)
            pygame.draw.rect(screen, RED, heroRechteck2, 2)
    for mine in minesAktiv:
        if SCREEN_TOP < mine.y < SCREEN_BOTTOM and SCREEN_LEFT < mine.x < SCREEN_RIGHT:
            mineRechteck = pygame.Rect(mine.x - 30, mine.y - 30, 60, 60)
            if SHOWRECTS:  pygame.draw.rect(screen, RED, mineRechteck, 2)

            if mineRechteck.colliderect(heroRechteck1) or mineRechteck.colliderect((heroRechteck2)):                # Mine trifft Raumschiff
                mine.zerstoeren(POINTS_NO)
                raumschiff.treffer()
            for meteor in meteorsAktiv:                                                                             # Mine trifft Meteor
                meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                             meteor.originalheight - 100 * meteor.scalefaktor)
                if mineRechteck.colliderect(meteorRechteck):
                    mine.zerstoeren(POINTS_NO)

    for enemyfire in enemyfireAktiv:
        #        enemyfireRechteck = pygame.Rect(int(enemyfire.x - enemyfire.width / 2) + 4, int(enemyfire.y - enemyfire.height / 2) + 4, enemyfire.width - 8, enemyfire.height - 8)
        enemyfireRechteck = pygame.Rect(enemyfire.x - 3, enemyfire.y - 3, 6, 6)
        if SHOWRECTS: pygame.draw.rect(screen, RED, enemyfireRechteck, 2)
        if enemyfireRechteck.colliderect(heroRechteck1) or enemyfireRechteck.colliderect(heroRechteck2):            # Gegnerfeuer trifft Raumschiff
            enemyfire.zerstoeren()
            raumschiff.treffer()

        for meteor in meteorsAktiv:                                                                                 # Gegnerfeuer trifft Meteor
            meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                         meteor.originalheight - 100 * meteor.scalefaktor)

            if enemyfireRechteck.colliderect(meteorRechteck):
                enemyfire.zerstoeren()


    for meteor in meteorsAktiv:                                                                                     # Meteor trifft Raumschiff
        meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                     meteor.originalheight - 100 * meteor.scalefaktor)
        if SHOWRECTS: pygame.draw.rect(screen, RED, meteorRechteck, 2)
        if meteorRechteck.colliderect(heroRechteck1) or meteorRechteck.colliderect(heroRechteck2):
            raumschiff.treffer()

    for enemy in enemyAktiv:                                    # Enemy kollidiert mit Meteor und Raumschiff
        if SCREEN_TOP+60 < enemy.y < SCREEN_BOTTOM and SCREEN_LEFT < enemy.x < SCREEN_RIGHT:
            enemyRechteck = pygame.Rect(int(enemy.x - enemy.width / 2) + 4, int(enemy.y - enemy.height / 2) + 4,
                                        enemy.width - 8,
                                        enemy.height - 8)
            if SHOWRECTS: pygame.draw.rect(screen, RED, enemyRechteck, 2)

            for meteor in meteorsAktiv:                                                                             # Gegner trifft auf Meteor
                meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                             meteor.originalheight - 100 * meteor.scalefaktor)
                if enemyRechteck.colliderect(meteorRechteck):
                    enemy.zerstoeren(POINTS_NO)

            if enemyRechteck.colliderect(heroRechteck1) or enemyRechteck.colliderect(heroRechteck2):                # Gegner trifft auf Raumschiff
                enemy.zerstoeren(POINTS_YES)
                raumschiff.treffer()

    for laser in laserAktiv:            # Laser zerstört Gegner, Kanonen, Minen, Meteore, Bosskanonen
        laserRechteck = pygame.Rect(laser.x - 3, laser.y - 3, 6, 6)
        if game.Mode == BOSS_RUN:
            for bosskanone in bosskanonenAktiv:                                                                     # Laser trifft Bosskanone
                bosskanoneRechteck = pygame.Rect(bosskanone.x - bosskanone.width / 2, bosskanone.y - bosskanone.height / 2, bosskanone.width, bosskanone.height)
                if SHOWRECTS: pygame.draw.rect(screen, RED, bosskanoneRechteck, 2)
                if bosskanoneRechteck.colliderect(laserRechteck):
                    if bosskanone.kapazitaet > 0:
                        laser.zerstoeren()
                    else:
                        laser.aufloesen()
                    bosskanone.treffer()
        for meteor in meteorsAktiv:                                                                                 # Laser trifft Meteor
            meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                         meteor.originalheight - 100 * meteor.scalefaktor)
            if laserRechteck.colliderect(meteorRechteck):
                laser.zerstoeren()

        for mine in minesAktiv:                                                                                     # Laser triff Mine
            if SCREEN_TOP < mine.y < SCREEN_BOTTOM and SCREEN_LEFT < mine.x < SCREEN_RIGHT:
                mineRechteck = pygame.Rect(mine.x - 30, mine.y - 30, 60, 60)
                if SHOWRECTS:  pygame.draw.rect(screen, RED, mineRechteck, 2)
                if mineRechteck.colliderect(laserRechteck):
                    if mine.kapazitaet > 0:
                        laser.zerstoeren()
                    else:
                        laser.aufloesen()
                    mine.treffer()

        for enemy in enemyAktiv:                                                                                    # Laser trifft Gegner
            if SCREEN_TOP+60 < enemy.y < SCREEN_BOTTOM and SCREEN_LEFT < enemy.x < SCREEN_RIGHT:
                enemyRechteck = pygame.Rect(int(enemy.x - enemy.width / 2) + 4, int(enemy.y - enemy.height / 2) + 4,
                                            enemy.width - 8,
                                            enemy.height - 8)
                if SHOWRECTS: pygame.draw.rect(screen, RED, enemyRechteck, 2)
                if enemyRechteck.colliderect(laserRechteck):
                    if enemy.shieldon == 0:
                        laser.aufloesen()
                        enemy.zerstoeren(POINTS_YES)
                    else:
                        laser.zerstoeren()

        for kanone in kanonenAktiv:                                                                                 # Laser trifft Kanone
            if SCREEN_TOP+40 < kanone.y < SCREEN_BOTTOM:
                kanoneRechteck = pygame.Rect(kanone.x - 40, kanone.y - 40, 80, 80)
                if SHOWRECTS: pygame.draw.rect(screen, RED, kanoneRechteck, 2)

                if kanoneRechteck.colliderect(laserRechteck):
                    if kanone.kapazitaet > 0:
                        laser.zerstoeren()
                    else:
                        laser.aufloesen()
                    kanone.treffer()

    for kanone in kanonenAktiv:
        if SCREEN_TOP < kanone.y < SCREEN_BOTTOM:
            kanoneRechteck = pygame.Rect(kanone.x - 40, kanone.y - 40, 80, 80)
            if SHOWRECTS: pygame.draw.rect(screen, RED, kanoneRechteck, 2)
            if kanoneRechteck.colliderect(heroRechteck1) or kanoneRechteck.colliderect(heroRechteck2):
                kanone.zerstoeren()
                raumschiff.treffer()

    heroRechteck1 = pygame.Rect(raumschiff.x - 50, raumschiff.y, 102, 36)
    heroRechteck2 = pygame.Rect(raumschiff.x - 10, raumschiff.y - 30, 20, 60)
    for bonus in bonusAktiv:
        if bonus.y > SCREEN_TOP and bonus.y < SCREEN_BOTTOM:
            bonusRechteck = pygame.Rect(int(bonus.x - bonus.width / 2) + 2, int(bonus.y - bonus.height / 2) + 2,
                                        bonus.width - 4,
                                        bonus.height - 4)
            if bonusRechteck.colliderect(heroRechteck1) or bonusRechteck.colliderect(heroRechteck2):
                bonus.sammeln()


class LevelPanel():
    def __init__(self):
        self.x = 150
        self.y = 500
        self.image = levelImages[game.Level]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dcounter = 5
        self.alpha = 0
        self.zeigen = True

    def init(self, mode):

        if mode == LEVEL_START:
            self.image = levelImages[game.Level]
        elif mode == LEVEL_ENDE:
            self.image = levelImages[0]
        elif mode == GAME_OVER:
            self.image = image.load('Sonstiges/Gameover.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = int((SCREEN_WIDTH - self.width) / 2)
        self.y = int((SCREEN_HEIGHT - self.height) / 2)
        self.dcounter = 4
        self.alpha = 0
        self.zeigen = True

    def show(self):
        if self.zeigen:
            if self.alpha >= 255:
                self.dcounter = -8
            self.alpha += self.dcounter
            if self.alpha >= 0:
                self.image.set_alpha(self.alpha)
                screen.blit(self.image, (self.x, self.y))
            else:
                self.zeigen = False


def now():
    return time() * 1000


def allObjectsHandler():
    # neue Gegner erzeugen im Modus NORMAL_RUN
    if game.Mode == NORMAL_RUN:
        # Kanonen erzeugen, wenn in Reichweite
        if len(Kanonen_y[game.Level - 1]) > game.kanonenListcounter:
            if Kanonen_y[game.Level - 1][game.kanonenListcounter] * 2 < background.scroll_yPos + Kanonen_Versatz[game.Level - 1]:
                # nächste Kanone erzeugen
                kanonenAktiv.append(Kanone(game.Level, game.kanonenListcounter))
                game.erhoeheklc()

        # neue Gegnerwellen erzeugen
        if now() - game.timeOfLastEnemyWave > game.timeTillNewWave:  # In Abhängigkeit vom Level neue Welle nach Zufallszeitspanne erzeugen
            createEnemys()
            game.setzewavetime()

        # ab Level 2 Minen
        if game.Level > 1 and now() - game.timeOfLastMine > game.timeTillNewMine:
            minesAktiv.append(Mine())
            game.setzeminetime()


        # ab Level 3 Meteoriten
        if game.Level > 2 and now() - game.timeOfLastMeteor > game.timeTillNewMeteor:
            meteorsAktiv.append(Meteor())
            game.setzemeteortime()

    # Bonussymbole in beiden Spielmodi erzeugen
    if game.Gegnergetroffen > 6 - game.Level:
        game.resetGegnergetroffen()
        bonusAktiv.append(Bonus(0))


    # print('Kanonen: '+str(len(kanonenAktiv))+'  Gegner: '+str(len(enemyAktiv))+'  Bonus: '+str(len(bonusAktiv))+'  Gegnerfeuer: '+str(len(enemyfireAktiv))+'  Lasers: '+str(len(laserAktiv))+'  Explosionen: '+str(len(explosionsAktiv)))

    # ab hier erzeugte Instanzen auf Bildschirm zeichnen, dabei Layer-Reihenfolge beachten (Überlagerungen)
    # 1. Hintergrund
    # 2. Kanonen am Boden
    # 3. Gegnerfeuer
    # 4. Gegner in der Luft
    # 5. Minen
    # 6. Meteore
    # 7. Bonussymbole
    # 8. Raumschiff
    # 9. Explosionen
    # 10. eigene Laser
    # 11. Spielkonsole
    # 12. Level-Panel

    if not (game.Mode == LEVEL_ENDE or game.Mode == WAIT or game.Mode == SPIEL_ENDE):
        # 1. Hintergrund
        background.update()
        background.zeichnen()

        # 2. Kanonen
        for kanone in kanonenAktiv:
            if kanone.remove:
                kanonenAktiv.remove(kanone)
            else:
                kanone.bewegen()
                kanone.zeichnen()

        if game.Mode == BOSS_RUN or game.Mode == BOSS_ENTER:
            if game.Mode == BOSS_RUN:
                if boss.remove:
                    if not boss.zerstoert:
                        boss.zerstoeren()
                    else:
                        game.setzeMode(LEVEL_ENDE)
                        print('GameMode = LEVEL_ENDE')
                        endLevel()
                else:
                    boss.bewegen()
            if game.Mode == BOSS_ENTER:
                boss.enter()
            boss.zeichnen()

            for bosskanone in bosskanonenAktiv:
                if bosskanone.remove:
                    bosskanonenAktiv.remove(bosskanone)
                else:
                    bosskanone.bewegen()
                    bosskanone.zeichnen()

        # 3. Gegnerschüsse bewegen und entfernen (werden automatisch von Enemy und Kanonen-Objekten erzeugt)
        for enemyfire in enemyfireAktiv:
            # Wenn Schuss ausserhalb des sichtbaren Spielfeldes, dann weg damit
            if enemyfire.remove:
                enemyfireAktiv.remove(enemyfire)
            else:
                enemyfire.update()
                enemyfire.zeichnen()

        # 4. Gegner in der Luft
        for enemy in enemyAktiv:  # alle gerade aktiven Gegner-Objekte animieren
            if enemy.remove:
                enemyAktiv.remove(enemy)
            else:
                enemy.update()
                enemy.zeichnen()

        # 5. Minen
        for mine in minesAktiv:
            if mine.remove:
                minesAktiv.remove(mine)
            else:
                mine.bewegen()
                mine.zeichnen()

        # 6. Meteore
        for meteor in meteorsAktiv:
            if meteor.remove:
                meteorsAktiv.remove(meteor)
            else:
                meteor.bewegen()
                meteor.zeichnen()

        # 8. eigenes Raumschiff
        raumschiff.update(True)
        raumschiff.zeichnen()

    # 7. Bonussymbole
    for bonus in bonusAktiv:
        if (bonus.remove) or (bonus.y > SCREEN_BOTTOM + 20):
            bonusAktiv.remove(bonus)
        else:
            bonus.bewegen()
            bonus.zeichnen()

    # 10. eigene Laser bewegen und entfernen (werden automatisch von Hero-Objekt erzeugt)
    for laser in laserAktiv:
        if (laser.remove) or (laser.y > SCREEN_BOTTOM + 20) or (laser.y < SCREEN_TOP - 20) or (laser.x < SCREEN_LEFT - 20) or (laser.x > SCREEN_RIGHT + 20):
            laserAktiv.remove(laser)
        else:
            laser.bewegen()
            laser.zeichnen()

    # 9. Explosionen ausführen und entfernen
    for explosion in explosionsAktiv:  # alle gerade aktiven Explosions-Objekte animieren
        if explosion.fertig:  # wenn Explosionssequenz fertig ist, denn Objekt löschen
            explosionsAktiv.remove(explosion)
        else:  # sonst Objekt animieren
            explosion.explode()
            explosion.bewegen()

    # 11. Rahmen der Gamekonsole legen
    game_console.zeichnen()

    # 12. Level-Panel zu Beginn
    if level_panel.zeigen:
        level_panel.show()


def startLevel():
    pygame.mouse.set_visible(False)
    background.loadlevel(game.Level)
    game_console.update()

    # Initialisiere Zeiten
    game.levelinit()

    del minesAktiv[:]
    del meteorsAktiv[:]
    del enemyfireAktiv[:]
    del enemyAktiv[:]
    del kanonenAktiv[:]
    del bonusAktiv[:]
    del explosionsAktiv[:]
    game.setzeMode(LEVEL_START)
    raumschiff.y = SCREEN_BOTTOM + 50

    level_panel.init(LEVEL_START)
    mixer.Sound("Sounds/Jetzt kann der Spaß anfangen.wav").play()
    playBackgroundSongs(game.Level)


def endLevel():
    level_panel.init(LEVEL_ENDE)
    mixer.Sound("Sounds/Atmen DV.wav").play()
    playBackgroundSongs(game.Level)


def gameover():
    level_panel.init(GAME_OVER)
    mixer.Sound("Sounds/game_over.wav").play()
    # game_backgroundmusic.play(game.Level)


def moveoutHero():
    if raumschiff.y > SCREEN_TOP - 100:
        raumschiff.moveout()
        background.zeichnen()
        raumschiff.update(False)
        raumschiff.zeichnen()
        game_console.zeichnen()
    else:
        game.erhoeheLevel()
        if game.Level <= 1:
            startLevel()
        else:
            game.setzeMode(SPIEL_ENDE)


def moveinHero():
    mousex, mousey = pygame.mouse.get_pos()
    if raumschiff.y >= mousey:
        raumschiff.setzepos((mousex, raumschiff.y -6))
        background.zeichnen()
        raumschiff.update(False)
        raumschiff.zeichnen()
        game_console.zeichnen()
    else:
        game.setzeMode(NORMAL_RUN)
        boss.initLevel()

def main():
    mousepressed = False
    pausestart = None
    # Game Loop
    while True:

        # Cycles through all occurring events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mouse.set_visible(True)
                pygame.quit()
                sys.exit()
            if event.type == BUTTON_DOWN_PRESSED:
                if game.Level > 1:
                    game.Level -= 1
            if event.type == BUTTON_UP_PRESSED:
                if game.Level < 4:
                    game.Level += 1
            if event.type == BUTTON_START_PRESSED:
                titel.ausblenden()
                startLevel()

            if event.type == MOUSEBUTTONUP:
                mousepressed = False
        # pygame.event.pump()
        print('GameMode =', game.Mode)
        if game.Mode == START:
            # Zeige Titelbild mit Buttons
            titel.update()
            titel.zeichnen()
            mouseButton = pygame.mouse.get_pressed()
            if mouseButton[0]:
                if not mousepressed:
                    mousepressed = True
                    titel.checkselection()
        if game.Mode == NORMAL_RUN or game.Mode == BOSS_RUN or game.Mode == BOSS_ENTER:
            # Abfrage, ob Taste gedrückt
            gedrueckt = pygame.key.get_pressed()
            # Linkspfeil gedrückt
            if gedrueckt[K_a]:
                if game.smallbonusavailable:
                    game.smallbonusavailable = False
                    bonusAktiv.append(Bonus(9))
            if gedrueckt[K_s]:
                if game.mediumbonusavailable:
                    game.mediumbonusavailable = False
                    bonusAktiv.append(Bonus(10))
            if gedrueckt[K_d]:
                if game.largebonusavailable:
                    game.largebonusavailable = False
                    bonusAktiv.append(Bonus(11))

            allObjectsHandler()
            # if not game.Mode == BOSS_ENTER:
            mouseButton = pygame.mouse.get_pressed()
            if mouseButton[0]:
                if raumschiff.aktiv:  # Schüsse abgeben mit linker Maustaste
                    if (now() - game.timeLastShot) > 1000 / raumschiff.firepower:
                        createLasers()
                        game.timeLastShot = now()
            if mouseButton[2]:  # Zünde Megabombe mit rechter Maustaste
                if raumschiff.has_megabomb():
                    raumschiff.zuendeMegabombe()
            collisionHandler()

        if game.Mode == LEVEL_ENDE:  # Bewege Raumschiff nach oben aus dem sichtbaren Bereich
            moveoutHero()
            allObjectsHandler()

            # collisionHandler()
        if game.Mode == LEVEL_START:
            moveinHero()
        if game.Mode == GAME_OVER:
            pausestart = now()
            gameover()
            game.Mode = WAIT
        if game.Mode == WAIT:
            allObjectsHandler()
            if now() - pausestart > 6000:
                game.setzeMode(SPIEL_ENDE)
        if game.Mode == SPIEL_ENDE:
            pygame.quit()
            sys.exit()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    background = ScrollingBackground()
    raumschiff = Hero()
    game_console = GameConsole()
    titel = Titel()
    level_panel = LevelPanel()
    pygame.mouse.set_visible(True)
    boss = Boss()


    main()