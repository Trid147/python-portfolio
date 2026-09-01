import datetime
import logging
import shutil
import sys
import time
from pathlib import Path

from .config_loader import read_config

logger = logging.getLogger(__name__)

current_dir = Path(__file__).resolve()
logs_dir = current_dir.parent.parent / 'logs'
backups_dir = current_dir.parent.parent / 'backups'

backup_name = f'backup_{datetime.datetime.now(datetime.timezone.utc).date()}'

def clear_old_logs():
    config = read_config()
    retention = config["BACKUP_RETENTION"]

    for file in backups_dir.iterdir():
        create_time = file.stat().st_mtime
        
        if time.time() - create_time >= 86400 * retention:
            try:
                file.unlink()
            except PermissionError:
                logger.error('Access error!')
                sys.exit()

def make_backup():
    try:
        log_files = [f for f in logs_dir.iterdir() if f.is_file() and f.suffix.lower() == '.log']

        if not log_files:
            logger.error('No .log files found to backup.')
            return None

        temp_dir = backups_dir / f'temp_{backup_name}'
        temp_dir.mkdir(parents=True, exist_ok=True)

        for file in log_files:
            destination = temp_dir / file.name
            shutil.copy2(file, destination)

        archive = shutil.make_archive(base_name=str(backups_dir / backup_name), format='zip', root_dir=str(temp_dir))
        shutil.rmtree(temp_dir)
        logger.info('Backup successfully created!')

        return Path(archive)
        
    except FileNotFoundError:
        logger.error('Logs directory is not found.')
        sys.exit(1)