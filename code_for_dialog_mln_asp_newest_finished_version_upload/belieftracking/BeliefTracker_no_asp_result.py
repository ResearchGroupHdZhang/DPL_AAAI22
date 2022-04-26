###############################################################################
# PyDial: Multi-domain Statistical Spoken Dialogue System Software
###############################################################################
#
# Copyright 2015 - 2019
# Cambridge University Engineering Department Dialogue Systems Group
#
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################

'''
BeliefTracker.py - Belief Tracker
====================================================

Copyright CUED Dialogue Systems Group 2015 - 2017

.. seealso:: CUED Imports/Dependencies: 

    import :mod:`utils.dact` |.|
    import :mod:`utils.ContextLogger`
    import :mod:`policy.SummaryUtils` |.|
    import :mod:`ontology.Ontology` |.|
    import :mod:`belieftracking.BeliefTrackingUtils` |.|

************************

'''


__author__ = "cued_dialogue_systems_group"

from collections import defaultdict
import math
import pprint
import copy

import numpy as np

from utils import ContextLogger, dact
from policy import SummaryUtils
from ontology import Ontology
import BeliefTrackingUtils
logger = ContextLogger.getLogger('') 


class BeliefTracker(object):
    '''
    Belief Tracker base class that implements most of the functionality within the dialogue system. The actual inference
    problem of belief tracking (ASR/SLU --> belief state update) is implemented by individual trackers (in baseline.py for example). 
    Hence this class will never be instantiated, it just implements common functionality.
    If developing a new tracker - it should inherit this class and implement a self.tracker.
    '''
    def __init__(self, domainString):
        self.prevbelief = None
        self.turn = 0
        self.domainString = domainString
        self.CONDITIONAL_BELIEF_PROB = 0.8

        from utils import Settings
        self.add_knowledge = False
        if Settings.config.has_option("GENERAL", "add_knowledge"):
            self.add_knowledge = Settings.config.getboolean("GENERAL", "add_knowledge")
        self.mln_training_data_size = None
        if Settings.config.has_option('GENERAL', "mln_training_data_size"):
            self.mln_training_data_size = Settings.config.getint('GENERAL', "mln_training_data_size")


        from ASP.knowledge_testing import reason_LP, Save_factors
        from ASP import knowledge_testing 
        import os


        # CONFIG:
        # add handles for ASP mode and MLN mode
        self.reason_LP = reason_LP
        # self.randomseed = 1234
        # if Settings.config.has_option('GENERAL', 'seed'):
        #     self.randomseed = Settings.config.getint('GENERAL', 'seed')

        # np.random.seed(int(self.randomseed))



        import os
        import dill
        if self.add_knowledge:
            # load simulated_result to get initial belief probability distribution
            # mode for only comparing MLN mode with training data size difference used in training in Alchemy
            if self.mln_training_data_size:
                init_belief_file = os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        '..',
                        'MLN/simulated_out_marginal_{}.result'.format(self.mln_training_data_size))
                )
                conditional_prob_file = os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        '..',
                        'MLN/conditional_prob_{}.pkl'.format(self.mln_training_data_size))
                )


            # # true version
            #                 init_belief_file = os.path.abspath(
            #                     os.path.join(
            #                         os.path.dirname(__file__),
            #                         '..',
            #                         'MLN3/simulated_out_marginal_{}.result'.format(self.mln_training_data_size))
            #                 )
            #                 conditional_prob_file = os.path.abspath(
            #                     os.path.join(
            #                         os.path.dirname(__file__),
            #                         '..',
            #                         'MLN3/conditional_prob_{}.pkl'.format(self.mln_training_data_size))
            #                 )

            # try version

                # if Settings.config.has_option('GENERAL', "mln_training_data_size_index"):
                #     index = Settings.config.getint('GENERAL', "mln_training_data_size_index")

                # init_belief_file = os.path.abspath(
                #     os.path.join(
                #         os.path.dirname(__file__),
                #         '..',
                #         'MLN1/simulated_out_marginal_{}_{}_false.result'.format(self.mln_training_data_size, index))
                # )
                # conditional_prob_file = os.path.abspath(
                #     os.path.join(
                #         os.path.dirname(__file__),
                #         '..',
                #         'MLN1/conditional_prob_{}_{}_false.pkl'.format(self.mln_training_data_size, index))
                # )




            else:
                # added
                if self.domainString == "CamRestaurants":
                    init_belief_file = os.path.abspath(
                        os.path.join(os.path.dirname(__file__), '..', 'MLN/simulated_out_marginal.result')
                    )
                    conditional_prob_file = os.path.abspath(
                        os.path.join(os.path.dirname(__file__), '..', 'MLN/conditional_prob.pkl')
                    )

                elif self.domainString == "CamHotels":
                    init_belief_file = os.path.abspath(
                        os.path.join(os.path.dirname(__file__), '..', 'MLN_CH/simulated_out_marginal.result')
                    )
                    conditional_prob_file = os.path.abspath(
                        os.path.join(os.path.dirname(__file__), '..', 'MLN_CH/conditional_prob.pkl')
                    ) 

                # init_belief_file = os.path.abspath(
                #     os.path.join(os.path.dirname(__file__), '..', 'MLN3/simulated_out_marginal.result')
                # )
                # conditional_prob_file = os.path.abspath(
                #     os.path.join(os.path.dirname(__file__), '..', 'MLN3/conditional_prob.pkl')
                # )
                
            self.knowledge = defaultdict(list)
            with open(init_belief_file, 'r') as f:
                for line in f:
                    info, prob = line.split()
                    slot = info[:info.index('(')].lower()
                    slot_val = info[info.index(',') + 1:info.index(')')].lower()
                    # if 'dontcare' in slot_val :
                    if 'dontcare' in slot_val or slot_val == '5':
                        slot_val = 'dontcare'
                    self.knowledge[slot].append((slot_val, float(prob)))

            self.conditional_prob_knowledge = dill.load(open(conditional_prob_file, 'rb'))
            # self.conditional_prob_knowledge = open(conditional_prob_file, 'rb') as f
    # TODO: @Jerry fix this
    # P1
    # added
    def _update_probability_cr(self, belief, track, slots):
        goal_label_keys = set(track['goal-labels'].keys())
        slots_needed_updated = [slot for slot in slots if slot not in goal_label_keys]
        slots_known = slots.difference(set(slots_needed_updated))
        
        if slots_needed_updated:
            for slot in slots_needed_updated:
                if 1 in set(belief[slot].values()):
                    slots_needed_updated.remove(slot)
        if slots_needed_updated and slots_known:
            if len(slots_known) == 1 and 'food' in slots_known:
                keys = []
                for slot in slots_known:
                    keys.append(slot + '=' + track['goal-labels'][slot].keys()[0])
                conditional_key = ','.join(sorted(keys))

                if self.conditional_prob_knowledge.get(conditional_key) is not None:
                    conditional_prob = self.conditional_prob_knowledge[conditional_key]
                    for slot in slots_needed_updated:
                        for slot_val, prob in conditional_prob[slot].items():
                            belief[slot][slot_val] = prob


    def _update_probability_ch(self, belief, track, slots):
        goal_label_keys = set(track['goal-labels'].keys())
        slots_needed_updated = [slot for slot in slots if slot not in goal_label_keys]
        slots_known = slots.difference(set(slots_needed_updated))
        
        if slots_needed_updated:
            for slot in slots_needed_updated:
                if 1 in set(belief[slot].values()):
                    slots_needed_updated.remove(slot)
        if slots_needed_updated and slots_known:
            if len(slots_known) == 2 and 'kind' in slots_known and 'stars' in slots_known:
                keys = []
                for slot in slots_known:
                    keys.append(slot + '=' + track['goal-labels'][slot].keys()[0])
                conditional_key = ','.join(sorted(keys))

                if self.conditional_prob_knowledge.get(conditional_key) is not None:
                    conditional_prob = self.conditional_prob_knowledge[conditional_key]
                    for slot in slots_needed_updated:
                        for slot_val, prob in conditional_prob[slot].items():
                            belief[slot][slot_val] = prob
            
    ##################################################
    # interface methods
    ##################################################
    
    def _updateBelief(self, turn):
        '''
        Update the belief given the current turn info
        '''
        pass
    
    def restart(self):
        '''
        Reset some private members
        '''
        self.prevbelief = None
        self.turn = 0
    
    ##################################################
    # general public methods
    ##################################################
        
    def update_belief_state(self, lastact, obs, constraints=None):
        '''
        Does the actual belief tracking via tracker.addTurn

        :param lastact: last system dialgoue act
        :type lastact: string

        :param obs: current observation
        :type obs: list
        
        :param constraints:
        :type constraints: dict

        :return: dict -- previous belief state
        '''
        curturn = self._convertHypToTurn(lastact, obs)
        last_feature = None

        if self.prevbelief is not None and 'features' in self.prevbelief.keys():
            last_feature = copy.deepcopy(self.prevbelief['features'])
 
        if self.turn == 0:
            self.prevbelief = self._init_belief(constraints)

        # combine current turn info -- converted to user hypothesis
        # with previous belief to form the new belief
        self.prevbelief = self._updateBelief(curturn)
