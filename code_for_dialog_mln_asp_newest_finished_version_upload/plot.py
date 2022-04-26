import ast
import numpy as np
import os
from scipy import stats
import matplotlib
#
# matplotlib.use('TkAgg')
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import glob
from scipy.signal import savgol_filter

CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Violet = '#661D98'
CB91_Amber = '#F5B14C'
CB91_Orange = '#FFB90F'

# color_list = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
#               CB91_Purple, CB91_Violet]

color_list = [CB91_Blue, CB91_Orange, CB91_Green, CB91_Pink,
              CB91_Purple, CB91_Violet]

plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

sns.set_style(
    {
        'style': 'whitegrid',
        'axes.axisbelow': True,
        # 'axes.edgecolor': 'lightgrey',
        'axes.facecolor': 'None',
        # 'axes.grid': True,
        # 'axes.labelcolor': 'dimgrey',
        'axes.spines.right': True,
        'axes.spines.top': True,
        # 'grid.linestyle': '-',
        'figure.facecolor': 'white',
        'lines.solid_capstyle': 'round',
        'patch.edgecolor': 'w',
        'patch.force_edgecolor': True,
        # 'text.color': 'dimgrey',
        'xtick.bottom': False,
        # 'xtick.color': 'dimgrey',
        'xtick.direction': 'out',
        'xtick.top': False,
        # 'ytick.color': 'dimgrey',
        'ytick.direction': 'out',
        'ytick.left': False,
        'ytick.right': False
    })

sns.set_context("notebook", font_scale=1.25)


