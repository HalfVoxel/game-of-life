import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
import Simulator
import time
import GUI

class View:

	# Minimum distance in pixels for a mouse drag to be handled
	MIN_DRAG_DIST = 5
	SCROLL_SPEED = 1.0/80.0

	def __init__(self, window, simulator):
		self.sim = simulator
		self.window = window

		self.lastUpdate = 0.0

		self.viewScale = 30
		self.viewOffset = (0,0)

		self.vertex_list = pyglet.graphics.vertex_list(self.sim.size*self.sim.size*6, 'v2f', 'c4B')

		self.mouseClickStartTime = 0
		self.accumulatedDrag = (0,0)
		self.mouseStartDrag = (0,0)
		self.viewOffsetStart = (0,0)

		self.running = False
		self.speed = 3
		self.skip = 0

		# Create a bunch of buttons to handle user interactions
		self.gui = GUI.GUI()

		controlBarY = window.height-30-5

		self.playButton = GUI.Button(5,window.height-30-5,80,30,"Run", self.on_click_run)
		self.stepButton = GUI.Button(self.playButton.x+self.playButton.width+5, controlBarY, 80, 30, "Step", self.on_click_step)

		self.clearButton = GUI.Button(self.stepButton.x+self.stepButton.width+5, controlBarY, 80, 30, "Clear", self.on_click_clear)

		self.slowerButton = GUI.Button(self.clearButton.x+self.clearButton.width+5+10, controlBarY, 40, 30, "<<", self.on_click_slower)
		self.speedLabel = GUI.Label(self.slowerButton.x+self.slowerButton.width+5, controlBarY, 80, 30, "Speed: "+str(self.speed))
		self.fasterButton = GUI.Button(self.speedLabel.x+self.speedLabel.width+5, controlBarY, 40, 30, ">>", self.on_click_faster)

		self.skipLessButton = GUI.Button(self.fasterButton.x+self.fasterButton.width+5+10, controlBarY, 40, 30, "<<", self.on_click_skip_less)
		self.skipLabel = GUI.Label(self.skipLessButton.x+self.skipLessButton.width+5, controlBarY, 80, 30, "Skip: "+str(self.skip))
		self.skipMoreButton = GUI.Button(self.skipLabel.x+self.skipLabel.width+5, controlBarY, 40, 30, ">>", self.on_click_skip_more)

		self.gui.addInteractable(self.playButton)
		self.gui.addInteractable(self.stepButton)
		self.gui.addInteractable(self.slowerButton)
		self.gui.addInteractable(self.speedLabel)
		self.gui.addInteractable(self.fasterButton)
		self.gui.addInteractable(self.skipLessButton)
		self.gui.addInteractable(self.skipLabel)
		self.gui.addInteractable(self.skipMoreButton)
		self.gui.addInteractable(self.clearButton)

		def set_array_element (i, arr):
			def set (state):
				arr[i] = state

			return set


		def toggle_column_with_header (x, y, arr, header_state):
			toggle = GUI.Toggle (x, y, 30, 30, "", None)
			toggle.set_state (header_state)
			toggle.enabled = False
			self.gui.addInteractable(toggle)

			header = GUI.Label (x, y-35, 30, 30, "V")
			self.gui.addInteractable(header)

			for i in range(0,len(arr)):
				toggle = GUI.Toggle (x, y-(i+2)*35, 30, 30, str(i), set_array_element(i,arr))
				toggle.set_state (arr[i])
				self.gui.addInteractable(toggle)

		# Create controls for modifying the rules of the game
		toggle_column_with_header (self.window.width-100, window.height-80, self.sim.aliveRule, True)
		toggle_column_with_header (self.window.width-100+50, window.height-80, self.sim.deadRule, False)

	def on_click_run (self):
		self.running = not self.running
		self.playButton.set_label ("Stop" if self.running else "Run")

	def on_click_step (self):
		if self.running:
			# Stop the simulation and update the button label
			self.on_click_run()

		self.sim.update()

	def on_click_slower (self):
		self.speed = max(self.speed-1,1)
		self.speedLabel.set_label("Speed: " +str(self.speed))

	def on_click_faster (self):
		self.speed = min(self.speed+1,5)
		self.speedLabel.set_label("Speed: " +str(self.speed))

	def on_click_skip_less (self):
		self.skip = max(self.skip-1,0)
		self.skipLabel.set_label("Skip: " +str(self.skip))

	def on_click_skip_more (self):
		self.skip = min(self.skip+1,4)
		self.skipLabel.set_label("Skip: " +str(self.skip))

	def on_click_clear (self):
		self.sim.clear()

	def on_key_press(self,symbol, modifiers):
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

			# Check if the click was handled by any buttons
			if self.gui.handle_click(x,y):
				return
			else:
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

	# Transforms a point from local space (cells) to screen space (pixels)
	def local_to_screen (self, point):
		return (point[0]*self.viewScale + self.viewOffset[0],point[1]*self.viewScale + self.viewOffset[1])

	# Transforms a point from screen space (pixels) to local space (cells)
	def screen_to_local (self, point):
		return ((point[0]-self.viewOffset[0])/self.viewScale, (point[1]-self.viewOffset[1])/self.viewScale)

	def draw(self):

		updateInterval = 1.0/(2**self.speed)
		if time.time() - self.lastUpdate > updateInterval and self.running:
			self.lastUpdate = time.time()

			start = time.time()

			for i in range(0,self.skip+1):
				self.sim.update()

			#print("Updating ",time.time()-start)

		start = time.time()

		self.draw_simulation()

		#print("Rendering ",time.time()-start)

		# Draw an outline around the world
		top_right = self.local_to_screen((self.sim.size,self.sim.size))
		bottom_left = self.local_to_screen((0,0))
		GUI.draw_rect_outline (bottom_left[0],bottom_left[1],top_right[0]-bottom_left[0],top_right[1]-bottom_left[1],80)

		self.gui.draw()

	def draw_simulation(self):
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
