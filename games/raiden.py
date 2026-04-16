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
