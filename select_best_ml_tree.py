import sys,string,dendropy,re

filename=sys.argv[1]
out_filename=sys.argv[2]
max_score=--sys.maxint - 1
index=-1
for m in range(1,11):
    f_w=open(filename+'_m'+str(m),'r')
    input=f_w.read()
    f_w.close()
    mat=re.findall('tree mpest \[-\d+\.\d*\]',input)
    print "  mar =",mat
    if(len(mat)>1):
        print " select_best_ml_tree.py ERROR"
    else:
	match=mat[0]
        l_index=string.find(match,'[')
        score=str(match[l_index+1:-1])
    	print "****  m =",m, "score =",score
	if ( score > max_score):
        	max_score=score
        	index=m
    
f_w=open(filename+'_m'+str(index),'r')
old_input=f_w.read()
f_w.close()
input=old_input

#Translate
l_index=string.find(input,'translate\n\t')
h_index=string.find(input,'\n  tree mpest')
input=input[l_index+len('translate\n\t'):h_index]
#print " new input =s", input

list_trrns=[ x.split(' ') for x in [ l.strip() for l in input.split('\n')]]
new_list=[num for elem in list_trrns for num in elem]
my_dict={}
for m in range(0,len(new_list),2):
    my_dict[new_list[m]]=new_list[m+1][:-1]
#print my_dict


input=old_input
mat=re.findall('\n  tree mpest \[-\d+\.\d*\] = \(',input)
#print " \n ",mat,"\n"
l_index=string.find(mat[0],'(')
ll_index=string.find(input,'\n  tree mpest')

#print " \nll\n ",input[l_index+ll_index:],"\n"

input=input[l_index+ll_index:]
h_index=string.find(input,';')
input=input[:h_index+1]
#print input
taxons=re.findall('\(\d+:',input)
for t in taxons:
    label=t[1:-1]
    #print t,label,' ',my_dict[str(label)]
    input=re.sub('\('+label+':','('+my_dict[str(label)]+':',input)

taxons=re.findall(',\d+:',input)
for t in taxons:
    label=t[1:-1]
    input=re.sub(','+label+':',','+my_dict[str(label)]+':',input)
#print " \n ",input,"\n"

f_w=open(sys.argv[2],'w')
f_w.write(input)
f_w.close()
