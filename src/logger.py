# src/logger.py
import logging
import os
from datetime import datetime

# Create logs directory relative to THIS file, not the current working dir.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = datetime.now().strftime('%m_%d_%Y_%H_%M_%S') + '.log'
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format='[ %(asctime)s ] %(name)s:%(lineno)d - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, mode='w', encoding='utf-8'),  # Changed to 'w' to ensure fresh file
        logging.StreamHandler()
    ],
    force=True
)

# Get the root logger (or use logging directly)
logger = logging.getLogger()  # Changed from __name__ to get root logger

if __name__ == '__main__':
    print(f'Writing logs to: {LOG_PATH}')
    logger.info('Logging has started')
    # Force flush to ensure it's written
    for handler in logger.handlers:
        handler.flush()