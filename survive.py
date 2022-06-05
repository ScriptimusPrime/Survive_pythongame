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

SMALL = 1
MEDIUM = 2
LARGE = 3

BUTTON_UP = 0
BUTTON_DOWN = 1
BUTTON_START = 2
LEVELWAHL = [3, 4, 5, 6]

BUTTON_UP_PRESSED = USEREVENT + 1
BUTTON_DOWN_PRESSED = USEREVENT + 2
BUTTON_START_PRESSED = USEREVENT + 3

Kanonen_x = [
    [59, 42, 36, 36, 72, 313, 304, 299, 275, 267, 260, 431, 204, 202, 444, 442, 114, 262, 408, 358, 358, 40,
     278, 35,
     263], [], [], []]
Kanonen_y = [
    [2127, 2369, 2451, 2545, 2683, 3782, 3925, 4064, 4677, 4825, 4958, 6240, 6273, 6337, 6396, 6464, 6629,
     6641, 6929,
     6977, 7043, 7331, 7343, 7558, 7571], [], [], [], []]
Background_Mapping = [3, 1, 2, 4]
Background_Count = [24, 24, 31, 57]
# Weitere Konstanten
SCREEN_WIDTH = 960  # Breite des sichtbaren Spielfeldbereichs
SCREEN_HEIGHT = 809
SCREEN_TOP = 38  # Min-y-Koordinate des sichtbaren Spielfeldbereichs
SCREEN_BOTTOM = 758  # Max-y-Koordinate des sichtbaren Spielfeldbereichs
SCREEN_LEFT = 0  # Min-x-Koordinate des sichtbaren Spielfeldbereichs
SCREEN_RIGHT = SCREEN_WIDTH  # Max-x-Koordinate des sichtbaren Spielfeldbereichs
SPEED = 5
SCORE = 0
LASERSPEED = 30
SCROLLSPEED = 2
POINTS_NO = False
POINTS_YES = True

showLevel = True
Level = 1
Gegnergetroffen = 0
smallbonusavailable = True
mediumbonusavailable = True
largebonusavailable = True

# Fonts festlegen
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Fenster erstellen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BLACK)
pygame.display.set_caption("Survive")
pygame.mouse.set_visible(False)
laserImages = [image.load('Laser/beam2.png'), image.load('Laser/beaml.png'), image.load('Laser/beamr.png'), image.load('Laser/beamdl.png'), image.load('Laser/beamdr.png')]
gegnerlaserImages = [image.load('Gegnerfeuer/1.png'), image.load('Gegnerfeuer/2.png'), image.load('Gegnerfeuer/3.png'),
                     image.load('Gegnerfeuer/4.png'), image.load('Gegnerfeuer/5.png'), image.load('Gegnerfeuer/20.png'),
                     image.load('Gegnerfeuer/boss1.png'), image.load('Gegnerfeuer/boss2.png'),
                     image.load('Gegnerfeuer/boss3.png'),
                     image.load('Gegnerfeuer/boss4.png'), ]
gegnerlaserSounds = [mixer.Sound('Gegnerfeuer/Schuss.wav'), mixer.Sound('Gegnerfeuer/Schussboss.wav')]
bonusImages = [image.load('Bonus/1.png'), image.load('Bonus/2.png'), image.load('Bonus/3.png'),
               image.load('Bonus/4.png'), image.load('Bonus/5.png'), image.load('Bonus/6.png'),
               image.load('Bonus/7.png'), image.load('Bonus/8.png'), image.load('Bonus/9.png'),
               image.load('Bonus/10.png'), image.load('Bonus/11.png')]
levelImages = [image.load('Sonstiges/Level1.png'),image.load('Sonstiges/Level2.png'),image.load('Sonstiges/Level3.png'),image.load('Sonstiges/Level4.png')]
buttonImages = [image.load('Sonstiges/Button_up.png'), image.load('Sonstiges/Button_down.png'), image.load('Sonstiges/Button_start.png'), image.load('Sonstiges/Levelwahl1.png'), image.load('Sonstiges/Levelwahl2.png'),
                image.load('Sonstiges/Levelwahl3.png'), image.load('Sonstiges/Levelwahl4.png')]
