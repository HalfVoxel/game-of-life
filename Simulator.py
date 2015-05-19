from functools import reduce

class Simulator:

	_dx = [1, 1, 0, -1, -1, -1, 0, 1]
	_dy = [0, 1, 1, 1, 0, -1, -1, -1]


	def __init__ (self, size):
		self.clear_and_set_size(size)
		self.aliveRule = [False, False, True, True, False, False, False, False, False]
		self.deadRule =  [False, False, False, True, False, False, False, False, False]

	def clear_and_set_size (self, size):
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

	def clear (self):
		for y in range(0,self.size):
			for x in range(0,self.size):
				self.set(x,y,False)

	def update (self):

		for y in range(0,self.size):
			for x in range(0,self.size):
				count = 0
				for i in range(0,len(Simulator._dx)):
					nx = x+Simulator._dx[i]
					ny = y+Simulator._dy[i]
					if self.get(nx,ny):
						count += 1

				self.tmpworld[y][x] = self.aliveRule[count] if self.world[y][x] else self.deadRule[count]

		# Swap
		tmp = self.world
		self.world = self.tmpworld
		self.tmpworld = tmp

	def load (self,dataString):
		try:
			coordinates = [(int(pair[0]), int(pair[1])) for pair in [line.split(' ') for line in dataString.strip().split('\n')]]
		except e:
			print ("Could not parse data. Invalid format.\nFormat should be '(\d+ \d+\\n)*'")
			print (e)
			return

		size = reduce(lambda acc,v: max(acc,max(v[0],v[1])), coordinates, 0)
		size = max(size,20)

		self.clear_and_set_size (size)

		for coord in coordinates:
			self.set(coord[0], coord[1], True)

