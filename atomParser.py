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
    #function to run grep and get line numbers of files in a list format
    def grep(self, string, fileName, lineNum=True):

	print("stringstringstringstringstringstringstring")
	print(string)
	print("string")
	
	#init line number list and file name list
	lineNumbers =  []
	locations = []	

	#run grep with specified parameters
	grepResult = os.popen( "grep --with-filename -n '" + string + "' " + fileName).read().split("\n")

#	print(grepResult)

	#get number of colons in first result
	colonCount = grepResult[0].count(":")

	#check how many times : appears in  grep results
	if(colonCount > 0):

	    #get rid of empty blank space in last slot of results
	    grepResult.pop()
	
	    #iterate though all results found 
	    for result in grepResult:

		if(lineNum):
	            #get line number of result
		    lineNumbers.append( int( result.split(":")[1]) )
		    locations.append( result.split(":")[0]  )

		else:
                    lineNumbers.append(result.split(string)[1])

#	    print("$$$$$$$$$$$$$$$$$4")
#	    print(lineNumbers)
#	    print(locations)
#           print("$$$$$$$$$$$$$$$$$$$")
	
	    #return lineNumbers
	    return lineNumbers, locations
	
	else:
	     #if grep results were empty return -1
	     return [-1]
     

###########################################################    
    #function to get number of atoms in simulation
    #by defualt uses coord file name to get number of atoms
    #if md=true, then looks in mdmaster for number of atoms
    def getNumberOfAtoms(self, coord="coord", md=False):
	
        if(md):
    	    #if md simulation then get number of atoms from mdmaster
            atomNumber = int(self.grep("natoms", "mdmaster", lineNum=False)[0][0])
	
        else:
	    #if not md sim, then use coord file
		
            #get grep on intdef
	    intdef = (self.grep("intdef", coord))[0]

	    #check if intdef exits in coord file
	    if(intdef != 0):
	        atomNumber = intdef - 2

	    #if not, use end tag instead
	    else:
		atomNumber = (self.grep("end", coord))[0] - 2

	
	#calculate number of atoms in simulation
	return atomNumber

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
        
       # print(rawFileData)
	return self.atomOrganizer(rawFileData, orgData)

###########################################################    
   #function to write data to files 
    def write(self, f, structures):

	#copy over entire coord file except for the last line, $end
	os.popen("head -n -1 " + str(f) + " > work.coord")

	#for each structure passed into the write function
	for molecule in structures:
		#for each substructure
		for atom in range(len(molecule)):		

			#init empty string variable
			data = ""
				
			#for each dimension 
			for dim in range(3):
				data += "    " + str(molecule["coords"][atom][dim])
			
			#append atom symbol to end of string
			data += "    " + str(molecule["atoms"][atom])
			
		#	print(data)
		
			#append data to new coord file
			os.popen("echo '" + data + "' >> work.coord")
	
	#add $end to coord file
	os.popen("echo '$end' >> work.coord")
        
	#overwrite the actual coord file
	os.popen("mv work.coord ./" + str(f))		
 
