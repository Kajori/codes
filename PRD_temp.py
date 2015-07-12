#-------------------------------------------------------------------------------
# File :  _PRD.py
# Description :  Definition and implementation of the class 'PRDWrapper'.
#
# Author :  J. Alvarez-Jarreta  ( jorgeal@unizar.es )
# Last version :  v0.2 ( 04/Dec/2013 )
#-------------------------------------------------------------------------------
# Historical report :
#
#   DATE :  04/Dec/2013
#   VERSION :  v0.2
#   AUTHOR(s) :  J. Alvarez-Jarreta
#   MODIFICATIONS :  Added an exception handler when DCM returns just one subset
#                    as output, meaning that there is no decomposition possible.
#
#   DATE :  27/Nov/2013
#   VERSION :  v0.1
#   AUTHOR(s) :  J. Alvarez-Jarreta
#
#-------------------------------------------------------------------------------

import os, subprocess, dendropy, tempfile
from subprocess import call

#  --------------------------------------------------------------------------  #

class PRDWrapper_temp :
    """
    
    """
    
    def __init__ ( self, subset, overlap ) :
        """
        Creates a PRD.

        Arguments:
            - subset        - maximum subset size, required (int)
            - overlap       - 1/4 of the number of overlapping sequences between
                              any two subsets, required (int)
        """
        if ( not isinstance(subset, int) ) :
            raise TypeError('"subset" argument should be an integer')
        if ( subset < 1 ) :
            raise ValueError('"subset" argument should be greater than 0')
        if ( not isinstance(overlap, int) ) :
            raise TypeError('"overlap" argument should be an integer')
        if ( overlap < 1 ) :
            raise ValueError('"overlap" argument should be greater than 0')
        if ( subset < overlap ) :
            raise ValueError('"subset" argument should be greater than ' \
                             '"overlap" argument')
        
        self._bin = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'bin', 'dcm')
        # We leave empty the tree input file
        self._args = ['3', None, str(overlap)]
        self._subset = subset


    def decompose_dataset ( self, filepath ) :
        """
        Decomposes the dataset of the tree in the input file using DCM type 3
        and returns the subsets as a list os lists with taxa ids. All the
        subsets in the output file will have at most self._subset taxa.

        Arguments:
            - filepath      - absolute path for input file, required (str)

        The format of the input file must be NEWICK (this is the only format
        supported by DCM).
        """
        #print " Inside decompose_dataset "
        if ( not isinstance(filepath, str) ) :
            raise TypeError('"filepath" argument should be a string')
        if ( not os.path.exists(filepath) ) :
            raise IOError('{0} does not exist'.format(filepath))

        command= "./dcm" #print " type(self._args)=",type(self._args) #print " self._args=",self._args
        command = command +" "+self._args[0]
        command = command + " "+filepath
        command = command +" "+self._args[2]
        print "\n command =",command
        with open(os.devnull, 'w') as stderr_file :
            
            if (os.getcwd()[-3:]!='bin'):
                os.chdir(os.getcwd()+"/bin")
            
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) #output = subprocess.check_output(command, stderr=stderr_file,universal_newlines=True)
            stdout, stderr = p.communicate()
            print " stdout =",stdout,"\n stderr=",stderr
            
        # Split the output in lines, removing the first and last lines which
        # do not contain any subset data
        subset_list = stdout.split('\n')[1:-1]
	# the following if statement is to alert you when the given parameters (maximum subsetsize and overlap) are not satisfiable. But it will output the large subsets. If you want, you can make it an "raise exception" instead of printing.
        #if ( len(subset_list) == 1 ) :
         #   print('> DCM can not obtain a decomposition with the given "subset"' \
          #        ' and "overlap"\n values for subset {0}\n'.format(subset_list[0].split(' ')[1:-1]))
        
	decomposition = []
        for subset_str in subset_list :
            # Split the subset string to get a list of taxa of the subset,
            # removing the first and last elements which do not correspond to
            # taxon ids
            subset = subset_str.split(' ')[1:-1]
            if ( (len(subset_list) > 1) and (len(subset) > self._subset) ) :
                # Recursively decompose each subset whose number of taxa is
                # greater than self._subset, extracting its corresponding
                # subtree from the tree of the input file
                #print('> Decompose recursively the subset {0}\n'.format(subset))
                tree = dendropy.Tree()
                tree.read_from_path(filepath, 'newick')
                tree.retain_taxa_with_labels(subset)
                subtree_file=tempfile.NamedTemporaryFile(mode='w',dir=os.getcwd(),prefix='tmp',delete=False)
                tree_str = tree.as_string('newick', suppress_rooting=True)
                subtree_file.write(tree_str) #f_w.write(tree_str[5:])
                subtree_file.close()
                subsets_ith = self.decompose_dataset(subtree_file.name)
                decomposition += subsets_ith
                
                
            else : # (len(subset_list) == 1) or (len(subset) <= self._subset)
                decomposition.append(subset)
        return ( decomposition )
	

#  --------------------------------------------------------------------------  #
