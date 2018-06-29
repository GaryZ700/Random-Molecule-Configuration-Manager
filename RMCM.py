#central file for the Random Molecule Configuration Manager

#import needed classes

#to parse atoms from coord file
from atomParser import atomParser
parser = atomParser()

#######################################################
#init global variables

#minimum distance that molecule can be placed towards certain atoms/molecules
atomBoundaries = {}

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
	print(numberOfAtoms)

	#init new variable to store centers
	finalCenter = []	

 	for centerPoint in center:
		#for each center point, divide by total number of atoms to find center point
		finalCenter.append( centerPoint / numberOfAtoms )

    return finalCenter

#######################################################
#start of main program code

#get list of all atoms in appropriate file, organized into specified structures
#0-19 = base quinoline, 21 -33 = water cluster, 34-36
masterAtoms = parser.all("coord", [21, 3, 3, 3, 3, 3, 3])

#iterate through structures in all atoms to get center of masses for all structures
for structure in range(len(masterAtoms)):
	
	#append center data to atom strucure dictionary
        masterAtoms[structure]["center"] = COCC(masterAtoms[structure]["coords"])	

print(masterAtoms)	
