#central file for the Random Molecule Configuration Manager

#import needed classes

import math
import random
import os

#to parse atoms from coord file
from atomParser import atomParser
parser = atomParser()

#######################################################
#init global variables

#minimum distance that molecule can be placed towards certain atoms/molecules
atomBoundaries = [5, 5, 5]

#maximum distance away from origin of system that molecules can be placed 
systemBoundaries = [20,20,20]

#location of system origin
originLocation = []

#number of molecules to place
instances = 2

#areas where atoms can not be placed
#[x list, y list, z list]
#if coordinate exists in appropriate list, than that atom can not be placed in that area
takenAreas = [[],[],[]]

#######################################################
#function definitions

#function to parse settings from settings file
def parseSettings():
    
    #open settings file
    settings = file("settings", 'r')

    #get settings

#######################################################
#get origin of specific structure
#COCC = center of cartesian coordinates
#is passed list of atoms in standard data structure
def COCC(atoms):

    #init empty list for center point
    center = [ 0.0, 0.0, 0.0 ]    

    #iterate through all atom data
    for atom in atoms:
	#iterate through three dimensions
	for dim in range(3):
                         
	    center[dim] += atom[dim]

        	
	#get center point by dividing each dimension value by the number of atom in the structure
	numberOfAtoms = len(atoms)

	#init new variable to store centers
	finalCenter = []	

	#for each center point, divide by total number of atoms to find center point
 	for centerPoint in center:
		finalCenter.append( centerPoint / numberOfAtoms )

    return finalCenter

#######################################################
#create random xyz coordinates based upon starting point and boundries
def randCoord(center, boundaries):

	#create new boundries with respect to the center point
	centerBoundaries = [ (pow(-1, i)) * boundaries[int(math.floor(i/2))] + center[int(math.floor(i/2))] for i in range(6) ]

	#init array for random coords
	randCoord = []

	#create random coords within boundries for x, y, and z axis
        for dim in range(3):
		randCoord.append(random.uniform(centerBoundaries[dim+3], centerBoundaries[dim]))
	
	return randCoord	

#######################################################
#check if coords of molecule overlay another molecule within defined boundaries
def spawnCheck(coord, atomList, boundaries):

	#check all three dimensions
	for dim in range(3):
		#iterate through all atoms in list
		for atom in atomList:
			
			#check if coord is less than min values
			if( coord[dim] > (atom[dim] - boundaries[dim]) ):
				#if not, and coord is greater than min boundry, 
				#check if coord is greater than coresponding max coord value
				if(coord[dim] < (atom[dim] + boundaries[dim])):
					#if no, and coord falls into a no place location, then adjust coord value
					print("random coord places atom(s) on top of another, creating new coord now")
					print(coord[dim])	
	return coord 


#######################################################
#start of main program code

#get list of all atoms in appropriate file, organized into specified structures
#0-19 = base quinoline, 21 -33 = water cluster, 34-36
masterAtoms = parser.all("coord", [21, 3, 3, 3, 3])

#iterate through structures in all atoms to get center of masses for all structures
for structure in range(len(masterAtoms)):
	
	#append center data to atom strucure dictionary
        masterAtoms[structure]["center"] = COCC(masterAtoms[structure]["coords"])	


waterCluster = []

for waterClusterMolecule in range(4):
    waterCluster.append(masterAtoms[waterClusterMolecule + 1]["center"])


waterClusterCenter = COCC(waterCluster)


waterClusterCenter = [2,2,2]

#get coord of random water molecule to spawn in 
#and check if the molecule is being placed too close to another molecule
waterCoord = spawnCheck(randCoord(waterClusterCenter, systemBoundaries), waterCluster, atomBoundaries)

water = parser.all("water")

#write to coord file new location
parser.write("coord", water)

