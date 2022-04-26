from pgmpy.models.BayesianModel import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.sampling import BayesianModelSampling
import numpy as np
import dill
import os


def construct_model(save_goal=False):
    # define models
    model = BayesianModel([('kind', 'pricerange'), ('stars', 'pricerange')])
    
    # kind: guesthouse, hotel, dontcare
    cpd_area = TabularCPD(variable='kind', variable_card=3,
                          values=[[0.45, 0.45, 0.1]])
    # stars: 0, 2, 3, 4, Dontcare
    cpd_stars = TabularCPD(variable='stars', variable_card=5,
                           values=[[0.1, 0.1, 0.2, 0.55, 0.05]])
    
    # price range: Cheap, Moderate, Expensive
    pricerange_values = []
    for i, star in enumerate(['0', '2', '3', '4', 'Dontcare']):
        for j, kind in enumerate(['Guesthouse', 'Hotel', 'Dontcare']):
            if star == '0' and kind == 'Guesthouse':
                pricerange_values.append([0.2, 0.65, 0.1, 0.05])
            elif star == '0' and kind == 'Hotel':
                pricerange_values.append([0.1, 0.2, 0.65, 0.05])
            elif star == '0' and kind == 'Dontcare':
                pricerange_values.append([0.15, 0.4, 0.4, 0.05])
            elif star == '2' and kind == 'Guesthouse':
                pricerange_values.append([0.1, 0.75, 0.1, 0.05])
            elif star == '2' and kind == 'Hotel':
                pricerange_values.append([0.1, 0.1, 0.75, 0.05])
            elif star == '2' and kind == 'Dontcare':
                pricerange_values.append([0.15, 0.4, 0.4, 0.05])
            elif star == '3' and kind == 'Guesthouse':
                pricerange_values.append([0.1, 0.75, 0.1, 0.05])
            elif star == '3' and kind == 'Hotel':
                pricerange_values.append([0.1, 0.1, 0.75, 0.05])
            elif star == '3' and kind == 'Dontcare':
                pricerange_values.append([0.15, 0.3, 0.5, 0.05])
            elif star == '4' and kind == 'Guesthouse':
                pricerange_values.append([0.1, 0.25, 0.6, 0.05])
            elif star == '4' and kind == 'Hotel':
                pricerange_values.append([0.05, 0.05, 0.85, 0.05])
            elif star == '4' and kind == 'Dontcare':
                pricerange_values.append([0.1, 0.15, 0.7, 0.05])
            elif star == 'Dontcare' and kind == 'Guesthouse':
                pricerange_values.append([0.1, 0.75, 0.1, 0.05])
            elif star == 'Dontcare' and kind == 'Hotel':
                pricerange_values.append([0.05, 0.05, 0.85, 0.05])
            elif star == 'Dontcare' and kind == 'Dontcare':
                pricerange_values.append([0.1, 0.2, 0.65, 0.05])
    
    pricerange_values = np.asarray(pricerange_values).transpose().tolist()
    
    cpd_pricerange = TabularCPD(variable='pricerange', variable_card=4,
                                values=pricerange_values,
                                evidence=['kind', 'stars'],
                                evidence_card=[3, 5])
    
    model.add_cpds(cpd_area, cpd_stars, cpd_pricerange)
    
    model.check_model()
    
    
    if save_goal:
        goal_sampling = GoalSampling(BayesianModelSampling(model))
        goal_sampling.sample(num_samples=10000)
        
        file_path = os.path.join(os.path.dirname(__file__), 'bn_inference.pkl')
        with open(file_path, 'wb') as f:
            dill.dump(goal_sampling, f, protocol=2)
            print(file_path + ' created!')
    
    return model


