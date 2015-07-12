import dendropy
import re  
import os,sys

filename=sys.argv[1]
outfile=sys.argv[2]
trees = dendropy.TreeList.get_from_path(filename,'newick')
f_w = open(outfile,'w')
for count in range (0,3):
    input=str(trees[count])
    #print  "\n\n input = ",input
    branch_length_list=re.findall('\d+:',input)
    for b in branch_length_list:
        #print " b= ",b
	input=re.sub(b,':',input)

    #e_list=re.findall('e-\d+',input)
    #for b in e_list:
    #    input=re.sub(b,'',input)
    
    e_list=re.findall(' ',input)
    for b in e_list:
        input=re.sub(b,'',str(input))
    
    
    #print "\n\n  New input = ",input   
    
    f_w.write(input+';')
f_w.close()
