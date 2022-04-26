
# echo 'Dealing with 250'
# ~/mln/learnwts -d -i ./simulated_knowledge_CR.mln -o simulated_out_conditional_25.mln \
#     -t simulated_train_25.db -ne Food,Pricerange  -dNumIter 30

# ~/mln/infer -ms -i simulated_out_conditional_25.mln -r simulated_out_marginal_25.result \
#     -e simulated_test.db -q Pricerange,Food
    
# ~/mln/infer -ms -i simulated_out_conditional_25.mln -r simulated_out_conditional_25.result \
#     -e simulated_conditional_test.db -q Pricerange,Food

# echo 'Dealing with 500'
# ~/mln/learnwts -d -i ./simulated_knowledge_CR.mln -o simulated_out_conditional_50.mln \
#     -t simulated_train_50.db -ne Food,Pricerange  -dNumIter 30

# ~/mln/infer -ms -i simulated_out_conditional_50.mln -r simulated_out_marginal_50.result \
#     -e simulated_test.db -q Pricerange,Food
    
# ~/mln/infer -ms -i simulated_out_conditional_50.mln -r simulated_out_conditional_50.result \
#     -e simulated_conditional_test.db -q Pricerange,Food

# echo 'Dealing with 1000'
# ~/mln/learnwts -d -i ./simulated_knowledge_CR.mln -o simulated_out_conditional_100.mln \
#     -t simulated_train_100.db -ne Food,Pricerange  -dNumIter 30

# ~/mln/infer -ms -i simulated_out_conditional_100.mln -r simulated_out_marginal_100.result \
#     -e simulated_test.db -q Pricerange,Food
    
# ~/mln/infer -ms -i simulated_out_conditional_100.mln -r simulated_out_conditional_100.result \
#     -e simulated_conditional_test.db -q Pricerange,Food

echo 'Dealing with 2000'

~/jerry_cr/mln-master/alchemy2-linux/learnwts -d -i ./simulated_knowledge_CR.mln -o simulated_out_conditional.mln \
    -t simulated_train_2000.db -ne Food,Pricerange  -dNumIter 30 > learn_wts.txt

~/jerry_cr/mln-master/alchemy2-linux/infer -ms -i simulated_out_conditional.mln -r simulated_out_marginal.result \
    -e simulated_test.db -q Pricerange,Food > infer_marginal.txt
    
~/jerry_cr/mln-master/alchemy2-linux/infer -ms -i simulated_out_conditional.mln -r simulated_out_conditional.result \
    -e simulated_conditional_test.db -q Pricerange,Food > infer_conditional.txt