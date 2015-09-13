import sys


SPEED_LIMIT_DEFAULT = 40

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
		for line in f:
			if not line.strip():
				continue
			highwayObj = self.parseHighway(line.rstrip())
			highways[(highwayObj.city1, highwayObj.city2)] = highwayObj
		self.highways = highways

	def parseHighway(self, line):
		city1, city2, length, speedLimit, name = line.strip().split(" ")
		return Highway(city1, city2, int(length), int(speedLimit or SPEED_LIMIT_DEFAULT), name)
	
def main():
	with open("city-gps.txt") as f:
		cityStore = CityStore(f)
	
	with open("road-segments.txt") as f:
		highwayStore = HighwayStore(f)
	


if __name__ == '__main__':
	main()