schutzschildImages = [image.load('Schutzschild/0.png'), image.load('Schutzschild/1.png'), image.load('Schutzschild/2.png'), image.load('Schutzschild/3.png'), image.load('Schutzschild/4.png')]
mineImages = [image.load('Mine/1.png'), image.load('Mine/2.png'), image.load('Mine/3.png'), image.load('Mine/4.png')]
meteorImage = [image.load('Meteor/meteor.png')]
zahlImages = [image.load('Zahlen/0.png'), image.load('Zahlen/1.png'), image.load('Zahlen/2.png'), image.load('Zahlen/3.png'), image.load('Zahlen/4.png'), image.load('Zahlen/5.png'), image.load('Zahlen/6.png'), image.load('Zahlen/7.png'),
              image.load('Zahlen/8.png'), image.load('Zahlen/9.png')]
laserSounds = [mixer.Sound('Sounds/Laser0.wav'), mixer.Sound('Sounds/Laser1.wav'), mixer.Sound('Sounds/Laser1.wav'), mixer.Sound('Sounds/Laser4.wav'), mixer.Sound('Sounds/Laser4.wav'), ]
explosionSounds = [mixer.Sound('Explosionssounds/exp1.wav'), mixer.Sound('Explosionssounds/exp2.wav'), mixer.Sound('Explosionssounds/exp3.wav'), mixer.Sound('Explosionssounds/exp4.wav'),
                   mixer.Sound('Explosionssounds/exp5.wav'), mixer.Sound('Explosionssounds/exp6.wav'), mixer.Sound('Explosionssounds/exp7.wav'), mixer.Sound('Explosionssounds/exp8.wav'),
                   mixer.Sound('Explosionssounds/exp9.wav')]
bonusSounds = [mixer.Sound('Bonussounds/1.mp3'), mixer.Sound('Bonussounds/2.wav'), mixer.Sound('Bonussounds/3.mp3'),
               mixer.Sound('Bonussounds/4.wav'), mixer.Sound('Bonussounds/5.wav'), mixer.Sound('Bonussounds/6.mp3'),
               mixer.Sound('Bonussounds/7.wav'), mixer.Sound('Bonussounds/8.wav'), mixer.Sound('Bonussounds/9.mp3'),
               mixer.Sound('Bonussounds/10.wav'), mixer.Sound('Bonussounds/11.wav'), mixer.Sound('Bonussounds/Plopp.wav')]
ingamemusicSounds = [mixer.Sound('Sounds/Act of War.mp3.wav'), mixer.Sound('Sounds/We will meet again.mp2.wav'), mixer.Sound('Sounds/determined_pursuit_loop.wav'), mixer.Sound('Sounds/Are You With Us.wav')]

laserAktiv = []
enemyAktiv = []
enemyfireAktiv = []
explosionsAktiv = []
kanonenAktiv = []
bonusAktiv = []
minesAktiv = []
meteorsAktiv = []

kanonenListcounter = 0
timeOfLastEnemyWave = 0
timeTillNewWave = 0
timeOfLastMine = 0
timeTillNewMine = 0
timeOfLastMeteor = 0
timeTillNewMeteor = 0

Lives = 13
Points = 12345

timeLastShot = time() * 1000
scroll_yPos = 0
game_Mode = START


class BgTile():
    def __init__(self, num, level):
        self.name = 'Backgrounds/' + str(Background_Mapping[level - 1]) + '-' + str(num) + '.png'
        self.image = image.load(self.name)
        self.num = num
        self.level = level


