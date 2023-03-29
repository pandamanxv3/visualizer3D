import os
os.environ['PYOPENGL_PLATFORM'] = 'wgl'

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from glapp.pyOGLApp import *
import numpy as np
from glapp.Utils import *
from glapp.GraphicsData import * 
from glapp.Square import *
from glapp.Triangle import *
from glapp.Cube import *
from glapp.LoadMesh import *
import time

from math import *
from glapp.Axes import *
from PIL import Image

vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vert_color;

uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;


uniform vec3 color_unif;
out vec3 colour;

void main()
{
	gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1.0);
	colour = vert_color;
} 
'''

fragment_shader = r'''
#version 330 core

in vec3 colour;

out vec4 frag_color;
void main ()
{
	frag_color = vec4(colour, 0.0f);
}
'''


import tkinter as tk
from tkinter import filedialog, messagebox


# Créez une fenêtre Tkinter
def getFile():

	root = tk.Tk()
	root.withdraw()
	script_dir = os.path.dirname(os.path.abspath(__file__))
	# Configurez les options de la boîte de dialogue de sélection de fichier
	file_options = {}
	file_options['initialdir'] = os.path.join(script_dir, 'models')
	file_options['title'] = 'Sélectionnez un fichier obj'
	file_options['filetypes'] = [('Fichier obj', '*.obj')]

	while True:
		# Affichez la boîte de dialogue de sélection de fichier
		file_path = filedialog.askopenfilename(**file_options)

		# Vérifiez si l'utilisateur a sélectionné un fichier
		if file_path:
			if file_path.endswith(".obj"):
				return file_path
			else:
				messagebox.showerror("Erreur de sélection", "Veuillez sélectionner un fichier obj.")				
		else:
			print("Aucun fichier n'a été sélectionné.")
			exit()


class   Projections(PyOGLapp):

	def __init__(self):
		super().__init__(320, 180, 1280, 720)
		self.square = None
		self.triangle = None
		self.Axes = None
		self.blade = None
		
	def initialise(self):
		# fileName = getFile()
		# print (fileName)
		fileName = "/mnt/c/Users/Adnan/Desktop/code/visualizer3D/Engine_Visualizer/models/dragonblade.obj"
		self.program_id = create_program(vertex_shader, fragment_shader)
		# self.shader = compileProgram(
		# 	compile_shader(vertex_source, GL_VERTEX_SHADER),
		# 	compile_shader(shader_source, GL_FRAGMENT_SHADER)
		# )
		# self.square = Square(self.program_id, pygame.Vector3(-0.5, 0.5, 0.0))
		# self.triangle = Triangle(self.program_id, pygame.Vector3(0.5, -0.5, 0.0))
		# self.Axes = Axes(self.program_id, pygame.Vector3(0, 0, 0))
		# self.cube = Cube(self.program_id, pygame.Vector3(0, 2.0, -3.0))
		self.blade = LoadMesh(fileName, self.program_id)
		# self.blade = LoadMesh(fileName, self.program_id)
		self.camera = Camera(self.program_id, self.screen_width, self.screen_height, self.blade.farest_point()*2)
		# self.camera.update_pos(0, 0, self.blade.farest_point()*2)
		# self.camera.initialise_mouse_pos()
		# glEnable(GL_DEPTH_TEST)

		self.i = 0


	def camera_init(self):
		pass

	def display(self):
		glUseProgram(self.program_id)#cest pas le programme qui decide il repasse juste sur les point pour ajuster quand il seront dessiney
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		self.camera.update()
		# self.Axes.draw()
		# self.triangle.draw()
		self.blade.draw(True)
		# if self.i == 360:
		# 	self.i = 0
		# else :
		# 	self.i = self.i + 1
		# self.square.draw()
		# unif_color = pygame.Vector3(abs(cos(radians(self.i)))*0.9 + 0.1, abs(sin(radians(self.i)))*0.9 + 0.1, (abs(sin(radians(self.i))) * abs(cos(radians(self.i))))*0.9 + 0.1)
		# unif_pos = pygame.Vector3(cos(radians(self.i))/2, sin(radians(self.i))/2, 0)
		# self.cube.draw()
		# self.triangle.draw()

		

		# self.triangle.draw(pygame.Vector3(cos(radians(self.i))/2,cos(radians(self.i))/2, 0))
		# print("red is:", abs(cos(radians(self.i))), abs(sin(radians(self.i))), "green is:", abs(sin(radians(self.i))) * abs(cos(radians(self.i))))
		# glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)#il utilise le bbind de plus haut


Projections().mainloop()
