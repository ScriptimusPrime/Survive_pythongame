# Imports
import pygame, sys, math
from pygame.locals import *
from pygame import image, mixer

import random, time
from time import *

# Initializing
pygame.init()

# Frames per Second festlegen
FPS = 60
clock = pygame.time.Clock()
mixer.set_num_channels(30)

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
SCREEN_HEIGHT = 800
SPEED = 5
SCORE = 0
LASERSPEED = 30
SCROLLSPEED = 2

Level = 1

# Fonts festlegen
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Fenster erstellen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BLACK)
pygame.display.set_caption("Survive")
# mouse.set_visible(False)
laserImages = [image.load('Laser/beam2.png'), image.load('Laser/beaml.png'), image.load('Laser/beamr.png'),
               image.load('Laser/beamdl.png'), image.load('Laser/beamdr.png')]
laserSounds = [mixer.Sound('Sounds/Laser0.wav'), mixer.Sound('Sounds/Laser1.wav'), mixer.Sound('Sounds/Laser1.wav'),
               mixer.Sound('Sounds/Laser4.wav'), mixer.Sound('Sounds/Laser4.wav'), ]
explosionSounds = [mixer.Sound('Explosionssounds/exp1.wav'), mixer.Sound('Explosionssounds/exp2.wav'),
                   mixer.Sound('Explosionssounds/exp3.wav'), mixer.Sound('Explosionssounds/exp4.wav'),
                   mixer.Sound('Explosionssounds/exp5.wav'), mixer.Sound('Explosionssounds/exp6.wav'),
                   mixer.Sound('Explosionssounds/exp7.wav'), mixer.Sound('Explosionssounds/exp8.wav'),
                   mixer.Sound('Explosionssounds/exp9.wav')]


class GameConsole():
    def __init__(self):
        self.x = 0
        self.y = 720

    def zeichnen(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 960, 80), 0)


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
        global scroll_yPos
        self.bottomTile += self.movingDownSpeed
        self.topTile += self.movingDownSpeed
        scroll_yPos += self.movingDownSpeed

        if self.bottomTile >= 720:
            self.bottomTile = 0
            self.topTile = -720
            self.bCounter += 1

    def zeichnen(self):
        screen.blit(self.bgField[self.bCounter].image, (0, self.bottomTile))
        screen.blit(self.bgField[self.bCounter + 1].image, (0, self.topTile))


class Hero():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.mode = 0
        self.image = []
        self.leftCannon = 0
        self.rightCannon = 0
        self.doubleCannon = 0
        self.rotatedImage = [image.load("Hero/Hero0.png"), image.load("Hero/Hero1.png"),
                             image.load("Hero/Hero2.png"), image.load("Hero/Hero3.png"),
                             image.load("Hero/Hero4.png"), image.load("Hero/Hero5.png"),
                             image.load("Hero/Hero6.png"), image.load("Hero/Hero7.png")]
        for i in range(8):
            self.image.append(pygame.transform.rotate(self.rotatedImage[i], 90))
            self.image[i] = pygame.transform.scale(self.image[i], (105, 90))
        self.height = self.image[0].get_height()
        self.width = self.image[0].get_width()

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        if self.y > 710:
            self.y = 710
        self.mode = self.leftCannon + self.rightCannon * 2 + self.doubleCannon * 4

    def zeichnen(self):
        screen.blit(self.image[self.mode], (self.x - int(self.width / 2), self.y - int(self.height / 2)))


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


class Enemy():
    def __init__(self, enemytyp, formation, fireTyp, drehbar, x, y, shield):
        self.enemyTyp = enemytyp
        self.formation = formation
        self.fireTyp = fireTyp
        self.drehbar = drehbar
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

    def bewegen(self):
        global game_hero

        if self.drehbar:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            self.image = pygame.transform.rotate(self.originalImage, int(angle))
            # self.rect = self.image.get_rect(center=(480, 400))
        else:
            self.image = pygame.transform.rotate(self.originalImage, -90)
        self.y += 5
        if self.formation == 1:
            self.x -= 6
        elif self.formation == 2:
            self.x += 6
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.origin_x = self.x - self.width / 2
        self.origin_y = self.y - self.height / 2

    def zeichnen(self):
        screen.blit(self.image, (self.origin_x, self.origin_y))
        image_rect = (self.x - self.width / 2, self.y - self.height / 2, self.width,
                      self.height)  # self.image.get_rect(center=(280, 300))