#         self._print_belief()

        logger.debug(pprint.pformat(curturn))

        # add 'features' into the belief
        self._updateMactFeat(last_feature, lastact)
        self.turn += 1
        logger.debug(self.str())
        
#         self._printTopBeliefs()
        
        return self.prevbelief
    
    def getBelief80_pairs(self):
        """
        Called by EXITING DOMAIN
        """
        pairs = {}
        for slot in Ontology.global_ontology.get_system_requestable_slots(self.domainString):
            maxval = max(self.prevbelief["beliefs"][slot].values())
            maxindex = self.prevbelief["beliefs"][slot].values().index(maxval)
            maxvalsKEY = self.prevbelief["beliefs"][slot].keys()[maxindex]
            if maxval > 0.80 and maxvalsKEY not in ['dontcare','none','**NONE**']:
                pairs[slot] = maxvalsKEY
        return pairs
    
    def get_conditional_constraints(self, prev_domain_constraints):
        """Called by ENTERING DOMAIN
        Takes a dict (keys=all available domains we have -- more info this way than just a list of 
        slots + values) of constraints from previous domains AS DETERMINED BY THE DIALOGS IN THOSE 
        DOMAINS WITH THE DOMAINS OWN TRACKER - then conditionally initialises the new tracker. 
        (Meaning this is only called when domain is first launched within a single dialog).

        :param prev_domain_constraints: a dict of constraints from previous domains
        :type prev_domain_constraints: dict

        :returns None:
        """
        #TODO -- in order to infer how other domain constraints (slotX=valueY) affect this domain, should potentially
        # ------ just be passing the entire prev_domain_constraints thru to tracker...
        constraints = dict.fromkeys(Ontology.global_ontology.get_system_requestable_slots(self.domainString))
        informable_vals = Ontology.global_ontology.get_informable_slots_and_values(self.domainString)
        for dstring in prev_domain_constraints: 
            if prev_domain_constraints[dstring] is not None:
                # is then a dict with the constraints from that domain. keys=slots, values=VALUE-FROM-SLOT
                for slot,val in prev_domain_constraints[dstring].iteritems():
                    if slot in constraints.keys():
                        if val in informable_vals[slot]: 
                            if constraints[slot] is None:
                                constraints[slot] = [val]
                            else:
                                constraints[slot].append(val)
        logger.debug("Constraints: "+str(constraints))
        return constraints
    
    def str(self):
        return pprint.pformat(self.prevbelief)
