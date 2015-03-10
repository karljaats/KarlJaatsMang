import pygame
class Wall(pygame.sprite.Sprite):#seina klass
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pildid/wall.png").convert()
        self.rect = self.image.get_rect()

class Spawner(pygame.sprite.Sprite):#spawner klass
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pildid/spawner.png").convert()
        self.rect = self.image.get_rect()