class BackgroundSongs():
    def __init__(self):
        self.sound = ingamemusicSounds[Level - 1]

    # def play(self):
    #     self.sound = ingamemusicSounds[Level - 1]
    #     self.sound.set_volume(0.1)
    #     self.sound.play(-1)



    def stop(self):
        self.sound.stop()


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
        if self.bCounter < Background_Count[Level - 1]:
            self.bottomTile += self.movingDownSpeed
            self.topTile += self.movingDownSpeed
            scroll_yPos += self.movingDownSpeed
            game_console.updateProgress(scroll_yPos, Background_Count[Level - 1] * 720)

            if self.bottomTile >= 720:
                self.bottomTile = 0
                self.topTile = -720
                self.bCounter += 1

    def zeichnen(self):
        if self.bCounter < Background_Count[Level - 1] - 1:
            screen.blit(self.bgField[self.bCounter + 1].image, (0, self.topTile + 38))
            screen.blit(self.bgField[self.bCounter].image, (0, self.bottomTile + 38))
        else:
            screen.fill(BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            game_Mode = BOSS_RUN


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

        self.rot_rect = 0
        self.orig_rect = 0

    def upgrade(self, typ):
        self.shields = 4
        self.shieldspowered = 4
        if typ == SMALL:
            self.leftCannon = 1
            if self.firepower < 4:
                self.firepower = 4
        elif typ == MEDIUM:
            self.leftCannon = 1
            self.rightCannon = 1
            if self.firepower < 6:
                self.firepower = 6
        elif typ == LARGE:
            self.leftCannon = 1
            self.rightCannon = 1
            self.doubleCannon = 1
            if self.firepower < 8:
                self.firepower = 8

    def update(self):
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
                    self.y - int(self.megabombImage.get_height() / 2) - 30))
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

    def looselive(self):
        self.lives -= 1
        if self.lives < 0:
            self.lives = 0

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
        global game_console
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
        global explosionsAktiv
        explosionsAktiv.append(Explosion(self.x, self.y, 1, 8, 0))
        self.hidden = True
        self.aktiv = False
        self.timehidden = 45
        self.lives -= 1
        if self.lives > 0:
            if self.firepower > 1:
                self.firepower -= 1
        else:
            print('Game over')

    def has_megabomb(self):
        return self.megabomb

    def zuendeMegabombe(self):
        self.megabomb = False
        explosionsAktiv.append(Explosion(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100, 3, 9, 0))
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
        self.lasersound = laserSounds[self.typ]
        self.lasersound.set_volume(0.07)
        self.lasersound.play()
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
    def __init__(self, typ, x, y, angle, speed):
        self.x = x
        self.y = y
        self.typ = typ
        self.angle = angle
        self.speed = speed
        self.image = gegnerlaserImages[self.typ - 1]
        self.image = pygame.transform.scale(self.image,(self.image.get_width()*0.75,self.image.get_height()*0.5))
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
        self.y += self.dy + SCROLLSPEED

    def zeichnen(self):
        screen.blit(self.image, (self.x - int(self.width / 2), self.y - int(self.height / 2)))

    def aufloesen(self):
        self.remove = True

    def zerstoeren(self):
        explosionsAktiv.append(Explosion(self.x, self.y, 0.3, 1, 0))
        self.aufloesen()