#         return pprint.pformat(BeliefTrackingUtils.simplify_belief(Ontology.global_ontology.get_ontology(self.domainString),
#                                                                   self.prevbelief))
    
    ##################################################
    # private methods
    ##################################################
        
    def _convertHypToTurn(self, lastact, obs):
        '''
        Convert hypotheses to turn
        
        :param lastact: last system dialgue act
        :type lastact: string

        :param obs: current observation
        :type obs: list
        
        :return: dict -- turn dict
        '''
        curturn = {'turn-index': self.turn}

        # Last system action
        slastact = []
        if self.turn > 0:
            slastact = dact.ParseAct(lastact, user=False)
            slastact = BeliefTrackingUtils._transformAct(slastact, {}, 
                                                         Ontology.global_ontology.get_ontology(self.domainString), 
                                                         user=False)
        curturn['output'] = {'dialog-acts': slastact}

        # User act hyps
        accumulated = defaultdict(float)
        for (hyp, prob) in obs:
            hyp = dact.ParseAct(hyp)
            hyp = BeliefTrackingUtils._transformAct(hyp, {}, Ontology.global_ontology.get_ontology(self.domainString))
            hyp = dact.inferSlotsForAct(hyp)

            prob = min(1.0, prob)
            if prob < 0:
                prob = math.exp(prob)
            accumulated = BeliefTrackingUtils._addprob(accumulated, hyp, prob)
        sluhyps = BeliefTrackingUtils._normaliseandsort(accumulated)

        curturn['input'] = {'live': {'asr-hyps':[], 'slu-hyps':sluhyps}}
        return curturn