class GoalSampling:
    def __init__(self, bn_model_sampling):
        self.star_mapping = {0: '0', 1: '2', 2: '3', 3: '4', 4: 'Dontcare'}
        self.price_mapping = {0: 'Cheap', 1: 'Moderate', 2: 'Expensive', 3: 'Dontcare'}
        self.area_mapping = {0: 'North', 1: 'South', 2: 'East', 3: 'West', 4: 'Centre', 5: 'Dontcare'}
        self.kind_mapping = {0: 'Guesthouse', 1: 'Hotel', 2: 'Dontcare'}
        
        self.mapping = {
            'stars': self.star_mapping,
            'pricerange': self.price_mapping,
            'area': self.area_mapping,
            'kind': self.kind_mapping
        }
        
        self.area_now_options = ['north', 'south', 'east', 'west', 'centre']
        
        self.sampling = bn_model_sampling
        self.external_factors_prob_dist = {
            # weather_now: bad, good
            'weather_now': [0.8, 0.2],
            # traffic_now: bad, good
            'traffic_now': [0.8, 0.2],
            # area_now: North, South, East, West, Centre
            'area_now': [0.2] * 5
        }
        self.other_slots = {
            'hasparking': [0.5, 0.5],
            'kind': [0.5, 0.5]
        }
        self.topological_order = self.sampling.topological_order
        self.samples = []
        self.index = 0
        self.flag = False
    
    def sample(self, num_samples):
        samples = self.sampling.forward_sample(size=num_samples, return_type='recarray')
        
        for sample in samples:
            # sample external factors
            external_factors = []
            slots = []
            for external_key, prob_dist in self.external_factors_prob_dist.items():
                if external_key == 'weather_now' or external_key == 'traffic_now':
                    external_factors.append((external_key, np.random.choice(['0', '1'], p=prob_dist)))
                else:
                    external_factors.append((external_key, np.random.choice(self.area_now_options, p=prob_dist)))
                    
            for slot_val_idx, slot in enumerate(self.topological_order):
                slots.append((slot, (self.mapping[slot][sample[slot_val_idx]]).lower()))

            self.samples.append((external_factors, slots))
    
    def sample_next_goal(self):
        # import random

        # from utils import Settings
        # # import Settings.random as random

        # # import numpy.random as random

        # if not self.flag:
        #     Settings.random.shuffle(self.samples)
        #     self.flag = True


        # "100" is train/test batch size

        if self.index == 100:
            self.index = 0

        # with open('./venues_len_tests1.txt', 'a+') as f:
        #     f.write("index: "+str(self.index) + "\n")

        # if self.index == len(self.samples):
        #     self.index = 0

            
        constraint = self.samples[self.index]
        self.index += 1
        return constraint


def sample_training_data(sample_size, save_path, save_goal=False):
    model = construct_model(save_goal)
    sampling = BayesianModelSampling(model)
    convert_to_triaining_data(sampling, sample_size=sample_size, save_path=save_path)


def convert_to_triaining_data(sampling, sample_size=2000, save_path='simulated_train.db'):
    # area_options = ['North', 'South', 'East', 'West', 'Centre', 'Dontcare']
    # parking_options = ['Hasparking', 'Noparking', 'Dontcare']
    # star_options = ['0', '2', '3', '4', 'Dontcare']
    
    kind_mapping = {0: 'Guesthouse', 1: 'Hotel', 2: 'KindDontcare'}
    star_mapping = {0: '0', 1: '2', 2: '3', 3: '4', 4: '5'}
    price_mapping = {0: 'Cheap', 1: 'Moderate', 2: 'Expensive', 3: 'PriceDontcare'}
    area_mapping = {0: 'North', 1: 'South', 2: 'East', 3: 'West', 4: 'Centre', 5: 'Dontcare'}
    
    mapping = {
        'stars': star_mapping,
        'pricerange': price_mapping,
        'area': area_mapping,
        'kind': kind_mapping
    }
    
    samples = sampling.forward_sample(size=sample_size, return_type='recarray')
    with open(save_path, 'w') as f:
        for user_id, sample in enumerate(samples):
            slots = sampling.topological_order
            f.write('User({})\n'.format(user_id))
            for slot_idx, slot in enumerate(slots):
                f.write('{}({}, {})\n'.format(slot.capitalize(), user_id, mapping[slot][sample[slot_idx]]))
    
    from collections import defaultdict
    info = dict()
    for sample in samples:
        slots = sampling.topological_order
        for slot_idx, slot in enumerate(slots):
            if slot not in info:
                info[slot] = dict()
            if mapping[slot][sample[slot_idx]] not in info[slot]:
                info[slot][mapping[slot][sample[slot_idx]]] = 0
            info[slot][mapping[slot][sample[slot_idx]]] += 1
    
    for slot, slot_val_freq in info.items():
        for slot_val in slot_val_freq.keys():
            print('{} = {}, prob: {}'.format(slot, slot_val, slot_val_freq[slot_val] / sample_size))


