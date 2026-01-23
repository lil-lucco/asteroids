import pygame # type: ignore
from constants import *
from logger import log_state, log_event
from player import Player
from circleshape import CircleShape
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():

    print("Starting Asteroids with pygame version: " + pygame.version.ver)
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    font = pygame.font.Font(None, 36)
    game_over = False
    high_score_path = "high_score.txt"
    try:
        with open(high_score_path, "r", encoding="utf-8") as high_score_file:
            high_score = int(high_score_file.read().strip() or 0)
    except (FileNotFoundError, ValueError):
        high_score = 0

    Shot.containers = (shots, drawable, updatable)
    AsteroidField.containers = (updatable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)

    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), PLAYER_RADIUS)
    asteroidfield = AsteroidField()
    text_surface  = font.render(f"SCORE: {player.get_score()}", True, (255, 255, 255))
    
    def clear_group(group):
        for sprite in group.sprites():
            sprite.kill()

    while True:
        log_state()
        events = pygame.event.get()
        if game_over:
            log_event(f"game ended with score {player.get_score()}")
            for event in events:
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_y:
                        game_over = False
                        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        player.rotation = 0
                        player.cooldown = 0
                        player.score = 0
                        clear_group(shots)
                        clear_group(asteroids)
                        asteroidfield.spawn_timer = 0
            screen.fill("black")
            game_over_surface = font.render(f"YOU DIED. SCORE: {player.get_score()}", True, (255, 255, 255))
            high_score_surface = font.render(f"HIGH SCORE: {high_score}", True, (255, 255, 255))
            prompt_surface = font.render("Press Y to continue or ESC to exit", True, (255, 255, 255))
            game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 32))
            high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 0))
            prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 32))
            screen.blit(game_over_surface, game_over_rect)
            screen.blit(high_score_surface, high_score_rect)
            screen.blit(prompt_surface, prompt_rect)
            pygame.display.flip()
            dt = clock.tick(60) / 1000.0
            continue
        for event in events:
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player.pause_flip()
        if player.pause:
            log_event(f"game paused")
            screen.fill("black")
            paused__surface = font.render(f"PAUSED. CURRENT SCORE: {player.get_score()}", True, (255, 255, 255))
            prompt_surface = font.render("PRESS ESC TO CONTINUE", True, (255, 255, 255))
            paused_rect = paused__surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 24))
            prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 24))
            screen.blit(paused__surface, paused_rect)
            screen.blit(prompt_surface, prompt_rect)
            pygame.display.flip()
            dt = clock.tick(60) / 1000.0
            continue
        
        updatable.update(dt)
        
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    player.increase_score()
                    if player.get_score() > high_score:
                        high_score = player.get_score()
                        with open(high_score_path, "w", encoding="utf-8") as high_score_file:
                            high_score_file.write(str(high_score))

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                game_over = True
                break

        screen.fill("black")
        for item in drawable:
            item.draw(screen)
        text_surface  = font.render(f"SCORE: {player.get_score()}", True, (255, 255, 255))
        high_score_surface = font.render(f"HIGH SCORE: {high_score}", True, (255, 255, 255))
        screen.blit(text_surface, (0.1 * SCREEN_WIDTH, 0.9 * SCREEN_HEIGHT))
        screen.blit(high_score_surface, (0.1 * SCREEN_WIDTH, 0.9 * SCREEN_HEIGHT + 28))
        pygame.display.flip()
        dt = clock.tick(60) / 1000.0


if __name__ == "__main__":
    main()
