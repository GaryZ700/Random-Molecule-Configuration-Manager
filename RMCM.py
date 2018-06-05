#central file for the Random Molecule Configuration Manager

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
#if coordinate exists in appropriate list, than that atom can not be spawned in that area
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




