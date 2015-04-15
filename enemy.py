import pygame
from player import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() #sprite klasssi seadistamine
        self.originalImage = pygame.image.load("pildid/Enemy.png").convert() #algse pildi keeramiseks
        self.image = self.originalImage
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)#taust läbipaistev
        self.rect = self.originalImage.get_rect()
        self.angle = 0
        self.speed = 2
        #mittetäisarvuliseks asukoha säilitamiseks
        self.x = x
        self.y = y

    #kutsuda välja enne update'i, iga frame
    def rotateAngle(self, player):#nurga arvutamine ja pildi enda pööramine
        x = self.rect.centerx - player.rect.centerx
        y = self.rect.centery - player.rect.centery
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

        #pildi pööramine keskkoha ümber
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect(center=oldCenter)
        
    def update(self, wall_list):#update - vaenlaste liikumine ja seinte kontroll
        collisionEnemy = CollisionDummy(self)#klass collisioni hõlbustamiseks
        if self.angle < 0:
            self.angle = -self.angle
        #arvutab vajaliku kauguse, mis sel framil liikuda x ja y suunas
        #muudab collision klassi asukohta ja kontrollib seintega kattuvust
        #kui kattuvus puudub muudab päris klassi asukohta
        #I veerand
        if self.angle <= 90:
            muut = sin(radians(self.angle))*self.speed
            collisionEnemy.rect.x += muut+self.x%1
            if pygame.sprite.spritecollide(collisionEnemy, wall_list, False) == []:
                self.x += muut
            else:
                collisionEnemy.rect.x -= muut+self.x%1
                
            muut = cos(radians(self.angle))*self.speed
            collisionEnemy.rect.y -= muut+self.y%1
            if pygame.sprite.spritecollide(collisionEnemy, wall_list, False) == []:
                self.y -= muut
            else:
                collisionEnemy.rect.y += muut+self.y%1
        #II veerand
        elif self.angle <= 180:
            muut = cos(radians(self.angle-90))*self.speed
            collisionEnemy.rect.x += muut+self.x%1
            if pygame.sprite.spritecollide(collisionEnemy, wall_list, False) == []:
                self.x += muut
            else:
                collisionEnemy.rect.x -= muut+self.x%1

            muut = sin(radians(self.angle-90))*self.speed
            collisionEnemy.rect.y += muut+self.y%1
            if pygame.sprite.spritecollide(collisionEnemy, wall_list, False) == []:
                self.y += muut
            else:
                collisionEnemy.rect.y -= muut+self.y%1
        #III veerand
        elif self.angle <= 270:
            muut = sin(radians(self.angle-180))*self.speed
            collisionEnemy.rect.x -= muut+self.x%1
            if pygame.sprite.spritecollide(collisionEnemy, wall_list, False) == []:
                self.x -= muut
            else:
                collisionEnemy.rect.x += muut+self.x%1
                
            muut = cos(radians(self.angle-180))*self.speed
            collisionEnemy.rect.y += muut+self.y%1
            if pygame.sprite.spritecollide(collisionEnemy, wall_list, False) == []:
                self.y += muut
            else:
                collisionEnemy.rect.y -= muut+self.y%1
        #IV veerand
        elif self.angle <= 360:
            muut = cos(radians(self.angle-270))*self.speed
            collisionEnemy.rect.x -= muut+self.x%1
            if pygame.sprite.spritecollide(collisionEnemy, wall_list, False) == []:
                self.x -= muut
            else:
                collisionEnemy.rect.x += muut+self.x%1

            muut = sin(radians(self.angle-270))*self.speed
            collisionEnemy.rect.y -= muut+self.y%1
            if pygame.sprite.spritecollide(collisionEnemy, wall_list, False) == []:
                self.y -= muut
            else:
                collisionEnemy.rect.y += muut+self.y%1
        self.rect.x = self.x
        self.rect.y = self.y
        
class CollisionDummy(pygame.sprite.Sprite):#klass collisioni hõlbustamiseks
    image = pygame.Surface([40, 40])
    rect = image.get_rect()
    def __init__(self, sprite):
        super().__init__()
        CollisionDummy.rect.x = sprite.x
        CollisionDummy.rect.y = sprite.y