# # added by zzc

#     @staticmethod
#     # utility function for sampling external factors
#     def sample_external_factors():
#         # user_loc, traffic, weather
#         possible_user_locs = ['north', 'south', 'west', 'east', 'centre']
#         possible_traffic = ['good', 'bad']
#         possible_weather = ['good', 'bad']
#         # shuffle
#         loc = np.random.choice(possible_user_locs)
#         user_loc = ['user_loc({}).'.format(loc)]
#         traffic_list = list()
#         weather = list()
        
#         # for curr_loc in possible_user_locs:
#         #     traffic_list.append('traffic({},{}).'.format(curr_loc, np.random.choice(possible_traffic, p=[0.9, 0.1])))
#         # weather.append('weather({}).'.format(np.random.choice(possible_weather, p=[0.9, 0.1])))
        
#         for curr_loc in possible_user_locs:
#             if loc == 'west':
#                 if curr_loc in ['west', 'east', 'north']:
#                     traffic_list.append('traffic({},{}).'.format(curr_loc,
#                                                                  np.random.choice(possible_traffic, p=[0.9, 0.1])))
#                 else:
#                     traffic_list.append('traffic({},{}).'.format(curr_loc,
#                                                                  np.random.choice(possible_traffic, p=[0.1, 0.9])))
#             elif loc == 'north':
#                 if curr_loc in ['west', 'south', 'north']:
#                     traffic_list.append('traffic({},{}).'.format(curr_loc,
#                                                                  np.random.choice(possible_traffic, p=[0.9, 0.1])))
#                 else:
#                     traffic_list.append('traffic({},{}).'.format(curr_loc,
#                                                                  np.random.choice(possible_traffic, p=[0.1, 0.9])))
#             else:
#                 traffic_list.append('traffic({},{}).'.format(curr_loc,
#                                                              np.random.choice(possible_traffic, p=[0.5, 0.5])))

#         if loc == 'north' or loc == 'west':
#             weather.append('weather({}).'.format(np.random.choice(possible_weather, p=[0.9, 0.1])))
#         else:
#             weather.append('weather({}).'.format(np.random.choice(possible_weather, p=[0.5, 0.5])))
    
