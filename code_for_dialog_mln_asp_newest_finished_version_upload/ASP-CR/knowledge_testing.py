#! python 3
import sys
# import color_print as prt
import clingo
# import dill
import random

# from utils import Settings

# class Save_factors:
#     external_factors_sample = []
#     NUM_DIALOGS = None
#     def __init__(self):
#         pass

def filter_show(model, name=None, arity=None):
    ##############################################
    # @Params: 
    #   model: the complete model, a list of Symbols
    # @Return: the list of matched Symbols
    ##############################################
    
    n = name
    a = arity
    result = []
    
    for s in model:
        if n is None and a is None:
            result.append(s)
        elif s.name == n:
            result.append(s)
    return result


def filter_Function(model, name=None, arity=None):
    ##############################################
    # @Params: 
    #   model: a model, a list of Symbols
    #   name: the filter name, a string Function
    # @Return: the list of Symbol tuples 
    #   satisfying the predicate @name
    ##############################################
    m_filtered = filter_show(model, name, arity)
    result = []
    for s in m_filtered:
        if (s.positive):
            result.append(s.arguments)
    return result


def filter_Function_str(model, name=None, arity=None):
    ##############################################
    # @Params: 
    #   model: a model, a list of Symbols
    #   name: the filter name, a string Function
    # @Return: the list of string(Symbol) tuples 
    #   satisfying the predicate @name
    ##############################################
    tuples = filter_Function(model, name, arity)
    result = []
    for t in tuples:
        r = []
        for s in t:
            if s.name != None:
                r.append(s.name)
            elif s.number != None:
                r.append(str(s.number))
            elif s.string != None:
                r.append(s.string)
        result.append(r)
    return result


def reason_LP(facts, lp_files):
    ##############################################
    # Load the lp file and solve the logic program.
    # @Params: 
    #   lpFile: the path of the lp file
    # @Return: the knowledge from the answer sets
    #   
    ##############################################
    ctl = clingo.Control("0")
    # Load the rules of logic program
    for f in lp_files:
        ctl.load(f)
    
    for fact in facts:
        ctl.add("base", [], fact)
    # testing: add the given facts
    # ctl.add("base", [], "live_area(north).")
    # ctl.add("base", [], "{req(X):area(X)} == 1.")
    
    ctl.ground([("base", [])])
    
    models = []  # to store all answer sets
    
    with ctl.solve(yield_=True) as handle:
        for m in handle:
            models.append(m.symbols(atoms=True))
    models = sorted(models)
    
    ctl.solve()  # on_model=lambda m: print("Solving: {}".format(m)))
    # prt.printGreen("Solving: {}".format(m)))
    
    models_show = []  # list of the models with #show option
    show_n_list = ["update_area"]  # ,"traffic"]
    show_a_list = [1, 1, 2]
    
    facts_show = []
    fact_show_n_list = ["weather", "traffic"]  # ,"traffic"]
    fact_show_a_list = [1, 2]
    
    i = 1
    for i in range(len(models)):
        fact_show = []
        # print("Answer Set: {}".format(i+1))
        for j in range(len(fact_show_n_list)):
            m_show = filter_show(models[i],
                                 fact_show_n_list[j], fact_show_a_list[j])
            m_show = sorted(m_show)
            # prt.printGreen(str(m_show))
            fact_show = fact_show + m_show
        facts_show.append(fact_show)
    # pass
    # print("Facts: {}".format(facts_show))
    # prt.printRed("Facts: {}".format(facts_show))
    
    i = 1
    for i in range(len(models)):
        model_show = []
        # print("Answer Set: {}".format(i+1))
        for j in range(len(show_n_list)):
            m_show = filter_show(models[i],
                                 show_n_list[j], show_a_list[j])
            m_show = sorted(m_show)
            # prt.printGreen(str(m_show))
            model_show = model_show + m_show
        models_show.append(model_show)
    # pass
    
    print("Answer Sets: {}".format(models_show))
    # prt.printYellow("Answer Sets: {}".format(models_show))
    
    '''
    # decode Symbols into list of str lists
    knowledge = None
    for i in range(len(models)):
        print("Filtered Answer Set {}: ".format(i+1))
        knowledge = filter_Function(
            models[i],show_n_list[0],show_a_list[0])
        prt.printYellow(str(knowledge))
    pass
    '''
    
    # if(models_show == []):
    #     print(">>> No answer set! <<<")
    # prt.printRed(">>> No answer set! <<<")
    return models_show


def sample_external_factors():
    import numpy as np
    # user_loc, traffic, weather
    possible_user_locs = ['north', 'south', 'west', 'east', 'centre']
    possible_traffic = ['good', 'bad']
    possible_weather = ['good', 'bad']
    # shuffle
    loc = np.random.choice(possible_user_locs)
    user_loc = ['user_loc({}).'.format(loc)]
    traffic_list = list()
    weather = list()
    
    for curr_loc in possible_user_locs:
        traffic_list.append('traffic({},{}).'.format(curr_loc, np.random.choice(possible_traffic)))
    weather.append('weather({}).'.format(np.random.choice(possible_weather)))
    
    return user_loc + traffic_list + weather


def main():
    while True:
        facts = sample_external_factors()
        # facts = ['user_loc(west).', 'traffic(north,bad).', 'traffic(south,good).', 'traffic(west,good).',
        #          'traffic(east,bad).', 'traffic(centre,bad).', 'weather(bad).']
        facts = ['user_loc(west).', 'traffic(north,bad).', 'traffic(south,good).', 'traffic(west,good).',
                 'traffic(east,bad).', 'traffic(centre,bad).', 'weather(good).']
        print("Example 1:")
        lpFiles = []
        lpFiles.append("CamHotels_rules.lp")
        # lpFiles.append("CamHotels_facts.lp")
        
        res1 = reason_LP(facts, lpFiles)[0]
        
        print("Example 2:")
        lpFiles_1 = []
        lpFiles_1.append("CamHotels_inaccurate_rules.lp")
        # lpFiles_1.append("CamHotels_facts_1.lp")
        
        res2 = reason_LP(facts, lpFiles_1)[0]
        
        print("Example 3:")
        lpFiles_2 = []
        lpFiles_2.append("CamHotels_incomplete_rules.lp")
        # lpFiles_2.append("CamHotels_facts_1.lp")
        res3 = reason_LP(facts, lpFiles_2)[0]
    
        if str(res1) != str(res3):
            print(facts)
            print(res1)
            print(res2)
            print(res3)
            break
        break
    
    #
    '''
    user_model_path = 'bn_inference.pkl'
    user_model = dill.load(open(user_model_path, 'rb'))
    size = len(user_model.samples)
    print(user_model.samples[random.randrange(size)])
    '''


if __name__ == "__main__":
    main()
    # pass
