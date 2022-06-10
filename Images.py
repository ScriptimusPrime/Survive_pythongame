import pygame
from pygame import image

laserImages = (image.load('Laser/beam2.png'), image.load('Laser/beaml.png'), image.load('Laser/beamr.png'), image.load('Laser/beamdl.png'), image.load('Laser/beamdr.png'))
gegnerImages = (image.load('Enemys/1n.png'), image.load('Enemys/2n.png'), image.load('Enemys/3n.png'), image.load('Enemys/4n.png'), image.load('Enemys/5n.png'), image.load('Enemys/6n.png'), image.load('Enemys/7n.png'), image.load('Enemys/8n.png'),
                image.load('Enemys/9n.png'), image.load('Enemys/1s.png'), image.load('Enemys/2s.png'), image.load('Enemys/3s.png'), image.load('Enemys/4s.png'), image.load('Enemys/5s.png'), image.load('Enemys/6s.png'), image.load('Enemys/7s.png'),
                image.load('Enemys/8s.png'), image.load('Enemys/9s.png'))
gegnerlaserImages = (image.load('Gegnerfeuer/1.png'), image.load('Gegnerfeuer/2.png'), image.load('Gegnerfeuer/3.png'),
                     image.load('Gegnerfeuer/4.png'), image.load('Gegnerfeuer/5.png'), image.load('Gegnerfeuer/20.png'),
                     image.load('Gegnerfeuer/boss1.png'), image.load('Gegnerfeuer/boss2.png'),
                     image.load('Gegnerfeuer/boss3.png'),
                     image.load('Gegnerfeuer/boss4.png') )
bonusImages = (image.load('Bonus/1.png'), image.load('Bonus/2.png'), image.load('Bonus/3.png'),
               image.load('Bonus/4.png'), image.load('Bonus/5.png'), image.load('Bonus/6.png'),
               image.load('Bonus/7.png'), image.load('Bonus/8.png'), image.load('Bonus/9.png'),
               image.load('Bonus/10.png'), image.load('Bonus/11.png'))
levelImages = (image.load('Sonstiges/Levelende.png'), image.load('Sonstiges/Level1.png'), image.load('Sonstiges/Level2.png'), image.load('Sonstiges/Level3.png'), image.load('Sonstiges/Level4.png'))
buttonImages = (image.load('Sonstiges/Button_up.png'), image.load('Sonstiges/Button_down.png'), image.load('Sonstiges/Button_start.png'), image.load('Sonstiges/Levelwahl1.png'), image.load('Sonstiges/Levelwahl2.png'),
                image.load('Sonstiges/Levelwahl3.png'), image.load('Sonstiges/Levelwahl4.png'))
schutzschildImages = (image.load('Schutzschild/0.png'), image.load('Schutzschild/1.png'), image.load('Schutzschild/2.png'), image.load('Schutzschild/3.png'), image.load('Schutzschild/4.png'))
mineImages = (image.load('Mine/1.png'), image.load('Mine/2.png'), image.load('Mine/3.png'), image.load('Mine/4.png'))
meteorImage = image.load('Meteor/meteor.png')
zahlImages = (image.load('Zahlen/0.png'), image.load('Zahlen/1.png'), image.load('Zahlen/2.png'), image.load('Zahlen/3.png'), image.load('Zahlen/4.png'), image.load('Zahlen/5.png'), image.load('Zahlen/6.png'), image.load('Zahlen/7.png'),
              image.load('Zahlen/8.png'), image.load('Zahlen/9.png'))
bossImages = (image.load('Boss/boss1.png'), image.load('Boss/boss2.png'), image.load('Boss/boss3.png'), image.load('Boss/boss4.png'))
Boss_Kanone_Image = [[image.load('Boss/1-1.png'), image.load('Boss/1-2.png'), image.load('Boss/1-3.png'), image.load('Boss/1-4.png'), image.load('Boss/1-5.png'), image.load('Boss/1-6.png')],
                     [image.load('Boss/2-1.png'), image.load('Boss/2-2.png'), image.load('Boss/2-3.png'), image.load('Boss/2-4.png'), image.load('Boss/2-5.png'), image.load('Boss/2-6.png')],
                     [image.load('Boss/3-1.png'), image.load('Boss/3-2.png'), image.load('Boss/3-3.png'), image.load('Boss/3-4.png'), image.load('Boss/3-5.png'), image.load('Boss/3-6.png')],
                     [image.load('Boss/4-1.png'), image.load('Boss/4-2.png'), image.load('Boss/4-3.png'), image.load('Boss/4-4.png'), image.load('Boss/4-5.png'), image.load('Boss/4-6.png')]]
