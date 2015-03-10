from math import radians,sin,cos
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        #sprite klassi seadistamine
        super().__init__()
        self.speed = 10
        
        self.image = pygame.image.load("pildid/bullet.png").convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL) #taust läbipaistvaks
        #muutujad asukoha täpsemaks jälgimiseks(muidu ümardatakse see täisarvuks)
        self.x = 0
        self.y = 0
        
    def start(self, playerCenterX, playerCenterY): #tulistamisel väljakutsutav funktsioon, arvutab püssi asukoha
        vahe = 20 #pixleid playerCenter-ist
        if self.angle < 0:
            self.angle = -self.angle
        #I veerand
        if self.angle <= 90:
            self.rect.centerx = playerCenterX + sin(radians(self.angle))*vahe
            self.rect.centery = playerCenterY - cos(radians(self.angle))*vahe
        #II veerand
        elif self.angle <= 180:
            self.rect.centerx = playerCenterX + cos(radians(self.angle-90))*vahe
            self.rect.centery = playerCenterY + sin(radians(self.angle-90))*vahe
        #III veerand
        elif self.angle <= 270:
            self.rect.centerx = playerCenterX - sin(radians(self.angle-180))*vahe
            self.rect.centery = playerCenterY + cos(radians(self.angle-180))*vahe
        #IV veerand
        elif self.angle <= 360:
            self.rect.centerx = playerCenterX - cos(radians(self.angle-270))*vahe
            self.rect.centery = playerCenterY - sin(radians(self.angle-270))*vahe
        self.x = self.rect.x
        self.y = self.rect.y
        
    def update(self):
        #I veerand
        if self.angle <= 90:
            self.x += sin(radians(self.angle))*self.speed
            self.y -= cos(radians(self.angle))*self.speed
        #II veerand
        elif self.angle <= 180:
            self.x += cos(radians(self.angle-90))*self.speed
            self.y += sin(radians(self.angle-90))*self.speed
        #III veerand
        elif self.angle <= 270:
            self.x -= sin(radians(self.angle-180))*self.speed
            self.y += cos(radians(self.angle-180))*self.speed
        #IV veerand
        elif self.angle <= 360:
            self.x -= cos(radians(self.angle-270))*self.speed
            self.y -= sin(radians(self.angle-270))*self.speed
        self.rect.x = self.x
        self.rect.y = self.y
        
