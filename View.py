import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
import Simulator
import time

class View:

	# Minimum distance in pixels for a mouse drag to be handled
	MIN_DRAG_DIST = 5
	SCROLL_SPEED = 1.0/80.0

	def __init__(self, window):
		self.sim = Simulator.Simulator(50)
		self.window = window

		self.sim.set(5,5,True)
		self.sim.set(6,5,True)
		self.sim.set(5,6,True)
		self.sim.set(6,6,True)

		self.sim.set(9,4,True)
		self.sim.set(9,5,True)
		self.sim.set(9,6,True)

		self.lastUpdate = 0.0

		self.viewScale = 30
		self.viewOffset = (0,0)

		self.label = pyglet.text.Label('Hello, world',
								  font_name='Times New Roman',
								  font_size=36,
								  x=window.width//2, y=window.height//2,
								  anchor_x='center', anchor_y='center')

		self.vertex_list = pyglet.graphics.vertex_list(self.sim.size*self.sim.size*6, 'v2f', 'c4B')

		self.mouseClickStartTime = 0
		self.accumulatedDrag = (0,0)
		self.mouseStartDrag = (0,0)
		self.viewOffsetStart = (0,0)

	def on_key_press(self,symbol, modifiers):
		#self.viewOffset = (self.viewOffset[0]+0.1,self.viewOffset[1])
		pass

	def on_mouse_press(self,x, y, button, modifiers):
		if button == mouse.LEFT:
			self.mouseClickStartTime = time.time()
			self.accumulatedDrag = (0,0)
			self.mouseStartDrag = (x,y)
			self.viewOffsetStart = self.viewOffset

	def on_mouse_release(self,x, y, button, modifiers):
		if button == mouse.LEFT and abs(self.accumulatedDrag[0]) < View.MIN_DRAG_DIST and abs(self.accumulatedDrag[1]) < View.MIN_DRAG_DIST:
			# Click detected
			p = self.screen_to_local ((x,y))
			self.sim.set_not_wrapped (int(p[0]),int(p[1]), not self.sim.get(int(p[0]),int(p[1])))

	def on_mouse_scroll(self, x, y, dx, dy):
		scroll = dy*View.SCROLL_SPEED

		alpha = 1 - scroll
		self.viewScale *= alpha

		# Some math to make sure that zooming is done towards the mouse cursor
		zoomTowards = (x,y)
		self.viewOffset = (
			(self.viewOffset[0]-zoomTowards[0])*alpha + zoomTowards[0],
			(self.viewOffset[1]-zoomTowards[1])*alpha + zoomTowards[1]
		)

	def on_mouse_drag(self,x, y, dx, dy, button, modifiers):
		if button == mouse.LEFT:
			self.accumulatedDrag = (self.accumulatedDrag[0]+dx, self.accumulatedDrag[1]+dy)

			if abs(self.accumulatedDrag[0]) >= View.MIN_DRAG_DIST or abs(self.accumulatedDrag[1]) >= View.MIN_DRAG_DIST:
				self.viewOffset = (self.viewOffsetStart[0]+self.accumulatedDrag[0], self.viewOffsetStart[1]+self.accumulatedDrag[1])

	def local_to_screen (self, point):
		return (point[0]*self.viewScale + self.viewOffset[0],point[1]*self.viewScale + self.viewOffset[1])

	def screen_to_local (self, point):
		return ((point[0]-self.viewOffset[0])/self.viewScale, (point[1]-self.viewOffset[1])/self.viewScale)

	def draw(self):

		#print("Draw...")

		

		if time.time() - self.lastUpdate > 0.3:
			self.lastUpdate = time.time()

			start = time.time()
			self.sim.update()
			print("Updating ",time.time()-start)

		start = time.time()

		vertices = []
		colors = []
		for y in range(0,self.sim.size):
			
			for x in range(0,self.sim.size):

				cellActive = self.sim.get(x,y)

				r=g=b = 255 if cellActive else 0

				for i in range(0,6):
					colors.append(r)
					colors.append(g)
					colors.append(b)
					colors.append(255)

				p = self.local_to_screen((x,y))
				vertices.append(p[0])
				vertices.append(p[1])

				p = self.local_to_screen((x+1,y))
				vertices.append(p[0])
				vertices.append(p[1])

				p = self.local_to_screen((x+1,y+1))
				vertices.append(p[0])
				vertices.append(p[1])

				p = self.local_to_screen((x,y))
				vertices.append(p[0])
				vertices.append(p[1])

				p = self.local_to_screen((x+1,y+1))
				vertices.append(p[0])
				vertices.append(p[1])

				p = self.local_to_screen((x,y+1))
				vertices.append(p[0])
				vertices.append(p[1])

		self.vertex_list.vertices = vertices
		self.vertex_list.colors = colors
		self.vertex_list.draw(GL_TRIANGLES)

		print("Rendering ",time.time()-start)

		self.label.draw()

