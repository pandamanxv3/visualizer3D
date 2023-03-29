from .camera import *
from .Utils import *
from pygame.locals import *
import os

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

import tkinter as tk
from tkinter import filedialog



# Créez une fenêtre Tkinter
class PyOGLapp():
    def __init__(self, screen_posX, screen_posY, window_width, window_height):
        print(screen_posX, screen_posY)

        # Obtenir le chemin absolu du répertoire du script Python
        script_dir = os.path.dirname(__file__)
        print(script_dir, "wwwwwwwwwwwwwwwwwwww")
    # Charger l'image à partir d'un chemin relatif
        self.background2 = pygame.image.load(os.path.join(script_dir, '../background/blur-background.jpg'))
        self.background_surface = pygame.transform.scale(self.background2, (window_width, window_height))
        # background1 = pygame.image.load("Engine_Visualizer/glapp/background/dark_background.jpg")
        # background2 = pygame.image.load(os.path.join(script_dir,"background/pale_background.jpg"))
        # background3 = pygame.image.load(os.path.join(script_dir,"background/white_background.jpg"))

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
        # shader = create_program(vertex_source,shader_source)
        self.screen = pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)
        formatedBG = pygame.Surface((window_width, window_height))
        formatedBG.fill(pygame.color.Color(255, 0, 0, 0))
        pygame.display.set_caption('OpenGL in Python')
      
        pygame.display.flip()
        self.camera = None
        self.program_id = None

    def initialise(self):
        pass
        
    def display(self):
        pass
    
    def camera_init(self):
        pass

    def compile_shader2(shader_source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, shader_source)
        glCompileShader(shader)

        if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
            raise Exception("Erreur de compilation du shader: " + glGetShaderInfoLog(shader).decode())

        return shader


    def link_program(vertex_shader, fragment_shader):
        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)

        if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
            raise Exception("Erreur de liaison du programme: " + glGetProgramInfoLog(program).decode())

        return program


    def mainloop(self):
        screen_width = 1280
        screen_height = 720
        self.initialise()

        vertex_shader_source = r'''
        #version 330 core

        layout(location = 0) in vec3 a_position;

        void main() {
            gl_Position = vec4(a_position, 0.0f);
        }
        '''

        fragment_shader_source = r'''
        #version 330 core

        uniform vec2 u_resolution;
        uniform float u_time;

        out vec4 frag_color;

        void main() {
            vec2 coord = -5.0 * gl_FragCoord.xy / u_resolution - 4.2;

            for (int n = 1; n < 12; n++) {
                float i = float(n);
                coord += vec2(0.7 / i * sin(i * coord.y + u_time + 0.3) + 0.8, 0.4 / i * sin(coord.x + u_time + 0.3 * i) + 1.6);
            }

            vec3 color = vec3(0.5 * sin(coord.x) + 0.5, 0.5 * sin(coord.y) + 0.5, sin(coord.x + coord.y));
            gl_FragColor = vec4(color, 1.0);
        }
        '''
        
        vertex_shader = compile_shader2(vertex_shader_source, GL_VERTEX_SHADER)
        fragment_shader = compile_shader2(fragment_shader_source, GL_FRAGMENT_SHADER)
        program = link_program(vertex_shader, fragment_shader)


        vertices = np.array([
            -1.0, -1.0, 0,
            1.0, -1.0, 0,
            -1.0, 1.0, 0,
            1.0, 1.0, 0
        ], dtype=np.float32)
        vao1 = glGenVertexArrays(1)
        glBindVertexArray(vao1)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        resolution_loc = glGetUniformLocation(program, "u_resolution")
        time_loc = glGetUniformLocation(program, "u_time")

        running = True
        clock = pygame.time.Clock()
        
        
        # glViewport(0, 0, screen_width, screen_height)
        # self.initialise()
        done = False
        pygame.event.set_grab(True) #appuye sur la souris comme ca elle reste sur la fenetre
        pygame.mouse.set_visible(False) #enleve la visu de la souris
        glEnable(GL_DEPTH_TEST)
        # glDepthMask(GL_FALSE)
        glClearColor(0.0, 0.0, 0.0, 0.0)

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: #comme on voit plus la souris on echap ac escap
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)

            # glViewport(0, 0, 1280, 720)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(program)
            glBindVertexArray(vao1)

            # glViewport(0, 0, screen_width, screen_height)
            # glClear(GL_COLOR_BUFFER_BIT)

            glUniform2f(resolution_loc, screen_width, screen_height)
            glUniform1f(time_loc, pygame.time.get_ticks() / 1000)
            glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
            # self.camera_init()

            #Mesh display
            self.display()
            pygame.display.flip()
            # pygame.time.wait(60)
        pygame.quit()


