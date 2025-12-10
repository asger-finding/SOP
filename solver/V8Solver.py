from z3 import *
import struct
from typing import List, Optional

class V8Solver:
	def __init__(self, sekvens: List[float], transform: float = 1.0, bits_tilgængelige: int = 53):
		self.state0, self.state1 = None, None
		self.intern_sekvens = sekvens[::-1]
		self.maske = 0xFFFFFFFFFFFFFFFF
		self.transform = transform
		self.bits_tilgængelige = bits_tilgængelige
		
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
			
			original_random = self.intern_sekvens[i] / self.transform
			mantisse = int(original_random * (1 << 53))
			
			shift_amount = 53 - self.bits_tilgængelige
			mantisse_masked = mantisse >> shift_amount
			state_masked = LShR(LShR(se_state0, 11), shift_amount)
			
			løser.add(mantisse_masked == state_masked)
		
		if løser.check() != sat:
			return None
		
		model = løser.model()
		self.state0 = model[t0_ref].as_long()
		self.state1 = model[t1_ref].as_long()
	
	def forudsig_næste(self) -> Optional[float]:
		if self.state0 is None or self.state1 is None:
			return None
		resultat = self.xorshift128p_baglæns()
		return ((resultat >> 11) / (2**53)) * self.transform
	
	def xorshift128p_baglæns(self):
		resultat = self.state0
		ps1 = self.state0
		ps0 = self.state1 ^ (self.state0 >> 26)
		ps0 = ps0 ^ self.state0
		ps0 = ps0 ^ (ps0 >> 17) ^ (ps0 >> 34) ^ (ps0 >> 51) & self.maske
		ps0 = (ps0 ^ (ps0 << 23) ^ (ps0 << 46)) & self.maske
		self.state0, self.state1 = ps0, ps1
		return resultat