class Meteor():
    def __init__(self):
        self.x = int(random.uniform(40, SCREEN_WIDTH - 40))
        self.y = SCREEN_TOP - 40
        if self.x < 300:
            self.dx = 4
        elif self.x > SCREEN_WIDTH - 300:
            self.dx = -4
        else:
            self.dx = int(random.uniform(-1, 2)) * 4

        self.scalefaktor = random.uniform(0.2, 0.5)
        self.rotatespeed = random.uniform(-4, 5)
        self.dy = random.uniform(1, 4)
        self.originalImage = meteorImage[0]  # immer als Referenz für alle Drehungen
        self.originalwidth = self.originalImage.get_width()
        self.originalheight = self.originalImage.get_height()
        self.originalImage = pygame.transform.scale(self.originalImage, (self.originalwidth * self.scalefaktor, self.originalheight * self.scalefaktor))
        self.originalwidth = self.originalImage.get_width()
        self.originalheight = self.originalImage.get_height()
        self.image = self.originalImage  # Bild für Drehung und Darstellung
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rotate = 0
        self.remove = False

    def bewegen(self):
        self.x += self.dx
        self.y += self.dy
        self.rotate += self.rotatespeed
        self.image = pygame.transform.rotate(self.originalImage, self.rotate)
        # neue Breite und Höhe des gedrehten Images bestimmen
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def zeichnen(self):
        screen.blit(self.image, (self.x - int(self.width / 2), self.y - int(self.height / 2)))

    def zerstoeren(self):
        explosionsAktiv.append(Explosion(self.x, self.y, 1, 4, SCROLLSPEED))
        self.remove = True
        game_hero.addPoints(20000)


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
            if self.y > SCREEN_TOP + 100:
                self.feuerzuletzt = time() * 1000
                enemyfireAktiv.append(Enemyfire(self.fireTyp, self.x, self.y, self.angle, int(random.uniform(7, 11))))

    def zeichnen(self):
        screen.blit(self.image, (self.origin_x, self.origin_y))
        # image_rect = (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)  # self.image.get_rect(center=(280, 300))

    def zerstoeren(self, getPoints):
        global Gegnergetroffen
        explosionsAktiv.append(Explosion(self.x, self.y, 0, int(random.uniform(1, 8)), self.speed))
        self.remove = True
        if getPoints:
            Gegnergetroffen += 1
            game_hero.addPoints(500)


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
        self.x += self.dx
        self.y += SCROLLSPEED + self.dy
        self.rotate += self.rotatespeed
        self.originalImage = mineImages[self.kapazitaet]
        self.image = pygame.transform.rotate(self.originalImage, self.rotate)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def zeichnen(self):
        screen.blit(self.image, (self.x - int(self.width / 2), self.y - int(self.height / 2)))

    def treffer(self):
        self.kapazitaet -= 1
        if self.kapazitaet < 0:
            self.zerstoeren(POINTS_YES)

    def zerstoeren(self, getPoints):
        global Gegnergetroffen
        explosionsAktiv.append(Explosion(self.x, self.y, 0, 1, SCROLLSPEED))
        self.remove = True
        if getPoints:
            Gegnergetroffen += 1
            game_hero.addPoints(200 * self.startkapazitaet)


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
    def __init__(self, number):
        self.number = number
        self.typ = int(random.uniform(1, 5))
        self.drehbar = (int(random.uniform(1, 5)) == 1)
        self.kapazitaet = int(random.uniform(0, Level + 1))
        self.startkapazitaet = self.kapazitaet + 1
        if self.kapazitaet > 3: self.kapazitaet = 3
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
            enemyfireAktiv.append(Enemyfire(6, self.x, self.y, self.angle, int(random.uniform(7, 11))))

    def zeichnen(self):
        screen.blit(self.image, (self.origin_x, self.origin_y))
        image_rect = (self.x - self.width / 2, self.y - self.height / 2, self.width,
                      self.height)  # self.image.get_rect(center=(280, 300))

    def treffer(self):
        self.kapazitaet -= 1
        if self.kapazitaet < 0:
            self.zerstoeren()

    def zerstoeren(self):
        global Gegnergetroffen
        explosionsAktiv.append(Explosion(self.x, self.y, 0, int(random.uniform(1, 8)), SCROLLSPEED))
        self.remove = True
        Gegnergetroffen += 1
        game_hero.addPoints(self.startkapazitaet * 500)


