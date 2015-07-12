#!/bin/bash 
##pipeline mrp - add lines for paup -paup - extract tree from paup outputfile - run prd_temp 
export PYTHONPATH=/home/kbanerj3/Dactal/reup-1.0:$PYTHONPATH
export PYTHONPATH=/home/kbanerj3/Dactal/spruce-1.0:$PYTHONPATH
export PYTHONPATH=/home/kbanerj3/Dactal/newick_modified-1.3.1:$PYTHONPATH
export JAVA_HOME=/projects/tallis/kbanerj3/tools/jdk1.7.0_79
export PATH=/projects/tallis/kbanerj3/tools/jdk1.7.0_79/bin:$PATH
export FASTMRP=/projects/tallis/kbanerj3/dactal/mrpmatrix-master
export LD_LIBRARY_PATH=/projects/tallis/kbanerj3/tools/libc/glibc-2.14/build:$LD_LIBRARY_PATH
AstralPATH=/projects/tallis/kbanerj3/astral/ASTRAL-master/Astral
genetreePATH=/projects/tallis/kbanerj3/dataset/simulated_mammalian
mpestPATH=mpest/src

oldpyhtonpath=$PATH
export PATH=/home/kbanerj3/tools/installed/python2.7/bin:$PATH
echo "oldpyhtonpath=",${oldpyhtonpath}
rm new_sptree_*
rm 1000_score_*
rm best_sptree_*
rm 1000_taxa_score_*
rm starting_tree_*

t=$1
r=$2
echo " ILS =  " $t
echo " r= $r"


genetree=${genetreePATH}/${t}X-200-500/R${r}/gene_tree_${r}
rm ${genetree}
python compute_gene_tree_list.py ${genetreePATH}/${t}X-200-500/R${r} ${genetree}
cp ${genetree} gene_tree_${r}


loop=0
basic_index=${t}X-200-500_R${r}

echo "Preparing gene trees  for ${basic_index} "
#preparing gene trees : removing the bootstrap values
python remove_bootstrap_support_val.py gene_tree_${r} gene_tree_tmp1_${basic_index}
python reroot.py gene_tree_tmp1_${basic_index} GAL  -nomrca gene_tree_${basic_index}
cp gene_tree_${basic_index} ${mpestPATH}/gene_tree_${basic_index}
echo "File gene_tree_${basic_index} created"
	
	
echo "  copying  gene_tree_${basic_index}  " 
start=`date +%s`
 
oldpwd2=$(pwd)
m=1
index=${basic_index}_L${loop}
while [ ${m} -lt 11 ]; do
	
	index2=${index}_m${m}
	
	echo "  Running MP-est for ${index2} "
	python create_control_program.py gene_tree_${basic_index}
	echo " control program echo my_control.usertree_${basic_index}  created "
	
	cp my_control.usertree_${basic_index} ${mpestPATH}/my_control.usertree_${basic_index}
	echo "  copying my_control.usertree "
	
	cd ${mpestPATH}
	./mpest my_control.usertree_${basic_index} &> abc_${index2}.txt
	cp gene_tree_${basic_index}.tre ../../ml_tre_${index2}
	echo " control program ml_tre_${index2} created "
	cd ${oldpwd2}
	let m=m+1
done
end=`date +%s`
runtime=$((end-start))
echo "$runtime" > runtime_mpest_${index}


python select_best_ml_tree.py ml_tre_${index} starting_tree_${index}
echo " control program starting_tree_${index} created "
#export PATH=${oldpyhtonpath}
	
	
loop=1
while [ ${loop} -lt 11 ]; do
    start=`date +%s`
    prev_index=${index}
    index=${basic_index}_L${loop}
        
    rm gene_tree_${r}_src.subsets.*
	echo "loop = ${loop} "
    rm subsets.*
       	
    echo "      Running DCM3 with starting_tree_${prev_index} "
    python resolve_polytomies.py starting_tree_${prev_index}
    
	python prd_decomp_temp.py $(pwd)/starting_tree_${prev_index}  15 4 > ds_${index}
	echo " control program ds_${index} created "
    echo " running extract_subsets.py with ds_${index}" 	    
    python extract_subsets.py  ds_${index}
    
    sets=$(ls subset_${index}_*)  
    echo "      sets ="${sets}
    j=1    
    for f in ${sets}
    do
        echo "      Processing $f"
        python induced_subtree_from_taxa.py gene_tree_${basic_index} ${f}
        cp gene_tree_${basic_index}.${f}  ${mpestPATH}/gene_tree_${basic_index}.${f}
        #estimate a species tree  species_tree_i on subset_i (here we have used astral instead of MPEST
        m=1
        while [ ${m} -lt 11 ]; do
	    
	        index2=${index}_S${j}_m${m}
	    
	        echo "  Running MP-est for ${index2} "
	        python create_control_program.py gene_tree_${basic_index}.${f}
	        echo " control program created "
	    
	        cp my_control.usertree_${basic_index} ${mpestPATH}/my_control.usertree_${basic_index}
	        echo "  copying my_control.usertree "
	    
	        cd ${mpestPATH}
	        ./mpest my_control.usertree_${basic_index} &> abc_${index2}.txt
	        cp gene_tree_${basic_index}.${f}.tre ../../ml_tre_${index2}
	        cd ${oldpwd2}
	        let m=m+1
	    done
	    python select_best_ml_tree.py ml_tre_${index}_S${j} species_tree_${index}_S${j}
        python combine.py all_species_tree_${index} species_tree_${index}_S${j}
        echo "      j="$j
        let j=j+1
    done #end of for j
    
    
    
    echo "      total j ="${j}
    
    oldpwd=$(pwd)
    cd /home/kbanerj3/Dactal/test
    export PATH=${oldpyhtonpath}
    echo "Running Superfine with all_species_tree_${index}"
    python runReup_v2.py -r rml ${oldpwd}/all_species_tree_${index}  > ${oldpwd}/starting_tree_${index}
    export PATH=/home/kbanerj3/tools/installed/python2.7/bin:$PATH
    cd ${oldpwd}    
       
    end=`date +%s`
    runtime=$((end-start))
    echo "$runtime" > runtime_${index}
    let loop=loop+1
done #end of loop
