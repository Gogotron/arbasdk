"""
    Arbalet - ARduino-BAsed LEd Table
    Arbasim - Arbalet Simulator

    Simulate an Arbalet table

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
import pygame
import os
import logging
import threading
import time
from Grid import *

__all__ = ['Arbasim']

class Arbasim(threading.Thread):
    def __init__(self, arbalet_height, arbalet_width, sim_height, sim_width, rate=30, autorun=True):
        """
        Arbasim constructor: launches the simulation
        Simulate a "arbalet_width x arbalet_height px" table rendered in a "sim_width x sim_height" window
        :param arbalet_width: Number of pixels of Arbalet in width
        :param arbalet_height: Number of pixels of Arbalet in height
        :param sim_width:
        :param sim_height:
        :param rate: Refresh rate in Hertz
        :return:
        """
        threading.Thread.__init__(self)
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S')
        self.sim_state = "idle"
        self.running = True
        self.refresh_rate = rate

        # Current table model storing all pixels
        self.arbamodel = None
        self.lock_model = threading.Lock()

        self.sim_width = sim_width
        self.sim_height = sim_height
        self.arbalet_width = arbalet_width
        self.arbalet_height = arbalet_height
        self.grid = Grid(sim_width/arbalet_width, sim_height/arbalet_height, arbalet_width, arbalet_height, (40, 40, 40))

        # Init Pygame
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        logging.info("Pygame initialized")
        self.screen = pygame.display.set_mode((self.sim_width, self.sim_height), 0, 32)
        self.sim_state = "idle"
        self.font = pygame.font.SysFont('sans', 14)

        # Autorun
        if autorun:
            self.start()

    def close(self, reason='unknown'):
        self.sim_state = "exiting"
        logging.info("Simulator exiting, reason: "+reason)
        self.running = False

    def set_model(self, arbamodel):
        """
        Updates the current model of the simulator
        :param arbamodel:
        :return:
        """
        with self.lock_model:
            self.arbamodel = arbamodel
        self.sim_state = "running" if arbamodel!=None else "idle"

    def run(self):
        # Main Simulation loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close("User request")
                    break

            # Render background and title
            pygame.draw.rect(self.screen,(0, 0, 0), pygame.Rect(0, 0, self.sim_width+2, self.sim_height+2))
            pygame.display.set_caption("Arbasim [{}]".format(self.sim_state))


            # Render grid and pixels
            with self.lock_model:
                self.grid.render(self.screen, self.arbamodel)

            caption = "[{}] Caption...".format(self.sim_state)
            rendered_caption = self.font.render(caption, 1, (255, 255, 255))
            location_caption = pygame.Rect((10,10), (300,20))
            self.screen.blit(rendered_caption, location_caption)

            pygame.display.update()
            time.sleep(1./self.refresh_rate)
        pygame.quit()
