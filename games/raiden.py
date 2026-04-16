"""Raiden - A vertical scrolling shoot-em-up game."""

import pygame
import sys
import random
import math

# Display
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60
TITLE = "Raiden"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player
PLAYER_SPEED = 5
PLAYER_LIVES = 3
BULLET_SPEED = 8

# Enemies
ENEMY_SPEED = 2
ENEMY_SPAWN_RATE = 45

PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
ENEMY_WIDTH = 28
ENEMY_HEIGHT = 28
BULLET_WIDTH = 4
BULLET_HEIGHT = 10
SHOOT_COOLDOWN = 15


class Player:
    """Player ship controlled by keyboard."""

    def __init__(self):
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2,
            SCREEN_HEIGHT - 80,
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
        )
        self.lives = PLAYER_LIVES

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PLAYER_SPEED

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)
        # Draw a small cockpit triangle
        cx = self.rect.centerx
        points = [
            (cx, self.rect.top - 4),
            (self.rect.left + 4, self.rect.top + 8),
            (self.rect.right - 4, self.rect.top + 8),
        ]
        pygame.draw.polygon(surface, YELLOW, points)

    def shoot(self):
        """Create a bullet at the player's position."""
        return Bullet(self.rect.centerx, self.rect.top)


class Bullet:
    """Bullet that moves upward."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(
            x - BULLET_WIDTH // 2, y, BULLET_WIDTH, BULLET_HEIGHT
        )

    def update(self):
        self.rect.y -= BULLET_SPEED

    def off_screen(self):
        return self.rect.bottom < 0

    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, self.rect)


class Enemy:
    """Enemy ship that spawns at top and moves downward."""

    def __init__(self):
        x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        self.rect = pygame.Rect(x, -ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.speed = ENEMY_SPEED + random.uniform(0, 1.5)

    def update(self):
        self.rect.y += self.speed

    def off_screen(self):
        return self.rect.top > SCREEN_HEIGHT

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)
        # Draw an X marking on the enemy
        pygame.draw.line(surface, WHITE, self.rect.topleft, self.rect.bottomright, 2)
        pygame.draw.line(surface, WHITE, self.rect.topright, self.rect.bottomleft, 2)
