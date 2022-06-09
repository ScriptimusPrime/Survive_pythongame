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

# SHOWRECTS = True
SHOWRECTS = False

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
LEVEL_START = 2
NORMAL_RUN = 3
BOSS_ENTER = 4
BOSS_RUN = 5
LEVEL_ENDE = 6
SPIEL_ENDE = 7
GAME_OVER = 8
WAIT = 9

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
LEVEL_ENDE_EVENT = USEREVENT + 4
SPIEL_ENDE_EVENT = USEREVENT + 5

Kanonen_x = [
    [59, 42, 36, 36, 72, 313, 304, 299, 275, 267, 260, 431, 204, 202, 444, 442, 114, 262, 408, 358, 358, 40, 278, 35, 263],
    [22, 55, 210, 162, 172, 222, 320, 328, 103, 379, 297, 306, 356, 69, 304, 220, 418, 26, 144, 26, 453, 298, 290, 171, 247, 266, 283, 392, 239, 362, 382, 278, 400, 210, 62, 308, 54, 247, 471, 70, 356, 174, 255, 68, 99, 166, 232, 82, 178, 242, 98,
     189, 253, 130, 115, 290, 467, 322, 179, 42, 83, 448, 352, 253, 102, 465, 81, 231, 278, 453, 378],
    [249, 164, 250, 192, 306, 152, 348, 460, 38, 138, 360, 360, 139, 123, 376, 325, 230, 81, 416, 250, 96, 402, 250, 145, 353, 250, 250, 147, 349, 154, 344, 248, 251, 144, 355, 141, 354, 141, 354, 141, 34, 141, 354, 174, 324, 249, 250, 250, 40, 456,
     248, 248, 89, 409, 58, 442, 52, 446, 255, 32, 467, 116, 383, 249, 21, 472, 249, 250, 47, 455, 249, 8, 204, 294, 250, 250, 128, 372, 16, 32, 467, 48, 450, 66, 424, 250, 88, 411, 249, 105, 394, 250, 69, 426, 127, 370, 250, 250, 200, 298],
    [86, 228, 363, 259, 103, 35, 323, 451, 385, 421, 368, 452, 34, 387, 281, 179, 41, 284, 212, 79, 319, 69, 326, 260, 219, 73, 6, 283, 249, 215, 182, 174, 280, 79, 147, 1, 275, 207, 74, 1, 168, 275, 63, 451, 210, 177, 142, 261, 108, 73, 378, 361,
     341, 196, 179, 161, 91, 187, 87, 152, 326, 304, 284, 263, 23, 442, 8, 247, 191, 60, 163, 301, 96, 257, 124, 208, 81, 444, 152, 353, 258, 33, 290, 166, 3, 259, 435, 249, 172, 334, 83, 7, 355, 23, 370, 386, 396, 403, 129, 208, 412, 98, 386, 359,
     328, 261, 45, 464, 376, 278, 241, 331, 391, 325, 407, 46, 146, 300, 422, 252, 226, 366, 417, 276, 332, 8, 136, 266, 410, 96, 93, 150, 205, 431, 343, 447, 271, 161, 455, 362, 114, 446, 141, 451, 434, 446, 394, 340, 115, 14, 268, 330, 61, 138,
     450, 273, 25, 147, 85, 340, 468, 399, 439, 387, 472, 71, 133, 46, 291, 31, 390, 211, 25, 242, 444, 20, 164, 418, 347, 261, 45, 259, 342, 150, 420, 167, 56, 240, 116, 330, 434, 247, 161, 446, 273, 351, 417, 272, 474, 344, 201, 440, 269, 378, 5,
     280, 352, 203, 415, 279, 133, 203, 371, 466, 266, 199, 157, 398, 364, 331, 299, 433, 130, 380, 343, 210, 25]]
