class Simulator:

	_dx = [1, 1, 0, -1, -1, -1, 0, 1]
	_dy = [0, 1, 1, 1, 0, -1, -1, -1]

	def __init__ (self, size):
		self.size = size
		self.world = [[False for x in range(0,size)] for x in range(0,size)]
		self.tmpworld = [[False for x in range(0,size)] for x in range(0,size)]

	def wrap(self,v,size):
		if v < 0:
			v -= (v//size)*size
		return v % size

	def set (self,x,y,value):
		self.world[y][x] = value

	def set_not_wrapped (self,x,y,value):
		if x < 0 or y < 0 or x >= self.size or y >= self.size:
			return
		self.world[y][x] = value

	def get (self,x,y):
		x = self.wrap(x,self.size)
		y = self.wrap(y,self.size)
		return self.world[y][x]

	def update (self):

		for y in range(0,self.size):
			for x in range(0,self.size):
				count = 0
				for i in range(0,len(Simulator._dx)):
					nx = x+Simulator._dx[i]
					ny = y+Simulator._dy[i]
					if self.get(nx,ny):
						count += 1

				self.tmpworld[y][x] = count == 3 or (count == 2 and self.get(x,y))

		# Swap
		tmp = self.world
		self.world = self.tmpworld
		self.tmpworld = tmp