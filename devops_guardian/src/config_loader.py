import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

current_dir = Path(__file__).resolve()
config_path = current_dir.parent.parent / 'config.json'

def read_config():
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            logger.info('Config successully loaded.')
            return json.load(file)
    except FileNotFoundError:
        logger.error(f'Could not find config.json at {config_path}!')
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error('config.json contains invalid JSON syntax!')
        sys.exit(1)