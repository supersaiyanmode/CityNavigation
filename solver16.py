import sys
from copy import deepcopy
from itertools import chain
from heapq import heappush, heappop
from Queue import PriorityQueue

class State(object):
	DIR_LEFT = 'L'
	DIR_UP = 'U'
	DIR_RIGHT = 'R'
	DIR_DOWN = 'D'

	GOAL = [
		[1, 2, 3, 4],
		[5, 6, 7, 8],
		[9, 10, 11, 12],
		[13, 14, 15, 16]
	]

	def __init__(self, arr, depth=0, prevState=None, movement=None):
		self.array = [list(row) for row in arr]
		self.prevState = prevState
		self.movement = '' if movement is None else movement
		self.depth = depth
		self.heurisitic = self.heurisitic2
	
	def moveLeft(self, rowNum):
		arr = State.moveLeftArr(self.array, rowNum)
		return State(arr, self.depth + 1, self, self.movement + 'L%d'%(rowNum+1))
	
	def moveRight(self, rowNum):
		arr = State.moveRightArr(self.array, rowNum)
		return State(arr, self.depth + 1, self, self.movement + 'R%d'%(rowNum+1))

	def moveUp(self, colNum):
		arr = deepcopy(self.array)
		arr = zip(*State.moveLeftArr(zip(*arr), colNum))
		return State(arr, self.depth + 1, self, self.movement + 'U%d'%(colNum+1))
	
	def moveDown(self, colNum):
		arr = deepcopy(self.array)
		arr = zip(*State.moveRightArr(zip(*arr), colNum))
		return State(arr, self.depth + 1, self, self.movement + 'D%d'%(colNum+1))

	def isGoal(self):
		return self.array == self.GOAL
	
	def heurisitic1(self):
		return sum(State.manhattanRound(self.array, self.GOAL, num) for num in range(1,17))
	
	def heurisitic2(self):
		return max(State.manhattanRound(self.array, self.GOAL, num) for num in range(1,17))

	def heurisitic3(self):
		return len([x for x,y in zip(chain(*self.GOAL), chain(*self.array)) if x != y])
	
	def heurisitic4(self):
		return 0
	
	def heurisitic5(self):
		zipped = [[x==y for x,y in zip(row1, row2)] for row1, row2 in zip(self.array, self.GOAL)]
		goodRows = sum([1 if all(x for x in row) else 0 for row in zipped])
		goodCols = sum([1 if all(x for x in row) else 0 for row in zip(*zipped)])
		return 8 - goodRows - goodCols
		
	def f(self):
		return self.depth + self.heurisitic()
	
	def to_tuple(self):
		return tuple(tuple(y for y in x) for x in self.array)

	@staticmethod
	def moveLeftArr(array, rowNum):
		arr = deepcopy(array)
		arr[rowNum] = (array[rowNum] * 2)[1:5]
		return arr

	@staticmethod
	def moveRightArr(array, rowNum):
		arr = deepcopy(array)
		arr[rowNum] = (array[rowNum] * 2)[3:7]
		return arr


	@staticmethod
	def manhattanRound(arr, goal, num):
		goalRow, goalCol = State.getPos(goal, num)
		curRow, curCol = State.getPos(arr, num)

		rowDiff = abs(goalRow - curRow)
		rowDiff = min(rowDiff, len(arr) - rowDiff)

		colDiff = abs(goalCol - curCol)
		colDiff = min(colDiff, len(arr[0]) - colDiff)

		return rowDiff + colDiff

	@classmethod
	def getPos(cls, arr, num):
		for rowNum, row in enumerate(arr):
			for colNum, cell in enumerate(row):
				if cell == num:
					return rowNum, colNum
		return None
 
 	def __str__(self):
		return ("\n".join(" ".join(str(x) for x in row) for row in self.array) + 
			"\nHeuristic Value: " + str(self.heurisitic()) + ", depth: " + str(self.depth) +
			"\nPath: " + self.movement)

def astar(state):
	queue = PriorityQueue()
        queue.put((0, state))
        [state]

	seen = set()
	while queue:
		score, best = queue.get()

		print "Currently Evaluating: "
		print best
		print "Number of nodes:", len(seen)
		print ""
		#raw_input()
		if best.isGoal():
			return best
		seen.add(best.to_tuple())

		for pos in range(4):
			left = best.moveLeft(pos)
			if left.to_tuple() not in seen:
				queue.put((left.f(), left))

			right = best.moveRight(pos)
			if right.to_tuple() not in seen:
				queue.put((right.f(), right))

			up = best.moveUp(pos)
			if up.to_tuple() not in seen:
				queue.put((up.f(), up))

			down = best.moveDown(pos)	
			if down.to_tuple() not in seen:
				queue.put((down.f(), down))

def main():
	with open(sys.argv[1]) as f:
		inputArr = [map(int, line.rstrip().split()) for line in f]
	
	s = State(inputArr)
	result = astar(s)
	print result

if __name__ == '__main__':
	main()

