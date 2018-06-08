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
    def all(self, f):    

        #parse arguments
        #args = parser.parse_args()
	
	return self.parser(f, "cat")        

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
    def parser(self, f, command):

        #get lines from coord file
        rawFileData = os.popen(" tail -n +2 " + f + " | head -n -1 | sed '/intdef/,$d' | " + command).read()
        
        print(rawFileData)
	return self.atomOrganizer(rawFileData)

###########################################################   
    #function to return coord in approriate list structure of [ [atom1], [atom2], ['symbol',x,y,z] ]
    #currently only works with TM file data
    def atomOrganizer(self, rawFileData):

	#init atom coord data structure
	atomData = []   

	#go through each coord line as separated by a newline
	for coord in rawFileData.split("\n"):
	    
            #filter out whitespaces from coord data
	    coordData = filter(None, coord.split(" "))
	    
            #if coord data is not empty is not empty data
	    if( len(coordData) > 1 ):
                #append atom data to list object
		atomSymbol = coordData.pop()
                atomData.append([atomSymbol] + [float(coordData[0])] + [float(coordData[1])] + [float(coordData[2])])
        
	#return processed data
	return atomData
 
