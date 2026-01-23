from constants import *
import pygame # type:ignore
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
        self.radius = PLAYER_RADIUS
        self.rotation = 0
        self.cooldown = 0
        self.score = 0
        self.pause = False
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-1 * dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-1 * dt)
        if keys[pygame.K_SPACE]:
            if self.cooldown > 0:
                pass
            else:
                self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
                self.shoot()
        if self.cooldown > 0:
            self.cooldown -= dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)  
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        new_position = self.position + rotated_with_speed_vector
        new_position.x = max(self.radius, min(SCREEN_WIDTH - self.radius, new_position.x))
        new_position.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, new_position.y))
        self.position = new_position        
    
    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity *= PLAYER_SHOT_SPEED

    def increase_score(self):
        self.score +=  1

    def get_score(self):
        return self.score
    
    def pause_flip(self):
        if self.pause:
            self.pause = False
        else:
            self.pause = True
