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

def get_configs():
    import glob
    configs = glob.glob("tests/test_configs/*.cfg")  # load all configs we will latter check
    return configs  


def get_loop_over_domains():
    from ontology import OntologyUtils
    domains = list(OntologyUtils.available_domains) # list to copy
    domains.remove('topicmanager')
    domains.remove('wikipedia')
    domains.remove('ood')
    if 'Booking' in domains:
        domains.remove('Booking')
    if 'letsgo' in domains:
        domains.remove('letsgo')
    return domains