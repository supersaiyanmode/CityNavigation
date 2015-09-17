import sys


PEOPLE = "Frank George Heather Irene Jerry".split()
PACKAGES = "Amplifier Banister Candelabrum Doorknob Elephant".split()
ADDRESSES = "Kirkwood_Street Lake_Avenue Maxwell_Street North_Avenue Orange_Drive".split()

def permutation(fixed, available):
	if not available:
		return [fixed]
	result = [] 
	for item in available:
		remaining = available[:]
		remaining.remove(item)
		result.extend(permutation(fixed + [item], remaining))
	return result

class Order(object):
	def __init__(self, name, address, package):
		self.name = name
		self.address = address
		self.package = package
	
	def __repr__(self):
		return "<%s %s (%s)>"%(self.package, self.name, self.address)

class Unknown(object):
	pass
UNKNOWN = Unknown()
	
class PartialOrder(Order):
	
	def __init__(self, name=UNKNOWN, address=UNKNOWN, package=UNKNOWN):
		super(PartialOrder, self).__init__( name, address, package)
		
	def canOverlap(self, other):
		match = unknownMatch = mismatch = 0
		for attrName in "name address package".split():
			attr1 = getattr(self, attrName)
			attr2 = getattr(other, attrName)
			if attr1 is not UNKNOWN and attr1 == attr2:
				match += 1
			elif (attr1 is UNKNOWN and attr2 is not UNKNOWN) or \
					(attr2 is UNKNOWN and attr1 is not UNKNOWN) or \
					(attr1 is UNKNOWN and attr2 is UNKNOWN):
				unknownMatch += 1
			elif attr1 is not UNKNOWN and attr2 is not UNKNOWN and attr1 != attr2:
				mismatch += 1
		if match > 0 and mismatch > 0:
			return -1
		if match == 0 and mismatch > 0:
			return 0
		if match > 0 and mismatch == 0:
			return 1
			
			

class State(object):
	def __init__(self, orders=None):
		if orders is None:
			self.orders = {x: None for x in PEOPLE}
		else:
			self.orders = {o.name: o for o in orders}

	def get(self, name=None, address=None, package=None):
		return State.applyConditions(self.orders, name, address, package)
		
	@staticmethod
	def applyConditions(orders, name=None, address=None, package=None):
		def condition(order):
			if name is not None and order.name != name:
				return False
			if address is not None and order.address != address:
				return False
			if package is not None and order.package != package:
				return False
			return True

		return filter(condition, orders.values())

	def goal(self):
		name1 = self.get(package="Candelabrum")[0].name
		name2 = self.get(package="Banister")[0].name
		name3 = self.get(package="Elephant")[0].name
		product1 = self.get(name="Irene")[0].package
		product2 = self.get(name="George")[0].package
		product3 = self.get(address="Kirkwood_Street")[0].package
		product4 = self.get(address="Orange_Drive")[0].package
		product5 = self.get(name="Heather")[0].package
		product6 = self.get(address="Maxwell_Street")[0].package

		
		if self.get(name=name1, package="Banister"):
			return False
		if self.get(name=name2, package=product1):
			return False
		if self.get(name="Frank", package="Doorknob"):
			return False
		if self.get(package=product2, address="Kirkwood_Street"):
			return False
		if self.get(package=product3, address="Lake_Avenue"):
			return False
		if self.get(name="Heather", package=product4):
			return False
		if self.get(name="Jerry", package=product5):
			return False
		if self.get(package="Elephant", address="North_Avenue"):
			return False
		if self.get(name=name3, package=product6):
			return False
		if self.get(package="Amplifier", address="Maxwell_Street"):
			return False
		
		#Condition1
		item1 = self.get(address="Orange_Drive")[0].package #Heather received this item1!
		if item1 == "Elephant":
			if not self.get(name="Heather", address="North_Avenue"):
				return False
		elif item1 == "Amplifier":
			if not self.get(name="Heather", address="Maxwell_Street"):
				return False

		#Condition2
		if (self.get(package="Doorknob")[0].name == 'Irene' and #If Irene ordered doorknob & was recd by one who
				self.get(package="Banister")[0].name != 'Frank'): #ordered Banister, then the latter can't be Frank because he recd doorknob
			return False
		if self.get(package="Elephant")[0].name == 'Irene' and self.get(package="Banister")[0].address != 'North_Avenue':
			return False
		if self.get(package="Amplifier")[0].name == 'Irene' and self.get(package="Banister")[0].address != 'Maxwell_Street':
			return False
		
		#Condition3: Partial Orders and overlap! :)
		partialOrders = [
			PartialOrder(name=name1, package="Banister"),
			PartialOrder(name=name2, package=product1),
			PartialOrder(name="Frank", package="Doorknob"),
			PartialOrder(package=product2, address="Kirkwood_Street"),
			PartialOrder(package=product3, address="Lake_Avenue"),
			PartialOrder(name="Heather", package=product4),
			PartialOrder(name="Jerry", package=product5),
			PartialOrder(package="Elephant", address="North_Avenue"),
			PartialOrder(name=name3, package=product6),
			PartialOrder(package="Amplifier", address="Maxwell_Street")
		]
		
		for x in partialOrders:
			for y in partialOrders:
				if x.canOverlap(y) == -1:
					return False
		return True

	@staticmethod
	def search():
		for pkg in permutation([], PACKAGES):
			for addr in permutation([], ADDRESSES):
				orders = [Order(*args) for args in zip(PEOPLE, addr, pkg)]
				s = State(orders)
				if s.goal():
					yield s




def main():
	solutions = list(State.search())
	if len(solutions) != 1:
		print>>sys.stderr, "More than one solutions possible! :("
		return
	print " ---  Solution  ---"
	print "\n".join("%15s|%15s|%15s"%(x.name, x.package, x.address) for x in solutions[0].orders.values())

if __name__ == '__main__':
	main()