# added by zzc
def uniform_sampling_from_2000_samples(db_path, sample_str):

    # import sys
    # os.chdir(os.path.dirname(sys.argv[0]))
    complete_str = 'simulated_train_' + sample_str + '.db' 
    sample_total_size = 2000
    sample_size = int(sample_str[:sample_str.find('_')])
    sample_index_list = sorted(np.random.choice(sample_total_size, size=sample_size, replace=False))  
    save_path = os.path.join(os.path.dirname(__file__), complete_str)

    # with open(save_path_200_1, 'w') as f:
    with open(db_path, 'r') as f: 
        lines = f.readlines()
        f.close()

    with open(save_path, 'w') as f_new:
        count = -1
        index = 0
        # num = 0
        user_id = 0
        # for item in sample_index_list:    
        for line in lines:
            count = count + 1
            if count >= sample_index_list[index]*4 and count <= sample_index_list[index]*4+3:

                if 'User' in line:
                    # print line
                    line = line.replace(line[line.find('(')+1:line.find(')')], str(user_id), 1)
                    # print line
                else:
                    # print line
                    line = line.replace(line[line.find('(')+1:line.find(', ')], str(user_id), 1)
                    # print line                    
                f_new.write(line)
                if count == sample_index_list[index]*4+3:
                    user_id = user_id + 1
                    index = index + 1
                    if index == len(sample_index_list):
                        break 
            

        f_new.close()
    # for item in sample_index_list:
            
    #     with open(save_path_200, 'r') as f1: 


if __name__ == '__main__':
    # construct_model(save_goal=True)
    # sample_training_data(sample_size=100, save_path='simulated_train_100.db', save_goal=False)
    # sample_training_data(sample_size=250, save_path='simulated_train_250.db', save_goal=False)
    # sample_training_data(sample_size=300, save_path='simulated_train_300.db', save_goal=False)
    # sample_training_data(sample_size=500, save_path='simulated_train_500.db', save_goal=False)
    # sample_training_data(sample_size=700, save_path='simulated_train_700.db', save_goal=False)
    # sample_training_data(sample_size=900, save_path='simulated_train_900.db', save_goal=False)
    # sample_training_data(sample_size=1000, save_path='simulated_train_1000.db', save_goal=False)
    # sample_training_data(sample_size=1500, save_path='simulated_train_1500.db', save_goal=False)

    # file_path = os.path.join(os.path.dirname(__file__), 'simulated_train_250.db')
    # sample_training_data(sample_size=250, save_path=file_path, save_goal=False)

    # file_path = os.path.join(os.path.dirname(__file__), 'simulated_train_500.db')
    # sample_training_data(sample_size=500, save_path=file_path, save_goal=False)

    # file_path = os.path.join(os.path.dirname(__file__), 'simulated_train_1000.db')
    # sample_training_data(sample_size=1000, save_path=file_path, save_goal=False)

    # file_path = os.path.join(os.path.dirname(__file__), 'simulated_train_2000.db')
    # sample_training_data(sample_size=2000, save_path=file_path, save_goal=False)

    # file_path = os.path.join(os.path.dirname(__file__), 'simulated_train_100.db')
    # sample_training_data(sample_size=100, save_path=file_path, save_goal=False)

    # file_path = os.path.join(os.path.dirname(__file__), 'simulated_train_50.db')
    # sample_training_data(sample_size=50, save_path=file_path, save_goal=False)

    # uniform_sampling_from_2000_samples('simulated_train_2000.db','100_1')
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','100_2')  
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','100_3')
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','200_1')
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','200_2')  
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','200_3')
    np.random.seed(2022)
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','250_1')
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','250_2')  
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','250_3')
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','500_1')
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','500_2')  
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','500_3')

    uniform_sampling_from_2000_samples('simulated_train_2000.db','100_1')
    uniform_sampling_from_2000_samples('simulated_train_2000.db','100_2')  
    uniform_sampling_from_2000_samples('simulated_train_2000.db','100_3')
    uniform_sampling_from_2000_samples('simulated_train_2000.db','500_1')
    uniform_sampling_from_2000_samples('simulated_train_2000.db','500_2')  
    uniform_sampling_from_2000_samples('simulated_train_2000.db','500_3')

    # uniform_sampling_from_2000_samples('simulated_train_2000.db','1000_1')
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','1000_2')  
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','1000_3')

    # uniform_sampling_from_2000_samples('simulated_train_2000.db','1000_70')  
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','1000_80')  
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','1000_90')  
    # uniform_sampling_from_2000_samples('simulated_train_2000.db','2000_1')      

    # sample_training_data(sample_size=2000, save_path='simulated_train_2000.db', save_goal=False)
    pass