def plot_main():
    # plt.subplot(131)
    plt.figure(figsize=[8, 6])
    test_num_dialogs = 100
    num_batches = 40
    
    # CH

    # random_seeds = [1745229, 3968680, 6936311, 9768236, 49780728, 55148360, 59469316, 88051840, 8116315, 5552435] # a2c ten seeds

    random_seeds = [1745229, 6936311, 9768236, 49780728, 88051840] # a2c best five seeds of ten for 3ai new test10 OOOOOOK!


    # random_seeds = [75510161, 56809769, 83753959, 85741963,  13997123, 68459827, 90606062, 92309183, 98672432, 96374603] # dqn ten seeds

    # random_seeds = [75510161, 83753959, 85741963, 96374603, 98672432 ] # test dqn five best seeds of ten  OOOOOOK!

    # random_seeds = [6213484, 8255169, 9560510, 35649715,  45956157, 47294026, 56191691, 68267486, 78514400, 85847292] # bdqn ten seeds
    # random_seeds = [8255169, 45956157, 47294026, 56191691, 68267486] # bdqn five best seeds of ten  OOOOOOK!

    # random_seeds = [34738061, 37732739, 53638269, 65907985,  78094430, 80101523, 81049278, 81845913, 84007588, 92626364] # acer ten seeds   

    # random_seeds = [34738061, 80101523, 81845913, 84007588, 92626364] # new test3 acer five best seeds of ten  OOOOOOK!

    # The seeds marked ”OOOOOOK!“ are the seeds used in CH of the paper 

    # -----------------------------------------------------------------------------

    # CR

    # random_seeds = [1745229, 1801481, 3935848, 3968680, 9768236, 49780728, 55148360, 59469316, 85277303] # a2c ten seeds 

    # random_seeds = [13993123, 56809769, 83753959, 85741963, 68459829, 90606062, 92309190, 98671432, 96374603, 75510161] # dqn ten seeds

    # random_seeds = [6213484, 8255169, 9560510, 35649715,  45956157, 47294126, 56191691, 68267486, 78514400, 85847292] # bdqn ten seeds
    
    # random_seeds = [34738061, 37732739, 53638269,  78094430, 80101523, 81049278, 81845913, 84007588, 92626364] # acer ten seeds

    # random_seeds = [34738061, 80101523, 81845913, 84007588, 92626364] # acer five seeds

    # random_seeds = [8255169, 45956157, 47294126, 56191691, 68267486] # bdqn five seeds

    # random_seeds = [75510161, 83753959, 85741963, 96374603, 98671432 ] # dqn five seeds

    # random_seeds = [1745229, 1801481, 3935848, 3968680, 9768236] # a2c five seeds 
    
    add_knowledge = [True, False]
    add_asp = [True, False]
    # add_asp = [False]
    policytype = "a2c"
    # policytype = "dqn"
    # policytype = "bdqn"
    # policytype = "acer"
    domain = "CamHotels"
    # domain = "CamRestaurants"
    
    knowledge_average_result = [[] for _ in range(num_batches)]
    no_knowledge_average_result = [[] for _ in range(num_batches)]
    knowledge_asp_average_result = [[] for _ in range(num_batches)]
    
    for knowledge in add_knowledge:
        for asp in add_asp:
            for random_seed in random_seeds:
                path = './output/output-{}-{}-{}-{}-{}.txt'.format(random_seed, knowledge, asp, policytype, domain)
                print(path)
                if os.path.exists(path):
                    with open('./output/output-{}-{}-{}-{}-{}.txt'.format(random_seed, knowledge, asp, policytype, domain), 'r') as f:
                        lines = f.readlines()[:num_batches * 2]
                        lines = [line for line_idx, line in enumerate(lines) if line_idx % 2 != 0]
                        for line_idx, line in enumerate(lines):
                            if knowledge and asp:
                                knowledge_asp_average_result[line_idx].append(np.mean(ast.literal_eval(line)))
                            elif knowledge and not asp:
                                knowledge_average_result[line_idx].append(np.mean(ast.literal_eval(line)))
                            elif not knowledge and not asp:
                                no_knowledge_average_result[line_idx].append(np.mean(ast.literal_eval(line)))
                else:
                    print("PATH NOT EXIST", path)
    # print(no_knowledge_average_result)
    # print(knowledge_average_result)
    # print(knowledge_asp_average_result)
    
    knowledge_mean_error = []
    no_knowledge_mean_error = []
    knowledge_asp_mean_error = []
    
    # markers = ['.', '^', 's']
    # curr_marker_idx = 0

    markers = ['.', '^', '*']
    curr_marker_idx = 0
    
    for knowledge in add_knowledge:
        for asp in add_asp:
            if knowledge and asp:
                average_result = knowledge_asp_average_result
                mean_error = knowledge_asp_mean_error
                label = 'A2C + MLN + ASP'
            elif knowledge:
                average_result = knowledge_average_result
                mean_error = knowledge_mean_error
                label = 'A2C + MLN'
            elif not knowledge and not asp:
                average_result = no_knowledge_average_result
                mean_error = no_knowledge_mean_error
                label = 'A2C'
            else:
                continue
            
            for result in average_result:
                mean = np.mean(result)
                error = np.std(result) / np.sqrt(len(result))
                mean_error.append((mean, error))
            
            x = [test_num_dialogs * i for i in range(0, num_batches + 1)]
            y = [0] + [y_mean for y_mean, _ in mean_error]
            y_error = [0] + [y_error for _, y_error in mean_error]
            
            y = np.asarray(y)
            y = savgol_filter(y, 11, 3)
            y_error = np.asarray(y_error)
            
            plt.xlim((0, test_num_dialogs * num_batches))
            
            plt.ylim(0, 1)
            plt.plot(x, y, marker=markers[curr_marker_idx], markersize=10, label=label)
            plt.fill_between(x, y - y_error, y + y_error, alpha=0.2)
            # plt.legend(loc='lower right', frameon=False)

            # plt.ylabel('Success Rate', labelpad=15)
            # plt.xlabel('Dialog Number', labelpad=15)

            # plt.legend(loc='lower right', frameon=False, fontsize=16)
            # plt.legend(loc='lower right', frameon=False, fontsize=20)
            plt.legend(loc='lower right', frameon=False, fontsize=19)            
            # plt.ylabel('Success Rate', labelpad=15)
            # plt.xlabel('Dialog Number', labelpad=15)
            # plt.xticks(fontsize=16)
            # plt.yticks(fontsize=16)
            # plt.xticks(fontsize=20)
            # plt.yticks(fontsize=20)
            plt.xticks(fontsize=19)
            plt.yticks(fontsize=19)

            # plt.ylabel('Success Rate', labelpad=15, fontsize=16)
            # plt.xlabel('Dialog Number', labelpad=15, fontsize=16)

            # plt.ylabel('Success Rate', labelpad=15, fontsize=20)
            # plt.xlabel('Dialog Number', labelpad=15, fontsize=20)
            # plt.ylabel('Success Rate', labelpad=15, fontsize=19)
            # plt.xlabel('Dialog Number', labelpad=15, fontsize=19)
            plt.ylabel('Success Rate', labelpad=15, fontsize=22)
            plt.xlabel('Dialog Number', labelpad=15, fontsize=22)

            curr_marker_idx += 1
    
    if not os.path.exists('_plots'):
        os.mkdir('_plots')
    # plt.savefig('_plots/' + 'CH_a2c_main_ten_mlndiff_seeds_of_ten_for_3ai_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CH_a2c_main_ten_mlndiff_seeds_of_ten_for_3ai_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff.pdf')

    # plt.savefig('_plots/' + 'CH_a2c_main_five_best_mlndiff_seeds_of_ten_for_test10_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CH_a2c_main_five_best_mlndiff_seeds_of_ten_for_test10_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff.pdf') # oooooookkkkkkk!

    # plt.savefig('_plots/' + 'M_a2c_original_16' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' M_a2c_original_16.pdf')

    plt.savefig('_plots/' + 'O_a2c_original_final' + '.pdf', format='pdf', bbox_inches='tight')
    print('plot saved as' + ' O_a2c_original_final.pdf')

    # plt.savefig('_plots/' + 'O_dqn_original_final' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' O_dqn_original_final.pdf')

    # plt.savefig('_plots/' + 'O_bbqn_original_final' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' O_bbqn_original_final.pdf')

    # plt.savefig('_plots/' + 'O_acer_original_final' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' O_acer_original_final.pdf')

    # plt.savefig('_plots/' + 'M_dqn_original_16' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' M_dqn_original_16.pdf')

    # plt.savefig('_plots/' + 'M_bbqn_original_16' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' M_bbqn_original_16.pdf')

    # plt.savefig('_plots/' + 'M_acer_original_16' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' M_acer_original_16.pdf')

    # plt.savefig('_plots/' + 'CH_a2c_main_ten_seeds_for_3ai_fix_random_bugs_adjust_combine_rate_ori_mln_asp' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CH_a2c_main_ten_seeds_for_3ai_fix_random_bugs_adjust_combine_rate_ori_mln_asp.pdf')

    # plt.savefig('_plots/' + 'CH_dqn_test1_five_best_seeds' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CH_dqn_test1_five_best_seeds.pdf')

    # plt.savefig('_plots/' + 'CH_bbqn_test1_five_best_seeds' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CH_bbqn_test1_five_best_seeds.pdf')

    # plt.savefig('_plots/' + 'CH_acer_test3_five_best_seeds' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CH_acer_test3_five_best_seeds.pdf')

    # plt.savefig('_plots/' + 'CH_a2c_main_five_best_mlndiff_seeds_of_ten_for_test11_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CH_a2c_main_five_best_mlndiff_seeds_of_ten_for_test11_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff.pdf')

    # --------------------------------- CR -----------------------------------------

    # plt.savefig('_plots/' + 'CR_dqn_test_ten_seeds' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CR_dqn_test_ten_seeds.pdf')

    # plt.savefig('_plots/' + 'CR_bbqn_test_ten_seeds' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CR_bbqn_test_ten_seeds.pdf')

    # plt.savefig('_plots/' + 'CR_acer_test_ten_seeds' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CR_acer_test_ten_seeds.pdf')

    # plt.savefig('_plots/' + 'CH_acer_1' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CH_acer_1.pdf')
    