Kanonen_y = [
    [2127, 2369, 2451, 2545, 2683, 3782, 3925, 4064, 4677, 4825, 4958, 6240, 6273, 6337, 6396, 6464, 6629, 6641, 6929, 6977, 7043, 7331, 7343, 7558, 7571],
    [377, 600, 750, 888, 960, 1001, 1193, 1261, 1305, 1305, 1460, 1530, 1574, 1613, 1686, 1890, 2071, 2110, 2370, 2543, 2607, 2665, 2841, 2860, 2980, 3119, 3257, 3489, 3508, 3866, 4006, 4034, 4143, 4464, 4482, 4593, 4737, 4747, 4753, 4927, 4954,
     5193, 5259, 5290, 5350, 5371, 5401, 5417, 5456, 5494, 5538, 5542, 5578, 5600, 5664, 5813, 6044, 6061, 6080, 6097, 6304, 6545, 6557, 6568, 6684, 6839, 6847, 7050, 7289, 7451, 7576],
    [773, 996, 1354, 1490, 1490, 1786, 1788, 1790, 1792, 2011, 2012, 2069, 2070, 2146, 2147, 2302, 2545, 2620, 2620, 2842, 3044, 3044, 3072, 3104, 3104, 3383, 3494, 3502, 3502, 3599, 3599, 3780, 4000, 4126, 4126, 4313, 4313, 4369, 4369, 4460, 4460,
     4518, 4518, 4579, 4579, 4964, 5204, 5350, 5592, 5592, 5773, 5992, 6100, 6102, 6310, 6310, 6474, 6474, 6602, 6648, 6648, 6962, 6962, 7134, 7409, 7409, 7414, 7696, 7760, 7760, 7840, 8199, 8234, 8234, 8544, 8691, 8772, 8772, 9016, 9090, 9090, 9163,
     9163, 9235, 9235, 9434, 9492, 9492, 9602, 9620, 9620, 9758, 9769, 9769, 10008, 10008, 10058, 10188, 10278, 10278],
    [450, 471, 485, 609, 658, 670, 684, 703, 717, 786, 837, 850, 1123, 1226, 1279, 1300, 1321, 1680, 1776, 1808, 1832, 2320, 2444, 2457, 2511, 2604, 2617, 2653, 2673, 2694, 2715, 2874, 2893, 2985, 3013, 3035, 3036, 3050, 3060, 3105, 3106, 3166, 3173,
     3176, 3241, 3262, 3281, 3294, 3300, 3419, 4387, 4415, 4442, 4658, 4684, 4710, 4741, 4881, 4916, 5003, 5088, 5138, 5189, 5243, 5346, 5379, 5623, 5845, 5984, 6157, 6196, 6365, 6447, 6467, 6787, 6857, 6888, 6968, 6973, 7039, 7110, 7232, 7309, 7318,
     8276, 8456, 8509, 8663, 8733, 8945, 8955, 8977, 9076, 9085, 9206, 9343, 9471, 9611, 9635, 9737, 9755, 9776, 9788, 9824, 9862, 9975, 10379, 10892, 10958, 11063, 11338, 11452, 11475, 11576, 11675, 11669, 11957, 12023, 12075, 12309, 12364, 12390,
     12562, 12600, 12624, 12894, 13066, 13236, 13409, 13518, 13787, 13796, 13805, 13930, 14219, 14278, 14291, 14330, 14443, 14548, 14585, 14696, 14819, 14836, 14988, 15453, 15462, 15476, 15701, 15777, 15780, 16162, 16188, 16198, 16242, 16287, 16318,
     16335, 16348, 16360, 16372, 16393, 16460, 16516, 16524, 16688, 16821, 16880, 17037, 17064, 17179, 17254, 17490, 17567, 17590, 17603, 17633, 17748, 17760, 17765, 17832, 17920, 17991, 18039, 18137, 18151, 18173, 18219, 18248, 18445, 18505, 18599,
     18619, 18699, 18724, 18809, 18838, 18858, 18875, 18884, 18906, 18925, 18931, 19164, 19204, 19279, 19309, 19330, 19349, 19352, 19375, 19399, 19402, 19467, 19470, 19484, 19537, 19537, 19560, 19580, 19603, 19608, 19629, 19630, 19659, 19738, 19860]]
