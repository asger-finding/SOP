"""
USAGE

1. Installer z3: pip install z3-solver

2. I din browser, åben et konsolvindue (Developer Tools)
   og indtast og submit: copy(Array.from({ length: 5 }, Math.random).join(","));
   Det er fem værdier vi anvender til forudsigelsen

3. Passer værdierne til dette script:
   $ python xorshift128pSolver.py <tal1,tal2,tal3,...> [engine=v8|spidermonkey] [transform=1.0] [bits=53]

Hvis vi har en successfuld løsning, printes værdierne i et array.
"""

import sys
from z3 import *

from V8Solver import V8Solver
from SpiderMonkeySolver import SpiderMonkeySolver

RANDOM_NUMBERS_TO_GENERATE = 10

def main():
	if len(sys.argv) < 2:
		print("Brug: python xorshift128pSolver.py <tal1,tal2,tal3,...> [engine=v8|spidermonkey] [transform=1.0] [bits=53]")
		sys.exit(1)

	tal_input = sys.argv[1]
	
	# Parse optional parameters
	engine = "v8"
	transform = 1.0
	bits = 53
	
	for arg in sys.argv[2:]:
		if arg.startswith("engine="):
			engine = arg.split("=", 1)[1]
		elif arg.startswith("transform="):
			try:
				transform = float(arg.split("=", 1)[1])
			except ValueError:
				print("Fejl: transform skal være et gyldigt decimaltal")
				sys.exit(1)
		elif arg.startswith("bits="):
			try:
				bits = int(arg.split("=", 1)[1])
			except ValueError:
				print("Fejl: bits skal være et gyldigt heltal")
				sys.exit(1)
	
	try:
		sekvens = [float(x.strip()) for x in tal_input.split(',')]
	except ValueError:
		print("Fejl: Alle inputværdier skal være gyldige decimaltal adskilt af kommaer.")
		sys.exit(1)

	print("Sekvens: %s" % sekvens)
	print("Browser Engine: %s" % engine)
	print("Transform: %s" % transform)
	print("Bits: %s" % bits)

	if engine == "v8":
		forudsiger = V8Solver(sekvens, transform, bits)
	elif engine == "spidermonkey":
		forudsiger = SpiderMonkeySolver(sekvens)
	else:
		print(f"Fejl: Ukendt engine \"{engine}\". Skal være \"v8\" eller \"spidermonkey\"")
		sys.exit(1)
	
	fremtidige_tal = []
	for _ in range(RANDOM_NUMBERS_TO_GENERATE):
		next = forudsiger.forudsig_næste()
		fremtidige_tal.append(next)
	
	if None in fremtidige_tal:
		print("Kunne ikke forudsige sekvens")
		sys.exit(0)
	
	print("\nForudsagte tal:")
	print(fremtidige_tal)

if __name__ == "__main__":
	main()
