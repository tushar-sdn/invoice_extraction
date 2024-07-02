
# import sys
# import os
# app_dir = "/home/hemantchoudhari/Desktop/all_project/Invoice-Extractor"
# sys.path.insert(0, app_dir)
# conda_env_path = '/home/hemantchoudhari/.conda/envs/myenv'
# site_packages_path = os.path.join(conda_env_path, 'lib/python3.12/site-packages')
# sys.path.insert(1, site_packages_path)
# os.environ['PATH'] = os.path.join(conda_env_path, 'bin') + ':' + os.environ['PATH']
# from app import app as application


import sys
import os

import sys
sys.path.insert(0,'/var/www/Invoice-Extractor')
activate_this = '/var/www/Invoice-Extractor/env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
from app import app as application