Kanonen_Versatz = [38, 38, 340, 750]
Background_Mapping = [3, 1, 2, 4]
Background_Count = [24, 24, 31, 57]
Bonus_Map = [1, 1, 2, 2, 2, 2, 3, 4, 4, 4, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8]
Boss_Bahn_x = [12, 12, 10, 10, 8, 7, 7, 6, 6, 6, 6, 6, 6, 5, 5, 5, 4, 4, 3, 3, 2, 1, 1, 0, 0, -1, -1, -2, -3, -3, -4, -4, -5, -5, -5, -6, -6, -6, -6, -6, -6, -7, -7, -8, -10, -10, -12, -12, -12, -12, -10, -10, -8, -7, -7, -6, -6, -6, -6, -6, -6, -5,
               -5, -5, -4, -4, -3, -3, -2, -1, -1, 0, 0, 1, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 8, 10, 10, 12, 12]
Boss_Bahn_y = [-6, -6, -5, -4, -4, -3, -2, -2, -1, -1, 0, 0, 0, 0, 1, 1, 2, 2, 3, 4, 4, 5, 6, 6, 6, 6, 5, 4, 4, 3, 2, 2, 1, 1, 0, 0, 0, 0, -1, -1, -2, -2, -3, -4, -4, -5, -6, -6, -6, -6, -5, -4, -4, -3, -2, -2, -1, -1, 0, 0, 0, 0, 1, 1, 2, 2, 3, 4,
               4, 5, 6, 6, 6, 6, 5, 4, 4, 3, 2, 2, 1, 1, 0, 0, 0, -1, -1, -2, -2, -3, -4, -4, -5, -6, -6]
Boss_Kanone_x = [[-38, -21, -96, 69, 80, 31, -75, 76, -96, 4, 2, -40, 106], [-27, -48, -65, -113, 65, 48, 27, 113, 1, 82, -82, -35, 35],
                 [-112, 112, -71, 71, -11, 11, 0, -94, 94, -151, 151, -93, 93, 30, -30, -45, 45], [-103, 103, -134, 134, -121, 121, -62, 62, -16, 16, -43, 43, -72, 72, -83, 83, -155, 155, -147, 147]]
Boss_Kanone_y = [[-22, -40, -33, -47, -48, -38, -21, 23, 16, -48, 14, 20, 3], [-53, -53, -23, 6, -23, -53, -53, 6, -4, -7, -7, 15, 15], [-30, -30, -23, -23, -41, -41, 4, 22, 22, -46, -46, -23, -23, -11, -11, -15, -15],
                 [-20, -20, -10, -10, -31, -31, -55, -55, -19, -19, -61, -61, -46, -46, -7, -7, 52, 52, -7, -7]]
Boss_Kanone_typ = [[2, 2, 2, 2, 3, 3, 3, 1, 1, 1, 4, 4, 4], [2, 2, 2, 2, 3, 3, 3, 3, 1, 1, 1, 4, 4], [4, 4, 4, 4, 4, 4, 1, 1, 1, 3, 2, 3, 2, 2, 3, 2, 3], [1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3]]
Boss_Kanone_hits = [[3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 2, 2, 2], [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 2, 2], [5, 5, 5, 5, 5, 5, 6, 6, 6, 5, 5, 5, 5, 6, 6, 6, 6], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6]]
Boss_Kanone_dy = [5, 0, 19, 50]

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
SCROLLSPEED = 4
POINTS_NO = False
POINTS_YES = True

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
laserImages = [image.load('Laser/beam2.png'), image.load('Laser/beaml.png'), image.load('Laser/beamr.png'), image.load('Laser/beamdl.png'), image.load('Laser/beamdr.png')]
gegnerImages = [image.load('Enemys/1n.png'), image.load('Enemys/2n.png'), image.load('Enemys/3n.png'), image.load('Enemys/4n.png'), image.load('Enemys/5n.png'), image.load('Enemys/6n.png'), image.load('Enemys/7n.png'), image.load('Enemys/8n.png'),
                image.load('Enemys/9n.png'), image.load('Enemys/1s.png'), image.load('Enemys/2s.png'), image.load('Enemys/3s.png'), image.load('Enemys/4s.png'), image.load('Enemys/5s.png'), image.load('Enemys/6s.png'), image.load('Enemys/7s.png'),
                image.load(
                    'Enemys/8s.png'), image.load('Enemys/9s.png')]
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
levelImages = [image.load('Sonstiges/Levelende.png'), image.load('Sonstiges/Level1.png'), image.load('Sonstiges/Level2.png'), image.load('Sonstiges/Level3.png'), image.load('Sonstiges/Level4.png')]
buttonImages = [image.load('Sonstiges/Button_up.png'), image.load('Sonstiges/Button_down.png'), image.load('Sonstiges/Button_start.png'), image.load('Sonstiges/Levelwahl1.png'), image.load('Sonstiges/Levelwahl2.png'),
                image.load('Sonstiges/Levelwahl3.png'), image.load('Sonstiges/Levelwahl4.png')]