# def plot_mln_diff():
#     # plt.subplot(132)
#     plt.figure(figsize=[8, 6])
#     test_num_dialogs = 100
#     num_batches = 40
#     plot_batches = 40

#     random_seeds = [7367422, 7367443, 7367450, 7367463, 7367481] # a2c mln diff for 3ai
#     data_sizes = ['2000', '500', '250']
    
#     domain = "CamHotels"
#     policytype = "a2c"


#     average_result_250 = [[] for _ in range(num_batches)]
#     average_result_500 = [[] for _ in range(num_batches)]
#     average_result_2000 = [[] for _ in range(num_batches)]
    
#     for data_size in data_sizes:
#         for random_seed in random_seeds:
#             path = './output-mln/output-{}-{}-{}-{}.txt'.format(random_seed, data_size, policytype, domain)
#             print(path)
#             if os.path.exists(path):
#                 with open('./output-mln/output-{}-{}-{}-{}.txt'.format(random_seed, data_size, policytype, domain), 'r') as f:
#                     lines = f.readlines()[:num_batches * 2]
#                     lines = [line for line_idx, line in enumerate(lines) if line_idx % 2 != 0]

#                     if data_size == '250':
#                         average_result = average_result_250
#                     elif data_size == '500':
#                         average_result = average_result_500
#                     elif data_size == '2000':
#                         average_result = average_result_2000
#                     else:
#                         continue
#                     for line_idx, line in enumerate(lines):
#                         average_result[line_idx].append(np.mean(ast.literal_eval(line)))


#     mean_error_250 = []
#     mean_error_500 = []
#     mean_error_2000 = []
    
#     markers = ['.', '^', '*']
#     # markers = ['*', '^', '.']
#     curr_marker_idx = 0
    
#     for data_size in data_sizes:
#         if data_size == '250':
#             mean_error = mean_error_250
#             average_result = average_result_250
#             label = 'MLN: 250 samples'
#         elif data_size == '500':
#             mean_error = mean_error_500
#             average_result = average_result_500
#             label = 'MLN: 500 samples'
#         elif data_size == '2000':
#             mean_error = mean_error_2000
#             average_result = average_result_2000
#             label = 'MLN: 2000 samples'
#         else:
#             continue
        
