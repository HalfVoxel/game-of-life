import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
import Simulator
import View
import time

window = pyglet.window.Window(1400,800)

view = View.View(window)


@window.event
def on_key_press(symbol, modifiers):
	view.on_key_press(symbol,modifiers)

@window.event
def on_draw():
	window.clear()

	view.draw()

def update(deltaTime):
	pass

@window.event
def on_mouse_press(x, y, button, modifiers):
	view.on_mouse_press(x,y,button,modifiers)

@window.event
def on_mouse_release(x, y, button, modifiers):
	view.on_mouse_release(x,y,button,modifiers)

@window.event
def on_mouse_scroll(x, y, dx, dy):
	view.on_mouse_scroll(x,y,dx,dy)

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
	view.on_mouse_drag(x,y,dx,dy,button,modifiers)

pyglet.clock.schedule_interval(update, 1.0/60.0)

pyglet.app.run()


# def compiler_shader (name):
# 	# Read our shaders into the appropriate buffers
# 	vertexSource = file(name+".vertex").read() # Get source code for vertex shader.
# 	fragmentSource = file(name+".vertex").read() # Get source code for fragment shader.
	 
# 	# Create an empty vertex shader handle
# 	vertexShader = glCreateShader(GL_VERTEX_SHADER)
	 
# 	# Send the vertex shader source code to GL
# 	# Note that std::string's .c_str is NULL character terminated.
# 	#const GLchar *source = (const GLchar *)vertexSource.c_str()
# 	glShaderSource(vertexShader, 1, [vertexSource], 0)
	
# 	# Compile the vertex shader
# 	glCompileShader(vertexShader)
	
# 	isCompiled = GLint(0)
# 	glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &isCompiled)
# 	if(isCompiled == GL_FALSE)
# 	{
# 		#GLint maxLength = 0
# 		#glGetShaderiv(vertexShader, GL_INFO_LOG_LENGTH, &maxLength)
	 
# 		# The maxLength includes the NULL character
# 		#std::vector<GLchar> infoLog(maxLength)
# 		#glGetShaderInfoLog(vertexShader, maxLength, &maxLength, &infoLog[0])
	 
# 		# We don't need the shader anymore.
# 		#glDeleteShader(vertexShader)
	 
# 		# Use the infoLog as you see fit.
	 
# 		# In this simple program, we'll just leave
# 		print ("Shader compilation failed")
# 		return
# 	}
	 
# 	# Create an empty fragment shader handle
# 	fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
	 
# 	# Send the fragment shader source code to GL
# 	# Note that std::string's .c_str is NULL character terminated.
# 	# source = (const GLchar *)fragmentSource.c_str()
# 	glShaderSource(fragmentShader, 1, [fragmentSource], 0)
# 	#glShaderSource(fragmentShader, 1, &source, 0)
	 
# 	# Compile the fragment shader
# 	glCompileShader(fragmentShader)
	 
# 	glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &isCompiled)
# 	if(isCompiled == GL_FALSE)
# 	{
# 		#GLint maxLength = 0
# 		#glGetShaderiv(fragmentShader, GL_INFO_LOG_LENGTH, &maxLength)
	 
# 		# The maxLength includes the NULL character
# 		#std::vector<GLchar> infoLog(maxLength)
# 		#glGetShaderInfoLog(fragmentShader, maxLength, &maxLength, &infoLog[0])
	 
# 		# We don't need the shader anymore.
# 		#glDeleteShader(fragmentShader)
# 		# Either of them. Don't leak shaders.
# 		#glDeleteShader(vertexShader)
	 
# 		# Use the infoLog as you see fit.
	 
# 		# In this simple program, we'll just leave
# 		print ("Shader compilation failed")
# 		return
# 	}
	 
# 	# Vertex and fragment shaders are successfully compiled.
# 	# Now time to link them together into a program.
# 	# Get a program object.
# 	program = glCreateProgram()
	 
# 	# Attach our shaders to our program
# 	glAttachShader(program, vertexShader)
# 	glAttachShader(program, fragmentShader)
	 
# 	# Link our program
# 	glLinkProgram(program)
	 
# 	# Note the different functions here: glGetProgram* instead of glGetShader*.
# 	isLinked = GLint(0)
# 	glGetProgramiv(program, GL_LINK_STATUS, (int *)&isLinked)
# 	if(isLinked == GL_FALSE)
# 	{
# 		#GLint maxLength = 0
# 		#glGetProgramiv(program, GL_INFO_LOG_LENGTH, &maxLength)
	 
# 		# The maxLength includes the NULL character
# 		#std::vector<GLchar> infoLog(maxLength)
# 		#glGetProgramInfoLog(program, maxLength, &maxLength, &infoLog[0])
	 
# 		# We don't need the program anymore.
# 		#glDeleteProgram(program)
# 		# Don't leak shaders either.
# 		#glDeleteShader(vertexShader)
# 		#glDeleteShader(fragmentShader)
	 
# 		# Use the infoLog as you see fit.
	 
# 		# In this simple program, we'll just leave
# 		print ("Linking failed")
# 		return
# 	}
	 
# 	# Always detach shaders after a successful link.
# 	glDetachShader(program, vertexShader)
# 	glDetachShader(program, fragmentShader)