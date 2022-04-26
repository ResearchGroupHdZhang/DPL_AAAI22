import sqlite3
import os
import numpy as np


def get_names():
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'ontology/ontologies/CamHotels-dbase.db')
    )
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    param = '''SELECT name from CamHotels'''
    cursor.execute(param)
    rows = cursor.fetchall()
    
    with open('all_hotel_names.json', 'w') as f:
        names = dict()
        names['name'] = []
        names['hotel'] = []
        names['guesthouse'] = []
        for row in rows:
            if row[0][:5] == 'hotel':
                names['hotel'].append(row[0])
            elif row[0][:10] == 'guesthouse':
                names['guesthouse'].append(row[0])
            else:
                names['name'].append(row[0])
        sorted(names['name'])
        sorted(names['hotel'])
        sorted(names['guesthouse'])
        
        names['name'].extend(names['hotel'])
        names['name'].extend(names['guesthouse'])
        
        import json
        json.dump(names, f)
    
    cursor.close()


def insert_random_entries(id, name, pricerange, kind, area, stars, hasparking,
                          phone='not available', price='not available',
                          addr='not available', postcode='not available',
                          hasinternet='not available'):
    try:
        path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'ontology/ontologies/CamHotels-dbase.db')
        )
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        
        param = '''INSERT INTO CamHotels (id, name, pricerange, kind, area, phone, price, addr, postcode,
        stars, hasinternet, hasparking, booknumber, bookname, booktime, bookdate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        
        data_tuple = (id, name, pricerange, kind, area, phone, price,
                      addr, postcode, stars, hasinternet, hasparking,
                      'not available', 'not available', 'not available',
                      'not available')
        
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
        os.path.join(os.path.dirname(__file__), '..', 'ontology/ontologies/CamHotels-dbase.db')
    )
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    param = '''SELECT pricerange, kind, stars, area, hasparking FROM CamHotels'''
    cursor.execute(param)
    rows = cursor.fetchall()
    
    for row in rows:
        key = ','.join(row)
        if all_combo[key] > 0:
            all_combo[key] -= 1


def insert_all_combo():
    all_combo = {}
    
    price_options = ['cheap', 'moderate', 'expensive']
    kind_options = ['hotel', 'guesthouse']
    area_options = ['north', 'west', 'south', 'centre', 'east']
    star_options = ['0', '2', '3', '4']
    parking_option = ['0', '1']
    
    import random
    for p in price_options:
        for k in kind_options:
            for s in star_options:
                for a in area_options:
                    for pk in parking_option:
                        key = ','.join([p, k, s, a, pk])
                        all_combo[key] = 1
    
    deduct_current_entries(all_combo)
    
    entry_id = 33
    print(sum(all_combo.values()))
    while sum(all_combo.values()) > 0:
        name = np.random.choice(kind_options) + str(entry_id)
        pricerange = np.random.choice(price_options)
        kind = np.random.choice(kind_options)
        area = np.random.choice(area_options)
        star = np.random.choice(star_options)
        hasparking = np.random.choice(parking_option)
        
        phone = '12233600' + str(entry_id)
        price = name + 'price'
        addr = name + 'addr'
        postcode = name + 'postcode'
        internet = np.random.choice(['0', '1'])
        
        curr_key = ','.join([pricerange, kind, star, area, hasparking])
        if all_combo[curr_key] > 0:
            insert_random_entries(entry_id, name, pricerange, kind, area, star,
                                  hasparking, phone, price, addr, postcode, internet)
            all_combo[curr_key] -= 1
            entry_id += 1


def generate_conditional_test_data():
    person_id = 2001
    info = {
        'Stars': ['0', '2', '3', '4', '5'],
        'Pricerange': ['Cheap', 'Moderate', 'Expensive', 'PriceDontcare'],
        'Kind': ['Guesthouse', 'Hotel', 'KindDontcare']
    }
    with open('./simulated_conditional_test.db', 'w') as f:
        for slot, slot_list in info.items():
            for slot_val in slot_list:
                f.write('{}({}, {})\n'.format(slot, person_id, slot_val))
                person_id += 1
        keys = list(info.keys())
        for i in range(len(keys) - 1):
            for j in range(i + 1, len(keys)):
                key_i, key_j = keys[i], keys[j]
                for i_val in info[key_i]:
                    for j_val in info[key_j]:
                        f.write('{}({}, {})\n'.format(key_i, person_id, i_val))
                        f.write('{}({}, {})\n'.format(key_j, person_id, j_val))
                        person_id += 1


def save_conditional_probability(db_file, result_file, data_size, save_prob=False):
    cond_prob = dict()
    
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
            if slot_val == '5' or 'dontcare' in slot_val:
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
            
            if slot_val == '5' or 'dontcare' in slot_val:
                slot_val = 'dontcare'
            
            if slot not in cond_prob[person_id]['given_slots']:
                if cond_prob[person_id].get(slot) is None:
                    cond_prob[person_id][slot] = dict()
            
            if slot not in cond_prob[person_id]['given_slots']:
                cond_prob[person_id][slot][slot_val] = float(prob)
    
    # print(cond_prob)
    
    final_cond = dict()
    for _, values in cond_prob.items():
        keys = sorted([key for key, info in values.items() if not info])
        prob = [(key, value) for key, value in values.items() if key not in values['given_slots']
                and key != 'given_slots' and value]
        
        for key, value in prob:
            for slot_val, slot_val_freq in value.items():
                if slot_val == '5' or 'dontcare' in slot_val:
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
        # file_path = os.path.join(os.path.dirname(__file__), 'conditional_prob.pkl')
        file_path = os.path.join(os.path.dirname(__file__), 'conditional_prob_{}.pkl'.format(data_size))
        # file_path = os.path.join(os.path.dirname(__file__), 'conditional_prob_false.pkl')
        # file_path = os.path.join(os.path.dirname(__file__), 'conditional_prob_{}_1.pkl'.format(data_size))
        # file_path = os.path.join(os.path.dirname(__file__), 'conditional_prob_{}_2.pkl'.format(data_size))
        # file_path = os.path.join(os.path.dirname(__file__), 'conditional_prob_{}_3.pkl'.format(data_size))
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

    # save_conditional_probability(db_file='simulated_conditional_test.db',
    #                              result_file='simulated_out_conditional.result',
    #                              data_size=2000,
    #                              save_prob=True)

    # save_conditional_probability(db_file='simulated_conditional_test.db',
    #                                 result_file='simulated_out_conditional.result',
    #                                 data_size=2000,
    #                                 save_prob=True)

    # save_conditional_probability(db_file='simulated_conditional_test.db',
    #                                 result_file='simulated_out_conditional_false.result',
    #                                 data_size=2000,
    #                                 save_prob=True)

    # save_conditional_probability(db_file='simulated_conditional_test.db',
    #                                 result_file='simulated_out_conditional_5_3.result',
    #                                 data_size=5,
    #                                 save_prob=True)

    # save_conditional_probability(db_file='simulated_conditional_test.db',
    #                                 result_file='simulated_out_conditional_500_3.result',
    #                                 data_size=500,
    #                                 save_prob=True)

    # save_conditional_probability(db_file='simulated_conditional_test.db',
    #                                 result_file='simulated_out_conditional_100.result',
    #                                 data_size=100,
    #                                 save_prob=True)

    # for item in ['100_1', '100_2', '100_3', '200_1', '200_2', '200_3', '250_1', '250_2', '250_3', '500_1', '500_2', '500_3', '1000_1', '1000_2', '1000_3']:
    #     save_conditional_probability(db_file='simulated_conditional_test.db',
    #                                     result_file='simulated_out_conditional_' + item + '.result',
    #                                     data_size=item,
    #                                     save_prob=True)

    # for item in ['500_1', '500_2', '500_3']:
    #     save_conditional_probability(db_file='simulated_conditional_test.db',
    #                                     result_file='simulated_out_conditional_' + item + '.result',
    #                                     data_size=item,
    #                                     save_prob=True)

    # for item in ['250_1', '250_2', '250_3', '500_1', '500_2', '500_3', '1000_1', '1000_2', '1000_3']:
    # for item in ['250_1', '250_2', '250_3', '500_1', '500_2', '500_3']:
    # for item in ['250_1', '250_2', '250_3', '100_1', '100_2', '100_3']:
    for item in ['100_1', '100_2', '100_3', '500_1', '500_2', '500_3']:
        save_conditional_probability(db_file='simulated_conditional_test.db',
                                        result_file='simulated_out_conditional_' + item + '.result',
                                        data_size=item,
                                        save_prob=True)

    # save_conditional_probability(db_file='simulated_conditional_test.db',
    #                                 result_file='simulated_out_conditional_5_1.result',
    #                                 data_size=5,
    #                                 save_prob=True)

    # save_conditional_probability(db_file='simulated_conditional_test.db',
    #                                 result_file='simulated_out_conditional_1000.result',
    #                                 data_size=1000,
    #                                 save_prob=True)
    
    # for data_size in range(250, 500, 1000):
    #     save_conditional_probability(db_file='simulated_conditional_test.db',
    #                                  result_file='simulated_out_conditional_{}.result'.format(data_size),
    #                                  data_size=data_size,
    #                                  save_prob=True) 


    # for data_size in range(1000, 2500, 500):
    #     save_conditional_probability(db_file='simulated_conditional_test.db',
    #                                  result_file='simulated_out_conditional_{}.result'.format(data_size),
    #                                  data_size=data_size,
    #                                  save_prob=True)
    pass
