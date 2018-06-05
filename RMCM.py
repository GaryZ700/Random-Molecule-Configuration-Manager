#central file for the Random Molecule Configuration Manager

#######################################################
#init global variables

#minimum distance that molecule can be placed towards certain atoms/molecules
atomBoundaries = {}

#maximum distance away from origin of system that molecules can be placed 
systemBoundaries = []

#location of system origin
originLocation = []

#number of molecules to place
instances = 1



#######################################################
#function definitions

#function to parse settings from settings file
def parseSettings():
    
    #open settings file
    settings = file("settings", 'r')

    #get settings

#######################################################




