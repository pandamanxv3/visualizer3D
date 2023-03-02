from .camera import *
from pygame.locals import *
import os
from OpenGL.GL import *
from OpenGL.GLU import *

import tkinter as tk
from tkinter import filedialog

# Créez une fenêtre Tkinter
class PyOGLapp():
    def __init__(self, screen_posX, screen_posY, window_width, window_height):
        print(screen_posX, screen_posY)
        # self.screen_width = screen_width
        # self.screen_height = screen_height
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (screen_posX, screen_posY) #Cette ligne de code utilise la variable d'environnement 'SDL_VIDEO_WINDOW_POS' pour définir la position de la fenêtre sur l'écran. Les paramètres screen_width et screen_height définissent la largeur et la hauteur de la fenêtre, respectivement.
        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        self.screen_width = screen_width
        self.screen_height = screen_height
        print("Taille de l'écran : ", screen_width, "x", screen_height)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)#MAGIE NOIR ANTI ALIASING
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)#MAGIE NOIR ANTI ALIASING
        #pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 32) #si ya des petit triangles qui apparaisse partt(surtout sur mac)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)#MAGIE NOIR ANTI ALIASING

        screen = pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption('OpenGL in Python')
        self.camera = None
        self.program_id = None

    def initialise(self):
        pass
        
    def display(self):
        pass
    
    def camera_init(self):
        pass

    def mainloop(self):
        
        done = False
        self.initialise()
        pygame.event.set_grab(True) #appuye sur la souris comme ca elle reste sur la fenetre
        pygame.mouse.set_visible(False) #enleve la visu de la souris
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: #comme on voit plus la souris on echap ac escap
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)
                    if event.key == K_SPACE:
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True) 
            self.camera_init()
            self.display()
            pygame.display.flip()
            # pygame.time.wait(60)
        pygame.quit()


