import sys
from collections import defaultdict


SPEED_LIMIT_DEFAULT = 40

class Meta(object):
	def __init__(self):
		self.pathCost = 0
		
class City(object):
	def __init__(self, name, latitude, longitude):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude
	

class Highway(object):
	def __init__(self, city1, city2, length, speedLimit, name):
		self.city1 = city1
		self.city2 = city2
		self.length = length
		self.speedLimit = speedLimit
		self.time = length / speedLimit
		self.name = name

class CityStore(object):
	def __init__(self, f):
		cities = {}
		for line in f:
			if not line.strip():
				continue
			cityObj = self.parseCity(line.rstrip())
			cities[cityObj.name] = cityObj
		self.cities = cities

	def parseCity(self, line):
		name, lat, lon = line.strip().split()
		return City(name, float(lat), float(lon))

class HighwayStore(object):
	def __init__(self, f):
		highways = {}
		connectedCities = defaultdict(list)
		for line in f:
			if not line.strip():
				continue
			highwayObj = self.parseHighway(line.rstrip())
			highways[(highwayObj.city1, highwayObj.city2)] = highwayObj
			highways[(highwayObj.city2, highwayObj.city1)] = highwayObj
			connectedCities[highwayObj.city1].append(highwayObj.city2)
			connectedCities[highwayObj.city2].append(highwayObj.city1)
		self.highways = highways
		self.connectedCities = connectedCities

	def parseHighway(self, line):
		city1, city2, length, speedLimit, name = line.strip().split(" ")
		return Highway(city1, city2, int(length), int(speedLimit or '0') or SPEED_LIMIT_DEFAULT, name)
	
	
	def getConnectedCities(self, city1, sortKey):
		return sorted(self.connectedCities[city1], key=sortKey)

class BFSSearch(object):
	def search(self, node, successorFn, pathCostFn, sortKey, goalFn):
		fringe = [(node, Meta())]

		while fringe:
			curCity, meta = fringe.pop(0)
			if goalFn(curCity):
				return curCity, meta
			connectedCities = successorFn(node, sortKey)
			for nextCity in connectedCities:
				m = Meta();
				m.pathCost = meta.pathCost + pathCostFn(curCity, nextCity)
				fringe.append((nextCity, m))

		
class DFSSearch(object):
	def search(self, node, successorFn, pathCostFn, sortKey, goalFn):
		fringe = [(node,Meta())]

		while fringe:
			curCity, meta = fringe.pop(0)
			if goalFn(curCity):
				return curCity, meta
			connectedCities = successorFn(node, sortKey)
			for nextCity in connectedCities
				m = Meta();
				m.pathCost = meta.pathCost + pathCostFn(curCity, nextCity)
				fringe.insert((nextcity, m))

class AStarSearch(object):
	pass


def main():
	with open("city-gps.txt") as f:
		cityStore = CityStore(f)
	
	with open("road-segments.txt") as f:
		highwayStore = HighwayStore(f)
	
	startCity = sys.argv[1]
	endCity = sys.argv[2]
	routingOption = sys.argv[3]
	routingAlgo = sys.argv[4]


	searches = {"bfs": BFSSearch, "dfs": DFSSearch, "astar": AStarSearch}
	search = searches[routingAlgo]().search
	res = search(startCity, highwayStore.getConnectedCities, lambda x,y : 1,
					lambda element: element.time, 
					lambda x: x.name == endCity)
	
	

if __name__ == '__main__':
	main()