schutzschildImages = [image.load('Schutzschild/0.png'), image.load('Schutzschild/1.png'), image.load('Schutzschild/2.png'), image.load('Schutzschild/3.png'), image.load('Schutzschild/4.png')]
mineImages = [image.load('Mine/1.png'), image.load('Mine/2.png'), image.load('Mine/3.png'), image.load('Mine/4.png')]
meteorImage = [image.load('Meteor/meteor.png')]
zahlImages = [image.load('Zahlen/0.png'), image.load('Zahlen/1.png'), image.load('Zahlen/2.png'), image.load('Zahlen/3.png'), image.load('Zahlen/4.png'), image.load('Zahlen/5.png'), image.load('Zahlen/6.png'), image.load('Zahlen/7.png'),
              image.load('Zahlen/8.png'), image.load('Zahlen/9.png')]
bossImages = [image.load('Boss/boss1.png'), image.load('Boss/boss2.png'), image.load('Boss/boss3.png'), image.load('Boss/boss4.png')]
Boss_Kanone_Image = [[image.load('Boss/1-1.png'), image.load('Boss/1-2.png'), image.load('Boss/1-3.png'), image.load('Boss/1-4.png'), image.load('Boss/1-5.png'), image.load('Boss/1-6.png')],
                     [image.load('Boss/2-1.png'), image.load('Boss/2-2.png'), image.load('Boss/2-3.png'), image.load('Boss/2-4.png'), image.load('Boss/2-5.png'), image.load('Boss/2-6.png')],
                     [image.load('Boss/3-1.png'), image.load('Boss/3-2.png'), image.load('Boss/3-3.png'), image.load('Boss/3-4.png'), image.load('Boss/3-5.png'), image.load('Boss/3-6.png')],
                     [image.load('Boss/4-1.png'), image.load('Boss/4-2.png'), image.load('Boss/4-3.png'), image.load('Boss/4-4.png'), image.load('Boss/4-5.png'), image.load('Boss/4-6.png')]]
laserSounds = [mixer.Sound('Sounds/Laser0.wav'), mixer.Sound('Sounds/Laser1.wav'), mixer.Sound('Sounds/Laser4.wav')]
explosionSounds = [mixer.Sound('Explosionssounds/exp1.wav'), mixer.Sound('Explosionssounds/exp2.wav'), mixer.Sound('Explosionssounds/exp3.wav'), mixer.Sound('Explosionssounds/exp4.wav'),
                   mixer.Sound('Explosionssounds/exp5.wav'), mixer.Sound('Explosionssounds/exp6.wav'), mixer.Sound('Explosionssounds/exp7.wav'), mixer.Sound('Explosionssounds/exp8.wav'),
                   mixer.Sound('Explosionssounds/exp9.wav')]
