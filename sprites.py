# This file was created by: James Che
# This code was inspired by Zelda and informed by Chris Bradfield

import pygame as pg
from settings import *
from random import choice
from utils import *

# player sprite

mobcamo = False

spawnx = 0
spawny = 0
playerspeed = 0
portalhit = False

invincible = False


# player class with attributes
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        global spawnx, spawny, playerspeed
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        spawnx = self.x
        self.y = y * TILESIZE
        spawny = self.y
        self.moneybag = 0
        self.portals = 0
        self.speed = 300
        self.status = ''
        self.hitpoints = 100
        playerspeed = self.speed
    
    # key code to manipulate player
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed  
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False
            
    # wall collision code
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # made possible by Aayush's question!
    # collision code
    def collide_with_group(self, group, kill):
            global mobcamo
            global invincible
            global portalhit
            global playerspeed
            hits = pg.sprite.spritecollide(self, group, kill)
            # code for collisions
            if hits:
                # coin collisions
                if str(hits[0].__class__.__name__) == "Coin":
                    self.moneybag += 1
                # powerup collisions
                if str(hits[0].__class__.__name__) == "Powerup":
                    print(choice(POWER_UP_EFFECTS))
                    # Randomization
                    if(choice(POWER_UP_EFFECTS) == "Speed"):
                        # Speed powerup
                        if(self.speed >= 1500):
                            self.speed /= 2
                            playerspeed = self.speed
                        else:
                            self.speed *= 3.5
                            playerspeed = self.speed
                    elif(choice(POWER_UP_EFFECTS) == "Camo"):
                        # Camo Powerup
                        # self.game.cooldown.cd = 5
                        if mobcamo == True:
                            invincible = True
                        else:
                            mobcamo = True
                        self.image.fill(RED)
                        print("Camo")
                        # if self.game.cooldown.cd < 1:
                        #     mobcamo = False
                        #     self.image.fill(GREEN)
                    elif(choice(POWER_UP_EFFECTS) == "Invincible"):
                        # Invincibility Powerup
                        if invincible == True:
                            for a in self.game.mobs:
                                a.kill()
                             
                        # self.game.cooldown.cd = 5
                        self.image.fill(GOLD)
                        if self.speed <= 300:
                            self.speed = 300
                        print("Invincible")
                        invincible = True
                        # if self.game.cooldown.cd < 1:
                        #     mobcamo = False
                        #     self.image.fill(GREEN)
                if str(hits[0].__class__.__name__) == "Mob":
                    # Mob collision
                    if invincible == False:
                        # subtract hitpoints
                        self.hitpoints -= 30
                        self.x = spawnx
                        self.y = spawny
                        if(self.speed > 150):
                            self.speed -= 150
                        elif (self.speed <= 150):
                            self.speed -= 0
                    elif invincible == True:
                        pass

                    if mobcamo == True:
                        # Invincibility loophole
                        mobcamo = False
                        self.image.fill(GREEN)
                        if(invincible == True):
                            self.image.fill(GOLD)
                
                if str(hits[0].__class__.__name__) == "mirrorMob":
                    # Mirrormob collision code
                    self.hitpoints -= 30
                    self.x = spawnx
                    self.y = spawny

                if str(hits[0].__class__.__name__) == "Portal":
                    # Portal collision code
                    self.portals += 1

    
    # sprite updates
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collsion later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mobs, False)
        self.collide_with_group(self.game.mirrormobs, False)
        self.collide_with_group(self.game.portals, False)

        # Add coins to moneybag
        coin_hits = pg.sprite.spritecollide(self, self.game.coins, True)
        if coin_hits:
            self.moneybag += 1

# Wall code
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Coin code
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Spawn block code (Also false coin)
class spawnBlock(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Portal code
class Portal(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.portals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Powerup code
class Powerup(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# class Powerup1(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.power_ups
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image.fill(ORANGE)
#         self.rect = self.image.get_rect()
#         self.x = x
#         self.y = y
#         self.rect.x = x * TILESIZE
#         self.rect.y = y * TILESIZE

# Mob code from Mr. Cozort's code
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
    def collide_with_walls(self, dir):
         if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
         if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        if mobcamo == False:
            # self.rect.x += 1
            self.x += self.vx * self.game.dt
            self.y += self.vy * self.game.dt
            
            if self.rect.x < self.game.player1.rect.x:
                self.vx = 100
            if self.rect.x > self.game.player1.rect.x:
                self.vx = -100    
            if self.rect.y < self.game.player1.rect.y:
                self.vy = 100
            if self.rect.y > self.game.player1.rect.y:
                self.vy = -100
            self.rect.x = self.x
            self.collide_with_walls('x')
            self.rect.y = self.y
            self.collide_with_walls('y')
        elif mobcamo == True:
                # if self.game.cooldown.cd < 1:
                pass
                # if self.game.cooldown.cd < 1:
                #                 self.x += self.vx * self.game.dt
                # self.y += self.vy * self.game.dt
                
                # if self.rect.x < self.game.player1.rect.x:
                #     self.vx = 100
                # if self.rect.x > self.game.player1.rect.x:
                #     self.vx = -100    
                # if self.rect.y < self.game.player1.rect.y:
                #     self.vy = 100
                # if self.rect.y > self.game.player1.rect.y:
                #     self.vy = -100
                # self.rect.x = self.x
                # self.collide_with_walls('x')
                # self.rect.y = self.y
                # self.collide_with_walls('y')

# Mirror mob code
class mirrorMob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mirrormobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(CRIMSON)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = playerspeed
    def collide_with_walls(self, dir):
         if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
         if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # Added to mimick player motion
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -playerspeed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = playerspeed 
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -playerspeed 
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = playerspeed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # Update mirror mob
    def update(self):
            # self.get_keys()
            # self.rect.x += 1
            self.x += self.vx * self.game.dt
            self.y += self.vy * self.game.dt
            
            if self.rect.x < self.game.player1.rect.x:
                self.vx = playerspeed
            if self.rect.x > self.game.player1.rect.x:
                self.vx = -playerspeed    
            if self.rect.y < self.game.player1.rect.y:
                self.vy = playerspeed
            if self.rect.y > self.game.player1.rect.y:
                self.vy = -playerspeed
            
            self.get_keys()

            self.rect.x = self.x
            self.collide_with_walls('x')
            self.rect.y = self.y
            self.collide_with_walls('y')