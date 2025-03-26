import sys
import pygame 
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import os
from explosion import Explosion
from engine_flame import EngineFlame



def main():

    pygame.init()
    pygame.font.init()

    score = 0
    score_increment = 10

    lives = 5

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    background_image = pygame.image.load('assets/images/tesla_bg.jpg').convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    hits = pygame.sprite.groupcollide(shots, asteroids, True, False)


    EngineFlame.containers = (drawable, updatable)
    Explosion.containers = (drawable, updatable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    running = True
    while running:
        font = pygame.font.Font(None, 36)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q and not player.alive:
                running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not player.alive:
                main()
                return

        if player.alive:
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    Explosion(asteroid.position.x, asteroid.position.y)
                    lives -= 1
                    asteroid.kill()
                    if lives == 0:
                        print("Game over!")
                        player.alive = False
                        break

        screen.blit(background_image, (0, 0))

        drawable.draw(screen)

        screen.blit(player.image, player.rect)

        if not player.alive:
            gameover = font.render("Press R to Respawn \n or Q to Quit", False, (255, 255, 255))
            rect = gameover.get_rect()
            rect.center = screen.get_rect().center
            screen.blit(gameover, rect)

        
        for shot in shots.copy():
            hit_asteroids = pygame.sprite.spritecollide(
            shot,
            asteroids,
            False,
            pygame.sprite.collide_circle
        )

            for asteroid in hit_asteroids:
                Explosion(asteroid.position.x, asteroid.position.y)
                score += score_increment
                shot.kill()
                asteroid.kill()
                asteroid.split()
                break

        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        lives_text = font.render(f'Lives: {lives}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