#         return user_loc + traffic_list + weather


    def _init_belief(self, constraints=None):
        '''
        Simply constructs the belief state data structure at turn 0

        :param constraints: a dict of constraints
        :type constraints: dict
       
        :return: dict -- initiliased belief state 
        '''
        # knowledge manually added
        belief = {}
        for slot in Ontology.global_ontology.get_informable_slots_and_values(self.domainString):
            inform_slot_vals = Ontology.global_ontology.get_informable_slot_values(self.domainString,slot)
            if slot not in Ontology.global_ontology.get_system_requestable_slots(self.domainString):
                belief[slot] = dict.fromkeys(inform_slot_vals, 0.0)
                belief[slot]['**NONE**'] = 1.0
            else:
                belief[slot] = dict.fromkeys(inform_slot_vals+['dontcare'], 0.0)
                # check if the slot is in knowledge_slots
                if self.add_knowledge and slot in self.knowledge:
                    for slot_val, prob in self.knowledge[slot]:
                        belief[slot][slot_val] = prob
                    belief[slot]['**NONE**'] = 0.0
                else:
                    belief[slot]['**NONE**'] = 1.0


        # When the belief initializes, the external elements are sampled
        # start

        # delete
        # from ASP.knowledge_testing import Save_factors
        # Save_factors.external_factors_sample = self.sample_external_factors()

        # end

        belief['method'] = dict.fromkeys(Ontology.global_ontology.get_method(self.domainString), 0.0)
        belief['method']['none'] = 1.0
        belief['discourseAct'] = dict.fromkeys(Ontology.global_ontology.get_discourseAct(self.domainString), 0.0)
        belief['discourseAct']['none'] = 1.0
        belief['requested'] = dict.fromkeys(Ontology.global_ontology.get_requestable_slots(self.domainString), 0.0)
        if constraints is not None:
            belief = self._conditionally_init_belief(belief,constraints)
        return {'beliefs': belief}
    
    def _conditionally_init_belief(self,belief,constraints):
        """
        Method for conditionally setting up the inital belief state of a domain based on information/events that occured
        earlier in the dialogue in ANOTHER (ie different) domain.
       
        :param belief: initial belief state
        :type belief: dict

        :param constraints: a dict of constraints
        :type constraints: dict
       
        :return: None        
        """ 
        # Now initialise the BELIEFS in this domain, based on the determine prior domain constraints
        for slot,valList in constraints.iteritems(): 
            if valList is not None and slot not in ['name']:
                prob_per_val = self.CONDITIONAL_BELIEF_PROB/float(len(set(valList))) 
                for val in valList:
                    belief[slot][val] = prob_per_val
                # and now normalise (plus deal with **NONE**)
                num_zeros = belief[slot].values().count(0.0)  #dont need a -1 for the **NONE** value as not 0 yet
                prob_per_other_val = (1.0-self.CONDITIONAL_BELIEF_PROB)/float(num_zeros)
                for k,v in belief[slot].iteritems():
                    if v == 0.0:
                        belief[slot][k] = prob_per_other_val  #cant think of better way than to loop for this...
                belief[slot]['**NONE**'] = 0.0
        #TODO - delete debug prints: print belief
        #print constraints
        #raw_input("just cond init blief")
        return belief
    
    def _updateMactFeat(self, last_feature, lastact):
        '''
        Add features into self.prevstate  - recording actions taken by machine

        :param last_feature: last system state features
        :type last_feature: dict
        
        :param lastact: last system dialgoue act
        :type lastact: string

        :return: None
        '''
        features = {}
        if self.turn == 0:
            features['lastInformedVenue'] = ''
            features['informedVenueSinceNone'] = []
            features['lastActionInformNone'] = False
            features['offerHappened'] = False

        else:
            last_system_act = dact.ParseAct(lastact, user=False)

            # lastInformedVenue
            current_informed_venue = BeliefTrackingUtils._getCurrentInformedVenue(last_system_act)
            current_informed_venue = self._list2str_bugfix(current_informed_venue)
            
            if current_informed_venue != '':
                features['lastInformedVenue'] = current_informed_venue
            else:
                features['lastInformedVenue'] = last_feature['lastInformedVenue']

            # informedVenueSinceNone
            if BeliefTrackingUtils._hasType(last_system_act, 'canthelp'):
                informedVenueSinceNone = []
            else:
                informedVenueSinceNone = last_feature['informedVenueSinceNone']
            if BeliefTrackingUtils._hasTypeSlot(last_system_act, 'offer', 'name'):
                venue = BeliefTrackingUtils._getTypeSlot(last_system_act, 'offer', 'name')
                venue = self._list2str_bugfix(venue)
                informedVenueSinceNone.append(venue)
            features['informedVenueSinceNone'] = informedVenueSinceNone

            # lastActionInformNone
            if BeliefTrackingUtils._hasType(last_system_act, 'canthelp'):
                features['lastActionInformNone'] = True
            else:
                features['lastActionInformNone'] = False

            # offerhappened
            if BeliefTrackingUtils._hasTypeSlot(last_system_act, 'offer', 'name'):
                features['offerHappened'] = True
            else:
                features['offerHappened'] = False

        # inform_info
        features['inform_info'] = []
        for numAccepted in range(1,6):
            temp =  SummaryUtils.actionSpecificInformSummary(self.prevbelief, numAccepted, self.domainString)
            features['inform_info'] += temp
           
        self.prevbelief['features'] = features
    
    def _list2str_bugfix(self, venue):
        # TODO -- BUG THAT SHOULD BE SORTED OUT FURTHER DOWN THE STACK THAN HERE            
        if isinstance(venue,list):
            return venue[0]
        else:
            return venue     
    
    
    def _print_belief(self):
        """Just a **Debug** function
        """
        if self.prevbelief is None:
            raw_input("Beliefs is None")
            return
        
