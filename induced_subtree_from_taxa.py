#!/lusr/bin/python
'''
Created on Jun 3, 2011

@author: smirarab, modified by Bayzid
'''
import dendropy
import sys
import os
import copy
import os.path

if __name__ == '__main__':

    treeName = sys.argv[1]
    sample = open(sys.argv[2])
    #print "sample =",sys.argv[2]
    included = [s[:-1] for s in sample.readlines()]
    resultsFile="%s.%s" % (treeName, os.path.basename(sample.name))
    trees = dendropy.TreeList.get_from_path(treeName, 'newick',rooted=True)  #rooted = True, I changed it to as_rooted
    
    filt = lambda node: True if (node.taxon is not None and node.taxon.label not in included) else False
    for tree in trees:
        #print "\n\n\n tree = ",tree
        
        nodes = tree.get_node_set(filt)
        #print "\n\n\n list = ",set([n.taxon.label for n in nodes]) & set([n.taxon.label for n in tree.leaf_nodes()])
        #print "\n\n\n difference = ",set([n.taxon.label for n in nodes]).difference(set([n.taxon.label for n in tree.leaf_nodes()]))
        
        diff=set([n.taxon.label for n in tree.leaf_nodes()]).difference(set([n.taxon.label for n in nodes]))
        #print "\n\n\n difference 2 = ",len(diff)
        
        #print "\n\n\n list 2 = ",[n.taxon.label for n in nodes]
        
        #print ' type(tree) = ',type(tree)
        if(len(diff)!=0):
            tree.prune_taxa_with_labels([n.taxon.label for n in nodes])

        else:
            trees.remove(tree)
    print "writing results to " + resultsFile        
    trees.write(open(resultsFile,'w'),'newick',write_rooting=False)  
