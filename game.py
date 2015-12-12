#!/usr/bin/python
__author__ = 'Jannes Hoeke'

import led
import sys
from Colors import *
from led.PixelEventHandler import *
import random

""" https://github.com/HackerspaceBremen/pixels_basegame
    depends on https://github.com/HackerspaceBremen/pygame-ledpixels
"""

class Basegame:

    def __init__(self):

        self.clock = pygame.time.Clock()
        pygame.joystick.init()

        # Initialize first joystick
        if pygame.joystick.get_count() > 0:
            stick = pygame.joystick.Joystick(0)
            stick.init()

        fallback_size = (90, 20)

        self.ledDisplay = led.dsclient.DisplayServerClientDisplay('localhost', 8123, fallback_size)

        pygame.font.init()
        self.font_text = pygame.font.SysFont(None, 18)

        # use same size for sim and real LED panel
        size = self.ledDisplay.size()
        self.simDisplay = led.sim.SimDisplay(size)
        self.screen = pygame.Surface(size)

        self.ticks = 0
        self.fps = 10
        self.gameover = False

        self.sprites = []


    # Draws the surface onto the display(s)
    def update_screen(self, surface):
        self.simDisplay.update(surface)
        self.ledDisplay.update(surface)

    # Gameloop update
    def update(self):
        screen = self.screen

        # Count ticks independently of time so the timings won't mess up if the
        # CPU is slow (you don't HAVE to use this,
        # but I recommend it, since I had problems with this
        self.ticks += 1
        ticks = self.ticks

        self.screen.fill(pygame.Color(0, 0, 0))

        # generate new layer
        if ticks % 3 is 0:
            newsprites = []
            for x in range(screen.get_width()):
                new = pygame.Surface((1, 10))
                h = random.randint(0, 30)
                s = random.randint(80, 100)
                v = random.randint(30, 50)
                c = pygame.Color(0)
                c.hsva = (h, s, v, 1)
                new.fill(c)
                newsprites.append([new, [x, 21], c])  # [sprite, [x, y], color]
                pass # generate new fire
            if len(self.sprites) > random.randint(8, 12):
                self.sprites.pop(0)
            self.sprites.append(newsprites)

        for sprites in self.sprites:
            for sprite in sprites:
                # decrease size
                new_size = sprite[0].get_height() - random.randint(0, 2)
                if new_size < 0:
                    sprites.remove(sprite)
                    continue
                # move sprite upwards
                sprite[1][1] -= random.randint(0, 3)
                sprite[0] = pygame.Surface((1, new_size))
                sprite[0].fill(sprite[2])
                screen.blit(sprite[0], sprite[1])

        # Print fps
        if ticks % self.fps == 0:
            print self.clock.get_fps()
            
    # Process event queue
    def process_event_queue(self):
    
        for pgevent in pygame.event.get():
            if pgevent.type == QUIT:
                pygame.quit()
                sys.exit()

            event = process_event(pgevent)

            # End the game
            if event.button == EXIT:
                self.gameover = True

    def main(self):

        screen = self.screen

        # Show loading message
        font_text = self.font_text

        write_lobby = font_text.render("Basegame", True, WHITE)

        screen.fill(BLACK)
        screen.blit(write_lobby, (2, 4))

        self.update_screen(screen)

        # Clear event list before starting the game
        pygame.event.clear()

        # Start of the gameloop
        while not self.gameover:

            # Check controls
            self.process_event_queue()

            # Call update method
            self.update()

            # Send screen to display
            self.update_screen(screen)

            # Tick the clock and pass the maximum fps
            self.clock.tick(self.fps)

        # End of the game
        write_gameover = font_text.render("GAME OVER", True, WHITE)

        screen.fill(BLACK)
        screen.blit(write_gameover, (10, 4))

        self.update_screen(screen)

        # Wait for keypress
        while True:
            event = process_event(pygame.event.wait())
            if event.type == PUSH:
                break

        # Show score
        screen.fill(BLACK)
        text_gameover = "Score: " + str(int(0))
        write_gameover = font_text.render(text_gameover, True, WHITE)

        screen.blit(write_gameover, (2, 4))

        self.update_screen(screen)

        # Wait for keypress
        while True:
            event = process_event(pygame.event.wait())
            if event.type == PUSH:
                break

        pygame.quit()
    
game = Basegame()
game.main()
