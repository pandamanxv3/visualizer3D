from .Mesh import *

class Triangle(Mesh):
    def __init__(self, program_id, location=pygame.Vector3(0, 0, 0)):
        vertices = [[0, 0.5, -1.0],
                    [0.5, -0.5, -1.0],
                    [-0.5, -0.5, -1.0]]        
        colors =    [[1, 0, 0],
                     [0.05, 1, 0.1],
                     [0.05, 1, 0.1]]
        super().__init__(program_id, vertices, colors, GL_TRIANGLE_FAN, location)