class Bonus():
    def __init__(self, typ):
        self.x = int(random.uniform(60, SCREEN_WIDTH - 60))
        self.y = -100
        self.typ = typ
        if self.typ == 0:
            self.typ = int(random.uniform(1, 9))
        self.bonussound = bonusSounds[self.typ - 1]
        self.bonussound.set_volume(1.0)
        self.bonusimage = bonusImages[self.typ - 1]
        self.width = self.bonusimage.get_width()
        self.height = self.bonusimage.get_height()
        self.remove = False

    def bewegen(self):
        self.y += SCROLLSPEED + 1
        self.rect = (self.x - self.width / 2, self.y - self.height / 2, self.width,
                     self.height)

    def zeichnen(self):
        screen.blit(self.bonusimage, (self.x, self.y))

    def sammeln(self):
        self.bonussound.play()
        if self.typ == 1:
            game_hero.upgradeshields()
            game_console.update()
        if self.typ == 2:
            game_hero.restoreshield()
            game_console.update()
        if self.typ == 3:
            game_hero.addlive()
            game_console.update()
        if self.typ == 4:
            game_hero.upgradefirepower()
        if self.typ == 5:
            game_hero.installcannon([1, 0, 0])
        if self.typ == 6:
            game_hero.installcannon([0, 0, 1])
        if self.typ == 7:
            game_hero.installcannon([0, 1, 0])
        if self.typ == 8:
            game_hero.installmegabomb()
        if self.typ == 9:
            game_hero.upgrade(SMALL)
            game_console.update()
        if self.typ == 10:
            game_hero.upgrade(MEDIUM)
            game_console.update()
        if self.typ == 11:
            game_hero.upgrade(LARGE)
            game_console.update()
        game_hero.addPoints(1000)
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
        self.actualshieldimage = self.shieldimage[game_hero.shields][game_hero.shieldspowered]

    def zeichnen(self):
        screen.blit(self.fortschrittimage, (self.x, self.y_fortschritt))
        screen.blit(self.progressimage, (self.progress_x, self.y_fortschritt + 4))
        screen.blit(self.infoimage, (self.x, self.y_rahmen))
        screen.blit(self.actualshieldimage, (self.x_schilde, self.y_schilde))
        livesstring = str(game_hero.lives)
        for i in range(len(livesstring)):
            ziffer = int(livesstring[i])
            screen.blit(zahlImages[ziffer], (self.x + 115 + i * 35, self.y_rahmen + 10))
        pointsstring = str(game_hero.points)
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
        self.x_max = self.x_min+self.button_width
        self.y_max = self.y_min+self.button_height

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
        self.buttonLevel.originalImage = buttonImages[LEVELWAHL[Level -1]]

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
        print('ausblenden')
        for i in range(255,0,-5):
            self.image.set_alpha(i)
            pygame.draw.rect(screen,BLACK,(0,0,SCREEN_WIDTH,SCREEN_HEIGHT),0)
            self.buttonup.setalpha(i)
            self.buttonLevel.setalpha(i)
            self.buttondown.setalpha(i)
            self.buttonstart.setalpha(i)
            self.zeichnen()
            pygame.display.update()
            self.sound.set_volume( 256/ (256-i) *0.2)
        self.sound.stop()

def createLasers():
    laserAktiv.append(Laser(0, game_hero.x, game_hero.y - 56, 0, LASERSPEED * 0.5, 90))
    if game_hero.leftCannon:
        laserAktiv.append(Laser(1, game_hero.x - 43, game_hero.y - 14, LASERSPEED * -0.22, LASERSPEED * 0.42, 115))
    if game_hero.rightCannon:
        laserAktiv.append(Laser(2, game_hero.x + 43, game_hero.y - 14, LASERSPEED * 0.22, LASERSPEED * 0.42, 65))
    if game_hero.doubleCannon:
        laserAktiv.append(Laser(3, game_hero.x - 50, game_hero.y + 36, 0, LASERSPEED * 1.2, 90))
        laserAktiv.append(Laser(4, game_hero.x + 50, game_hero.y + 36, 0, LASERSPEED * 1.2, 90))


def createEnemys():
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