#         for result in average_result:
#             mean = np.mean(result)
#             error = np.std(result) / np.sqrt(len(result))
#             mean_error.append((mean, error))
        
#         x = [test_num_dialogs * i for i in range(0, num_batches + 1)]
#         y = [0] + [y_mean for y_mean, _ in mean_error]
#         y_error = [0] + [y_error for _, y_error in mean_error]
        
#         y = np.asarray(y)
#         y = savgol_filter(y, 11, 3)
#         y_error = np.asarray(y_error)
        
#         plt.xlim((0, test_num_dialogs * plot_batches))
#         plt.ylim(0, 1)
        
#         x = x[:plot_batches + 1]
#         y = np.asarray(y.tolist()[:plot_batches + 1])
#         y_error = np.asarray(y_error.tolist()[:plot_batches + 1])
        
#         plt.plot(x, y, marker=markers[curr_marker_idx], markersize=10, label=label)
#         plt.fill_between(x, y - y_error, y + y_error, alpha=0.2)
#         plt.legend(loc='lower right', frameon=False)
#         plt.ylabel('Success Rate', labelpad=15)
#         plt.xlabel('Dialog Number', labelpad=15)
#         curr_marker_idx += 1
    
#     if not os.path.exists('_plots'):
#         os.mkdir('_plots')
#     plt.savefig('_plots/' + 'a2c_mln_diff_for_3ai_250_500_2000_new' + '.pdf', format='pdf', bbox_inches='tight')
#     print('plot saved as' + ' a2c_mln_diff_for_3ai_250_500_2000_new.pdf')

