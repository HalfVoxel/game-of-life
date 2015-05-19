import pyglet
from pyglet.gl import *

class GUI:
	def __init__ (self):
		self.interactable = []

	def addInteractable (self,entity):
		self.interactable.append(entity)

	def handle_click (self,x, y):
		for entity in self.interactable:
			if entity.handle_click(x,y):
				return True

		return False

	def draw(self):
		for entity in self.interactable:
			entity.draw()

class Interactable:

	def __init__ (self, x, y, width, height, label):
		self.enabled = True
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.state = 0

		self.label = pyglet.text.Label(label,
								  font_name='Helvetica',
								  font_size=14,
								  x=x+width//2, y=y+height//2,
								  anchor_x='center', anchor_y='center')

	
	def clicked (self):
		pass

	def set_label (self, label):
		self.label.text = label

	def in_rect (self, x, y):
		return x >= self.x and y >= self.y and x <= self.x+self.width and y <= self.y+self.height

	def handle_click (self, x, y):
		if self.enabled and self.in_rect(x,y):
			self.clicked()
			return True

		return False

	def draw(self):

		if self.state == 0:
			# Draw solid 1px border

			draw_rect_solid (self.x,self.y,self.width,self.height,50)
			draw_rect_outline (self.x,self.y,self.width,self.height,255)

		elif self.state == 1:

			# Draw active state
			draw_rect_solid (self.x,self.y,self.width,self.height,0)
			draw_rect_outline (self.x,self.y,self.width,self.height,200)

		self.label.draw()

class Label(Interactable):

	def handle_click (self, x, y):
		return False

	def draw (self):
		self.label.draw()

class Button(Interactable):
	def __init__ (self, x, y, width, height, label, callback):
		super().__init__(x,y,width,height,label)
		self.callback = callback

	def clicked(self):
		self.state = 1
		self.callback()

	def draw(self):
		super().draw()

		# state 1 (active) will revert to state 0 (normal) after one frame
		self.state = 0

class Toggle(Interactable):
	def __init__ (self, x, y, width, height, label, callback):
		super().__init__(x,y,width,height,label)
		self.callback = callback

	def clicked(self):
		self.state = 1 if self.state == 0 else 0
		self.callback(self.state == 0)

	def set_state (self, state):
		self.state = 0 if state else 1

def draw_rect_solid (x, y, width, height, gray):
	glBegin(GL_TRIANGLES)
	_data_rect_solid(x,y,width,height,gray)
	glEnd()

def _data_rect_solid (x, y, width, height, gray):
	glColor3ub(gray,gray,gray)
	glVertex2f(x,y)

	glColor3ub(gray,gray,gray)
	glVertex2f(x+width,y)				

	glColor3ub(gray,gray,gray)
	glVertex2f(x+width,y+height)

	glColor3ub(gray,gray,gray)
	glVertex2f(x,y)

	glColor3ub(gray,gray,gray)
	glVertex2f(x+width,y+height)

	glColor3ub(gray,gray,gray)
	glVertex2f(x,y+height)
	

def draw_rect_outline (x, y, width, height, gray):
	glBegin(GL_TRIANGLES)
	_data_rect_outline (x,y,width,height,gray)
	glEnd()

def _data_rect_outline (x, y, width, height, gray):
	_data_rect_solid (x,y,1,height,gray)
	_data_rect_solid (x+width-1,y,1,height,gray)
	_data_rect_solid (x,y,width,1,gray)
	_data_rect_solid (x,y+height-1,width,1,gray)
