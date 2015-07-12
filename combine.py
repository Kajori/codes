import os,sys

#combine all the species tree into a single file

file_w = open(sys.argv[1],'a')
file_r = open(sys.argv[2],'r')

file_w.write(file_r.read())
file_w.write("\n")
file_w.close()
file_r.close()
