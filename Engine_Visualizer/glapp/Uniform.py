from OpenGL.GL import *
import numpy as np

class Uniform():
    def __init__(self, data_type, data):
        self.data_type = data_type
        self.data = data
        self.variable_id = None
    
    def find_variable(self, program_id, variable_type):
        self.variable_id = glGetUniformLocation(program_id, variable_type)

    # def change_variable(self. )
    def load(self, data = None):
        if isinstance(data, np.ndarray):
            self.data = data
        if self.data_type == "vec3":
            glUniform3f(self.variable_id, self.data[0], self.data[1], self.data[2])
        elif self.data_type == "mat4":
            glUniformMatrix4fv(self.variable_id, 1, GL_TRUE, self.data)