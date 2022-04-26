#!/usr/bin/env bash

nohup python pydial.py train config/asp_config/env1-A2C-CH-ASP-ac.cfg & 
nohup python pydial.py train config/asp_config/env1-A2C-CH-ASP-ia.cfg &
nohup python pydial.py train config/asp_config/env1-A2C-CH-ASP-ic.cfg &
nohup python pydial.py train config/asp_config/env1-A2C-CH-MLN.cfg & 
nohup python pydial.py train config/asp_config/env2-A2C-CH-ASP-ac.cfg &
nohup python pydial.py train config/asp_config/env2-A2C-CH-ASP-ia.cfg &
nohup python pydial.py train config/asp_config/env2-A2C-CH-ASP-ic.cfg &
nohup python pydial.py train config/asp_config/env2-A2C-CH-MLN.cfg &
nohup python pydial.py train config/asp_config/env3-A2C-CH-ASP-ac.cfg &
nohup python pydial.py train config/asp_config/env3-A2C-CH-ASP-ia.cfg &
nohup python pydial.py train config/asp_config/env3-A2C-CH-ASP-ic.cfg &
nohup python pydial.py train config/asp_config/env3-A2C-CH-MLN.cfg &
nohup python pydial.py train config/asp_config/env4-A2C-CH-ASP-ac.cfg &
nohup python pydial.py train config/asp_config/env4-A2C-CH-ASP-ia.cfg &
nohup python pydial.py train config/asp_config/env4-A2C-CH-ASP-ic.cfg &
nohup python pydial.py train config/asp_config/env4-A2C-CH-MLN.cfg &
nohup python pydial.py train config/asp_config/env5-A2C-CH-ASP-ac.cfg &
nohup python pydial.py train config/asp_config/env5-A2C-CH-ASP-ia.cfg &
nohup python pydial.py train config/asp_config/env5-A2C-CH-ASP-ic.cfg &
nohup python pydial.py train config/asp_config/env5-A2C-CH-MLN.cfg &