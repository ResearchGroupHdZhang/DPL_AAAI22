from pgmpy.models.BayesianModel import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.sampling import BayesianModelSampling
import numpy as np
import dill
import os

# from utils import Settings
# import Settings.random as random

def construct_model(save_goal=False):
    # define models
    model = BayesianModel([('food', 'pricerange')])
    
    # kind: guesthouse, hotel, dontcare
    # food: ["indian", "chinese", "italian", "british", "european"], Dontcare
    cpd_food = TabularCPD(variable='food', variable_card=6,
                          values=[[0.18, 0.18, 0.18, 0.18, 0.18, 0.1]])
    # stars: 0, 2, 3, 4, Dontcare
    # food -> price range
    
    food_values = ["indian", "chinese", "italian", "british", "european", 'Dontcare']
    # price range: Cheap, Moderate, Expensive, dontcare
    pricerange_values = []
    for food in food_values:
        if food == 'indian':
            pricerange_values.append([0.2, 0.65, 0.1, 0.05])
        elif food == 'chinese':
            pricerange_values.append([0.1, 0.75, 0.1, 0.05])
        elif food == 'italian':
            pricerange_values.append([0.1, 0.1, 0.75, 0.05])
        elif food == 'british':
            pricerange_values.append([0.05, 0.05, 0.85, 0.05])
        elif food == 'european':
            pricerange_values.append([0.1, 0.2, 0.65, 0.05])
        elif food == 'Dontcare':
            pricerange_values.append([0.1, 0.2, 0.65, 0.05])

    # for i, star in enumerate(['0', '2', '3', '4', 'Dontcare']):
    #     for j, kind in enumerate(['Guesthouse', 'Hotel', 'Dontcare']):
    #         if star == '0' and kind == 'Guesthouse':
    #             pricerange_values.append([0.2, 0.65, 0.1, 0.05])
    #         elif star == '0' and kind == 'Hotel':
    #             pricerange_values.append([0.1, 0.2, 0.65, 0.05])
    #         elif star == '0' and kind == 'Dontcare':
    #             pricerange_values.append([0.15, 0.4, 0.4, 0.05])
    #         elif star == '2' and kind == 'Guesthouse':
    #             pricerange_values.append([0.1, 0.75, 0.1, 0.05])
    #         elif star == '2' and kind == 'Hotel':
    #             pricerange_values.append([0.1, 0.1, 0.75, 0.05])
    #         elif star == '2' and kind == 'Dontcare':
    #             pricerange_values.append([0.15, 0.4, 0.4, 0.05])
    #         elif star == '3' and kind == 'Guesthouse':
    #             pricerange_values.append([0.1, 0.75, 0.1, 0.05])
    #         elif star == '3' and kind == 'Hotel':
    #             pricerange_values.append([0.1, 0.1, 0.75, 0.05])
    #         elif star == '3' and kind == 'Dontcare':
    #             pricerange_values.append([0.15, 0.3, 0.5, 0.05])
    #         elif star == '4' and kind == 'Guesthouse':
    #             pricerange_values.append([0.1, 0.25, 0.6, 0.05])
    #         elif star == '4' and kind == 'Hotel':
    #             pricerange_values.append([0.05, 0.05, 0.85, 0.05])
    #         elif star == '4' and kind == 'Dontcare':
    #             pricerange_values.append([0.1, 0.15, 0.7, 0.05])
    #         elif star == 'Dontcare' and kind == 'Guesthouse':
    #             pricerange_values.append([0.1, 0.75, 0.1, 0.05])
    #         elif star == 'Dontcare' and kind == 'Hotel':
    #             pricerange_values.append([0.05, 0.05, 0.85, 0.05])
    #         elif star == 'Dontcare' and kind == 'Dontcare':
    #             pricerange_values.append([0.1, 0.2, 0.65, 0.05])
    
    pricerange_values = np.asarray(pricerange_values).transpose().tolist()
    
    cpd_pricerange = TabularCPD(variable='pricerange', variable_card=4,
                                values=pricerange_values,
                                evidence=['food'],
                                evidence_card=[6])
    
    model.add_cpds(cpd_food, cpd_pricerange)
    
    model.check_model()
    
    
    if save_goal:
        goal_sampling = GoalSampling(BayesianModelSampling(model))
        goal_sampling.sample(num_samples=10000)
        
        file_path = os.path.join(os.path.dirname(__file__), 'bn_inference.pkl')
        with open(file_path, 'wb') as f:
            dill.dump(goal_sampling, f, protocol=2)
            print(file_path + ' created!')
    
    return model

#     food_values = ["indian", "chinese", "italian", "british", "european", 'Dontcare']
class GoalSampling:
    def __init__(self, bn_model_sampling):
        # self.star_mapping = {0: '0', 1: '2', 2: '3', 3: '4', 4: 'Dontcare'}
        self.price_mapping = {0: 'Cheap', 1: 'Moderate', 2: 'Expensive', 3: 'Dontcare'}
        self.area_mapping = {0: 'North', 1: 'South', 2: 'East', 3: 'West', 4: 'Centre', 5: 'Dontcare'}
        # @Jerry TODO: Should be upper case?? P1
        self.food_mapping = {0: 'indian', 1: 'chinese', 2: 'italian', 3:'british', 4:'european', 5:'Dontcare'}
        
        self.mapping = {
            # 'stars': self.star_mapping,
            'pricerange': self.price_mapping,
            'area': self.area_mapping,
            'food': self.food_mapping
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
            'food': [0.2] * 5
            # TODO: @Jerry should we remove food?
            # 'kind': [0.5, 0.5]
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

        # with open('./venues_len_tests2.txt', 'a+') as f:
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
    
    price_mapping = {0: 'Cheap', 1: 'Moderate', 2: 'Expensive', 3: 'PriceDontcare'}
    area_mapping = {0: 'North', 1: 'South', 2: 'East', 3: 'West', 4: 'Centre', 5: 'AreaDontcare'}
    food_mapping = {0: 'Indian', 1: 'Chinese', 2: 'Italian', 3:'British', 4:'European', 5:'FoodDontcare'}
    
    mapping = {
        # 'stars': self.star_mapping,
        'pricerange': price_mapping,
        'area': area_mapping,
        'food': food_mapping
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

    file_path = os.path.join(os.path.dirname(__file__), 'simulated_train_2000.db')
    sample_training_data(sample_size=2000, save_path=file_path, save_goal=False)

    # for data_size in [25, 50, 100]:
    #     sample_training_data(sample_size=data_size, save_path='simulated_train_{}.db'.format(data_size), save_goal=False)
    pass
