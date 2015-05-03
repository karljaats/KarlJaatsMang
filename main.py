#Autor: Karl Jääts
import pygame,os
from bullet import *
from mapObjects import *
from player import *
from enemy import *

pygame.init()

#window suurus
width = 1000
heigth = 650
screen = pygame.display.set_mode((width, heigth))
pygame.display.set_caption("zombie shooter 2000")

#Mängu funktsioon
def game(width, heigth, screen):
    global done
    Clock = pygame.time.Clock() #aja ja fps-i mõõtmiseks/piiramiseks

    font = pygame.font.SysFont("Calibri", 30)

    """
    Map:
    1 märk on 50X50 ruut

    # on sein
    . on põrand
    S on spawner
    P on player
    """
    map_list = [
    ("#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"),
    ("#","S",".","#",".",".",".",".",".",".",".",".",".","#",".",".",".",".","S","#"),
    ("#",".",".","#",".",".",".",".",".",".",".",".",".","#",".",".",".",".",".","#"),
    ("#",".",".",".",".",".","#","#","#","#","#",".",".","#",".",".","#",".",".","#"),    
    ("#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#",".",".","#"),
    ("#",".",".","#",".",".",".",".",".",".",".",".",".",".",".",".","#",".",".","#"),
    ("#",".",".","#","#",".","#",".",".","#","#","#",".","#",".",".","#",".",".","#"),
    ("#",".",".",".",".",".",".",".",".",".","P",".",".",".",".",".",".",".",".","#"),
    ("#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"),
    ("#",".",".","#",".",".","#","#","#","#","#","#",".",".","#","#","#",".",".","#"),
    ("#",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#"),
    ("#","S",".","#",".",".",".",".",".",".",".",".",".",".","#",".",".",".","S","#"),
    ("#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"),]

    screen.fill((30, 200, 35))

    #Sprite gruppid
    wall_list = pygame.sprite.Group()
    spawner_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()

    player = Player() #player klassi väljakutsumine
    
    #Määrab ära seinte/spawnerite/mängija algse asukoha
    #seinte/spawnerite klasside väljakutsumine ja gruppidesse panemine
    for y in range(len(map_list)):
        for x in range(len(map_list[y])):
            if map_list[y][x] == "#":
                wall = Wall()
                wall.rect.x = x*50
                wall.rect.y = y*50
                wall_list.add(wall)
            elif map_list[y][x] == "S":
                spawner = Spawner()
                spawner.rect.x = x*50
                spawner.rect.y = y*50
                spawner_list.add(spawner)
            elif map_list[y][x] == "P":
                player.rect.x, player.rect.y = x*50, y*50

    #algsed muutujad
    dright = 0
    dleft = 0
    dup = 0
    ddown = 0
    kills = 0
    healthback = pygame.image.load("pildid/healthback.png").convert()
    killsback = pygame.image.load("pildid/killsback.png").convert()
    texthealth = font.render("Health: " + str(player.health), True, (0, 0, 0))
    textkills = font.render("Kills: " + str(kills), True, (0, 0, 0))

    gameover = False
    pygame.time.set_timer(pygame.USEREVENT, 2500) #event mis käivitub iga 4 sekundi tagant
    while not gameover and not done: #main loop
        for event in pygame.event.get():
            #mängu errorita lõpetamiseks
            if event.type == pygame.QUIT:
                done = True
                gameover = True
            #dleft/dright/dup/ddown on mängija liigutamise muutujad
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    dleft = -player.speed
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    dright = player.speed
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    dup = -player.speed
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    ddown = player.speed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    dleft = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    dright = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    dup = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    ddown = 0
            #klikk tekitab uue kuuli objekti
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet()
                bullet.angle = player.angle
                bullet.start(player.rect.centerx, player.rect.centery)
                bullet_list.add(bullet)
            #iga 4 sekundi tagant tekib igast spawnerist vaenlane
            elif event.type == pygame.USEREVENT:
                if len(enemy_list) < 60:
                    for spawner in spawner_list:
                        enemy = Enemy(spawner.rect.x+5, spawner.rect.y+5)
                        enemy_list.add(enemy)
                        
        #liigutamine
        collisionPlayer = PlayerCollisionDummy(player) #uus klass, sest pildi keeramine muudab selle mõõtmeid ja nii on lihtne seinadesse kinni jääda
        #iga suuna kohta eraldi muudetakse mängija collision klassi asukohta,
        #kontrollitakse seintega kattuvust
        #kui kattuvus puudub muudetakse päris mängija asukohta
        if dleft != 0:
            collisionPlayer.rect.x += dleft
            if pygame.sprite.spritecollide(collisionPlayer, wall_list, False) == []:
                player.rect.x += dleft
            else:
                collisionPlayer.rect.x -= dleft
        if dright != 0:
            collisionPlayer.rect.x += dright
            if pygame.sprite.spritecollide(collisionPlayer, wall_list, False) == []:
                player.rect.x += dright
            else:
                collisionPlayer.rect.x -= dright
        if ddown != 0:
            collisionPlayer.rect.y += ddown
            if pygame.sprite.spritecollide(collisionPlayer, wall_list, False) == []:
                player.rect.y += ddown
            else:
                collisionPlayer.rect.x -= ddown
        if dup != 0:
            collisionPlayer.rect.y += dup
            if pygame.sprite.spritecollide(collisionPlayer, wall_list, False) == []:
                player.rect.y += dup
            else:
                collisionPlayer.rect.y -= dup

        mouseX, mouseY = pygame.mouse.get_pos() #hiire asukoht

        #pildi pööramise nurga arvutamine
        player.rotateAngle(mouseX, mouseY)
        #pildi pööramine
        player.rotateImage()

        screen.fill((30, 200, 35))
        #kuulide asukoha muutmine
        bullet_list.update()
        
        collisionPlayer = PlayerCollisionDummy(player) # uus collision klass
        #vaenlaste update
        for enemy in enemy_list:
            enemy.rotateAngle(player)#pöörab mängija poole
            enemy.update(wall_list)#liigub, kontrollides seinu
            colenemy_list = pygame.sprite.Group()#grupp lihtsaks collision kontrolliks
            collisionEnemy = CollisionDummy(enemy)#klass collisionite kontrolliks
            #kui kuul tabab vaenlast kustutatakse mõlemad
            if pygame.sprite.spritecollide(collisionEnemy, bullet_list, True) != []:
                enemy.kill()
                #kill count update
                kills += 1
                textkills = font.render("Kills: " + str(kills), True, (0, 0, 0))
            else:
                colenemy_list.add(collisionEnemy)#gruppi lisamine. Alati on grupis ainult üks liige
            #kui vaenlane jõuab mängijani
            if pygame.sprite.spritecollide(collisionPlayer, colenemy_list, False) !=[]:
                enemy.kill()
                #health update
                player.health -= 20
                texthealth = font.render("Health: " + str(player.health), True, (0, 0, 0))

        #kustutab seinu tabanud kuulid
        for wall in wall_list:
            pygame.sprite.spritecollide(wall, bullet_list, True)

        if player.health <= 0:
            gameover = True
        
        #joonistab kõik asjad ekraanile
        spawner_list.draw(screen)
        bullet_list.draw(screen)
        player.draw(screen)
        enemy_list.draw(screen)
        wall_list.draw(screen)
        
        Clock.tick(60)#mõõdab fps-i ja piirab selle 60-le

        #nubrid ekraanile
        textfps = font.render(str(round(Clock.get_fps())), True, (0, 0, 0))
        screen.blit(textfps, (5, heigth-35))
        screen.blit(healthback, (0, 0))
        screen.blit(texthealth, (5, 5))
        screen.blit(killsback, (width-120, 0))
        screen.blit(textkills, (width-110, 5))

        pygame.display.flip()

def instructions(screen):
    global done
    font = pygame.font.SysFont("Calibri", 24)
    texts = ["The aim of the game is to kill as many baddies as you can before you die.",
             "",
             "You can move around using WASD or the arrow keys.",
             "Click to shoot and when you die you can restart by pressing SPACE.",
             "",
             "",
             "Press any key to continue..."]
    screen.fill((0, 0, 0))
    index = 0
    for text in texts:
        text = font.render(text, True, (255, 255, 255))
        screen.blit(text, (10, index*20+60))
        index += 1
    
    pressed = False
    while not done and not pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                pressed = True
                
        pygame.display.flip()

#tegelik mängu väljakutsumine
done = False
gameoverfont = pygame.font.SysFont("Calibri", 60)
textgameover = gameoverfont.render("You died...", True, (0, 0, 0))
deadback = pygame.image.load("pildid/deadback.png").convert()
instructions(screen)
game(width, heigth, screen)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #tühikut vajutades hakkab mäng otsast peale
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game(width, heigth, screen)
    if not done: #et kui veel elus olles pannakse mäng kinni, ei kuvataks enne sulgumist surma teadet
        screen.blit(deadback, (width/2-135, heigth/2-45))
        screen.blit(textgameover, (width/2-120, heigth/2-30))
    pygame.display.flip()
        
pygame.quit()
