import os
os.environ['PYOPENGL_PLATFORM'] = 'wgl'

import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *

pygame.init()

def compile_shader(shader_source, shader_type):
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


def main():
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)

    # glEnable(GL_DEPTH_TEST)
    # glDepthFunc(GL_LESS)

    vertex_shader_source = r'''
    #version 330 core

    layout(location = 0) in vec3 a_position;

    void main() {
        gl_Position = vec4(a_position, 1.0);
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

    vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)
    program = link_program(vertex_shader, fragment_shader)

    glUseProgram(program)

    vertices = np.array([
        -1.0, -1.0, 0.0,
        1.0, -1.0, 0.0,
        -1.0, 1.0, 0.0,
        1.0, 1.0, 0.0
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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glUseProgram(program)
        glBindVertexArray(vao1)

        # glViewport(0, 0, screen_width, screen_height)
        glClear(GL_COLOR_BUFFER_BIT)

        glUniform2f(resolution_loc, screen_width, screen_height)
        glUniform1f(time_loc, pygame.time.get_ticks() / 1000)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        pygame.display.flip()
        clock.tick(60)  # Limite le taux de rafraîchissement à 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