bonusSounds = [mixer.Sound('Bonussounds/1.mp3'), mixer.Sound('Bonussounds/2.wav'), mixer.Sound('Bonussounds/3.mp3'),
               mixer.Sound('Bonussounds/4.wav'), mixer.Sound('Bonussounds/5.wav'), mixer.Sound('Bonussounds/6.mp3'),
               mixer.Sound('Bonussounds/7.wav'), mixer.Sound('Bonussounds/8.wav'), mixer.Sound('Bonussounds/9.mp3'),
               mixer.Sound('Bonussounds/10.wav'), mixer.Sound('Bonussounds/11.wav'), mixer.Sound('Bonussounds/Plopp.wav')]
ingamemusicSounds = ['Sounds/Act of War.mp3','Sounds/We will meet again.mp3','Sounds/determined_pursuit_loop.mp3','Sounds/Are You With Us.mp3']


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
        self.timeTillNewWave = int(random.uniform(2000, 4000))
        self.timeOfLastMine = now() + int(random.uniform(10000,15000))
        self.timeTillNewMine = int(random.uniform(20000, 25000))
        self.timeOfLastMeteor = now() + int(random.uniform(10000,15000))
        self.timeTillNewMeteor = int(random.uniform(5000, 10000))
        self.timeLastShot = now()
        self.showLevel = True
        self.Gegnergetroffen = 0
        self.smallbonusavailable = True
        self.mediumbonusavailable = True
        self.largebonusavailable = True

    def setzeMode(self,mode):
        self.Mode = mode
        print("game.Mode auf %i gesetzt", self.Mode)

    def erhoeheklc(self):
        self.kanonenListcounter += 1

    def resetGegnergetroffen(self):
        self.Gegnergetroffen = 0

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
        global game
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
        self.lasersound = laserSounds[0]
        self.sidelasersound = laserSounds[1]
        self.doublelasersound = laserSounds[2]

        self.lasersound.set_volume(0.09)
        self.sidelasersound.set_volume(0.09)
        self.doublelasersound.set_volume(0.1)

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
        self.originalImage = meteorImage[0]  # immer als Referenz für alle Drehungen
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
        game_hero.addPoints(20000)


