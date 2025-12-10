from z3 import *
import struct
from typing import List, Optional

class SpiderMonkeySolver:
	def __init__(self, sekvens: List[float]):
		self.sekvens = sekvens
		self.maske = 0xFFFFFFFFFFFFFFFF
		self.tilstand0, self.tilstand1 = None, None
		
		se_tilstand0, se_tilstand1 = BitVecs("se_tilstand0 se_tilstand1", 64)
		t0_ref, t1_ref = se_tilstand0, se_tilstand1
		
		løser = Solver()
		
		for i in range(len(sekvens)):
			se_s1 = se_tilstand0
			se_s0 = se_tilstand1
			se_tilstand0 = se_s0
			se_s1 ^= se_s1 << 23
			se_s1 ^= LShR(se_s1, 17)
			se_s1 ^= se_s0
			se_s1 ^= LShR(se_s0, 26)
			se_tilstand1 = se_s1
			
			mantisse = int(sekvens[i] * (1 << 53))
			
			løser.add(
				int(mantisse) == ((se_tilstand0 + se_tilstand1) & 0x1FFFFFFFFFFFFF)
			)
		
		if løser.check() != sat:
			return None
		
		model = løser.model()
		self.tilstand0 = model[t0_ref].as_long()
		self.tilstand1 = model[t1_ref].as_long()
		
		for i in range(len(sekvens)):
			self.xorshift128p()
	
	def forudsig_næste(self) -> Optional[float]:
		if self.tilstand0 is None or self.tilstand1 is None:
			return None
		
		resultat = self.xorshift128p()
		return float(resultat & 0x1FFFFFFFFFFFFF) / (1 << 53)
	
	def xorshift128p(self) -> int:
		s1 = self.tilstand0 & self.maske
		s0 = self.tilstand1 & self.maske
		self.tilstand0 = s0
		s1 ^= (s1 << 23) & self.maske
		s1 ^= (s1 >> 17) & self.maske
		s1 ^= s0 & self.maske
		s1 ^= (s0 >> 26) & self.maske
		self.tilstand1 = s1 & self.maske
		return (self.tilstand0 + self.tilstand1) & self.maske
