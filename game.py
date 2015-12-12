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
        self.fps = 30
        self.gameover = False

    # Draws the surface onto the display(s)
    def update_screen(self, surface):
        self.simDisplay.update(surface)
        self.ledDisplay.update(surface)

    # Gameloop update
    def update(self):
        screen = self.screen

        # Count ticks independently of time so the timings won't mess up if the CPU is slow (you don't HAVE to use this,
        # but I recommend it, since I had problems with this
        self.ticks += 1
        ticks = self.ticks

        # Example
        pixel = pygame.Surface((1, 1))
        pixel.fill(pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        screen.blit(pixel, (random.randint(0, 89), random.randint(0, 19)))

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

            # Keypresses on keyboard and joystick axis motions / button presses
            if event.player == PLAYER1:
                if event.type == PUSH:
                    # Joysticks
                    if event.button == UP:
                        pass
                    elif event.button == DOWN:
                        pass
                    elif event.button == RIGHT:
                        pass
                    elif event.button == LEFT:
                        pass

                    # Buttons
                    elif event.button == B1:
                        pass
                    elif event.button == B2:
                        pass
                    elif event.button == B3:
                        pass
                # Same stuff here
                elif event.type == RELEASE:
                    pass

            # Same stuff here
            elif event.player == PLAYER2:
                pass

            # Player buttons
            elif event.button == P1:
                pass
            elif event.button == P2:
                pass


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
