echo 'Dealing with 250'

/root/mln-master-Integration-multi-env/alchemy2-linux/learnwts -d -i ./simulated_knowledge.mln -o simulated_out_conditional_250.mln -t simulated_train_250.db -ne Kind,Stars,Pricerange -dNumIter 30 > learn_wts_250.txt

/root/mln-master-Integration-multi-env/alchemy2-linux/infer -ms -i simulated_out_conditional_250.mln -r simulated_out_marginal_250.result -e simulated_test.db -q Kind,Stars,Pricerange > infer_marginal_250.txt
    
/root/mln-master-Integration-multi-env/alchemy2-linux/infer -ms -i simulated_out_conditional_250.mln -r simulated_out_conditional_250.result -e simulated_conditional_test.db -q Kind,Stars,Pricerange > infer_conditional_250.txt