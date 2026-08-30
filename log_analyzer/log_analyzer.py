import argparse
import os
import re
import sys
from pathlib import Path


def check_root():
    if os.getuid() != 0:
        print('Script do not have root rights.')
        sys.exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Linux authefication log analyzer')

    parser.add_argument('--log', type=str, default='test_auth.txt', help='log file path')

    parser.add_argument('--limit', type=int, default=5, help='limit of unsuccessful attempts')

    return parser.parse_args()

def analyze_log(log_path, limit):
    print(f'Starting analysis of: {log_path}')
    path = Path(log_path)

    if not path.exists():
        print('Log file does not exist')
        sys.exit(1)

    success_count = 0
    failure_count = 0

    failed_ips = {}

    ip_regex = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            if 'Accepted' in line:
                success_count += 1
            elif 'Failed' in line:
                failure_count += 1

                ip_match = re.search(ip_regex, line)

                if ip_match:
                    ip = ip_match.group()

                    if ip in failed_ips:
                        failed_ips[ip] += 1
                    else:
                        failed_ips[ip] = 1
    
    print(f'\nAnalysis result:\nSuccessful attempts: {success_count}\nFailed attempts: {failure_count}')

    print('\nSuspicious IPs:')
    for ip, attempts in failed_ips.items():
        if attempts >= limit:
            print(f'IP: {ip}\nAttempts: {attempts}')


if __name__ == '__main__':
    check_root()

    args = parse_arguments()
    analyze_log(args.log, args.limit)