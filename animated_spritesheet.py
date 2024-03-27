# Import modules
import pygame as pg

# Define FPS
FPS = 30

# List of frames
frames = ["Frame 1", "Frame 2", "Frame 3", "Frame 4"]

# Create clock
clock = pg.time.Clock()

# Variables to store frame and time info
last_update = 0
current_frame = 0

# Animate function
def animate():
    global last_update
    global current_frame
    now = pg.time.get_ticks()
    if now - last_update > 350:
        current_frame = (current_frame + 1) % len(frames)
        print(frames[current_frame])
        print(now)
        last_update = now
    # print(now)

# While loop to run animate function
while True:
    clock.tick(FPS)
    animate()