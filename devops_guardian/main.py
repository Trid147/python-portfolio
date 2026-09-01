import argparse
import asyncio
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("app.log", encoding="utf-8"),logging.StreamHandler(sys.stdout),],
)

from src.config_loader import read_config
from src.monitor import run_bot, run_cli

config = read_config()

async def init():
    parser = argparse.ArgumentParser(description='DevOps Monitoring & Backup Tool')
    parser.add_argument('--mode', choices=['cli', 'bot'], required=True, help='Run as disposable script or constant Telegram bot')

    args = parser.parse_args()

    if args.mode == 'cli':
        await run_cli()
    elif args.mode == 'bot':
        await run_bot()

if __name__ == '__main__':
    try:
        asyncio.run(init())
    except KeyboardInterrupt:
        sys.exit(0)