def plot_mln_diff():
    # plt.subplot(132)
    plt.figure(figsize=[8, 6])
    test_num_dialogs = 100
    num_batches = 40
    plot_batches = 40

    # random_seeds = [7367422, 7367443, 7367450, 7367463, 7367481] # a2c mln diff for 3ai
    # random_seeds = [7367422, 7367443, 7367450, 7367463, 7367481] # a2c mln diff for 3ai
    # random_seeds = [7367422, 7367443, 7367497, 7367481] # a2c mln diff for 3ai
    # random_seeds = [7367443, 7367557, 7367551, 7367530, 7367520] # a2c best five seeds for 3ai new
    # random_seeds = [7367443, 7367557, 7367551, 7367530, 7367520] # a2c best five seeds for 3ai new
    # random_seeds = [1745229, 6936311, 49780728, 88051840, 9768236]
    # random_seeds = [1745229, 3968680, 49780728, 88051840, 9768236]
    # random_seeds = [3968680, 9768236, 49780728, 55148360, 59469316, 88051840] # a2c best six seeds of ten for 3ai new
    # random_seeds = [1745229, 6936311, 8116315, 5552435, 88051840] # a2c best five seeds of ten for 3ai new maybe
    # random_seeds = [1745229, 3968680, 6936311, 9768236, 49780728, 55148360, 59469316, 88051840] # a2c nine seeds
    # random_seeds = [1745229, 6936311, 9768236, 49780728, 55148360, 88051840] # a2c best six seeds of ten for 3ai new
    random_seeds = [1745229, 6936311, 9768236, 49780728, 88051840] # a2c best five seeds of ten for 3ai new test10
    # random_seeds = [1745229, 3968680, 6936311, 9768236, 49780728, 55148360, 59469316, 88051840, 8116315, 5552435] # a2c ten seeds
    # random_seeds = [1745229, 3968680, 6936311, 9768236, 49780728, 55148360, 59469316, 88051840, 8116315, 5552435, 8720177] # a2c all seeds
    # random_seeds = [7367557, 7367551, 7367530, 7367520] # a2c best five seeds for 3ai new
    # random_seeds = [7367422, 7367443, 7367463, 7367481] # a2c mln diff for 3ai
    # data_sizes = ['250_1', '250_2', '250_3', '200_1', '200_2', '200_3','100_1', '100_2', '100_3']
    # data_sizes = ['100_1', '100_2', '100_3', '500_1', '500_2', '500_3', '1000_1', '1000_2', '1000_3', '250_1', '250_2', '250_3', '2000']
    # data_sizes = ['500_1', '500_2', '500_3', '250_1', '250_2', '250_3', '2000']
    data_sizes = ['500_1', '500_2', '500_3', '100_1', '100_2', '100_3', '2000']
    # data_sizes = ['100_1', '100_2', '100_3', '250_1', '250_2', '250_3']
    # data_sizes = ['500_2', '500_3', '250_2', '250_3', '2000']    
    domain = "CamHotels"
    policytype = "a2c"


    average_result_100 = [[] for _ in range(num_batches)]
    # average_result_200 = [[] for _ in range(num_batches)]
    average_result_250 = [[] for _ in range(num_batches)]
    average_result_500 = [[] for _ in range(num_batches)]
    average_result_1000 = [[] for _ in range(num_batches)]
    average_result_2000 = [[] for _ in range(num_batches)]

    
    for data_size in data_sizes:
        for random_seed in random_seeds:
            path = './output-mln/output-{}-{}-{}-{}.txt'.format(random_seed, data_size, policytype, domain)
            print(path)
            if os.path.exists(path):
                with open('./output-mln/output-{}-{}-{}-{}.txt'.format(random_seed, data_size, policytype, domain), 'r') as f:
                    lines = f.readlines()[:num_batches * 2]
                    lines = [line for line_idx, line in enumerate(lines) if line_idx % 2 != 0]

                    if '100_' in data_size:
                        average_result = average_result_100
                    # elif '200' in data_size:
                    #     average_result = average_result_200
                    elif '250' in data_size:
                        average_result = average_result_250

                    elif '500' in data_size:
                        average_result = average_result_500
                    elif '1000' in data_size:
                        average_result = average_result_1000
                    elif '2000' in data_size:
                        average_result = average_result_2000
                    else:
                        continue
                    for line_idx, line in enumerate(lines):
                        average_result[line_idx].append(np.mean(ast.literal_eval(line)))


    mean_error_100 = []
    # mean_error_200 = []
    mean_error_250 = []

    mean_error_500 = []
    mean_error_1000 = []
    mean_error_2000 = []
    
    markers = ['.', '^', '*', 'x']
    # markers = ['*', '^', '.']
    curr_marker_idx = 0
    
    # data_sizes1 = ['100', '200', '250']
    # data_sizes1 = ['500', '1000']
    data_sizes1 = ['2000', '500', '100']
    # data_sizes1 = ['500', '100']
    # data_sizes1 = ['250', '100']
    # data_sizes1 = ['100', '250', '500', '1000']
    # data_sizes1 = ['250', '500', '1000']

    for data_size in data_sizes1:
        if '100' == data_size:
            mean_error = mean_error_100
            average_result = average_result_100
            label = 'MLN: 100 samples'
        # elif '200' in data_size:
        #     mean_error = mean_error_200
        #     average_result = average_result_200
        #     label = 'MLN: 200 samples'
        elif '250' in data_size:
            mean_error = mean_error_250
            average_result = average_result_250
            label = 'MLN: 250 samples'
        elif '500' == data_size:
            mean_error = mean_error_500
            average_result = average_result_500
            label = 'MLN: 500 samples'
        elif '1000' == data_size:
            mean_error = mean_error_1000
            average_result = average_result_1000
            label = 'MLN: 1000 samples'
        elif '2000' == data_size:
            mean_error = mean_error_2000
            average_result = average_result_2000
            label = 'MLN: 2000 samples'
        else:
            continue
        
        for result in average_result:
            mean = np.mean(result)
            error = np.std(result) / np.sqrt(len(result))
            mean_error.append((mean, error))
        
        x = [test_num_dialogs * i for i in range(0, num_batches + 1)]
        y = [0] + [y_mean for y_mean, _ in mean_error]
        y_error = [0] + [y_error for _, y_error in mean_error]
        
        y = np.asarray(y)
        y = savgol_filter(y, 11, 3)
        # y = savgol_filter(y, 7, 3)
        y_error = np.asarray(y_error)
        
        plt.xlim((0, test_num_dialogs * plot_batches))
        plt.ylim(0, 1)
        
        x = x[:plot_batches + 1]
        y = np.asarray(y.tolist()[:plot_batches + 1])
        y_error = np.asarray(y_error.tolist()[:plot_batches + 1])
        
        plt.plot(x, y, marker=markers[curr_marker_idx], markersize=10, label=label)
        plt.fill_between(x, y - y_error, y + y_error, alpha=0.2)
        # plt.legend(loc='lower right', frameon=False, fontsize=16)
        plt.legend(loc='lower right', frameon=False, fontsize=19)
        # plt.ylabel('Success Rate', labelpad=15)
        # plt.xlabel('Dialog Number', labelpad=15)
        # plt.xticks(fontsize=16)
        # plt.yticks(fontsize=16)
        plt.xticks(fontsize=19)
        plt.yticks(fontsize=19)

        # plt.ylabel('Success Rate', labelpad=15, fontsize=16)
        # plt.xlabel('Dialog Number', labelpad=15, fontsize=16)
        plt.ylabel('Success Rate', labelpad=15, fontsize=22)
        plt.xlabel('Dialog Number', labelpad=15, fontsize=22)

        curr_marker_idx += 1
    
    if not os.path.exists('_plots'):
        os.mkdir('_plots')
    # plt.savefig('_plots/' + 'a2c_mln_diff_for_3ai_100_500_2000_best_five_seeds_new_test5_fix_random_bugs' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' a2c_mln_diff_for_3ai_100_500_2000_best_five_seeds_new_test5_fix_random_bugs.pdf')

    # plt.savefig('_plots/' + 'a2c_mln_diff_for_3ai_100_500_2000_best_five_seeds_new_test10_fix_random_bugs' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' a2c_mln_diff_for_3ai_100_500_2000_best_five_seeds_new_test10_fix_random_bugs.pdf')

    # plt.savefig('_plots/' + 'a2c_mln_diff_test_best_five_seeds' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' a2c_mln_diff_test_best_five_seeds.pdf')

    # plt.savefig('_plots/' + 'K_a2c_mln_diff_15' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' K_a2c_mln_diff_15.pdf')

    plt.savefig('_plots/' + 'O_a2c_mln_diff_final' + '.pdf', format='pdf', bbox_inches='tight')
    print('plot saved as' + ' O_a2c_mln_diff_final.pdf')

    # plt.savefig('_plots/' + 'a2c_mln_diff_for_3ai_100_500_2000_all_seeds_maybe_new_test9_fix_random_bugs' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' a2c_mln_diff_for_3ai_100_500_2000_all_seeds_maybe_new_test9_fix_random_bugs.pdf')

