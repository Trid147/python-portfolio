import asyncio
import logging
from pathlib import Path

from telebot.async_telebot import AsyncTeleBot

from .config_loader import read_config
from .monitor import get_system_metrics

logger = logging.getLogger(__name__)

config = read_config()

access_token = config['BOT_TOKEN']
admin_id = config['CHAT_ID']

current_dir = Path(__file__).resolve()
logs_dir = current_dir.parent.parent / 'logs'

bot = AsyncTeleBot(access_token)

#decorator for security
def admin_only(hander_func):
    """Decorator whick accepts messages only from admin"""
    async def wrapper(message, *args, **kwargs):
        if message.chat.id == admin_id:
            logger.warning(f'Unathorized access attempt from ID: {message.chat.id}')
            return
        return await hander_func(message, *args, **kwargs)
    return wrapper

@bot.message_handler(commands=['start', 'help'])
@admin_only
async def send_welcome(message):
    await bot.reply_to(message, "Hello! I am DevOps guardian.\nCommands:\nstatus - metrics\nlogs - last logs")

@bot.message_handler(commands=['status'])
@admin_only
async def send_status(message):
    metrics = await get_system_metrics()
    text = (
        f"📊 *Current server metrics:*\n\n"
        f"💻 CPU: `{metrics['cpu']}%`\n"
        f"💾 RAM: `{metrics['ram']}%`\n"
        f"💽 DISK: `{metrics['disk']}%`"
    )
    await bot.send_message(message.chat.id, text, parse_mode='MarkdownV2')

@bot.message_handler(commands=['logs'])
@admin_only
async def send_logs(message):
    matching_lines = []

    for file in logs_dir.iterdir():
        for line in file.read_text(encoding='utf-8').splitlines():
            if 'ERROR' in line or 'WARNING' in line:
                matching_lines.append(line)

        for line in matching_lines:
            await bot.send_message(message.chat.id, line)

async def watch_dog():
    """Background task which tests the server every 30 seconds"""
    logger.info('Background monitoring Watchdog is started.')
    while True:
        try:
            metrics = await get_system_metrics()

            if metrics['cpu'] > 90:
                await bot.send_message(admin_id, f'⚠️ *ALERT:* Critical CPU load: `{metrics['cpu']}%!`', parse_mode='MarkdownV2')

            if metrics['ram'] > 90:
                await bot.send_message(admin_id, f'⚠️ *ALERT:* Critical RAM load: `{metrics['ram']}%`!', parse_mode='MarkdownV2')

            if metrics['disk'] > 90:
                await bot.send_message(admin_id, f'⚠️ *ALERT:* Running out of disk space: `{metrics['disk']}%!`', parse_mode='MarkdownV2')

        except Exception:
            logger.exception('An error occured in Watchdog cycle.')

        await asyncio.sleep(30)

async def run_telegram_bot():
    logger.info('Starting Telegram bot...')

    asyncio.create_task(watch_dog())

    await bot.polling(non_stop=True)