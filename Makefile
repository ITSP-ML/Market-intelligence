#################################################################################
# GLOBALS                                                                       #
#################################################################################
.ONESHELL:

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = Market-intelligence
# DEEP_PAVLOV_ENV = deep-pavlov

#################################################################################
# COMMANDS                                                                      #
#################################################################################

#update the environment after manually changing environment.yml
environment.lock: environment.yml
	conda env update -n $(PROJECT_NAME) -f $< --prune
	conda env export -n $(PROJECT_NAME) -f $@

# ## environment for deep-pavlov
# dp_environment.lock: dp_environment.yml
# 	conda env update -n $(DEEP_PAVLOV_ENV) -f $< --prune
# 	conda env export -n $(DEEP_PAVLOV_ENV) -f $@

#shortcuts for environment update
def_env: environment.lock

# dp_env: dp_environment.lock

env: def_env 
# IMPORTANT: If you want to run a deep-pavlov model for the first time on your machine, you need to install it first:
#    make env
#    conda activate deep-pavlov
#    python -m deeppavlov install YOUR_DEEP_PAVLOV_MODEL_NAME
# where YOUR_DEEP_PAVLOV_MODEL_NAME is e.g. sentiment_sst_conv_bert