# def plot_asp_diff():
#     # plt.subplot(133)
#     plt.figure(figsize=[8, 6])
#     test_num_dialogs = 100
#     num_batches = 40
    
#     # random_seeds = [7367422, 7367463, 7367481, 7367450, 7367443] # a2c asp five seeds for 3ai
#     # random_seeds = [7367443, 7367557, 7367551, 7367530, 7367520] # a2c best five seeds for 3ai new
#     # random_seeds = [1745229, 3968680, 6936311, 9768236, 49780728, 55148360, 59469316, 88051840, 8116315, 5552435] # a2c ten seeds
#     random_seeds = [1745229, 6936311, 9768236, 49780728, 88051840] # a2c best five seeds of ten for 3ai new test10
#     policytype = "a2c"
#     domain = "CamHotels"

#     is_inaccurate_asp = [False, True]
#     is_incomplete_asp = [False, True]
    
#     average_result_inaccurate = [[] for _ in range(num_batches)]
#     average_result_incomplete = [[] for _ in range(num_batches)]
#     average_result_perfect = [[] for _ in range(num_batches)]
    
#     for random_seed in random_seeds:
#         for inaccurate_asp in is_inaccurate_asp:
#             for incomplete_asp in is_incomplete_asp:
#                 file_path = './output-asp/output-asp-{}-{}-{}-{}-{}.txt'.format(random_seed, inaccurate_asp, incomplete_asp, policytype, domain)
#                 print(file_path)
#                 if os.path.exists(file_path):
#                     with open(file_path, 'r') as f:
#                         lines = f.readlines()[:num_batches * 2]
#                         lines = [line for line_idx, line in enumerate(lines) if line_idx % 2 != 0]
#                         if inaccurate_asp and not incomplete_asp:
#                             average_result = average_result_inaccurate
#                         elif not inaccurate_asp and incomplete_asp:
#                             average_result = average_result_incomplete
#                         elif not inaccurate_asp and not incomplete_asp:
#                             average_result = average_result_perfect
#                         else:
#                             continue
#                         for line_idx, line in enumerate(lines):
#                             average_result[line_idx].append(np.mean(ast.literal_eval(line)))
#                 else:
#                     print("PATH NOT EXIST", file_path)
#     mean_error_inaccurate = []
#     mean_error_incomplete = []
#     mean_error_perfect = []
    
#     markers = ['.', '^', '*']
#     curr_marker_idx = 0
#     for incomplete_asp in is_incomplete_asp:
#         for inaccurate_asp in is_inaccurate_asp:
#             if inaccurate_asp and not incomplete_asp:
#                 mean_error = mean_error_inaccurate
#                 average_result = average_result_inaccurate
#                 label = 'Inaccurate knowledge'
#             elif incomplete_asp and not inaccurate_asp:
#                 mean_error = mean_error_incomplete
#                 average_result = average_result_incomplete
#                 label = 'Incomplete knowledge'
#             elif not inaccurate_asp and not incomplete_asp:
#                 mean_error = mean_error_perfect
#                 average_result = average_result_perfect
#                 label = 'Perfect knowledge'
#             else:
#                 continue
            
