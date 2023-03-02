import pygame
from OpenGL.GLU import *
from math import *
import numpy as np
from .Transformations import *
from .Uniform import *
import pyautogui

class Camera:
    def __init__(self, program_id, w, h, z=1):
        self.program_id = program_id
        self.transformation = identity_matrix()
        self.transformation = translate(self.transformation, 0, 0, z)
        self.last_mouse = pygame.math.Vector2(0, 0)
        self.mouse_sensitivityX = 0.1
        self.mouse_sensitivityY = 0.1
        self.key_sensitivity = 0.008
        self.projection_mat = self.perspective_mat(60, w / h, 0.01, 10000)
        self.projection = Uniform("mat4", self.projection_mat)
        self.projection.find_variable(program_id, "projection_mat")
        self.screen_width = w
        self.screen_height = h
        self.program_id = program_id
        print("Taille de l'eécran : ", self.screen_width / 2, "y", self.screen_height / 2)

        # pygame.mouse.set_pos(500, 400)


    def get_camera_matrix(self):
    # Définir la position, l'orientation et l'échelle de la caméra
        position = np.array([0, 0, 0], np.float32)  # position de la caméra
        orientation = np.array([0, 0, 0], np.float32)  # orientation de la caméra
        scale = np.array([1, 1, 1], np.float32)  # échelle de la caméra

        # Calculer la matrice de transformation de la caméra
        translation_matrix = translate_mat(-position[0], -position[1], -position[2])
        rotation_matrix = rotate_y_mat(orientation[1]) @ rotate_x_mat(orientation[0])
        scale_matrix = np.array([[scale[0], 0, 0, 0],
                                [0, scale[1], 0, 0],
                                [0, 0, scale[2], 0],
                                [0, 0, 0, 1]], np.float32)
        camera_matrix = translation_matrix @ rotation_matrix @ scale_matrix

        return camera_matrix

    def perspective_mat(self, angle_of_view, aspect_ratio, near_plane, far_plane):
        a = radians(angle_of_view)
        d = 1.0 / tan(a / 2.0)
        r = aspect_ratio
        b = (far_plane + near_plane) / ( near_plane - far_plane)
        c = far_plane * near_plane / ( near_plane - far_plane)
        return np.array([[d/r, 0,  0, 0],
                         [0  , d,  0, 0],
                         [0  , 0,  b, c],
                         [0  , 0, -1, 0]], np.float32)

    def rotate(self, yaw, pitch):
        forward = pygame.Vector3(self.transformation[0,2], self.transformation[1,2], self.transformation[2,2])
        up = pygame.Vector3(0, 1, 0)
        angle = forward.angle_to(up)

        self.transformation = rotate(self.transformation, yaw, "y", False)
        if angle < 170.0 and pitch > 0 or angle > 30.0 and pitch < 0:
            self.transformation = rotate(self.transformation, pitch, "x")
        # self.yaw += yaw
        # self.pitch += pitch
        #
        # if self.pitch > 89.0:
        #    self.pitch = 89.0
        #
        # if self.pitch < -89.0:
        #    self.pitch = 89.0
        #
        # self.forward.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        # self.forward.y = sin(radians(self.pitch))
        # self.forward.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        # self.forward = self.forward.normalize()
        # self.right = self.forward.cross(pygame.math.Vector3(0, 1, 0)).normalize()
        # self.up = self.right.cross(self.forward).normalize()
    

    def initialise_mouse_pos(self):
        self.mouse_pos = pygame.mouse.get_pos()

        


    def update(self):
        if pygame.mouse.get_visible():
            return
        
        # self.mouse_pos = pygame.mouse.get_pos()
        # print("Position de la souris :", self.mouse_pos)

        # mouse_change = self.last_mouse - pygame.math.Vector2(self.mouse_pos)
        # # print("Mouse Change: " + str(mouse_change[0]) + ", " + str(mouse_change[1]))
        # pygame.mouse.set_pos(500, 400)
        # self.last_mouse = pygame.mouse.get_pos()
        # self.rotate(mouse_change.x * self.mouse_sensitivityX, mouse_change.y * self.mouse_sensitivityY)

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_DOWN]:
        #     self.transformation = translate(self.transformation, 0, 0, self.key_sensitivity)
        # if keys[pygame.K_UP]:
        #     self.transformation = translate(self.transformation, 0, 0, -self.key_sensitivity)
        # if keys[pygame.K_RIGHT]:
        #     self.transformation = translate(self.transformation, self.key_sensitivity, 0, 0)
        # if keys[pygame.K_LEFT]:
        #     self.transformation = translate(self.transformation, -self.key_sensitivity, 0, 0)

        # # self.look = self.eye + self.forward
        # # gluLookAt(self.eye.x, self.eye.y, self.eye.z,
        # #         self.look.x, self.look.y, self.look.z,
        # #         self.up.x, self.up.y, self.up.z)

        self.projection.load()
        lookat_map = self.transformation
        lookat = Uniform("mat4", lookat_map)
        lookat.find_variable(self.program_id, "view_mat")
        lookat.load()