#         import pprint
        pprint.pprint(self.prevbelief)
        
    def _printTopBeliefs(self):
        # currently top 5 values per slot
        for slot in self.prevbelief['beliefs']:
            str = slot + ": "
            slotBelief = copy.deepcopy(self.prevbelief['beliefs'][slot])
#             slotBelief = sorted(slotBelief, key=slotBelief.get, reverse=True) # sort slot belief based on probability
            count = 0
            for key in sorted(slotBelief, key=slotBelief.get, reverse=True):
                count += 1
                str += " {}:{} ".format(key,slotBelief[key]) # append top x belief entries to string
                if count >= 5:
                    break
            logger.info(str)
#             print str
        
#         for a in self.prevbelief["beliefs"]:
#             print a, self.prevbelief["beliefs"][a]
#         for slot,value in self.prevbelief["beliefs"].iteritems():
#             print value
#             print slot
#         raw_input("hold and check beliefs in "+self.domainString)

if __name__ == "__main__":
    from belieftracking.baseline import FocusTracker
    from utils import Settings
    Settings.load_root('/Users/su259/pydial-letsgo/')
    Settings.load_config(None)
    Settings.set_seed(123)
    Settings.config.add_section("GENERAL")
    Settings.config.set("GENERAL",'domains', 'CamRestaurants')
    
    Ontology.init_global_ontology()
    tracker = FocusTracker('CamRestaurants')
    print "hello()"
    tracker.update_belief_state(None, [('hello()',1.0)])
    print 'inform(area="centre")'
    tracker.update_belief_state('request(area)', [('inform(area="centre")',0.3)])
    print 'inform(area="north")'
    tracker.update_belief_state('confirm(area="centre")', [('negate(area="north",pricerange="cheap")',1.0)])
    tracker.update_belief_state('confirm(area="centre")', [('deny(area="centre",area="north",pricerange="cheap")',1.0)])
#     tracker.update_belief_state('confirm(area="centre")', [('negate(area="north")',1.0)])

#END OF FILE