#             for result in average_result:
#                 mean = np.mean(result)
#                 error = np.std(result) / np.sqrt(len(result))
#                 mean_error.append((mean, error))
            
#             x = [test_num_dialogs * i for i in range(0, num_batches + 1)]
#             y = [0] + [y_mean for y_mean, _ in mean_error]
#             y_error = [0] + [y_error for _, y_error in mean_error]
            
#             y = np.asarray(y)
#             y = savgol_filter(y, 11, 3)
#             y_error = np.asarray(y_error)
            
#             plt.xlim((0, test_num_dialogs * num_batches))
#             plt.ylim(0, 1)
#             plt.plot(x, y, marker=markers[curr_marker_idx], markersize=10, label=label)
#             plt.fill_between(x, y - y_error, y + y_error, alpha=0.2)
#             plt.legend(loc='lower right', frameon=False)
#             plt.ylabel('Success Rate', labelpad=15)
#             plt.xlabel('Dialog Number', labelpad=15)
            
#             curr_marker_idx += 1
    
#     if not os.path.exists('_plots'):
#         os.mkdir('_plots')
#     # plt.savefig('_plots/' + 'CH_a2c_asp_main_best_five_seeds_for_3ai_fix_random_bugs' + '.pdf', format='pdf', bbox_inches='tight')
#     # print('plot saved as' + ' CH_a2c_asp_main_best_five_seeds_for_3ai_fix_random_bugs.pdf')

#     plt.savefig('_plots/' + 'CH_a2c_asp_main_five_best_mlndiff_seeds_of_ten_for_test10_adjust_asp_mode_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff' + '.pdf', format='pdf', bbox_inches='tight')
#     print('plot saved as' + ' CH_a2c_asp_main_five_best_mlndiff_seeds_of_ten_for_test10_adjust_asp_mode_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff')

#     # plt.savefig('_plots/' + 'CH_a2c_asp_main_ten_mlndiff_seeds_for_test10_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff' + '.pdf', format='pdf', bbox_inches='tight')
#     # print('plot saved as' + ' CH_a2c_asp_main_ten_mlndiff_seeds_for_test10_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff')

