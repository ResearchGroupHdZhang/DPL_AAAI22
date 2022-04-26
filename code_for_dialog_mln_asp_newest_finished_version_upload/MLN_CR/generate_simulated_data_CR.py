import sqlite3
import os
import numpy as np
from pprint import pprint

def get_names():
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'ontology/ontologies/CamRestaurants-dbase.db')
    )
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    param = '''SELECT name from CamRestaurants'''
    cursor.execute(param)
    rows = cursor.fetchall()
    
    with open('all_restaurant_names.json', 'w') as f:
        # names = dict()
        names = []
        for row in rows:
            names.append(row[0])
        names = sorted(names)

        import json
        json.dump(names, f)
    
    cursor.close()


def insert_random_entries(id, name, pricerange, food, area,
                          phone='not available',
                          addr='not available', postcode='not available',
                          description='not available', signature='not available'):
    try:
        path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'ontology/ontologies/CamRestaurants-dbase.db')
        )
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        
        param = '''INSERT INTO CamRestaurants (id, name,addr,area,food,phone,pricerange, postcode, 
        signature, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        
        data_tuple = (id, name, addr, area, food, phone, pricerange, postcode, signature, description)
        
        cursor.execute(param, data_tuple)
        conn.commit()
        
        cursor.close()
    
    except sqlite3.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()
            print('connection is closed')


def deduct_current_entries(all_combo):
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'ontology/ontologies/CamRestaurants-dbase.db')
    )
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    param = '''SELECT pricerange, food, area FROM CamRestaurants'''
    cursor.execute(param)
    rows = cursor.fetchall()
    for row in rows:
        key = ','.join(row)
        if all_combo[key] > 0:
            # print('match ', row)
            all_combo[key] -= 1
            if all_combo[key] < 0:
                raise ValueError(key)

def insert_all_combo():
    all_combo = {}
    
    price_options = ['cheap', 'moderate', 'expensive']
    # len(food) = 91
    food_options = [
            "indian",
            "chinese",
            "italian",
            "british",
            "european"
        ]
    area_options = ['north', 'west', 'south', 'centre', 'east']
    # parking_option = ['0', '1']
    import random
    for p in price_options:
        for f in food_options:
            for a in area_options:
                key = ','.join([p,f,a])
                all_combo[key] = 1

    deduct_current_entries(all_combo)
    
    entry_id = 30000
    pprint(sum(all_combo.values()))
    while sum(all_combo.values()) > 0:
        pricerange = np.random.choice(price_options)
        food = np.random.choice(food_options)
        name = food + str(entry_id)
        area = np.random.choice(area_options)
        # hasparking = np.random.choice(parking_option)
        
        phone = '12233600' + str(entry_id)
        addr = name + 'addr'
        postcode = name + 'postcode'
        # internet = np.random.choice(['0', '1'])
        description = name + '_desc'
        signature = name + '_signature'

        curr_key = ','.join([pricerange, food, area])
        if all_combo[curr_key] > 0:
            # def insert_random_entries(id, name, pricerange, food, area, hasparking,
            #               phone='not available',
            #               addr='not available', postcode='not available',
            #               hasinternet='not available', description='not available', signature='not available'):
            insert_random_entries(entry_id, name, pricerange, food, area,
                                 phone, addr, postcode, description)
            all_combo[curr_key] -= 1
            entry_id += 1


def generate_conditional_test_data():
    person_id = 4001
    info = {
        'Pricerange': ['Cheap', 'Moderate', 'Expensive', 'PriceDontcare'],
        'Food': ["Indian", "Chinese", "Italian", "British", "European", 'FoodDontcare']
    }
    with open('./simulated_conditional_test.db', 'w') as f:
        for slot, slot_list in info.items():
            for slot_val in slot_list:
                f.write('{}({}, {})\n'.format(slot, person_id, slot_val))
                person_id += 1
        # keys = list(info.keys())
        # for i in range(len(keys) - 1):
        #     for j in range(i + 1, len(keys)):
        #         key_i, key_j = keys[i], keys[j]
        #         for i_val in info[key_i]:
        #             for j_val in info[key_j]:
        #                 f.write('{}({}, {})\n'.format(key_i, person_id, i_val))
        #                 f.write('{}({}, {})\n'.format(key_j, person_id, j_val))
        #                 person_id += 1


def save_conditional_probability(db_file, result_file, data_size, save_prob=False):
    cond_prob = dict()
    pprint('hi')
    with open(db_file, 'r') as f:
        for line in f:
            line = line.strip()
            left_par_index = line.index('(')
            comma_index = line.index(',')
            right_par_index = line.index(')')
            
            slot = line[:left_par_index].lower()
            person_id = line[left_par_index + 1:comma_index]
            slot_val = line[comma_index + 2:right_par_index].lower()
            
            if cond_prob.get(person_id) is None:
                cond_prob[person_id] = dict()
                cond_prob[person_id]['given_slots'] = set()
            
            cond_prob[person_id]['given_slots'].add(slot)
            if 'dontcare' in slot_val:
                slot_val = 'dontcare'
            cond_prob[person_id][slot + '=' + slot_val] = dict()
    
    with open(result_file, 'r') as f:
        for line in f:
            line = line.strip()
            slot_info, prob = line.split()
            left_par_index = slot_info.index('(')
            comma_index = slot_info.index(',')
            right_par_index = slot_info.index(')')
            
            slot = line[:left_par_index].lower()
            person_id = line[left_par_index + 1:comma_index]
            slot_val = line[comma_index + 1:right_par_index].lower()
            
            if 'dontcare' in slot_val:
                slot_val = 'dontcare'
            
            if slot not in cond_prob[person_id]['given_slots']:
                if cond_prob[person_id].get(slot) is None:
                    cond_prob[person_id][slot] = dict()
            
            if slot not in cond_prob[person_id]['given_slots']:
                cond_prob[person_id][slot][slot_val] = float(prob)
    
    pprint(cond_prob)
    
    final_cond = dict()
    for _, values in cond_prob.items():
        keys = sorted([key for key, info in values.items() if not info])
        prob = [(key, value) for key, value in values.items() if key not in values['given_slots']
                and key != 'given_slots' and value]
        
        for key, value in prob:
            for slot_val, slot_val_freq in value.items():
                if 'dontcare' in slot_val:
                    value['dontcare'] = value.pop(slot_val)
        
        # print(keys, prob)
        
        prob_dict = dict()
        for key, value in prob:
            prob_dict[key] = value
        
        keys = sorted(keys)
        final_cond[','.join(keys)] = prob_dict
    
    print(final_cond)
    if save_prob:
        import dill
        file_path = os.path.join(os.path.dirname(__file__), 'conditional_prob.pkl')
        # file_path = os.path.join(os.path.dirname(__file__), 'conditional_prob_{}.pkl'.format(data_size))
        with open(file_path, 'wb') as f:
            dill.dump(final_cond, f, protocol=2)
            print(file_path + ' created!')


if __name__ == '__main__':
    # insert_all_combo()
    # get_names()
    # generate_conditional_test_data()
    # save_conditional_probability(db_file='simulated_conditional_test.db',
    #                              result_file='simulated_out_conditional_{}.result'.format(250),
    #                              data_size=250,
    #                              save_prob=True)

    # for data_size in [25, 50, 100]:
    #     save_conditional_probability(db_file='simulated_conditional_test.db',
    #                                  result_file='simulated_out_conditional_{}.result'.format(data_size),
    #                                  data_size=data_size,
    #                                  save_prob=True)


    save_conditional_probability(db_file='simulated_conditional_test.db',
                                    result_file='simulated_out_conditional.result',
                                    data_size=2000,
                                    save_prob=True)

    pass