class Explosion():
    def __init__(self, x_pos, y_pos, size, exp_type):
        self.x = x_pos
        self.y = y_pos
        self.size = size
        self.exp_type = exp_type
        self.image = []
        self.expImageCount = [0, 7, 19, 7, 17, 12, 16, 20, 11, 10, 7]
        self.expScale = [0, 0.7, 0.7, 0.7, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
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
        self.expsound.set_volume(0.2)
        self.expsound.play()

    def bewegen(self):
        self.y += SCROLLSPEED

    def explode(self):
        self.image_number += 1
        if self.image_number < self.expImageCount[self.exp_type]:
            self.height = self.image[self.image_number].get_height()
            self.width = self.image[self.image_number].get_width()
            screen.blit(self.image[self.image_number], (self.x - int(self.width / 2), self.y - int(self.height / 2)))


class Kanone():
    def __init__(self, number):
        self.number = number
        self.typ = int(random.uniform(1, 5))
        self.drehbar = (int(random.uniform(1, 5)) == 1)
        self.kapazitaet = int(random.uniform(0, 4))
        self.feuerabstand = int(random.uniform(4, 7))
        self.feuerzuletzt = time() * 1000
        self.x = Kanonen_x[0][self.number] * 2  # erstes Feld später für Level
        self.y = scroll_yPos - Kanonen_y[0][self.number] * 2
        self.richtung = int(random.uniform(0, 90))
        if self.x > 240:
            self.richtung *= -1
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
            if not self.drehbar:
                self.originalImage[i] = pygame.transform.rotate(self.originalImage[i], -90)
        self.image = self.originalImage[0]
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()

    def bewegen(self):
        global game_hero

        if self.drehbar:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            self.image = pygame.transform.rotate(self.originalImage[self.kapazitaet], int(angle))
        else:
            self.image = pygame.transform.rotate(self.originalImage[self.kapazitaet], self.richtung)
        self.y += SCROLLSPEED
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.origin_x = self.x - self.width / 2
        self.origin_y = self.y - self.height / 2

    def zeichnen(self):
        screen.blit(self.image, (self.origin_x, self.origin_y))
        image_rect = (self.x - self.width / 2, self.y - self.height / 2, self.width,
                      self.height)  # self.image.get_rect(center=(280, 300))


def explosionHandler():
    global explosionsAktiv
    for explosion in explosionsAktiv:
        if not explosion.fertig:
            explosion.explode()
            explosion.bewegen()
        else:
            explosionAktiv.remove(explosion)


def enemyHandler():
    global enemyAktiv, lastWavePos
    waveDistance = 200
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
            enemyAktiv.append(Enemy(typ, formation, fire_typ, drehbar, x_start, y_start, False))

    for enemy in enemyAktiv:
        if enemy.y < SCREEN_HEIGHT - 20:
            enemy.bewegen()
            enemy.zeichnen()
        else:
            enemyAktiv.remove(enemy)


def collisionHandler():
    global enemyAktiv, laserAktiv, explosionsAktiv

    heroRechteck = pygame.Rect(int(game_hero.x-game_hero.width / 2), int(game_hero.y-game_hero.height/2)+10, game_hero.width,game_hero.height-12)

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
            enemy.remove=True
            print ('Held tot')

        if enemy.remove:
            explosionsAktiv.append(Explosion(enemy.x, enemy.y, 100, int(random.uniform(1, 8))))
            enemyAktiv.remove(enemy)
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
                kanone.kapazitaet=-1
            if kanone.kapazitaet < 0:
                    kanone.remove = True
            if kanone.remove:
                explosionsAktiv.append(Explosion(kanone.x, kanone.y, 100, int(random.uniform(1, 8))))
                kanonenAktiv.remove(kanone)

    # Prüfe Kollision von Gegner mit Hero
    #pygame.draw.rect(screen, WHITE, heroRechteck,2)



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
explosionsAktiv = []
kanonenAktiv = []

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
            if (act_time - last_time) > 300:
                game_schuesse.feuer()
                last_time = time() * 1000
        backgroundHandler()
        game_hero.update()
        game_hero.zeichnen()
        kanonenHandler()
        enemyHandler()
        laserHandler()

        collisionHandler()
        explosionHandler()

        for l in laserAktiv:
            l.zeichnen()
        # Gegner bewegen
        game_console.zeichnen()

    pygame.display.update()
    clock.tick(FPS)
