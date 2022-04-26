echo 'Dealing with 100_3'

/home/zzc/fix_random_bugs/code_for_dialog_mln_asp/alchemy2-linux/learnwts -d -i ./simulated_knowledge.mln -o simulated_out_conditional_100_3.mln -t simulated_train_100_3.db -ne Kind,Stars,Pricerange -dNumIter 30 > learn_wts_100_3.txt

/home/zzc/fix_random_bugs/code_for_dialog_mln_asp/alchemy2-linux/infer -ms -i simulated_out_conditional_100_3.mln -r simulated_out_marginal_100_3.result -e simulated_test.db -q Kind,Stars,Pricerange > infer_marginal_100_3.txt
    
/home/zzc/fix_random_bugs/code_for_dialog_mln_asp/alchemy2-linux/infer -ms -i simulated_out_conditional_100_3.mln -r simulated_out_conditional_100_3.result -e simulated_conditional_test.db -q Kind,Stars,Pricerange > infer_conditional_100_3.txt