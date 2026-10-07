import subprocess
import sys
from pathlib import Path
from scanner import scan_line

# ANSI codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def get_staged_files():
    '''gets list of files which were added to git'''
    try:
        result = subprocess.run(['git', 'diff', '--name-only', '--cached'], capture_output=True, text=True, check=True)
        if result:
            files = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            return files
    except subprocess.CalledProcessError:
        print('Could not find added files. Are you inside the reposiroty?')
        return []

def main():
    print('Secret Shield started...')

    staged_files = get_staged_files()

    if not staged_files:
        print('No files to check.')
        sys.exit(0)

    has_secrets = False

    for file in staged_files:
        file_path = Path(file)

        if not file_path.exists():
            continue

        print(f'Scanning {file_path}...')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for number, line in enumerate(f, start=1):
                    result = scan_line(line)
                    if result:
                        print(f'{YELLOW}{BOLD}[String: {number}] [{result['type']}] [{result['reason']}]{RESET}')
                        print(f'{YELLOW}{BOLD}Text: {line.strip()}{RESET}')
                        has_secrets = True
        except Exception as e:
            print(f'Could not read file {file_path}: {e}')
    
    if has_secrets:
        print(f'\n{RED}{BOLD}[-] Secrets found. Commit not commited.{RESET}')
        sys.exit(1)
    else:
        print(f'\n{GREEN}{BOLD}[+] No secrets found. Commit commited.{RESET}')
        sys.exit(0)

if __name__ == '__main__':
    main()