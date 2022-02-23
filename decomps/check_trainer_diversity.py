import os
import numpy as np

# gets the number of times each species is found in the trainer_parties.h file

with open('../../include/constants/species.h') as f:
	lines = f.readlines()

start = 0
names=[]
index = 0
for line in lines:
	if 'SPECIES_EGG' in line:
		NUM_SPECIES = int(line.split(' ')[-1].lstrip())
		break
	if start and 'SPECIES' in line:
		line = line.replace('#define ','').split(' ')
		names.append(line[0])
		index += 1
	if 'SPECIES_NONE' in line:
		start=1

f.close()
#print(NUM_SPECIES)
counts = np.zeros(NUM_SPECIES)
with open('../../src/data/trainer_parties.h') as f:
	lines = f.readlines()

for line in lines:
	if 'species' in line:
		line = line.replace('.species = ','').replace(',\n','').lstrip()
		
		if line in names:
			counts[names.index(line) + 1] += 1

results=''
for idx in range(NUM_SPECIES-1):
	results += names[idx] + ': ' + str(int(counts[idx + 1])) + '\n'
			
print(results)

