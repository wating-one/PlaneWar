import pygame

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, speed=1):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
