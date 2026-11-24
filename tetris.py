
"""
TETRIS - Offline Game (Python + Pygame)
=======================================

Bilkul offline chalta hai - koi internet nahi chahiye.

Run:
    pip install pygame
    python tetris.py

Controls:
    Arrow Left / Right -> Move block
    Arrow Up           -> Rotate
    Arrow Down         -> Soft drop (fast fall)
    Space              -> Hard drop (instant)
    P                  -> Pause
    R                  -> Restart
    ESC                -> Quit
"""

import random
import sys
import pygame

# ---------------- Constants ----------------

CELL = 30
GRID_W = 10
GRID_H = 20

BOARD_W = GRID_W * CELL
BOARD_H = GRID_H * CELL

SIDE_W = 220

SCREEN_W = BOARD_W + SIDE_W
SCREEN_H = BOARD_H

FPS = 60

# ---------------- Colors ----------------

C_BG = (18, 18, 28)
C_BOARD_BG = (8, 8, 14)

C_GRID = (28, 28, 42)

C_TEXT = (235, 235, 245)
C_DIM = (140, 140, 160)

C_ACCENT = (0, 210, 255)

C_GOLD = (255, 205, 60)
C_GREEN = (80, 220, 120)
C_RED = (255, 90, 90)