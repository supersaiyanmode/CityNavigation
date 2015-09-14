import sys
from collections import defaultdict
from math import sin, cos, sqrt, atan2, radians

SPEED_LIMIT_DEFAULT = 40

class Meta(object):
	def __init__(self):
		self.pathCost = 0
		self.cities = []
		self.totalTime = 0
		self.totalDistance = 0
		self.heurisiticValue = 0
	
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
		city1 = self.cityStore.cities.setdefault(cityName1, City(cityName1, None, None))
		city2 = self.cityStore.cities.setdefault(cityName2, City(cityName2, None, None))
		return Highway(city1, city2, int(length), int(speedLimit or '0') or SPEED_LIMIT_DEFAULT, name)
	
	def getOutwardHighways(self, city1, sortKey):
		return sorted(self.outwardHighways[city1], key=sortKey)
	
	def maxSpeed(self):
		return max(x.speedLimit for x in self.highways.itervalues())

class BFSSearch(object):
	def search(self, node, successorFn, pathCostFn, sortKey, goalFn, heuristic=None):
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
				m.pathCost = meta.pathCost + pathCostFn(highway)
				m.totalTime = meta.totalTime + highway.time
				m.totalDistance = meta.totalDistance + highway.length
				m.cities = meta.cities + [nextCity]
				fringe.append((nextCity, m))

		
class DFSSearch(object):
	def search(self, node, successorFn, pathCostFn, sortKey, goalFn, heuristic=None):
		m=Meta()
		m.cities=[node]
		fringe = [(node,m)]

		while fringe:
			curCity, meta = fringe.pop(0)
			if goalFn(curCity):
				return curCity, meta
			print meta
			outwardHighways = successorFn(curCity, sortKey)
			for highway in outwardHighways : 	
				nextCity = highway.city2
				m = Meta();
				m.pathCost = meta.pathCost + pathCostFn(highway)
				m.totalTime = meta.totalTime + highway.time
                                m.totalDistance = meta.totalDistance + highway.length
                                m.cities = meta.cities + [nextCity]

				fringe.insert(0,(nextCity, m))

class AStarSearch(object):
	def search(self, node, successorFn, pathCostFn, sortKey, goalFn, heuristicFn):
		m = Meta()
		m.cities = [node]
		fringe = [(node, m)]

		while fringe:
			obj = min(fringe, key=lambda x: x[1].heurisiticValue + x[1].pathCost)
			fringe.remove(obj)
			curCity, meta = obj
			print "Current meta:", meta

			if goalFn(curCity):
				return curCity, meta

			outwardHighways = successorFn(curCity, sortKey)
			for highway in outwardHighways:
				nextCity = highway.city2
				m = Meta()
				m.pathCost = meta.pathCost + pathCostFn(highway)
				m.totalTime = meta.totalTime + highway.time
				m.totalDistance = meta.totalDistance + highway.length
				m.cities = meta.cities + [nextCity]
				try:
					m.heurisiticValue = heuristicFn(nextCity)
				except:
					import pdb; pdb.set_trace()
				fringe.append((nextCity, m))

def curvedDistance(lat1, long1, lat2, long2):
	"""
	Author: Michael0x2a (http://stackoverflow.com/users/646543/michael0x2a)
	The function below was found on StackOverflow: http://stackoverflow.com/a/19412565/227884
	"""
	R = 3959.0

	lat1 = radians(lat1)
	lon1 = radians(long1)
	lat2 = radians(lat2)
	lon2 = radians(long2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	return  R * c

def populateLatLongForCity(highwayStore, cityStore, city, seenCities=None):
	if seenCities is None:
		seenCities = []
	connectedCities = [h.city2 for h in highwayStore.getOutwardHighways(city, lambda x: 1)]
	emptyCities = filter(lambda x: x.latitude is None, connectedCities)
	nonEmptyCities = filter(lambda x: x.latitude is not None, connectedCities)
	if nonEmptyCities:
		city.latitude = sum(x.latitude for x in nonEmptyCities)/float(len(nonEmptyCities))
		city.longitude = sum(x.longitude for x in nonEmptyCities)/float(len(nonEmptyCities))
		print "Populating approx coordinates for City: ", city
		return
	
	emptyNonSeenCities = filter(lambda x: x not in seenCities, emptyCities)
	for city in emptyNonSeenCities:
		populateLatLongForCity(highwayStore, cityStore, city, seenCities + [city])


def populateLatLong(highwayStore, cityStore):
	for city in cityStore.cities.itervalues():
		if city.latitude is None and city.longitude is None:
			populateLatLongForCity(highwayStore, cityStore, city)
			print "-"*25
	raw_input()



def main():
	with open("city-gps.txt") as f:
		cityStore = CityStore(f)
	
	with open("road-segments.txt") as f:
		highwayStore = HighwayStore(f, cityStore)
	
	populateLatLong(highwayStore, cityStore)
	
	startCity = cityStore.cities[sys.argv[1]]
	endCity = cityStore.cities[sys.argv[2]]
	routingOption = sys.argv[3]
	routingAlgo = sys.argv[4]

	searches = {"bfs": BFSSearch, "dfs": DFSSearch, "astar": AStarSearch}

	cityDistToGoal = lambda city: curvedDistance(city.latitude, city.longitude, endCity.latitude, endCity.longitude)


	options = {
		"segments": {
			"pathCostFn": lambda highway: 1,
			"sortKey": lambda highway: -highway.length,
			"heuristicFn": lambda city: 1, #Dummy
		},
		"time": {
			"pathCostFn": lambda highway: highway.time,
			"sortKey": lambda highway: highway.time,
			"heuristicFn": lambda city: cityDistToGoal(city) / highwayStore.maxSpeed()
		},
		"distance": {
			"pathCostFn": lambda highway: highway.length,
			"sortKey": lambda highway: highway.length,
			"heuristicFn": lambda city:	cityDistToGoal(city)
		}
	}
	curOptions = options[routingOption]
	
	search = searches[routingAlgo]().search
	goal, meta = search(node=startCity, 
						successorFn=highwayStore.getOutwardHighways,
						goalFn=lambda x: x.name == endCity.name,
						**curOptions)

	print meta	

if __name__ == '__main__':
	main()
