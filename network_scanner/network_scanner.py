import asyncio
import time
from pathlib import Path

import aiohttp
from colorama import Fore, Style, init

init(autoreset=True)

hosts_dir = Path('hosts.txt')
ports = [53, 80, 443]

def load_hosts():
    hosts = []
    with open(hosts_dir, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            hosts.append(line)
        return hosts

async def check_port(host, port, timeout=2.0) -> tuple:
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return port, True
    except Exception:
        return port, False

async def check_host(semaphore, session, host):
    async with semaphore:
        start_time = time.time()

        url = f'https://{host}' if not host.replace('.', '').isdigit() else f'http://{host}'

        output = []

        try:
            async with session.get(url, timeout=5) as response:
                latency = round((time.time() - start_time) * 1000)
                output.append(f'\n{Fore.GREEN}ONLINE: {url}')
                output.append(f'\nStatus: {response.status}')
                output.append(f'\nLatency: {latency}')

        except Exception as e:
            output.append(f'\n{Fore.RED}OFFLINE: {url}')
            output.append(f'\nError: {type(e).__name__}')

        port_tasks = [check_port(host, port) for port in ports]
        port_results = await asyncio.gather(*port_tasks)

        for port, is_open in port_results:
            status = f'{Fore.GREEN}OPEN{Style.RESET_ALL}' if is_open else f'{Fore.RED}CLOSED{Style.RESET_ALL}'
            output.append(f'\n{Fore.CYAN}Port: {port}')
            output.append(f'\n Status: {status}')

        print(''.join(output))

async def main():
    hosts = load_hosts()
    if not hosts:
        return

    semaphore = asyncio.Semaphore(10)

    async with aiohttp.ClientSession() as session:
        tasks = [check_host(semaphore, session, host) for host in hosts]

        await asyncio.gather(*tasks)

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(f'\nScan is fully completed after: {round(time.time() - start_time)} seconds')