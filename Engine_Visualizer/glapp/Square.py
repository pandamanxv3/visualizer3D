from .Mesh import *

class Square(Mesh):
    def __init__(self, program_id, location=pygame.Vector3(0, 0, 0)):
        vertices = [[0.5, 0.5, -1.0],
                    [0.5, -0.5, -1.0],
                    [-0.5, -0.5, -1.0],
                    [-0.5, 0.5, -1.0]]
        
        self.colors =  [[1, 0, 0],
                        [1, 0.5, 0],
                        [1, 1, 0.5],
                        [0, 0, 1]]
        super().__init__(program_id, vertices, self.colors, GL_TRIANGLE_FAN, location)