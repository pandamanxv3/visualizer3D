from glapp.pyOGLApp import *
import numpy as np
from glapp.Utils import *
from glapp.GraphicsData import * 
from glapp.Square import *
from glapp.Triangle import *
from math import *

vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vert_color;
uniform vec3 translation;
uniform vec3 color_unif;
out vec3 colour;

void main()
{
    vec3 pos = position + translation;
    gl_Position = vec4(pos, 1);
    colour = vert_color * color_unif;
} 
'''

fragment_shader = r'''
#version 330 core

in vec3 colour;

out vec4 frag_color;
void main ()
{
    frag_color = vec4(colour, 1);
}
'''

class   MyFirstShader(PyOGLapp):

    def __init__(self):
        super().__init__(850, 200, 1000, 800)
        # self.vao_ref = None
        #self.vertex_count = 0
        self.square = None
        self.triangle = None

    
    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.square = Square(self.program_id)
        self.triangle = Triangle(self.program_id, pygame.Vector3(0.5, -0.5, 0))
        self.i = 0
        
        # self.vao_ref = glGenVertexArrays(1)
        # glBindVertexArray(self.vao_ref) #permet de bind les modificatoin de vertexarray utiliser partout a cette variable
        
        # glPointSize(10)
        # position_data = [[0, -0.9, 0],
        #                  [-0.6, 0.8, 0],
        #                  [0.9, -0.2, 0],
        #                  [-0.9, -0.2, 0],
        #                  [0.6, 0.8, 0],
        #                  [0, -0.9, 0]]
        # self.vertex_count = len(position_data)
        # position_variable = GraphicsData("vec3", position_data)
        # position_variable.create_variable(self.program_id, "position")
        # color_data = [[0,0,1], [0,1,0], [1,0,1], [1,0,0], [1,1,0], [0,1,1]]
        # color_variable = GraphicsData("vec3", color_data)
        # color_variable.create_variable(self.program_id, "vert_color")
    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id) #cest pas le programme qui decide il repasse juste sur les point pour ajuster quand il seront dessiney
        
        if self.i == 360:
            self.i = 0
        else :
            self.i = self.i + 1
        # self.square.draw()
        unif_color = pygame.Vector3(abs(cos(radians(self.i)))*0.9 + 0.1, abs(sin(radians(self.i)))*0.9 + 0.1, (abs(sin(radians(self.i))) * abs(cos(radians(self.i))))*0.9 + 0.1)
        unif_pos = pygame.Vector3(cos(radians(self.i))/2, sin(radians(self.i))/2, 0)
        self.square.draw(unif_pos, unif_color)

        

        # self.triangle.draw(pygame.Vector3(cos(radians(self.i))/2,cos(radians(self.i))/2, 0))
        print("red is:", abs(cos(radians(self.i))), abs(sin(radians(self.i))), "green is:", abs(sin(radians(self.i))) * abs(cos(radians(self.i))))
        # glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)#il utilise le bbind de plus haut


MyFirstShader().mainloop()
