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

SCORE_PER_KILL = 100


def check_collisions(player, bullets, enemies):
    """Returns (score_gained, game_over)."""
    score, hit_b, hit_e = 0, set(), set()
    for i, b in enumerate(bullets):
        for j, e in enumerate(enemies):
            if b.rect.colliderect(e.rect):
                hit_b.add(i); hit_e.add(j); score += SCORE_PER_KILL
    for i in sorted(hit_b, reverse=True): bullets.pop(i)
    for j in sorted(hit_e, reverse=True): enemies.pop(j)
    return score, any(e.rect.colliderect(player.rect) for e in enemies)


def draw_game_over(surface, score):
    """Draw the game over screen."""
    font_big = pygame.font.SysFont(None, 64)
    font_sm = pygame.font.SysFont(None, 32)
    surface.fill(BLACK)
    go = font_big.render("GAME OVER", True, RED)
    sc = font_sm.render(f"Score: {score}", True, WHITE)
    rs = font_sm.render("Press R to restart", True, YELLOW)
    cx = SCREEN_WIDTH // 2
    surface.blit(go, (cx - go.get_width() // 2, 240))
    surface.blit(sc, (cx - sc.get_width() // 2, 320))
    surface.blit(rs, (cx - rs.get_width() // 2, 380))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    player = Player()
    bullets = []
    enemies = []
    score = 0
    shoot_timer = 0
    spawn_timer = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_r:
                return main()

        if not game_over:
            keys = pygame.key.get_pressed()
            player.update()

            shoot_timer += 1
            if keys[pygame.K_SPACE] and shoot_timer >= SHOOT_COOLDOWN:
                bullets.append(player.shoot())
                shoot_timer = 0

            spawn_timer += 1
            if spawn_timer >= ENEMY_SPAWN_RATE:
                enemies.append(Enemy())
                spawn_timer = 0

            for b in bullets: b.update()
            for e in enemies: e.update()
            bullets[:] = [b for b in bullets if not b.off_screen()]
            enemies[:] = [e for e in enemies if not e.off_screen()]

            gained, game_over = check_collisions(player, bullets, enemies)
            score += gained

        if game_over:
            draw_game_over(screen, score)
        else:
            screen.fill(BLACK)
            player.draw(screen)
            for b in bullets: b.draw(screen)
            for e in enemies: e.draw(screen)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
