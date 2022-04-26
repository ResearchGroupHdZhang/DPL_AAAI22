echo 'Dealing with 500'

/root/mln-master-Integration-multi-env/alchemy2-linux/learnwts -d -i ./simulated_knowledge.mln -o simulated_out_conditional_500.mln -t simulated_train_500.db -ne Kind,Stars,Pricerange -dNumIter 30 > learn_wts_500.txt

/root/mln-master-Integration-multi-env/alchemy2-linux/infer -ms -i simulated_out_conditional_500.mln -r simulated_out_marginal_500.result -e simulated_test.db -q Kind,Stars,Pricerange > infer_marginal_500.txt
    
/root/mln-master-Integration-multi-env/alchemy2-linux/infer -ms -i simulated_out_conditional_500.mln -r simulated_out_conditional_500.result -e simulated_conditional_test.db -q Kind,Stars,Pricerange > infer_conditional_500.txt