class Enemy():
    def __init__(self, enemytyp, formation, fireTyp, drehbar, x, y, speed):
        global game
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
        global game_hero, enemyfireAktiv

        if self.hasshield:
            if now() - self.shieldtimer > self.shieldduration:
                self.wechselSchutzschild()
                self.shieldtimer = now()
                self.ladeGegnerImage()
        self.y += self.speed
        if self.y < SCREEN_BOTTOM + 20:
            if self.drehbar:
                self.angle = pygame.math.Vector2(self.x - game_hero.x, self.y - game_hero.y).angle_to((-1, 0))
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
        global game
        explosionsAktiv.append(Explosion(self.x, self.y, 0, int(random.uniform(1, 8)), self.speed))
        self.aufloesen()
        if getPoints:
            game.Gegnergetroffen += 1
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
        global game
        explosionsAktiv.append(Explosion(self.x, self.y, 0, 1, SCROLLSPEED))
        self.aufloesen()
        if getPoints:
            game.Gegnergetroffen += 1
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
        global game_hero

        if self.y < SCREEN_BOTTOM + 30:
            if self.drehbar:
                self.angle = self.angle = pygame.math.Vector2(self.x - game_hero.x, self.y - game_hero.y).angle_to((-1, 0))

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
        global game
        explosionsAktiv.append(Explosion(self.x, self.y, 0, int(random.uniform(1, 8)), SCROLLSPEED))
        self.aufloesen()
        game.Gegnergetroffen += 1
        game_hero.addPoints(self.startkapazitaet * 500)


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
        global game
        explosionsAktiv.append(Explosion(self.x, self.y, 0, int(random.uniform(1, 8)), SCROLLSPEED))
        self.remove = True
        boss.kanonezerstoert()
        game.Gegnergetroffen += 1
        game_hero.addPoints(self.startkapazitaet * 500)

    def update(self):
        self.angle = pygame.math.Vector2(self.x - game_hero.x, self.y - game_hero.y).angle_to((-1, 0))

        self.image = pygame.transform.rotate(self.originalImage, int(self.angle))
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def updateImage(self):
        self.originalImage = Boss_Kanone_Image[self.typ - 1][self.kapazitaet - 1]

    def bewegen(self):
        global boss
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
        global game
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
        global game
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
        #        if self.bosskanonencount<0:
        #            self.bosskanonencount=0
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
    laserAktiv.append(Laser(0, game_hero.x, game_hero.y - 56, 0, LASERSPEED * 0.5, 90))
    if game_hero.leftCannon:
        laserAktiv.append(Laser(1, game_hero.x - 43, game_hero.y - 14, LASERSPEED * -0.22, LASERSPEED * 0.42, 115))
    if game_hero.rightCannon:
        laserAktiv.append(Laser(2, game_hero.x + 43, game_hero.y - 14, LASERSPEED * 0.22, LASERSPEED * 0.42, 65))
    if game_hero.doubleCannon:
        laserAktiv.append(Laser(3, game_hero.x - 50, game_hero.y + 36, 0, LASERSPEED * 1.2, 90))
        laserAktiv.append(Laser(4, game_hero.x + 50, game_hero.y + 36, 0, LASERSPEED * 1.2, 90))
    # Wähle abzuspielden Sound aus
    if game_hero.doubleCannon:
        game_hero.doublelasersound.set_volume(0.1)
        game_hero.doublelasersound.play()
    elif game_hero.leftCannon or game_hero.rightCannon:
        game_hero.sidelasersound.set_volume(0.09)
        game_hero.sidelasersound.play()
    else:
        game_hero.lasersound.set_volume(0.09)
        game_hero.lasersound.play()


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
    if game_hero.hidden or game_hero.unverwundbar:
        heroRechteck1 = heroRechteck2 = pygame.Rect(0, 0, 0, 0, )
    else:
        heroRechteck1 = pygame.Rect(game_hero.x - 50, game_hero.y, 102, 36)
        heroRechteck2 = pygame.Rect(game_hero.x - 9, game_hero.y - 35, 20, 80)
        if SHOWRECTS:
            pygame.draw.rect(screen, RED, heroRechteck1, 2)
            pygame.draw.rect(screen, RED, heroRechteck2, 2)
    for mine in minesAktiv:
        if SCREEN_TOP < mine.y < SCREEN_BOTTOM and SCREEN_LEFT < mine.x < SCREEN_RIGHT:
            mineRechteck = pygame.Rect(mine.x - 30, mine.y - 30, 60, 60)
            if SHOWRECTS:  pygame.draw.rect(screen, RED, mineRechteck, 2)

            if mineRechteck.colliderect(heroRechteck1) or mineRechteck.colliderect((heroRechteck2)):
                mine.zerstoeren(POINTS_NO)
                game_hero.treffer()
            for laser in laserAktiv:
                laserRechteck = pygame.Rect(laser.x - 3, laser.y - 3, 6, 6)

                if mineRechteck.colliderect(laserRechteck):
                    if mine.kapazitaet > 0:
                        laser.zerstoeren()
                    else:
                        laser.aufloesen()
                    mine.treffer()
            for meteor in meteorsAktiv:
                meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                             meteor.originalheight - 100 * meteor.scalefaktor)
                if mineRechteck.colliderect(meteorRechteck):
                    mine.zerstoeren(POINTS_NO)

    for laser in laserAktiv:
        laserRechteck = pygame.Rect(laser.x - 3, laser.y - 3, 6, 6)
        if SHOWRECTS: pygame.draw.rect(screen, RED, laserRechteck, 2)
        for meteor in meteorsAktiv:
            meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                         meteor.originalheight - 100 * meteor.scalefaktor)
            if laserRechteck.colliderect(meteorRechteck):
                laser.zerstoeren()

    for enemyfire in enemyfireAktiv:
        #        enemyfireRechteck = pygame.Rect(int(enemyfire.x - enemyfire.width / 2) + 4, int(enemyfire.y - enemyfire.height / 2) + 4, enemyfire.width - 8, enemyfire.height - 8)
        enemyfireRechteck = pygame.Rect(enemyfire.x - 3, enemyfire.y - 3, 6, 6)
        if SHOWRECTS: pygame.draw.rect(screen, RED, enemyfireRechteck, 2)
        if enemyfireRechteck.colliderect(heroRechteck1) or enemyfireRechteck.colliderect(heroRechteck2):
            enemyfire.zerstoeren()
            game_hero.treffer()

        for meteor in meteorsAktiv:
            meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                         meteor.originalheight - 100 * meteor.scalefaktor)

            # pygame.draw.rect(screen,(255,0,0),meteorRechteck,2)
            if enemyfireRechteck.colliderect(meteorRechteck):
                enemyfire.zerstoeren()

    if game.Mode == BOSS_RUN:
        for bosskanone in bosskanonenAktiv:
            bosskanoneRechteck = pygame.Rect(bosskanone.x - bosskanone.width / 2, bosskanone.y - bosskanone.height / 2, bosskanone.width, bosskanone.height)
            if SHOWRECTS: pygame.draw.rect(screen, RED, bosskanoneRechteck, 2)
            for laser in laserAktiv:
                laserRechteck = pygame.Rect(laser.x - 3, laser.y - 3, 6, 6)

                if bosskanoneRechteck.colliderect(laserRechteck):
                    if bosskanone.kapazitaet > 0:
                        laser.zerstoeren()
                    else:
                        laser.aufloesen()
                    bosskanone.treffer()

    for meteor in meteorsAktiv:
        meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                     meteor.originalheight - 100 * meteor.scalefaktor)
        if SHOWRECTS: pygame.draw.rect(screen, RED, meteorRechteck, 2)
        if meteorRechteck.colliderect(heroRechteck1) or meteorRechteck.colliderect(heroRechteck2):
            game_hero.treffer()

    for enemy in enemyAktiv:
        if SCREEN_TOP < enemy.y < SCREEN_BOTTOM and SCREEN_LEFT < enemy.x < SCREEN_RIGHT:
            enemyRechteck = pygame.Rect(int(enemy.x - enemy.width / 2) + 4, int(enemy.y - enemy.height / 2) + 4,
                                        enemy.width - 8,
                                        enemy.height - 8)
            if SHOWRECTS: pygame.draw.rect(screen, RED, enemyRechteck, 2)
            for laser in laserAktiv:
                laserRechteck = pygame.Rect(laser.x - 3, laser.y - 3, 6, 6)

                if enemyRechteck.colliderect(laserRechteck):
                    if enemy.shieldon == 0:
                        laser.aufloesen()
                        enemy.zerstoeren(POINTS_YES)
                    else:
                        laser.zerstoeren()

            for meteor in meteorsAktiv:
                meteorRechteck = pygame.Rect(meteor.x - int(meteor.originalwidth / 2) + 50 * meteor.scalefaktor, meteor.y - int(meteor.originalheight / 2) + 50 * meteor.scalefaktor, meteor.originalwidth - 100 * meteor.scalefaktor,
                                             meteor.originalheight - 100 * meteor.scalefaktor)
                if enemyRechteck.colliderect(meteorRechteck):
                    enemy.zerstoeren(POINTS_NO)

            if enemyRechteck.colliderect(heroRechteck1) or enemyRechteck.colliderect(heroRechteck2):
                enemy.zerstoeren(POINTS_YES)
                game_hero.treffer()

    for kanone in kanonenAktiv:
        if SCREEN_TOP < kanone.y < SCREEN_BOTTOM:

            kanoneRechteck = pygame.Rect(kanone.x - 40, kanone.y - 40, 80, 80)
            if SHOWRECTS: pygame.draw.rect(screen, RED, kanoneRechteck, 2)
            for laser in laserAktiv:
                laserRechteck = pygame.Rect(int(laser.x - laser.width / 2) + 4, int(laser.y - laser.height / 2) + 4,
                                            laser.width - 8,
                                            laser.height - 8)

                if kanoneRechteck.colliderect(laserRechteck):
                    if kanone.kapazitaet > 0:
                        laser.zerstoeren()
                    else:
                        laser.aufloesen()
                    kanone.treffer()
            if kanoneRechteck.colliderect(heroRechteck1) or kanoneRechteck.colliderect(heroRechteck2):
                kanone.zerstoeren()
                game_hero.treffer()

    heroRechteck1 = pygame.Rect(game_hero.x - 50, game_hero.y, 102, 36)
    heroRechteck2 = pygame.Rect(game_hero.x - 10, game_hero.y - 30, 20, 60)
    for bonus in bonusAktiv:
        if bonus.y > SCREEN_TOP and bonus.y < SCREEN_BOTTOM:
            bonusRechteck = pygame.Rect(int(bonus.x - bonus.width / 2) + 2, int(bonus.y - bonus.height / 2) + 2,
                                        bonus.width - 4,
                                        bonus.height - 4)
            if bonusRechteck.colliderect(heroRechteck1) or bonusRechteck.colliderect(heroRechteck2):
                bonus.sammeln()


