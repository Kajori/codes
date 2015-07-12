#-------------------------------------------------------------------------------
# File :  centroid_decomposition.py
# Description :  /dcm does not work when the input tree has polytomies . It resolves polytomies
#
# Author :  Kajori Banerjee ( taked from PASTA code)
# Last version :  ( 23/June/2015 )
#-------------------------------------------------------------------------------

import dendropy,os,sys

def main(argv):
    input_tree_path = sys.argv[1]
    S=dendropy.Tree.get_from_path(input_tree_path,schema="newick")
    S.resolve_polytomies() 
    os.remove(input_tree_path)
    f=open(input_tree_path,"w")
    tree_str = S.as_string('newick', suppress_rooting=True)
    f.write(tree_str)
    f.close()
    
if __name__ == "__main__":
    main(sys.argv)