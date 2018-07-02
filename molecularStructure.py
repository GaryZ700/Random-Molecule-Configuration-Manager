#class to create structure of molecular objects based upon having atoms build up to molecules, and molecules building up to structures
#parser reads atoms to form molecues
#molecules can then be appended to a new molecular object to form a structure object
#allows for easy movement of atoms according to center points of molecules and structures

#import classes
from atomParser import atomParser


class molecularObject():

    #init atom parser 
    parser = atomParser()

    #global variables
    #init list of molecules
    #molecule defined by {atoms, coord, center}
    structures = []

#######################################################
#create a molecule object from specified file
#f is name of file, orgData is how many atoms belong to a single molecule, form = t for Turbomole file, and = x for xyz format
    def load(f, orgData=[False], form="t"):

