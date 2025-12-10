from z3 import *
import struct
from typing import List, Optional

class SpiderMonkeySolver:
	def __init__(self, sekvens: List[float]):
		self.state0, self.state1 = None, None
		self.intern_sekvens = sekvens
		self.maske = 0xFFFFFFFFFFFFFFFF
		
		se_state0, se_state1 = BitVecs("se_state0 se_state1", 64)
		t0_ref, t1_ref = se_state0, se_state1
		
		løser = Solver()
		
		for i in range(len(self.intern_sekvens)):
			se_s1 = se_state0
			se_s0 = se_state1
			se_state0 = se_s0
			se_s1 ^= se_s1 << 23
			se_s1 ^= LShR(se_s1, 17)
			se_s1 ^= se_s0
			se_s1 ^= LShR(se_s0, 26)
			se_state1 = se_s1
			
			mantisse = int(self.intern_sekvens[i] * (1 << 53))
			
			løser.add(
				int(mantisse) == ((se_state0 + se_state1) & 0x1FFFFFFFFFFFFF)
			)
		
		if løser.check() != sat:
			return None
		
		model = løser.model()
		self.state0 = model[t0_ref].as_long()
		self.state1 = model[t1_ref].as_long()
		
		for i in range(len(self.intern_sekvens)):
			self.xorshift128p()
	
	def forudsig_næste(self) -> Optional[float]:
		if self.state0 is None or self.state1 is None:
			return None
		
		resultat = self.xorshift128p()
		return float(resultat & 0x1FFFFFFFFFFFFF) / (1 << 53)
	
	def xorshift128p(self) -> int:
		s1 = self.state0 & self.maske
		s0 = self.state1 & self.maske
		self.state0 = s0
		s1 ^= (s1 << 23) & self.maske
		s1 ^= (s1 >> 17) & self.maske
		s1 ^= s0 & self.maske
		s1 ^= (s0 >> 26) & self.maske
		self.state1 = s1 & self.maske
		return (self.state0 + self.state1) & self.maske
