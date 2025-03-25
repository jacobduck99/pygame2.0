import pygame
import os
from circleshape import CircleShape

class Explosion(CircleShape):
    frames = []
    FRAME_TIME = 0.6

    def __init__(self, x, y):
        super().__init__(x, y, radius=0)

        if not Explosion.frames:
            path = os.path.join("assets", "images", "explosion.png")
            img = pygame.image.load(path).convert_alpha()
            # Directly scale the full image down — skip cropping
            small = pygame.transform.smoothscale(img, (64, 64))
            Explosion.frames.append(small)

        self.frame_index = 0
        self.timer = 0.0
        self.image = Explosion.frames[0]
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))

    def update(self, dt):
        self.timer += dt
        if self.timer >= Explosion.FRAME_TIME:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
