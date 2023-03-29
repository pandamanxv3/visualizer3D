from OpenGL.GL import *
import numpy as np

def format_vertices(coordinates, triangles): #fait une array avec les triangle composé de leurs points a la suite 
    allTriangles = []
    for t in range(0, len(triangles), 3):
        allTriangles.append(coordinates[triangles[t]])
        allTriangles.append(coordinates[triangles[t + 1]])
        allTriangles.append(coordinates[triangles[t + 2]])
    return np.array(allTriangles, np.float32)

def compile_shader2(shader_source, shader_type):
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


def compile_shader(shader_type, shader_source): #prend le type de shader(vertex ou fragment) et le code GLSL
    shader_id = glCreateShader(shader_type) #Cette ligne crée un nouvel objet de shader avec le type de shader spécifié.
    glShaderSource(shader_id, shader_source) #specifie la source en tant que chaine de charactere
    glCompileShader(shader_id) #compile et genere du code binaire executable par la carte graphique
    compile_success = glGetShaderiv(shader_id, GL_COMPILE_STATUS) #La fonction renvoie une valeur booléenne qui indique si la compilation a réussi ou échoué.
    if not compile_success:
        error_message = glGetShaderInfoLog(shader_id) 
        glDeleteShader(shader_id)
        error_message = "\n" + error_message.decode("utf-8")
        raise Exception(error_message)
    #Si la compilation échoue, cette section récupère le message d'erreur du compilateur de shader 
    #en appelant la fonction OpenGL glGetShaderInfoLog avec l'ID de shader. 
    #Le message d'erreur est ensuite formaté et une exception est levée avec le message d'erreur.
    
    return shader_id

def create_program(vertex_shader_code, fragment_shader_code):
    vertex_shader_id = compile_shader(GL_VERTEX_SHADER, vertex_shader_code)
    fragment_shader_id = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_code)
    program_id = glCreateProgram()
    glAttachShader(program_id, vertex_shader_id)
    glAttachShader(program_id, fragment_shader_id)
    glLinkProgram(program_id)
    link_success = glGetProgramiv(program_id, GL_LINK_STATUS)
    if not link_success:
        info = glGetProgramInfoLog(program_id)
        raise RuntimeError(info)
    glDeleteShader(vertex_shader_id)
    glDeleteShader(fragment_shader_id)
    return program_id