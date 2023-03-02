from OpenGL import *
import pygame
import time
from .GraphicsData import *
import numpy as np
from .Uniform import *
from .Transformations import *

class Mesh:
    def __init__(self, program_id, vertices, vertex_colors, draw_type, translation=pygame.Vector3(0, 0, 0)):
        self.vertices = vertices
        self.draw_type = draw_type
        self.vao_ref = glGenVertexArrays(1) #un vao(vertex array object) stock plusieurs buffer
        glBindVertexArray(self.vao_ref)
        position = GraphicsData("vec3", self.vertices)
        position.create_variable(program_id, "position")
        color = GraphicsData("vec3", vertex_colors)
        color.create_variable(program_id, "vert_color")
        self.color_uniform = Uniform("vec3", pygame.Vector3(0, 1, 0))
        self.color_uniform.find_variable(program_id, "color_unif")
        self.transformation_mat = identity_matrix()
        self.transformation_mat = translate(self.transformation_mat, translation.x, translation.y, translation.z)

        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(program_id, "model_mat")

    def draw(self, rotation = False):
        if rotation == True:
            rotation_angle = time.time() % 360 * 15 #pour chaque seconde passé on rotate de 15degres
            rotation_matrix = rotate_y_mat(rotation_angle)
            self.transformation.load(rotation_matrix)
        else:
            self.transformation.load()
        self.color_uniform.load()
        glBindVertexArray(self.vao_ref)
        glDrawArrays(self.draw_type, 0, len(self.vertices))
        