def collisionHandler():
    if game_hero.hidden or game_hero.unverwundbar:
        heroRechteck = pygame.Rect(0, 0, 0, 0, )
    else:
        heroRechteck = pygame.Rect(int(game_hero.x - game_hero.width / 2), int(game_hero.y - game_hero.height / 2) + 10, game_hero.width, game_hero.height - 12)

    for mine in minesAktiv:
        mineRechteck = pygame.Rect(int(mine.x - mine.width / 2), int(mine.y - mine.height / 2), mine.width, mine.height)
        if mineRechteck.colliderect(heroRechteck):
            mine.zerstoeren(POINTS_NO)
            game_hero.treffer()
        for laser in laserAktiv:
            laserRechteck = pygame.Rect(int(laser.x - laser.width / 2) + 4, int(laser.y - laser.height / 2) + 4,
                                        laser.width - 8,
                                        laser.height - 8)

            if mineRechteck.colliderect(laserRechteck):
                laserAktiv.remove(laser)
                mine.treffer()
        for meteor in meteorsAktiv:
            meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                         meteor.originalheight - 100 * meteor.scalefaktor)
            if mineRechteck.colliderect(meteorRechteck):
                mine.zerstoeren(POINTS_NO)

    for laser in laserAktiv:
        laserRechteck = pygame.Rect(int(laser.x - laser.width / 2) + 4, int(laser.y - laser.height / 2) + 4,
                                    laser.width - 8,
                                    laser.height - 8)
        for meteor in meteorsAktiv:
            meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                         meteor.originalheight - 100 * meteor.scalefaktor)
            if laserRechteck.colliderect(meteorRechteck):
                laser.zerstoeren()

    for enemyfire in enemyfireAktiv:
        enemyfireRechteck = pygame.Rect(int(enemyfire.x - enemyfire.width / 2) + 4, int(enemyfire.y - enemyfire.height / 2) + 4, enemyfire.width - 8, enemyfire.height - 8)
        if enemyfireRechteck.colliderect(heroRechteck):
            enemyfire.aufloesen()
            game_hero.treffer()

        for meteor in meteorsAktiv:
            meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                         meteor.originalheight - 100 * meteor.scalefaktor)

            # pygame.draw.rect(screen,(255,0,0),meteorRechteck,2)
            if enemyfireRechteck.colliderect(meteorRechteck):
                enemyfire.zerstoeren()

    for enemy in enemyAktiv:
        enemyRechteck = pygame.Rect(int(enemy.x - enemy.width / 2) + 4, int(enemy.y - enemy.height / 2) + 4,
                                    enemy.width - 8,
                                    enemy.height - 8)
        for laser in laserAktiv:
            laserRechteck = pygame.Rect(int(laser.x - laser.width / 2) + 4, int(laser.y - laser.height / 2) + 4,
                                        laser.width - 8,
                                        laser.height - 8)

            if enemyRechteck.colliderect(laserRechteck):
                laserAktiv.remove(laser)
                enemy.zerstoeren(POINTS_YES)

        for meteor in meteorsAktiv:
            meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                         meteor.originalheight - 100 * meteor.scalefaktor)
            if enemyRechteck.colliderect(meteorRechteck):
                enemy.zerstoeren(POINTS_NO)

        if enemyRechteck.colliderect(heroRechteck):
            enemy.zerstoeren(POINTS_YES)
            game_hero.treffer()

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
                kanone.treffer()
        if kanoneRechteck.colliderect(heroRechteck):
            kanone.zerstoeren()
            game_hero.treffer()

    for bonus in bonusAktiv:
        bonusRechteck = pygame.Rect(int(bonus.x - bonus.width / 2) + 2, int(bonus.y - bonus.height / 2) + 2,
                                    bonus.width - 4,
                                    bonus.height - 4)
        if bonusRechteck.colliderect(heroRechteck):
            bonus.sammeln()

    # Prüfe Kollision von Gegner mit Hero
    # pygame.draw.rect(screen, WHITE, heroRechteck,2)

class LevelPanel():
    def __init__(self):
        self.x = 150
        self.y = 500
        self.image = levelImages[Level-1]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dcounter = 5
        self.alpha = 0
        self.zeigen = True

    def init(self):
        global Level
        self.image = levelImages[Level-1]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = int((SCREEN_WIDTH-self.width)/2)
        self.y = int((SCREEN_HEIGHT-self.height)/2)
        self.dcounter = 4
        self.alpha = 0
        self.zeigen = True

    def show(self):
        if self.zeigen:
            if self.alpha >= 255:
                self.dcounter =-8
            self.alpha += self.dcounter
            if self.alpha >=0:
                self.image.set_alpha(self.alpha)
                screen.blit(self.image, (self.x,self.y))
            else:
                self.zeigen = False

