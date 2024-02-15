# This file was created by: James Che
# import libraries and modules
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path

# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
     # code to load text file containing game board
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        # 'r'     open for reading (default)
        # 'w'     open for writing, truncating the file first
        # 'x'     open for exclusive creation, failing if the file already exists
        # 'a'     open for writing, appending to the end of the file if it exists
        # 'b'     binary mode
        # 't'     text mode (default)
        # '+'     open a disk file for updating (reading and writing)
        # 'U'     universal newlines mode (deprecated)
        # below opens file for reading in text mode
        # with 
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    # Create run method which runs the whole GAME
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        # code to add walls and render player
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                # "1" character in map.txt creates a wall
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                # "p" caracter in map.txt defines the location of the player
                if tile == 'p':
                   self.player1 =  Player(self, col, row)

    def run(self):
        # function to run the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
    #function to quit the game
    def quit(self):
         pg.quit()
         sys.exit()

    # function to update the game
    def update(self):
        self.all_sprites.update()
    
    # function to draw the grid on the game
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    # function to draw sprites onto the game
    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            pg.display.flip()

    # function to handle detected events in the game
    def events(self):
        # code to handle quit event
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
        # code to handle key presses
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_a:
            #         self.player1.move(dx=-1)
            #     if event.key == pg.K_d:
            #         self.player1.move(dx=+1)
            #     if event.key == pg.K_w:
            #         self.player1.move(dy=-1)
            #     if event.key == pg.K_s:
            #         self.player1.move(dy=+1)
            #     if event.key == pg.K_LEFT:
            #         self.player1.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player1.move(dx=+1)
            #     if event.key == pg.K_UP:
            #         self.player1.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player1.move(dy=+1)

# Instantiate the game... 
g = Game()
# use game method run to run
# g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()