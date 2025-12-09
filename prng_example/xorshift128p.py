def xorshift128plus(state0, state1):
	# Python har ikke 64 bit begrænsning på tal,
	# så vi maskerer
	MASK_64 = (1 << 64) - 1
	
	print("xorshift128+")
	print(f"Initial state0: {state0:#018x} (base-10: {state0})")
	print(f"Initial state1: {state1:#018x} (base-10: {state1})")
	print()
	
	s1 = state0
	print(f"Trin 1: s1 = state0")
	print(f"        s1 = {s1:#018x}")
	print()
	
	s0 = state1
	print(f"Trin 2: s0 = state1")
	print(f"        s0 = {s0:#018x}")
	print()
	
	state0 = s0
	print(f"Trin 3: state0 = s0")
	print(f"        state0 = {state0:#018x}")
	print()
	
	shifted = (s1 << 23) & MASK_64
	s1 = s1 ^ shifted
	s1 &= MASK_64
	print(f"Trin 4: s1 ^= s1 << 23")
	print(f"        s1 << 23 = {shifted:#018x}")
	print(f"        s1 (new) = {s1:#018x}")
	print()
	
	shifted = s1 >> 17
	s1 = s1 ^ shifted
	s1 &= MASK_64
	print(f"Trin 5: s1 ^= s1 >> 17")
	print(f"        s1 >> 17 = {shifted:#018x}")
	print(f"        s1 (new) = {s1:#018x}")
	print()
	
	s1 = s1 ^ s0
	s1 &= MASK_64
	print(f"Trin 6: s1 ^= s0")
	print(f"        s0       = {s0:#018x}")
	print(f"        s1 (new) = {s1:#018x}")
	print()
	
	shifted = s0 >> 26
	s1 = s1 ^ shifted
	s1 &= MASK_64
	print(f"Trin 7: s1 ^= s0 >> 26")
	print(f"        s0 >> 26 = {shifted:#018x}")
	print(f"        s1 (new) = {s1:#018x}")
	print()
	
	state1 = s1
	print(f"Trin 8: state1 = s1")
	print(f"        state1 = {state1:#018x}")
	print()
	
	output = (s0 + s1) & MASK_64
	print(f"Trin 9: output = s0 + s1")
	print(f"        s0     = {s0:#018x}")
	print(f"        s1     = {s1:#018x}")
	print(f"        output = {output:#018x} (base-10: {output})")
	print()
	
	print(f"Endelig state0: {state0:#018x}")
	print(f"Endelig state1: {state1:#018x}")
	print(f"Output:         {output:#018x}")
	print("\n")
	
	return output, state0, state1


# Kørsel med simple state-værdier
print("Simple startværdier\n")
output1, new_state0_1, new_state1_1 = xorshift128plus(
	state0=0x0000000000000001,
	state1=0x0000000000000002
)

print("\n\n")

# Kørsel med store state-værdier
print("Større startværdier\n")
output2, new_state0_2, new_state1_2 = xorshift128plus(
	state0=0xBADA55B00B1E5101,
	state1=0xC0FFEE1CEC0FFEE5
)

print("\n\n")

# Kørsel med flere iterationer
iterations = 30
print(f"{iterations} iterationer\n")
state0 = 0x0000000000000001
state1 = 0x0000000000000002

for iteration in range(iterations):
	print(f"\n{'='*50}")
	print(f"Iteration {iteration + 1}")
	print(f"{'='*50}\n")
	output, state0, state1 = xorshift128plus(state0, state1)