###########################################################    
    #function to parse specified time structure from mdlog files
    #ts = specific timestep to parse, can be either single timestep or list of timesteps, should be ts number, not actual time,
    #    ex. ts=[1,2,3] not ts=[0,20,40,60]
    #r = true or false, if true, then will parse all timesteps inbetween range specifed in ts
    #logHead is string of name of start of mdlog files
    #pv is string of either p or v or both, represents whether user wants to parse both position and velocity, or only one or the other, p is for position, v is for velocity
    def parseLog(self, ts, r=False, logHead="mdlog", pv="pv"):
	
	#init data holder
	logData = []

	#get number of atoms in simulation as well as tsDelta
	atomNumber = self.getNumberOfAtoms(md=True)
        
	#get time step delta value, use loop to check if there are any blank strings instead of numerical values
	for value in os.popen("sed '" + str( atomNumber + self.grep("t=   0", "mdlog.1")[0][0] + 1) + "q;d' '" + str(logHead) + ".1'").read().split(" "):
	    
	    if(value == ""):
	        continue
	    else:
	        tsDelta = int(float(value))
		break
	
        #check if range of timesteps are to be parsed
        if(r):
	
	    #get list of timesteps to parse
	    tsToParse = [ (counter +  ts[0]) for counter in range( (ts[1] - ts[0])) ]	

	elif(type(ts) == type([])):
	    #if list of timesteps do not need to be parsed, then check if list of timesteps were passed in
            #if yes, then add that list to tsToParse
	    tsToParse = ts

	else:
	    #if single timestep passed in, then append that sole ts to timesteps to parse list
            tsToParse = [ts]	

	#loop through all timesteps to parse
	for ts in tsToParse:
	
	    print(tsToParse)
	    #get actual timestep numerical value
	    tsNum =  float( (ts-1) * tsDelta) 

	    #get linenumber where timstep data begins 
	    lineNumber, location = self.grep("t=   " + str(tsNum) + "00", (logHead + ".*"))

	    #calculate linenumber where timestep data ends
	    lineNumber.append( lineNumber[0] + atomNumber
)
	    
	    #section to figure whether full coord and velocity should be parsed or only one or the other
	    if(pv.lower() == "p"):
		#only parse position, stop linenumber at last coord location
	        lineNumber.append( lineNumber[0] + atomNumber)
	    
           # print(tsDelta)
	   # print(tsNum)
	    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
	    print(lineNumber)
	    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            #get raw timestep data from file
	    timestepData = os.popen( "sed -n '" + str(lineNumber[0]) + "," + str(lineNumber[1]) + "p' " + location[0]).read()

	   # print(timestepData) 
           # print(lineNumber)	

	    #convert raw data into json type list structure of the form
	    #[ {time:time, "atomLetter":[{coord, atom# in mdlog, velocity}], timestep, timestep  ]
	    logData.append(self.organizeMDLog(timestepData, pv))
		
        return logData

###########################################################   
    #function to organize logdata into a json ready list structure
    #[ {time:time, "atomLetter":[{coord, atom# in mdlog, velocity}], timestep, timestep  ]
    def organizeMDLog(self, timestepData, pv):

	#init lines from mdlog and empty data structure
	lines =  timestepData.split("\n")
	lines.pop()

	tsData = {

            #get numerical value of timestep time
	    "time": float(lines.pop(0).split("=")[1])	
	    
}
#	print(lines)

	#iterate through all mdlog lines passed into function
	for rawLine in lines:
	
	    line = filter(None, rawLine.split(" "))
	    print("\n\n\n #################################3")
	    print(line)
	    print("#######################################")

	    #if atom type not added in to ts data, then do so
	    if( not (line[3] in tsData) ):
	        tsData[line[3]] = { "coord": [] }

            #append coord data to tsData
	    tsData[line[3]]["coord"].append( [ float(line[val]) for val in range(3) ] )	


	return tsData

###########################################################   
#function to take a specific timestep data structure and create a coord file from that timestep
#tsData = [ ts1, ts2, ... tsn ]
    def log2coord(self, tsData, folder="log2coord"):
    
    	#make new folder and move into said folder
    	os.popen("mkdir " + str(folder))
    	os.chdir(folder)		
    
    	#loop over all timesteps in tsData
    	for ts in tsData:
            print(ts)	
    	    #create folder with time of timestep as name and move into said folder
    	    time = str(ts.pop("time"))
    	    os.popen("mkdir " + time)
    	    os.chdir(time)	
    	
    	    #begin converting log data to a coord file
    	    coord = "$coord\n"
		   
    	    for atomType in ts:
                for atom in ts[atomType]["coord"]:
    	            for dim in range(3):
                        coord += str(atom[dim]) + "    "	
    		    
	            coord += atomType + "\n"
   	
    	    coord += "$end"	
    	    os.popen("echo '" + coord + "' > coord")			
    
    	    os.chdir("..")
    
        os.chdir("..")

###########################################################   
    #function to return coord in approriate list structure of [ {atoms:[atom1], [atom2], ['symbol1', 'symbol2', 'symbol3'], coords: [atom1], [x,y,z], [atom3]}, {structure2}, {structure3} ]
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
                atomData[counter]["atoms"].append(atomSymbol)
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
 
