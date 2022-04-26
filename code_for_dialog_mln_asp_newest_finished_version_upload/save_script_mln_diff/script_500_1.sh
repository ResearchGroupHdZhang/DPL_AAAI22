echo 'Dealing with 500_1'

/home/zzc/fix_random_bugs/code_for_dialog_mln_asp/alchemy2-linux/learnwts -d -i ./simulated_knowledge.mln -o simulated_out_conditional_500_1.mln -t simulated_train_500_1.db -ne Kind,Stars,Pricerange -dNumIter 30 > learn_wts_500_1.txt

/home/zzc/fix_random_bugs/code_for_dialog_mln_asp/alchemy2-linux/infer -ms -i simulated_out_conditional_500_1.mln -r simulated_out_marginal_500_1.result -e simulated_test.db -q Kind,Stars,Pricerange > infer_marginal_500_1.txt
    
/home/zzc/fix_random_bugs/code_for_dialog_mln_asp/alchemy2-linux/infer -ms -i simulated_out_conditional_500_1.mln -r simulated_out_conditional_500_1.result -e simulated_conditional_test.db -q Kind,Stars,Pricerange > infer_conditional_500_1.txt