# necessary for tests to run correctny 
# (solves issue with importing to tests.)

import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(PROJECT_PATH,"src")

sys.path.append(SOURCE_PATH)