class LevelPanel():
    def __init__(self):
        global game
        self.x = 150
        self.y = 500
        self.image = levelImages[game.Level]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dcounter = 5
        self.alpha = 0
        self.zeigen = True

    def init(self, mode):
        global game
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
    global game

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
    if game.Gegnergetroffen > 8 - game.Level:
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

    if not game.Mode == LEVEL_ENDE:
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
        game_hero.update(True)
        game_hero.zeichnen()

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
    global game_hero

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
    game_hero.y = SCREEN_BOTTOM + 50

    level_panel.init(LEVEL_START)
    mixer.Sound("Sounds/Jetzt kann der Spaß anfangen.wav").play()
    playBackgroundSongs(game.Level)


def endLevel():
    global game, level_panel, game_backgroundmusic, game_hero

    level_panel.init(LEVEL_ENDE)
    mixer.Sound("Sounds/Atmen DV.wav").play()
    playBackgroundSongs(game.Level)


def gameover():
    global game, level_panel

    level_panel.init(GAME_OVER)
    mixer.Sound("Sounds/game_over.wav").play()
    # game_backgroundmusic.play(game.Level)


def moveoutHero():
    global game_hero, game, background

    if game_hero.y > SCREEN_TOP - 100:
        game_hero.y -= 15
        background.zeichnen()
        game_hero.update(False)
        game_hero.zeichnen()
        game_console.zeichnen()
    else:
        game.Level += 1
        if game.Level <= 4:
            startLevel()
        else:
            game.setzeMode(SPIEL_ENDE)


