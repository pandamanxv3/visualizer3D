from .Mesh import *
from .Utils import *
import random

class   LoadMesh(Mesh):
    def __init__(self, filename, program_id, draw_type=GL_TRIANGLES, location=pygame.Vector3(0,0,0)):
        #rotation=Rotation(0, pygame.Vector3(0, 1, 0))):
        coordinate, triangles = self.load_drawing(filename)
        self.vertices = format_vertices(coordinate, triangles)
        colors = [] 
        for i in range(len(self.vertices)): #pour linstant on va generer une random color pour chaque point quon a extrait de load_drawing
            colors.append(random.random())
            colors.append(random.random())
            colors.append(random.random())

        super().__init__(program_id, self.vertices, colors, draw_type, location)
    
    def farest_point(self):
        max_distance = 0
        for vertex in self.vertices:
            distance = np.linalg.norm(vertex)
            if distance > max_distance:
                max_distance = distance
        return max_distance

    def load_drawing(self, filename):
        vertices = []
        triangles = []
        with open(filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    vertices.append((vx, vy, vz))
                if line[:2] == "f ": #on gere pour linstant que le premier de x/x/x ou x//x etc..
                    t1, t2, t3 = [value for value in line[2:].split()]
                    triangles.append( [int(value) for value in t1.split('/')][0] - 1)
                    triangles.append( [int(value) for value in t2.split('/')][0] - 1)
                    triangles.append( [int(value) for value in t3.split('/')][0] - 1)
                #if vf
                #if vt
                line = fp.readline()
        return vertices, triangles

