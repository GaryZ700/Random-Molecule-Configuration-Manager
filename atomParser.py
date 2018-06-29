#class object to parse atoms from TM coord file and return list object in the format of ['symbol', float x, float y, float z]

import os

class atomParser():

    #begin by loading arguments
    
    #init argument parser
    #parser = argparse.ArgumentParser()
    
    #create arguments
    #-f, first x atoms to parse data
    #-l, last x atoms to parse data from
    #-file, file to parse data from
    #parser.add_argument('-f', metavar='f', type=int, help='first x atoms to parse', default=0)
    #parser.add_argument('-l', metavar='l', type=int, help='last x atoms to parse', default=0)
    #parser.add_argument('-file', metavar='file', type=str, help='name of Turbomole coord file', default='coord')

###########################################################    
    #define to parse all atoms
    def all(self, f, orgData=[False]):

        #parse arguments
        #args = parser.parse_args()
	
	return self.parser(f, "cat", orgData)        

###########################################################    
    #function to parse first x lines of atoms
    def first(self, f, first):

	return self.parser(f, "head -n " + str(first))
	
###########################################################    
    #function to parse last x lines of atoms
    def last(self, f, last):
	
	return self.parser(f, "tail -n " + str(last))

###########################################################    
   #main code for parsing atoms from coord file
    def parser(self, f, command, orgData):

        #get lines from coord file
        rawFileData = os.popen(" tail -n +2 " + f + " | head -n -1 | sed '/intdef/,$d' | " + command).read()
        
        print(rawFileData)
	return self.atomOrganizer(rawFileData, orgData)

###########################################################   
    #function to return coord in approriate list structure of [ {atoms:[atom1], [atom2], ['symbol',x,y,z]}, {structure2}, {structure3} ]
    #currently only works with TM file data
    #can organize atoms based upon data in [[first x atoms, next y atoms, and last z atoms] orgData structure to return atoms in said configuration
    def atomOrganizer(self, rawFileData, orgData):

	#init list indice counter
	counter = 0
	
	#init atom list
	atomData = []
	for object in orgData:
	    atomData.append({

	    "atoms": [], 
	    "coords": [] 
})	
	
	#go through each coord line as separated by a newline
	for coord in rawFileData.split("\n"):  

            #filter out whitespaces from coord data
	    coordData = filter(None, coord.split(" "))
	    
            #if coord data is not empty is not empty data
	    if( len(coordData) > 1 ):
                #append atom data to list object
		atomSymbol = coordData.pop()
                atomData[counter]["atoms"].append([atomSymbol])
                atomData[counter]["coords"].append([float(coordData[0])] + [float(coordData[1])] + [float(coordData[2])])
                
		#if orgdata was passed by user
		if(orgData[counter] != False):
		    
	            #decrease orgData atom counter
		    orgData[counter] -= 1;
		    
		    #check if counter should be incremented
		    if(orgData[counter] == 0):
		        #increment counter
			counter += 1
		    
		    #check if loop should end now, since end of orgData reached
		    if(counter >= len(orgData)):
		       break
		

	#return processed data
	return atomData
 
