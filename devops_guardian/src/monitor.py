import json
import logging
from pathlib import Path

import aiohttp
import psutil

from .backup import make_backup
from .config_loader import read_config

logger = logging.getLogger(__name__)

current_dir = Path(__file__).resolve()
logs_dir = current_dir.parent.parent / 'logs'

project_drive = current_dir.anchor

async def get_system_metrics():
    CPU_load = psutil.cpu_percent(interval=0.1)
    VM_percent = psutil.virtual_memory().percent
    DISK_percent = psutil.disk_usage(project_drive).percent

    return {
        "cpu": CPU_load,
        "ram": VM_percent,
        "disk": DISK_percent
    }

async def send_message_to_telegram(data):
    config = read_config()

    token = config['BOT_TOKEN']
    id = config['CHAT_ID']

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': id,
        'text': data,
        'parse_mode': 'MarkdownV2'
    }

    try:
        async with aiohttp.ClientSession() as session, session.post(url, json=payload) as response:
            if response.status == 200:
                logger.info('Log sent to Telegram.')
            else:
                error = await response.text()
                logger.warning(f'Error of sending Telegram API: {response.status} - {error}')
    except aiohttp.ClientError as e:
        logger.warning(f'Could not connect to Telegram: {e}')

async def run_cli():
    metrics = await get_system_metrics()
    backup = make_backup()
    if backup is not None:
        status = 'SUCCESS'
        archive_size = round(backup.stat().st_size / (1024 * 1024), 2)
    else:
        status = 'ERROR'
        archive_size = 0

    data_to_send = {"backup_status": status, "archive_size_mb": archive_size, "system_metrics": metrics}
    json_string = json.dumps(data_to_send, ensure_ascii=False, indent=2)

    formatted_message = f"```json\n{json_string}\n```"

    await send_message_to_telegram(formatted_message)

async def run_bot():
    from .bot import run_telegram_bot

    await run_telegram_bot()