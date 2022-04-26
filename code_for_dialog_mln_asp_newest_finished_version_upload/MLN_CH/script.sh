echo 'Dealing with 2000'

~/jerry_cr/mln-master/alchemy2-linux/learnwts -d -i ./simulated_knowledge.mln -o simulated_out_conditional.mln \
    -t simulated_train_2000.db -ne Kind,Stars,Pricerange -dNumIter 30 > learn_wts.txt

~/jerry_cr/mln-master/alchemy2-linux/infer -ms -i simulated_out_conditional.mln -r simulated_out_marginal.result \
    -e simulated_test.db -q Kind,Stars,Pricerange > infer_marginal.txt
    
~/jerry_cr/mln-master/alchemy2-linux/infer -ms -i simulated_out_conditional.mln -r simulated_out_conditional.result \
    -e simulated_conditional_test.db -q Kind,Stars,Pricerange > infer_conditional.txt