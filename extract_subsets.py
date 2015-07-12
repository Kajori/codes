#input : ds_${index}

import re  
import os,sys

filename=sys.argv[1]
f_r=open(filename,'r')
input=f_r.read()
f_r.close()

subsets=re.findall('subset  \d+: \[.*\]',input)
print subsets
for subs in subsets:
    print ' subs =',subs
    
    index=subs[len('subset  '):subs.index(':')]
    print ' index=',index
    
    taxa=subs[subs.index('[')+1:subs.index(']')]
    print ' all taxa',taxa
    taxa_list=taxa.split(',')
    f_w=open('subset_'+filename[3:]+'_S'+str(index),'w')
    for t in taxa_list:
        print t,' , ',t[t.index("'")+1:-1]
        f_w.write(t[t.index("'")+1:-1]+'\n')
    f_w.close()
    
