from circleshape import CircleShape
import os
import pygame

class EngineFlame(CircleShape):
    frames = []
    FRAME_TIME = float('inf')  # Flame persists indefinitely

    def __init__(self, x, y):
        super().__init__(x, y, radius=0)
        
        if not EngineFlame.frames:
            path = os.path.join("assets", "images", "engine_flame.png")
            img = pygame.image.load(path).convert_alpha()
            # Directly scale the full image down — skip cropping
            small = pygame.transform.smoothscale(img, (55, 55))
            EngineFlame.frames.append(small)
        
        self.frame_index = 0
        self.timer = 0.0
        self.image = EngineFlame.frames[0]
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))

    def update(self, dt):
        # Update the timer and frame index (though with FRAME_TIME = inf, frame_index remains 0)
        self.timer += dt
        self.frame_index = int(self.timer / EngineFlame.FRAME_TIME)
        if self.frame_index >= len(EngineFlame.frames):
            self.kill()
        else:
            self.image = EngineFlame.frames[self.frame_index]
            self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))

    def draw(self, surface):
        if self.engine_flame:
            self.engine_flame.draw(surface)
    
        surface.blit(self.image, self.rect)
   
