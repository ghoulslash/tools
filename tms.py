inp = input("Enter TM list in matrix form: ").split(' ')	#list of numbers separated by space

tms = [0] * 128		#base bitfield

#get TM data into bitfields
for i in range(len(inp)):
	ind = int(inp[i]) - 1
	tms[ind] = 1

first_word = list(reversed(tms[0:32]))
second_word = list(reversed(tms[32:64]))
third_word = list(reversed(tms[64:96]))
fourth_word = list(reversed(tms[96:128]))

#convert lists to binary strings
tms32 = ''
tms64 = ''
tms96 = ''
tms128 = ''
for i in first_word:
	tms32 += str(i)
for i in second_word:
	tms64 += str(i)
for i in third_word:
	tms96 += str(i)
for i in fourth_word:
	tms128 += str(i)
	
#get big endian hex values	
hex32_fwd = '{:0{}X}'.format(int(tms32, 2), len(tms32) // 4)
hex64_fwd = '{:0{}X}'.format(int(tms64, 2), len(tms64) // 4)
hex96_fwd = '{:0{}X}'.format(int(tms96, 2), len(tms96) // 4)
hex128_fwd = '{:0{}X}'.format(int(tms128, 2), len(tms128) // 4)

#transform into little endian hex
hex32 = ''
hex64 = ''
hex96 = ''
hex128 = ''

for i in range(0,8):
	if i % 2 == 1:	#odd num
		x = 8 - i		#odd index
	else:
		x = 6 - i		#even index

	hex32 += str(list(hex32_fwd)[x])
	hex64 += str(list(hex64_fwd)[x])
	hex96 += str(list(hex96_fwd)[x])
	hex128 += str(list(hex128_fwd)[x])	
	
print(hex32 + hex64 + hex96 + hex128)	

