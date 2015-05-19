import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
import Simulator
import View
import time
import sys

window = pyglet.window.Window(1400,800)

sim = Simulator.Simulator(50)

# Load input file if any
if len(sys.argv) > 1:
	sim.load (open(sys.argv[1]).read())

view = View.View(window, sim)

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