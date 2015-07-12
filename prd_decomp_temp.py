#! /usr/bin/python

import sys
from PRD_temp import PRDWrapper_temp

if ( __name__ == '__main__' ) :
    filepath = sys.argv[1]
    subset = int(sys.argv[2])
    overlap = int(sys.argv[3])
    dec = PRDWrapper_temp(subset, overlap)
    output = dec.decompose_dataset(filepath)
    print 'I am here ',output,'***'
    for i, subset in enumerate(output) :
        print('subset {0:2d}: {1}'.format(i, subset))
