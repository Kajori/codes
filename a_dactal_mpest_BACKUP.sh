#!/bin/bash 
##pipeline mrp - add lines for paup -paup - extract tree from paup outputfile - run prd_temp 
export PYTHONPATH=/home/kbanerj3/Dactal/reup-1.0:$PYTHONPATH
export PYTHONPATH=/home/kbanerj3/Dactal/spruce-1.0:$PYTHONPATH
export PYTHONPATH=/home/kbanerj3/Dactal/newick_modified-1.3.1:$PYTHONPATH
export JAVA_HOME=/projects/tallis/kbanerj3/tools/jdk1.7.0_79
export PATH=/projects/tallis/kbanerj3/tools/jdk1.7.0_79/bin:$PATH
export FASTMRP=/projects/tallis/kbanerj3/dactal/mrpmatrix-master
export LD_LIBRARY_PATH=/projects/tallis/kbanerj3/tools/libc/glibc-2.14/build:$LD_LIBRARY_PATH

oldpyhtonpath=$PATH
echo "oldpyhtonpath=",${oldpyhtonpath}
rm new_sptree_*
rm 1000_score_*
rm best_sptree_*
rm 1000_taxa_score_*
rm starting_tree_*

t=$1
echo " ILS =  " $t

r=1
while [ $r -lt 2 ]; do
    echo " r= $r"
    genetree=/projects/tallis/kbanerj3/dataset/simulated_mammalian/${t}X-200-500/R${r}/gene_tree_${r}
    rm ${genetree}
    echo " done deleting "
    python compute_gene_tree_list.py /projects/tallis/kbanerj3/dataset/simulated_mammalian/${t}X-200-500/R${r} ${genetree}
    let r=r+1
done
echo " Here "
r=1
start=`date +%s`
while [ $r -lt 2 ]; do
    loop=0	
	genetree=/projects/tallis/kbanerj3/dataset/simulated_mammalian/${t}X-200-500/R${r}/gene_tree_${r}
	m=1
	j=0
	
	
	
	export PATH=/home/kbanerj3/tools/installed/python2.7/bin:$PATH
	oldpwd2=$(pwd)
	while [ ${m} -lt 11 ]; do
	    rm ${genetree}.tre 
	    python create_control_program.py ${genetree}
	    cp /projects/tallis/kbanerj3/dactal/scripts/mpest/my_control.usertree /projects/tallis/kbanerj3/tools/mpest_1.5/src/
	    cd /projects/tallis/kbanerj3/tools/mpest_1.5/src/
	    ./mpest my_control.usertree 
	    cd ${oldpwd2}
	    cp ${genetree}.tre $(pwd)/ml_tre_${t}X_R${r}_loop_${loop}_j_${j}_m_${m}
	    let m=m+1
	done   
	python select_best_ml_tree.py ml_tre_${t}X_R${r}_loop_${loop}_j_${j} starting_tree_${t}X_R${r}_${loop}
	export PATH=${oldpyhtonpath}
	
	#java -jar /projects/tallis/kbanerj3/astral/ASTRAL-master/Astral/astral.4.7.8.jar -i ${genetree}  -o starting_tree_${t}X_R${r}_${loop} &> xyz.txt
	
	
	loop=1
    current_score=$(java -jar /projects/tallis/kbanerj3/astral/ASTRAL-master/Astral/astral.4.7.8.jar -q starting_tree_${t}X_R${r}_${loop} -i ${genetree} 2>&1 | tail -n1 | cut -f5 -d' ' )
    echo ${current_score} > simulated_mammalian_current_score_${t}X_R${r}_loop_${loop}
    echo " r = ${r}  Astral running "	   
    current_score=-1
    maxscore=-1
    max_index=-1
    
    while [ ${loop} -lt 6 ]; do
        rm ${genetree}.subsets.*
		echo "  loop = ${loop} "
        rm subsets.*
       	export PATH=/home/kbanerj3/tools/installed/python2.7/bin:$PATH
        echo "      Running DCM3 with starting_tree_${t}X_R${r}_${loop} "
        python resolve_polytomies.py starting_tree_${t}X_R${r}_${loop}
	    python prd_decomp_temp.py $(pwd)/starting_tree_${t}X_R${r}_${loop} 15 4 > ds_${t}X_R${r}_${loop}
        perl extract_subsets.pl -i ds_${t}X_R${r}_${loop}
        sets=$(ls subsets.*)  
        echo "      sets ="${sets}
        j=1
        path=$(pwd)    
        for f in ${sets}
        do
            echo "          Processing $f"
            python induced_subtree_from_taxa.py ${genetree} ${f}
        
            #estimate a species tree  species_tree_i on subset_i (here we have used astral instead of MPEST
            m=1
	        oldpwd2=$(pwd)
	        while [ ${m} -lt 11 ]; do
	            cd /projects/tallis/kbanerj3/tools/mpest_1.5/src/
	            cp $(oldpwd2)/my_control.usertree /projects/tallis/kbanerj3/tools/mpest_1.5/src/my_control.usertree
	            ./mpest my_control.usertree 
	            cd ${oldpwd2}
	            cp ${genetree}.tre $(pwd)/ml_tre_${t}X_R${r}_loop_${loop}_j_${j}_m_${m}
	            let m=m+1
	        done
	        python select_best_ml_tree.py ml_tre_${t}X_R${r}_loop_${loop}_j_${j} species_tree_${t}X_R${r}_${loop}_${j}
	       
            python combine.py all_species_tree_${t}X_R${r}_${loop} species_tree_${t}X_R${r}_${loop}_${j}
        
            echo "          j="$j
            let j=j+1
        done #end of for j
    
        echo "      total j ="${j}
        oldpwd=$(pwd)
        cd /home/kbanerj3/Dactal/test
        export PATH=${oldpyhtonpath}
        let next_loop=${loop}+1
        echo "Running Superfine with all_species_tree_${t}X_R${r}_${loop}"
       	python runReup_v2.py -r rml ${oldpwd}/all_species_tree_${t}X_R${r}_${loop}  > ${oldpwd}/starting_tree_${t}X_R${r}_${next_loop}

        cd ${oldpwd}
    
        current_score=$(java -jar /projects/tallis/kbanerj3/astral/ASTRAL-master/Astral/astral.4.7.8.jar -q starting_tree_${t}X_R${r}_${next_loop} -i ${genetree} 2>&1 | tail -n1 | cut -f5 -d' ' )
        
       	echo " current_score ="${current_score}
       	echo ${current_score} > simulated_mammalian_current_score_${t}X_R${r}_loop_${loop}
        val=$(echo "${current_score} >= ${maxscore} " | bc)
        if [ $val -eq 1 ]
        then
            maxscore=${current_score}
            max_index=${next_loop}
       	fi
        echo " maxscore "${maxscore}
       
        let loop=loop+1
    done #end of loop
    echo ${current_score} > simulated_mammalian_current_score_${t}X_R${r}_loop_${loop}
    echo ${maxscore} > simulated_mammalian_max_score_${t}X_R${r}
    echo " Final maxscore "${maxscore}
    echo " max_index  = ${max_index} "
	echo ${max_index} > simulated_mammalian_index_${t}X_R${r}
    cat starting_tree_${t}X_R${r}_${max_index} > best_sptree_${t}X_R${r} 
    let r=r+1
done
end=`date +%s`
runtime=$((end-start))
echo "$runtime" > runtime_${t}X
