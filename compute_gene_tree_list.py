#-------------------------------------------------------------------------------
# File :  compute gene tree list.py
# Description :  Used to collect the genes from  inside the folder sys.argv[1] and make a gene tree list and output file is sys.argv[2]
#
# Author :  Kajori Banerjee
#
#-------------------------------------------------------------------------------
# Inputs : python compute_gene tree_list.py input_filename output_filename
#
# example : python collect_data.py 1000_taxa_score_* simulated_mammalian_score.txt simulated_mammalian_avg.txt
#-------------------------------------------------------------------------------

import glob, os,sys

f_w=open(sys.argv[2],'w')
path=sys.argv[1]
#print "os.listdir(path): ",os.listdir(path)
for dir in os.listdir(path):
    if(dir.isdigit()):
	f_r=open(path+'/'+dir+'/raxmlboot.gtrgamma/RAxML_bipartitions.final.f200','r')
    	#print dir
	f_w.write(f_r.read())
	f_r.close()
f_w.close()

    
