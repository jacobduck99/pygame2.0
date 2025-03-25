import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.movement_timer = 0
        self.boost_active = False
        self.boost_timer = 0
        self.boost_cooldown = 0

        # Create a transparent square exactly big enough for the ship
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        # Movement + rotation

        self.shoot_timer = max(0, self.shoot_timer - dt)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]: self.move(dt)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: self.move(-dt)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.rotate(-dt)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.rotate(dt)
        if keys[pygame.K_SPACE]: self.shoot()

        keys = pygame.key.get_pressed()
        if not (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.movement_timer = 0


        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)


        # Draw triangle into image using local coords
        self.image.fill((0,0,0,0))
        # Convert world points to surface-local
        center = pygame.Vector2(self.radius, self.radius)
        points = [(p - self.position) + center for p in self.triangle()]
        pygame.draw.polygon(self.image, (255,255,255), points)

        # Sync rect for group.draw
        self.rect.center = (int(self.position.x), int(self.position.y))

    def shoot(self):
        if self.shoot_timer > 0: return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt


    def wrap_position(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT


    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
    # Always accumulate dt when moving
        self.movement_timer += dt

        if self.boost_active:
            self.boost_timer += dt
            self.position += forward * PLAYER_EXTRA_SPEED * dt

            if self.boost_timer >= BOOST_DURATION:
                self.boost_active = False
                self.boost_timer = 0
                self.boost_cooldown = 3
                self.movement_timer = 0
        else:
            if self.boost_cooldown > 0:
                self.boost_cooldown -= dt
                self.position += forward * PLAYER_SPEED * dt
            else:
            # Not boosting and no cooldown: check if it's time to boost
                if self.movement_timer >= 2:
                    self.boost_active = True        # Trigger boost
                    self.position += forward * PLAYER_EXTRA_SPEED * dt
                else:
                    self.position += forward * PLAYER_SPEED * dt