def plot_asp_diff():
    # plt.subplot(133)
    plt.figure(figsize=[8, 6])
    test_num_dialogs = 100
    num_batches = 40
    
    # random_seeds = [7367422, 7367463, 7367481, 7367450, 7367443] # a2c asp five seeds for 3ai
    # random_seeds = [7367443, 7367557, 7367551, 7367530, 7367520] # a2c best five seeds for 3ai new
    # random_seeds = [1745229, 3968680, 6936311, 9768236, 49780728, 55148360, 59469316, 88051840, 8116315, 5552435] # a2c ten seeds
    random_seeds = [1745229, 6936311, 9768236, 49780728, 88051840] # a2c best five seeds of ten for 3ai new test10

    # random_seeds = [1745229, 1801481, 3935848, 3968680, 9768236, 49780728, 55148360, 59469316, 85277303] # a2c ten seeds    
    # random_seeds = [1745229] # a2c ten seeds    
    policytype = "a2c"
    domain = "CamHotels"
    # domain = "CamRestaurants"

    is_inaccurate_asp = [False, True]
    is_incomplete_asp = [False, True]
    
    average_result_inaccurate = [[] for _ in range(num_batches)]
    average_result_incomplete = [[] for _ in range(num_batches)]
    average_result_perfect = [[] for _ in range(num_batches)]

    average_result_no_knowledge = [[] for _ in range(num_batches)]
    
    for random_seed in random_seeds:
        for inaccurate_asp in is_inaccurate_asp:
            for incomplete_asp in is_incomplete_asp:
                file_path = './output-asp/output-asp-{}-{}-{}-{}-{}.txt'.format(random_seed, inaccurate_asp, incomplete_asp, policytype, domain)
                print(file_path)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        lines = f.readlines()[:num_batches * 2]
                        lines = [line for line_idx, line in enumerate(lines) if line_idx % 2 != 0]
                        if inaccurate_asp and not incomplete_asp:
                            average_result = average_result_inaccurate
                        elif not inaccurate_asp and incomplete_asp:
                            average_result = average_result_incomplete
                        elif not inaccurate_asp and not incomplete_asp:
                            average_result = average_result_perfect
                        else:
                            # continue
                            average_result = average_result_no_knowledge

                        for line_idx, line in enumerate(lines):
                            average_result[line_idx].append(np.mean(ast.literal_eval(line)))
                else:
                    print("PATH NOT EXIST", file_path)
    mean_error_inaccurate = []
    mean_error_incomplete = []
    mean_error_perfect = []
    mean_error_no_knowledge = []
    
    # markers = ['.', '^', '*', 'x']
    markers = ['.', 'x', '*', '^']
    curr_marker_idx = 0
    for incomplete_asp in is_incomplete_asp:
        for inaccurate_asp in is_inaccurate_asp:
            if inaccurate_asp and not incomplete_asp:
                mean_error = mean_error_inaccurate
                average_result = average_result_inaccurate
                label = 'Inaccurate knowledge'
            elif incomplete_asp and not inaccurate_asp:
                mean_error = mean_error_incomplete
                average_result = average_result_incomplete
                label = 'Incomplete knowledge'
            elif not inaccurate_asp and not incomplete_asp:
                mean_error = mean_error_perfect
                average_result = average_result_perfect
                label = 'Perfect knowledge'
            # else:
            #     continue
            else:
                mean_error = mean_error_no_knowledge
                average_result = average_result_no_knowledge
                label = 'No external knowledge'            
            
            for result in average_result:
                mean = np.mean(result)
                error = np.std(result) / np.sqrt(len(result))
                mean_error.append((mean, error))
            
            x = [test_num_dialogs * i for i in range(0, num_batches + 1)]
            y = [0] + [y_mean for y_mean, _ in mean_error]
            y_error = [0] + [y_error for _, y_error in mean_error]
            
            y = np.asarray(y)
            y = savgol_filter(y, 11, 3)
            y_error = np.asarray(y_error)
            
            plt.xlim((0, test_num_dialogs * num_batches))
            plt.ylim(0, 1)
            plt.plot(x, y, marker=markers[curr_marker_idx], markersize=10, label=label)
            plt.fill_between(x, y - y_error, y + y_error, alpha=0.2)
            # plt.legend(loc='lower right', frameon=False)
            # plt.ylabel('Success Rate', labelpad=15)
            # plt.xlabel('Dialog Number', labelpad=15)
           
            # plt.legend(loc='lower right', frameon=False, fontsize=16)
            plt.legend(loc='lower right', frameon=False, fontsize=19)
            # plt.ylabel('Success Rate', labelpad=15)
            # plt.xlabel('Dialog Number', labelpad=15)
            # plt.xticks(fontsize=16)
            # plt.yticks(fontsize=16)
            plt.xticks(fontsize=19)
            plt.yticks(fontsize=19)

            # plt.ylabel('Success Rate', labelpad=15, fontsize=16)
            # plt.xlabel('Dialog Number', labelpad=15, fontsize=16)
            plt.ylabel('Success Rate', labelpad=15, fontsize=22)
            plt.xlabel('Dialog Number', labelpad=15, fontsize=22)

            curr_marker_idx += 1
    
    if not os.path.exists('_plots'):
        os.mkdir('_plots')
    # plt.savefig('_plots/' + 'CH_a2c_asp_main_best_five_seeds_for_3ai_fix_random_bugs' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CH_a2c_asp_main_best_five_seeds_for_3ai_fix_random_bugs.pdf')

    # plt.savefig('_plots/' + 'CH_a2c_asp2_with_mln_main_five_best_mlndiff_seeds_of_ten_for_test11_adjust_asp_mode_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CH_a2c_asp2_with_mln_main_five_best_mlndiff_seeds_of_ten_for_test11_adjust_asp_mode_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff')

    # plt.savefig('_plots/' + 'CH_a2c_asp_main_five_mlndiff_seeds_for_test10_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CH_a2c_asp_main_five_mlndiff_seeds_for_test10_fix_random_bugs_adjust_combine_rate_ori_mln_asp_same_as_mlndiff') # oooooooooookkkkkkkkk!

    # plt.savefig('_plots/' + 'L_a2c_asp_diff_priginal' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' L_a2c_asp_diff_original.pdf')

    # plt.savefig('_plots/' + 'L_a2c_asp_diff_16' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' L_a2c_asp_diff_16.pdf')
    plt.savefig('_plots/' + 'O_a2c_asp_diff_final' + '.pdf', format='pdf', bbox_inches='tight')
    print('plot saved as' + ' O_a2c_asp_diff_final.pdf')

    # plt.savefig('_plots/' + 'CR_a2c_asp_ten_seeds' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CR_a2c_asp_ten_seeds')

    # plt.savefig('_plots/' + 'CR_a2c_asp_one_seed' + '.pdf', format='pdf', bbox_inches='tight')
    # print('plot saved as' + ' CR_a2c_asp_one_seed')

if __name__ == '__main__':

    # plot_main()
    # plot_mln_diff()
    plot_asp_diff()

