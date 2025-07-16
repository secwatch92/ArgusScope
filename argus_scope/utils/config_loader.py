import os
from dotenv import load_dotenv
import yaml
from pathlib import Path

load_dotenv()

def load_config(env='dev'):
    config_path = Path(__file__).parent.parent / 'config' / f'{env}.yaml'
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    config['database']['url'] = os.getenv('DATABASE_URL', config['database']['url'])
    config['elasticsearch']['url'] = os.getenv('ELASTICSEARCH_URL', config['elasticsearch']['url'])
    
    return config
