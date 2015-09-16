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


class State(object):
	def __init__(self, orders=None):
		if orders is None:
			self.orders = {x: None for x in PEOPLE}
		else:
			self.orders = {o.name: o for o in orders}

	def goal(self):
		print "State:"
		print "\n".join(repr(self.orders[name]) for name in PEOPLE)
		print "======\n"

	@staticmethod
	def search():
		for pkg in permutation([], PACKAGES):
			for addr in permutation([], ADDRESSES):
				orders = [Order(*args) for args in zip(PEOPLE, addr, pkg)]
				s = State(orders)
				if s.goal():
					return s




def main():
	State.search()

if __name__ == '__main__':
	main()