def allObjectsHandler():
    global background, level_panel, kanonenListcounter, timeOfLastEnemyWave, timeTillNewWave, timeOfLastMine, timeTillNewMine, timeOfLastMeteor, timeTillNewMeteor, Gegnergetroffen

    # print('Kanonen: '+str(len(kanonenAktiv))+'  Gegner: '+str(len(enemyAktiv))+'  Bonus: '+str(len(bonusAktiv))+'  Gegnerfeuer: '+str(len(enemyfireAktiv))+'  Lasers: '+str(len(laserAktiv))+'  Explosionen: '+str(len(explosionsAktiv)))

    # Hintergrund scrollen
    background.update()
    background.zeichnen()

    now = time()*1000

    # Aktive Gegnerschüsse bewegen und entfernen (werden automatisch von Enemy und Kanonen-Objekten erzeugt)
    for enemyfire in enemyfireAktiv:
        # Wenn Schuss ausserhalb des sichtbaren Spielfeldes, dann weg damit
        if enemyfire.remove or (enemyfire.y > SCREEN_BOTTOM + 20) or (enemyfire.y < SCREEN_TOP - 20) or (enemyfire.x < SCREEN_LEFT - 20) or (enemyfire.x > SCREEN_RIGHT + 20):
            enemyfireAktiv.remove(enemyfire)
        else:
            enemyfire.update()
            enemyfire.zeichnen()

    # Neue Kanonen erzeugen, bewegen und entfernen
    if len(Kanonen_y[0]) > kanonenListcounter:
        if Kanonen_y[0][kanonenListcounter] * 2 - scroll_yPos < 50:
            # nächste Kanone erzeugen
            kanonenAktiv.append(Kanone(kanonenListcounter))
            kanonenListcounter += 1
        for kanone in kanonenAktiv:
            kanone.bewegen()
            kanone.zeichnen()
            if kanone.remove or (kanone.y > SCREEN_BOTTOM + 20):
                kanonenAktiv.remove(kanone)

    if (now - timeOfLastMine > timeTillNewMine):
        timeOfLastMine = time() * 1000
        timeTillNewMine = int(random.uniform(10000, 15000))
        minesAktiv.append(Mine())
    for mine in minesAktiv:
        if (mine.remove) or (mine.y > SCREEN_BOTTOM + 20):
            minesAktiv.remove(mine)
        else:
            mine.bewegen()
            mine.zeichnen()

    if (now - timeOfLastMeteor > timeTillNewMeteor):
        timeOfLastMeteor = time() * 1000
        timeTillNewMeteor = int(random.uniform(10000, 20000))
        meteorsAktiv.append(Meteor())
    for meteor in meteorsAktiv:
        if (meteor.remove) or (meteor.y > SCREEN_BOTTOM + 60) or (meteor.x < SCREEN_LEFT - 60) or (meteor.x > SCREEN_RIGHT + 60):
            meteorsAktiv.remove(meteor)
        else:
            meteor.bewegen()
            meteor.zeichnen()

    # neue Gegnerwellen erzeugen, bewegen und entfernen
    if now - timeOfLastEnemyWave > timeTillNewWave:  # In Abhängigkeit vom Level neue Welle nach Zufallszeitspanne erzeugen
        createEnemys()
        timeOfLastEnemyWave = time() * 1000  # aktuelle Zeit als neuen Bezugspunkt festlegen
        timeTillNewWave = int(random.uniform(4000, 6000) - Level * 500)  # Zufallszeitspanne bis zu nächster Welle festlegen
    for enemy in enemyAktiv:  # alle gerade aktiven Gegner-Objekte animieren
        if (enemy.remove) or (enemy.y > SCREEN_BOTTOM + 20):
            enemyAktiv.remove(enemy)
        else:
            enemy.update()
            enemy.zeichnen()

    # Aktive Explosionen ausführen und entfernen
    for explosion in explosionsAktiv:  # alle gerade aktiven Explosions-Objekte animieren
        if explosion.fertig:  # wenn Explosionssequenz fertig ist, denn Objekt löschen
            explosionsAktiv.remove(explosion)
        else:  # sonst Objekt animieren
            explosion.explode()
            explosion.bewegen()

    # Bonussymbole erzeugen, bewegen und entfernen
    if Gegnergetroffen > 6 - Level:
        Gegnergetroffen = 0
        bonusAktiv.append(Bonus(0))

    for bonus in bonusAktiv:
        if (bonus.remove) or (bonus.y > SCREEN_BOTTOM + 20):
            bonusAktiv.remove(bonus)
        else:
            bonus.bewegen()
            bonus.zeichnen()

    # eigenes Raumschiff animieren und zeichnen
    game_hero.update()
    game_hero.zeichnen()

    # Laser bewegen und entfernen (werden automatisch von Hero-Objekt erzeugt)
    for laser in laserAktiv:
        if (laser.remove) or (laser.y > SCREEN_BOTTOM + 20) or (laser.y < SCREEN_TOP - 20) or (laser.x < SCREEN_LEFT - 20) or (laser.x > SCREEN_RIGHT + 20):
            laserAktiv.remove(laser)
        else:
            laser.bewegen()
            laser.zeichnen()

    # über alles den Rahmen der Gamekonsole legen
    game_console.zeichnen()

    if level_panel.zeigen:
        level_panel.show()

