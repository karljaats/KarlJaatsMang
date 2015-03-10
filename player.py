from math import asin,sqrt,pi,radians,sin,cos
import pygame

#Mängija klass
class Player(pygame.sprite.Sprite):
    def __init__(self):
        #sprite klassi seadistamine
        super().__init__()
        self.angle = 0
        self.health = 100
        self.speed = 4
        
        self.originalImage = pygame.image.load("pildid/Player3.png").convert() #et iga frame pöörata algsset pilti
        self.image = self.originalImage
        #taust läbipaistvaks
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)

        self.rect = self.originalImage.get_rect() #pildi mõõtmed

    def draw(self, screen): #joonista mängija
        screen.blit(self.image, self.rect)

    def rotateAngle(self, mouseX, mouseY): #pildi pööramisnurga arvutamine
        x = self.rect.centerx - mouseX
        y = self.rect.centery - mouseY
        c = round(sqrt(x**2 + y**2))
        #radian to angle is radian * 180/pi
        #I veerand
        if x < 0 and y >= 0:
            x = x*(-1)
            self.angle = round(asin(x/c) * (180/pi) * (-1))
        #II veerand
        elif x <= 0 and y < 0:
            x = x*(-1)
            y = y*(-1)
            self.angle = round((90 + (asin(y/c) * (180/pi))) * (-1))
        #III veerand
        elif x >= 0 and y < 0:
            y = y*(-1)
            self.angle = round((180 + (asin(x/c) * (180/pi))) * (-1))
        #IV veerand
        elif x > 0 and y >= 0:
            self.angle = round((270 + (asin(y/c) * (180/pi))) * (-1))
            
    def rotateImage(self): #pildi enda pööramine jättes pildi keskkoha paika
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect(center=oldCenter)

#collisionite tegemiseks
class PlayerCollisionDummy(pygame.sprite.Sprite):
    def __init__(self, sprite):
        #sprite klassi seadistamine
        super().__init__()
        self.image = pygame.Surface([40, 40])#40X40 pilt
        self.rect = self.image.get_rect()
        self.rect.centerx = sprite.rect.centerx
        self.rect.centery = sprite.rect.centery
