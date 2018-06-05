#script to parse atoms from TM coord file and return list object in the format of ['symbol', float x, float y, float z]

import argparse
import os

#begin by loading arguments

#init argument parser
parser = argparse.ArgumentParser(description='Process some integers.')

#create arguments
#-f, first x atoms to parse data
#-l, last x atoms to parse data from
#-file, file to parse data from
parser.add_argument('-f', metavar='f', type=int, help='first x atoms to parse', default=0)
parser.add_argument('-l', metavar='l', type=int, help='last x atoms to parse', default=0)
parser.add_argument('-file', metavar='file', type=str, help='name of Turbomole coord file', default='coord')

#parse arguments
args = parser.parse_args()

#generate appropriate command
if(args.f > 0):

    command = "head -n " + str(args.f + 1)

elif(args.l > 0):
   
    command = "tail -n " + str(args.l - 1)

else:
    
    command = "cat"


#get lines from coord file
lines = os.popen(command + " " + args.file).read()

print(lines)
