import sys
from collections import defaultdict


SPEED_LIMIT_DEFAULT = 40

class Meta(object):
	def __init__(self):
		self.pathCost = 0
		self.cities = []
		self.totalTime = 0
		self.totalDistance = 0
	
	def __repr__(self):
		return "%d %f"%(self.totalDistance, self.totalTime) + " " +  " => ".join(x.name for x in self.cities)
	
class City(object):
	def __init__(self, name, latitude=None, longitude=None):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude
		self.empty = (not latitude) and (not longitude)
			
	def __eq__(self, other):
		return self.name == other.name

	def __hash__(self):
		return hash(self.name)
	
	def __repr__(self):
		return "<City: '%s' (%f, %f)>"%(self.name, self.latitude, self.longitude)
	
class Highway(object):
	def __init__(self, city1, city2, length, speedLimit, name):
		self.city1 = city1
		self.city2 = city2
		self.length = length
		self.speedLimit = speedLimit
		self.time = length / float(speedLimit)
		self.name = name
	
	def __repr__(self):
		return "<Highway: '%s' %s => %s>"%(self.name, repr(self.city1), repr(self.city2))

class CityStore(object):
	def __init__(self, f):
		cities = defaultdict(lambda : City("NONE"))
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
	def __init__(self, f, cityStore):
		self.cityStore = cityStore
		highways = {}
		outwardHighways = defaultdict(list)
		for line in f:
			if not line.strip():
				continue
			highwayObj1 = self.parseHighway(line.rstrip())
			highwayObj2 = self.parseHighway(line.rstrip())
			highwayObj2.city1, highwayObj2.city2 = highwayObj2.city2, highwayObj2.city1
			highways[(highwayObj1.city1, highwayObj1.city2)] = highwayObj1
			highways[(highwayObj2.city2, highwayObj2.city1)] = highwayObj2
			outwardHighways[highwayObj1.city1].append(highwayObj1)
			outwardHighways[highwayObj2.city1].append(highwayObj2)
		self.highways = highways
		self.outwardHighways = outwardHighways

	def parseHighway(self, line):
		cityName1, cityName2, length, speedLimit, name = line.strip().split(" ")
		city1 = self.cityStore.cities[cityName1]
		city2 = self.cityStore.cities[cityName2]
		return Highway(city1, city2, int(length), int(speedLimit or '0') or SPEED_LIMIT_DEFAULT, name)
	
	def getOutwardHighways(self, city1, sortKey):
		return sorted(self.outwardHighways[city1], key=sortKey)

class BFSSearch(object):
	def search(self, node, successorFn, pathCostFn, sortKey, goalFn):
		m = Meta()
		m.cities = [node]
		fringe = [(node, m)]

		while fringe:
			curCity, meta = fringe.pop(0)
			print "Current Meta:", meta

			if goalFn(curCity):
				return curCity, meta
			outwardHighways = successorFn(curCity, sortKey)
			for highway in outwardHighways:
				nextCity = highway.city2
				m = Meta()
				m.pathCost = meta.pathCost + pathCostFn(curCity, nextCity)
				m.totalTime = meta.totalTime + highway.time
				m.totalDistance = meta.totalDistance + highway.length
				m.cities = meta.cities + [nextCity]
				fringe.append((nextCity, m))

		
class DFSSearch(object):
	def search(self, node, successorFn, pathCostFn, sortKey, goalFn):
		fringe = [(node,Meta())]

		while fringe:
			curCity, meta = fringe.pop(0)
			if goalFn(curCity):
				return curCity, meta
				m = Meta();
				nextCity = cityFn(nextCityName)
				m.pathCost = meta.pathCost + pathCostFn(curCity, nextCity)
				fringe.insert((nextcity, m))

class AStarSearch(object):
	pass


def main():
	with open("city-gps.txt") as f:
		cityStore = CityStore(f)
	
	with open("road-segments.txt") as f:
		highwayStore = HighwayStore(f, cityStore)
	
	startCity = sys.argv[1]
	endCity = sys.argv[2]
	routingOption = sys.argv[3]
	routingAlgo = sys.argv[4]


	searches = {"bfs": BFSSearch, "dfs": DFSSearch, "astar": AStarSearch}
	search = searches[routingAlgo]().search
	goal, meta = search(cityStore.cities[startCity], highwayStore.getOutwardHighways, lambda x,y : 1,
					lambda element: element.time, 
					lambda x: x.name == endCity)

	print meta	

if __name__ == '__main__':
	main()
