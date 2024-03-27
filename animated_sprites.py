# Import modules
import time
import pygame as pg

# List of frames
frames = ["Frame 1", "Frame 2", "Frame 3", "Frame 4"]

last_update = 0

# While loop to run forever
while True:
    now  = pg.time.get_ticks()
    if now - last_update > 350:
        last_update = now
        print(now)
    print(now)
    # For loop that loops per item in frames list
    for i in frames:
        # Pause for 1 second
        # time.sleep(1)
        # Print frames list iteration
        print(i)