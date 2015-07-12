#Version 2

#python create_control_program.py -r ${r} -loop ${loop} -j ${j}  -gt ${genetree}

import sys,dendropy,random

genetree=str(sys.argv[1])

random.seed()
if '.' in genetree:
	basic_index=genetree[len('gene_tree_'):genetree.index('.')]
else:
	basic_index=genetree[len('gene_tree_'):]

f_w=open('my_control.usertree_'+basic_index,'w')
f_w.write(genetree+'\n')
f_w.write('0'+'\n') # 1: calculate triple distance among trees. 0: donot calculate
f_w.write(str(random.randint(0,10000000))+'\n') # seed
f_w.write('1 \n')  # number of independent runs

treelist=dendropy.TreeList.get_from_path(sys.argv[1],'newick')
model_tree = treelist[0]
taxon_set_model_tree=[n.taxon.label for n in model_tree.leaf_nodes()]

f_w.write(str(len(treelist))+' '+str(len(taxon_set_model_tree))+'\n') # number of genes and number of species 

for t in taxon_set_model_tree:
    # species, number of alleles, allele names in gene trees
    f_w.write(t+' 1 '+t+'\n')
f_w.write('0')
f_w.close()
