echo 'Dealing with 500_3'

/home/zzc/mln_diff_work_test/code_for_dialog_mln_asp/alchemy2-linux/learnwts -d -i ./simulated_knowledge.mln -o simulated_out_conditional_500_3.mln -t simulated_train_500_3.db -ne Kind,Stars,Pricerange -dNumIter 30 > learn_wts_500_3.txt

/home/zzc/mln_diff_work_test/code_for_dialog_mln_asp/alchemy2-linux/infer -ms -i simulated_out_conditional_500_3.mln -r simulated_out_marginal_500_3.result -e simulated_test.db -q Kind,Stars,Pricerange > infer_marginal_500_3.txt
    
/home/zzc/mln_diff_work_test/code_for_dialog_mln_asp/alchemy2-linux/infer -ms -i simulated_out_conditional_500_3.mln -r simulated_out_conditional_500_3.result -e simulated_conditional_test.db -q Kind,Stars,Pricerange > infer_conditional_500_3.txt


taskset -c 48 nohup python pydial.py train config/mln_config/env15-A2C-CH-ASP-100_3.cfg &

taskset -c 6 nohup sh script_500_3.sh &

taskset -c 60 nohup python pydial.py train config/mln_config/env20-A2C-CH-ASP-500_3.cfg &


taskset -c 10 nohup python pydial.py train config/mln_config/env2-A2C-CH-ASP-100_2.cfg &

taskset -c 36 nohup python pydial.py train config/mln_config/env12-A2C-CH-ASP-500_3.cfg &

taskset -c 30 nohup python pydial.py train config/main_config/env28-A2C-CH-ASP.cfg &

taskset -c 3 nohup python pydial.py train config/asp_config/env1-A2C-CH-ASP-ac.cfg &

taskset -c 34 nohup python pydial.py train config/asp_config/env10-A2C-CH-ASP-ic.cfg &

taskset -c 32 nohup python pydial.py train config/mln_config/env8-A2C-CH-ASP-500_3.cfg &

taskset -c 36 nohup python pydial.py train config/main_config/env1-A2C-CH.cfg &

taskset -c 51 nohup python pydial.py train config/main_config/env22-A2C-CH-ASP.cfg &

env12/env21/env14/env19/env22

taskset -c 82 nohup python pydial.py train config/test_acer_config/env10-ACER-CH-ASP.cfg &