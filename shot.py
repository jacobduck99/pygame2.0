import pygame
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        # Create a small circular sprite
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (33,115,255), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = (int(self.position.x), int(self.position.y))