def startLevel():
    global game_Mode, level_panel, timeOfLastEnemyWave,timeTillNewWave,timeOfLastMine,timeTillNewMine,timeOfLastMeteor,timeTillNewMeteor, game_backgroundmusic, showLevel

    pygame.mouse.set_visible(False)
    # Initialisiere Zeiten
    now = time()*1000
    timeOfLastEnemyWave = now
    timeTillNewWave = int(random.uniform(2000, 4000))
    timeOfLastMine = now
    timeTillNewMine = int(random.uniform(20000, 25000))
    timeOfLastMeteor = now
    timeTillNewMeteor = int(random.uniform(5000, 10000))
    game_Mode = NORMAL_RUN
    game_backgroundmusic.sound.set_volume(0.3)
    game_backgroundmusic.sound.play(-1)

    level_panel.init()

background = ScrollingBackground()
game_hero = Hero()
game_console = GameConsole()
game_backgroundmusic = BackgroundSongs()
game_titel = Titel()
level_panel = LevelPanel()
pygame.mouse.set_visible(True)

mousepressed = False

# Game Loop
while True:
    act_time = time() * 1000
    # Cycles through all occurring events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.mouse.set_visible(True)
            pygame.quit()
            sys.exit()
        if event.type == BUTTON_DOWN_PRESSED:
            if Level > 1:
                Level -= 1
        if event.type == BUTTON_UP_PRESSED:
            if Level < 4:
                Level += 1
        if event.type == BUTTON_START_PRESSED:
            game_titel.ausblenden()
            startLevel()

        if event.type == MOUSEBUTTONUP:
            mousepressed = False

    if game_Mode == START:
        # Zeige Titelbild mit Buttons
        game_titel.update()
        game_titel.zeichnen()
        mouseButton = pygame.mouse.get_pressed()
        if mouseButton[0]:
            if not mousepressed:
                mousepressed=True
                game_titel.checkselection()
    if game_Mode == NORMAL_RUN:
        # Abfrage, ob Taste gedrückt
        gedrueckt = pygame.key.get_pressed()
        # Linkspfeil gedrückt
        if gedrueckt[K_a]:
            if smallbonusavailable:
                smallbonusavailable = False
                bonusAktiv.append(Bonus(9))
        if gedrueckt[K_s]:
            if mediumbonusavailable:
                mediumbonusavailable = False
                bonusAktiv.append(Bonus(10))
        if gedrueckt[K_d]:
            if largebonusavailable:
                largebonusavailable = False
                bonusAktiv.append(Bonus(11))
        mouseButton = pygame.mouse.get_pressed()
        if mouseButton[0]:
            if game_hero.aktiv:  # Schüsse abgeben mit linker Maustaste
                if (act_time - timeLastShot) > 1000 / game_hero.firepower:
                    createLasers()
                    timeLastShot = time() * 1000
        allObjectsHandler()
        collisionHandler()
        if mouseButton[2]:  # Zünde Megabombe mit rechter Maustaste
            if game_hero.has_megabomb():
                game_hero.zuendeMegabombe()

    pygame.display.update()
    clock.tick(FPS)