def moveinHero():
    global game_hero, game, background

    mousex, mousey = pygame.mouse.get_pos()
    if game_hero.y >= mousey:
        game_hero.x = mousex

        game_hero.y -= 6
        background.zeichnen()
        game_hero.update(False)
        game_hero.zeichnen()
        game_console.zeichnen()
    else:
        game.setzeMode(NORMAL_RUN)
        boss.initLevel()


game = Game()
background = ScrollingBackground()
game_hero = Hero()
game_console = GameConsole()

game_titel = Titel()
level_panel = LevelPanel()
pygame.mouse.set_visible(True)
boss = Boss()

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
            game_titel.ausblenden()
            startLevel()

        if event.type == MOUSEBUTTONUP:
            mousepressed = False
    pygame.event.pump()
    if game.Mode == START:
        # Zeige Titelbild mit Buttons
        game_titel.update()
        game_titel.zeichnen()
        mouseButton = pygame.mouse.get_pressed()
        if mouseButton[0]:
            if not mousepressed:
                mousepressed = True
                game_titel.checkselection()
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
            if game_hero.aktiv:  # Schüsse abgeben mit linker Maustaste
                if (now() - game.timeLastShot) > 1000 / game_hero.firepower:
                    createLasers()
                    game.timeLastShot = now()
        if mouseButton[2]:  # Zünde Megabombe mit rechter Maustaste
            if game_hero.has_megabomb():
                game_hero.zuendeMegabombe()
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
