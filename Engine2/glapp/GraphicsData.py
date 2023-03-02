from OpenGL.GL import *
import numpy as np

class GraphicsData():
    ''' Cette partie définit la classe GraphicsData qui est utilisée pour stocker et transmettre des données graphiques. 
        Le constructeur de la classe prend deux arguments: 
        data_type et data, qui sont respectivement le type de données et les données elles-mêmes. 
        La classe crée également une référence à un tampon de mémoire OpenGL en utilisant glGenBuffers.'''
    def __init__(self, data_type, data):
        self.data_type = data_type  # spécifie le type de donnée, par exemple "vec3", "vec4", etc.
        self.data = data # les données elles-mêmes
        self.buffer_ref = glGenBuffers(1) # crée une référence à un tampon de mémoire OpenGL
        self.load() # charge les données dans le tampon

    
    ''' Cette méthode est appelée par le constructeur de la classe et charge les données dans le tampon de mémoire OpenGL associé à l'instance de GraphicsData. 
        Pour cela, elle commence par convertir les données en un tableau NumPy de type float32. 
        Ensuite, elle associe le tampon actif à GL_ARRAY_BUFFER et charge les données dans le tampon OpenGL en utilisant glBufferData.'''
    def load(self):
        data = np.array(self.data, np.float32) # convertit les données en un tableau numpy de type float32
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ref) # associe le tampon actif à GL_ARRAY_BUFFER
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW) # charge les données dans le tampon OpenGL actif

    ''' Cette méthode est utilisée pour transmettre les données aux shaders.
        Elle prend en entrée l'ID du programme de shaders et le nom de la variable d'attribut à laquelle les données doivent être associées. 
        Tout d'abord, la méthode utilise glGetAttribLocation pour obtenir l'ID de l'attribut pour le nom de variable spécifié.
        Ensuite, elle associe le tampon de mémoire OpenGL actif à GL_ARRAY_BUFFER.
        Si le type de données est "vec3", la méthode spécifie comment les données doivent être traitées pour l'attribut spécifié en utilisant glVertexAttribPointer.'''
    def create_variable(self, program_id, variable_name):
        variable_id = glGetAttribLocation(program_id, variable_name) # obtient l'ID de l'attribut pour le nom de variable spécifié
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ref) # associe le tampon de mémoire OpenGL actif à GL_ARRAY_BUFFER
        #il est possible que d'autres opérations de dessin effectuées après aient modifié l'état d'OpenGL et donc que GL_ARRAY_BUFFER ne soit plus lié à ce moment-là du coup je link mon buffer ou ya les data au buffer de vertex
        if self.data_type == "vec3":
            glVertexAttribPointer(variable_id, 3, GL_FLOAT, False, 0, None) # spécifie la façon de traiter les données pour l'attribut spécifié
        glEnableVertexAttribArray(variable_id)

        # en gros le constructeur prend la var et la charge dans un buffer, et la fonction create_variable la transmet au shader via le program_id
        # en specifiant le "type" que cest, cest a dire le 'in' correspondant dans le GLSL
        